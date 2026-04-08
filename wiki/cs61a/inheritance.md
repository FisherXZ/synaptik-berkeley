---
title: Inheritance
course: cs61a
tags: [oop, inheritance, subclass, override]
sources: [20-Inheritance.pdf]
confidence: medium
last_updated: 2026-04-08
---

## Definition

Inheritance is an OOP mechanism where a subclass automatically gains all attributes and methods of its base class, and can override or extend them selectively.

## Core Explanation

**Syntax:**
```python
class CheckingAccount(Account):    # CheckingAccount inherits from Account
    withdraw_fee = 1
    interest = 0.01                # overrides Account.interest = 0.02

    def withdraw(self, amount):    # overrides Account.withdraw
        return Account.withdraw(self, amount + self.withdraw_fee)
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**What is inherited:**
- All class attributes and methods defined on the base class
- Attributes are NOT copied — the subclass looks them up in the base class at runtime

**Attribute lookup chain for `CheckingAccount`:**
1. Look in `CheckingAccount` instance dict
2. Look in `CheckingAccount` class dict
3. Look in `Account` class dict
4. (Continue up the chain if deeper hierarchy)
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**Full example — Account and CheckingAccount:**
```python
class Account:
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance -= amount
        return self.balance

class CheckingAccount(Account):
    withdraw_fee = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_fee)
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

```python
ch = CheckingAccount("Alice")
ch.deposit(20)     # uses Account.deposit (not overridden)
ch.withdraw(5)     # uses CheckingAccount.withdraw → calls Account.withdraw(ch, 6)
ch.interest        # → 0.01  (found in CheckingAccount, not Account)
```
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**Calling base class method explicitly:**
`Account.withdraw(self, amount + self.withdraw_fee)` — pass `self` explicitly because we're calling an unbound method on the class, not via dot notation on the instance.
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

**Overriding `__init__`:**
If the subclass doesn't define `__init__`, it inherits the base class `__init__`. If it does define its own, it must explicitly call the base class `__init__` if needed:
```python
class SavingsAccount(Account):
    deposit_fee = 2
    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_fee)
```
<!-- source: INFERRED — synthesized from "20-Inheritance.pdf" -->

## Key Rules

- Subclass: `class Sub(Base):`
- Base class attributes are NOT copied — they're looked up dynamically
- Overriding a method: define a method with the same name in the subclass
- To call the base class version explicitly: `Base.method(self, args)`
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

## Connections

- [[attribute]] — inheritance extends the attribute lookup chain
- [[class]] — inheritance builds on the class/instance system

## Exam Relevance

- Given a class hierarchy, trace which method/attribute gets used for a given call
- `ch.interest` when CheckingAccount defines `interest = 0.01` and Account has `interest = 0.02` → which one?
<!-- source: EXTRACTED from "20-Inheritance.pdf" -->

## Common Mistakes

- Thinking the subclass gets a copy of base class attributes — lookup is dynamic
- Calling base class methods without passing `self`: `Account.withdraw(amount)` is wrong; needs `Account.withdraw(self, amount)`
- Assuming `super()` is used in CS 61A — the course uses explicit `Base.method(self, ...)` instead
