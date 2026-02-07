# Inventory System v2 — Backend Systems Project

This project is a backend-only inventory system built to practice real backend engineering fundamentals: state modeling, invariants, transactional persistence, and correctness.

There is no UI. All interaction happens through HTTP endpoints using curl.

The goal of this project is not rapid feature building — it is learning how to design systems that preserve correctness under all transitions.

---

## Architecture

transport → service → validate → persist → service return

Concrete stack:

* Django (transport + models)
* Service layer (transitions + transactions)
* SQLite (persistence)

No repository layer is used.
The Django model + database are the source of truth.

---

## System Design Principles

### State Model

S = Map[id → item]
item = { id, name, qty }

All operations are state transitions:

S' = f(S, input)

---

### Invariants (truth)

The system guarantees:

* name.strip() ≠ ""
* qty ∈ ℤ
* qty ≥ 0
* name is unique

If any invariant fails:

S' = S

No mutation is allowed.

---

### Invariant Enforcement

Invariants are:

* centralized in `invariants.py`
* pure (no mutation)
* dict in → dict out
* deterministic

They are enforced at the model boundary before any database commit.

Mutation happens only at:

model.save()

---

### Transition Law

All transitions follow:

validate → commit → return

Never:

commit → fix later

This guarantees database correctness and rollback safety.

---

### Transactions

All write operations are wrapped in:

transaction.atomic()

This ensures:

valid → commit
invalid → rollback

---

## Endpoints

All interaction is done via curl.

### Create item

POST /items

Example:

curl -X POST [http://127.0.0.1:8000/items](http://127.0.0.1:8000/items) 
-H "Content-Type: application/json" 
-d '{"name":"apple","qty":5}'

Success response:

201 Created
{
"id": "...",
"name": "apple",
"qty": 5
}

Invalid input returns 400 and does not mutate state.
Duplicate names are rejected.

---

## Running Locally

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start server:
python manage.py runserver

Run tests:
python manage.py test

Tests assert database state, not just return values.

---

## Current Features

* transactional create_item
* centralized invariant enforcement
* database-enforced uniqueness
* rollback on failure
* curl-driven interaction
* state-based testing

---

## Upcoming Transitions

* delete_item(id) (idempotent)
* adjust_qty(delta) (bounded)
* authentication layer
* PostgreSQL migration

---

## Why this project exists

Most tutorials focus on frameworks and UI.
This project focuses on:

state
invariants
transactions
correctness

The goal is to build backend systems that are predictable, testable, and safe under failure.

---

## License

MIT
