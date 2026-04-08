Run a wiki health check.

## Automated Check (if wiki_guard.py exists)
Run `python3 wiki_guard.py lint-quick` first for fast structural issues.
Then run `python3 wiki_guard.py validate` for frontmatter validation.

## Manual Scan (always)
Scan all wiki/ pages and check:
- Broken or missing [[wikilinks]] (link target page doesn't exist)
- Concepts mentioned in page bodies but lacking their own page
- Contradictions between pages (flag both page names + conflicting claims)
- Orphan pages (no inbound links from any other page)
- Pages with confidence: low not reviewed in the last 3 sessions
- Topics from practice exams in raw/ that have no wiki coverage
- Near-duplicate page slugs (suggest merging)
- Pages missing provenance labels (<!-- source: ... -->)

## Actions
- Fix what's unambiguous: add missing links, create stub pages for mentioned concepts
- Flag contradictions and gaps that need a source to resolve
- Suggest: new questions worth investigating, concepts that need depth, sources worth adding to raw/

Append to wiki/log.md:
```
## [YYYY-MM-DD] lint | Issues found: X | Fixed: Y | Flagged: Z
```
