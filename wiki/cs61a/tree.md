---
title: Tree
course: cs61a
tags: [data-structures, recursion, abstraction]
sources: [14-Trees.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

A tree is a hierarchical data structure with a root label and zero or more branches, each of which is itself a tree. Leaves are trees with no branches.

## Core Explanation

CS 61A implements trees as nested lists using a data abstraction. The abstraction hides the representation — callers only use the constructor and selectors, not the raw list internals.

**Constructor and selectors:**

```python
def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch)
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_leaf(tree):
    return not branches(tree)

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True
```
<!-- source: EXTRACTED from "14-Trees.pdf" -->

**Building trees:**
```python
# A tree with label 3 and two leaf branches
t = tree(3, [tree(1), tree(2)])
# label(t) → 3
# branches(t) → [tree(1), tree(2)]
# is_leaf(tree(1)) → True
```
<!-- source: EXTRACTED from "14-Trees.pdf" -->

**Tree recursion pattern:**

Most tree processing follows this skeleton:
```python
def process(t):
    if is_leaf(t):
        return <base case>
    else:
        processed_branches = [process(b) for b in branches(t)]
        return <combine label(t) with processed_branches>
```

**Example — largest label:**
```python
def largest_label(t):
    if is_leaf(t):
        return label(t)
    else:
        return max([largest_label(b) for b in branches(t)] + [label(t)])
```
<!-- source: EXTRACTED from "14-Trees.pdf" -->

## Key Rules

- A tree with no branches is a **leaf**
- Every branch of a tree is itself a tree (recursive structure)
- Never access `tree[0]` or `tree[1:]` directly — always use `label()` and `branches()` (abstraction barrier)
<!-- source: EXTRACTED from "14-Trees.pdf" -->

## Connections

- [[higher_order_function_patterns]] — list comprehensions used when processing branches
- [[linked_list]] — another recursive data structure, but linear not hierarchical

## Exam Relevance

- Tree recursion problems are common: "sum all labels", "count leaves", "find max label"
- The abstraction barrier matters on exams: using `t[0]` instead of `label(t)` is wrong style even if it works
<!-- source: EXTRACTED from "14-Trees.pdf" -->

## Common Mistakes

- Forgetting to include the current node's label in aggregations (only recursing on branches)
- Treating a single leaf as `[]` instead of `tree(label)` — a leaf is still a tree
- Breaking the abstraction barrier by indexing the list directly
