---
title: "OLTP vs OLAP"
type: concept
sources: [storage-and-retrieval]
related: [b-tree, lsm-tree, sstables, batch-processing, columnar-storage]
updated: 2026-05-02
---

# OLTP vs OLAP

*Two workload archetypes that drive opposite storage-engine choices. The same database cannot serve both well, which is why analytical workloads ended up in separate data warehouses.*

## Definition

| | **OLTP** (Online Transaction Processing) | **OLAP** (Online Analytical Processing) |
|---|---|---|
| Workload | Many small transactions | Few but huge analytical queries |
| Read pattern | Few rows by primary key | Aggregations over millions of rows |
| Write pattern | Continuous, small | Bulk loads (ETL) |
| Storage layout | **Row-oriented** | **Column-oriented** |
| Storage engine | [[b-tree|B-tree]] dominant | [[columnar-storage]], compressed |
| Latency target | ms | seconds–minutes |
| Examples | E-commerce checkout, banking ledger | Sales reporting, trend analysis |

## Why it matters

The single most important workload distinction in storage. Storage engineers choose row vs column orientation based on this dichotomy alone.

## Mechanism — why row vs column

- **Row-oriented:** all fields of a record stored together → fast point lookups (read one row to get all its fields). Bad for "average price across 100M sales" because you read every column you don't care about.
- **Column-oriented:** each column stored as its own file/array → "average price" reads one column. Heavy compression possible (run-length, dictionary encoding) because columns are usually homogeneous.

## Mechanism — why a single DB struggles to do both

OLTP needs low-latency point reads + writes; the storage layout for that (rows, B-trees) is exactly the wrong layout for OLAP scans. Doing both in one engine means losing on both.

The historical solution: keep production data in an OLTP database, then **ETL** (Extract-Transform-Load) periodically into a separate **data warehouse** that stores it column-oriented for analytics.

Modern systems blur the line — HTAP (Hybrid Transactional-Analytical Processing) systems try to serve both, but the architectural pull remains.

## Trade-offs

- **Two systems, two costs.** Running an OLTP DB plus a warehouse means double the operational load.
- **ETL latency.** The warehouse is always slightly stale.
- **Schema evolution.** Changes to the OLTP schema must propagate through ETL.

## Examples in the syllabus

- Storage and Retrieval s. 3 names the distinction explicitly: "transactional workload (write-intensive) vs analytics workload (read-intensive)."
- [[batch-processing]] (MapReduce-era) was, historically, the OLAP-side answer when warehouses couldn't handle the volume.

## Common exam framing

- "Distinguish OLTP and OLAP workloads. Why does each motivate a different storage layout?"
- "Why is column-oriented storage particularly suited to analytical queries?"
- "Why do organisations typically run OLTP and OLAP on separate systems?"

## See also

- [[b-tree]]
- [[lsm-tree]]
- [[columnar-storage]]
- [[batch-processing]]
