---
title: "Topic: Distributed systems"
type: topic
sources: []
related: [replication, partitioning, cap-theorem, consensus, linearizability, two-phase-commit, replication-lag]
updated: 2026-05-02
---

# Topic: Distributed systems

*The cluster of concepts covering how data is distributed, kept consistent, and how failures are managed across multiple machines.*

## Core tension

More machines → more capacity and fault tolerance, but coordination becomes hard. Every distributed system must navigate:

- **Consistency** — do all nodes agree on the current state?
- **Availability** — does every request get a response?
- **Partition tolerance** — can the system survive network splits?

The [[cap-theorem]] formalises this three-way tension.

## Key concepts

### Data distribution
- [[replication]] — copies of data on multiple nodes; reduces latency, improves availability.
- [[partitioning]] — subsets of data on different nodes; enables horizontal scale.
- [[replication-vs-partitioning]] — comparison page.

### Consistency models
- [[linearizability]] — strongest single-object consistency; one-copy illusion.
- [[eventual-consistency]] — all replicas converge eventually; no recency guarantee.
- [[acid-properties]] — transaction-level consistency in databases.

### Coordination
- [[consensus]] — getting distributed nodes to agree on a single value.
- [[two-phase-commit]] — distributed atomic commit via prepare + commit phases.

### Replication specifics
- [[leader-follower-replication]] — one writer, many readers.
- [[synchronous-vs-asynchronous-replication]] — durability vs latency trade-off.
- [[replication-lag]] — staleness and read anomalies.

## See also

- [[cap-theorem]]
- [[replication]]
- [[partitioning]]
- [[scalability]]
