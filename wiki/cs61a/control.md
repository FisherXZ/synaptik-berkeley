---
title: Control Flow
course: cs61a
tags: [control, if, while, loops, boolean, multiple-assignment]
sources: [03-Control.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

Control flow determines which statements execute and in what order, using conditional statements (`if/elif/else`) and iterative statements (`while`).

## Core explanation

### Conditional statements (if/elif/else)

```python
if <test1>:
    <suite1>
elif <test2>:
    <suite2>
else:
    <suite3>
```

Execution:
1. Evaluate `test1`; if truthy, execute `suite1` and skip everything else
2. Otherwise, evaluate `test2`; if truthy, execute `suite2`
3. Otherwise, execute `suite3`

`elif` and `else` clauses are optional. Only one suite executes per `if` statement.
<!-- source: EXTRACTED from "03-Control.pdf" -->

### While loops

```python
while <condition>:
    <body>
```

Execution:
1. Evaluate `condition`
2. If truthy: execute `body`, then go back to step 1
3. If falsy: exit the loop

**Critical requirement**: something in `body` must eventually make `condition` false, or the loop runs forever.
<!-- source: EXTRACTED from "03-Control.pdf" -->

### Example: prime factorization

```python
def prime_factors(n):
    """Print the prime factors of n in non-decreasing order."""
    k = 2
    while k < n:
        if n % k == 0:
            print(k)
            n = n // k   # divide out the factor
        else:
            k += 1
    print(n)
```

Pattern: trial division from 2 upward, reducing `n` whenever a factor is found.
<!-- source: EXTRACTED from "03-Control.pdf" -->

### Multiple assignment — THE key rule

```python
b, a = a + b, b
```

**ALL right-hand side expressions are evaluated first (left to right), THEN all assignments happen simultaneously.**

Without this rule, `b, a = a+b, b` would corrupt the values if `b` updated before `a+b` was computed. This is why swap in Python works:

```python
x, y = y, x   # correct swap — both RHS evaluated before any binding
```
<!-- source: EXTRACTED from "03-Control.pdf" -->

### Fibonacci with multiple assignment

```python
def fib(n):
    pred, curr = 0, 1   # F(0), F(1)
    k = 1
    while k < n:
        pred, curr = curr, pred + curr
        k += 1
    return curr
```

This avoids needing a temp variable because both sides of the update are evaluated together.
<!-- source: EXTRACTED from "03-Control.pdf" -->

## Key equations / rules

- `if/elif/else`: at most one suite executes; evaluated top to bottom
- `while`: body executes repeatedly while condition is truthy
- Multiple assignment: evaluate ALL RHS → then bind ALL names simultaneously
- Short-circuit: `and` / `or` stop evaluating as soon as result is determined (see [[boolean]])

## Connections

- [[boolean]] — truthiness determines which branch/iteration runs
- [[function]] — control flow appears inside function bodies
- [[recursion]] — recursion is an alternative to iteration; while loops can often be rewritten recursively

## Exam relevance

- Multiple assignment in Fibonacci and similar programs — trace carefully
- `while n > 1` vs. `while n >= 1` — off-by-one errors on boundaries
- Identifying when a while loop terminates (or doesn't)

## Common mistakes

- Evaluating multiple assignment left-to-right sequentially (wrong) instead of all-RHS-first-then-bind (correct)
- Forgetting that `elif` is skipped if any earlier `if`/`elif` was truthy
- Infinite loops: forgetting to update the loop variable in the body
