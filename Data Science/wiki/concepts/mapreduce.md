---
title: "MapReduce"
type: concept
sources: [batch-processing]
related: [batch-processing, distributed-filesystem, unix-philosophy, reduce-side-join, distributed-machine-learning]
updated: 2026-05-02
---

# MapReduce

*A programming model and execution framework for batch processing on a distributed cluster. Reduces every batch job to two callbacks: a mapper and a reducer.*

## Definition

**MapReduce** (Dean & Ghemawat, Google 2004) is a programming model in which:

- The **mapper** is called once per input record. It outputs zero or more `(key, value)` pairs. Stateless across records.
- The framework **sorts** all `(key, value)` pairs by key (this is the **shuffle** phase).
- The **reducer** is called once per key, with an iterator over all values for that key. It outputs zero or more output records.

Hadoop is the open-source implementation; Google's internal systems (MapReduce, FlumeJava, Dataflow) are the lineage.

## Why it matters

MapReduce was the architecture that made commodity-cluster batch processing tractable. It dominated big-data thinking for a decade. 

### The "Aha!" Analogy: Filing Cabinet vs. Factory
- **A Database** is like a **filing cabinet**: It is optimized for finding one specific record (e.g., "What is User 123's age?") very quickly.
- **MapReduce** is like a **factory**: It is for when you need to process *every single record* in the building (e.g., "What is the average age of all 60 million users?"). 

Modern systems (Spark, Flink) are descendants — they keep the data-flow shape but use DAGs and in-memory execution.

## The "National Census" Analogy
To understand why we need these two specific phases, imagine calculating the **average age per city** for the entire UK:

1.  **The Split:** You hire 1,000 workers and give each a stack of census forms for a specific street.
2.  **The MAP Phase:** Each worker reads their forms and writes down `(City, Age)` on small slips of paper. They don't need to talk to any other workers. **This is parallel execution.**
3.  **The SHUFFLE Phase:** Every worker goes to a central hall where there are desks labeled by city (Exeter, London, etc.). They drop their slips at the corresponding desk. Now, one desk has *all* the ages for one city.
4.  **The REDUCE Phase:** One person at the "Exeter" desk takes the pile of slips and calculates the final average.

## The Problem MapReduce Solved: "The Old Way"

Before MapReduce, there were two main ways to process large data, both of which failed at "Big Data" scale:

### 1. The Single-Server Bottleneck (Disk & CPU)
- **The Old Way:** You have a 10TB log file. You write a script (e.g., in Python or Java) that opens the file and reads it line-by-line.
- **The Problem:** 
    - **Disk Speed:** A single hard drive reads at ~100 MB/s. To read 10TB, it would take **28 hours** just to *read* the data, before doing any math.
    - **CPU:** One CPU can't keep up with the processing requirements of billions of records.
- **MapReduce Solution:** It breaks the 10TB file into 1,000 chunks of 10GB each. 1,000 machines read their chunk simultaneously. The time drops from **28 hours to 2 minutes**.

### 2. The Database Lookup Bottleneck (Random Access)
- **The Old Way:** You store everything in a relational database. To find the average age, you run `SELECT AVG(age) FROM users`.
- **The Problem:** Databases are designed for **Random Access** (jumping to one specific row). When you ask for *every* row, the database has to do massive amounts of "seeking" on the disk, and the overhead of the database engine (locks, transactions, indexes) slows it down.
- **MapReduce Solution:** It uses **Sequential I/O**. It treats the data as a continuous stream. Modern hard drives are much faster at reading a continuous stream of data than jumping around to different locations.

### 3. The Network Bottleneck (Data Locality)
- **The Old Way (Classic HPC):** You have a "Supercomputer" and a "Storage Server." You send the data over the network to the computer to be processed.
- **The Problem:** The network is the slowest part. Moving 10TB over a standard network takes days.
- **MapReduce Solution:** **"Bring the computation to the data."** MapReduce sends the *code* (only a few kilobytes) to the machine that already has the data on its hard drive.

## Mechanism — execution

```
INPUT FILES (on HDFS, sharded)
       |
       v
[ Mapper ]   [ Mapper ]   [ Mapper ]    <-- run on the nodes where the data lives
       |          |             |          (data locality)
       +----------+-------------+
                  |
              SHUFFLE
        (sort and partition by key, send pairs to the right reducer)
                  |
       +----------+-------------+
       |          |             |
[ Reducer ]   [ Reducer ]   [ Reducer ]
       |          |             |
       v          v             v
                OUTPUT FILES
```

- **Data locality:** mappers run on the same machine as their input partition. Avoids network for the mapper phase.
- **Shuffle:** the framework sorts and partitions intermediate `(key, value)` pairs. This is the expensive bit.
- **Parallelism:** mappers across input shards; reducers across key partitions.

## Mechanism — example: word count

```
Input:        "the cat sat on the mat"
Mapper out:   ("the", 1) ("cat", 1) ("sat", 1) ("on", 1) ("the", 1) ("mat", 1)
After shuffle: "cat" -> [1]; "mat" -> [1]; "on" -> [1]; "sat" -> [1]; "the" -> [1, 1]
Reducer out:   ("cat", 1) ("mat", 1) ("on", 1) ("sat", 1) ("the", 2)
```

## Mechanism — workflows

A single MapReduce job is limited. Real applications chain jobs: the output directory of one becomes the input of the next. Hadoop has no built-in workflow support — chaining is by directory naming. Tools like Oozie, Airflow, or Spark DAGs handle the orchestration.

## Mechanism — joins in MapReduce

[[reduce-side-join|Reduce-side joins]] use the shuffle to bring matching records together: extract the join key in the mapper, the reducer sees both sides for each key.

## Trade-offs

- **+** Massively parallel; fault tolerant (re-execute failed tasks); deterministic.
- **+** Simple programming model — just two callbacks.
- **−** Expressive limits — many algorithms need many MR stages.
- **−** Disk I/O between every pair of stages — hence Spark's in-memory advantage.
- **−** Latency is high (minutes minimum) — pure batch.

## Examples in the syllabus

- s. 6–9 describe the model and execution.
- s. 11–13 show reduce-side joins.
- [[distributed-machine-learning|Distributed ML]] uses MapReduce for parallel k-means (Distributed ML s. 32).

## Common exam framing

- "Explain how a MapReduce job is executed across a cluster."
- "What is the role of the shuffle phase, and why is it the most expensive?"
- "Write the mapper and reducer for word-count."
- "How would you implement a join between two large datasets using MapReduce?"

## See also

- [[batch-processing]]
- [[distributed-filesystem]]
- [[unix-philosophy]]
- [[reduce-side-join]]
- [[distributed-machine-learning]]
