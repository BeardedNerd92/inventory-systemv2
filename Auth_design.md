# CountIQ Auth & Ownership Schema Plan

## Goal

Design and implement a correct, layered schema for user authentication and ownership using **opaque tokens (1↔1 per user)**.
We will build **one layer at a time** for correctness and fewer bugs.

No implementation until each layer is fully designed and validated.

---

# Build Strategy

```
User model → Token model → Item model → Transitions → Implementation
```

Each layer must be completed and validated before moving forward.

---

# System Problem

Authenticate users via opaque tokens and ensure only approved users can read/change state.

---

# Layer 1 — User Model (FOUNDATION)

## Purpose

Root identity for the system.
All ownership and auth relationships originate here.

## Schema

**users**

* id: UUID (PK, NOT NULL)
* username: VARCHAR(255) UNIQUE NOT NULL
* is_active: BOOLEAN NOT NULL
* created_at: TIMESTAMP NOT NULL
* updated_at: TIMESTAMP NOT NULL

## Invariants

* username must be unique
* user must exist before token or item
* id is immutable

## Status

* [ ] designed
* [ ] validated
* [ ] implemented

---

# Layer 2 — Token Model (1 ↔ 1)

## Purpose

Opaque bearer token for authentication.
Each user receives exactly one token on onboarding.

## Relationship

```
User (1) ↔ (1) Token
```

Enforced via:

```
UNIQUE(tokens.user_id)
```

## Schema

**tokens**

* id: UUID (PK, NOT NULL)
* user_id: UUID (FK → users.id, NOT NULL, UNIQUE)
* token_hash: CHAR(...) UNIQUE NOT NULL
* expires_at: TIMESTAMP NOT NULL (TTL)
* revoked_at: TIMESTAMP NULL
* created_at: TIMESTAMP NOT NULL
* last_used_at: TIMESTAMP NULL

## Invariants

* token belongs to exactly one user
* user has at most one token
* token invalid if revoked
* token invalid if expired

## Status

* [ ] designed
* [ ] validated
* [ ] implemented

---

# Layer 3 — Item Model (Ownership)

## Purpose

Domain objects owned by users.

## Relationship

```
User (1) → (*) Items
```

## Schema

**items**

* id: UUID (PK, NOT NULL)
* owner_id: UUID (FK → users.id, NOT NULL)
* name: VARCHAR(255) NOT NULL
* qty: INTEGER NOT NULL CHECK(qty ≥ 0)
* created_at: TIMESTAMP NOT NULL
* updated_at: TIMESTAMP NOT NULL

## Invariants

* item must belong to a user
* qty ≥ 0
* ownership immutable

## Status

* [ ] designed
* [ ] validated
* [ ] implemented

---

# Constraints

* PK, FK, NOT NULL
* UNIQUE(username)
* UNIQUE(token.user_id)
* TTL via expires_at
* revocation via revoked_at

---

# Tradeoffs

## Database (initial)

Pros:

* durability
* data integrity
* indexing (B-tree)

Cons:

* higher latency
* potential bottlenecks at scale

## Redis (future)

Pros:

* fast lookup
* low latency

Cons:

* less durable
* requires sync with DB

**Decision**
DB = source of truth
Redis = future cache layer

---

# Transition Design (later phase)

```
State Before
State After
Transition
Failure Modes
Storage
Concurrency
Tradeoffs
Contract
Query or Command
Return Type
```

---

# Mathematical Model

```
f : (State, Input) → (New State, Output)
Invariant(New State) = true
```

---

# Layer Completion Rule

A layer is only complete when:

* schema defined
* invariants defined
* relationships defined
* failure risks identified

Then and only then:

```
implementation begins
```