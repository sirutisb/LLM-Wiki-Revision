---
title: "Manager-Worker and Task-Based Parallelism — Complete Exam Reference"
tags: [hpc, week-8, mpi, openmp, manager-worker, tasks, communicators, mandelbrot, final-prep]
date: 2026-05-13
---

# Manager-Worker & Task-Based Parallelism — Complete Exam Reference

This is a one-stop reference for Week 8 material: the **manager-worker** model, **task-based parallelism**, **MPI wildcards**, **MPI groups and communicators**, **OpenMP sections / single / tasks**, and the **Mandelbrot set** as the canonical worked example in both MPI and OpenMP.

---

## 1. Motivation — Why Beyond Loops and Domain Decomposition?

So far we have used two data-parallel approaches:

| Approach | What it does | Limitation |
|---|---|---|
| **OpenMP parallel loops** | Same operation on different loop iterations | Requires a known trip count, regular work per iteration |
| **MPI domain decomposition** | Each process owns a chunk of the data | Static allocation → load imbalance if work per chunk varies |

Both are **data parallel**: same operations, different data. They fail when:

- Work per unit varies wildly (Mandelbrot: a single point may converge in 1 iteration or take the full `maxIter`)
- The problem is **recursive** (e.g. tree traversal, divide-and-conquer)
- The problem traverses a **linked list** of unknown length
- We have **heterogeneous tasks** — different operations on the same data

The two alternatives introduced in Week 8:

- **Manager-Worker** (MPI pattern): one process hands out work units on demand; workers pull when ready → dynamic load balancing.
- **Task-based parallelism** (OpenMP construct): one thread generates discrete tasks; any thread in the team picks them up from a queue.

> Key parallel: manager-worker (MPI) ≈ `schedule(dynamic)` (OpenMP). Both load-balance at runtime.

---

## 2. The Manager-Worker Model — Concept

### 2.1 Roles

- **Manager (rank 0 by convention):** holds the queue of work units. Performs **no computation**. Waits for any worker to ask for work, sends back the next unit, and tracks when work is exhausted.
- **Workers (all other ranks):** loop forever asking for work → computing → returning results → asking again. Stop when the manager sends a termination flag.

### 2.2 Why it works for load balancing

Fast workers naturally complete more units; slow workers complete fewer. The total time is bounded by the **slowest worker on its last unit**, not by the worst-case allocation made up front. This matches OpenMP's `schedule(dynamic)` for loops — work goes to whichever worker is free.

### 2.3 Trade-offs

| Pros | Cons |
|---|---|
| Automatic dynamic load balancing | Manager rank does no compute → wastes one process |
| Resilient to heterogeneous work | Every work unit incurs round-trip comms with manager |
| Easy to scale to more workers | Manager can become a bottleneck if work units are tiny |

**Granularity matters:** units must be large enough that compute time ≫ communication overhead, but small enough to give the manager flexibility.

---

## 3. MPI Building Blocks for Manager-Worker

To implement manager-worker in MPI, we need two features beyond plain point-to-point:

1. **Wildcards** — so the manager can receive from "whoever asks first."
2. **Groups & communicators** — so collective ops (like `MPI_Reduce`) can be done **across workers only**, excluding the idle manager.

### 3.1 Wildcards

In a `for` loop with fixed ranks we know who sends to whom. In manager-worker we **don't** — any worker might finish next.

| Wildcard | Where used | Effect |
|---|---|---|
| `MPI_ANY_SOURCE` | `source` arg of `MPI_Recv` | Accept message from any rank |
| `MPI_ANY_TAG` | `tag` arg of `MPI_Recv` | Accept message with any tag |

The actual sender and tag are recovered from the `MPI_Status` object:

```c
MPI_Status status;
int buf;
MPI_Recv(&buf, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG,
         MPI_COMM_WORLD, &status);

int worker_rank = status.MPI_SOURCE;   // who sent it
int recv_tag    = status.MPI_TAG;      // what tag they used
```

