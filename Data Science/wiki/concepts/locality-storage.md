---
title: "Locality (storage)"
type: concept
sources: [data-models-nosql]
related: [document-model, wide-column-store, b-tree, sstables]
updated: 2026-05-02
---

# Locality (storage)

*Storing related data together so it can be read in one go. The defining advantage — and the defining cost — of document and column-family models.*

## Definition

**Storage locality** is the property that data accessed together is stored physically close together — typically in the same disk page, same file, or same continuous byte range. It's a property of the storage layout, not the query.

## Why it matters

Disk reads come in chunks (pages, blocks). If the data you need is contiguous, one read suffices; if it's scattered across tables, every join is another seek. Locality is one of the strongest performance levers a database has.

## Mechanism — locality in different models

| Model | How locality is achieved |
|---|---|
| [[document-model|Document]] | Whole document stored as a single JSON/BSON string |
| [[wide-column-store|Wide-column]] | Column families group co-accessed columns into the same file |
| [[relational-model|Relational]] (Spanner, partitioned) | Co-location of related rows under a partition key |
| Heap-organised relational | Poor — rows scattered, joins required |

## Trade-offs

The same property cuts both ways:

- **+** Whole-object access is one read. No joins to reconstruct.
- **+** Cache-friendly — adjacent reads pre-fetch what you'll need next.
- **−** **Document loading is all-or-nothing.** When you fetch a doc, you fetch *the whole doc*. If most of it is unused, you waste IO.
- **−** Locality decisions made at write time can be wrong by read time as access patterns evolve.

## When locality bites

If you frequently update small parts of large documents, document DBs make you rewrite the whole document. That's worse than relational, which can update one column. As Kleppmann puts it: locality is good for **whole-object reads** and bad for **partial reads or updates**.

## Examples in the syllabus

- Document DBs store JSON contiguously (s. 16) — pro and con.
- Spanner offers locality in a relational model (s. 17).
- Cassandra column families (s. 17) — same idea, relational-shaped.

## Common exam framing

- "Explain the concept of locality in storage. Give one advantage and one disadvantage."
- "Why is locality not exclusive to document models? Give an example from a relational or wide-column system."
- "When does locality become a liability rather than an asset?"

## See also

- [[document-model]]
- [[wide-column-store]]
- [[b-tree]]
- [[sstables]]
