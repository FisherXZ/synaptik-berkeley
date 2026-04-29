
# synaptik-berkeley

**[synaptik](https://github.com/FisherXZ/synaptik) pre-loaded with Berkeley's most popular courses.**

An AI-maintained knowledge base with real lecture materials from UC Berkeley's highest-enrollment classes. Three courses come fully ingested as demos — the rest have raw materials ready for you to `/ingest`.

<img width="1012" height="815" alt="Screenshot 2026-04-29 at 15 52 09" src="https://github.com/user-attachments/assets/4e7f9df5-535c-4054-844a-d4ab4fe19469" />

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

## See it in action

A real compiled page from NEU 100B — built from lecture pdfs, cross-linked to related concepts, with provenance tags on every claim:

<img width="673" height="697" alt="Screenshot 2026-04-29 at 15 45 19" src="https://github.com/user-attachments/assets/eaadd60b-cd56-45a3-8392-46f82075d6ea" />

Quiz yourself on it. When you get one wrong, the explanation walks you through it — and the miss gets logged to `gaps.md` for next session:

<img width="814" height="636" alt="Screenshot 2026-04-29 at 15 51 47" src="https://github.com/user-attachments/assets/8569ad3b-f7dd-4788-8afc-c2aeb4e5d77c" />


Ask for a ground-up explanation and you get a visual breakdown:

<img width="1019" height="613" alt="Screenshot 2026-04-29 at 15 49 15" src="https://github.com/user-attachments/assets/7d331b33-0259-42ad-9004-996b5874c623" />
<img width="1205" height="642" alt="Screenshot 2026-04-29 at 15 50 18" src="https://github.com/user-attachments/assets/9a339f1b-4d1c-4711-a99b-a91d88653027" />

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

## Credit

Inspired by [Andrej Karpathy's "LLM wiki" gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the idea of turning raw source material into a compiled, cross-linked personal knowledge base maintained by an LLM. Synaptik operationalizes that pattern as a repo you can clone, with slash commands, a gap tracker, and session continuity baked in.

## License

MIT
