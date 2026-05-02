---
title: "Lecture: Data Models and NoSQL Databases"
type: lecture
sources: [data-models-nosql]
related: [relational-model, document-model, graph-model, nosql-databases, schema-on-read, key-value-store, wide-column-store]
updated: 2026-05-02
---

# Lecture: Data Models and NoSQL Databases

*The choice of data model — relational, document, graph, key-value, wide-column — is the most important architectural decision after storage. Each fits different relationship patterns and evolution profiles.*

## Slide-by-slide notes

- **(s. 3)** A **data model** maps an application entity (e.g. a Python object) to a storage representation (tables, documents, key-value pairs). Every model is a lossy translation.
- **(s. 4–6)** [[relational-model|Relational model]] + ORMs (Object-Relational Mappers) translate classes ↔ tables. Translation is rarely intuitive — the *impedance mismatch* between objects and rows. LinkedIn-style profile data is the running example.
- **(s. 7)** **One-to-many relationships** in SQL: separate tables with foreign keys (normalised), or a structured field (XML/JSON) inside the parent table, or just a JSON-blob text column. Modern SQL (PostgreSQL ≥ 9.3, MySQL ≥ 5.7) supports indexing and querying inside JSON.
- **(s. 9)** [[document-model]] — encode data in semi-structured documents (JSON, XML). Stored as a single instance; **flexible** (no rigid schema). Examples: MongoDB, CouchDB, Firestore.
- **(s. 10)** **Many-to-many** breaks document models: connections, experiences, tags. Document DBs implement weak join functionality, but joins are usually slower and clumsier than in SQL.
- **(s. 11)** [[relational-vs-document|Relational vs document]]:
  - Document advantages: schema flexibility, **locality** (related data stored together), closer to application data structures.
  - Relational advantages: better support for **joins** and many-to relationships.
- **(s. 12–15)** [[schema-on-read]]:
  - Most document DBs don't enforce a schema. Structure is implicit, validated when data is read by the application — like dynamic typing in programming.
  - **Schema-on-read** vs **schema-on-write**: the relational ALTER-TABLE pain (slow, downtime, full rewrites) disappears, but you have no guarantees about the contents of any document.
  - Useful when: data is heterogeneous; you don't control the structure (e.g. tweets); you need to evolve the format quickly.
- **(s. 16–17)** **Locality**:
  - *Pro:* "all the data for a given object is stored together" — fewer reads, no joins for whole-object access.
  - *Con:* same — "the DB will load the entire document"; if your documents are large, you waste IO.
  - Not exclusive to document DBs: Google Spanner has locality in a relational model; column-family in [[wide-column-store|wide-column DBs]] like Cassandra is the same idea.
- **(s. 18)** **Document and relational convergence**: modern relational DBs support JSON/XML; document DBs are adding join-like capabilities (RethinkDB). The line between them blurs.
- **(s. 19)** [[graph-model|Graph-like models]] for complex many-to-many: social networks, the WWW, road networks. Entities are **nodes**, relationships are **edges**.
- **(s. 20)** Classic graph algorithms become natural: Dijkstra (shortest routes), PageRank (web search relevance).
- **(s. 21–22)** **Property graphs** — every vertex has a unique ID, incoming/outgoing edges, and a key-value property bag. Every edge has an ID, head/tail vertices, label, and properties. Implementable as two relational tables (vertices, edges) with adjacency indexed for fast traversal.
- **(s. 23–25)** [[nosql-databases]] umbrella: non-relational storage that focuses on simplicity, scalability, horizontal scaling, availability. Four families:
  - **Document** (MongoDB, CouchDB, Firestore)
  - **Key-value** (DynamoDB, Redis, Riak)
  - **Wide-column** (Cassandra, HBase, Bigtable)
  - **Graph** (Neo4j, JanusGraph, ArangoDB)
- **(s. 26)** **Document store** organisation in MongoDB: databases → collections (analogous to tables, but schema-less) → documents. SQL-like query language.
- **(s. 27)** [[key-value-store]] — data as associative arrays; every object is a set of key-value pairs. Composite primary keys are common (e.g. DynamoDB partition + sort key).
- **(s. 28)** [[wide-column-store]] — data in tables/rows/columns, but column names and formats can vary row to row. Cassandra is the canonical example.

## Key takeaways

1. **Data model = the lens.** It determines what's easy and what's painful: relational makes joins easy and schema migrations hard; document makes whole-object access easy and many-to-many joins hard.
2. **One-to-many is solved everywhere.** Many-to-many is where the choice bites.
3. **Schema-on-read** trades guarantees for flexibility. It's brilliant for heterogeneous, evolving data and dangerous for invariants.
4. **Locality is a double-edged sword.** Great for whole-object reads, wasteful for partial reads.
5. **Graph models earn their keep when relationships are first-class.** If you're doing 5+ joins to answer a query, a graph DB is probably the right tool.
6. **NoSQL ≠ "no SQL."** It's "non-relational" — and modern systems converge: SQL gets JSON, document DBs get joins, graph DBs get SQL-like languages.

## Concepts introduced

- [[relational-model]]
- [[document-model]]
- [[graph-model]]
- [[key-value-store]]
- [[wide-column-store]]
- [[nosql-databases]]
- [[schema-on-read]]
- [[locality-storage]]

## Open questions / things to clarify

- Property-graph slide (s. 21) lists the structure precisely — likely exam fodder.
- "Document and relational convergence" is a frequent essay-style question.

## See also

- [[relational-model]]
- [[document-model]]
- [[graph-model]]
- [[nosql-databases]]
- [[storage-and-retrieval]]
