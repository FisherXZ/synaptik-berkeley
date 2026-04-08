Run an active recall quiz session on: $ARGUMENTS

## Setup
1. Detect course — scan wiki/<course>/ directories for a page matching the topic
2. Read wiki/<course>/<topic>.md and all pages it links to via [[wikilinks]]
3. Read wiki/gaps.md — check for active gaps on this topic
4. Read wiki/log.md — find last quiz session on this topic
5. Scan raw/<course>/ for practice exams and psets covering this topic
   - Extract question style and structure from those sources
   - If no source material exists, generate from wiki content

## Mode Selection (ask once, then execute)
Based on state, recommend one mode. Present all three:

A) Quick check — 3-5 questions, stop if solid. Best after /explain or for retention checks.
B) Exam prep — full session, exam difficulty, covers the full topic. Best before exams.
C) Gap attack — target specific weak spots from gaps.md. Only shown if active gaps exist on this topic.

RECOMMENDATION logic:
- If this /quiz follows an /explain in the same session → recommend A
- If active gaps exist on this topic → recommend C, citing the specific gap and date
- Default → recommend B

## Question Design
Progression depends on mode:
- Quick check: start at application level, skip definitions
- Exam prep: definition → mechanism → apply-to-new-scenario → multi-step → edge case
- Gap attack: focus questions around the specific gap, approach from multiple angles

Quality standard — require inference under constraint, not recall:
- Novel mutation/drug blocks one molecule mid-pathway → predict downstream effect
- Give a symptom pattern → localize the lesion (not the reverse)
- Conflicting data → design experiment to resolve
- Cross-topic combinations
- New receptor/cell type with given properties → predict behavior
BAD: "Patient has right-side lesion → what deficits?" (answer is directly on a diagram)

## Execution
- One question at a time. Wait for answer before next.
- **Correct:** acknowledge, add one layer of depth ("what would change if...")
- **Partially correct:** identify exactly what was right vs missing
- **Incorrect:** give full explanation:
  1. Core concept — plain English, analogy before formalism
  2. Step-by-step reasoning — why each step follows from the last
  3. Full derivation/calculation — every step shown
  4. Real-world connection
  5. Visual SVG/HTML diagram if the concept is spatial/mechanistic

## After Each Answer (immediately, do not batch)
- Wrong or shaky → add/update narrative gap entry in wiki/gaps.md using the gap format from CLAUDE.md
- Correct 2+ times on same concept → update confidence on wiki page (low→medium, medium→high)

## End of Session
Summary: what was solid, what needs work, suggested follow-up /quiz targets.
Offer: "Want me to /save any of these explanations to the wiki?"
