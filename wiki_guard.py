"""wiki_guard.py — Invisible infrastructure for the School PKM Wiki.

Silently enforces wiki quality rules so Claude Code doesn't have to remember them.
Like Apple's ISP in a camera pipeline: the user never sees it, but every output is better.

Subcommands (run via `python wiki_guard.py <cmd>`):
  cache-check    — compare raw/ files against ingest cache, print new/changed/unchanged
  cache-update   — mark a file as ingested (store its SHA256 in the cache)
  slug-check     — verify a slug is unique before creating a wiki page
  slug-register  — register a new slug after page creation
  validate       — validate frontmatter, required fields, confidence, provenance
  lint-quick     — fast structural check: broken links, orphans, near-duplicates
  init           — initialize cache and slug registry from current wiki state

Uses ONLY Python stdlib — no pip install required.
"""

import hashlib
import json
import re
import sys
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

# ---------------------------------------------------------------------------
# Path constants (overridden in tests via monkeypatch)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
CACHE_FILE = ROOT / ".ingest_cache.json"
SLUGS_FILE = ROOT / ".slug_registry.json"


# ---------------------------------------------------------------------------
# Cache functions
# ---------------------------------------------------------------------------

def file_hash(path: Path) -> str:
    """Return the SHA256 hex digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def load_cache() -> dict:
    """Load the ingest cache from disk. Returns {} if no cache file exists."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    """Write the ingest cache to disk as JSON."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def cache_check() -> None:
    """Compare raw/ files against the cache. Print status for each file.

    Status labels:
      NEW       — file not in cache (never ingested)
      CHANGED   — file hash differs from cached value (re-ingest needed)
      unchanged — file hash matches cache (no action needed)
    """
    cache = load_cache()
    files = sorted(RAW_DIR.rglob("*"))
    files = [f for f in files if f.is_file() and not f.name.startswith(".")]

    for filepath in files:
        rel = str(filepath.relative_to(ROOT))
        current_hash = file_hash(filepath)

        if rel not in cache:
            print(f"  NEW       {rel}")
        elif cache[rel] != current_hash:
            print(f"  CHANGED   {rel}")
        else:
            print(f"  unchanged {rel}")


def cache_update(filepath: str) -> None:
    """Mark a file as ingested by storing its current hash in the cache."""
    path = Path(filepath)
    if not path.is_absolute():
        path = ROOT / path
    cache = load_cache()
    rel = str(path.relative_to(ROOT))
    cache[rel] = file_hash(path)
    save_cache(cache)


# ---------------------------------------------------------------------------
# Slug registry functions
# ---------------------------------------------------------------------------

