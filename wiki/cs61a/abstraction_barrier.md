---
title: Abstraction Barrier
course: cs61a
tags: [abstraction, data-abstraction, practice, hw04, lab04]
sources: [hw04.py, lab04.py]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** The rule that code using a data structure must only access it through its defined constructor/selector interface — never through implementation details like direct indexing.

## Core explanation

The 61A tree is represented as `[label] + branches`, so `tree[0]` is the label and `tree[1:]` are branches. But code that uses trees **must not** use `tree[0]` or `tree[1:]` directly — it must use `label(t)` and `branches(t)`.

This is tested concretely in `balanced` from hw04:

```python
# WRONG — violates abstraction barrier
def balanced(m):
    return m[1] * total_mass(m[2][2]) == m[2] * total_mass(m[1][2])

# CORRECT — uses selector functions
def balanced(m):
    left_end, right_end = end(left(m)), end(right(m))
    torque_left = length(left(m)) * total_mass(left_end)
    torque_right = length(right(m)) * total_mass(right_end)
    return torque_left == torque_right and balanced(left_end) and balanced(right_end)
```

The `construct_check` test in hw04 literally bans `Index` operations — the autograder enforces the barrier.

<!-- source: EXTRACTED from "hw04.py" -->

### City abstraction (lab04)

`closer_city` in lab04 uses `make_city`, `get_lat`, `get_lon`, `get_name` — never `city[0]`, `city[1]`, etc.:

```python
def closer_city(lat, lon, city_a, city_b):
    new_city = make_city('arb', lat, lon)
    dist1 = distance(city_a, new_city)
    dist2 = distance(city_b, new_city)
    if dist1 < dist2:
        return get_name(city_a)
    return get_name(city_b)
```

The `change_abstraction` test switches the underlying representation from list to dict — if your code uses selectors correctly, it still works. If you indexed directly, it breaks.

<!-- source: EXTRACTED from "lab04.py" -->

### Mobile abstraction (hw04)

The mobile problem uses a multi-level abstraction:
- `mobile(left, right)` → `['mobile', left_arm, right_arm]`
- `arm(length, end)` → `['arm', length, mobile_or_planet]`
- `planet(mass)` → `['planet', mass]`

Selectors: `left(m)`, `right(m)`, `length(arm)`, `end(arm)`, `mass(planet)`, `is_planet(p)`, `is_mobile(m)`, `is_arm(s)`

`total_mass` correctly uses only selectors:
```python
def total_mass(m):
    if is_planet(m):
        return mass(m)
    return total_mass(end(left(m))) + total_mass(end(right(m)))
```

<!-- source: EXTRACTED from "hw04.py" -->

## Key patterns

1. **Always use constructors and selectors** — never index directly
2. **Test by swapping representation**: if it breaks when the underlying list becomes a dict, you violated the barrier
3. **Predicate functions first**: check `is_leaf(t)`, `is_planet(p)` before accessing fields
4. **Constructor validates**: `tree()` asserts all branches are trees; `mobile()` asserts arms; `arm()` asserts mobile or planet

## Connections

[[tree_recursion_strategies]] [[oop_class_patterns]]

## Exam relevance

- hw04 `balanced` explicitly bans `Index` in construct_check — must use `end()`, `left()`, `right()`, `length()`, `total_mass()`
- The abstraction barrier principle is why the OOP `Tree` class replaces the list tree: once you use `t.label` and `t.branches`, you can add methods without changing client code

## Common mistakes

- Writing `m[1]` instead of `left(m)` — works but fails construct_check
- Forgetting `end()`: `left(m)` returns an arm, not a planet/mobile. Need `end(left(m))` to get what's hanging
- Mixing up `length(arm)` vs `end(arm)` — `length` is the rod length (for torque), `end` is what hangs at the end

## Provenance

<!-- source: EXTRACTED from "hw04.py" -->
<!-- source: EXTRACTED from "lab04.py" -->
