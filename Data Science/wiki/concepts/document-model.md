---
title: "Document model"
type: concept
sources: [data-models-nosql, review]
related: [relational-model, schema-on-read, locality-storage, nosql-databases, key-value-store]
updated: 2026-05-02
---

# Document model

*Data as semi-structured documents (JSON, XML, BSON), each one self-contained. Flexible schemas, good locality, awkward many-to-many.*

## Definition

A **document database** stores data as a collection of **documents** — typically JSON, BSON or XML. Each document is a self-describing tree of fields and values, including nested objects and arrays. Documents are grouped into **collections** (MongoDB) or **buckets** (Couchbase), which are loose analogues of relational tables but **without an enforced schema**.

Examples: MongoDB, CouchDB (Apache), Firestore (Google), Couchbase, Amazon DocumentDB.

## Why it matters

The document model dominates web/mobile applications where the unit of access is "an object" (a user, a post, a product). It's the most direct mapping from application objects to storage — no ORM translation needed.

## Mechanism — what a document looks like

```json
{
  "_id": "user-42",
  "name": "Hugo",
  "positions": [
    { "title": "Senior Lecturer", "from": 2018 },
    { "title": "Lecturer", "from": 2014, "to": 2018 }
  ],
  "education": [ { "institution": "Exeter", "year": 2014 } ]
}
```

Notice: nested arrays, no separate `Position` table, no joins.

## Mechanism — strengths

- **Locality.** A whole document loads in one read. No joins to reconstruct an object.
- **[[schema-on-read|Schema flexibility]].** Each document can have different fields. Add a new field by writing it; the application interprets at read time.
- **Closer to application objects.** No impedance mismatch — JSON in, JSON out.
- **Horizontal scaling-friendly.** No cross-document joins makes sharding easier.

## Mechanism — weaknesses

- **Many-to-many is awkward.** Connections, tags, references between documents have to be stored as IDs and then resolved by the application — or by the DB's join feature, which is usually slower and more limited than SQL's.
- **No referential integrity** by default — IDs can dangle.
- **Locality is double-edged** — large documents waste IO when you only need one field.

## Trade-offs vs relational

See [[relational-vs-document]]. Headline:
- **Document wins** on schema flexibility, locality, mapping-to-objects.
- **Relational wins** on relationships, constraints, ad-hoc queries.

## Convergence

Modern relational DBs (PostgreSQL, MySQL) now support JSON columns with indexing and partial queries — narrowing the gap. Document DBs (RethinkDB, MongoDB) have added join-like capabilities. The strict either/or is fading.

## Examples in the syllabus

- MongoDB (databases → collections) is the canonical example (s. 26).
- LinkedIn profile (s. 8) modelled as a single document avoids the join needed in the relational version.

## Common exam framing

- "List two advantages and two disadvantages of the document model compared to the relational model."
- "Why is many-to-many harder to model in a document DB?"
- "Explain schema-on-read with an example."

## See also

- [[relational-model]]
- [[schema-on-read]]
- [[locality-storage]]
- [[nosql-databases]]
