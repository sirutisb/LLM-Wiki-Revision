---
title: "Schema-on-write"
type: concept
sources: [data-models-nosql]
related: [relational-model, schema-on-read, acid-properties]
updated: 2026-05-06
---

# Schema-on-write

*The structure of the data is strictly enforced by the database management system (DBMS) at the time of insertion or update. Writes that do not conform to the predefined schema are rejected.*

## Definition

In a **schema-on-write** system (traditionally relational databases like PostgreSQL or MySQL), the data structure (tables, columns, types, and constraints) must be defined explicitly before any data can be stored.

- **Enforcement**: The database engine validates every incoming record against the schema.
- **Contract**: The schema acts as a formal contract between the database and all applications that interact with it.

## Mechanism

### Schema Definition
Data is organized into tables with fixed columns and data types.
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0)
);
```

### Schema Evolution
Changing the structure requires a **migration**.
- **Adding a column**: `ALTER TABLE products ADD COLUMN description TEXT;`
- **Renaming/Removing**: Requires careful coordination to avoid breaking application code.
- **Impact**: On large datasets, migrations can be slow (locking tables) or require "online" migration tools (s. 14).

## Rationale

1. **Data Integrity**: Ensures that no "junk" data enters the system. All records are guaranteed to have the required fields in the correct format.
2. **Simplified Readers**: Because the database guarantees the structure, application code (the "readers") can be simpler and doesn't need to handle missing fields or type mismatches.
3. **Optimisation**: The database can use the fixed structure to optimize storage (e.g., fixed-width fields) and indexing.

## Trade-offs

- **+ High Quality**: Errors are caught early (at write time).
- **+ Predictability**: The structure is stable and documented by the DDL.
- **− Rigidity**: Changing the schema is a heavy-weight process.
- **− Impedance Mismatch**: Often requires mapping complex application objects to flat tables (joins).

## Exam Framing

- Often contrasted with [[schema-on-read]] in the context of Relational vs NoSQL.
- Focus on the "migration pain" as a driver for the adoption of [[document-model]] databases.

## See also

- [[relational-model]]
- [[schema-on-read]]
- [[acid-properties]]
