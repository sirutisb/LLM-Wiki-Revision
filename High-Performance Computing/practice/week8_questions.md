---
title: "Week 8 Practice Questions: Manager-Worker and Task-Based Parallelism"
tags: [hpc, week-8, mpi, openmp, tasks, practice]
date: 2026-05-14
---

# Week 8 Practice Questions: Manager-Worker and Task-Based Parallelism

These questions cover all examinable material from Week 8: the manager-worker MPI pattern, MPI wildcards (`MPI_ANY_SOURCE`, `MPI_ANY_TAG`), MPI groups and communicators, OpenMP `sections`, `single`, `task`, and `taskwait`, the `firstprivate` clause, and the comparison between static and dynamic work distribution.

---

## Section A: Short Answer / Definition

---

### Q1. Define `MPI_ANY_SOURCE` and `MPI_ANY_TAG`. When is each used?

**Model Answer (key marking points):**

- `MPI_ANY_SOURCE` is a wildcard value that can be passed as the `source` argument to `MPI_Recv`. It tells MPI to accept an incoming message from **any** sender rank, rather than a specific one. *(1 mark)*
- `MPI_ANY_TAG` is a wildcard for the `tag` argument of `MPI_Recv`. It tells MPI to accept a message carrying **any** tag value. *(1 mark)*
- Both are used in the manager-worker pattern, where the manager cannot predict which worker will finish and send a request next. Without wildcards, the manager would need to poll each worker in a fixed order, destroying dynamic balancing. *(1 mark)*
- After a wildcard receive, the actual sender rank and tag are recovered from the `MPI_Status` struct via `status.MPI_SOURCE` and `status.MPI_TAG`. *(1 mark)*

---

### Q2. Write the full function signature of `MPI_Recv` and briefly describe every parameter.

**Model Answer:**

```c
int MPI_Recv(void *buf, int count, MPI_Datatype datatype,
             int source, int tag, MPI_Comm comm, MPI_Status *status);
```

| Parameter  | Description |
|:-----------|:------------|
| `buf`      | Pointer to the receive buffer (data is written here). |
| `count`    | Maximum number of elements to receive. |
| `datatype` | MPI data type of each element (e.g. `MPI_INT`, `MPI_DOUBLE`). |
| `source`   | Rank of the sender, or `MPI_ANY_SOURCE` to receive from any rank. |
| `tag`      | Message tag expected, or `MPI_ANY_TAG` to accept any tag. |
| `comm`     | Communicator (e.g. `MPI_COMM_WORLD`). |
| `status`   | Output struct. After the call, `status.MPI_SOURCE` holds the actual sender rank and `status.MPI_TAG` holds the actual tag received. |

*(1 mark per correct parameter description, up to 6 marks.)*

---

### Q3. List the six steps in the standard recipe for creating a new MPI communicator from a subset of `MPI_COMM_WORLD`.

**Model Answer:**

1. **`MPI_Comm_group`** — obtain the group object associated with `MPI_COMM_WORLD`.
2. **`MPI_Group_incl` or `MPI_Group_excl`** — build a new group by specifying which ranks to include or exclude.
3. **`MPI_Comm_create`** — create a new communicator from the new group (called collectively by all processes in the parent communicator).
4. **`MPI_Comm_rank`** — determine the calling process's rank within the new communicator.
5. **Do work** — use the new communicator for collective or point-to-point operations restricted to the group.
6. **`MPI_Comm_free` and `MPI_Group_free`** — release the communicator and group objects to avoid resource leaks.

*(1 mark per step; must be in correct order for full credit.)*

---

### Q4. What is the difference between `MPI_Group_incl` and `MPI_Group_excl`?

**Model Answer:**

- `MPI_Group_incl(group, n, ranks, newgroup)` — creates a new group containing **exactly** the `n` ranks listed in the `ranks` array (taken from `group`). Useful when you know precisely which processes should be in the new group.
- `MPI_Group_excl(group, n, ranks, newgroup)` — creates a new group containing **all ranks in `group` except** the `n` listed in `ranks`. More convenient when you want to exclude a small number of processes (e.g. the manager).

*(2 marks: 1 for each.)*

---

### Q5. What value does a process that is **not** a member of the new group receive from `MPI_Comm_create`?

**Model Answer:**

Non-member processes receive `MPI_COMM_NULL`. They must still call `MPI_Comm_create` (because it is **collective over the parent communicator**), but the result is a null communicator which cannot be used in further communication calls.

Key point: failing to call `MPI_Comm_create` on every process in `MPI_COMM_WORLD` would cause a **deadlock**, because collective operations require all participants to call them.

*(2 marks: 1 for `MPI_COMM_NULL`, 1 for the collective requirement.)*

---

### Q6. What are the three work-sharing constructs available in OpenMP **before** OpenMP 3.0 (in C)?

**Model Answer:**

1. `#pragma omp for` — distributes loop iterations across threads.
2. `#pragma omp sections` — assigns distinct, independent blocks of code to different threads.
3. `#pragma omp single` — designates a block that is executed by exactly one thread (any thread).

OpenMP 3.0 added `#pragma omp task` as a fourth mechanism for irregular parallelism.

*(1 mark per construct; 1 mark for noting when tasks were added.)*

---

### Q7. Explain what `#pragma omp single` does and how it differs from `#pragma omp master`.

**Model Answer:**

- `#pragma omp single` ensures that the enclosed block is executed by **exactly one thread**, but it does not specify which thread — it is whichever reaches the construct first. All other threads skip the block and wait at an implicit barrier at the end (unless `nowait` is specified).
- `#pragma omp master` also executes the block on only one thread, but it is **always the master thread** (thread 0). Crucially, there is **no implicit barrier** at the end of `master` — other threads continue without waiting.

