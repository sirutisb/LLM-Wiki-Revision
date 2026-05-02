---
title: "Relational vs document vs graph"
type: comparison
sources: [data-models-nosql-2025]
related: [relational-model, document-model, graph-model, nosql-databases, schema-on-read]
updated: 2026-05-02
---

# Relational vs document vs graph

*Three data models, each optimised for a different shape of data and access pattern — rows and joins, hierarchical documents, or deeply connected networks.*

## Summary

Use **relational** for structured, normalised data with complex multi-table queries and strong consistency requirements. Use **document** for hierarchical, self-contained data where locality matters and schema flexibility is valuable. Use **graph** when the relationships between entities are the primary focus — social networks, fraud graphs, recommendation engines.

## Comparison table

| Dimension | Relational | Document | Graph |
|---|---|---|---|
| **Data unit** | Row in a table | JSON/BSON document | Vertex + edges |
| **Schema** | Schema-on-write (rigid, enforced) | Schema-on-read (flexible) | Schema flexible |
| **Joins** | Native, efficient (foreign keys) | Limited / manual | Traversals (first-class) |
| **Best for** | Normalised, many-to-many | Hierarchical, one-to-many | Highly connected, many-to-many |
| **Locality** | Spread across tables | Document self-contained | Depends on traversal |
| **Consistency** | Strong (ACID transactions) | Varies | Varies |
| **Scalability** | Vertical (historically) | Horizontal (sharding) | Depends on implementation |
| **Examples** | PostgreSQL, MySQL | MongoDB, CouchDB | Neo4j, Amazon Neptune |
| **Query language** | SQL | Query API / MongoDB query | Cypher, Gremlin |

## Key differences explained

**Impedance mismatch**: Relational databases represent one-to-many relationships across multiple tables, requiring joins to reassemble an "object". Document databases store the whole tree in one document, removing the mismatch — but at the cost of join capability.

**Graph traversals**: A relational database can traverse a graph (via recursive CTEs or multiple joins), but performance degrades with depth. A graph database is designed for multi-hop traversal — "friends of friends who bought X" is natural.

**Schema flexibility**: Schema-on-write (relational) catches errors early but requires migrations when structure changes. Schema-on-read (document) allows flexible structures but pushes interpretation responsibility to application code.

## Decision rule

> If you have normalised, multi-table data with complex queries → relational. If data is hierarchical and self-contained with rare joins → document. If entities are defined by their relationships → graph.

## See also

- [[relational-model]]
- [[document-model]]
- [[graph-model]]
- [[nosql-databases]]
- [[schema-on-read]]