Reply directly to that worker using `worker_rank` as the `dest` in the matching `MPI_Send`.

### 3.2 Full signature of `MPI_Recv` (recap)

```c
int MPI_Recv(void *buf, int count, MPI_Datatype datatype,
             int source, int tag, MPI_Comm comm, MPI_Status *status);
```

- `source`: explicit rank **or** `MPI_ANY_SOURCE`
- `tag`: user label **or** `MPI_ANY_TAG`
- `status`: written-to struct with `.MPI_SOURCE`, `.MPI_TAG`

---

## 4. MPI Groups and Communicators

### 4.1 Why a new communicator?

`MPI_COMM_WORLD` includes **every** process. If we want a collective like `MPI_Reduce` to operate **only on workers** (manager has no result to contribute), we need a communicator that excludes the manager. Calling `MPI_Reduce` on `MPI_COMM_WORLD` would force the manager to participate, which it cannot — it has no data of the right shape and would just be dead weight.

### 4.2 The standard 6-step recipe

This is examinable — memorise the order.

```
1. Get the group of MPI_COMM_WORLD       → MPI_Comm_group
2. Build a new group (include or exclude) → MPI_Group_incl / MPI_Group_excl
3. Create the new communicator           → MPI_Comm_create
4. Get rank in the new communicator      → MPI_Comm_rank
5. Do work / collective comms            → using new comm
6. Free the communicator and group       → MPI_Comm_free, MPI_Group_free
```

### 4.3 Group construction functions

| Function | Result |
|---|---|
| `MPI_Group_incl` | New group **including** specified ranks of an existing group |
| `MPI_Group_excl` | New group **excluding** specified ranks of an existing group |
| `MPI_Group_union` | All of group A followed by elements of B not in A |
| `MPI_Group_intersection` | Elements in both A and B |
| `MPI_Group_difference` | Elements in A not in B |

### 4.4 Concrete pattern — workers-only communicator

```c
MPI_Group worldGroup, workerGroup;
MPI_Comm  workerComm;

int manager = 0;
int ranks_to_exclude[1] = {manager};

// 1. Group of MPI_COMM_WORLD
MPI_Comm_group(MPI_COMM_WORLD, &worldGroup);

// 2. Build a group with the manager removed
MPI_Group_excl(worldGroup, 1, ranks_to_exclude, &workerGroup);

// 3. Create the new communicator (collective on MPI_COMM_WORLD)
MPI_Comm_create(MPI_COMM_WORLD, workerGroup, &workerComm);

// 4. Workers now have a valid workerComm; manager gets MPI_COMM_NULL
if (workerComm != MPI_COMM_NULL) {
    int newRank;
    MPI_Comm_rank(workerComm, &newRank);
    // 5. Do collective work — only workers participate
    MPI_Reduce(local, global, count, MPI_INT, MPI_SUM, 0, workerComm);

    // 6. Cleanup
    MPI_Comm_free(&workerComm);
}
MPI_Group_free(&workerGroup);
MPI_Group_free(&worldGroup);
```

> **Important:** `MPI_Comm_create` is **collective over the parent communicator** (here `MPI_COMM_WORLD`). Every process in the parent must call it, even those not in the new group — they simply receive `MPI_COMM_NULL`.

---

## 5. Manager-Worker in MPI — Code Skeleton

Below is the canonical pattern with comments showing how each piece fits.

