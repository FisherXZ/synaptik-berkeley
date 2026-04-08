---
title: Representation
course: cs61a
tags: [oop, special-methods, str, repr, dunder]
sources: [21-Representation.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

Representation refers to how Python objects display themselves as strings. `str()` gives a human-readable display; `repr()` gives a developer-friendly representation that ideally evaluates back to the original object.

## Core Explanation

**`str` vs `repr`:**

| | `str(obj)` | `repr(obj)` |
|--|-----------|------------|
| Purpose | Human-readable | Developer/debugging |
| Used by | `print()` | REPL, error messages |
| Python method | `__str__` | `__repr__` |
| Example | `'1/2'` | `'Fraction(1, 2)'` |
<!-- source: EXTRACTED from "21-Representation.pdf" -->

```python
from fractions import Fraction
half = Fraction(1, 2)

str(half)    # → '1/2'
repr(half)   # → 'Fraction(1, 2)'
print(half)  # prints: 1/2   (uses __str__)
half         # REPL shows: Fraction(1, 2)  (uses __repr__)
```
<!-- source: EXTRACTED from "21-Representation.pdf" -->

**Fallback rule:**
If `__str__` is not defined, Python uses `__repr__` for both `str()` and `print()`. So always define `__repr__` at minimum.
<!-- source: EXTRACTED from "21-Representation.pdf" -->

**Defining both on a custom class:**
```python
class Rational:
    def __init__(self, n, d):
        self.numer = n
        self.denom = d
    
    def __str__(self):
        return f'{self.numer}/{self.denom}'      # human-readable
    
    def __repr__(self):
        return f'Rational({self.numer}, {self.denom})'  # eval-able
```
<!-- source: INFERRED — synthesized from "21-Representation.pdf" -->

**Other important special methods (dunder methods):**

```python
__init__(self, ...)       # Constructor — called by ClassName(args)
__str__(self)             # Called by str(obj) and print(obj)
__repr__(self)            # Called by repr(obj) and REPL
__eq__(self, other)       # Called by == operator
__bool__(self)            # Called by bool(obj) and in if/while conditions
```
<!-- source: EXTRACTED from "21-Representation.pdf" -->

**Example — `__eq__` and `__bool__`:**
```python
class Rational:
    ...
    def __eq__(self, other):
        return self.numer * other.denom == other.numer * self.denom
    
    def __bool__(self):
        return self.numer != 0   # False if numerator is 0
```
<!-- source: INFERRED — synthesized from "21-Representation.pdf" -->

## Key Rules

- `__repr__` should ideally return a string that, when passed to `eval()`, recreates the object
- If only `__repr__` is defined, it serves as both `str` and `repr`
- All special method names start and end with double underscores ("dunder" = "double under")
- `print(obj)` calls `str(obj)`, which calls `__str__`
<!-- source: EXTRACTED from "21-Representation.pdf" -->

## Connections

- [[class]] — special methods are defined inside class bodies
- [[inheritance]] — subclasses inherit `__repr__` and `__str__` if not overridden

## Exam Relevance

- 21-Representation.pdf references Spring 2023 Midterm 2 Q2(a) with a `Letter` class — `send()` method patterns
- Predict output of `print(obj)` vs REPL display
<!-- source: EXTRACTED from "21-Representation.pdf" -->

## Common Mistakes

- Defining `__str__` but not `__repr__` — REPL output shows the default `<ClassName object at 0x...>`
- Thinking `repr(obj)` always returns Python-valid syntax — it should, but it's a convention not enforced
- Confusing `==` (calls `__eq__`) with `is` (identity check, no dunder involved)
