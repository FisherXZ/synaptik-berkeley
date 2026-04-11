# synaptik-berkeley

**[synaptik](https://github.com/FisherXZ/synaptik) pre-loaded with Berkeley's most popular courses.**

An AI-maintained knowledge base with real lecture materials from UC Berkeley's highest-enrollment classes. Three courses come fully ingested as demos — the rest have raw materials ready for you to `/ingest`.

![Obsidian graph view of the CS 61A wiki — cross-linked concept pages built from real lecture materials](assets/obsidian-graph.png)

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

A real compiled page from CS 61A — built from `04-Higher-Order_Functions.pdf` and `05-Environments.pdf`, cross-linked to related concepts, with provenance tags on every claim:

![wiki/cs61a/higher_order_function.md rendered in Obsidian](assets/compiled-page-cs61a.png)

Quiz yourself on it. When you get one wrong, the explanation walks you through it — and the miss gets logged to `gaps.md` for next session:

![/quiz higher_order_function — question, wrong answer, 5-element tutoring correction](assets/quiz-cs61a.png)

Ask for a ground-up explanation and you get a proper diagram, not ASCII art:

![/explain environment_diagram — SVG diagram showing frames, bindings, and parent pointers](assets/explain-diagram.png)

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