```c
#include <mpi.h>

#define WORK_TAG 1
#define DIE_TAG  2

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int N = 1000;                 // total work units
    const int manager = 0;

    if (rank == manager) {
        /* ------------- MANAGER ------------- */
        int next_i = 0;
        int active_workers = size - 1;
        MPI_Status status;
        int dummy;

        while (active_workers > 0) {
            // Receive a request from any worker
            MPI_Recv(&dummy, 1, MPI_INT,
                     MPI_ANY_SOURCE, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);

            int worker = status.MPI_SOURCE;

            if (next_i < N) {
                // Hand out the next work unit
                MPI_Send(&next_i, 1, MPI_INT,
                         worker, WORK_TAG, MPI_COMM_WORLD);
                next_i++;
            } else {
                // No more work — tell this worker to stop
                MPI_Send(&next_i, 1, MPI_INT,
                         worker, DIE_TAG, MPI_COMM_WORLD);
                active_workers--;
            }
        }
    } else {
        /* ------------- WORKER ------------- */
        MPI_Status status;
        int i, my_rank = rank;

        while (1) {
            // 1) Ask manager for work
            MPI_Send(&my_rank, 1, MPI_INT,
                     manager, WORK_TAG, MPI_COMM_WORLD);

            // 2) Receive either a work unit or a termination flag
            MPI_Recv(&i, 1, MPI_INT,
                     manager, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);

            if (status.MPI_TAG == DIE_TAG) break;

            // 3) Compute the work unit (e.g. one column i of Mandelbrot)
            compute_work_unit(i);
        }
    }

    MPI_Finalize();
    return 0;
}
```

Key features mapped to the lectures:

- **Wildcard `MPI_ANY_SOURCE`** lets the manager respond to whichever worker asks first.
- **Tags `WORK_TAG` / `DIE_TAG`** distinguish "here is work" from "we are done."
- The manager's loop is a **`while`**, not a `for` — we don't know how many requests we will receive in total (each worker requests `N/(size-1) + 1` times).

---

## 6. Splitting a Big Problem → Manager-Worker → Reduce — End-to-End Pattern