For task generation, `single` is preferred over `master` because the implicit barrier at the end of `single` ensures all generated tasks complete before the program proceeds past that point.

*(2 marks: 1 for each construct's behaviour; 1 bonus mark for noting which is preferred for task generation.)*

---

### Q8. Define the `firstprivate` clause in the context of `#pragma omp task`. Why is it essential when creating tasks inside a loop?

**Model Answer:**

`firstprivate(x)` declares a variable private to a task and **initialises the task's private copy with the value that `x` has at the moment the `#pragma omp task` construct is encountered** — i.e. at task creation time, not at task execution time.

This is essential in a loop because tasks are executed **asynchronously**. By the time a task actually runs, the loop variable may have advanced to a different value (or the loop may have already terminated). Without `firstprivate`, each task would use the same shared loop variable and likely see the wrong value. With `firstprivate`, each task receives its own snapshot of the variable taken at the instant the task was queued.

Example: if tasks are generated for `i = 0, 1, ..., N` and `firstprivate(i)` is not used, every task might execute with `i == N` (the final value), computing the same column N times.

*(3 marks: 1 for the definition, 1 for async execution hazard, 1 for the concrete consequence.)*

---

### Q9. What does "granularity" mean in the context of task-based parallelism, and what trade-off does it impose?

**Model Answer:**

Granularity refers to the size of each unit of work (task or work unit) relative to the overhead of managing it.

- **Too coarse** (few large tasks): the runtime has limited flexibility to rebalance — one thread may still finish early and sit idle.
- **Too fine** (many tiny tasks): the scheduling overhead (pushing/popping from the task queue, context-switching) dominates the actual compute time; performance degrades.

The guideline from the lecture: **"make sure there are more tasks than threads"** — enough tasks for the runtime to keep all threads busy, but each task large enough that compute time significantly exceeds scheduling overhead.

*(2 marks: 1 for the trade-off direction each way.)*

---

### Q10. In one sentence each, state when you would choose (a) `sections`, (b) `task`, and (c) `parallel for` in OpenMP.

**Model Answer:**

**(a) `sections`:** Use when you have a **small, fixed number of independent, heterogeneous code blocks** that can run concurrently (e.g. initialising two different arrays simultaneously).

**(b) `task`:** Use when the work is **irregular, recursive, or has an unknown trip count** at compile time (e.g. linked list traversal, tree recursion, while loops, Mandelbrot where each column's cost varies wildly).

**(c) `parallel for`:** Use when you have a **loop with a known trip count and roughly uniform work per iteration** — it maps directly to the parallel loop model with optional `schedule` clause for minor load imbalance.

*(1 mark each.)*

---

## Section B: Code Analysis

---

### Q11. Examine the following MPI manager code fragment. Identify **two bugs** and explain what will go wrong at runtime.

```c
// Manager (rank 0 only)
int next_i = 0;
int active = size - 1;
MPI_Status status;
int dummy;

while (active > 0) {
    MPI_Recv(&dummy, 1, MPI_INT,
             0, MPI_ANY_TAG,          // <-- Bug A
             MPI_COMM_WORLD, &status);

    int worker = status.MPI_SOURCE;

    if (next_i < N) {
        MPI_Send(&next_i, 1, MPI_INT,
                 worker, WORK_TAG, MPI_COMM_WORLD);
        next_i++;
    } else {
        MPI_Send(&next_i, 1, MPI_INT,
                 worker, DIE_TAG, MPI_COMM_WORLD);
        // Bug B: active is never decremented here
    }
}
```

**Model Answer:**

**Bug A — Wrong `source` argument in `MPI_Recv`:**
The `source` argument is `0` (the manager's own rank), but the manager should be receiving from **any** worker, not from itself. This should be `MPI_ANY_SOURCE`. As written, the manager will block forever waiting for a message from itself, causing a deadlock. *(2 marks)*

**Bug B — `active` is never decremented:**
When `next_i >= N`, the manager sends a `DIE_TAG` to tell a worker to stop, but the `active` counter is never decremented. The `while (active > 0)` loop will therefore never terminate: the manager will keep receiving termination requests and sending DIE_TAG replies in an infinite loop (or more likely deadlock once all workers have already exited). The fix is to add `active--;` inside the `else` branch. *(2 marks)*

---

### Q12. Read the following OpenMP code. State exactly what it prints and explain why.

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int x = 10;

    #pragma omp parallel num_threads(4)
    {
        #pragma omp single
        {
            printf("Thread %d is in single, x = %d\n",
                   omp_get_thread_num(), x);
        }

        printf("Thread %d past single\n", omp_get_thread_num());
    }
    return 0;
}
```

**Model Answer:**

**What it prints (order of lines 2–4 may vary):**

```
Thread ? is in single, x = 10      (printed by exactly one thread, ? = any of 0–3)
Thread 0 past single
Thread 1 past single
Thread 2 past single
Thread 3 past single
```

**Explanation:**

- Four threads are created by `omp parallel`.
- Only one thread (whichever reaches the `single` construct first) executes the `printf` inside the `single` block. The other three skip it and wait at the implicit barrier at the end of `single`.
- After the barrier, **all four threads** execute the second `printf`. The order of those four lines is non-deterministic.
- `x = 10` is printed because `x` is shared (declared outside the parallel region) and is not modified.

Key exam point: unlike `master`, the `single` construct does not guarantee it is thread 0 that executes it.

*(3 marks: 1 for correct number of lines, 1 for correct explanation of single, 1 for barrier explanation.)*

---

### Q13. The following OpenMP task code is **missing a critical clause**. What is the bug, and what is the fix?

```c
#pragma omp parallel
{
    #pragma omp single
    {
        for (int i = 0; i <= N; i++) {
            #pragma omp task shared(nIter, z_Re, z_Im, N, maxIter)
            {
                for (int j = 0; j <= N; j++) {
                    // ... Mandelbrot inner loop writing nIter[i][j] ...
                }
            }
        }
    }
}
```

**Model Answer:**

**Bug:** The loop variable `i` is **not declared `firstprivate`**. Tasks are executed asynchronously — by the time a task runs, the generator thread may have advanced `i` to a later value (or past `N`). Every task will capture the same, stale value of `i` rather than the value it had when the task was created. In the worst case all tasks execute with `i == N+1` (post-loop value), computing the same (or an out-of-bounds) column repeatedly and producing incorrect results.

**Fix:** Add `firstprivate(i)` to the task pragma:

```c
#pragma omp task firstprivate(i) shared(nIter, z_Re, z_Im, N, maxIter)
```

This gives each task its own private copy of `i` initialised to the value `i` had when the task was created — the correct column index.

*(3 marks: 1 for identifying missing `firstprivate`, 1 for explaining the async hazard, 1 for the fix.)*

---

### Q14. What does the following communicator code do? Trace through it step by step.

```c
MPI_Group worldGroup, workerGroup;
MPI_Comm  workerComm;

int excluded[1] = {0};

MPI_Comm_group(MPI_COMM_WORLD, &worldGroup);
MPI_Group_excl(worldGroup, 1, excluded, &workerGroup);
MPI_Comm_create(MPI_COMM_WORLD, workerGroup, &workerComm);

if (workerComm != MPI_COMM_NULL) {
    long local_result = compute();
    long global_result;
    MPI_Reduce(&local_result, &global_result, 1, MPI_LONG,
               MPI_SUM, 0, workerComm);
    int wrank;
    MPI_Comm_rank(workerComm, &wrank);
    if (wrank == 0) printf("Sum = %ld\n", global_result);
    MPI_Comm_free(&workerComm);
}
MPI_Group_free(&workerGroup);
MPI_Group_free(&worldGroup);
```

**Model Answer (step-by-step):**

1. `MPI_Comm_group` extracts the group corresponding to `MPI_COMM_WORLD` (contains all ranks 0 to size-1). *(1 mark)*
2. `MPI_Group_excl` creates `workerGroup`: all ranks **except** rank 0 (the manager). *(1 mark)*
3. `MPI_Comm_create` creates `workerComm` — a new communicator covering only the worker ranks. All processes must call this (collective on `MPI_COMM_WORLD`). Rank 0 (the manager) gets `MPI_COMM_NULL`. *(1 mark)*
4. Workers (who have a valid `workerComm`) call `compute()` and then `MPI_Reduce` with `MPI_SUM` to sum all `local_result` values onto rank 0 of `workerComm` (which is the lowest-numbered worker, not the manager). *(1 mark)*
5. Worker-rank-0 prints the total sum. *(1 mark)*
6. `MPI_Comm_free` and `MPI_Group_free` release resources. *(1 mark)*

**Overall purpose:** Aggregate a result across all worker processes, explicitly excluding the manager, which has no computed data to contribute.

---

## Section C: Code Writing

---

### Q15. Write a complete MPI manager-worker program skeleton (in C) with the following specification:

- `N` total work units (integer indices 0 to N-1).
- Rank 0 is the manager; all other ranks are workers.
- Workers request work, compute `result = index * index`, and request more until terminated.
- The manager sends work units one at a time using `WORK_TAG` and sends a termination signal using `DIE_TAG`.
- Use `MPI_ANY_SOURCE` and `MPI_ANY_TAG` appropriately.
- Include `MPI_Init`, `MPI_Finalize`, and required status inspection.

**Model Answer:**

```c
#include <mpi.h>
#include <stdio.h>

#define WORK_TAG 1
#define DIE_TAG  2

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int N = 100;
    const int manager = 0;

    if (rank == manager) {
        /* ---- MANAGER ---- */
        int next_i = 0;
        int active = size - 1;   // how many workers still running
        MPI_Status status;
        int dummy;

        while (active > 0) {
            // Receive a request from whichever worker is free
            MPI_Recv(&dummy, 1, MPI_INT,
                     MPI_ANY_SOURCE, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);

            int worker = status.MPI_SOURCE;

            if (next_i < N) {
                // Send the next work unit index
                MPI_Send(&next_i, 1, MPI_INT,
                         worker, WORK_TAG, MPI_COMM_WORLD);
                next_i++;
            } else {
                // All work done — tell this worker to stop
                MPI_Send(&next_i, 1, MPI_INT,
                         worker, DIE_TAG, MPI_COMM_WORLD);
                active--;
            }
        }

    } else {
        /* ---- WORKER ---- */
        MPI_Status status;
        int idx;
        long local_result = 0;

        while (1) {
            // Send a request to the manager
            MPI_Send(&rank, 1, MPI_INT,
                     manager, WORK_TAG, MPI_COMM_WORLD);

            // Receive either a work unit or the termination signal
            MPI_Recv(&idx, 1, MPI_INT,
                     manager, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);

            if (status.MPI_TAG == DIE_TAG) break;

            // Compute the work
            local_result += (long)idx * idx;
        }

        printf("Worker %d computed local sum = %ld\n", rank, local_result);
    }

    MPI_Finalize();
    return 0;
}
```

**Key marking points:**
- Manager uses `MPI_ANY_SOURCE` in its `MPI_Recv`. *(1 mark)*
- Manager reads `status.MPI_SOURCE` to find which worker to reply to. *(1 mark)*
- Manager loop is `while (active > 0)` and decrements `active` only on `DIE_TAG` send. *(1 mark)*
- Worker uses `MPI_ANY_TAG` in its `MPI_Recv` and checks `status.MPI_TAG` for termination. *(1 mark)*
- Worker loop breaks on `DIE_TAG`. *(1 mark)*
- Correct `MPI_Init` / `MPI_Finalize` bookends. *(1 mark)*

---

### Q16. Write the complete OpenMP `sections` code that fills two arrays `x[N]` and `y[N]` concurrently: `x[i] = i * 2.0` and `y[i] = i * 3.0`. Declare variables with correct scoping.

**Model Answer:**

```c
#include <omp.h>

void fill_arrays(double *x, double *y, int N) {
    #pragma omp parallel default(none) shared(x, y, N)
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                for (int i = 0; i < N; i++) {
                    x[i] = i * 2.0;
                }
            }

            #pragma omp section
            {
                for (int i = 0; i < N; i++) {
                    y[i] = i * 3.0;
                }
            }
        }
        // Implicit barrier here: both sections complete before continuing
    }
}
```

**Key marking points:**
- `#pragma omp parallel` opens the team. *(1 mark)*
- `#pragma omp sections` wraps both section blocks. *(1 mark)*
- Each array fill is in its own `#pragma omp section`. *(1 mark)*
- Loop variable `i` is **local** to each section (declared inside the section), so it is automatically private. *(1 mark)*
- `x`, `y`, `N` are shared — correct for this pattern since each section writes to a different array. *(1 mark)*

