---
title: Attribute
course: cs61a
tags: [oop, attribute, dot-expression, lookup]
sources: [19-Attributes.pdf, 20-Inheritance.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

An attribute is a named value associated with an object, accessed via dot notation (`obj.name`). Python distinguishes between instance attributes (per-object) and class attributes (shared across all instances).

## Core Explanation

**Instance attributes vs. class attributes:**

```python
class Account:
    interest = 0.02          # CLASS attribute — shared by all instances

    def __init__(self, holder):
        self.balance = 0     # INSTANCE attribute — unique to each instance
        self.holder = holder
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

```python
a = Account("Alice")
b = Account("Bob")

a.interest    # → 0.02  (found on class)
b.interest    # → 0.02  (same class attribute)

a.balance     # → 0     (found on instance a)
b.balance     # → 0     (found on instance b, different object)
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**Dot expression lookup rule (4 steps):**
1. Evaluate the left side to get the object
2. Look up the name on the object's **instance dictionary** first
3. If not found, look up in the **class**
4. If the value found in the class is a function, bind `self` to the instance → becomes a **bound method**
<!-- source: EXTRACTED from "19-Attributes.pdf" -->

**Assignment creates/shadows instance attributes:**
```python
Account.interest = 0.05    # Changes class attribute for ALL instances
a.interest = 0.08          # Creates INSTANCE attribute on 'a' only — shadows class attr
a.interest    # → 0.08  (found on instance, shadows class)
b.interest    # → 0.05  (class attr, because b has no instance 'interest')
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**The critical asymmetry:**
- Assigning to `instance.attr` always creates/updates an instance attribute
- Assigning to `Class.attr` updates the class attribute for all instances that don't have their own shadow
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**Class attributes as shared state:**
```python
class Counter:
    count = 0    # shared across all instances
    
    def increment(self):
        Counter.count += 1   # explicitly modifying class attr
```
<!-- source: INFERRED — synthesized from "19-Attributes.pdf" + "20-Inheritance.pdf" -->

## Key Rules

- Instance attribute lookup: instance dict → class dict → base class dicts
- Assignment `self.x = v` always writes to the instance (never class)
- Assignment `Class.x = v` writes to the class
- Methods found on the class become bound methods when accessed via instance
<!-- source: EXTRACTED from "19-Attributes.pdf" -->

## Connections

- [[class]] — classes define the template; attributes are how state is stored
- [[inheritance]] — attribute lookup chain extends through the inheritance hierarchy

## Exam Relevance

- Trace attribute lookup: which dict is checked first?
- After `a.interest = 0.08`: what does `a.interest` return? What does `Account.interest` return?
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

## Common Mistakes

- Thinking `a.interest = 0.08` changes the class attribute — it creates an instance attribute
- Forgetting that after creating an instance shadow, `Account.interest` is unchanged
- Not realizing that `del a.interest` would remove the shadow and expose the class attribute again
