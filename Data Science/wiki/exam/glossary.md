---
title: "Glossary"
type: exam
sources: []
related: []
updated: 2026-05-02
---

# Glossary

*Term → one-line definition → concept page. Alphabetical order.*

---

**ACID**: Atomicity, Consistency, Isolation, Durability — the four transaction guarantees of relational databases. → [[acid-properties]]

**ADWIN**: ADaptive WINdowing — concept drift detector that grows its observation window during stability and shrinks it when change is detected. → [[adwin]]

**All-reduce**: Communication primitive that computes a reduction across all machines and materialises the result on every machine. → [[communication-patterns]]

**Amdahl's Law**: S = 1/((1−p)+p/s) — the sequential fraction bounds parallel speedup regardless of processor count. → [[amdahls-law]]

**Atomicity**: A transaction either fully completes or fully rolls back — no partial writes. → [[acid-properties]]

**B-tree**: Balanced page-tree storage engine; updates pages in place; read-optimised; standard OLTP storage. → [[b-tree]]

**Backpressure**: Flow control mechanism that slows a producer when consumers can't keep up. → [[messaging-systems]]

**Batch processing**: Bounded input → computation → bounded output. Latency: minutes–hours. Primary metric: throughput. → [[batch-processing]]

**Broadcast**: Communication pattern where one machine sends data to all others. → [[communication-patterns]]

**CAP theorem**: A distributed system cannot simultaneously guarantee Consistency, Availability, and Partition Tolerance. Partition tolerance is mandatory → choose CP or AP. → [[cap-theorem]]

**Compaction**: Background process in LSM-tree that merges SSTables and removes obsolete/deleted data. → [[compaction]]

**Concept drift**: The relationship between inputs and outputs changes over time — the hardest form of data shift. → [[concept-drift]]

**Consistency (CAP)**: Every read receives the most-recent write or an error. → [[cap-theorem]]

**Consistency (ACID)**: Transactions only make changes that preserve database invariants. → [[acid-properties]]

**Container**: A portable, isolated, OS-level virtualisation unit that packages an application and its dependencies. → [[containerisation]]

**Container orchestration**: Automated deployment, scaling, and management of containers across many machines. → [[container-orchestration]]

**Covariate shift**: Input distribution changes; output-given-input distribution unchanged. → [[data-shifts]]

**CSR (Compressed Sparse Row)**: Sparse tensor format using three arrays: V (values), COL_INDEX, ROW_INDEX. → [[sparse-tensors]]

**DDM (Drift Detection Method)**: Concept drift detector monitoring error rate; warns at p+s ≥ p_min+2s_min; detects at 3s_min threshold. → [[ddm-eddm]]

**Distributed filesystem**: Filesystem abstracted over a cluster; splits files into replicated blocks; provides data locality. → [[distributed-filesystem]]

**Document model**: Data stored as self-contained JSON/BSON documents; flexible schema; good for hierarchical data. → [[document-model]]

**DOK (Dictionary of Keys)**: Sparse tensor format: `{(row,col): value}` hashmap. → [[sparse-tensors]]

**Durability**: Committed transaction data survives system failures. → [[acid-properties]]

**Edge computing**: Computation performed at or near the data source (device) rather than in a central cloud. → [[edge-computing]]

**EDDM**: Early Drift Detection Method — DDM variant that detects gradual drift earlier. → [[ddm-eddm]]

**Event**: A small, self-contained, immutable, timestamped record describing something that happened. → [[event-streams]]

