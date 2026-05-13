---
title: "OpenMP — Complete Exam Reference"
tags: [hpc, openmp, week-2, week-7, week-8, week-10, week-11, final-prep]
date: 2026-05-13
---

# OpenMP — Complete Exam Reference

---

### Execution Model

- **Fork-Join**: master thread forks a team of threads at a parallel region, they join (synchronize + terminate) at the end.
- **Shared memory only** — works within one node. Cannot span distributed-memory nodes (that is MPI's job).

---

### Compiler Directives (Pragmas)

| Directive | What it does |
|---|---|
| `#pragma omp parallel` | Opens a parallel region; spawns thread team |
| `#pragma omp for` | Distributes loop iterations across threads (inside a parallel region) |
| `#pragma omp parallel for` | Shorthand combining the two above |
| `#pragma omp barrier` | Explicit synchronization barrier — all threads wait |
| `#pragma omp single` | Only one thread executes the block; implicit barrier at end |
| `#pragma omp sections` | Container for independent code blocks |
| `#pragma omp section` | One block inside a `sections` construct |
| `#pragma omp task` | Creates a deferred task unit placed in a task queue |
| `#pragma omp target` | Offloads code to GPU device (OpenMP 4.0+) |
| `#pragma omp target teams distribute` | Offload + distribute across GPU thread groups |

---

### Clauses (attach to directives)

#### Scoping Clauses

| Clause | Behaviour |
|---|---|
| `shared(x)` | All threads read/write the same memory location — risk of data race |
| `private(x)` | Each thread gets its own **uninitialized** copy |
| `firstprivate(x)` | Each thread gets its own copy **initialized with the value at time of task creation** — critical for `#pragma omp task` where the loop variable may change before the task runs |
| `lastprivate(x)` | Private during execution, but after the region ends the variable holds the value from the **sequentially last iteration** — fixes output dependency |
| `reduction(op : x)` | Each thread accumulates locally, then all local values are combined using `op` (`+`, `*`, `max`, `min`, etc.) |
| `default(none)` | Forces you to explicitly declare every variable's scope — best practice to catch accidental data races |

#### Synchronization Clauses

| Clause | Behaviour |
|---|---|
| `nowait` | Removes the implicit barrier at the end of `for`, `single`, or `sections` — threads proceed immediately |

#### Scheduling Clause

`schedule(type, chunk_size)` — controls how loop iterations are assigned to threads:

| Type | How it works | When to use |
|---|---|---|
| `static` | Iterations divided into `chunk`-sized blocks, assigned round-robin at **compile time** | Uniform workloads; lowest overhead |
| `dynamic` | Threads grab a new `chunk` at **runtime** whenever they finish their current chunk | Variable/unpredictable workloads; higher overhead |
| `guided` | Like dynamic but chunk size **starts large and shrinks** (down to minimum `chunk`) | Good middle ground; reduces overhead at end |

#### GPU Map Clause

| Clause | Behaviour |
|---|---|
| `map(to: a[0:N])` | Copy array from host (CPU) → device (GPU) before execution |
| `map(from: c[0:N])` | Copy array from device → host after execution |
| `map(tofrom: x)` | Copy both directions (default if not specified) |

---

### Implicit Barriers (automatic, at end of)

- `#pragma omp parallel`
- `#pragma omp for`
- `#pragma omp single`
- `#pragma omp sections`

Use `nowait` to suppress them (except at end of `parallel`).

---

### Runtime Library Functions (include `<omp.h>`)

| Function | Returns |
|---|---|
| `omp_get_thread_num()` | This thread's ID (0 = master) |
| `omp_get_num_threads()` | Total threads in the current team |

---

### Environment Variables

| Variable | Effect |
|---|---|
| `OMP_NUM_THREADS` | Sets the number of threads forked in a parallel region |

---

### Data Dependencies — What to Know

| Type | Pattern | Parallelisable? | Fix |
|---|---|---|---|
| **Flow** (Read-after-Write) | `a[i] = a[i-1] + 1` — iteration `i` needs output of `i-1` | No — true dependency; algorithm must change | Cannot be solved by a new array |
| **Anti** (Write-after-Read) | `a[i] = a[i+1] * 2` — storage conflict, not true dependency | Yes | Write results to a separate array `b[]` |
| **Output** (Write-after-Write) | Multiple iterations write the same variable | Yes | Use `lastprivate` to keep the last value |

---

### OpenMP Tasks Pattern (Week 8)

```c
#pragma omp parallel
{
    #pragma omp single
    {
        for (int i = 0; i < N; i++) {
            #pragma omp task firstprivate(i)
            { do_work(i); }
        }
    }
}
```

- `single` ensures only one thread generates tasks.
- `firstprivate(i)` captures `i` at task-creation time (not execution time).
- Used for irregular parallelism: while loops, linked lists, recursion.

---

### Sections Pattern (Week 8)

```c
#pragma omp parallel
{
    #pragma omp sections
    {
        #pragma omp section
        { task_A(); }
        #pragma omp section
        { task_B(); }
    }
}
```

Use when you have a fixed number of independent code blocks (not loop iterations).

---

### GPU Offloading Pattern (Week 10)

```c
#pragma omp target teams distribute map(to: a[0:N], b[0:N]) map(from: c[0:N])
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

Key principle: **minimize PCIe data transfers** — offloading a small task is often slower than running it on CPU due to transfer overhead.

---

### NUMA + OpenMP (Week 6)

- **First-touch policy**: OS places a memory page on the socket of the first thread to write to it.
- If master thread initializes a shared array sequentially, all pages land on its socket → remote access penalty for other threads.
- **Fix**: parallelize the initialization loop so each thread touches its own portion first.

---

### Hybrid MPI + OpenMP (Week 11)

- MPI: one process per socket, handles inter-node communication.
- OpenMP: threads within that process, handles intra-node parallelism.
- Benefits: fewer halos, fewer MPI messages, extended scaling, better NUMA locality.

---

### Conditional Compilation

```c
#ifdef _OPENMP
    // OpenMP-specific code
#else
    // Sequential fallback
#endif
```

---

That covers every OpenMP concept, clause, directive, and pattern taught across Weeks 2, 7, 8, 10, and 11. The highest-exam-frequency items are: `reduction`, `private`/`shared`/`default(none)`, `schedule` types, `nowait`, `firstprivate` in tasks, `lastprivate` for output dependencies, and the fork-join model.