Putting everything together: split a large problem (an integer count, a partial sum, a Mandelbrot grid) so that workers compute partial answers, then aggregate via `MPI_Reduce` on a **workers-only** communicator.

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

    const int N = 10000;
    const int manager = 0;

    /* -------- 1. Build a workers-only communicator -------- */
    MPI_Group worldGroup, workerGroup;
    MPI_Comm  workerComm = MPI_COMM_NULL;
    int excluded[1] = {manager};
    MPI_Comm_group(MPI_COMM_WORLD, &worldGroup);
    MPI_Group_excl(worldGroup, 1, excluded, &workerGroup);
    MPI_Comm_create(MPI_COMM_WORLD, workerGroup, &workerComm);

    long local_sum = 0;   // each worker accumulates here

    if (rank == manager) {
        /* -------- 2a. Manager hands out work -------- */
        int next_i = 0;
        int active = size - 1;
        MPI_Status status;
        int dummy;

        while (active > 0) {
            MPI_Recv(&dummy, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
            int w = status.MPI_SOURCE;
            if (next_i < N) {
                MPI_Send(&next_i, 1, MPI_INT, w, WORK_TAG, MPI_COMM_WORLD);
                next_i++;
            } else {
                MPI_Send(&next_i, 1, MPI_INT, w, DIE_TAG, MPI_COMM_WORLD);
                active--;
            }
        }
    } else {
        /* -------- 2b. Workers compute -------- */
        MPI_Status status;
        int i;
        while (1) {
            MPI_Send(&rank, 1, MPI_INT, manager, WORK_TAG, MPI_COMM_WORLD);
            MPI_Recv(&i, 1, MPI_INT, manager, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
            if (status.MPI_TAG == DIE_TAG) break;

            // Toy "work": accumulate i*i
            local_sum += (long)i * i;
        }
    }

    /* -------- 3. Reduce across workers only -------- */
    long global_sum = 0;
    if (workerComm != MPI_COMM_NULL) {
        MPI_Reduce(&local_sum, &global_sum, 1, MPI_LONG, MPI_SUM,
                   0, workerComm);   // root = rank 0 of workerComm
        // Worker-0 now holds the final aggregated answer
        int wrank;
        MPI_Comm_rank(workerComm, &wrank);
        if (wrank == 0) {
            printf("Aggregated sum across workers: %ld\n", global_sum);
            // Optionally send back to the manager
            MPI_Send(&global_sum, 1, MPI_LONG, manager, 99, MPI_COMM_WORLD);
        }
    }

    /* -------- 4. Manager can collect the single aggregated value -------- */
    if (rank == manager) {
        MPI_Status status;
        MPI_Recv(&global_sum, 1, MPI_LONG, MPI_ANY_SOURCE, 99,
                 MPI_COMM_WORLD, &status);
        printf("Manager received final result: %ld\n", global_sum);
    }

    /* -------- 5. Cleanup -------- */
    if (workerComm != MPI_COMM_NULL) MPI_Comm_free(&workerComm);
    MPI_Group_free(&workerGroup);
    MPI_Group_free(&worldGroup);

    MPI_Finalize();
    return 0;
}
```

Walkthrough of the lifecycle:

1. **Split** — problem of size N is decomposed into N independent work units (here single integers, but in Mandelbrot each unit is a column).
2. **Distribute** — manager assigns one unit at a time, dynamically.
3. **Workers compute** — each accumulates `local_sum` for the units it processed.
4. **Reduce across workers only** — using a worker communicator excluding the manager; root = rank 0 of `workerComm`.
5. **Aggregate to root** — worker-0 sends the final value back to the manager via a single point-to-point message.
6. **Cleanup** — free communicator and group; finalize MPI.

---

## 7. Mandelbrot — Recap of the Algorithm

The Mandelbrot set: for each complex point `c`, iterate `z ← z² + c` starting from `z = 0`. Count iterations until `|z| > 2` (escape) or until `maxIter` is reached. The work per pixel is **highly variable** — points inside the set run the full `maxIter`; points far outside escape in one step. This is the textbook motivation for dynamic scheduling.

Grid setup (from `mandelbrot_mpi_mw.c`):

- `N` intervals on each axis → `(N+1) × (N+1)` grid points
- `maxIter` iterations per point
- `z_Re[i]` and `z_Im[j]` populated with grid coordinates
- Result stored in `nIter[i][j]` — the iteration count at each point

The outer loop is over `i` (columns along the real axis); column `i` is the natural unit of work.

---

## 8. Mandelbrot — MPI Manager-Worker Version

This combines everything from sections 3–6 specialised to Mandelbrot.

### 8.1 Structure (matching `mandelbrot_mpi_mw.c` from the lecture)

```c
#include <mpi.h>
#include <stdio.h>

#define WORK_TAG 1
#define DIE_TAG  2

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    double t0 = MPI_Wtime();
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int N = 1000;          // grid intervals per axis
    const int maxIter = 5000;
    const int manager = 0;

    double z_Re[N+1], z_Im[N+1];
    int    nIter[N+1][N+1];

    // Initialise nIter to zero; populate axes
    for (int i = 0; i <= N; i++) {
        for (int j = 0; j <= N; j++) nIter[i][j] = 0;
        z_Re[i] = -2.0 + 3.0 * i / N;
        z_Im[i] = -1.5 + 3.0 * i / N;
    }

    if (rank == manager) {
        /* ---- Manager hands out column indices i ---- */
        int next_i = 0;
        int active = size - 1;
        MPI_Status status;
        int dummy;

        while (active > 0) {
            MPI_Recv(&dummy, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
            int w = status.MPI_SOURCE;
            if (next_i <= N) {
                MPI_Send(&next_i, 1, MPI_INT, w, WORK_TAG, MPI_COMM_WORLD);
                next_i++;
            } else {
                MPI_Send(&next_i, 1, MPI_INT, w, DIE_TAG, MPI_COMM_WORLD);
                active--;
            }
        }
    } else {
        /* ---- Worker computes one column at a time ---- */
        MPI_Status status;
        int i;
        while (1) {
            MPI_Send(&rank, 1, MPI_INT, manager, WORK_TAG, MPI_COMM_WORLD);
            MPI_Recv(&i, 1, MPI_INT, manager, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
            if (status.MPI_TAG == DIE_TAG) break;

            // Compute the whole column i
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
    }

    /* ---- Reduce nIter across workers only ---- */
    MPI_Group worldGroup, workerGroup;
    MPI_Comm  workerComm = MPI_COMM_NULL;
    int excl[1] = {manager};
    MPI_Comm_group(MPI_COMM_WORLD, &worldGroup);
    MPI_Group_excl(worldGroup, 1, excl, &workerGroup);
    MPI_Comm_create(MPI_COMM_WORLD, workerGroup, &workerComm);

    if (workerComm != MPI_COMM_NULL) {
        // Pack nIter into a 1D buffer for the reduction
        int buf_in[(N+1)*(N+1)];
        int buf_out[(N+1)*(N+1)];
        for (int i = 0; i <= N; i++)
            for (int j = 0; j <= N; j++)
                buf_in[i*(N+1)+j] = nIter[i][j];

        // Each column was touched by exactly one worker, others have 0
        // → MPI_SUM works as "merge non-zero contributions"
        MPI_Reduce(buf_in, buf_out, (N+1)*(N+1), MPI_INT, MPI_SUM,
                   0, workerComm);

        int wrank;
        MPI_Comm_rank(workerComm, &wrank);
        if (wrank == 0) {
            // Unpack and write results to file
            for (int i = 0; i <= N; i++)
                for (int j = 0; j <= N; j++)
                    nIter[i][j] = buf_out[i*(N+1)+j];
            // write_to_file(nIter);
        }

        MPI_Comm_free(&workerComm);
    }
    MPI_Group_free(&workerGroup);
    MPI_Group_free(&worldGroup);

    double t1 = MPI_Wtime();
    printf("Rank %d elapsed %f s\n", rank, t1 - t0);
    MPI_Finalize();
    return 0;
}
```

### 8.2 Why this should scale well

Per the lecture: this **should scale better than a domain decomposition** because the work-per-column varies enormously (some columns are entirely inside the set → expensive; others escape immediately → cheap). A static block decomposition would assign whole stripes to whole ranks and waste them. Manager-worker rebalances dynamically — **the analogue of `schedule(dynamic)` in OpenMP**.

### 8.3 Key implementation tricks

| Pattern | What it does |
|---|---|
| `while (active > 0)` on manager | Continue until every worker has been told to die |
| `MPI_ANY_SOURCE` on manager's `MPI_Recv` | Whichever worker is free responds |
| `status.MPI_TAG == DIE_TAG` on worker | Workers know when to exit |
| Pack 2-D `nIter` into 1-D buffer | `MPI_Reduce` needs a contiguous buffer |
| `MPI_SUM` on workers-only comm | Each column is written by exactly one worker; other workers hold zero → sum is a valid merge |
| Exclude manager from comm | Manager has no `nIter` data to contribute |

---

## 9. OpenMP Work-Sharing Constructs (Recap)

OpenMP provides three classical work-sharing constructs (the only ones in C before OpenMP 3.0):

| Construct | Use |
|---|---|
| `#pragma omp for` | Distribute loop iterations across threads |
| `#pragma omp sections` | Run two or more independent code blocks concurrently |
| `#pragma omp single` | Have exactly one thread (any one) execute a block |

OpenMP 3.0 added **tasks** for irregular parallelism.

### 9.1 `sections`

Use when you have several distinct blocks of code that can run in parallel — not iterations of a loop.

```c
#pragma omp parallel
{
    #pragma omp sections
    {
        #pragma omp section
        {
            // Block A — e.g. fill array x
            for (int i = 0; i < N; i++) x[i] = f(i);
        }
        #pragma omp section
        {
            // Block B — e.g. fill array y
            for (int i = 0; i < N; i++) y[i] = g(i);
        }
    }
}
```

- Each `section` runs on **one thread**.
- The loops **inside** sections are not parallelised — values appear in correct order.
- Variables declared inside a section are private to it.
- Implicit barrier at the end of `sections` (suppress with `nowait`).

### 9.2 `single`

In a parallel region, code not inside a work-sharing construct is **executed by every thread**. Often you want exactly one thread to do something (printf, I/O, generate tasks):

```c
#pragma omp parallel
{
    // every thread does this
    do_local_setup();

    #pragma omp single
    {
        printf("Only one thread prints this.\n");
        // (No guarantee which thread)
    }
    // implicit barrier here — every thread waits

    do_parallel_work();
}
```

- Exactly one thread runs the block; **which** thread is unspecified.
- Implicit barrier at the end (use `nowait` to skip it).
- Used in the previous week's Mandelbrot program **and** as the standard pattern to wrap a task generator.

---

## 10. OpenMP Tasks (OpenMP 3.0+)

### 10.1 When you need tasks

Loops and sections cover regular parallelism. Tasks are needed when work is **irregular**:

- Recursive algorithms (quicksort, tree traversal)
- Linked list traversal (length unknown statically)
- While loops with data-dependent termination
- Heterogeneous workloads where each piece is different

### 10.2 The pattern: one generator, many executors

```c
#pragma omp parallel
{
    #pragma omp single
    {
        // ONE thread generates tasks
        while (node != NULL) {
            #pragma omp task firstprivate(node)
            {
                process(node);
            }
            node = node->next;
        }
    }
    // implicit barrier after single — all tasks complete before exit
}
```

How threads cooperate:

1. The parallel region forks a team of threads.
2. `single` ensures **only one thread** runs the generation loop.
3. Each `#pragma omp task` packages a unit of work and pushes it onto an internal queue.
4. The other threads in the team pull tasks from the queue and execute them.
5. After the generating thread finishes generating, it joins the others in executing tasks.
6. The barrier at the end of `single` (or `parallel`) waits for all queued tasks to complete.

### 10.3 The `firstprivate` clause — essential for tasks

Tasks are executed **asynchronously** — the value of a loop variable might change between when the task is created and when it actually runs. `firstprivate(x)`:

> Declares one or more list items private to a task, and **initialises each of them with the value the original item has at the moment the construct is encountered**.

So for an outer iterator `i`:

```c
for (int i = 0; i <= N; i++) {
    #pragma omp task firstprivate(i)
    {
        // 'i' here is the snapshot taken at task creation
        compute_column(i);
    }
}
```

Without `firstprivate(i)`, by the time the task runs, the generator may have advanced `i` past the value the task intended.

### 10.4 Granularity

> "Make sure there are more tasks than threads."

If `numTasks ≈ numThreads`, dynamic balancing is no better than static — each thread gets one task and uneven work creates idle time. With many smaller tasks, the runtime keeps queues balanced. Trade-off: too small → scheduling overhead dominates.

---

## 11. Mandelbrot — OpenMP Versions

The Mandelbrot grid has the same outer loop over `i`. We can parallelise it with **three different OpenMP constructs**, depending on what the lecture demonstrates.

### 11.1 With `parallel for` and `schedule(dynamic)` (baseline)

Standard data-parallel approach:

```c
#pragma omp parallel for schedule(dynamic) default(none) \
        shared(z_Re, z_Im, nIter, N, maxIter)
for (int i = 0; i <= N; i++) {
    for (int j = 0; j <= N; j++) {
        double zr = 0, zi = 0;
        double cr = z_Re[i], ci = z_Im[j];
        int k;
        for (k = 0; k < maxIter; k++) {
            double zr2 = zr*zr - zi*zi + cr;
            double zi2 = 2*zr*zi + ci;
            zr = zr2; zi = zi2;
            if (zr*zr + zi*zi > 4.0) break;
        }
        nIter[i][j] = k;
    }
}
```

`schedule(dynamic)` is the OpenMP analogue of MPI manager-worker — threads grab chunks at runtime.

### 11.2 With `sections` (only if columns split into two halves)

Less common for Mandelbrot — sections is appropriate when you have **fixed, independent blocks**, not many similar tasks. You could split the grid into top half / bottom half:

```c
#pragma omp parallel
{
    #pragma omp sections
    {
        #pragma omp section
        {
            for (int i = 0; i <= N/2; i++) compute_column(i);
        }
        #pragma omp section
        {
            for (int i = N/2+1; i <= N; i++) compute_column(i);
        }
    }
}
```

This is a poor fit for load balancing if work per column varies — it's only listed for completeness.

### 11.3 With tasks (lecture example)

This is the construct shown explicitly in the lecture slides for Mandelbrot.

```c
#pragma omp parallel
{
    #pragma omp single
    {
        // Only one thread generates the tasks
        for (int i = 0; i <= N; i++) {

            // firstprivate(i) — snapshot the current value of i
            // before the task is queued
            #pragma omp task firstprivate(i) \
                            shared(z_Re, z_Im, nIter, maxIter, N)
            {
                for (int j = 0; j <= N; j++) {
                    double zr = 0, zi = 0;
                    double cr = z_Re[i], ci = z_Im[j];
                    int k;
                    for (k = 0; k < maxIter; k++) {
                        double zr2 = zr*zr - zi*zi + cr;
                        double zi2 = 2*zr*zi + ci;
                        zr = zr2; zi = zi2;
                        if (zr*zr + zi*zi > 4.0) break;
                    }
                    nIter[i][j] = k;
                }
            } // end task

        } // end for
    } // end single — implicit barrier until tasks done
}
```

Key points (and lecture-highlighted gotchas):

- `single` ensures one thread generates tasks; the others execute.
- `firstprivate(i)`: each task captures its own `i`. **Without this, every task would see the final value of `i` after the loop exits.**
- Tasks can run in any order — that's fine because each task writes into a distinct column `nIter[i][:]`.
- `N+1` tasks ≫ thread count → good dynamic balancing.

---

## 12. MPI Manager-Worker vs OpenMP Tasks — Side-by-Side

| Aspect | MPI Manager-Worker | OpenMP Tasks |
|---|---|---|
| Scope | Distributed memory (across nodes) | Shared memory (single node) |
| Work distributor | Dedicated manager process | A single thread inside `omp single` |
| Worker pool | All other ranks | All other threads in the team (and the generator after it finishes) |
| Work request | Explicit `MPI_Send` from worker | Implicit — threads pull from runtime queue |
| Synchronisation | Explicit message-passing | Implicit at end of `single` / `parallel` |
| Termination | Manager sends `DIE_TAG` | Generator exits the `single` block |
| Equivalent in loops | `schedule(dynamic)` for OpenMP loops | `parallel for schedule(dynamic)` |
| Cost of one work unit | Round-trip MPI message → must be coarse | Queue push/pop → can be much finer |
| Data sharing | None (copy via messages) | Free (shared memory) |
| Aggregation | `MPI_Reduce` on a workers-only communicator | Just write into shared array, or `reduction` clause |

---

## 13. Mandelbrot — MPI vs OpenMP Tasks Side-by-Side

| Element | MPI Manager-Worker | OpenMP Tasks |
|---|---|---|
| Outer loop owner | Manager (rank 0) | One thread under `omp single` |
| Work unit | Column index `i` | Column index `i`, captured via `firstprivate(i)` |
| Dispatch | `MPI_Send(i)` to requesting worker | `#pragma omp task` enqueues task |
| Termination | `DIE_TAG` flag message | End of generator loop + implicit barrier |
| Result storage | Each worker fills its `nIter[i][:]` rows | All tasks share `nIter` — distinct columns, no race |
| Aggregation | `MPI_Reduce` on workers-only comm into root's `nIter` | Already in shared memory — nothing to do |
| Idle process? | Yes — manager performs no compute | No — generator joins task pool after the loop |

---

## 14. Exam Checklist — Things to Be Able to Recite

### Concepts
- Difference between **data parallel** (loops, domain decomposition) and **task parallel** (manager-worker, OpenMP tasks).
- Why manager-worker scales better than static domain decomposition for irregular workloads → load balancing at runtime.
- Granularity trade-off: too fine → comms/scheduling overhead dominates; too coarse → poor balance.
- The Mandelbrot set as the **canonical example** of irregular per-unit work.

### MPI features
- Function signature of `MPI_Recv`, including `MPI_Status`.
- `MPI_ANY_SOURCE`, `MPI_ANY_TAG`, retrieving sender via `status.MPI_SOURCE`.
- 6-step recipe for creating a new communicator (group → group → comm → rank → work → free).
- Group construction: `MPI_Group_incl`, `MPI_Group_excl`, `MPI_Group_union`, `MPI_Group_intersection`, `MPI_Group_difference`.
- Why `MPI_Comm_create` is collective on the parent communicator (every rank must call it).
- Non-member ranks receive `MPI_COMM_NULL`.

### OpenMP features
- The three work-sharing constructs before 3.0: `for`, `sections`, `single`.
- Implicit barriers: end of `parallel`, `for`, `sections`, `single`; suppress with `nowait` (except `parallel`).
- Tasks were added in OpenMP **3.0**.
- Standard task pattern: `parallel` → `single` → `task` inside generator loop.
- `firstprivate(x)`: private copy of `x` initialised at the moment the task is created — required so each task gets the right loop-variable snapshot.
- "More tasks than threads" rule for good load balancing.

### Code patterns
- Be able to sketch a manager-worker MPI program with `WORK_TAG`/`DIE_TAG`.
- Be able to write the workers-only communicator boilerplate from memory.
- Be able to convert a `for` loop into an OpenMP task-generation loop with `firstprivate`.
- Be able to identify when `sections` is appropriate (independent, heterogeneous blocks) vs `task` (irregular or recursive) vs `for` (regular loop with known trip count).

---

## 15. Common Pitfalls (Exam Bait)

| Pitfall | Why it's wrong | Fix |
|---|---|---|
| Calling `MPI_Reduce` on `MPI_COMM_WORLD` when manager has no data | Manager must participate but has nothing to contribute → undefined or wasted work | Build workers-only communicator |
| `MPI_Comm_create` called only by group members | Function is collective on **parent** comm — would deadlock | All ranks of parent call it; non-members get `MPI_COMM_NULL` |
| Forgetting `firstprivate(i)` in a task generator | `i` is shared by default — every task ends up using the post-loop value | Add `firstprivate(i)` (and other captured iterators) |
| Putting `#pragma omp task` outside an `omp single` | All threads generate the same tasks → duplicated work | Wrap generator in `single` |
| `MPI_ANY_SOURCE` without inspecting `status.MPI_SOURCE` | Manager can't tell which worker to reply to | Read `status.MPI_SOURCE`, send the reply there |
| Forgetting `MPI_Comm_free` / `MPI_Group_free` | Resource leak; some MPI implementations error | Free both at the end |
| Treating manager-worker as automatically faster | If work units are tiny and uniform, manager round-trips cost more than they save | Compare against `schedule(static)` for uniform work |
| Using `sections` for highly variable per-block work | Sections cannot rebalance | Use tasks instead |

---

## 16. Related Wiki Pages

- [Manager-Worker Model](../concepts/Manager_Worker_Model.md)
- [OpenMP Tasks](../concepts/OpenMP_Tasks.md)
- [OpenMP Advanced Work Sharing](../concepts/OpenMP_Advanced_Work_Sharing.md)
- [MPI Advanced Features (Wildcards & Communicators)](../concepts/MPI_Advanced_Features.md)
- [MPI Point-to-Point Communication](../concepts/MPI_Point_to_Point_Communication.md)
- [MPI Collective Communication](../concepts/MPI_Collective_Communication.md)
- [Load Balancing and Scheduling](../concepts/Load_Balancing_and_Scheduling.md)
- [OpenMP Complete Reference](OpenMP_Complete_Reference.md)
- [Week 8 Summary](../summaries/Week_8_Summary.md)
