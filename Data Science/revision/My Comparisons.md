## The Three Models at a Glance

| Dimension | Relational | Document | Graph |
|---|---|---|---|
| **Data unit** | Rows in tables | Self-contained JSON doc | Vertices + edges |
| **Joins** | Native, efficient (FK) | Limited / manual | Traversals (first-class) |
| **Best for** | Normalised, many-to-many | Hierarchical, one-to-many | Highly connected networks |
| **Schema** | Schema-on-write (rigid) | Schema-on-read (flexible) | Flexible |

## Key Differences

**Relational (PostgreSQL, MySQL):**
- Spreads related data across multiple tables
- Foreign keys connect them
- You reconstruct an object via joins — e.g., to fetch a user and all their positions, join User to Position
- **Strength:** Many-to-many relationships; constraints; mature ecosystem
- **Weakness:** Object-relational impedance mismatch; schema migrations are painful

**Document (MongoDB, Firestore):**
- Stores entire objects as self-contained JSON documents
- A user document includes their positions nested inside
- No joins needed — the whole tree loads in one read
- **Strength:** Great locality; schema flexibility; maps directly to application objects
- **Weakness:** Many-to-many is awkward (you store IDs and resolve them manually); no referential integrity

**Graph (Neo4j, Neptune):**
- Entities (vertices) and their relationships (edges) are both first-class
- Made for traversal — "friends of my friends" is a graph primitive
- **Strength:** Multi-hop traversals are fast; schema evolution is easy
- **Weakness:** Aggregations across many vertices get expensive

## Decision rule

> Relational if you have normalised, multi-table data with complex queries → Document if data is hierarchical and self-contained (rare joins) → Graph if entities are defined by their relationships (social networks, fraud detection, recommendations)

## Example: LinkedIn profile

- **Relational:** User table + separate Position table (join to get user + positions)
- **Document:** One document with positions nested inside (no join)
- **Graph:** User vertex connected to Position vertices via "has_position" edges (or jobs, education, endorsements all as separate relationships)

See [[relational-vs-document-vs-graph]] for the full comparison.