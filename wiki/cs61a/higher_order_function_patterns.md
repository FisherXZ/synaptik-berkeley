---
title: Higher-Order Function Patterns
course: cs61a
tags: [functions, higher-order, practice, hw02]
sources: [hw02.py]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** Techniques for building, composing, and abstracting over functions as first-class values — the concrete coding moves that show up in every homework and exam.

## Core explanation

Higher-order functions (HOFs) take or return other functions. The 61A homework patterns go well beyond the definition — they involve specific structural idioms that are worth naming and memorizing as patterns.

### Pattern 1: The accumulator loop

The `accumulate` function in hw02 is the canonical template. It shows how any fold (sum, product, anything) can be expressed uniformly:

```python
def accumulate(fuse, start, n, term):
    total, k = start, 1
    while k <= n:
        total, k = fuse(total, term(k)), k + 1
    return total
```

Key moves:
- `start` is the identity element for `fuse` (0 for add, 1 for mul)
- `term` maps index → value; `fuse` combines running total with new value
- `summation` and `product` are just `accumulate(add, 0, ...)` and `accumulate(mul, 1, ...)`

<!-- source: EXTRACTED from "hw02.py" -->

### Pattern 2: Closure-based function factory

`make_repeater` from hw02 — returning a function that closes over its arguments:

```python
def make_repeater(f, n):
    def repeater(x):
        k = 0
        while k < n:
            x, k = f(x), k + 1
        return x
    return repeater
```

The inner function `repeater` closes over both `f` and `n`. This is the standard pattern for creating configurable functions.

<!-- source: EXTRACTED from "hw02.py" -->

### Pattern 3: Choosing a function based on a condition

From hw01 — selecting which function to call, instead of branching inside the call:

```python
def a_plus_abs_b(a, b):
    if b < 0:
        f = sub
    else:
        f = add
    return f(a, b)   # single return, f varies
```

Exam note: the constraint was that the function body must have exactly one `return` statement. This forces the pattern of assigning the function to a variable.

<!-- source: EXTRACTED from "hw01.py" -->

### Pattern 4: Anonymous factorial (Y-combinator style)

The most advanced HOF pattern in hw03 — achieving recursion without named functions or assignment:

```python
(lambda f: lambda k: f(f, k))(lambda f, k: k if k == 1 else mul(k, f(f, sub(k, 1))))
```

The trick: pass `f` to itself so it can call itself. `f(f, k)` is the recursive call. This appears on exams as a fill-in-the-blank on lambda expressions.

<!-- source: EXTRACTED from "hw03.py" -->

## Key patterns

| Pattern | When to use | Core structure |
|---|---|---|
| Accumulator | Sum/product/any fold over 1..n | `total = start; while k <= n: total = fuse(total, term(k))` |
| Factory | Return a configured function | `def outer(config): def inner(x): ...use config... return inner` |
| Function selection | Choose behavior at call time | `f = op_a if cond else op_b; return f(args)` |
| Self-application | Recursion without names | `(lambda f: f(f))(lambda f: ...)` |

## Connections

[[recursion_patterns]] [[lambda_and_closures]] [[abstraction_barrier]]

## Exam relevance

- MT1 Q4 "We're Going Up, Up, Up": entire problem is HOF manipulation — `sum_sequence`, `cap`, `reverse` all require understanding next-function encodings
- MT1 Q1 WWPD: tests closure — `make_something(print)(8)` requires tracing which `f` is captured
- Final Q1: `times(a, b, c)` tests closure + variable rebinding (key trap: `x = a`, then `x = b`, then `x = c` — `f` still closes over the original `a`)

<!-- source: EXTRACTED from "61a-fa25-mt1_sol.pdf" -->

## Common mistakes

- Confusing `fuse(total, term(k))` order — for non-commutative fuse, order matters
- In `make_repeater`, forgetting that `n=0` means no applications (return `x` unchanged)
- In the self-application lambda, writing `f(k)` instead of `f(f, k)` — `f` needs itself as first argument
- On MT1 Q1(b): `make_something(print)` — `print` is truthy, so the `if f(about)` branch runs, rebinding `f`. Students often miss that `f(about)` side-effects (prints 6) AND reassigns `f`

## Provenance

<!-- source: EXTRACTED from "hw01.py" -->
<!-- source: EXTRACTED from "hw02.py" -->
<!-- source: EXTRACTED from "hw03.py" -->
<!-- source: EXTRACTED from "61a-fa25-mt1_sol.pdf" -->
