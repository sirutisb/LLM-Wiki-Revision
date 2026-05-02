---
title: "Cheatsheet"
type: exam
sources: [review]
related: []
updated: 2026-05-02
---

# Cheatsheet

*One-page condensed reference. Formulas, definitions, key trade-offs.*

---

## Foundations

**Reliability** = performs expected function + tolerates faults + secure  
**Fault** = one component misbehaves | **Failure** = whole system stops  
**Scalability** = copes with increased load (load parameters: req/sec, r/w ratio)  
**Maintainability** = Operability + Simplicity + Evolvability  

---

## Consistency

**CAP theorem**  
Consistency (every read gets latest write or error) + Availability (every request gets a response) + Partition Tolerance (survives network splits)  
**P is mandatory** → choose CP or AP  

**ACID**: Atomicity · Consistency · Isolation · Durability  
**Eventual consistency**: replicas converge eventually; no recency guarantee  
**Linearizability**: strongest single-object guarantee; one-copy illusion; atomic per operation  

---

## Storage

| Engine | Writes | Reads | Mechanism |
|---|---|---|---|
| **LSM-tree** | Fast (append) | Slower (multi-level) | memtable → SSTable → compaction |
| **B-tree** | Slower (in-place) | Fast | balanced page tree, WAL |

**OLTP**: many small reads/writes, random access, row-oriented  
**OLAP**: large scans, analytics, column-oriented (data warehouses)  

---

## Data Models

**Relational**: tables + foreign keys + SQL + schema-on-write  
**Document**: JSON/BSON + flexible schema (schema-on-read) + locality + limited joins  
**Graph**: vertices (id, properties) + directed edges (id, tail, head, label, properties)  
**Key-value**: simplest; lookup by key only  
**Wide-column**: sparse table; rows have flexible column sets (Cassandra, HBase)  

---

## Replication & Partitioning

**Leader-follower replication**: leader takes writes; followers replicate; reads from any  
**Sync**: durable but blocks if follower fails | **Async**: low latency but data loss risk  
**Replication lag problems**: read-your-writes, monotonic reads  

**Partitioning**: each piece of data on exactly one node  
**Key-range**: good for range queries; hotspot risk  
**Hash**: uniform distribution; no range queries  
**Rebalancing**: fixed partition count (move whole partitions) or dynamic (split/merge)  

---

## Batch vs Stream

| | Batch | Stream | Online (service) |
|---|---|---|---|
| Input | Bounded | Unbounded | Per-request |
| Latency | min–days | ms–sec | ms |
| Metric | Throughput | Throughput+freshness | Response time |

**MapReduce**: mapper emits (k,v) → shuffle groups by k → reducer produces output  
**Reduce-side join**: both datasets map with join_key; shuffle brings together; reducer joins  
**Backpressure options**: drop · buffer · slow producer  
**Load balancing**: one consumer per message | **Fan-out**: all consumers per message  
**Event time** (in event) vs **Processing time** (when system saw it) — use event time  
**Watermark**: signal that all events ≤ T have arrived → close the window  

---

## Distributed ML

**Communication patterns**: Push · Pull · Broadcast · Reduce · **All-reduce** · Wait · Barrier  
**All-reduce SGD**: B = M × B'; each worker computes gradient for B'; all-reduce sums → all workers update identically  
**Drawback**: workers idle during all-reduce (no overlap)  
**Parallel k-means**: Map=assign to cluster, Combine=local sums, Reduce=update centroids  

---

## Online Learning & Drift

**Full batch** → all data, true gradient | **Mini-batch** → subset | **Online** → one observation  
**Data shifts**: Covariate (inputs change) | Prior probability (outputs change) | **Concept drift** (relationship changes)  
**Drift types**: gradual · abrupt · recurring  
**ADWIN**: variable window; grows when stable; shrinks on drift  
**DDM**: Warning: pᵢ+sᵢ ≥ p_min+**2**s_min | Change: pᵢ+sᵢ ≥ p_min+**3**s_min  

---

## HPC

**FLOPS**: GFLOPS=10⁹ | TFLOPS=10¹² | PFLOPS=10¹⁵ | EFLOPS=10¹⁸  
Smartphone 1-2G | Laptop 10G | Server 25-100G | GPU 20G–2T  
**Moore's Law**: transistor count doubles ~every 2 years; now slowing  
**Amdahl's Law**: `S = 1 / ((1−p) + p/s)` — sequential fraction (1−p) caps max speedup  
**SLURM entities**: Nodes → Partitions → Jobs → Job Steps  

---

## Thread-Level Parallelism

**SISD** uniprocessor | **SIMD** one instruction, many data streams | **MIMD** multiple instructions + data  
**OpenMP**: shared memory, single node, fork-join compiler directives  
**MPI**: distributed memory, multi-node; communicator = context+group+size+ranks; MPI_COMM_WORLD = all processes; two-sided messages  

---

## Tensors

**Orders**: 0=scalar, 1=vector, 2=matrix, 3+=tensor  
**Shapes**: features | features×timestamps | W×H×C | frames×W×H×C  
**Sparse**: sparsity = proportion zeros; store only non-zeros  
**DOK**: `{(r,c): val}` | **COO**: `(r,c,val)` list | **CSR**: V + COL_INDEX + ROW_INDEX  
**CSR row r**: `V[ROW_INDEX[r]:ROW_INDEX[r+1]]`  

---

## Virtualisation vs Containerisation

| | VM | Container |
|---|---|---|
| Isolation | Hardware (hypervisor) | OS (kernel namespaces) |
| Kernel | Own per VM | Shared |
| Overhead | High (full OS) | Low (app+deps only) |
| Startup | Seconds–mins | Milliseconds |
| Portability | VM image (large) | Container image (small) |

**PaaS**: developers push code; platform manages containers, scaling, infrastructure  

---

## Software-Hardware Co-design

**Bottom-up**: hardware first → software for it  
**Top-down**: software requirements → design new hardware (e.g. Nvidia tensor cores)  
**Co-design**: hardware + software designed together iteratively  
**Partitioning**: allocate functions → hardware (speed/parallel) or software (flexible)  
**Edge computing**: compute on device, not cloud; low power, personalised  