---

### Q17. Convert the following serial `while` loop into an OpenMP task-based parallel version. Use `firstprivate` correctly. The function `process_node(node)` may be called in any order.

```c
// Serial version
Node *current = head;
while (current != NULL) {
    process_node(current);
    current = current->next;
}
```

**Model Answer:**

```c
#include <omp.h>

// Parallel task-based version
#pragma omp parallel default(none) shared(head)
{
    #pragma omp single
    {
        Node *current = head;
        while (current != NULL) {
            // Capture current value of 'current' at task creation time
            #pragma omp task firstprivate(current)
            {
                process_node(current);
            }
            current = current->next;
        }
        // Implicit barrier at end of 'single': all tasks complete
        // before any thread proceeds past this block
    }
}
```

**Key marking points:**
- `#pragma omp parallel` creates the thread team. *(1 mark)*
- `#pragma omp single` ensures only one thread generates tasks. *(1 mark)*
- `#pragma omp task` creates one task per node. *(1 mark)*
- `firstprivate(current)` captures the pointer value at task-creation time, preventing all tasks from seeing the post-loop value of `current`. *(2 marks)*
- The `while` loop advances `current` in the generator thread, not inside the task. *(1 mark)*

---

### Q18. Write the workers-only communicator boilerplate (in MPI C) that:
1. Excludes rank 0 from the new communicator.
2. Calls `MPI_Reduce` to sum `local_val` (a `double`) across workers only, with the result on worker-rank-0.
3. Frees all resources correctly.

