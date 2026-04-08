# synaptik-berkeley

**[synaptik](https://github.com/FisherXZ/synaptik) pre-loaded with Berkeley's most popular courses.**

An AI-maintained knowledge base with real lecture materials from UC Berkeley's highest-enrollment classes. Three courses come fully ingested as demos — the rest have raw materials ready for you to `/ingest`.

## Courses

| Course | Status | Description |
|--------|--------|-------------|
| CS 61A | Ingested | Structure & Interpretation of Computer Programs |
| CS 61B | Ingested | Data Structures |
| Data 8 | Ingested | Foundations of Data Science |
| CS 70 | Raw only | Discrete Math & Probability |
| Math 54 | Raw only | Linear Algebra & Differential Equations |
| Bio 1A | Raw only | General Biology |
| Psych 1 | Raw only | Introduction to Psychology |
| Econ 1 | Raw only | Introduction to Economics |

**Ingested** = wiki pages already built, ready to `/quiz` and `/explain`.
**Raw only** = materials in `raw/`, run `/ingest` to build wiki pages.

## Quickstart

1. [Use this template](../../generate) → clone your repo
2. Open in [Claude Code](https://claude.ai/download)
3. Type `/status` to see what's available
4. Try `/quiz` on any ingested topic, or `/ingest` the courses you're taking

## All materials are from public course websites

- CS 61A: [cs61a.org](https://cs61a.org)
- CS 61B: [datastructur.es](https://datastructur.es)
- Data 8: [data8.org](https://data8.org)

No copyrighted bCourses materials are included.

## Not at Berkeley?

Use the empty template instead: **[synaptik](https://github.com/FisherXZ/synaptik)** — works for any subject, any school, any kind of learning.

## Commands

| Command | What it does |
|---------|-------------|
| `/ingest <file>` | Process source material into wiki pages |
| `/quiz <topic>` | Active recall quiz with 3 modes: quick check, exam prep, gap attack |
| `/explain <topic>` | Deep explanation with visuals |
| `/practice <exam>` | Walk through a practice exam |
| `/tutor` | Generate a personalized study plan |
| `/save` | File a useful answer back into the wiki |
| `/gaps` | Review your knowledge gap tracker |
| `/lint` | Wiki health check |
| `/status` | Session orientation |

## Requirements

- [Claude Code](https://claude.ai/download) (CLI, desktop app, or web)
- Python 3.8+ (for wiki_guard.py — stdlib only, no pip install)

## License

MIT
