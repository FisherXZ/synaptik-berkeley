---
title: Functional Abstraction
course: cs61a
tags: [abstraction, spec, domain, range, DRY]
sources: [04-Higher-Order_Functions.pdf, 06-Functional_Abstraction.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

Functional abstraction is the principle that a function's specification (what it does) should be separable from its implementation (how it does it), allowing users and implementers to work independently.

## Core explanation

### The three aspects of a function

A function can be described completely by three things:
1. **Domain** — the set of valid inputs (argument types and constraints)
2. **Range** — the set of possible outputs (return type and constraints)
3. **Behavior** — the relationship between inputs and outputs (what it computes)

You do NOT need to know the implementation to use a function correctly. The spec is a contract.
<!-- source: EXTRACTED from "04-Higher-Order_Functions.pdf" -->

### The spec — five components

A complete function spec includes:

| Component | Description |
|---|---|
| **Name** | The function's identifier |
| **Input(s)** | Types and preconditions (e.g., "n must be a positive integer") |
| **Output** | Type and postcondition (what the return value satisfies) |
| **Side effects** | Any observable effects beyond the return value (e.g., printing) |
| **Example calls** | Concrete input/output pairs in the docstring |

The spec says **WHAT** the function does, never **HOW**.
<!-- source: EXTRACTED from "06-Functional_Abstraction.pdf" -->

### Freedom of implementation

As long as you satisfy the spec, you can change the implementation without breaking callers. This is the whole point of abstraction — the caller is isolated from implementation details.

```python
# Implementation A
def square(x):
    return x * x

# Implementation B — different how, same what
def square(x):
    return pow(x, 2)
```

Both satisfy the same spec. Code that calls `square` doesn't care which is used.
<!-- source: EXTRACTED from "06-Functional_Abstraction.pdf" -->

### DRY — Don't Repeat Yourself

If you write the same logic more than once, extract it into a function. Repeated code:
- Creates maintenance burden (fix a bug in 3 places)
- Signals that you haven't found the right abstraction yet

```python
# Bad: repeated computation
area1 = 3.14159 * r1 * r1
area2 = 3.14159 * r2 * r2

# Good: one function
def circle_area(r):
    return 3.14159 * r * r
```
<!-- source: EXTRACTED from "06-Functional_Abstraction.pdf" -->

### One job per function

Each function should do exactly one thing. Mixing concerns makes code:
- Harder to test
- Harder to reuse
- Harder to reason about

Example: a function that both computes and prints a result is harder to reuse than one that just computes and returns.
<!-- source: EXTRACTED from "06-Functional_Abstraction.pdf" -->

## Connections

- [[function]] — def statements are how abstractions are implemented
- [[higher_order_function]] — HOFs are a form of abstraction (abstract over computation)
- [[environment_diagram]] — abstraction hides implementation; diagrams show the actual implementation state

## Exam relevance

- Distinguish spec (what) from implementation (how) — exam questions test whether you can write a function that satisfies a given spec
- Preconditions: if the spec says "n is positive," you don't need to handle n ≤ 0
- Docstring reading: understand what a function is supposed to do before implementing it

## Common mistakes

- Implementing behavior not specified by the spec (over-engineering)
- Violating the precondition and expecting graceful behavior
- Writing functions that both compute and print — usually a sign the abstraction is wrong
