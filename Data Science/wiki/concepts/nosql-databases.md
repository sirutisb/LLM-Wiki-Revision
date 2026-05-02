---
title: "NoSQL databases"
type: concept
sources: [data-models-nosql, review]
related: [document-model, key-value-store, wide-column-store, graph-model, relational-model, schema-on-read]
updated: 2026-05-02
---

# NoSQL databases

*The umbrella term for non-relational data stores that prioritise simplicity, scalability, and availability — at the cost of some of the relational guarantees.*

## Definition

**NoSQL** is shorthand for "Not Only SQL" — a family of database systems that depart from the strict relational model. The lecture's definition (s. 24): non-relational storage focused on **simplicity of design**, **scalability** (especially horizontal), and **availability**.

Four families:

- **[[document-model|Document]]** — JSON-like records (MongoDB, CouchDB, Firestore).
- **[[key-value-store|Key-value]]** — opaque values keyed by ID (Redis, DynamoDB, Riak).
- **[[wide-column-store|Wide-column]]** — tabular but schema-per-row (Cassandra, HBase, Bigtable).
- **[[graph-model|Graph]]** — vertices and edges (Neo4j, JanusGraph).

## Why it matters

NoSQL emerged in the late 2000s when web-scale systems hit limits of relational scaling and rigid schemas. The choice of NoSQL family is an architectural decision that touches every layer above the database.

## Mechanism — what they sacrifice

Relative to relational databases, NoSQL systems typically give up some combination of:

- **Strong consistency** — most are eventually consistent (see [[eventual-consistency]]). Trade-off comes from [[cap-theorem|CAP]].
- **Joins** — done in the application or denormalised away.
- **Schemas** — schema-on-read is the default for document stores.
- **ACID transactions** — many offer per-row atomicity but not multi-row transactions (this is changing — Cosmos DB, MongoDB ≥ 4.0, FaunaDB).

## Mechanism — what they gain

- **Horizontal scalability.** Sharding and replication are first-class.
- **Schema flexibility** ([[schema-on-read]]) — easier evolution.
- **Locality** — documents and column families bring related data together.
- **Higher write throughput** — most use [[lsm-tree|LSM-tree]] storage.
- **Availability** — many can serve reads/writes during network partitions (with eventual reconciliation).

## Trade-offs — the convergence

Modern relational DBs have added JSON columns, partial indexes, and horizontal-scale variants (CockroachDB, Spanner). NoSQL systems have added join-like operations and richer transactions. The hard either/or of 2010 is now a spectrum.

## Examples in the syllabus

- All four families covered (s. 25–28).
- MongoDB collections (s. 26), DynamoDB composite keys (s. 27), Cassandra wide columns (s. 28).

## Common exam framing

- "List the four main families of NoSQL databases. For each, give one example system and one application scenario."
- "What relational guarantees do most NoSQL databases sacrifice, and why?"
- "Why is horizontal scaling easier in a NoSQL database than in a traditional relational one?"

## See also

- [[document-model]]
- [[key-value-store]]
- [[wide-column-store]]
- [[graph-model]]
- [[relational-model]]
- [[cap-theorem]]
