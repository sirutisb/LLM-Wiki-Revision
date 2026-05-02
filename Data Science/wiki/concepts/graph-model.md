---
title: "Graph model"
type: concept
sources: [data-models-nosql]
related: [relational-model, document-model, nosql-databases]
updated: 2026-05-02
---

# Graph model

*Data as nodes (vertices) and edges. The right tool when relationships are first-class and queries traverse many hops.*

## Definition

A **graph data model** represents entities as **vertices** and relationships as **edges**. The most common variant is the **property graph**:

- **Vertex:** unique ID; collection of incoming and outgoing edges; key-value property bag.
- **Edge:** unique ID; head vertex; tail vertex; relationship label; key-value property bag.

Examples: Neo4j (Cypher query language), JanusGraph, ArangoDB, Amazon Neptune.

## Why it matters

Many real systems are *naturally* graphs:

- **Social networks** — heterogeneous nodes (users, posts, pages) and edges (follows, likes, mentions).
- **The Web** — pages and links.
- **Road networks** — junctions and roads, with weights.
- **Recommendation systems** — users, items, ratings.

Modelling these as relational tables forces dozens of joins for traversal queries; graph DBs make traversal a primitive.

## Mechanism — implementation

A property graph is essentially **two relational tables** (vertices, edges) with traversal indexes that let you, given a vertex, immediately find its incoming and outgoing edges. By labelling edges differently, you can encode many relationship types in the same store.

## Mechanism — algorithms that "fall out"

- **Dijkstra** — shortest path on a weighted graph (road navigation).
- **PageRank** — relevance ranking of web pages by link structure.
- **Community detection, centrality, BFS/DFS** — all natural primitives.

## Trade-offs

- **+** Traversal-heavy queries are O(neighbours) per hop, not O(table-scan + join).
- **+** Schema evolution is easy — add a new edge label without changing existing data.
- **−** Aggregations across many vertices can be expensive.
- **−** Less mature ecosystem than relational.
- **−** Different query languages per vendor (Cypher, Gremlin, SPARQL) — no SQL-style standard.

## Examples in the syllabus

- Social networks, road networks, the WWW (s. 19).
- Dijkstra and PageRank as canonical algorithms (s. 20).
- Property-graph schema (s. 21–22) — likely exam fodder ("describe the structure of a property graph").

## Common exam framing

- "What is a property graph? Describe the structure of vertices and edges."
- "Give two example application domains where a graph data model is more suitable than a relational one. Justify."
- "How can a property graph be implemented over relational storage?"

## See also

- [[relational-model]]
- [[document-model]]
- [[nosql-databases]]
