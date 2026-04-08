---
title: Environment Diagrams
course: cs61a
tags: [environment, frames, name-lookup, scope]
sources: [02-Functions.pdf, 05-Environments.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

An environment diagram is a precise visual model of Python's name-binding state: a sequence of frames, each mapping names to values, used to trace exactly what a program does.

## Core explanation

### Frames

A **frame** is a mapping from names to values. Every Python program has:

1. **Global frame** — created when the program starts; holds all top-level bindings
2. **Local frame** — created each time a function is called; holds the function's parameters and local names

Frames form a chain. Each local frame has a **parent frame** (the frame where the function was *defined*, not where it was called).
<!-- source: EXTRACTED from "02-Functions.pdf" -->

### How name lookup works

When Python encounters a name:
1. Look it up in the **current frame** first
2. If not found, follow the chain to the **parent frame**
3. Keep going up to the global frame
4. If still not found: `NameError`

This is the **environment** of a function call: the current frame plus all its ancestors up to global.
<!-- source: EXTRACTED from "05-Environments.pdf" -->

### Drawing an environment diagram — 4 steps

For each **assignment statement** `x = expr`:
1. Evaluate the right-hand side expression
2. Bind the name `x` to the resulting value in the current frame

For each **function definition** `def f(params): body`:
1. Draw a function object: `f` with formal params and parent = current frame
2. Bind the name `f` to that function object in the current frame

For each **function call** `f(arg1, arg2)`:
1. Draw a new frame: label it with the function name and a frame number
2. Set the frame's **parent** = the function's defined-in frame (NOT the calling frame)
3. Bind each parameter name to its argument value in the new frame
4. Execute the body; any assignments create new bindings in this frame
<!-- source: EXTRACTED from "05-Environments.pdf" -->

### Parent frames for higher-order functions

When a function is returned from another function and called later, the parent frame is **where it was defined**, which may be a frame that has already returned.

```python
def make_adder(n):       # frame 1: n = 5
    def adder(k):        # adder's parent = frame 1
        return k + n
    return adder

add5 = make_adder(5)
add5(3)  # new frame: k=3, parent=frame 1 → finds n=5 there → returns 8
```

The local frame for `adder` can still look up `n` in frame 1 even after `make_adder` has returned.
<!-- source: EXTRACTED from "05-Environments.pdf" -->

### Box-and-pointer notation for lists

Lists in environment diagrams are drawn as a row of adjacent boxes, one per element.
- Each box contains a primitive value directly, or an arrow pointing to a compound value (another list, function, etc.)
- Nested lists: the outer list box points to the inner list's own row of boxes
<!-- source: EXTRACTED from "12-Containers.pdf" -->

## Key equations / rules

- **Parent of a function** = the frame where the `def` statement executed
- **Environment of a call** = new local frame → parent frame → ... → global frame
- **Name lookup direction**: always current → parent → ... → global (never child or sibling)

## Connections

- [[function]] — def statements create function objects that record their parent
- [[higher_order_function]] — returned functions retain access to their defining frame
- [[control]] — if/while inside a function execute in that function's frame

## Exam relevance

- Drawing environment diagrams is a standard exam problem type
- Watch parent frame assignments for nested `def` — the parent is where the inner `def` lives, not where the outer function was called
- Returning a locally defined function (closure) — the returned function's parent is the enclosing frame

## Common mistakes

- Confusing the **calling** frame with the **parent** frame: `f` calls `g`, but g's parent is where `g` was *defined*
- Forgetting to bind parameters before executing the body
- Not drawing a new frame for each separate call — each call is independent
