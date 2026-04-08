"""Tests for wiki_guard.py — cache + slug registry modules."""

import importlib
import json
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Fixture: isolated project tree inside tmp_path
# ---------------------------------------------------------------------------

@pytest.fixture()
def project(tmp_path, monkeypatch):
    """Set up a fake project tree and reload wiki_guard with overridden paths."""
    raw_dir = tmp_path / "raw"
    wiki_dir = tmp_path / "wiki"
    raw_dir.mkdir()
    wiki_dir.mkdir()

    # Ensure the module can be imported from the repo root
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    import wiki_guard

    # Override module-level path constants to point at tmp_path
    monkeypatch.setattr(wiki_guard, "ROOT", tmp_path)
    monkeypatch.setattr(wiki_guard, "RAW_DIR", raw_dir)
    monkeypatch.setattr(wiki_guard, "WIKI_DIR", wiki_dir)
    monkeypatch.setattr(wiki_guard, "CACHE_FILE", tmp_path / ".ingest_cache.json")
    monkeypatch.setattr(wiki_guard, "SLUGS_FILE", tmp_path / ".slugs.json")

    return {
        "tmp": tmp_path,
        "raw": raw_dir,
        "wiki": wiki_dir,
        "mod": wiki_guard,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFileHash:
    """file_hash() produces deterministic SHA256 hex digests."""

    def test_file_hash_deterministic(self, project):
        """Same content always yields the same 64-char hex hash."""
        wg = project["mod"]
        f = project["raw"] / "note.txt"
        f.write_text("hello world")

        h1 = wg.file_hash(f)
        h2 = wg.file_hash(f)

        assert h1 == h2
        assert len(h1) == 64
        assert all(c in "0123456789abcdef" for c in h1)

    def test_file_hash_changes_with_content(self, project):
        """Different content produces a different hash."""
        wg = project["mod"]
        f = project["raw"] / "note.txt"

        f.write_text("version 1")
        h1 = wg.file_hash(f)

        f.write_text("version 2")
        h2 = wg.file_hash(f)

        assert h1 != h2


class TestCacheRoundtrip:
    """load_cache / save_cache preserve data through JSON."""

    def test_cache_roundtrip(self, project):
        """save_cache then load_cache returns the same dict."""
        wg = project["mod"]
        data = {"raw/neu/lecture1.pdf": "abc123", "raw/neu/lecture2.pdf": "def456"}

        wg.save_cache(data)
        loaded = wg.load_cache()

        assert loaded == data

    def test_load_cache_returns_empty_when_missing(self, project):
        """load_cache returns {} when no cache file exists."""
        wg = project["mod"]
        assert wg.load_cache() == {}


class TestCacheCheck:
    """cache_check() compares raw/ files against the cache."""

    def test_cache_check_new_file(self, project, capsys):
        """A file not in the cache shows as NEW."""
        wg = project["mod"]
        neu = project["raw"] / "neu"
        neu.mkdir()
        (neu / "lecture.pdf").write_bytes(b"pdf content")

        wg.cache_check()

        out = capsys.readouterr().out
        assert "NEW" in out
        assert "lecture.pdf" in out

    def test_cache_check_unchanged(self, project, capsys):
        """A file whose hash matches the cache shows as unchanged."""
        wg = project["mod"]
        neu = project["raw"] / "neu"
        neu.mkdir()
        f = neu / "lecture.pdf"
        f.write_bytes(b"pdf content")

        # Simulate prior ingest: store its hash in the cache
        rel = str(f.relative_to(project["tmp"]))
        wg.save_cache({rel: wg.file_hash(f)})

        wg.cache_check()

        out = capsys.readouterr().out
        assert "unchanged" in out.lower()
        assert "lecture.pdf" in out

    def test_cache_check_changed_file(self, project, capsys):
        """A file whose content changed since caching shows as CHANGED."""
        wg = project["mod"]
        neu = project["raw"] / "neu"
        neu.mkdir()
        f = neu / "lecture.pdf"
        f.write_bytes(b"original content")

        # Cache with original hash
        rel = str(f.relative_to(project["tmp"]))
        wg.save_cache({rel: wg.file_hash(f)})

        # Modify the file
        f.write_bytes(b"updated content")

        wg.cache_check()

        out = capsys.readouterr().out
        assert "CHANGED" in out
        assert "lecture.pdf" in out


# ---------------------------------------------------------------------------
# Slug registry tests
# ---------------------------------------------------------------------------

class TestNormalizeSlug:
    """normalize_slug() converts concept names to deterministic slugs."""

    def test_normalize_slug_basic(self, project):
        """Simple names: lowercase, spaces to underscores."""
        wg = project["mod"]
        assert wg.normalize_slug("Retina") == "retina"
        assert wg.normalize_slug("Action Potential") == "action_potential"

    def test_normalize_slug_strips_junk(self, project):
        """Strips leading/trailing whitespace, underscores, and non-alphanum chars."""
        wg = project["mod"]
        assert wg.normalize_slug("  __retina__  ") == "retina"
        assert wg.normalize_slug("pain & modulation!") == "pain_modulation"


class TestFindSimilarSlugs:
    """find_similar_slugs() uses SequenceMatcher for fuzzy matching."""

    def test_find_similar_slugs(self, project):
        """'retina_circuit' should match 'retina' but not 'hippocampus'."""
        wg = project["mod"]
        existing = {"retina": "Retina", "hippocampus": "Hippocampus"}
        matches = wg.find_similar_slugs("retina_circuit", existing, threshold=0.5)
        slugs_found = [m[0] for m in matches]
        assert "retina" in slugs_found
        assert "hippocampus" not in slugs_found


class TestSlugCheck:
    """slug_check() prints guidance about slug collisions."""

    def test_slug_check_exact_match(self, project, capsys):
        """Existing slug prints EXACT MATCH and 'Do NOT create a new one'."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        wg.slug_check("retina")

        out = capsys.readouterr().out
        assert "EXACT MATCH" in out
        assert "Do NOT create a new one" in out

    def test_slug_check_similar(self, project, capsys):
        """Near-duplicate slug prints 'similar slugs'."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        wg.slug_check("retina_circuit")

        out = capsys.readouterr().out
        assert "similar" in out.lower()

    def test_slug_check_new(self, project, capsys):
        """Totally new slug prints NEW SLUG."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        wg.slug_check("hippocampus")

        out = capsys.readouterr().out
        assert "NEW SLUG" in out


class TestSlugRegister:
    """slug_register() adds a slug and persists it."""

    def test_slug_register(self, project, capsys):
        """Registering a slug persists it to the JSON file."""
        wg = project["mod"]
        # Start with empty registry
        wg.save_slugs({})

        wg.slug_register("retina", "Retina")

        slugs = wg.load_slugs()
        assert "retina" in slugs
        assert slugs["retina"] == "Retina"


class TestSlugRegistryRoundtrip:
    """save_slugs / load_slugs preserve data through JSON."""

    def test_slug_registry_roundtrip(self, project):
        """save_slugs then load_slugs returns the same dict."""
        wg = project["mod"]
        data = {"retina": "Retina", "hippocampus": "Hippocampus"}

        wg.save_slugs(data)
        loaded = wg.load_slugs()

        assert loaded == data


# ---------------------------------------------------------------------------
# Frontmatter validation tests
# ---------------------------------------------------------------------------

VALID_PAGE = """\
---
title: Retina
course: neu
tags: [vision, retina]
sources: [01_20 Intro.pdf]
confidence: medium
last_updated: 2026-04-07
---

The retina is the light-sensitive tissue lining the inner surface of the eye.

<!-- source: 01_20 Intro.pdf -->

Photoreceptors (rods and cones) convert light into electrical signals
that are processed by retinal circuits before being sent to the brain
via the optic nerve. This is a long enough body to trigger provenance checks.
"""

PAGE_NO_FRONTMATTER = """\
# Retina

The retina is the light-sensitive tissue lining the inner surface of the eye.
"""

PAGE_MISSING_FIELDS = """\
---
title: Retina
tags: [vision]
sources: [01_20 Intro.pdf]
last_updated: 2026-04-07
---

Short body.
"""

PAGE_BAD_CONFIDENCE = """\
---
title: Retina
course: neu
tags: [vision]
sources: [01_20 Intro.pdf]
confidence: very-high
last_updated: 2026-04-07
---

Short body.
"""

PAGE_MISSING_PROVENANCE = """\
---
title: Retina
course: neu
tags: [vision, retina]
sources: [01_20 Intro.pdf]
confidence: medium
last_updated: 2026-04-07
---

The retina is the light-sensitive tissue lining the inner surface of the eye.
Photoreceptors (rods and cones) convert light into electrical signals
that are processed by retinal circuits before being sent to the brain
via the optic nerve. This is a long enough body to trigger provenance checks.
"""


class TestParseFrontmatter:
    """parse_frontmatter() extracts YAML frontmatter from markdown."""

    def test_parse_frontmatter_valid(self, project):
        """Extracts title, course, confidence from valid frontmatter."""
        wg = project["mod"]
        fm = wg.parse_frontmatter(VALID_PAGE)

        assert fm is not None
        assert fm["title"] == "Retina"
        assert fm["course"] == "neu"
        assert fm["confidence"] == "medium"

    def test_parse_frontmatter_missing(self, project):
        """Returns None for content without frontmatter."""
        wg = project["mod"]
        fm = wg.parse_frontmatter(PAGE_NO_FRONTMATTER)

        assert fm is None


class TestValidateFile:
    """validate_file() returns a list of error strings for a wiki page."""

    def test_validate_file_good(self, project):
        """No errors on valid page with all fields + provenance."""
        wg = project["mod"]
        # Register the slug so it passes the slug check
        wg.save_slugs({"retina": "Retina"})

        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(VALID_PAGE)

        errors = wg.validate_file(f)
        assert errors == []

    def test_validate_file_missing_frontmatter(self, project):
        """Catches missing frontmatter."""
        wg = project["mod"]
        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(PAGE_NO_FRONTMATTER)

        errors = wg.validate_file(f)
        assert any("frontmatter" in e.lower() for e in errors)

    def test_validate_file_missing_fields(self, project):
        """Catches missing course and confidence fields."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(PAGE_MISSING_FIELDS)

        errors = wg.validate_file(f)
        error_text = " ".join(errors).lower()
        assert "course" in error_text
        assert "confidence" in error_text

    def test_validate_file_bad_confidence(self, project):
        """Catches 'very-high' as invalid confidence value."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(PAGE_BAD_CONFIDENCE)

        errors = wg.validate_file(f)
        assert any("confidence" in e.lower() for e in errors)
        assert any("very-high" in e for e in errors)

    def test_validate_file_missing_provenance(self, project):
        """Catches missing provenance labels on long body."""
        wg = project["mod"]
        wg.save_slugs({"retina": "Retina"})

        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(PAGE_MISSING_PROVENANCE)

        errors = wg.validate_file(f)
        assert any("provenance" in e.lower() for e in errors)

    def test_validate_file_unregistered_slug(self, project):
        """Catches slug not in registry."""
        wg = project["mod"]
        # Empty slug registry — 'retina' not registered
        wg.save_slugs({})

        page = project["wiki"] / "neu"
        page.mkdir()
        f = page / "retina.md"
        f.write_text(VALID_PAGE)

        errors = wg.validate_file(f)
        assert any("slug" in e.lower() for e in errors)
        assert any("retina" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# lint_quick tests
# ---------------------------------------------------------------------------

PAGE_WITH_LINKS = """\
---
title: Retina
course: neu
tags: [vision]
sources: [intro.pdf]
confidence: medium
last_updated: 2026-04-07
---

The retina connects to the [[lgn]] and the [[nonexistent_page]].

<!-- source: intro.pdf -->

Extra text to make the body long enough for provenance checks if needed.
"""

PAGE_SIMPLE = """\
---
title: LGN
course: neu
tags: [vision]
sources: [intro.pdf]
confidence: medium
last_updated: 2026-04-07
---

The lateral geniculate nucleus receives input from the retina.
"""

PAGE_ORPHAN = """\
---
title: Hippocampus
course: neu
tags: [memory]
sources: [lecture3.pdf]
confidence: low
last_updated: 2026-04-07
---

The hippocampus is involved in memory formation.
"""


class TestLintQuickBrokenLink:
    """lint_quick() detects [[wikilinks]] pointing to pages that don't exist."""

    def test_lint_quick_broken_link(self, project, capsys):
        """A page linking to [[nonexistent_page]] reports BROKEN LINKS."""
        wg = project["mod"]
        neu = project["wiki"] / "neu"
        neu.mkdir()

        # retina.md links to [[lgn]] and [[nonexistent_page]]
        (neu / "retina.md").write_text(PAGE_WITH_LINKS)
        # lgn.md exists — so [[lgn]] should be fine
        (neu / "lgn.md").write_text(PAGE_SIMPLE)

        wg.lint_quick()

        out = capsys.readouterr().out
        assert "BROKEN LINKS" in out
        assert "nonexistent_page" in out


class TestLintQuickNearDuplicate:
    """lint_quick() detects near-duplicate page slugs."""

    def test_lint_quick_near_duplicate(self, project, capsys):
        """retina.md + retinal.md should report NEAR-DUPLICATE."""
        wg = project["mod"]
        neu = project["wiki"] / "neu"
        neu.mkdir()

        (neu / "retina.md").write_text(PAGE_SIMPLE.replace("LGN", "Retina"))
        (neu / "retinal.md").write_text(PAGE_SIMPLE.replace("LGN", "Retinal"))

        wg.lint_quick()

        out = capsys.readouterr().out
        assert "NEAR-DUPLICATE" in out


class TestLintQuickOrphan:
    """lint_quick() detects orphan pages (no inbound links)."""

    def test_lint_quick_orphan(self, project, capsys):
        """A page with no inbound links from any other page reports ORPHAN."""
        wg = project["mod"]
        neu = project["wiki"] / "neu"
        neu.mkdir()

        # retina links to lgn, but nobody links to hippocampus
        (neu / "retina.md").write_text(PAGE_WITH_LINKS)
        (neu / "lgn.md").write_text(PAGE_SIMPLE)
        (neu / "hippocampus.md").write_text(PAGE_ORPHAN)

        wg.lint_quick()

        out = capsys.readouterr().out
        assert "ORPHAN" in out
        assert "hippocampus" in out


# ---------------------------------------------------------------------------
# init tests
# ---------------------------------------------------------------------------

class TestInitBuildsRegistry:
    """init() builds slug registry + ingest cache from existing wiki and raw/."""

    def test_init_builds_registry(self, project, capsys):
        """Creates slugs from wiki pages and caches raw files."""
        wg = project["mod"]

        # Set up wiki pages
        neu = project["wiki"] / "neu"
        neu.mkdir()
        (neu / "retina.md").write_text(PAGE_SIMPLE.replace("LGN", "Retina"))
        (neu / "lgn.md").write_text(PAGE_SIMPLE)

        # Set up raw files
        raw_neu = project["raw"] / "neu"
        raw_neu.mkdir()
        (raw_neu / "lecture1.pdf").write_bytes(b"pdf content")
        (raw_neu / "lecture2.pdf").write_bytes(b"more pdf content")

        wg.init()

        out = capsys.readouterr().out

        # Check slug registry was built
        assert "Slug registry" in out
        slugs = wg.load_slugs()
        assert "retina" in slugs
        assert "lgn" in slugs

        # Check ingest cache was built
        assert "Ingest cache" in out
        cache = wg.load_cache()
        assert len(cache) == 2  # two raw files

    def test_init_skips_system_files(self, project, capsys):
        """init() skips index.md, log.md, gaps.md."""
        wg = project["mod"]

        # System files at wiki root
        (project["wiki"] / "index.md").write_text("# Index\n")
        (project["wiki"] / "log.md").write_text("# Log\n")
        (project["wiki"] / "gaps.md").write_text("# Gaps\n")

        # One real page
        neu = project["wiki"] / "neu"
        neu.mkdir()
        (neu / "retina.md").write_text(PAGE_SIMPLE.replace("LGN", "Retina"))

        wg.init()

        slugs = wg.load_slugs()
        assert "index" not in slugs
        assert "log" not in slugs
        assert "gaps" not in slugs
        assert "retina" in slugs

    def test_init_extracts_title_from_frontmatter(self, project, capsys):
        """init() uses frontmatter title, not slug, as the registry value."""
        wg = project["mod"]
        neu = project["wiki"] / "neu"
        neu.mkdir()

        page_content = """\
---
title: Lateral Geniculate Nucleus
course: neu
tags: [vision]
sources: [intro.pdf]
confidence: medium
last_updated: 2026-04-07
---

The LGN is a relay center.
"""
        (neu / "lgn.md").write_text(page_content)

        wg.init()

        slugs = wg.load_slugs()
        assert slugs["lgn"] == "Lateral Geniculate Nucleus"
