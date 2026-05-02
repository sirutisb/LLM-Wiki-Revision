---
title: "Wide-column store"
type: concept
sources: [data-models-nosql]
related: [document-model, key-value-store, nosql-databases, partitioning, locality-storage]
updated: 2026-05-02
---

# Wide-column store

*Tables of rows and columns — but the columns can vary per row, and physical layout groups columns into "families" for locality. Cassandra, HBase, Bigtable.*

## Definition

A **wide-column store** organises data in tables, rows, and columns — superficially relational — but with two big differences:

1. **Schema is per-row.** The set of columns can vary from one row to the next. New columns can be added at any time.
2. **Column families** group columns that are physically stored together (locality). Different families can have different storage characteristics.

Examples: Apache Cassandra, Apache HBase, Google Bigtable, ScyllaDB.

## Why it matters

Wide-column stores combine the schema flexibility of NoSQL with a tabular query model that's easier to reason about than pure key-value. They scale horizontally (Cassandra is famously linearly scalable) and are widely used for time-series and very high-throughput workloads.

## Mechanism — structure

```
                   row key                column family A          column family B
                                          (frequently read)       (rarely read)
                  -------                 ------------------      ------------
                  user42                  name=H, email=h@…       last_login=2026-04-30, ...
                  user99                  name=Y                  ipaddr=…, …, …, ...
```

- Each row is identified by a **row key** (often hashed for partitioning).
- Each column family is stored in a separate file/region — read just the family you need.
- Inside a family, columns are sparse and per-row.

## Mechanism — locality (column families)

Column families let you **co-locate** columns that are usually accessed together. Reading "name + email" from family A doesn't pay the cost of reading family B. This is the same locality argument as [[document-model|document models]] (s. 17 of the lecture says so explicitly: column families "manage locality in similar ways").

## Trade-offs

- **+** Linear horizontal scaling. Cassandra's reputation rests here.
- **+** Schema flexibility per row.
- **+** [[lsm-tree|LSM-tree]] storage internally → very high write throughput.
- **−** Limited query model — row-key primary access; secondary indexes are limited.
- **−** Strong eventual consistency by default; tuning consistency is non-trivial.
- **−** Joins are not supported.

## Examples in the syllabus

- s. 28 — wide-column row/column structure.
- Cassandra is referenced in [[partitioning]] (s. 4) as an example NoSQL using "vnodes."

## Common exam framing

- "Explain the structure of a wide-column store. How does it differ from a relational table?"
- "What is a column family and why does it help performance?"
- "Why are wide-column stores well-suited to high-throughput, write-heavy workloads?"

## See also

- [[document-model]]
- [[key-value-store]]
- [[nosql-databases]]
- [[lsm-tree]]
- [[partitioning]]
