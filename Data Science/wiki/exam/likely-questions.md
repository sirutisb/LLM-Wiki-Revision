---
title: "Likely exam questions"
type: exam
sources: [review, dec-2025-revision-session]
related: []
updated: 2026-05-18
---

# Likely exam questions

*Derived from Review deck coverage, slide-level exam framings, and the module structure. Review-deck topics are highest confidence. The Dec 2025 revision session section below is direct intelligence from Hugo — treat it as the highest-priority source.*

---

## Exam format & technique (Dec 2025 revision session)

*Hugo ran a live revision + past-paper walkthrough session on 12 Dec 2025. The following is drawn directly from what he said.*

### Exam facts
- **2 hours, 100 marks, 70% of final grade.**
- Word-count hints are printed next to each question as guidance — use them.
- Grammar and spelling are **not penalised**: "as long as I can see what they actually mean."
- No code writing. No algorithm memorisation. The **only calculation** expected: **sparsity of a sparse matrix** (proportion of values that are zero).
- Multiple-choice questions are possible (not always present in past papers).

### Three question types — everything falls into one of these

Hugo's exact words (end of session): *"it's going to be easier for you to demonstrate your understanding of course."*

| # | Type | Hugo's description | What to do |
|---|---|---|---|
| 1 | **Bookwork / definition** | *"What's the definition of reliability, or what was the definition for that?"* Delivered **abductively**: he gives the definition, you name the concept. | Know the precise word, not a paraphrase. One wrong word = zero. |
| 2 | **Compare / advantages & disadvantages** | *"For you to be able to compare things. Talk about the advantages and disadvantages of things."* | Cover both sides; link to trade-offs and the scenario given. |
| 3 | **Design / scenario** | *"For you to make choices — make a design about the system. I'm going to give you a problem and ask you to write a solution."* | Your answer doesn't have to match the model if your justification holds. |

### Mark scheme logic
- **1 mark**: mention the specific word/concept. *"If you mention this word, then it's one [mark]."*
- **2–3 marks**: explain something. *"If I ask you to write about that a little bit more... then it's going to be 2 or 3 marks."*
- **More marks**: assess or elaborate. *"If I need you to make some assessment of something, then that's going to be more marks."*
- Half marks are possible on longer questions.

### Topics Hugo explicitly flagged (Dec 2025 session)

These are topics he walked through or specifically told the class to study. Direct quotes or close paraphrases from the transcript.

