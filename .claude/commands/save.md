File a valuable answer, synthesis, or insight back into the wiki.

If a title is provided, use it: $ARGUMENTS

## What to Save
Identify what's worth keeping from the current conversation:
- A clear multi-step explanation
- A synthesis across multiple concepts
- A comparison or connection between topics
- A worked exam problem

## Destination Decision
- Deepens an existing concept → update that page's Core Explanation or Common Mistakes section
- Synthesizes multiple concepts → create new page in wiki/<course>/
- Worked exam problem → create wiki/<course>/worked-problems/ page

## Execution
1. Write the page using standard frontmatter format (title, course, tags, sources, confidence, last_updated)
2. Set confidence based on how well it was understood in conversation
3. Add [[wikilinks]] to all related concept pages
4. Update wiki/index.md if a new page was created
5. If wiki_guard.py exists, run slug-check before creating, slug-register after
6. Append to wiki/log.md:
   ```
   ## [YYYY-MM-DD] save | <page title>
   Type: <explanation | synthesis | comparison | worked-problem>
   Filed to: wiki/<course>/<filename>.md
   ```