def load_slugs() -> dict:
    """Load the slug registry from disk. Returns {} if no file exists."""
    if SLUGS_FILE.exists():
        with open(SLUGS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_slugs(slugs: dict) -> None:
    """Write the slug registry to disk as JSON."""
    with open(SLUGS_FILE, "w") as f:
        json.dump(slugs, f, indent=2)


def normalize_slug(name: str) -> str:
    """Convert a concept name to a deterministic slug.

    Lowercase, replace non-alphanum with underscores, collapse runs,
    strip leading/trailing underscores.
    """
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug


def find_similar_slugs(
    candidate: str, slugs: dict, threshold: float = 0.55
) -> list[tuple[str, str, float]]:
    """Return existing slugs similar to *candidate* above *threshold*.

    Returns list of (slug, title, ratio) sorted by ratio descending.
    """
    matches = []
    for slug, title in slugs.items():
        ratio = SequenceMatcher(None, candidate, slug).ratio()
        if ratio >= threshold:
            matches.append((slug, title, ratio))
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches


def slug_check(slug: str) -> None:
    """Check if a slug exists or has near-duplicates. Print guidance."""
    slugs = load_slugs()

    if slug in slugs:
        print(f"  EXACT MATCH  {slug} → \"{slugs[slug]}\"")
        print(f"  Do NOT create a new one. Update the existing page.")
        return

    similar = find_similar_slugs(slug, slugs)
    if similar:
        print(f"  SIMILAR  Found similar slugs for \"{slug}\":")
        for s, title, ratio in similar:
            print(f"    {s} → \"{title}\" (similarity: {ratio:.0%})")
        print(f"  Consider updating an existing page instead.")
        return

    print(f"  NEW SLUG  \"{slug}\" is unique. Safe to create.")


def slug_register(slug: str, title: str) -> None:
    """Register a new slug. Warn if similar exists, but register anyway."""
    slugs = load_slugs()

    if slug in slugs:
        print(f"  ALREADY EXISTS  {slug} → \"{slugs[slug]}\"")
        return

    similar = find_similar_slugs(slug, slugs)
    if similar:
        print(f"  WARNING  Similar slugs exist:")
        for s, t, ratio in similar:
            print(f"    {s} → \"{t}\" (similarity: {ratio:.0%})")

    slugs[slug] = title
    save_slugs(slugs)
    print(f"  REGISTERED  {slug} → \"{title}\"")


# ---------------------------------------------------------------------------
# Frontmatter validation functions
# ---------------------------------------------------------------------------

REQUIRED_FRONTMATTER = {"title", "course", "tags", "sources", "confidence", "last_updated"}
VALID_CONFIDENCE = {"low", "medium", "high"}

# System files that skip slug registry checks
_SYSTEM_FILES = {"index.md", "log.md", "gaps.md"}


def parse_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content.

    Simple key:value parsing using string splitting — no PyYAML dependency.
    Returns a dict of frontmatter fields, or None if no frontmatter block found.
    """
    stripped = content.strip()
    if not stripped.startswith("---"):
        return None

    # Find the closing --- (skip the opening one)
    end = stripped.find("---", 3)
    if end == -1:
        return None

    block = stripped[3:end].strip()
    if not block:
        return None

    result = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        result[key] = value

    return result if result else None


def validate_file(filepath: Path) -> list[str]:
    """Validate a single wiki page. Returns list of error strings.

    Checks:
      1. Frontmatter exists
      2. All required fields present
      3. Confidence value is valid (low/medium/high)
      4. Slug (filename stem) exists in slug registry (skipped for system files)
      5. Provenance labels (<!-- source: ... -->) exist in body (if body > 100 chars)
    """
    filepath = Path(filepath)
    errors: list[str] = []

    content = filepath.read_text(encoding="utf-8")

    # 1. Frontmatter exists
    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(f"{filepath.name}: missing frontmatter block")
        return errors  # Can't check fields without frontmatter

    # 2. All required fields present
    missing = REQUIRED_FRONTMATTER - set(fm.keys())
    if missing:
        for field in sorted(missing):
            errors.append(f"{filepath.name}: missing required field '{field}'")

    # 3. Confidence value is valid
    if "confidence" in fm and fm["confidence"] not in VALID_CONFIDENCE:
        errors.append(
            f"{filepath.name}: invalid confidence '{fm['confidence']}' "
            f"(must be one of: {', '.join(sorted(VALID_CONFIDENCE))})"
        )

    # 4. Slug check (skip system files)
    if filepath.name not in _SYSTEM_FILES:
        slug = filepath.stem
        slugs = load_slugs()
        if slug not in slugs:
            errors.append(f"{filepath.name}: slug '{slug}' not in registry")

    # 5. Provenance labels in body (if body > 100 chars)
    # Body is everything after the closing --- of frontmatter
    stripped = content.strip()
    second_fence = stripped.find("---", 3)
    if second_fence != -1:
        body = stripped[second_fence + 3:]
        if len(body) > 100 and "<!-- source:" not in body:
            errors.append(f"{filepath.name}: missing provenance label (<!-- source: ... -->)")

    return errors


def validate(filepath: str | None = None) -> None:
    """Validate one file or all wiki pages. Prints PASS/FAIL per file, exits 1 on errors."""
    all_errors: list[str] = []

    if filepath:
        path = Path(filepath)
        if not path.is_absolute():
            path = WIKI_DIR / path
        errors = validate_file(path)
        all_errors.extend(errors)
        if errors:
            print(f"  FAIL  {path.name}")
            for e in errors:
                print(f"         {e}")
        else:
            print(f"  PASS  {path.name}")
    else:
        # Validate all .md files in wiki/
        pages = sorted(WIKI_DIR.rglob("*.md"))
        for page in pages:
            errors = validate_file(page)
            all_errors.extend(errors)
            if errors:
                print(f"  FAIL  {page.relative_to(WIKI_DIR)}")
                for e in errors:
                    print(f"         {e}")
            else:
                print(f"  PASS  {page.relative_to(WIKI_DIR)}")

    if all_errors:
        sys.exit(1)


# ---------------------------------------------------------------------------
# lint_quick — fast structural wiki check
# ---------------------------------------------------------------------------

def lint_quick() -> None:
    """Fast structural check: broken links, orphans, near-duplicates, unregistered slugs.

    Scans all .md files under wiki/ (excluding system files and dotfiles).
    Prints a report with counts for each issue category.
    """
    # Collect all wiki pages (skip system files and dotfiles)
    pages: list[Path] = []
    for p in sorted(WIKI_DIR.rglob("*.md")):
        if p.name.startswith("."):
            continue
        if p.name in _SYSTEM_FILES:
            continue
        pages.append(p)

    # Build slug-to-path map and read all content
    slug_to_path: dict[str, Path] = {}
    page_contents: dict[str, str] = {}  # stem -> content
    all_slugs: set[str] = set()

    for p in pages:
        stem = p.stem
        all_slugs.add(stem)
        slug_to_path[stem] = p
        page_contents[stem] = p.read_text(encoding="utf-8")

    # 1. BROKEN LINKS — [[wikilinks]] pointing to pages that don't exist
    broken_links: list[tuple[str, str]] = []  # (source_page, target)
    # Also track all inbound links for orphan detection
    inbound: dict[str, set[str]] = {s: set() for s in all_slugs}

    for stem, content in page_contents.items():
        targets = re.findall(r"\[\[([^\]]+)\]\]", content)
        for target in targets:
            target_slug = normalize_slug(target)
            if target_slug in all_slugs:
                inbound[target_slug].add(stem)
            else:
                broken_links.append((stem, target))

    # 2. ORPHAN PAGES — pages with no inbound links
    orphans = [s for s in sorted(all_slugs) if not inbound[s]]

    # 3. NEAR-DUPLICATE SLUGS — pairs with SequenceMatcher ratio >= 0.80
    near_dupes: list[tuple[str, str, float]] = []
    slug_list = sorted(all_slugs)
    for i, a in enumerate(slug_list):
        for b in slug_list[i + 1:]:
            ratio = SequenceMatcher(None, a, b).ratio()
            if ratio >= 0.80:
                near_dupes.append((a, b, ratio))

    # 4. UNREGISTERED SLUGS — pages not in .slugs.json
    registry = load_slugs()
    unregistered = [s for s in sorted(all_slugs) if s not in registry]

    # Print report
    total_issues = 0

    if broken_links:
        total_issues += len(broken_links)
        print(f"BROKEN LINKS ({len(broken_links)}):")
        for source, target in broken_links:
            print(f"  {source}.md → [[{target}]]")
        print()

    if orphans:
        total_issues += len(orphans)
        print(f"ORPHAN PAGES ({len(orphans)}):")
        for s in orphans:
            print(f"  {s}.md")
        print()

    if near_dupes:
        total_issues += len(near_dupes)
        print(f"NEAR-DUPLICATE SLUGS ({len(near_dupes)}):")
        for a, b, ratio in near_dupes:
            print(f"  {a} ↔ {b} ({ratio:.0%})")
        print()

    if unregistered:
        total_issues += len(unregistered)
        print(f"UNREGISTERED SLUGS ({len(unregistered)}):")
        for s in unregistered:
            print(f"  {s}")
        print()

    if total_issues == 0:
        print("lint-quick: all clear ✓")
    else:
        print(f"lint-quick: {total_issues} issue(s) found")


# ---------------------------------------------------------------------------
# init — build slug registry + ingest cache from existing state
# ---------------------------------------------------------------------------

def init() -> None:
    """Build slug registry and ingest cache from existing wiki/ and raw/ files.

    Scans wiki/*.md for pages (skipping system files), extracts title from
    frontmatter, and registers each slug. Scans raw/ files, computes SHA256,
    and populates the ingest cache.
    """
    # --- Slug registry ---
    existing_slugs = load_slugs()
    newly_registered = 0

    pages = sorted(WIKI_DIR.rglob("*.md"))
    for p in pages:
        if p.name.startswith("."):
            continue
        if p.name in _SYSTEM_FILES:
            continue

        slug = p.stem
        if slug not in existing_slugs:
            # Try to extract title from frontmatter
            content = p.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            if fm and "title" in fm:
                title = fm["title"]
            else:
                title = slug.replace("_", " ").title()
            existing_slugs[slug] = title
            newly_registered += 1

    save_slugs(existing_slugs)
    print(f"Slug registry: {len(existing_slugs)} total ({newly_registered} newly registered)")

    # --- Ingest cache ---
    existing_cache = load_cache()
    newly_cached = 0

    if RAW_DIR.exists():
        raw_files = sorted(RAW_DIR.rglob("*"))
        raw_files = [f for f in raw_files if f.is_file() and not f.name.startswith(".")]

        for filepath in raw_files:
            rel = str(filepath.relative_to(ROOT))
            if rel not in existing_cache:
                existing_cache[rel] = file_hash(filepath)
                newly_cached += 1

    save_cache(existing_cache)
    print(f"Ingest cache: {len(existing_cache)} total ({newly_cached} newly cached)")


# ---------------------------------------------------------------------------
# CLI dispatcher
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python wiki_guard.py <subcommand>")
        print("Subcommands: cache-check, cache-update <file>, slug-check <slug>,")
        print("             slug-register <slug> <title>, validate [file],")
        print("             lint-quick, init")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "cache-check":
        cache_check()
    elif cmd == "cache-update":
        if len(sys.argv) < 3:
            print("Usage: python wiki_guard.py cache-update <filepath>")
            sys.exit(1)
        cache_update(sys.argv[2])
    elif cmd == "slug-check":
        if len(sys.argv) < 3:
            print("Usage: python wiki_guard.py slug-check <slug>")
            sys.exit(1)
        slug_check(sys.argv[2])
    elif cmd == "slug-register":
        if len(sys.argv) < 4:
            print("Usage: python wiki_guard.py slug-register <slug> <title>")
            sys.exit(1)
        slug_register(sys.argv[2], sys.argv[3])
    elif cmd == "validate":
        validate(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "lint-quick":
        lint_quick()
    elif cmd == "init":
        init()
    else:
        print(f"Unknown subcommand: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