| Topic | What Hugo said | Key watch-out |
|---|---|---|
| **Eventual consistency vs linearizability** | *"Explain the tradeoff between eventual consistency and linearizability... if you want guaranteed linearizability, you're going to have to sacrifice performance... if there is a network partition, you may need to get the system unavailable for the system to recover from the inconsistent state."* | Must link to CAP theorem; must cover impact on availability explicitly. |
| **Schema-on-read** | *"I had many students getting this one wrong because I described: structures defined when the data is loaded by the application, allows for more efficient changes in the format of the data. So that's schema-on-read. And I had people saying that's data locality — but not exactly what I was looking for."* | The definition: structure is enforced at **read time**, not write time. Do not write "data locality." |
| **Hardware vs software faults** | *"They started talking about differences between software and hardware, but without putting them in the context of the availability of the system."* | Always contextualise in terms of **availability impact**, not just what they are. |
| **Data locality (document stores)** | *"One of the advantages of document storage is data locality. But it's also one of the disadvantages — it can be wasteful."* | Same concept is **both** advantage and disadvantage. Must name both sides. |
| **Vertical vs horizontal scaling** | *"This is one of the key topics in this module."* Also: *"I had a question where the answer was vertical scaling / single machine — because in the specification I gave several indications that this data is not going to scale beyond a certain size."* | Context matters. If question signals small/non-critical system, vertical scaling may be the right answer. Always justify. |
| **Replication & partitioning** | *"What kind of problem we want to solve with replication? With what cost does it come for us? It makes it much harder to maintain the system... same thing for partitioning."* | Replication → availability/fault tolerance. Partitioning → scalability. Know the cost of each. |
| **Batch processing** | *"Doing analytics on chunks of data at regular intervals."* And full batch vs mini-batch: *"In a large scale system I can distribute these operations... my data might be so huge it wouldn't fit in memory."* | Frame batch vs mini-batch trade-offs in a distributed, large-scale context — not a single machine. |
| **Stream processing** | *"We narrow down the batch processing window so much that it becomes a single data point — we process each point as they arrive."* | Know the conceptual relationship to batch; it's a spectrum. |
| **Message broker / event streams** | *"Message broker... event streams how we manage queues... message panels hold message disruptions if the message broker goes offline."* | Durability of events when broker is offline; queue management. |
| **Event time vs processing time** | *"A discrepancy between the actual event time and when things are read by a server — hence the importance of having different timestamps on events when you're processing them."* | Why watermarks matter; out-of-order/late events corrupt windows if you use processing time. |
| **NoSQL databases** | *"Go through all of them and understand how they work and what kind of scenario they are useful."* Explicitly: document store, graph database, wide-column. | Data locality is advantage AND disadvantage. Know when each model fits. |
| **Graph database** | *"Just for graph database because that's a natural application — who follows whom... But if your justification makes sense, I will give you the full marks [for a different answer]."* | Social network / many-to-many traversal = graph. Justify your model choice. |
| **Sparse tensors — sparsity calc** | *"Sparsity — I also expect that. Most straightforward bit: what proportion of values are zeros in this matrix? And I had probably more than half of the students missing that part."* | Sparsity = (number of zeros) / (total elements). Do not skip this in any tensor question. |
| **CSR / CSC format** | *"There will be one question about either CSR or compressed column — one or the other. You should expect that."* | Know both CSR and CSC; know how to reconstruct a row/column and how dimensions + non-zero count are derived. |
| **Containerisation vs virtualisation** | *"The key again is about advantages and disadvantages of each one... containerisation: we share the operating system layer... with virtualisation we have an operating system running for each of these machines."* | Container = shared OS kernel, lightweight, fast start. VM = full OS per machine, strong isolation, heavier overhead. |
| **Kubernetes / orchestration** | *"Make sure you go through Kubernetes and understand what they are for... I'm not going to ask questions about Docker. I can ask questions about virtualisation, containerisation, orchestration."* | Concept only — not Docker CLI commands. |
| **Consistency (general)** | *"Consistency is one of the key topics in this module... make sure you understand all the implications in terms of the choices, issues that can arise with having to enforce eventual consistency."* | CAP theorem, consistency trade-offs with availability and performance. |
| **MPI** | *"Message passing interface — expect you to describe/explain what MPI stands for [1 mark]... it is a library [1 mark]... parallel copies of a distributed memory [1 mark]... exchange messages [1 mark]."* | Know: full name, it's a standard/library spec, parallel copies, distributed memory, message-passing mechanism. |

### The single most important mindset tip
Hugo: *"Always have a data center or cluster in mind when writing answers — not a single machine — **unless** the question gives you clues the system is small or non-critical. Then justify why vertical scaling / a single machine fits better."*

### Common student mistakes (named by Hugo)
- Writing about schema-on-read as "data locality" — they are **not the same**.
- Discussing hardware vs software faults **without** framing the answer around availability.
- Missing the **sparsity calculation** entirely in sparse matrix questions.
- Forgetting to address **all three NFRs** (scalability, maintainability, reliability) in design questions — *"be careful because sometimes you miss one and forget you have to talk about it."*
- Over-writing short answers (wasting time) or under-writing long ones — use word-count hints.