**Model Answer:**

```c
MPI_Group world_group, worker_group;
MPI_Comm  worker_comm = MPI_COMM_NULL;

int manager_rank = 0;
int excluded[1] = {manager_rank};

// Step 1: get the group of MPI_COMM_WORLD
MPI_Comm_group(MPI_COMM_WORLD, &world_group);

// Step 2: build the worker group (exclude manager)
MPI_Group_excl(world_group, 1, excluded, &worker_group);

// Step 3: create the communicator — MUST be called by all ranks in MPI_COMM_WORLD
MPI_Comm_create(MPI_COMM_WORLD, worker_group, &worker_comm);

// Step 4–5: workers do the collective; manager skips (has MPI_COMM_NULL)
double global_val = 0.0;
if (worker_comm != MPI_COMM_NULL) {
    int wrank;
    MPI_Comm_rank(worker_comm, &wrank);

    // Step 5: reduce across workers only
    MPI_Reduce(&local_val, &global_val, 1, MPI_DOUBLE,
               MPI_SUM, 0, worker_comm);

    if (wrank == 0) {
        printf("Worker-root result: %f\n", global_val);
    }

    // Step 6: free the communicator
    MPI_Comm_free(&worker_comm);
}

// Free groups (all ranks)
MPI_Group_free(&worker_group);
MPI_Group_free(&world_group);
```

**Key marking points:**
- `MPI_Comm_group` called first. *(1 mark)*
- `MPI_Group_excl` with correct arguments. *(1 mark)*
- `MPI_Comm_create` called by ALL ranks (not just workers). *(1 mark)*
- Guard `if (worker_comm != MPI_COMM_NULL)` before using the communicator. *(1 mark)*
- `MPI_Reduce` uses `worker_comm`, not `MPI_COMM_WORLD`. *(1 mark)*
- Both `MPI_Comm_free` and both `MPI_Group_free` calls present. *(1 mark)*

---

### Q19. Write an OpenMP task-based parallelisation of the Mandelbrot outer loop below. Use `firstprivate` and `single` correctly. Assume `z_Re`, `z_Im`, `nIter`, `N`, and `maxIter` are declared outside the parallel region.

