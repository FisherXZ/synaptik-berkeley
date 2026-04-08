---
title: Mutability
course: cs61a
tags: [lists, mutation, identity, state]
sources: [15-Mutability.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

Mutability is the property of an object that allows its contents to be changed in place after creation. Python lists are mutable; strings and tuples are not.

## Core Explanation

**List mutation methods** (modify the list in place, return `None`):

```python
s = [2, 3, 4]
s.append(5)        # s is now [2, 3, 4, 5]  — adds one element to end
s.extend([6, 7])   # s is now [2, 3, 4, 5, 6, 7]  — adds all elements of iterable
s.remove(3)        # s is now [2, 4, 5, 6, 7]  — removes first occurrence
s.pop()            # returns 7, s is now [2, 4, 5, 6]  — removes and returns last
s.pop(0)           # returns 2, s is now [4, 5, 6]  — removes by index
s[0] = 99          # s is now [99, 5, 6]  — index assignment
```
<!-- source: EXTRACTED from "15-Mutability.pdf" -->

**Mutation vs. creating a new list:**

```python
# This creates a NEW list — original unchanged:
s = [1, 2, 3]
t = s + [4]        # t = [1, 2, 3, 4], s = [1, 2, 3]

# This MUTATES the existing list:
s.append(4)        # s = [1, 2, 3, 4], same object
```
<!-- source: EXTRACTED from "15-Mutability.pdf" -->

**Identity (`is`) vs. equality (`==`):**

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b   # True  — same values
a is b   # False — different objects in memory
a is c   # True  — c points to the same object as a

a.append(4)
# a is now [1, 2, 3, 4]
# c is now [1, 2, 3, 4]  — same object!
# b is still [1, 2, 3]   — different object
```
<!-- source: EXTRACTED from "15-Mutability.pdf" -->

**Why it matters — aliasing:**
When two names refer to the same mutable object, mutating through one name affects what the other name sees. This is called aliasing and is a common source of bugs.

## Key Rules

- `append(x)` adds a single element; `extend(iterable)` adds each element of an iterable
- `is` checks object identity (same memory address); `==` checks value equality
- Mutable default arguments are a trap: `def f(lst=[]):` reuses the same list across calls
<!-- source: EXTRACTED from "15-Mutability.pdf" -->

## Connections

- [[linked_list]] — linked lists support O(1) insertion mid-structure; Python lists do not
- [[class]] — instances are mutable objects; instance attribute assignment is mutation

## Exam Relevance

- Common question type: trace through mutations and identify the final state of all names
- `is` vs `==` tested directly: `a = [1,2]; b = a; a is b` → True
<!-- source: EXTRACTED from "15-Mutability.pdf" -->

## Common Mistakes

- Thinking `s.extend([4])` is the same as `s + [4]` — extend mutates, `+` creates new
- Forgetting that `append` and `extend` return `None`, not the modified list
- Using `is` when you mean `==` for value comparison
