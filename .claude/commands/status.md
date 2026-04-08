Quick session orientation.

## Steps
1. Read wiki/log.md (last 10 entries)
2. Read wiki/gaps.md (Active Gaps section)
3. If wiki_guard.py exists, run `python3 wiki_guard.py cache-check` to identify uningested files precisely
4. Otherwise scan raw/ vs wiki/log.md to find files not yet ingested

## Report Format
- **Last session:** what was covered (date, command, key topics)
- **Top 3 gaps:** one-line each, ranked by times surfaced
- **Uningested files:** list of files in raw/ not yet processed
- **Suggested first action:** based on gaps + uningested files, recommend what to do this session