```c
// Serial version to parallelise:
for (int i = 0; i <= N; i++) {
    for (int j = 0; j <= N; j++) {
        double zr = 0.0, zi = 0.0;
        double cr = z_Re[i], ci = z_Im[j];
        int k;
        for (k = 0; k < maxIter; k++) {
            double zr2 = zr*zr - zi*zi + cr;
            double zi2 = 2.0*zr*zi + ci;
            zr = zr2; zi = zi2;
            if (zr*zr + zi*zi > 4.0) break;
        }
        nIter[i][j] = k;
    }
}
```

**Model Answer:**

```c
#pragma omp parallel default(none) \
        shared(z_Re, z_Im, nIter, N, maxIter)
{
    #pragma omp single
    {
        for (int i = 0; i <= N; i++) {

            // firstprivate(i): each task gets its own copy of i,
            // initialised to the value at task-creation time.
            #pragma omp task firstprivate(i) \
                            shared(z_Re, z_Im, nIter, maxIter, N)
            {
                for (int j = 0; j <= N; j++) {
                    double zr = 0.0, zi = 0.0;
                    double cr = z_Re[i], ci = z_Im[j];
                    int k;
                    for (k = 0; k < maxIter; k++) {
                        double zr2 = zr*zr - zi*zi + cr;
                        double zi2 = 2.0*zr*zi + ci;
                        zr = zr2; zi = zi2;
                        if (zr*zr + zi*zi > 4.0) break;
                    }
                    nIter[i][j] = k;
                }
            } // end task

        } // end generator loop
    } // end single — implicit barrier: all tasks complete before exit
}
```

**Key marking points:**
- `#pragma omp parallel` with `shared(...)`. *(1 mark)*
- `#pragma omp single` wrapping the generator loop. *(1 mark)*
- `#pragma omp task firstprivate(i)` inside the loop. *(2 marks)*
- The entire Mandelbrot inner computation is inside the task body. *(1 mark)*
- No race condition: each task writes to a distinct row `nIter[i][:]`. *(1 mark)*

---

## Section D: Explain / Describe

---

### Q20. Explain why the manager-worker pattern provides better load balancing than static domain decomposition for the Mandelbrot set calculation.

**Model Answer (key points for 6 marks):**

- **Static domain decomposition** divides the N+1 columns into p equal-sized contiguous chunks, one per process. If some columns are inside the Mandelbrot set (requiring `maxIter` iterations) and others escape immediately (1 iteration), some processes receive "expensive" chunks and others "cheap" chunks. The overall runtime is bounded by the slowest process — the one holding the most expensive columns. Fast processes sit idle waiting at the next barrier. *(2 marks)*

- **Manager-worker** hands out one column at a time on demand. When a worker finishes a column, it immediately asks for the next — so fast workers do more columns and slow workers do fewer. The total work naturally balances at runtime. The overall runtime is determined by the last task assigned, not by the unlucky static allocation. *(2 marks)*

- **Mandelbrot's irregular work** is the textbook motivation: per-pixel cost is inherently unpredictable (depends on whether the point converges), so any static partition will be unbalanced. Dynamic assignment is the only way to guarantee good balance. *(1 mark)*

- **Analogy:** manager-worker in MPI is the distributed-memory equivalent of `schedule(dynamic)` in OpenMP — both assign work units on demand at runtime. *(1 mark)*

---

### Q21. Explain what would happen if `MPI_Comm_create` were called **only by the worker processes** (i.e. the manager skipped the call). What is the correct behaviour?

**Model Answer:**

`MPI_Comm_create` is a **collective operation** over the parent communicator (in this case `MPI_COMM_WORLD`). Every process in `MPI_COMM_WORLD` must call it, regardless of whether they will be in the new group.

If rank 0 (the manager) skips the call while the other ranks call it, the operation will **deadlock**: the workers will all block inside `MPI_Comm_create` waiting for the manager to participate, while the manager has moved on to a different code path and is no longer listening.

The correct approach: **all processes call `MPI_Comm_create`**. Processes not in the new group simply receive `MPI_COMM_NULL` as their communicator result, which they can test and then skip any operations using that communicator.

*(3 marks: 1 for collective requirement, 1 for deadlock consequence, 1 for MPI_COMM_NULL handling.)*

---

### Q22. Describe when it is appropriate to use OpenMP `sections` versus OpenMP `task`. Give one concrete example of each.

**Model Answer:**

**`#pragma omp sections` is appropriate when:**
- The number of distinct code blocks is **small and known at compile time**.
- The blocks are **heterogeneous** (different operations, not the same operation on different data).
- The work per block is **roughly equal** (sections cannot dynamically rebalance; each section runs on exactly one thread).

*Example:* Filling two separate arrays with different functions:
```c
#pragma omp sections
{
    #pragma omp section
    { for (int i=0; i<N; i++) x[i] = sin(i); }
    #pragma omp section
    { for (int i=0; i<N; i++) y[i] = cos(i); }
}
```

**`#pragma omp task` is appropriate when:**
- The number of work units is **large or unknown at compile time**.
- The work is **irregular** — different units take different amounts of time.
- The parallelism comes from a **recursive** structure, a linked list traversal, or a `while` loop with data-dependent termination.

*Example:* Processing nodes of a linked list of unknown length:
```c
#pragma omp single
{
    Node *n = head;
    while (n != NULL) {
        #pragma omp task firstprivate(n)
        { process(n); }
        n = n->next;
    }
}
```

*(4 marks: 1 for each when-to-use description, 1 for each correct example.)*

---

### Q23. Why does the manager process in the MPI manager-worker pattern use a `while` loop rather than a `for` loop to distribute work?

**Model Answer:**

