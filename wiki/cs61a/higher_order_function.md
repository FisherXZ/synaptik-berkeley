---
title: Higher-Order Functions
course: cs61a
tags: [higher-order, functions-as-values, closure, abstraction]
sources: [04-Higher-Order_Functions.pdf, 05-Environments.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

A higher-order function (HOF) is a function that takes another function as an argument, returns a function as its value, or both.

## Core explanation

### Functions as arguments

The canonical example is `summation`, which generalizes "sum the first n terms of a sequence":

```python
def summation(n, term):
    """Sum the first n terms of a sequence defined by term."""
    total, k = 0, 1
    while k <= n:
        total, k = total + term(k), k + 1
    return total
```

`term` is a function passed in as an argument. Callers supply any single-argument function:
```python
def cube(k): return pow(k, 3)
summation(5, cube)   # → 225
```

This abstraction separates the **iteration logic** from the **per-term computation** — neither knows how the other works.
<!-- source: EXTRACTED from "04-Higher-Order_Functions.pdf" -->

### Functions as return values

A function can build and return a new function. The returned function has access to the enclosing function's local names (a **closure**):

```python
def make_adder(n):
    def adder(k):
        return k + n   # n comes from make_adder's frame
    return adder

add5 = make_adder(5)
add5(3)   # → 8
```

`add5` is a function. Its **parent frame** is the frame created by `make_adder(5)`, so it can still see `n = 5` even after `make_adder` has returned.
<!-- source: EXTRACTED from "04-Higher-Order_Functions.pdf" -->

### Locally defined functions

Functions defined inside other functions are **locally defined** (nested). They:
- Can reference names from the enclosing scope (closure over the enclosing frame)
- Are not visible outside the enclosing function
- Get a parent frame equal to the enclosing function's local frame
<!-- source: EXTRACTED from "05-Environments.pdf" -->

### Why HOFs matter

Three design benefits:
1. **Modularity**: separate concerns cleanly (`summation` doesn't know what `term` computes)
2. **Abstraction**: general patterns captured once, specialized by passing different functions
3. **Separation of concerns**: iteration logic vs. per-element logic are independent
<!-- source: EXTRACTED from "04-Higher-Order_Functions.pdf" -->

### HOFs with environment diagrams

Each call to a HOF that returns a function creates a frame that persists (as the returned function's parent). Example walkthrough for `make_adder(5)(3)`:
1. Call `make_adder(5)` → new frame f1: `n = 5`; `adder` defined with parent = f1; returned
2. Call the returned `adder` with `3` → new frame f2: `k = 3`, parent = f1
3. Body: `k + n` → looks up `k=3` in f2, `n=5` in f1 → returns 8
<!-- source: EXTRACTED from "05-Environments.pdf" -->

## Connections

- [[environment_diagram]] — parent frames make closures work
- [[function]] — HOFs are functions; same def/call mechanics apply
- [[functional_abstraction]] — HOFs are the primary tool for abstraction
- [[recursion]] — recursive HOFs (e.g. `summation` over recursive sequences)

## Exam relevance

- Draw the full environment diagram for any HOF call — parent frames are always tested
- Understand what gets captured in a closure vs. what is a parameter
- `make_adder` / `make_multiplier` patterns appear frequently

## Common mistakes

- Confusing the function *object* with a function *call*: `make_adder` vs. `make_adder(5)`
- Forgetting that the inner function's parent is the frame where it was defined (the enclosing call's frame), not the global frame
- Thinking a returned function "copies" its enclosing variables — it actually retains a reference to the enclosing frame
