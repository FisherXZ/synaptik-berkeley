---
title: Tree Recursion
course: cs61a
tags: [tree-recursion, fibonacci, branching, exponential]
sources: [10-Tree_Recursion.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

Tree recursion is a form of recursion where a function makes two or more recursive calls per invocation, producing a branching call tree rather than a linear call chain.

## Core explanation

### What makes it "tree" recursion

In linear recursion, each call generates exactly one recursive call — the call chain is a line. In tree recursion, each call generates **two or more** recursive calls, so the call graph looks like a branching tree.

The total number of calls grows **exponentially** with the depth.
<!-- source: EXTRACTED from "10-Tree_Recursion.pdf" -->

### Canonical example: Fibonacci

```python
def fib(n):
    if n == 0:
        return 0          # base case 1
    if n == 1:
        return 1          # base case 2
    return fib(n - 1) + fib(n - 2)   # two recursive calls
```

For `fib(5)`:
- Calls `fib(4)` and `fib(3)`
- `fib(4)` calls `fib(3)` and `fib(2)`
- `fib(3)` calls `fib(2)` and `fib(1)`
- ... and so on

The call tree for `fib(n)` has roughly `2^n` nodes — exponential growth.
<!-- source: EXTRACTED from "10-Tree_Recursion.pdf" -->

### Two base cases are required

Fibonacci needs two base cases (`n == 0` and `n == 1`) because the recurrence `fib(n-1) + fib(n-2)` eventually reaches both 0 and 1. If only one base case exists, the recursion bottoms out incorrectly.

Pattern: when the reduction step can reach multiple small values, you need a base case for each.
<!-- source: EXTRACTED from "10-Tree_Recursion.pdf" -->

### Game trees — the 10-to-0 game

Tree recursion naturally models **game trees**: a game where two players alternate removing 1 or 2 from a pile of 10, and whoever reaches 0 wins.

```python
def can_win(n):
    """Return True if the current player can force a win with n left."""
    if n == 0:
        return False     # you're stuck at 0 — you lose
    if can_win(n - 1) == False or can_win(n - 2) == False:
        return True      # leave a losing position for opponent
    return False
```

A position is **winning** if you can move to a **losing** position for your opponent. This is a tree-recursive search over all possible moves.
<!-- source: EXTRACTED from "10-Tree_Recursion.pdf" -->

### Strong solution

A **strong solution** to a game computes the optimal strategy for every possible position — not just whether you can win from the start, but what move to make from any state. Tree recursion naturally enumerates all states and their outcomes.
<!-- source: EXTRACTED from "10-Tree_Recursion.pdf" -->

### Efficiency note

Naive tree recursion recomputes the same subproblems repeatedly:
- `fib(5)` computes `fib(3)` twice, `fib(2)` three times, etc.
- This is exponential in time even though the set of unique subproblems is linear

The fix (memoization / dynamic programming) is covered in later lectures.
<!-- source: INFERRED — synthesized from "10-Tree_Recursion.pdf" + standard CS theory -->

## Key equations / rules

- Fibonacci: `fib(n) = fib(n-1) + fib(n-2)` with `fib(0)=0`, `fib(1)=1`
- Call count for `fib(n)`: approximately `2^n` (exponential)
- Game tree: winning position = can move to a losing position; losing position = all moves lead to winning positions

## Connections

- [[recursion]] — tree recursion is a generalization; same base-case + trust-the-recursion principles apply
- [[list]] — tree recursion over lists uses `s[0]` and `s[1:]` as two branches

## Exam relevance

- Write tree-recursive functions for: Fibonacci variants, counting arrangements (parking problem), game trees
- Identify how many recursive calls are made at each level
- Trace small examples: `fib(4)` call tree is a standard exam diagram problem
- Parking problem (Spring 2023 Midterm 2 Q5): `count_park(n) = count_park(n-1) + count_park(n-2)` — similar structure to Fibonacci

## Common mistakes

- Forgetting a base case when the recurrence can reach both 0 and 1 (or other small values)
- Confusing linear and tree recursion — if you make two calls, draw the tree, not a line
- Expecting tree recursion to be fast — it's exponential without memoization
