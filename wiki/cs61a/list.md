---
title: Lists
course: cs61a
tags: [list, sequence, indexing, slicing, list-comprehension, for-loop]
sources: [11-Sequences.pdf, 12-Containers.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

A list is an ordered, mutable sequence of values accessed by integer index, supporting indexing, slicing, iteration, and comprehension syntax.

## Core explanation

### List literals and indexing

```python
digits = [8, 0, 8, 1]
#  index:  0  1  2  3
# neg idx:-4 -3 -2 -1

digits[2]    # → 8   (element at index 2)
digits[-1]   # → 1   (last element; negative index counts from end)
```

Index `i` for a list of length `n`:
- Positive: 0 to n-1
- Negative: -n to -1 (same element as `n + i`)
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### Nested lists

Lists can contain other lists. Access is chained:
```python
x = [3, 1, [4, 1, [5, 2], 6, 5], 3, 5]
x[2]         # → [4, 1, [5, 2], 6, 5]
x[2][2]      # → [5, 2]
x[2][2][1]   # → 2
```
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### Slicing

`s[start:end]` returns a new list containing elements from index `start` up to (but not including) `end`.

```python
s = [2, 3, 6, 4]
s[1:]   # → [3, 6, 4]  (from index 1 to end)
s[:2]   # → [2, 3]     (from start to index 2)
s[1:3]  # → [3, 6]
```

**Slicing creates a new list — it does not modify the original.** `s[1:]` is "all elements except the first" — the canonical recursive decomposition of a list.
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### First and rest

For any list `s`:
- `s[0]` is the first element
- `s[1:]` is the rest (all elements except the first), a shorter list

This is the list analog of `n` and `n-1` in integer recursion.
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### For loops

```python
for <name> in <iterable>:
    <body>
```

Iterates over each element of the iterable, binding `<name>` to each one in turn. Works with lists, ranges, strings, and any iterable.
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### Ranges

A `range` is a sequence of consecutive integers (or evenly spaced integers):

```python
range(4)        # → 0, 1, 2, 3
range(-2, 2)    # → -2, -1, 0, 1
list(range(4))  # → [0, 1, 2, 3]
```

Properties:
- **Length**: `end - start`
- **Element at index i**: `start + i`

`range(n)` is commonly used in `for` loops to iterate n times.
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### List comprehensions

Build a list by applying an expression to each element of an iterable, optionally filtered:

```python
[<map exp> for <name> in <iter exp> if <filter exp>]
[<map exp> for <name> in <iter exp>]   # without filter
```

Examples:
```python
[2 * x for x in range(n)]              # first n even numbers
[e for e in s if f(e)]                 # elements where f(e) is truthy
[e for e in s if f(e)] + [e for e in s if not f(e)]  # promoted pattern
```

The `promoted` pattern: reorder a sequence by putting elements satisfying `f` first, preserving relative order within each group.
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### List concatenation

`+` concatenates two lists into a new list:
```python
[1, 2] + [3, 4]   # → [1, 2, 3, 4]
reverse = lambda s: reverse(s[1:]) + [s[0]] if s else []
```
<!-- source: EXTRACTED from "11-Sequences.pdf" -->

### Box-and-pointer notation

In environment diagrams, a list is drawn as a row of boxes (one per element). Each box either:
- Contains a primitive value directly
- Holds an arrow pointing to a compound value (nested list, function, etc.)

Variable names in frames point (arrow) to the list object, not to the elements directly.
<!-- source: EXTRACTED from "12-Containers.pdf" -->

### Built-in aggregations

```python
sum(iterable[, start])   # sum of elements; start defaults to 0
max(iterable[, key=f])   # largest element; key= transforms before comparing
all(iterable)            # True if bool(x) is True for all x
```

These work on any iterable (list, range, etc.).
<!-- source: EXTRACTED from "12-Containers.pdf" -->

## Key equations / rules

- `len(s)` = number of elements
- `s[i]` valid for `-len(s) <= i < len(s)`
- `s[1:]` creates a NEW list (does not modify `s`)
- Comprehension: `[expr for x in s if cond]` — filter then map

## Connections

- [[recursion]] — `s[0]` / `s[1:]` is the list recursion decomposition
- [[tree_recursion]] — tree recursion over lists (e.g., subsets, counting)
- [[higher_order_function]] — `promoted` is a HOF taking a predicate
- [[boolean]] — filter expression in comprehensions uses truthiness
- [[environment_diagram]] — box-and-pointer shows list structure in diagrams

## Exam relevance

- Slicing: `s[1:]` creates a new list; `s` is unchanged
- List comprehension with filter: `[x for x in s if p(x)]`
- Recursive list processing: base case is `if not s: return []`; recursive case processes `s[0]` + recurse on `s[1:]`
- `double_eights` style problems: iterate with index or slice — both approaches appear on exams

## Common mistakes

- Thinking `s[1:]` modifies `s` — it does not; it returns a new list
- Off-by-one in indexing: last element is `s[len(s)-1]` = `s[-1]`, NOT `s[len(s)]`
- Using `range(n)` when you need `range(1, n+1)` — depends on whether you want 0-indexed or 1-indexed
- Forgetting that list `+` creates a new list — it does not append in place
