---
title: Booleans and Truthiness
course: cs61a
tags: [boolean, truthiness, bool, short-circuit, conditional]
sources: [07-Function_Examples.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

In Python, every value has a truth value: `False`, `0`, `0.0`, `''`, and `None` are **falsy**; everything else is **truthy**.

## Core explanation

### The bool function

`bool(x)` converts any value to `True` or `False` according to Python's truthiness rules.

**Falsy values** — `bool(x)` returns `False`:
- `False` (the boolean literal)
- `0` (integer zero)
- `0.0` (float zero)
- `''` (empty string)
- `[]` (empty list)
- `None`

**Truthy values** — `bool(x)` returns `True`:
- Everything else: non-zero numbers, non-empty strings, non-empty lists, any function object, etc.
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

### Why this matters

Conditional statements (`if`, `while`) evaluate their test expression and check its **truthiness**, not whether it literally equals `True`. So:

```python
if x:       # runs if x is truthy (x != 0, x != '', x != None, ...)
    ...

while lst:  # runs while lst is non-empty
    ...
```

This is idiomatic Python — prefer `if x:` over `if x != 0:` when checking for zero-ness.
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

### Short-circuit evaluation

Python's `and` and `or` operators short-circuit:

- `A and B`: evaluate `A`; if falsy, return `A` (skip `B`); else return `B`
- `A or B`: evaluate `A`; if truthy, return `A` (skip `B`); else return `B`

Note: `and`/`or` return the **value** that determined the result, not necessarily `True`/`False`:
```python
0 and 5    # → 0   (falsy, returned immediately)
3 and 5    # → 5   (3 is truthy, so result is B=5)
0 or 5     # → 5   (0 is falsy, so result is B=5)
3 or 5     # → 3   (3 is truthy, returned immediately)
```
<!-- source: INFERRED — synthesized from "07-Function_Examples.pdf" + standard Python semantics -->

### `not` operator

`not x` returns `True` if `x` is falsy, `False` if `x` is truthy. Always returns a boolean.

```python
not 0     # → True
not []    # → True
not 5     # → False
not None  # → True
```

## Connections

- [[control]] — if/while conditions rely on truthiness
- [[function]] — conditional expressions use truthiness
- [[list]] — empty list `[]` is falsy; useful in recursive list functions (`if not s: return []`)

## Exam relevance

- Know the complete falsy list: `False`, `0`, `0.0`, `''`, `[]`, `None`
- Short-circuit: `and` / `or` return values, not booleans — trace carefully
- `not` always returns a boolean; `and`/`or` may not

## Common mistakes

- Assuming `and`/`or` always return `True`/`False` — they return the determining operand
- Forgetting `None` is falsy (important when functions return `None` implicitly)
- Writing `if x == True:` instead of `if x:` — the former fails for truthy non-boolean values
