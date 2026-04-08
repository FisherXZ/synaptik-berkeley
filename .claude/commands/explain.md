Give a deep, ground-up explanation of: $ARGUMENTS

## Setup
1. Detect course — scan wiki/<course>/ directories for a matching page
2. Read wiki/<course>/<topic>.md and all linked pages
3. Read wiki/gaps.md — check for active gaps related to this topic
4. If foundational concepts are needed, read wiki/shared/ pages

## Depth Calibration (silent, no question asked)
- Confidence low + page is thin → full ground-up, start from absolute basics
- Confidence medium + specific gap exists → cover all 5 elements but weight toward the gap area
- Confidence high → skip basic setup, go deeper on mechanisms and connections

## Explanation Protocol (all 5 elements, every time)
1. **Core concept** — plain English first. Analogy before formalism. No jargon until the foundation is laid.
2. **Step-by-step reasoning** — explain *why* each step follows from the last, not just what the steps are
3. **Full derivation/calculation** — every step shown, nothing skipped
4. **Real-world connection** — where this actually shows up outside the classroom
5. **Visual SVG/HTML diagram** — proper geometric or mechanistic illustration, not ASCII art.
   Save it as a standalone HTML file: wiki/visuals/<concept-slug>.html
   Self-contained (inline CSS/SVG, no external deps). Notion-style light theme.

## If the student says "I don't get it"
Rebuild from scratch with:
- Simpler language, different analogy
- Smaller pieces — break the concept into sub-steps
- More intermediate diagrams
- Ask "which specific part lost you?" to target the confusion

## After Explaining
1. Ask: "What questions do you have?" — keep going until clear
2. Update the wiki page's Common Mistakes section if any confusion came up
3. Offer: "Want me to /save this explanation to the wiki?"
