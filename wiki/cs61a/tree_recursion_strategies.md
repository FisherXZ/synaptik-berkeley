---
title: Tree Recursion Strategies
course: cs61a
tags: [recursion, tree, practice, hw04, hw05, exam-relevant]
sources: [hw04.py, hw05.py, lab05.py, 61a-fa25-mt1_sol.pdf]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** Patterns for writing recursive functions over the 61A tree data structure — traversal, accumulation, path-finding, pruning, and mutation.

## Core explanation

The 61A tree is represented as a list: `[label, branch1, branch2, ...]`. The API:
- `label(t)` — root value
- `branches(t)` — list of subtrees
- `is_leaf(t)` — True if no branches

### Pattern 1: Tree accumulation (sum/max over paths)

`max_path_sum` from hw04 — the template for "compute something over all root-to-leaf paths":

```python
def max_path_sum(t):
    if is_leaf(t):
        return label(t)
    return label(t) + max(max_path_sum(b) for b in branches(t))
```

General form: base case returns leaf value; recursive case combines `label(t)` with the result of processing all branches using `max`, `sum`, or any aggregator.

<!-- source: EXTRACTED from "hw04.py" -->

### Pattern 2: Tree transformation (returning new tree)

`prune_leaves` from hw04 — builds a new tree, filtering branches:

```python
def prune_leaves(t, vals):
    if is_leaf(t) and label(t) in vals:
        return None
    new_branches = [prune_leaves(b, vals) for b in branches(t)]
    new_branches = [b for b in new_branches if b is not None]
    return tree(label(t), new_branches)
```

`sprout_leaves` from lab05 — adds new leaves at every existing leaf:

```python
def sprout_leaves(t, leaves):
    if is_leaf(t):
        return tree(label(t), [tree(leaf) for leaf in leaves])
    return tree(label(t), [sprout_leaves(s, leaves) for s in branches(t)])
```

Key: these return a **new tree** — they don't mutate. The list comprehension over `branches(t)` is the standard structural recursion.

<!-- source: EXTRACTED from "hw04.py" -->
<!-- source: EXTRACTED from "lab05.py" -->

### Pattern 3: Mutation (modify in place)

`prune_small` from hw06 uses the OOP Tree class — mutates `t.branches`:

```python
def prune_small(t, n):
    while len(t.branches) > n:
        largest = max(t.branches, key=lambda x: x.label)
        t.branches.remove(largest)
    for b in t.branches:
        prune_small(b, n)
```

`delete` from hw06 — delete nodes and splice their children up:

```python
def delete(t, x):
    new_branches = []
    for b in t.branches:
        delete(b, x)
        if b.label == x:
            new_branches.extend(b.branches)   # splice children up
        else:
            new_branches.append(b)
    t.branches = new_branches
```

Key: process children first (post-order), then handle the current node's branch list.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 4: Path finding with generators

`yield_paths` from hw05 — yield all root-to-target paths:

```python
def yield_paths(t, target):
    if label(t) == target:
        yield [target]
    for b in branches(t):
        for path in yield_paths(b, target):
            yield [label(t)] + path
```

Key pattern: yield the path at the target, then for every sub-path found below, prepend the current label. The `for path in yield_paths(b, target)` loop collects from the generator recursively.

<!-- source: EXTRACTED from "hw05.py" -->

### Pattern 5: Balanced tree check

From lab05:

```python
def balanced(t):
    for b in branches(t):
        if sum_tree(branches(t)[0]) != sum_tree(b) or not balanced(b):
            return False
    return True
```

Pattern: check each branch sum equals the first branch's sum, AND recurse to verify each branch is itself balanced. Leaves are trivially balanced (loop doesn't execute).

<!-- source: EXTRACTED from "lab05.py" -->

## Key patterns summary

| Goal | Pattern |
|---|---|
| Aggregate over paths | `label(t) + max/sum(f(b) for b in branches(t))` |
| Build new filtered tree | List comp over branches, filter None, return `tree(label, new_branches)` |
| Mutate tree in place | Process children first, then reassign `t.branches` |
| Find paths to target | `yield [label]` at target; `yield [label(t)] + path` for sub-paths |
| Check property recursively | `all(check(b) for b in branches(t))` pattern |

## Connections

[[recursion_patterns]] [[generator_patterns]] [[oop_class_patterns]]

## Exam relevance

- Final Q4 "Trim the Tree": `sums(t)` builds a dict mapping each node to its subtree label sum — requires `insert(b)` before computing `result[t]`; `one_cut` finds and removes the subtree whose removal brings total closest to n
- MT2 Q3 "Inclusive": tree inclusion check — dual-pointer walk over branches with `p < len(part.branches) and w < len(whole.branches)` as loop condition
- MT1 patterns: max_path_sum and prune_leaves are direct hw4 questions

<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->

## Common mistakes

- **Pruning: returning None vs empty**: `prune_leaves` returns `None` when the whole subtree is pruned — must filter None from new_branches list
- **Mutation vs. new tree**: `prune_small` mutates `t.branches` directly; `prune_leaves` returns a new tree. Mixing them up causes subtle bugs
- **yield_paths order**: yielding `[target]` first (when current node matches), then recursing into branches — not the other way around
- **balanced check**: comparing to `branches(t)[0]`, not to a fixed number — all branches must have equal sums as each other
- **Final Q4 sums**: `insert(b)` must be called before `result[t] = ...` because `result[t]` uses `result[b]` which must already exist

## Provenance

<!-- source: EXTRACTED from "hw04.py" -->
<!-- source: EXTRACTED from "hw05.py" -->
<!-- source: EXTRACTED from "lab05.py" -->
<!-- source: EXTRACTED from "hw06.py" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
