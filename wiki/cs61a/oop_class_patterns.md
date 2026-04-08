---
title: OOP Class Patterns
course: cs61a
tags: [oop, classes, inheritance, practice, hw06, lab06, lab07, exam-relevant]
sources: [hw06.py, lab06.py, lab07.py, 61a-fa25-mt2_sol.pdf, 61a-fa25-final_sol.pdf]
confidence: low
last_updated: 2026-04-08
---

**One-line definition:** The concrete OOP implementation patterns in 61A — class variables vs instance variables, inheritance + super(), stateful instance design, and class-level shared state.

## Core explanation

### Pattern 1: Stateful class with transaction history

`BankAccount` from hw06 — the canonical pattern for tracking history via a list attribute:

```python
class BankAccount:
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
        self.transactions = []      # starts empty

    def deposit(self, amount):
        self.transactions.append(Transaction(self.next_id(), self.balance, self.balance + amount))
        self.balance += amount
        return self.balance

    def next_id(self):
        return len(self.transactions)   # ID = count of existing transactions
```

Key: record the transaction BEFORE updating balance? No — record with `(before=self.balance, after=self.balance + amount)`, then update. The `next_id` is simply `len(self.transactions)`.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 2: VendingMachine — branching on state

`VendingMachine` from hw06 — multiple state flags checked in priority order:

```python
def vend(self):
    if self.stock == 0:
        return 'Nothing left to vend. Please restock.'
    difference = self.price - self.balance
    if difference > 0:
        return f'Please add ${difference} more funds.'
    message = f'Here is your {self.product}'
    if difference != 0:
        message += f' and ${-difference} change'
    self.balance = 0
    self.stock -= 1
    return message + '.'
```

Key: check stock first, then funds. The change calculation is `−difference` because `difference = price − balance` which is negative when overpaid.

<!-- source: EXTRACTED from "hw06.py" -->

### Pattern 3: Inheritance + super()

`FreeChecking` from lab07 — overriding `withdraw` with a counter:

```python
class FreeChecking(Account):
    withdraw_fee = 1
    free_withdrawals = 2

    def __init__(self, account_holder):
        super().__init__(account_holder)
        self.withdrawals = 0

    def withdraw(self, amount):
        self.withdrawals += 1
        fee = self.withdraw_fee if self.withdrawals > self.free_withdrawals else 0
        return super().withdraw(amount + fee)
```

Alternate (cleaner) version without overriding `__init__`:

```python
def withdraw(self, amount):
    self.free_withdrawals -= 1
    if self.free_withdrawals >= 0:
        return super().withdraw(amount)
    return super().withdraw(amount + self.withdraw_fee)
```

Key: `super().withdraw(amount + fee)` delegates to the parent — don't reimplement the balance check.

<!-- source: EXTRACTED from "lab07.py" -->

### Pattern 4: Class variable as shared state

`Mint` and `Coin` from lab06 — class variable `present_year` is shared across all instances:

```python
class Mint:
    present_year = 2025

    def __init__(self):
        self.update()

    def update(self):
        self.year = Mint.present_year   # copy class var to instance var

class Coin:
    cents = None  # overridden by subclasses

    def worth(self):
        return self.cents + max(0, Mint.present_year - self.year - 50)
```

Key trap: `Mint.present_year = 2105` changes the class variable, but existing mint instances still have their OLD `self.year` until `mint.update()` is called. The coin's `worth()` always reads `Mint.present_year` live.

<!-- source: EXTRACTED from "lab06.py" -->

### Pattern 5: Class-level registry (DiscGroup)

Final Q7 "Students" — `DiscGroup.groups` is a class-level list shared across all instances:

```python
class DiscGroup:
    groups = []   # class variable — ALL DiscGroup instances share this

    def __init__(self, keyword):
        self.students = []
        self.keyword = keyword
        self.id = len(DiscGroup.groups)   # sequential ID
        DiscGroup.groups.append(self)     # register in class-level list
```

`Student.__init__` searches `DiscGroup.groups` for an existing group with the right keyword before creating a new one.

<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

### Pattern 6: OOP inheritance on exam (PizzaParlor)

MT2 Q5 — `MegaParlor` inherits from `Parlor` and overrides `cook`:

```python
class MegaParlor(Parlor):
    def __init__(self, price):
        self.name, self.price, self.profit = "MEGA", price, 0

    def cook(self, q):
        return 0    # can always cook any quantity; overload = 0
```

The `order` method calls `self.cook(quantity)` — using `self.cook` means the overridden version is dispatched based on the actual class. This is standard polymorphism.

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->

## Key patterns

| Pattern | Key implementation detail |
|---|---|
| Transaction history | `self.transactions.append(...)` before or after update; use `len(self.transactions)` as next ID |
| State-guarded methods | Check stock/funds in priority order; return early |
| Inheritance | `super().__init__(...)` in `__init__`; `super().method(...)` to delegate |
| Class variable trap | Class var is shared; changing it affects all instances that read it via class name |
| Class-level registry | `ClassName.list.append(self)` in `__init__` for global tracking |

## Connections

[[linked_list_patterns]] [[abstraction_barrier]]

## Exam relevance

- MT2 Q5 Pizza Parlor: tests `self.cook()` polymorphism, `self.alt.order(rest, self)` delegation, profit arithmetic
- Final Q7 Students: tests class variable as registry, `DiscGroup.groups` iteration, sequential ID with `len(groups)`
- Lab06 Mint/Coin: class var vs instance var distinction — classic exam trap

<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->

## Common mistakes

- **Class var vs instance var**: `self.free_withdrawals -= 1` creates an instance variable that shadows the class variable — subsequent instances still have the original class value
- **super() call order**: call `super().__init__()` before accessing `self.balance` (which the parent sets up)
- **Mint.update()**: `self.year = Mint.present_year` at call time — if you don't call `update()`, the mint's stamp stays at its creation year
- **Pizza Parlor cook()**: `overload = max(0, q - self.pizzas)` not `abs(q - self.pizzas)` — overload is zero if parlor has enough
- **DiscGroup.groups vs self.groups**: class variable access — `DiscGroup.groups` is preferred; `self.groups` also works but is ambiguous

## Provenance

<!-- source: EXTRACTED from "hw06.py" -->
<!-- source: EXTRACTED from "lab06.py" -->
<!-- source: EXTRACTED from "lab07.py" -->
<!-- source: EXTRACTED from "61a-fa25-mt2_sol.pdf" -->
<!-- source: EXTRACTED from "61a-fa25-final_sol.pdf" -->