In a `for` loop the number of iterations is fixed at the start. In the manager-worker pattern, the manager does not simply iterate through work units in order — it responds to **requests** from workers, and the number of requests it will receive is not directly the number of work units `N`. Each worker may make several requests (one per work unit it processes), and requests arrive in an unpredictable order.

The manager continues until **all workers have been sent a termination signal** — a condition tracked by the `active` counter. The loop terminates when `active` reaches zero, which happens only after the manager has (a) given out all N work units and (b) sent a DIE_TAG to every worker. This is inherently a **condition-based** (while) rather than a count-based (for) termination.

Additionally, since workers request work asynchronously, the manager cannot pre-compute how many requests it will service per worker — using `while` with a wildcard receive correctly models the reactive, demand-driven nature of the pattern.

*(3 marks: 1 for request-driven model, 1 for active counter logic, 1 for unpredictable order.)*

---

## Section E: Compare / Contrast

---

### Q24. Complete the following comparison table between MPI manager-worker and OpenMP task-based parallelism.

| Aspect | MPI Manager-Worker | OpenMP Tasks |
|:---|:---|:---|
| Memory model | ? | ? |
| Work distributor | ? | ? |
| Work request mechanism | ? | ? |
| Termination signal | ? | ? |
| Aggregating results | ? | ? |
| Idle process/thread? | ? | ? |
| Typical cost per work unit | ? | ? |

**Model Answer:**

| Aspect | MPI Manager-Worker | OpenMP Tasks |
|:---|:---|:---|
| Memory model | Distributed memory (across nodes) | Shared memory (within a node) |
| Work distributor | Dedicated manager process (rank 0) | One thread executing inside `omp single` |
| Work request mechanism | Explicit `MPI_Send` from worker to manager | Implicit: threads pull from runtime task queue |
| Termination signal | Manager sends `DIE_TAG` message | Generator exits the `single` block; implicit barrier consumes remaining tasks |
| Aggregating results | `MPI_Reduce` on a workers-only communicator | Workers write into shared array; no message needed |
| Idle process/thread? | Yes — manager does no compute | No — generator joins task pool after the loop |
| Typical cost per work unit | Must be coarse (round-trip MPI message overhead) | Can be fine-grained (queue push/pop is cheap) |

*(1 mark per correct row, 7 marks total.)*

---

### Q25. Compare **static** and **dynamic** work distribution. For each of the following scenarios, state which strategy is preferable and justify your choice.

**(a)** Solving a simple 1-D advection equation where each grid point update costs the same amount.

**(b)** Computing the Mandelbrot set where iteration counts per pixel vary from 1 to `maxIter`.

**(c)** A parallel reduction where each iteration performs a single floating-point addition.

**Model Answer:**

**(a) 1-D advection — Static is preferable.**
All grid point updates require exactly the same computation (one stencil evaluation), so a static block assignment will keep all threads equally busy. Dynamic scheduling would add unnecessary overhead (queue management, atomic counter increments) with no benefit because there is no imbalance to correct. *(2 marks)*

**(b) Mandelbrot — Dynamic is preferable (or manager-worker in MPI).**
The work per pixel varies enormously: points inside the set take `maxIter` steps; points far outside escape in one step. A static block decomposition assigns some threads cheap strips and some threads expensive strips, causing severe load imbalance. Dynamic scheduling (OpenMP `schedule(dynamic)`) or MPI manager-worker assigns columns on demand, so faster threads automatically pick up more work. *(2 marks)*

**(c) Simple parallel reduction — Static is preferable.**
Each iteration is trivially cheap (one addition), so scheduling overhead would dwarf the actual computation. Furthermore, a reduction is a well-understood pattern where the runtime can split iterations equally with `schedule(static)` or the `reduction` clause. Dynamic scheduling would be wasteful. *(2 marks)*

---

## Section F: Multi-Part Exam Questions

---

### Q26. (Multi-part — 14 marks total)

A research group wants to parallelise a simulation where the total work consists of 500 independent jobs, each of unpredictable duration. They have 9 MPI processes available (ranks 0–8) and choose a manager-worker approach.

**(a)** Explain the role of the manager process and the role of the worker processes in this design. Why is one process dedicated to management rather than giving all processes equal roles? *(4 marks)*

**(b)** Why must `MPI_ANY_SOURCE` be used in the manager's receive call? What would happen if the manager used a fixed source rank (e.g. rank 1) instead? *(3 marks)*

**(c)** After all 500 jobs are complete, the research group wants to compute the **average** result across all workers using `MPI_Reduce` with `MPI_SUM`, and then divide by 8. Explain why calling `MPI_Reduce` on `MPI_COMM_WORLD` is problematic, and outline the steps needed to perform the reduction on workers only. *(4 marks)*

**(d)** Suggest one disadvantage of the manager-worker approach compared to static domain decomposition, and describe a scenario where static decomposition would actually be faster. *(3 marks)*

---

**Model Answer:**

**(a)** (4 marks)

- The **manager** (rank 0) holds the queue of 500 job indices. It waits in a loop, receives requests from any worker, sends the next available job index, and counts down until all jobs are distributed and all workers are terminated. The manager performs **no computation itself**. *(1 mark)*
- The **workers** (ranks 1–8) repeatedly: send a request to the manager, receive a job index, execute that job (compute a result), and immediately ask for the next job. They stop when the manager sends a termination tag. *(1 mark)*
- One process is dedicated to management because the manager's task (receiving requests from an arbitrary source, maintaining the job queue, and dispatching) requires its full attention — if the manager also computed, it might miss a worker's request while busy, creating a bottleneck. Additionally, having a single dispatcher avoids race conditions on the job queue. *(2 marks)*

**(b)** (3 marks)

