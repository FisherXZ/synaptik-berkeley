---
title: Containers and Aggregation
course: cs61a
tags: [container, aggregation, sum, max, all, strings, iteration]
sources: [12-Containers.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

Containers are data structures that hold multiple values; Python's built-in aggregation functions (`sum`, `max`, `all`) process any iterable container into a single result.

## Core explanation

### What is a container

A container is any value that holds other values and supports:
1. Membership testing: `x in container`
2. Iteration: `for x in container`

In CS 61A lectures 1-12, the primary containers are **lists**, **ranges**, and **strings**.
<!-- source: EXTRACTED from "12-Containers.pdf" -->

### Built-in aggregation functions

Several built-in functions accept an iterable and reduce it to a single value:

#### `sum(iterable[, start])`
Returns the sum of all elements plus `start` (default 0). Empty iterable returns `start`.
```python
sum([1, 2, 3])       # → 6
sum([1, 2, 3], 10)   # → 16
sum(range(5))        # → 10
```

#### `max(iterable[, key=func])` / `max(a, b, c, ...[, key=func])`
Returns the largest element. With `key=`, compares by `key(element)` instead of the element itself.
```python
max([3, 1, 4])           # → 4
max([3, 1, 4], key=lambda x: -x)  # → 1 (largest by negation = smallest)
```

#### `all(iterable)`
Returns `True` if `bool(x)` is `True` for **every** element; `False` as soon as one is falsy. Returns `True` for empty iterables.
```python
all([True, 1, "yes"])   # → True
all([True, 0, "yes"])   # → False  (0 is falsy)
all([])                 # → True   (vacuously true)
```
<!-- source: EXTRACTED from "12-Containers.pdf" -->

### Strings as sequences

Strings behave like sequences: they support indexing, slicing, iteration, and `len`.
```python
s = "hello"
s[0]      # → 'h'
s[1:]     # → 'ello'
len(s)    # → 5
for c in s:   # iterates character by character
    ...
```

Tree recursion with strings works analogously to lists:
- Base case: empty string `""` or single character
- Recursive case: `s[0]` (first char) + recurse on `s[1:]` (rest)
<!-- source: EXTRACTED from "12-Containers.pdf" -->

### Processing container values — patterns

**Using indices** (explicit loop variable):
```python
for i in range(len(s)):
    if s[i] == 8 and s[i+1] == 8:
        return True
```

**Using slices** (recursive-style):
```python
if s[:2] == [8, 8]:
    return True
elif len(s) < 2:
    return False
else:
    return double_eights(s[1:])
```

Both styles appear on exams. The slice style maps naturally to recursive thinking; the index style maps to iterative thinking.
<!-- source: EXTRACTED from "12-Containers.pdf" -->

### Box-and-pointer recap for nested containers

Compound structures in environment diagrams:
```python
one_two = [1, 2]
nested = [[1, 2], [], [[3, False, None], [4, lambda: 5]]]
```

Each list is a row of boxes. A box pointing to another list shows an arrow to that list's row. A function value in a list box shows an arrow to the function object (with its parent frame pointer).
<!-- source: EXTRACTED from "12-Containers.pdf" -->

## Key equations / rules

- `sum(s)` = sum of all elements; `sum(s, start)` adds `start` to the total
- `max(s)` = largest element by default comparison
- `all(s)` = `True` iff no element is falsy
- Strings support all sequence operations (indexing, slicing, `in`, `len`, iteration)

## Connections

- [[list]] — the primary container in early CS 61A; shares indexing/slicing/iteration
- [[boolean]] — `all()` uses truthiness; filter conditions in comprehensions too
- [[higher_order_function]] — `max(key=f)` is a HOF pattern
- [[tree_recursion]] — tree recursion with strings (count_park, subsets)
- [[environment_diagram]] — box-and-pointer notation for nested containers

## Exam relevance

- `sum`, `max`, `all` with list comprehension arguments: `sum([f(x) for x in s])`
- String recursion: treat a string like a list — `s[0]` is first char, `s[1:]` is the rest
- `all` with a comprehension: `all([x > 0 for x in s])` — tests a condition on every element

## Common mistakes

- `max` with `key=` vs without — `key` changes the comparison criterion but `max` still returns the original element (not the key value)
- `all([])` is `True` (vacuously) — can cause subtle bugs if you expected `False` for empty inputs
- Trying to use `sum` on a list of strings — `sum` doesn't work on strings; use `"".join(s)` instead