### What won't be on the exam
- Writing code of any kind.
- Memorising algorithm internals: *"When talking about MapReduce, K-means — don't spend time memorising that... understand the trick in making something like K-means work with MapReduce."*
- Google Cloud / vendor-specific platform details: *"The big stuff like the Google Cloud stuff — none of that's going to be on [the exam]."*
- Docker or VirtualBox specific commands/tools.

### Past paper context
- Module started 2022; Hugo wrote every exam himself — format has been consistent.
- Average mark 2024: **48.3**. Highest ever: **84**. Distinction is very achievable.
- Past three papers + solutions are on ELE. Focus on 2022–2024 papers; questions from those won't be reused.

---

## Foundations

### Q1. What are the three NFRs for data-intensive applications? Define each.
**Answer skeleton:**
- **Reliability** — system performs its expected function, tolerates faults/mistakes, prevents unauthorised access. *Fault* = one component misbehaves; *failure* = whole system stops.
- **Scalability** — ability to handle increased load. Measured by load parameters (requests/sec, read/write ratio). Average case and outlier headroom both matter.
- **Maintainability** — overall cost to keep a system running. Three sub-dimensions: *Operability* (easy for ops), *Simplicity* (easy for new engineers), *Evolvability* (easy to change).
→ [[reliability]], [[scalability]], [[maintainability]]

---

## Consistency

### Q2. State the CAP theorem. What does it imply for distributed systems?
**Answer skeleton:**
- CAP: a distributed system cannot simultaneously guarantee Consistency, Availability, and Partition Tolerance.
- Partition tolerance is mandatory (network splits happen) → real choice is **CP** (sacrifice availability) vs **AP** (sacrifice strong consistency).
- CP example: relational DB with synchronous replication. AP example: Dynamo-style key-value store.
→ [[cap-theorem]]