- `MPI_ANY_SOURCE` is needed because the manager cannot predict which of the 8 workers will finish its current job next. Any worker might send the next request at any time. *(1 mark)*
- If the manager used a fixed source (e.g. `source = 1`), it would block waiting for rank 1 to send a request even if ranks 2–8 are all idle and ready. The manager could not respond to the other workers until rank 1 next sends — this would cause **partial deadlock** (workers waiting for work while the manager ignores them) and destroy the dynamic load-balancing benefit. *(2 marks)*

**(c)** (4 marks)

- `MPI_Comm_world` includes the manager (rank 0), which has **no result data** — it performed no computation. Including it in `MPI_Reduce` would force the manager to contribute a meaningless value (e.g. uninitialised memory) to the sum, giving an incorrect total. *(1 mark)*
- Steps to perform a workers-only reduction:
  1. Call `MPI_Comm_group(MPI_COMM_WORLD, &worldGroup)` to get the world group. *(1 mark)*
  2. Call `MPI_Group_excl(worldGroup, 1, {0}, &workerGroup)` to exclude rank 0. *(0.5 mark)*
  3. Call `MPI_Comm_create(MPI_COMM_WORLD, workerGroup, &workerComm)` — all ranks must call this; rank 0 gets `MPI_COMM_NULL`. *(0.5 mark)*
  4. Workers call `MPI_Reduce(&local, &global, 1, MPI_DOUBLE, MPI_SUM, 0, workerComm)` and then rank 0 of `workerComm` divides by 8. *(1 mark)*

**(d)** (3 marks)

- **Disadvantage of manager-worker:** Every work unit requires a round-trip message to the manager (worker sends request, manager replies with job). For small, fast jobs, this communication overhead may dominate the computation time and make manager-worker **slower** than static decomposition. The manager can also become a bottleneck if work units are very small and workers complete them faster than the manager can respond. *(2 marks)*
- **Scenario where static is faster:** If each of the 500 jobs takes exactly the same time to compute, simply assigning 62–63 jobs per worker (static distribution) achieves perfect balance with no communication overhead at all — far outperforming manager-worker. *(1 mark)*

---

### Q27. (Multi-part — 12 marks total)

Consider the following OpenMP `task` program for traversing a binary tree and computing a sum of values stored at each node:

```c
typedef struct Node {
    int value;
    struct Node *left;
    struct Node *right;
} Node;

long tree_sum;

void process_tree(Node *root) {
    #pragma omp parallel default(none) shared(tree_sum, root)
    {
        #pragma omp single
        {
            tree_sum = 0;
            traverse(root);
        }
    }
}

void traverse(Node *node) {
    if (node == NULL) return;

    #pragma omp task firstprivate(node)
    {
        tree_sum += node->value;   // <-- potential issue here
        traverse(node->left);
        traverse(node->right);
    }
}
```

**(a)** Explain what the `firstprivate(node)` clause achieves in this recursive task pattern. Why is it necessary here? *(3 marks)*

**(b)** Identify the data race in the code above. Explain what causes it and how it could manifest as a bug. *(3 marks)*

**(c)** Propose a fix for the data race identified in (b), writing the corrected line(s) of code. *(2 marks)*

**(d)** The `traverse` function calls itself recursively inside a task body, creating new child tasks. Explain how `taskwait` could be used here, and what it would guarantee. *(4 marks)*

---

**Model Answer:**

**(a)** (3 marks)

`firstprivate(node)` creates a **private copy** of the `node` pointer for each task, initialised to the value `node` had at the moment the `#pragma omp task` construct was encountered — i.e. the value passed to the current `traverse()` call.

In a recursive setting, the `node` argument is a local variable on the call stack of each invocation of `traverse`. Without `firstprivate`, the task might capture a reference to a variable that is modified by the time the task runs. With `firstprivate`, each task gets its own immutable snapshot of the pointer, ensuring it processes the correct subtree node regardless of when the task is actually scheduled.

*(1 mark: what firstprivate does; 1 mark: why needed in recursive context; 1 mark: correct snapshot explanation.)*

**(b)** (3 marks)

The data race is on `tree_sum`:

```c
tree_sum += node->value;
```

`tree_sum` is a global `long` declared `shared`. Multiple tasks may execute concurrently, each reading and updating `tree_sum` simultaneously. The `+=` operation is **not atomic** — it is a load-modify-store sequence. Two tasks can both read the same value of `tree_sum`, both add their `node->value`, and both write back — one update is lost. The final value of `tree_sum` will be less than the true sum of all node values, and the result is **non-deterministic** (different between runs).

*(1 mark: identifies `tree_sum += node->value`; 1 mark: explains non-atomic load-modify-store; 1 mark: consequence — lost updates.)*

**(c)** (2 marks)

Use `#pragma omp atomic` to make the update thread-safe:

```c
#pragma omp atomic
tree_sum += node->value;
```

Alternatively, restructure to use a local accumulator per task and a reduction — but `atomic` is the simplest direct fix in this context.

*(1 mark for `atomic`; 1 mark for correct placement.)*

**(d)** (4 marks)

`#pragma omp taskwait` is a synchronisation directive that **suspends the current task until all child tasks it has directly created are complete**.

In the recursive `traverse` pattern:

```c
void traverse(Node *node) {
    if (node == NULL) return;

    #pragma omp task firstprivate(node)
    {
        tree_sum += node->value;

        // Create child tasks for subtrees
        #pragma omp task firstprivate(node)
        traverse(node->left);

        #pragma omp task firstprivate(node)
        traverse(node->right);

        // Wait for both child tasks to finish before this task exits
        #pragma omp taskwait
    }
}
```

