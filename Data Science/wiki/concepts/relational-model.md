---
title: "Relational model"
type: concept
sources: [data-models-nosql, review]
related: [document-model, graph-model, schema-on-read, nosql-databases, b-tree]
updated: 2026-05-02
---

# Relational model

*Data as tables of rows, related by foreign keys, queried with SQL. Strong on joins and many-to-many relationships; weak on schema evolution and the object-table impedance mismatch.*

## Definition

The **relational model** (Codd, 1970) represents data as **relations** (tables): a fixed set of **attributes** (columns) and a multi-set of **tuples** (rows). Relationships between tables are expressed by **foreign keys** (a column whose value matches a primary key in another table). Queries are written in SQL.

## Why it matters

Forty-plus years of relational dominance means most production data still lives in relational databases (PostgreSQL, MySQL, SQL Server, Oracle). Knowing what relational models are good and bad at frames every NoSQL trade-off in this module.

## Mechanism — strengths

- **Joins.** Many-to-many relationships drop out for free. Want all the connections of users in London? One join.
- **Constraints.** Schemas enforce invariants — types, uniqueness, foreign-key referential integrity, NOT NULL. The DB refuses bad data.
- **Mature ecosystem.** Drivers, ORMs, query optimisers, tooling.
- **ACID transactions** — see [[acid-properties]].

## Mechanism — weaknesses

- **Object-relational impedance mismatch.** Application objects don't map cleanly to flat rows. ORMs (Hibernate, SQLAlchemy, ActiveRecord) translate, but leakily.
- **Schema migrations are painful.** ALTER TABLE on a 100M-row table can be slow and require downtime. (Modern DBs have improved this.)
- **Rigid schema.** Adding a field means changing the schema for *every* row.
- **One-to-many requires extra tables or JSON columns** — which is fine, but inelegant compared to a document.

## Mechanism — modelling LinkedIn-style data

Three options for the User → Positions one-to-many relationship:

1. **Normalised:** separate `Position` table with a `user_id` foreign key. Classic. Flexible, supports indexing on positions.
2. **Structured field:** store as a JSON or XML column inside `User`. Modern SQL supports indexing and querying inside (PostgreSQL ≥ 9.3, MySQL ≥ 5.7).
3. **Blob column:** stuff JSON into a TEXT field. Simple but the DB can't see inside.

## Trade-offs vs document/graph

See [[relational-vs-document]] for the head-to-head; the short version: relational wins on relationships and constraints, document wins on locality and schema evolution, graph wins on traversal-heavy queries.

## Examples in the syllabus

- LinkedIn profile modelling (s. 5–8) — the canonical example.
- The starting point for every NoSQL conversation in the lecture.

## Common exam framing

- "What is the object-relational impedance mismatch? Give one example."
- "Compare the three ways of modelling a one-to-many relationship in a relational database."
- "Why are schema migrations expensive in a large relational database?"

## See also

- [[document-model]]
- [[graph-model]]
- [[schema-on-read]]
- [[acid-properties]]
