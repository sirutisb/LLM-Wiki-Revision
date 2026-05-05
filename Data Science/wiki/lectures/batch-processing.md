---
title: "Lecture: Batch Processing"
type: lecture
sources: [batch-processing]
related: [batch-processing, mapreduce, unix-philosophy, distributed-filesystem, reduce-side-join, online-vs-batch-vs-stream]
updated: 2026-05-02
---

# Lecture: Batch Processing

*Bounded data + scheduled job + throughput-as-success-metric. The big-data architecture pattern that put commodity-cluster computing on the map, via MapReduce.*

## Slide-by-slide notes

- **(s. 2)** Three classes of system:
  - **Online (services)** — wait for a request, respond fast. Metrics: response time, availability.
  - **Offline (batch)** — process a large input, produce output, take minutes to days. Metric: **throughput**.
  - **Near-real-time (stream)** — between online and offline; consume input events shortly after they happen.
- **(s. 3–4)** Reading a log and counting occurrences is the canonical batch task. Doable in Unix (`sort | uniq -c | sort`) or a Ruby script — the simple form lets us see what big-data systems generalise.
- **(s. 5)** [[unix-philosophy|The Unix philosophy]]:
  - Each program does one thing well.
  - Output of one program becomes input of another (stdin/stdout, plain text where possible).
  - Build software early, iterate, throw away clumsy parts.
  - Use tools to lighten programming work.
- **(s. 6)** [[mapreduce|MapReduce]]:
  - A batch-processing algorithm and low-level programming model.
  - Each MapReduce job is like one Unix process: takes input(s), produces output(s).
  - Runs on a [[distributed-filesystem]] — examples:
    - **Colossus** — Google's successor to GFS.
    - **HDFS** — Hadoop Distributed File System.
    - **GlusterFS**, **QFS** (Quantcast).
- **(s. 7)** **MapReduce job execution:**
  1. Read input files; break into records.
  2. Call **mapper** on every input record → it emits zero or more (key, value) pairs.
  3. Sort all pairs by key.
  4. Call **reducer** on each key, given an iterator over the values for that key → it emits output records.
- **(s. 8)** **Mapper** is stateless across records — each record handled independently. **Reducer** sees all values for a single key and aggregates.
- **(s. 9)** **The key advantage of MapReduce is parallelism.** Both phases parallelise across machines:
  - Mappers run on the nodes where the input is stored (data locality).
  - The framework partitions the intermediate (key, value) pairs by key (so reducers are balanced).
  - Reducers run in parallel, each on a subset of keys.
- **(s. 10)** **Workflows** — single MapReduce jobs are limited; real applications chain them. The first job's output directory becomes the next job's input. Hadoop has no built-in workflow support — chaining is implicit, by directory naming.
- **(s. 11–13)** [[reduce-side-join|Reduce-side join]] — joining two datasets in MapReduce.
  - Naive: per record, look up the joined record in a database — terrible (random per-record reads).
  - **Sort-merge approach:**
    - Two sets of mappers extract the join key from both datasets, emitting `(user_id, activity)` and `(user_id, user_record)`.
    - The framework sorts and groups by `user_id`.
    - The reducer sees, for each user, all their activity events plus their user record — joined.
  - "In order to achieve good throughput... computation must be local to one machine."
- **(s. 14–15)** [[map-side-join|Map-side join]] (**Broadcast hash join**) — an optimization when one dataset is small.
  - One side (e.g., small user DB) is loaded into an in-memory hash table on every mapper.
  - Large side (e.g., activities) is streamed through; join happens locally in the mapper.
  - **Advantage:** Avoids the expensive shuffle, sort, and merge steps of the reduce-side approach.

## Python Implementation Walkthrough

The lecture provides a Python skeleton to demonstrate the underlying mechanics of a MapReduce framework.

### The Core Engine: `run_mapreduce`
This function simulates the framework's responsibility: handling the flow of data and the expensive shuffle phase.

```python
from itertools import groupby
from operator import itemgetter

def run_mapreduce(records, mapper, reducer):
    # 1. MAP PHASE
    # Each record is passed to the mapper, which yields (key, value) pairs.
    mapped = []
    for r in records:
        for kv in mapper(r):
            mapped.append(kv)

    # 2. SHUFFLE PHASE (The expensive part!)
    # Sort all pairs by key so that identical keys are adjacent.
    mapped.sort(key=itemgetter(0))
    
    # Group by key so the reducer gets an iterator of all values for that key.
    shuffled = []
    for k, group in groupby(mapped, key=itemgetter(0)):
        shuffled.append((k, [v for _, v in group]))

    # 3. REDUCE PHASE
    # Call the reducer once for every unique key.
    out = []
    for k, vs in shuffled:
        for kv in reducer(k, iter(vs)):
            out.append(kv)
            
    return out
```

### Example: Status Code Count
Using the engine to count HTTP status codes from a log file.

**Input Data:**
```python
logs = [
    '127.0.0.1 - [10/Oct] "GET /index" 200',
    '127.0.0.1 - [10/Oct] "GET /img" 200',
    '127.0.0.1 - [10/Oct] "GET /oops" 500',
    '127.0.0.1 - [10/Oct] "GET /old" 301',
]
```

**Mapper and Reducer Functions:**
```python
def status_mapper(line):
    status = line.split()[-1] # Extract the last element (e.g., "200")
    yield (status, 1)

def sum_reducer(k, vs):
    yield (k, sum(vs))
```

**Execution Trace:**
1.  **Map:** `status_mapper` turns the logs into `[('200', 1), ('200', 1), ('500', 1), ('301', 1)]`.
2.  **Shuffle:** The framework sorts them: `[('200', 1), ('200', 1), ('301', 1), ('500', 1)]` and groups them: `[('200', [1, 1]), ('301', [1]), ('500', [1])]`.
3.  **Reduce:** `sum_reducer` aggregates the counts: `[('200', 2), ('301', 1), ('500', 1)]`.

## Background — material the slides assume but don't fully explain

- **Spark, Tez, Flink** as MapReduce successors — keep the data-flow model but use DAGs in memory rather than two-phase chained jobs. Workshops may cover Spark.
- **The MapReduce performance model** — sort by key (shuffle) is the expensive part; both mappers and reducers can stream.

## Key takeaways

1. **Batch = bounded input → throughput-optimised output.** Latency is not the metric; processing efficiency is.
2. **MapReduce reduces all batch problems to two callbacks**: mapper (extract key/value) and reducer (aggregate). The framework handles parallelism, sorting, and recovery.
3. **Data locality is everything.** Mappers run where the data lives — minimises network shuffle.
4. **Joins in batch are *sort-merge***, not loop-and-lookup. The framework sorting (key, value) pairs is what makes joins parallelisable.
5. **Workflows are job DAGs.** Chained MapReduce stages = the DAG you'd draw in Spark.
6. **MapReduce inherits the Unix philosophy:** small composable tools that read input, write output, with the framework doing the plumbing.

## Concepts introduced

- [[batch-processing]]
- [[mapreduce]]
- [[unix-philosophy]]
- [[distributed-filesystem]]
- [[reduce-side-join]]
- [[map-side-join]]
- [[online-vs-batch-vs-stream]]

## Open questions / things to clarify

- The lecture text is cut at the reduce-side-join slide; further slides on output-from-batch, derived data, and Spark-style alternatives may exist in the original PDF.
- Workshop materials likely cover Spark (Module Overview lists Spark/TensorFlow as workshop tech).

## See also

- [[mapreduce]]
- [[stream-processing]]
- [[online-vs-batch-vs-stream]]
- [[unix-philosophy]]
