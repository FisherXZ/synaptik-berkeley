---
title: Functions
course: cs61a
tags: [functions, def, parameters, return, abstraction]
sources: [02-Functions.pdf, 04-Higher-Order_Functions.pdf, 06-Functional_Abstraction.pdf, 07-Function_Examples.pdf]
confidence: low
last_updated: 2026-04-08
---

## One-line definition

A function is a named, reusable block of code that takes inputs (parameters), performs a computation, and returns a value.

## Core explanation

### def statement

Defines a new function and binds it to a name in the current frame.

```python
def <name>(<parameters>):
    """<docstring>"""
    <body>
    return <expression>
```

Execution: Python evaluates the `def` statement, creates a function object, and binds `<name>` to it in the current frame. The body is NOT executed yet — only when the function is called.
<!-- source: EXTRACTED from "02-Functions.pdf" -->

### Call expressions

```
<operator>(<operand1>, <operand2>, ...)
```

Evaluation rule:
1. Evaluate the operator (should produce a function)
2. Evaluate all operands left-to-right
3. Apply the function to the argument values
<!-- source: EXTRACTED from "02-Functions.pdf" -->

### Parameters vs. arguments

- **Parameters**: names listed in the `def` header (`def f(x, y)` — x and y are parameters)
- **Arguments**: actual values passed at call time (`f(3, 4)` — 3 and 4 are arguments)
- Parameters are bound to argument values in the new local frame when the function is called
<!-- source: EXTRACTED from "02-Functions.pdf" -->

### Return values

- `return <expr>` exits the function and produces the return value
- A function without an explicit `return` returns `None`
- `print(x)` displays output but evaluates to `None` — do not confuse with `return x`
<!-- source: EXTRACTED from "02-Functions.pdf" -->

### Optional arguments (default parameter values)

```python
def greet(name, greeting="Hello"):
    return greeting + ", " + name
```

Parameters with defaults can be omitted at call time; they take the default value.
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

### Conditional expressions

```python
<then_exp> if <test_exp> else <else_exp>
```

Evaluation: evaluate `test_exp`; if truthy, evaluate and return `then_exp`; otherwise evaluate and return `else_exp`. One-liner version of `if/else`.

```python
abs_x = x if x >= 0 else -x
```
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

### Returning multiple values

Python allows returning a tuple implicitly:
```python
def min_max(s):
    return min(s), max(s)

lo, hi = min_max([3, 1, 4, 1, 5])
```
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

### compose

Higher-order pattern: composing two functions into one:
```python
def compose(f, g):
    def h(x):
        return f(g(x))
    return h
```
<!-- source: EXTRACTED from "07-Function_Examples.pdf" -->

## Key rules

- All expressions in a `def` header are evaluated when the `def` is executed, but the **body executes only on call**
- Each call creates a brand-new local frame, independent of prior calls
- DRY: Don't Repeat Yourself — if you write the same logic twice, make it a function
<!-- source: EXTRACTED from "06-Functional_Abstraction.pdf" -->

## Connections

- [[environment_diagram]] — how frames are created and names are looked up
- [[higher_order_function]] — functions as arguments and return values
- [[functional_abstraction]] — spec (what vs. how)
- [[boolean]] — truthiness used in conditional expressions
- [[control]] — if/else and while inside function bodies

## Exam relevance

- Distinguish `print` vs `return` — a very common exam trap
- `return` without a value (or no return) gives `None`; using that `None` in arithmetic crashes
- Know the evaluation order for call expressions (operator first, then operands left-to-right)

## Common mistakes

- Confusing `print` with `return`: `print` has a side effect (displays) but the function still returns `None`
- Forgetting that the body does not execute at definition time — only at call time
- Thinking parameters are global — they exist only inside the function's local frame
