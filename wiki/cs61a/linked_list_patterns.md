---
title: Linked List Patterns
course: cs61a
tags: [linked-list, practice, hw06, lab07, exam-relevant]
sources: [hw06.py, lab07.py, 61a-fa25-mt2_sol.pdf, 61a-fa25-final_sol.pdf]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** The concrete patterns for operating on the `Link` class — recursive construction, mutation, filtering, and the sentinel node idiom.

## Core explanation

The `Link` class:
```python
class Link:
    empty = ()
    def __init__(self, first, rest=Link.empty):
        self.first = first
        self.rest = rest
```

`s is Link.empty` checks for the empty list. `s.first` is the head; `s.rest` is the tail.

### Pattern 1: Build a linked list from digits (iterative, bottom-up)

`store_digits` from hw06 — builds from right to left using remainders:

```python
def store_digits(n):
    result = Link.empty
    while n > 0:
        result = Link(n % 10, result)   # prepend last digit
        n //= 10
    return result
```

Each iteration prepends `n % 10` to the front. Since we process right-to-left and prepend, the result is left-to-right ordered.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 2: Recursive filtering (non-mutating)

`exclude_link` from MT2 — return a new linked list excluding all x:

```python
def exclude_link(s, x):
    if s is Link.empty:
        return s
    elif s.first == x:
        return exclude_link(s.rest, x)   # skip this node
    else:
        return Link(s.first, exclude_link(s.rest, x))
```

Three cases: empty → return empty; match → skip (recurse on rest); no match → keep (build new Link).

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->

### Pattern 3: Recursive mutation (deep map)

`deep_map_mut` from hw06 — mutate in place, no new Links:

```python
def deep_map_mut(func, s):
    if s is Link.empty:
        return None
    elif isinstance(s.first, Link):
        deep_map_mut(func, s.first)   # recurse into nested list
    else:
        s.first = func(s.first)       # mutate in place
    deep_map_mut(func, s.rest)        # always advance to rest
```

Key: the two recursive calls — one into `.first` (if it's a Link), one along `.rest` — are both needed.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 4: Mutation with insertion (duplicate_link)

`duplicate_link` from lab07 — insert a new node after every matching node:

```python
def duplicate_link(s, val):
    if s is Link.empty:
        return
    elif s.first == val:
        remaining = s.rest
        s.rest = Link(val, remaining)    # insert duplicate
        duplicate_link(remaining, val)   # recurse PAST the new node
    else:
        duplicate_link(s.rest, val)
```

Key: recurse on `remaining` (the original next node), NOT on `s.rest` (which is the newly inserted copy). Otherwise you'd recurse on the copy and create infinite duplicates.

<!-- source: EXTRACTED from "lab07.py" -->

### Pattern 5: Recursive without (skip index)

`without` from lab07 — return new linked list skipping element at index i:

```python
def without(s, i):
    if s is Link.empty:
        return s
    if i == 0:
        return s.rest
    else:
        return Link(s.first, without(s.rest, i-1))
```

Pattern: decrement i at each step; when i reaches 0, skip that node.

<!-- source: EXTRACTED from "lab07.py" -->

### Pattern 6: Sentinel node (iterative linked list builder)

`two_list_iterative` from hw06 — the sentinel (dummy head) pattern:

```python
def two_list_iterative(vals, counts):
    result = Link(None)   # sentinel: dummy head node
    p = result
    for index in range(len(vals)):
        for _ in range(counts[index]):
            p.rest = Link(vals[index])
            p = p.rest
    return result.rest    # skip the sentinel
```

Sentinel avoids special-casing the first node. At the end, `result.rest` is the actual list.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 7: Two-pointer (match at distance k)

Final Q6(a) `match` — advance one pointer k steps ahead, then walk both together:

```python
def match(s, k):
    t, count = s, 0
    for x in range(k):            # advance t by k steps
        if t is not Link.empty:
            t = t.rest
    while t is not Link.empty:    # walk s and t together
        if s.first == t.first:
            count += 1
        s, t = s.rest, t.rest
    return count
```

<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

## Key patterns

| Pattern | Key implementation |
|---|---|
| Build from int | `result = Link(n % 10, result); n //= 10` |
| Filter (non-mutating) | 3-case: empty / match (skip) / no-match (keep) |
| Deep map (mutation) | Two recursive calls: into `.first` if Link, along `.rest` always |
| Insert after match | Store `remaining = s.rest`; set `s.rest = Link(val, remaining)`; recurse on `remaining` |
| Skip index i | Decrement i each step; when `i == 0`, return `s.rest` |
| Two-pointer at distance k | Advance one pointer k steps; then walk both |

## Connections

[[oop_class_patterns]] [[recursion_patterns]]

## Exam relevance

- MT2 Q4 "Exclusive": `exclude_link` — 5-blank fill-in, tests the 3-case recursive pattern
- Final Q6(a) `match`: two-pointer with `for x in range(k)` to advance; simultaneous walk
- hw06 `deep_map_mut`: banned from creating new Links — must mutate `.first` in place

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

## Common mistakes

- **`duplicate_link` infinite loop**: recursing on `s.rest` (the new copy) instead of `remaining` (the original next) creates an infinite chain
- **`store_digits` direction**: processing `n % 10` (last digit) and prepending builds left-to-right — this is correct and elegant but non-obvious
- **Checking empty**: use `s is Link.empty` not `s == Link.empty` — `Link.empty = ()` and `() == ()` is True but you want identity check for clarity
- **`without` out-of-bounds**: if `i >= len(s)`, the function returns all of s unchanged (falls off the end when `s is Link.empty`) — this is correct behavior
- **two_list recursive version**: the helper tracks `count` and `index` separately — confusing the two causes off-by-one on the count

## Provenance

<!-- source: EXTRACTED from "hw06.py" -->
<!-- source: EXTRACTED from "lab07.py" -->
<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->