`taskwait` guarantees that the left and right subtree traversals are complete before the current node's task exits. This is important if the current node's result depends on its children (e.g. a tree-reduction where each node accumulates its children's sums). Without `taskwait`, the parent task might continue or terminate before the subtrees are processed, leading to incorrect partial results.

In the original code above (where only `tree_sum` is updated atomically), `taskwait` is not strictly required for correctness, but it gives the runtime a natural synchronisation point and helps bound the number of simultaneously live tasks.

*(2 marks for correct definition of taskwait; 2 marks for placing it correctly and explaining the guarantee.)*

---

### Q28. (Multi-part — 10 marks total)

**(a)** In the OpenMP `single` construct, there is an implicit barrier at the end by default. Explain what this barrier guarantees in the context of task generation. *(2 marks)*

**(b)** A student writes the following code, intending to generate tasks in parallel (all threads generate tasks simultaneously) to speed up task creation. Explain why this is incorrect.

```c
#pragma omp parallel num_threads(4) default(none) shared(N, data)
{
    // No 'single' — all 4 threads reach this loop
    for (int i = 0; i < N; i++) {
        #pragma omp task firstprivate(i) shared(data)
        {
            process(data, i);
        }
    }
}
```
*(3 marks)*

**(c)** The student's supervisor suggests using `#pragma omp taskloop` instead. Briefly describe what `taskloop` does and how it differs from manually writing `#pragma omp task` inside `#pragma omp single`. *(3 marks)*

**(d)** Write the corrected version of the student's code from (b) using the standard `single` + `task` pattern. *(2 marks)*

---

**Model Answer:**

**(a)** (2 marks)

The implicit barrier at the end of `single` ensures that **no thread proceeds past the `single` construct until the one thread executing it has finished, and crucially until all tasks generated within it have been queued**. In practice, the barrier means the entire thread team waits until the task generation loop is complete, guaranteeing that all task objects exist before threads start competing to execute them. It also ensures that code following the `single` block will not run until all queued tasks have been executed (the barrier at the end of the parallel region serves as a taskwait).

*(1 mark for "waits for single block to finish"; 1 mark for "tasks complete before parallel region exits".)*

**(b)** (3 marks)

Without `single`, all 4 threads execute the `for` loop independently. Each thread generates tasks for **all N values of `i`**, so the total number of tasks created is `4 × N` instead of `N`. The task for index `i` is created 4 times and executed 4 times — `process(data, i)` runs **4 times on the same data for every `i`**, producing incorrect results (e.g. quadruple-processed output) and wasting computation.

Furthermore, if `process` writes to shared memory, the repeated concurrent execution of the same task body on the same data element creates additional data races.

*(1 mark for 4× duplication; 1 mark for incorrect output; 1 mark for race condition.)*

**(c)** (3 marks)

`#pragma omp taskloop` (added in OpenMP 4.5) applies to a `for` loop and automatically generates one task per iteration (or per chunk), distributing them across the thread team without requiring an explicit `single` block.

Differences from manual `single` + `task`:
- `taskloop` is more concise — the `single` + task-generation boilerplate is replaced by a single directive on the loop.
- `taskloop` can optionally group multiple iterations into one task (`grainsize` or `num_tasks` clauses), giving the runtime more control over granularity without manual tuning.
- Manual `single` + `task` is more flexible — the generator can be a `while` loop, a recursive call, or any irregular code structure; `taskloop` requires a standard `for` loop with a known structure.

*(1 mark for what taskloop does; 1 mark for syntactic difference; 1 mark for flexibility comparison.)*

**(d)** (2 marks)

```c
#pragma omp parallel num_threads(4) default(none) shared(N, data)
{
    #pragma omp single
    {
        for (int i = 0; i < N; i++) {
            #pragma omp task firstprivate(i) shared(data)
            {
                process(data, i);
            }
        }
    } // implicit barrier: all tasks complete before any thread exits
}
```

*(1 mark for `#pragma omp single`; 1 mark for structurally correct code.)*

---

## Quick Reference: Key Facts for Exam

| Fact | Value |
|:---|:---|
| OpenMP tasks introduced in | OpenMP 3.0 |
| Wildcard for any sender | `MPI_ANY_SOURCE` |
| Wildcard for any tag | `MPI_ANY_TAG` |
| Actual sender after wildcard recv | `status.MPI_SOURCE` |
| Actual tag after wildcard recv | `status.MPI_TAG` |
| Function to exclude ranks from a group | `MPI_Group_excl` |
| Function to include ranks in a group | `MPI_Group_incl` |
| Non-member result from `MPI_Comm_create` | `MPI_COMM_NULL` |
| `MPI_Comm_create` is | Collective over parent communicator |
| `single` vs `master` | `single` = any thread + implicit barrier; `master` = thread 0, no barrier |
| `firstprivate(x)` in task | Private copy of x, initialised at task creation |
| Granularity rule | More tasks than threads |
| Manager-worker MPI analogue in OpenMP | `schedule(dynamic)` |
| Why `while` not `for` in manager | Request-driven, not iteration-driven termination |

---

*Source pages: [Manager-Worker Model](../wiki/concepts/Manager_Worker_Model.md) · [MPI Advanced Features](../wiki/concepts/MPI_Advanced_Features.md) · [OpenMP Advanced Work Sharing](../wiki/concepts/OpenMP_Advanced_Work_Sharing.md) · [OpenMP Tasks](../wiki/concepts/OpenMP_Tasks.md) · [Manager-Worker Final Prep](../wiki/final_prep/Manager_Worker_and_Tasks.md)*
