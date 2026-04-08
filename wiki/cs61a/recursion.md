---
title: Recursion
course: cs61a
tags: [recursion, base-case, recursive-case, divide-invoke-combine]
sources: [09-Recursion.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

Recursion is a technique where a function solves a problem by calling itself on a simpler version of the same problem, until it reaches a base case that can be solved directly.

## Core explanation

### Structure of a recursive function

Every correct recursive function has exactly two parts:

1. **Base case**: a condition under which the answer is known directly — no recursive call needed
2. **Recursive case**: reduce the problem to a smaller/simpler version of itself, call `self` on it, combine the result

```python
def factorial(n):
    if n == 0:           # base case
        return 1
    return n * factorial(n - 1)   # recursive case
```
<!-- source: EXTRACTED from "09-Recursion.pdf" -->

### The Divide / Invoke / Combine pattern

A useful mental template for writing recursive functions:

1. **Divide**: split the problem — what's the simplest version (base case)? What's the reduction step?
2. **Invoke**: call the function recursively on the reduced problem — TRUST that it works correctly
3. **Combine**: take the recursive result and combine it with the current piece to get the final answer

For `factorial(n)`:
- Divide: base case is `n == 0`; reduction is `factorial(n-1)`
- Invoke: `factorial(n-1)` gives `(n-1)!` — trust it
- Combine: multiply by `n` → `n * factorial(n-1)` = `n!`
<!-- source: EXTRACTED from "09-Recursion.pdf" -->

### "Trust the recursion"

The hardest mental shift in learning recursion: **do not trace through the recursive call in your head**. Instead, assume it returns the correct answer for the smaller input, and just think about how to combine it with the current step.

If `factorial(n-1)` correctly returns `(n-1)!`, what do you multiply by `n` to get `n!`? Answer: multiply by `n`. That's the whole insight.
<!-- source: EXTRACTED from "09-Recursion.pdf" -->

### Example: digit sum

```python
def digit_sum(n):
    """Sum of digits of n (n >= 0)."""
    if n < 10:
        return n          # base case: single digit
    return digit_sum(n // 10) + n % 10   # last digit + sum of rest
```

- `n % 10` gives the last digit
- `n // 10` removes the last digit (reduces the problem)
- Trust: `digit_sum(n // 10)` correctly returns the sum of all other digits
<!-- source: INFERRED — synthesized from "09-Recursion.pdf" examples -->

### Example: counting down (mutual structure with while)

```python
# Iterative
def countdown(n):
    while n >= 0:
        print(n)
        n -= 1

# Recursive equivalent
def countdown(n):
    if n < 0:
        return
    print(n)
    countdown(n - 1)
```

Both produce the same output; recursion naturally mirrors iteration for linear problems.
<!-- source: INFERRED — synthesized from "09-Recursion.pdf" -->

## Key equations / rules

- Base case: simplest input where the answer is known directly
- Recursive case: `f(n)` defined in terms of `f(n-1)` (or smaller inputs)
- Trust the recursion: assume the recursive call returns the correct answer

## Connections

- [[tree_recursion]] — multiple recursive calls per invocation
- [[control]] — while loops are the iterative alternative
- [[list]] — list recursion uses `s[0]` (first) and `s[1:]` (rest) as the divide step
- [[higher_order_function]] — HOFs can take recursive functions as arguments

## Exam relevance

- Write recursive functions for: digit operations, list operations, counting, Fibonacci variants
- Identify base case and recursive case given a skeleton
- Trace a small example manually (e.g., `factorial(3)`) — know how the call stack grows and unwinds

## Common mistakes

- Missing the base case (causes infinite recursion / stack overflow)
- Base case that never triggers (e.g., `if n == 0` when `n` decrements by 2 and can skip 0)
- Trying to mentally trace multiple levels of recursion — trust the recursion instead
- Forgetting to return the recursive result (writing `factorial(n-1)` without `return`)
