---
title: Class
course: cs61a
tags: [oop, class, object, instance, constructor]
sources: [18-Objects.pdf, 19-Attributes.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

A class is a template that defines the behavior and structure shared by all objects of that type. An object (instance) is a concrete value created from a class, with its own state.

## Core Explanation

**Defining a class:**
```python
class Rational:
    def __init__(self, n, d):
        self.numer = n
        self.denom = d
    
    def multiply(self, other):
        return Rational(self.numer * other.numer,
                        self.denom * other.denom)
```
<!-- source: EXTRACTED from "18-Objects.pdf" -->

**Key terms:**
- **Class** — the template (defines structure and behavior)
- **Object / instance** — a single value created from the class
- **Method** — a function defined inside a class; accessed via dot notation
- **`__init__`** — the constructor; called automatically when you do `Rational(1, 2)`
- **`self`** — refers to the specific instance being operated on; always the first parameter of methods
<!-- source: EXTRACTED from "18-Objects.pdf" -->

**Creating and using an instance:**
```python
half = Rational(1, 2)     # __init__ is called with n=1, d=2
half.numer                # → 1   (instance attribute)
half.denom                # → 2
half.multiply(Rational(2, 3))  # → Rational(2, 6)
```
<!-- source: EXTRACTED from "18-Objects.pdf" -->

**How method calls work:**
```python
half.multiply(other)
# Python translates this to:
Rational.multiply(half, other)
# 'half' is automatically passed as 'self'
```
<!-- source: INFERRED — synthesized from "18-Objects.pdf" -->

**Object state:**
Each instance has its own copy of instance attributes. Mutating one instance does not affect another:
```python
a = Rational(1, 2)
b = Rational(3, 4)
a.numer = 99    # only affects 'a', not 'b'
```
<!-- source: INFERRED — synthesized from "18-Objects.pdf" -->

## Key Rules

- `__init__` is called by Python immediately after the object is created
- `self` is the instance — every method gets it implicitly as the first argument
- Dot notation (`obj.method()`) automatically passes the object as `self`
<!-- source: EXTRACTED from "18-Objects.pdf" -->

## Connections

- [[attribute]] — details on instance vs. class attribute lookup rules
- [[inheritance]] — how subclasses extend or override class behavior
- [[representation]] — `__str__` and `__repr__` control how objects display

## Exam Relevance

- Trace through `__init__` to determine what attributes an instance has after creation
- Understand that `obj.method(arg)` is `Class.method(obj, arg)`
<!-- source: EXTRACTED from "18-Objects.pdf" -->

## Common Mistakes

- Forgetting `self` as the first parameter of every method definition
- Calling `__init__` directly: `Rational.__init__(half, 1, 2)` is valid but unusual; just use `Rational(1, 2)`
- Thinking `self` is a special keyword — it's a convention; any name works, but `self` is universal
