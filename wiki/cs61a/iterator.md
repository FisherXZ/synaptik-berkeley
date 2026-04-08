---
title: Iterator
course: cs61a
tags: [iteration, protocol, lazy-evaluation]
sources: [16-Iterators.pdf, 19-Attributes.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

An iterator is an object that produces values one at a time on demand, via `next()`. An iterable is any object you can iterate over — it produces an iterator when you call `iter()` on it.

## Core Explanation

**The two-level protocol:**

| Concept | What it is | Key method | Exhausted? |
|---------|-----------|-----------|------------|
| Iterable | Can produce an iterator | `__iter__()` — returns a fresh iterator | No — can iterate multiple times |
| Iterator | Produces values one by one | `__next__()` — returns next value | Yes — single-pass, one-time use |

```python
s = [1, 2, 3]      # list is an ITERABLE (not an iterator)
it = iter(s)       # iter() calls s.__iter__(), returns iterator
next(it)           # → 1
next(it)           # → 2
next(it)           # → 3
next(it)           # raises StopIteration
```
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

**Key insight — iterators ARE iterables:**
An iterator implements both `__iter__` (returns `self`) and `__next__`. So you can pass an iterator anywhere an iterable is expected. But a plain list is NOT an iterator — calling `next([1,2,3])` raises `TypeError`.
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

**How `for` loops work under the hood:**
```python
for x in [1, 2, 3]:
    print(x)

# Equivalent to:
it = iter([1, 2, 3])
while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break
```
<!-- source: INFERRED — synthesized from "16-Iterators.pdf" -->

**`map()` returns an iterator (lazy):**
```python
doubled = map(lambda x: x * 2, [1, 2, 3])
# doubled is NOT a list — it's a map object (iterator)
next(doubled)   # → 2
next(doubled)   # → 4
# Values only computed when requested
```
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

**Single-use nature:**
```python
it = iter([1, 2, 3])
list(it)    # → [1, 2, 3]  — consumes all
list(it)    # → []          — already exhausted!
```
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

## Key Rules

- `iter(x)` → calls `x.__iter__()` → returns iterator
- `next(x)` → calls `x.__next__()` → returns next value or raises `StopIteration`
- Iterators are single-use; iterables (like lists) can produce fresh iterators each time
- `map`, `filter`, `zip`, `range` all return lazy iterators
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

## Connections

- [[generator]] — generator functions are the easiest way to create custom iterators
- [[higher_order_function_patterns]] — `map` and `filter` use iterators

## Exam Relevance

- Predict what happens after partially consuming an iterator then iterating again
- Distinguish `iter([1,2,3])` (creates new iterator) from passing the same iterator twice
<!-- source: EXTRACTED from "16-Iterators.pdf" -->

## Common Mistakes

- Treating `map(f, lst)` as if it returns a list — it returns an iterator
- Calling `next()` on a list (not an iterator) — `TypeError`
- Forgetting that iterating a list with `for` creates a fresh iterator each time; iterating the same iterator twice gives different results