### Q3. Define the four ACID properties.
**Answer skeleton:** Atomicity (all-or-nothing), Consistency (transactions leave DB in valid state), Isolation (concurrent transactions don't interfere), Durability (committed data survives failure).
→ [[acid-properties]]

### Q4. What is eventual consistency? When is it acceptable?
**Answer skeleton:** At any point in time, replicas may differ. Eventually (given no more writes) all replicas converge. No *recency* guarantee. Acceptable when users can tolerate briefly stale reads (shopping cart, social feeds). Not acceptable for money transfers.
→ [[eventual-consistency]]

### Q5. Define linearizability. How does it differ from eventual consistency?
**Answer skeleton:** Linearizability = every operation appears to take effect atomically at some point between its start and end; the system behaves as if there's one copy. This provides *recency*. Eventual consistency only promises convergence — not when. Linearizability is the strongest single-object guarantee.
→ [[linearizability]]

---

## Storage & Data Models

### Q6. Compare LSM-tree and B-tree storage engines.
**Answer skeleton:**
- LSM-tree: writes to memtable, flush to SSTables, compaction merges. Write-optimised; reads may check multiple levels; better compression; no in-place updates.
- B-tree: mutable pages, update in place, WAL for durability. Read-optimised; strong consistency; standard OLTP choice.
→ [[lsm-tree]], [[b-tree]]

### Q7. Distinguish relational, document, and graph data models.
**Answer skeleton:**
- Relational: data in tables, foreign-key joins, schema-on-write, strong consistency, SQL.
- Document: JSON/BSON documents, flexible schema (schema-on-read), locality for hierarchical data, limited joins.
- Graph: vertices + edges, each with properties; property graph model; excels at many-to-many traversals (social graphs, fraud detection).
→ [[relational-model]], [[document-model]], [[graph-model]]

### Q8. What is schema-on-read vs schema-on-write?
**Answer skeleton:** Schema-on-write enforces structure at write time (relational DBs — migrations needed to change). Schema-on-read interprets structure at read time (document stores — flexible, but application bears responsibility). Trade-off: safety vs flexibility.
→ [[schema-on-read]]

---

## Replication & Partitioning

### Q9. Describe leader-follower replication. What are the trade-offs of synchronous vs asynchronous replication?
**Answer skeleton:**
- Leader-follower: leader receives writes and propagates to followers. Reads can go to any replica.
- Sync: follower acknowledged before leader confirms write → durability guarantee but higher write latency; if follower fails, writes block.
- Async: leader confirms immediately → lower latency, but follower may lag; data loss on leader failure.
→ [[leader-follower-replication]], [[synchronous-vs-asynchronous-replication]]

### Q10. What problems can replication lag cause? How can they be mitigated?
**Answer skeleton:**
- Read-your-writes violation: user writes, reads from a lagging replica, sees old data.
- Mitigation: read own writes from leader; track latest write timestamp and wait for replica to catch up.
- Monotonic reads violation: two reads return data from different replica timestamps → user sees "time go backwards".
- Mitigation: route each user's reads to the same replica consistently.
→ [[replication-lag]]

### Q11. Compare key-range and hash partitioning. When would you use each?
**Answer skeleton:**
- Key-range: partitions are contiguous key ranges. Enables efficient range scans. Risk: hotspots on monotonic keys.
- Hash: apply hash to key; assign to partition by hash range. Distributes load evenly. Destroys range ordering.
- Use key-range for time-series or range queries. Use hash for uniform write distribution.
→ [[key-range-partitioning]], [[hash-partitioning]]

---

## Batch & Stream Processing

### Q12. Distinguish online, batch, and stream systems on input, latency, and primary metric.
**Answer skeleton:**

| | Online (services) | Batch | Stream |
|---|---|---|---|
| Input | Live requests | Bounded files | Unbounded events |
| Latency | ms | minutes–days | ms–seconds |
| Metric | Response time | Throughput | Throughput + freshness |

→ [[online-vs-batch-vs-stream]]

### Q13. Describe how MapReduce works. What are mappers, reducers, and the shuffle?
**Answer skeleton:** Mappers read input records and emit (key, value) pairs. Shuffle groups all values for each key and routes them to a reducer. Reducers process each key's values and emit output records. Framework handles distribution, fault tolerance, and data movement.
→ [[mapreduce]]

### Q14. Describe how to implement a join using MapReduce (reduce-side vs map-side).
**Answer skeleton:**
- **Reduce-side join (default):** Run two mappers in parallel — one per dataset — both emit (join_key, tagged_record). Shuffle groups both datasets' records by join key. Reducer receives all records for the same key and performs the join (one-to-many). Avoids per-record database lookups.
- **Map-side join (optimization):** If one dataset is small enough to fit in memory. Load small dataset into a hash table on every mapper. Stream large dataset through mappers; join happens via memory lookup. No shuffle needed.
→ [[reduce-side-join]], [[map-side-join]]

### Q15. What strategies does a stream system use when producers outrun consumers?
**Answer skeleton:** Three options: (1) **Drop** messages — simple, but data loss. (2) **Buffer** in a queue — tolerates bursts, but bounded memory. (3) **Backpressure** — slow the producer down (flow control). Choice depends on whether data loss is acceptable.
→ [[messaging-systems]]

### Q16. Distinguish load balancing and fan-out in a message broker.
**Answer skeleton:** Load balancing: each message goes to one consumer — workers share the work. Fan-out: each message goes to all consumers — each subscriber sees every message independently. Kafka implements these via consumer groups: same group = load balance; different groups = fan-out.
→ [[multiple-consumers]]

### Q17. Why is event-time semantics important in a stream pipeline?
**Answer skeleton:** Event time = when the event happened; processing time = when the system saw it. Network delays cause events to arrive out of order or late. Using processing time puts a delayed batch of events in the wrong window, corrupting aggregations. Event time + watermarks correctly assign each event to its logical window.
→ [[event-time-vs-processing-time]]

---

## Distributed ML / Online Learning

### Q18. Describe how SGD can be parallelised with all-reduce.
**Answer skeleton:** Distribute minibatch B across M workers (each gets B' = B/M samples). Each worker computes its partial gradient. All-reduce sums the partial gradients → each worker now holds the full gradient. All workers update their model identically. Statistically equivalent to serial minibatch SGD.
→ [[sgd-all-reduce]]

### Q19. Distinguish covariate shift, prior probability shift, and concept drift.
**Answer skeleton:**
- Covariate: input distribution changes; output given input unchanged. (Face recogniser meets masked faces.)
- Prior: target distribution changes; inputs unchanged. (Flu model during pandemic.)
- Concept drift: the input→output relationship itself changes. (Fraud patterns evolve.)
→ [[data-shifts]]

### Q20. How does ADWIN detect concept drift?
**Answer skeleton:** Maintains a variable-size window. Grows during stable periods (more data → better estimates). Tests whether any sub-window has a statistically different mean. If yes → drift detected, discard older window portion. No fixed window size to tune.
→ [[adwin]]

### Q21. Describe DDM and its warning/change thresholds.
**Answer skeleton:** Tracks error rate pᵢ and std sᵢ at each step. Maintains p_min, s_min (best observed). Warning: pᵢ + sᵢ ≥ p_min + 2×s_min. Change: pᵢ + sᵢ ≥ p_min + 3×s_min. 2σ/3σ mirrors statistical process control.
→ [[ddm-eddm]]

---

## HPC / Parallelism

### Q22. State Amdahl's Law. What does it imply?
**Answer skeleton:** S = 1 / ((1−p) + p/s). The sequential fraction (1−p) bounds the maximum speedup regardless of cores added. With p=0.9, max speedup = 10× even with infinite processors.
→ [[amdahls-law]]

### Q23. What are the four SLURM entities?
**Answer skeleton:** Nodes (individual computers), Partitions (job queues with constraints), Jobs (resource allocations), Job Steps (parallel tasks within a job).
→ [[slurm]]

### Q24. Distinguish SISD, SIMD, MIMD.
**Answer skeleton:** SISD = single instruction, single data (uniprocessor). SIMD = single instruction, multiple data (same instruction on different data streams simultaneously — GPU cores, vector units). MIMD = multiple instructions, multiple data (each processor has its own instruction stream and data — multi-core CPUs, clusters).
→ [[thread-level-parallelism]]

### Q25. Compare OpenMP and MPI.
**Answer skeleton:** OpenMP: shared memory, single node, compiler-directive parallelism, fork-join model — lightweight for multi-core CPUs. MPI: distributed memory, multi-node, explicit two-sided message passing via communicators/ranks — scales to thousands of nodes.
→ [[openmp]], [[mpi]]

---

## Tensors

### Q26. What is a sparse tensor? Describe the CSR format and how to extract a row.
**Answer skeleton:** Sparse = most elements zero. CSR stores: V (non-zero values), COL_INDEX (column of each non-zero), ROW_INDEX (length m+1 marking row boundaries). Row r: slice V[ROW_INDEX[r] : ROW_INDEX[r+1]], column indices from COL_INDEX same slice.
→ [[sparse-tensors]]

---

## Virtualisation

### Q27. Distinguish virtualisation and containerisation.
**Answer skeleton:** Virtualisation: hypervisor creates full VMs each with their own OS kernel. Strong isolation, heavy overhead. Containerisation: OS-level virtualisation, shares host kernel, packages only app+dependencies. Lightweight, fast startup, portable. VMs better for strong isolation; containers better for rapid deployment and scale.
→ [[virtualisation]], [[containerisation]]

---

## Applied System Design & Past Paper Scenarios

### Q28. Describe the difference between hardware and software faults. Why are software faults often more damaging?
**Answer skeleton:** 
- **Hardware faults:** Usually independent, random (e.g., hard drive crash). Often mitigated by redundancy (RAID, multiple nodes).
- **Software faults:** Harder to anticipate, systematically correlated across nodes (e.g., a bug triggered by specific input). Can cause widespread, cascading failures, taking down the entire system despite redundancy.
→ [[fault-vs-failure]], [[reliability]]

### Q29. Explain data locality in the context of document models. What is one advantage and one disadvantage?
**Answer skeleton:** Data locality means that all data for a given object is stored together in a single continuous string (like JSON). 
- **Advantage:** Fast retrieval. Reading the entire document requires only a single database lookup/disk read.
- **Disadvantage:** If a document is large, updating a small field or reading a single field is inefficient because the whole document must be loaded/rewritten.
→ [[document-model]]

### Q30. What are the benefits and drawbacks of combining replication and partitioning?
**Answer skeleton:** 
- **Benefits:** Achieves both scalability (partitioning distributes data and load) and high availability/fault tolerance (replication ensures data survives node failures).
- **Drawbacks:** Increased system complexity. Requires coordinating distributed transactions across partitions and managing consistency across replicas.
→ [[partitioning]], [[replication]]

### Q31. What are the key considerations when deciding between vertical and horizontal scaling?
**Answer skeleton:**
- **Vertical scaling (scale up):** Simpler to maintain, strong consistency, but cost does not scale linearly (expensive at high end) and offers limited fault tolerance (single point of failure).
- **Horizontal scaling (scale out):** Cost-effective (commodity hardware), highly fault-tolerant, but increases complexity (networking, distributed consistency, data partitioning).
→ [[vertical-vs-horizontal-scaling]]

### Q32. How would you design a scalable and reliable data distribution architecture for a global social media platform (e.g., user profiles, posts, followers)?
**Answer skeleton:**
- **Data Model:** Graph database for the user "follows" network (optimised for traversals). Document or Wide-column store for user posts (schema-on-read, high write throughput).
- **Partitioning:** Hash partitioning on User ID for posts to distribute load evenly. 
- **Replication:** Leader-follower replication across multiple geographic data centres to ensure high availability and low latency globally.
- **Consistency:** Eventual consistency for posts and likes (AP system). Users tolerate slight delays in seeing new posts. Strong consistency (linearizability) is too slow for global scale here.
→ [[cap-theorem]], [[graph-model]], [[document-model]]

### Q33. Design a data pipeline for aggregating daily COVID-19 test results from hospitals to a live dashboard and social media.
**Answer skeleton:**
- **Batch vs Stream:** Use stream processing (e.g., Kafka) to ingest test results as they arrive, enabling real-time dashboard updates. A nightly batch job (MapReduce) can process the immutable daily data for official reporting.
- **Social Media Integration:** Use a message broker with a fan-out pattern to push updates to social media APIs. 
- **Why not MPI?** MPI is for tightly coupled, shared/distributed memory HPC clusters, not for loosely coupled, unreliable web API integration.
→ [[online-vs-batch-vs-stream]], [[messaging-systems]], [[mpi]]

### Q34. For a video recommendation system continuously updated by user interactions, should you use full batch, mini-batch, or online learning?
**Answer skeleton:** A combination. 
- **Online learning:** Updates the model incrementally as each interaction arrives. Essential for adapting instantly to trending videos and short-term concept drift.
- **Batch/Mini-batch:** Run periodically (e.g., nightly) over massive historical datasets to learn deep, complex patterns that online learning might miss.
→ [[online-learning]], [[concept-drift]]

### Q35. What is consensus in a leader-follower architecture, and how does it impact the system?
**Answer skeleton:** Consensus is the process of multiple nodes agreeing on a value or state (e.g., agreeing on the leader or the order of writes).
- **Impact:** Ensures strong consistency and prevents split-brain. However, it requires synchronous communication (e.g., a quorum), which reduces performance (higher latency) and can impact availability during network partitions.
→ [[consensus]], [[leader-follower-replication]]
