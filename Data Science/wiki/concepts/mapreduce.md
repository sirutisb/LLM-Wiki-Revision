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

MapReduce was the architecture that made commodity-cluster batch processing tractable. It dominated big-data thinking for a decade. Modern systems (Spark, Flink) are descendants — they keep the data-flow shape but use DAGs and in-memory execution.

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
