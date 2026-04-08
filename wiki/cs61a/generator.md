---
title: Generator
course: cs61a
tags: [iteration, generator, yield, lazy-evaluation]
sources: [17-Generators.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

A generator is a special type of iterator created by a function that uses `yield` instead of `return`. Calling a generator function does not execute its body — it returns a generator object that produces values lazily on each `next()` call.

## Core Explanation

**Basic example:**
```python
def plus_minus(x):
    yield x
    yield -x

t = plus_minus(3)   # generator object created — body NOT run yet
next(t)             # → 3   (runs until first yield, pauses)
next(t)             # → -3  (resumes, runs until second yield, pauses)
next(t)             # raises StopIteration (function body exhausted)
```
<!-- source: EXTRACTED from "17-Generators.pdf" -->

**How execution works:**
1. Call `plus_minus(3)` → returns generator object, body not started
2. First `next()` → body runs until `yield x`, produces `3`, **pauses**
3. Second `next()` → resumes after first yield, runs until `yield -x`, produces `-3`, **pauses**
4. Third `next()` → resumes, function returns (no more yields) → `StopIteration`
<!-- source: INFERRED — synthesized from "17-Generators.pdf" -->

**Yield from an iterator:**
```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)   # 3, 2, 1
```
<!-- source: INFERRED — synthesized from "17-Generators.pdf" -->

**Generator as lazy sequence:**
```python
def naturals():
    n = 1
    while True:        # infinite — but lazy, so fine
        yield n
        n += 1

g = naturals()
next(g)   # 1
next(g)   # 2
# Never exhausts — only computes what is requested
```
<!-- source: INFERRED — synthesized from "17-Generators.pdf" -->

**`yield from` (delegation):**
```python
def chain(s, t):
    yield from s   # yields each element of s, then
    yield from t   # each element of t
```
<!-- source: INFERRED — synthesized from "17-Generators.pdf" -->

## Key Rules

- A function containing `yield` is a **generator function**
- Calling a generator function returns a **generator object** (no code runs yet)
- A generator object is both an iterator and an iterable
- Each `next()` runs the body until the next `yield`, then pauses
- When the function body ends (or hits `return`), `StopIteration` is raised
<!-- source: EXTRACTED from "17-Generators.pdf" -->

## Connections

- [[iterator]] — generators implement the iterator protocol; same `next()`/`StopIteration` behavior
- [[higher_order_function_patterns]] — generators can replace list comprehensions for memory efficiency

## Exam Relevance

- Trace what is yielded at each `next()` call
- Predict `StopIteration` timing
- Understand that calling the function does NOT start execution
<!-- source: EXTRACTED from "17-Generators.pdf" -->

## Common Mistakes

- Calling the generator function and expecting immediate execution — nothing runs until `next()`
- Confusing `yield` (pauses, produces value, resumes) with `return` (terminates)
- Forgetting that a generator is single-use — once exhausted, it stays exhausted