**Event time**: When the real-world event actually occurred (carried in the event's timestamp). → [[event-time-vs-processing-time]]

**Eventual consistency**: All replicas will converge to the same value given no further writes — no recency guarantee. → [[eventual-consistency]]

**Fan-out**: Message delivery pattern where each message is sent to all consumers. → [[multiple-consumers]]

**Fault**: One component of a system behaves unexpectedly. Distinct from failure. → [[fault-vs-failure]]

**Failure**: The entire system stops providing its service. → [[fault-vs-failure]]

**FLOPS**: Floating Point Operations Per Second — standard compute throughput metric. GFLOPS=10⁹, TFLOPS=10¹², PFLOPS=10¹⁵, EFLOPS=10¹⁸. → [[flops]]

**Graph model**: Data as vertices and directed edges, each with properties; suited to multi-hop traversals. → [[graph-model]]

**Hash partitioning**: Distribute data by hashing the key; uniform distribution; destroys range ordering. → [[hash-partitioning]]

**Hypervisor**: Software layer that enables multiple VMs to share physical hardware. → [[virtualisation]]

**Isolation (ACID)**: Concurrent transactions do not interfere with each other. → [[acid-properties]]

**Key-range partitioning**: Contiguous key ranges assigned to partitions; supports range scans; risk of hotspots. → [[key-range-partitioning]]

**Leader-follower replication**: One leader accepts writes and replicates to followers; reads may go to any replica. → [[leader-follower-replication]]

**Linearizability**: Strongest consistency guarantee — every operation appears to take effect instantaneously at a single point; system behaves as one copy. → [[linearizability]]

**Load balancing (consumers)**: Each message delivered to exactly one consumer — work is shared. → [[multiple-consumers]]

**LSM-tree**: Log-Structured Merge-tree — write-optimised storage engine using memtable + immutable SSTables + compaction. → [[lsm-tree]]

**Maintainability**: Overall cost to keep a system operational: Operability + Simplicity + Evolvability. → [[maintainability]]

**MapReduce**: Distributed batch computation framework: map → shuffle → reduce. → [[mapreduce]]

**Message broker**: Server-side intermediary that durably stores and routes events between producers and consumers. → [[message-broker]]

**MIMD**: Multiple Instruction, Multiple Data — each processor has its own instructions and data (multi-core CPUs, clusters). → [[thread-level-parallelism]]

**Moore's Law**: Transistor count doubles ~every 2 years. Now slowing, driving co-design. → [[moores-law]]

**MPI**: Message Passing Interface — standard for distributed-memory parallelism using explicit two-sided messaging. → [[mpi]]

**NoSQL**: Non-relational databases prioritising scalability, flexibility, and availability. Four families: key-value, document, wide-column, graph. → [[nosql-databases]]

**Online learning**: Model parameters updated on every arriving observation; adapts instantly to changes. → [[online-learning]]

**OpenMP**: API for shared-memory parallel programming using compiler directives and fork-join model. → [[openmp]]

**Partition (data)**: A subset of a dataset assigned to one node; enables horizontal scalability. → [[partitioning]]

**Partition tolerance (CAP)**: System continues operating despite network partitions. → [[cap-theorem]]

**PaaS**: Platform as a Service — third-party platform for building/running apps without managing infrastructure. → [[container-orchestration]]

**Prior probability shift**: Target variable distribution changes; input distribution unchanged. → [[data-shifts]]

**Processing time**: When the stream processing system received and processed an event. → [[event-time-vs-processing-time]]

**Reduce-side join**: MapReduce join via shuffle — both datasets emit by join key; reducer performs the join. → [[reduce-side-join]]

**Reliability**: System performs expected function, tolerates faults, is secure. → [[reliability]]

**Replication**: Each node stores a full copy of the data; improves availability, read throughput, and latency. → [[replication]]

**Replication lag**: The delay between a leader write and a follower acknowledging it; can cause stale reads. → [[replication-lag]]

**Scalability**: Ability to handle increased load by adding resources. → [[scalability]]

**Schema-on-read**: Structure interpreted at query time (document stores). → [[schema-on-read]]

**Schema-on-write**: Structure enforced at write time (relational DBs). → [[schema-on-read]]

**SGD with all-reduce**: Distributed minibatch SGD — workers compute partial gradients, all-reduce sums them; statistically equivalent to serial minibatch SGD. → [[sgd-all-reduce]]

**SIMD**: Single Instruction, Multiple Data — same instruction applied to multiple data streams (GPU cores, vector units). → [[thread-level-parallelism]]

**SISD**: Single Instruction, Single Data — uniprocessor model. → [[thread-level-parallelism]]

**SLURM**: Slurm Workload Manager — HPC job scheduler managing nodes, partitions, jobs, job steps. → [[slurm]]

**Snapshot (replication)**: Point-in-time copy of database state used to initialise a new follower without locking. → [[leader-follower-replication]]

**Snapshot (VM)**: Captured state of a VM at a moment in time; enables rollback or migration. → [[virtualisation]]

**Software-hardware co-design**: Designing hardware and software jointly so each is optimised with respect to the other. → [[software-hardware-codesign]]

**Sparse tensor**: A tensor where most elements are zero; stored efficiently using DOK, COO, or CSR. → [[sparse-tensors]]

**SSTable**: Sorted String Table — immutable, sorted key-value file on disk; the storage layer of LSM-trees. → [[sstables]]

**Stream processing**: Continuous computation over an unbounded event sequence; low-latency; batch with vanishing window. → [[stream-processing]]

**Tensor**: Multi-dimensional numerical array; 0-order=scalar, 1-order=vector, 2-order=matrix. → [[tensors]]

**Two-phase commit (2PC)**: Distributed atomic commit protocol — prepare phase then commit phase; coordinator + participants. → [[two-phase-commit]]

**Vertical scaling**: Adding more resources to one machine (scale up); limited fault tolerance. → [[vertical-vs-horizontal-scaling]]

**Horizontal scaling**: Adding more machines (scale out); better fault tolerance and cost scaling. → [[vertical-vs-horizontal-scaling]]

**Virtualisation**: Creating software-based VMs via a hypervisor; each VM has its own OS; strong isolation; heavy overhead. → [[virtualisation]]

**Watermark**: A signal in a stream pipeline that all events with event time ≤ T have (probably) arrived; used to close time windows. → [[event-time-vs-processing-time]]
