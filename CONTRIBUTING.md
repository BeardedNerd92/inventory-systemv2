# Contributing — Inventory System v2

This project is a backend systems learning project focused on correctness,
state transitions, and invariants.

It is intentionally minimal and explicit.

Before contributing, please read this file.

---

## Philosophy

The goal of this project is not feature speed.
The goal is correctness under all state transitions.

Every change must preserve:

- invariants
- atomicity
- deterministic behavior
- rollback safety

If a change makes correctness harder to reason about, it should not be merged.

---

## Architecture Rules

All logic follows:

transport → service → model → database

### Transport layer (views)
Responsible for:
- parsing HTTP
- validating request shape
- mapping service results → HTTP responses

Not responsible for:
- invariants
- business logic
- database writes

---

### Service layer
Responsible for:
- state transitions
- invariants
- atomic updates
- transactions

Service functions must be deterministic.

They should return:

- object → success
- None → not found
- raise ValueError → invalid transition

---

### Model layer
Responsible for:
- invariant enforcement
- canonicalization
- persistence

All mutations must go through `model.save()`.

Never mutate database state outside service functions.

---

## Adding a New Feature

1. Define the state transition
2. Define invariants
3. Implement service function
4. Wrap mutation in `transaction.atomic()`
5. Add transport endpoint
6. Add tests

Never implement logic directly in views.

---

## Testing Expectations

Tests must verify:

- database state
- invariants preserved
- rollback on failure
- idempotency where required

We test state, not just return values.

Run tests:

```

python manage.py test

```

---

## Code Style

- explicit > clever
- small functions
- deterministic transitions
- no hidden mutation
- no silent failures

---

## Pull Requests

PRs should include:

- clear summary
- bug fixes encountered
- reasoning for changes
- invariant impact
- test results

Commit messages should be descriptive and explicit.

---

## Non-goals

This project intentionally avoids:

- unnecessary abstractions
- premature optimization
- UI frameworks
- heavy libraries

We are practicing backend systems fundamentals.

---

## Questions

If unsure where logic belongs:

- state transition → service
- parsing → view
- persistence → model
```