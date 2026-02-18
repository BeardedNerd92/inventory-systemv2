# auth_schema.md

## AUTH + OWNERSHIP SCHEMA DIAGRAM

```
                    ┌──────────────────────────┐
                    │          users           │
                    ├──────────────────────────┤
                    │ id          UUID  PK     │
                    │ username    VARCHAR UQ   │
                    │ is_active   BOOL  NN     │
                    │ created_at  TS    NN     │
                    │ updated_at  TS    NN     │
                    └───────────┬──────────────┘
                                │
                                │ 1
                                │
                                │
                                │ 1
                    ┌───────────▼──────────────┐
                    │          tokens          │
                    ├──────────────────────────┤
                    │ id          UUID  PK     │
                    │ user_id     UUID  FK,UQ  │
                    │ token_hash  ...   UQ,NN  │
                    │ expires_at  TS    NN     │
                    │ revoked_at  TS    NULL   │
                    │ created_at  TS    NN     │
                    │ last_used   TS    NULL   │
                    └───────────┬──────────────┘
                                │
                                │
                                │
                                │
                                │
                    ┌───────────▼──────────────┐
                    │           items          │
                    ├──────────────────────────┤
                    │ id          UUID  PK     │
                    │ owner_id    UUID  FK,NN  │
                    │ name        VARCHAR NN   │
                    │ qty         INT    NN    │
                    │ created_at  TS     NN    │
                    │ updated_at  TS     NN    │
                    └──────────────────────────┘
```

## RELATIONSHIPS

User (1) ↔ (1) Token
User (1) → (*) Items

## CONSTRAINT LEGEND

PK  = Primary Key
FK  = Foreign Key
UQ  = Unique
NN  = Not Null
TS  = Timestamp
