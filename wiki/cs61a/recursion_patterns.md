---
title: Recursion Patterns
course: cs61a
tags: [recursion, practice, hw03, exam-relevant]
sources: [hw03.py, 61a-fa25-mt1_sol.pdf]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** The concrete structural patterns for writing recursive functions in 61A — digit decomposition, tree recursion with branching, and count-ways problems.

## Core explanation

### Pattern 1: Digit decomposition

Every recursive digit problem uses the same two operations:
- `num % 10` — last digit
- `num // 10` — everything except last digit

`num_eights` is the template:

```python
def num_eights(num):
    if num % 10 == 8:
        return 1 + num_eights(num // 10)
    elif num < 10:      # base case: single digit, not 8
        return 0
    else:
        return num_eights(num // 10)
```

`digit_distance` extends this to need the *adjacent pair*:

```python
def digit_distance(num):
    if num < 10:
        return 0
    return abs(num % 10 - (num // 10) % 10) + digit_distance(num // 10)
```

Key insight: `(num // 10) % 10` gives the second-to-last digit without needing a helper. Compare two adjacent digits, then recurse.

<!-- source: EXTRACTED from "hw03.py" -->

### Pattern 2: Tree recursion (count-ways)

The canonical template from `count_dollars`:

```python
def constrained_count(sum_needed, largest_bill):
    if sum_needed == 0: return 1       # found a valid combination
    if sum_needed < 0: return 0        # overshot
    if largest_bill == None: return 0  # no more denominations
    without = constrained_count(sum_needed, next_smaller_dollar(largest_bill))
    with_it  = constrained_count(sum_needed - largest_bill, largest_bill)
    return without + with_it
```

This is the **partition / change-making** pattern. Two recursive calls:
1. Skip the current denomination entirely (move to next smaller)
2. Use the current denomination once (subtract it, stay on same denomination)

The same structure solves stairways (hw05), coin change, and any "how many ways" problem.

<!-- source: EXTRACTED from "hw03.py" -->

### Pattern 3: Interleaved sum (no mod, no loops)

`interleaved_sum` shows how to handle "odd positions get f_odd, even get f_even" without `%`:

```python
def sum_from(k):
    if k > num: return 0
    elif k == num: return f_odd(k)
    else: return f_odd(k) + f_even(k+1) + sum_from(k + 2)
return sum_from(1)
```

Key: start at 1 (odd), handle both current and next in the same call, recurse by +2.

<!-- source: EXTRACTED from "hw03.py" -->

### Pattern 4: Towers of Hanoi — the spare-peg trick

```python
def move_stack(num, start, end):
    if num == 1:
        print_move(start, end)
    else:
        other = 6 - start - end    # since start, end, other sum to 1+2+3=6
        move_stack(num-1, start, other)
        print_move(start, end)
        move_stack(num-1, other, end)
```

`other = 6 - start - end` is the elegant trick — no conditionals needed to find the spare peg.

<!-- source: EXTRACTED from "hw03.py" -->

## Key patterns

| Problem type | Base cases | Recursive structure |
|---|---|---|
| Digit property | `num < 10` | `f(num % 10) + recurse(num // 10)` |
| Count ways | `amount == 0` → 1, `amount < 0` or `no items` → 0 | `without(item) + with(item)` |
| Interleaved | `k > n` → 0 | `odd(k) + even(k+1) + recurse(k+2)` |
| Towers of Hanoi | `num == 1` | `move(n-1, start→other)`, move bottom, `move(n-1, other→end)` |

## Connections

[[higher_order_function_patterns]] [[tree_recursion_strategies]] [[generator_patterns]]

## Exam relevance

- MT1 Q3 "Saja Boys": fill-in-blank iterative pattern for digit scanning — track `odd` (max odd seen so far), return `odd == 0`
- MT1 Q4(a) `sum_sequence`: HOF recursion — `t = f(0)` starts the sequence, `while t: t, total = f(t), total + t`
- Final Q3 `feasible`: uses recursion over equation list + `any()` — the pattern is replacing the first `?` with each allowed value

<!-- source: EXTRACTED from "61a-fa25-mt1_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

## Common mistakes

- **Off-by-one on digit base case**: using `num == 0` instead of `num < 10` means single-digit numbers aren't handled correctly
- **Tree recursion order**: for `count_dollars`, the "without" branch passes `next_smaller_dollar(largest_bill)` NOT `largest_bill - 1`. The denominations are discrete.
- **Interleaved sum**: handling the last element — if `k == num`, only `f_odd(k)` (don't call `f_even(k+1)` when `k+1 > num`)
- **Hanoi**: the `other = 6 - start - end` only works when pegs are labeled 1, 2, 3

## Provenance

<!-- source: EXTRACTED from "hw03.py" -->
<!-- source: EXTRACTED from "61a-fa25-mt1_sol.pdf" -->
