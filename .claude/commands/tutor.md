Generate a personalized study plan.

If arguments are provided, use them as the scope: $ARGUMENTS

## Phase 1 — Intake (one question at a time, in order)

1. **Scope:** "What do you want to cover? (specific topics, whole course, a lecture range, or 'help me figure it out')"
2. **Timeline:** "How much total time do you have, and when is the deadline?"
3. **Mode:** "What's the goal?"
   - exam-prep — upcoming exam, cover material + practice problem-solving
   - concept-learning — understand from the ground up, no time pressure
   - homework — work through a specific pset or assignment
   - gap-fill — targeting weak spots from prior sessions
   - review — refresher on material seen before
4. **Diagnostic:** Check wiki/gaps.md first for known weak spots. Then ask 3-5 application-level questions on the target scope (not "define X"). Assess: strong / shaky / cold on each major topic.

## Phase 2 — Plan Generation

Read wiki/gaps.md + wiki/index.md + diagnostic results. Generate:

```
## Study Plan — [scope] | [mode] | [timeline]
Generated: YYYY-MM-DD

### Diagnostic summary
- Strong: [topics]
- Shaky: [topics]
- Cold: [topics]

### Session 1 (X hrs) — [focus]
- [ ] /ingest raw/<course>/<file> — not yet ingested
- [ ] /explain <concept> — currently cold
- [ ] /quiz <concept> — exam-style
- [ ] /explain <concept2>
- [ ] /quiz <concept2>

### Session 2 (X hrs) — [focus]
...

### Final Session — Synthesis
- [ ] /practice raw/<course>/practice_exam
- [ ] /gaps — review full tracker
- [ ] /lint — health check wiki
```

## Ordering Logic by Mode
- exam-prep: review session topics first → high-weight gaps → cold topics
- concept-learning: bottom-up — shared foundations before course-specific
- homework: load relevant wiki pages, then work problems one by one
- gap-fill: order active gaps by frequency (most-missed first) + recency
- review: light /quiz sweeps, skip confidence: high pages

Append to wiki/log.md: `## [YYYY-MM-DD] study-guide | [mode] | [scope]`
