---
title: "Key-value store"
type: concept
sources: [data-models-nosql]
related: [document-model, hash-index, nosql-databases]
updated: 2026-05-02
---

# Key-value store

*The simplest NoSQL family: data as opaque values addressed by primary keys. Trivial to scale horizontally; useless for queries that don't go through the key.*

## Definition

A **key-value store** treats data as a giant associative array (`dict`, hash map). Every record is keyed by a unique primary key and the value is opaque to the database — usually bytes, sometimes a JSON blob.

Examples: Redis, Amazon DynamoDB, Riak, Memcached, Aerospike.

Some support **composite keys** — DynamoDB's partition-key + sort-key pair lets you store many records under one partition key and range-scan the sort key.

## Why it matters

Key-value stores are the simplest thing that scales horizontally — partition by hash of the key and you're done. They're the workhorse of caching layers (Redis, Memcached) and high-throughput operational stores (DynamoDB).

## Mechanism

- **Read by key** — fast, predictable, easy to partition.
- **Read by anything else** — not supported. Either use a secondary index (often slower, sometimes eventually consistent) or denormalise the data so the key contains what you need.
- **Persistence** — varies. Redis is in-memory with optional snapshots; DynamoDB is durable + replicated.

## Trade-offs

- **+** Simplest possible model — minimal API, easy to reason about.
- **+** Horizontal scaling is trivial: hash the key, route to the right shard.
- **+** Very high throughput, very low latency.
- **−** No native joins, secondary indexes, or aggregations.
- **−** Complex queries push complexity into the application layer.

## Examples in the syllabus

- DynamoDB composite primary key (s. 27) — the canonical illustration.
- Caches, session stores, leaderboards (Redis sorted sets).

## Common exam framing

- "Describe the key-value model. Why is it especially well-suited to horizontal scaling?"
- "What sort of query is the key-value model bad at? How do real systems work around this?"

## See also

- [[document-model]]
- [[nosql-databases]]
- [[hash-index]]
