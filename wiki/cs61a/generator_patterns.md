---
title: Generator Patterns
course: cs61a
tags: [generators, iterators, practice, hw05, lab05, exam-relevant]
sources: [hw05.py, lab05.py, 61a-fa25-mt2_sol.pdf]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** The concrete patterns for writing Python generators — `yield`, `yield from`, infinite generators, and the merge/interleave idiom tested on exams.

## Core explanation

### Pattern 1: Recursive generator with yield from

`hailstone` generator from hw05 — infinite generator that yields 1 forever at the end:

```python
def hailstone(n):
    yield n
    if n == 1:
        yield from hailstone(n)    # infinite: keeps yielding 1
    elif n % 2 == 0:
        yield from hailstone(n // 2)
    else:
        yield from hailstone(n * 3 + 1)
```

`yield from` delegates to a sub-generator. This is cleaner than a loop and handles infinite sequences naturally.

<!-- source: EXTRACTED from "hw05.py" -->

### Pattern 2: Merge two sorted infinite generators

`merge` from hw05 — the canonical two-pointer merge:

```python
def merge(a, b):
    a_val, b_val = next(a), next(b)
    while True:
        if a_val == b_val:
            yield a_val
            a_val, b_val = next(a), next(b)
        elif a_val < b_val:
            yield a_val
            a_val = next(a)
        else:
            yield b_val
            b_val = next(b)
```

Key points:
- Advance **both** pointers on equality (deduplication)
- Advance only the smaller-value pointer otherwise
- The `while True` loop is correct because both inputs are infinite

<!-- source: EXTRACTED from "hw05.py" -->

### Pattern 3: Generating all combinations (stairways)

`stair_ways` from hw05 — yield all paths through a combinatorial space:

```python
def stair_ways(n):
    if n == 0:
        yield []
    elif n == 1:
        yield [1]
    else:
        for way in stair_ways(n - 1):
            yield [1] + way
        for way in stair_ways(n - 2):
            yield [2] + way
```

Pattern: base case yields the identity path `[]`; recursive case prepends the current choice to every sub-path. This is the generator version of the tree-recursion count-ways pattern.

<!-- source: EXTRACTED from "hw05.py" -->

### Pattern 4: Iterator consumption (count_occurrences)

`count_occurrences` from lab05 — iterates exactly `n` elements and counts matches:

```python
def count_occurrences(t, n, x):
    count = 0
    for _ in range(n):
        if next(t) == x:
            count += 1
    return count
```

Crucial: the iterator `t` is advanced by `next(t)` — calling `for _ in range(n)` consumes exactly n elements and leaves the iterator positioned for future use. This is tested on exams by checking what `list(u)` returns after partial consumption.

<!-- source: EXTRACTED from "lab05.py" -->

### Pattern 5: Generator WWPD (What Would Python Display)

MT2 Q1 "What Would Python Display" tests generator tracing — the `weird` generator:

```python
def weird(s):
    if s:
        if len(s) > 1:
            yield s[1]
        for x in weird(s[1:]):
            yield x
        yield s[0]
```

Tracing rule: a generator function does not execute until `next()` is called. When `t = weird([5, [6,7], 8])`:
- `next(t)` → yields `s[1]` = `[6, 7]`
- `[x for x in t]` → exhausts: recurses into `weird([[6,7], 8])`, etc., ends with `s[0]` = 5
- Result: `[8, 8, [6, 7], 5]`

Order-of-growth: `even(s)` is O(log n) because it calls `weirder(t, 1)` and each level doubles the index.

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->

## Key patterns

| Pattern | Key code | Use case |
|---|---|---|
| Infinite recursive generator | `yield n; yield from hailstone(next_n)` | Sequences that continue indefinitely |
| Merge sorted infinite streams | Two-pointer with `next()` in `while True` | Combining sequences without duplicates |
| All-paths generator | Base: `yield []`; recursive: `yield [choice] + way` | Combinatorial enumeration |
| Partial iterator consumption | `for _ in range(n): next(t)` | Consuming exactly n elements |

## Connections

[[recursion_patterns]] [[tree_recursion_strategies]] [[lambda_and_closures]]

## Exam relevance

- MT2 Q1: generator WWPD — must understand execution is lazy, state persists between `next()` calls
- MT2 Q1(c): order of growth of `even(s)` — logarithmic because index doubles each level
- Final Q3(d) `solve`: uses `candidates(n)` which is a generator that yields all n-length lists — `yield [first] + rest` for `first in allowed`, `rest in candidates(n-1)`

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

## Common mistakes

- **yield from vs yield**: `yield from gen` yields each element of `gen`; `yield gen` yields the generator object itself
- **Infinite generator base case**: for `hailstone`, when `n == 1` the base case is `yield from hailstone(1)` — NOT `return` (which would terminate)
- **merge deduplication**: on equal values, advance BOTH pointers and yield once — advancing only one would yield duplicates
- **Iterator state**: after `count_occurrences(u, 3, 2)` consumes 3 elements, `list(u)` gives the remaining elements. Students forget that iterators are stateful
- **Generator WWPD trap**: calling `next()` once on a generator that has `yield` statements in both branches — execution halts at the FIRST yield hit, not all of them

## Provenance

<!-- source: EXTRACTED from "hw05.py" -->
<!-- source: EXTRACTED from "lab05.py" -->
<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->
