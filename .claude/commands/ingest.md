Process the file or folder $ARGUMENTS into the wiki.

## Pre-checks
1. If wiki_guard.py exists, run `python3 wiki_guard.py cache-check` to see which files are NEW or CHANGED. Only process those.
2. Check wiki/log.md for previously ingested files. Skip files already listed unless the source has been updated.
3. If no argument provided, scan raw/ for all uningested files and process them.

## For Each Source File
1. Read the source file fully
2. Extract: key concepts, definitions, mechanisms, exam-flagged topics
3. For each concept:
   - Run `python3 wiki_guard.py slug-check <proposed-slug>` if wiki_guard.py exists
   - If EXACT MATCH → update existing page instead of creating new
   - If no page exists → create wiki/<course>/<concept-slug>.md with full frontmatter:
     ```yaml
     ---
     title: <Concept Name>
     course: <detected from raw/ subdirectory>
     tags: [tag1, tag2]
     sources: [filename]
     confidence: low
     last_updated: YYYY-MM-DD
     ---
     ```
   - Tag every factual claim with provenance:
     `<!-- source: EXTRACTED from "filename.pdf" -->` — directly stated
     `<!-- source: INFERRED — synthesized across Source1 + Source2 -->` — LLM synthesis
   - Run `python3 wiki_guard.py slug-register <slug> "<Title>"` after creating
4. Add [[wikilinks]] to related pages already in the wiki
5. Update wiki/index.md — add new pages with one-line summary under correct course section
6. Append to wiki/log.md:
   ```
   ## [YYYY-MM-DD] ingest | <filename>
   Pages created: X | Pages updated: Y
   Key concepts: <comma-separated list>
   Exam-relevant topics flagged: <list or "none">
   ```
7. Run `python3 wiki_guard.py cache-update <raw-file>` for each processed file
8. Run `python3 wiki_guard.py validate` to check all pages

## Course Auto-Detection
Detect courses from raw/ subdirectories. Each subdirectory under raw/ is a course.
Create corresponding wiki/<course>/ directories automatically.

## Priority Order (for full ingest runs)
1. Review session slides + transcript (instructor-curated, highest exam signal)
2. Lecture transcripts (full verbal explanation)
3. Lecture slides (structure + diagrams)
4. Practice exams + psets (question style source)
