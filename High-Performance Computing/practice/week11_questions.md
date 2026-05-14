---
title: "Week 11 Practice Questions: Hybrid Parallelism (MPI + OpenMP)"
tags: [hpc, week-11, mpi, openmp, hybrid, practice]
date: 2026-05-14
---

# Week 11 Practice Questions: Hybrid Parallelism (MPI + OpenMP)

> These questions cover hybrid MPI+OpenMP parallelism as synthesised in the Week 11 module review. All questions include model answers with key marking points. Topics: motivation for hybrid parallelism, MPI thread safety levels, process/thread binding, NUMA interaction, flat vs hierarchical decomposition, performance analysis, and code writing.

---

## Section A: Short Answer

---

### Q1. Define hybrid parallelism in the context of HPC clusters. [3 marks]

**Model Answer:**

- Hybrid parallelism combines two complementary parallel programming models to match the two-level hierarchy of a modern HPC cluster. **(1 mark)**
- **MPI** handles coarse-grained, inter-node parallelism across distributed-memory compute nodes connected by an interconnect. **(1 mark)**
- **OpenMP** handles fine-grained, intra-node parallelism across the shared-memory CPU cores within each node. **(1 mark)**

---

### Q2. List and briefly describe the four MPI thread safety levels, in increasing order of thread support. [4 marks]

**Model Answer:**

| Level | Constant | Meaning |
|---|---|---|
| 1 | `MPI_THREAD_SINGLE` | Only one thread will execute — no thread support required. |
| 2 | `MPI_THREAD_FUNNELED` | Multiple threads exist but **only the main (master) thread** makes MPI calls. |
| 3 | `MPI_THREAD_SERIALIZED` | Multiple threads may make MPI calls but **not simultaneously** — calls are serialized by the application. |
| 4 | `MPI_THREAD_MULTIPLE` | **Any thread** may call MPI at any time with no restrictions. |

Award 1 mark per correct level with correct description. Accept any reasonable wording.

---

### Q3. What function replaces `MPI_Init` in a hybrid MPI+OpenMP program, and what are its two key parameters beyond `argc` and `argv`? [3 marks]

**Model Answer:**

- The function is `MPI_Init_thread(int *argc, char ***argv, int required, int *provided)`. **(1 mark)**
- `required` — the thread safety level the application needs (e.g., `MPI_THREAD_FUNNELED`). **(1 mark)**
- `provided` — output parameter: the actual thread safety level the MPI library is willing to guarantee. The application must check that `provided >= required` before proceeding. **(1 mark)**

---

### Q4. Why is `MPI_THREAD_FUNNELED` often sufficient for a typical hybrid program where MPI communication is performed outside OpenMP parallel regions? [2 marks]

**Model Answer:**

- In the most common hybrid pattern, OpenMP parallel regions handle computation (loop iterations) and MPI calls are made only by the master thread, **before or after** the OpenMP `#pragma omp parallel` region. **(1 mark)**
- Since only the master thread ever makes MPI calls, the weaker (and more efficiently implemented) `MPI_THREAD_FUNNELED` level is sufficient; there is no risk of concurrent MPI calls from multiple threads. **(1 mark)**

---

### Q5. What is process binding (affinity) and why is it important in a hybrid MPI+OpenMP program? [3 marks]

**Model Answer:**

- Process binding (or affinity) controls which physical CPU cores an MPI process and its OpenMP threads are permitted to run on. **(1 mark)**
- Without binding, the OS scheduler may migrate processes or threads between cores or sockets, causing **remote NUMA memory accesses** and cache thrashing, degrading performance. **(1 mark)**
- Binding each MPI process to a specific socket and pinning its OpenMP threads to the cores of that socket ensures **cache locality, NUMA locality**, and prevents threads from migrating across sockets. **(1 mark)**

---

### Q6. Explain what "oversubscription" means in the context of pure MPI parallelism, and how hybrid MPI+OpenMP avoids it. [3 marks]

**Model Answer:**

- Oversubscription occurs when more MPI processes are launched than there are physical CPU cores, so multiple processes must time-share a core, increasing context-switch overhead and degrading performance. **(1 mark)**
- In pure MPI, one common approach is to use one process per physical core, which maximises utilisation but incurs large per-process memory overheads (each process has its own independent address space, halo buffers, etc.). **(1 mark)**
- Hybrid parallelism avoids this by launching fewer MPI processes (e.g., one per socket) and using OpenMP threads — which share the process's memory — to saturate the remaining cores within the socket. Threads share data, so halos and shared arrays are not duplicated per core. **(1 mark)**

---

### Q7. State two reasons why hybrid MPI+OpenMP can reduce total network communication compared with pure MPI using one process per core. [2 marks]

**Model Answer (any two):**

- **Fewer MPI messages**: With fewer MPI processes per node, there are fewer halo exchange pairs, so fewer distinct messages are sent across the interconnect.
- **Larger, more efficient messages**: Each remaining message carries more data per send/receive, making better use of interconnect bandwidth (amortising latency over more data).
- **Intra-node communication eliminated**: Cores that previously communicated via MPI shared-memory buffers (still incurring MPI protocol overhead) now communicate via ordinary shared-memory loads/stores under OpenMP at essentially cache speed.

Award 1 mark each for any two distinct, correct reasons.

---

### Q8. What is the `OMP_PROC_BIND` environment variable (or `proc_bind` clause), and what values can it take? Give one concrete use case. [3 marks]

**Model Answer:**

- `OMP_PROC_BIND` (or the `proc_bind(policy)` clause on `#pragma omp parallel`) controls how OpenMP threads are bound to hardware resources. **(1 mark)**
- Common values: `close` (bind threads to hardware units close together, e.g., hyperthreads or adjacent cores); `spread` (spread threads as far apart as possible across sockets/NUMa domains); `master` (bind all threads to the same hardware as the master thread). **(1 mark)**
- Use case: in a hybrid program with one MPI process per socket, `proc_bind(close)` confines all OpenMP threads to the cores of that socket, preventing inter-socket migration and preserving NUMA locality. **(1 mark)**

---

## Section B: Code Analysis

---

### Q9. Examine the following hybrid MPI+OpenMP code fragment. [6 marks]

```c
#include <mpi.h>
#include <omp.h>
#include <stdio.h>

int main(int argc, char **argv) {
    int rank, size;
    MPI_Init(&argc, &argv);                    // (A)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double result = 0.0;

    #pragma omp parallel for reduction(+:result)
    for (int i = 0; i < 1000; i++) {
        result += compute(i, rank);
    }

    double global_result;
    MPI_Reduce(&result, &global_result, 1, MPI_DOUBLE,  // (B)
               MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0)
        printf("Global result: %f\n", global_result);

    MPI_Finalize();
    return 0;
}
```

**(a)** Identify the error at line (A). What should replace it, and why? [2 marks]

**(b)** Describe the two levels of parallelism this code exploits and how they interact. [2 marks]

**(c)** Is the `MPI_Reduce` at (B) thread-safe? Explain your reasoning. [2 marks]

**Model Answers:**

**(a)** `MPI_Init` does not initialise the MPI environment with thread support. Since the code uses OpenMP, it must call `MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided)` instead and verify `provided >= MPI_THREAD_FUNNELED`. Without this, the behaviour of MPI in a multithreaded environment is undefined. **(2 marks: 1 for naming `MPI_Init_thread` with correct level; 1 for the check on `provided`.)**

**(b)** MPI distributes the computation across `size` nodes/processes; each process independently computes its local `result` over all 1000 iterations (though ideally the loop range would be partitioned per rank). Within each process, OpenMP parallelises the 1000-iteration loop across available cores, using a `reduction(+:result)` to safely accumulate partial sums from each thread into the local `result`. The `MPI_Reduce` then combines each process's local result into a global sum. **(2 marks: 1 for each level of parallelism clearly described.)**

**(c)** Yes, it is thread-safe as written. The `MPI_Reduce` call appears **after** the closing brace of the `#pragma omp parallel for` region, which includes an implicit barrier. By the time `MPI_Reduce` is called, all threads have joined back to the single master thread, so only one thread makes the MPI call — satisfying `MPI_THREAD_FUNNELED`. **(2 marks: 1 for stating it is safe; 1 for the implicit-barrier / single-thread reasoning.)**

---

### Q10. Consider the following code intended for a hybrid program. Identify **two** bugs or performance problems and explain how to fix each. [4 marks]

```c
// Run with: mpirun -np 8 ./prog   (8 MPI processes, each with 4 OMP threads)
// Node has 2 sockets × 4 cores = 8 cores total

int main(int argc, char **argv) {
    int provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &provided);

    double *data = malloc(N * sizeof(double));

    // Master thread initialises all data
    for (int i = 0; i < N; i++) data[i] = 0.0;

    #pragma omp parallel for num_threads(4)
    for (int i = 0; i < N; i++) {
        data[i] = heavy_compute(i);
    }
    ...
}
```

**Model Answer:**

**Bug 1 — Oversubscription (1 mark for identification + 1 mark for fix):**
With 8 MPI processes per node and 4 OpenMP threads each, the program launches 32 threads on a node with only 8 physical cores. This is severe oversubscription; cores must time-share 4 threads each, causing scheduler overhead, cache thrashing, and degraded performance. Fix: use 1 or 2 MPI processes per node (e.g., one per socket) and 4 threads per process, so total threads = 8, matching the core count.

**Bug 2 — Sequential initialization causing NUMA penalty (1 mark for identification + 1 mark for fix):**
The master thread (running on one socket) initialises the entire `data` array sequentially before the parallel region. Under Linux's first-touch policy, all pages of `data` are allocated on the master thread's socket. When OpenMP threads on the other socket access `data[i]` during the parallel loop, they incur remote NUMA memory accesses. Fix: replace the sequential initialisation loop with a parallel one:
```c
#pragma omp parallel for num_threads(4)
for (int i = 0; i < N; i++) data[i] = 0.0;
```
This way each thread touches its own portion first, and pages are distributed across both sockets.

---

### Q11. The following code launches one MPI process per node and uses OpenMP for all on-node parallelism. A colleague suggests that using `MPI_THREAD_SERIALIZED` rather than `MPI_THREAD_FUNNELED` would improve performance because "more threads can communicate." Is this correct? Justify your answer. [3 marks]

```c
MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

#pragma omp parallel
{
    // computation
}
// Only master thread ever calls MPI
MPI_Allreduce(...);
```

**Model Answer:**

The colleague is incorrect. **(1 mark)**

`MPI_THREAD_SERIALIZED` permits multiple threads to make MPI calls, but requires the application to ensure they do not call MPI **simultaneously** — calls must be serialized by the user (e.g., with a mutex). It does not allow truly concurrent MPI calls from multiple threads, and it typically incurs higher library overhead than `MPI_THREAD_FUNNELED`. **(1 mark)**

In this specific program, the MPI call (`MPI_Allreduce`) is placed outside the parallel region, after the implicit barrier, so only the master thread ever calls MPI. `MPI_THREAD_FUNNELED` is precisely the correct and most efficient level here. Requesting a higher level than needed may impose unnecessary internal synchronisation overhead inside the MPI library. **(1 mark)**

---

## Section C: Code Writing

---

### Q12. Write a complete, correct hybrid MPI+OpenMP C program that: initialises MPI with thread support; has each MPI process compute a partial sum of a 1000-element array using OpenMP; and reduces the partial sums to rank 0, which prints the global total. [8 marks]

**Model Answer:**

```c
#include <mpi.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int rank, size, provided;

    // (1) Initialise MPI with thread support
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
    if (provided < MPI_THREAD_FUNNELED) {
        fprintf(stderr, "MPI thread support insufficient\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int N = 1000;
    // (2) Partition work across MPI ranks
    int chunk = N / size;
    int start = rank * chunk;
    int end   = (rank == size - 1) ? N : start + chunk;

    // (3) Each MPI process allocates its local portion
    double local_sum = 0.0;

    // (4) OpenMP parallelises the local loop
    #pragma omp parallel for reduction(+:local_sum)
    for (int i = start; i < end; i++) {
        local_sum += (double)i;   // replace with actual computation
    }

    // (5) MPI reduction — called by master thread only (outside parallel region)
    double global_sum = 0.0;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE,
               MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Global sum = %.1f\n", global_sum);
    }

    MPI_Finalize();
    return 0;
}
```

**Marking scheme (8 marks):**
- `MPI_Init_thread` with correct level and check on `provided` — **2 marks**
- Correct domain partitioning across MPI ranks (start/end or equivalent) — **1 mark**
- `#pragma omp parallel for reduction(+:local_sum)` with correct variable — **2 marks**
- `MPI_Reduce` called outside parallel region (thread-safe placement) with correct arguments — **2 marks**
- `MPI_Finalize` and correct conditional print on rank 0 — **1 mark**

---

### Q13. Write the launch command (using `mpirun` or `srun`) and the environment variable settings needed to run a hybrid program on a cluster where each node has 2 sockets × 8 cores = 16 cores total. Use 1 MPI rank per socket, 8 OpenMP threads per rank, across 4 nodes. [3 marks]

**Model Answer:**

```bash
export OMP_NUM_THREADS=8
export OMP_PROC_BIND=close

mpirun -np 8 --map-by socket --bind-to socket ./hybrid_prog
```

Or equivalently with SLURM:
```bash
export OMP_NUM_THREADS=8
srun --nodes=4 --ntasks=8 --ntasks-per-socket=1 --cpus-per-task=8 \
     --cpu-bind=sockets ./hybrid_prog
```

**Marking scheme:**
- Total MPI ranks = 4 nodes × 2 sockets = 8; `OMP_NUM_THREADS=8` — **1 mark**
- Binding strategy maps one rank per socket (`--map-by socket` / `--ntasks-per-socket=1`) — **1 mark**
- `OMP_PROC_BIND=close` (or `spread`) to confine threads to their socket — **1 mark**

---

### Q14. Write a short code fragment that uses `MPI_Comm_split` to create a communicator containing only the MPI processes that share the same compute node (an "intra-node communicator"). Assume each node runs 4 MPI processes. [4 marks]

**Model Answer:**

```c
int world_rank, node_rank, node_id;
MPI_Comm node_comm;

MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

// Assign a "color" — processes on the same node share the same color.
// With 4 ranks per node: node 0 has ranks 0-3, node 1 has ranks 4-7, etc.
node_id = world_rank / 4;

MPI_Comm_split(MPI_COMM_WORLD, node_id, world_rank, &node_comm);

MPI_Comm_rank(node_comm, &node_rank);
// node_rank is now 0..3 within this node's communicator

// Use node_comm for intra-node MPI collectives if needed,
// MPI_COMM_WORLD (or an inter-node communicator) for cross-node operations.

// Clean up
MPI_Comm_free(&node_comm);
```

**Marking scheme:**
- Correct computation of `color` (grouping co-located ranks) — **1 mark**
- Correct `MPI_Comm_split` call with `(comm, color, key, &newcomm)` — **2 marks**
- `MPI_Comm_free` to release the communicator — **1 mark**

---

### Q15. Write an OpenMP parallel loop that correctly initialises a double-precision array `A[N]` in a NUMA-aware fashion inside an MPI process, so that each thread touches its own portion of memory first. [3 marks]

**Model Answer:**

```c
double *A = malloc(N * sizeof(double));

// NUMA-aware first-touch: each thread initialises its own portion.
// Pages are then allocated on the socket local to each thread.
#pragma omp parallel for schedule(static)
for (int i = 0; i < N; i++) {
    A[i] = 0.0;
}
```

**Marking scheme:**
- Use of `#pragma omp parallel for` (not a sequential loop) — **1 mark**
- `schedule(static)` to ensure the same thread that initialises a portion will also compute it (matching the subsequent computation loop's distribution) — **1 mark**
- Explanation that this causes pages to be placed on the socket of the touching thread, avoiding remote accesses — **1 mark**

---

## Section D: Performance Analysis and Design

---

### Q16. A cluster node has 2 sockets, each with 12 cores (24 cores total, no hyperthreading). You are running a domain-decomposed application. Evaluate the following three deployment strategies in terms of memory footprint, NUMA behaviour, and MPI message overhead: [9 marks]

- **(a) Pure MPI: 24 ranks per node, 1 rank per core**
- **(b) Hybrid: 2 ranks per node, 1 rank per socket, 12 threads per rank**
- **(c) Hybrid: 4 ranks per node, 2 ranks per socket, 6 threads per rank**

**Model Answer:**

**(a) Pure MPI — 24 ranks/node:**
- **Memory**: Each rank maintains its own address space, halo buffers, and duplicated variables. Total memory overhead is 24× the per-process overhead. This is the worst memory footprint. **(1 mark)**
- **NUMA**: Each rank's memory is allocated on whichever socket it is pinned to, so NUMA locality is good if ranks are pinned. However, 12 independent processes per socket compete for the socket's memory bandwidth. **(1 mark)**
- **MPI messages**: The most inter-rank messages per node — 24 ranks may communicate with 24 neighbours across nodes, saturating the interconnect. Intra-node MPI (between the two sockets' ranks) uses shared memory but still incurs MPI protocol overhead. **(1 mark)**

**(b) Hybrid — 2 ranks/node, 1/socket:**
- **Memory**: Only 2 address spaces per node. Halos are shared within each socket via OpenMP threads — minimum memory footprint. **(1 mark)**
- **NUMA**: Ideal. Each MPI process is pinned to one socket; its 12 OpenMP threads only access memory local to that socket. No inter-socket NUMA traffic if arrays are initialised with a parallel first-touch loop. **(1 mark)**
- **MPI messages**: Only 2 ranks per node participate in inter-node communication. Fewest messages, largest message size — most bandwidth-efficient. **(1 mark)**

**(c) Hybrid — 4 ranks/node, 2/socket:**
- **Memory**: 4 address spaces per node — intermediate footprint. Each socket runs 2 MPI processes, so halos are only shared among 6 threads (not 12). **(1 mark)**
- **NUMA**: If each rank is bound to the correct half of a socket, NUMA is acceptable. However, each rank's 6 threads share a socket with another rank's 6 threads — potential memory bandwidth contention within the socket. **(1 mark)**
- **MPI messages**: Intermediate — 4 ranks communicate across nodes. More messages than (b) but fewer than (a). May be useful if the computation has a load imbalance that benefits from finer MPI grain. **(1 mark)**

**Summary recommendation**: Strategy (b) is optimal for memory and NUMA; strategy (c) is a pragmatic compromise if load balance is uneven.

---

### Q17. You are running a pure MPI code on 4 nodes, each with 16 cores. Strong scaling shows good efficiency up to 4 nodes (64 processes) but degrades rapidly beyond that. A colleague proposes switching to hybrid with 4 MPI processes per node (1 per socket, nodes have 4 sockets × 4 cores) and 4 OpenMP threads per process. [4 marks]

**(a)** Explain why scaling degraded in the pure MPI case. **(2 marks)**

**(b)** Explain how the hybrid approach may recover scaling beyond 64 processes. **(2 marks)**

**Model Answer:**

**(a)** In a domain-decomposed application, as the number of MPI processes grows, each process's subdomain shrinks. The ratio of halo (boundary) points to interior points increases, so the fraction of time spent on MPI communication (halo exchange) grows relative to computation. Beyond a threshold, the communication overhead dominates and Amdahl's Law limits speedup. Additionally, with 64+ MPI processes, the interconnect carries many more small messages, increasing latency-bound overhead. **(2 marks)**

**(b)** By reducing the MPI process count to 4 per node (16 total across 4 nodes, compared to 64), each MPI subdomain is 4× larger, reducing the halo-to-interior ratio and the total number of inter-node messages. The intra-node parallelism (the 4 OpenMP threads per process) now handles what previously required 4 MPI processes, but via shared-memory access — orders of magnitude lower latency than network communication. As a result, the application can continue to scale (by adding more nodes) without the communication bottleneck that choked the pure MPI approach. **(2 marks)**

---

### Q18. A two-socket node runs a hybrid program with 1 MPI process per socket and 8 OpenMP threads per process. The programmer initialises a shared array sequentially in the master thread of MPI process 0, then distributes a portion of it to process 1 via `MPI_Send`. Describe the performance implications and suggest a better initialisation strategy. [4 marks]

**Model Answer:**

**Performance implications:**
- The master thread of process 0 (running on socket 0) initialises the entire array sequentially. Under the first-touch policy, all memory pages land on socket 0's local DRAM. **(1 mark)**
- Process 0's OpenMP threads on socket 0 access local memory — no penalty. **(0.5 mark)**
- The portion sent to process 1 (socket 1) via `MPI_Send` is received into process 1's buffer. If process 1's buffer was not first-touched by its own threads (e.g., also initialised sequentially on socket 0 or by a single thread), process 1's 8 OpenMP threads will access memory physically located on socket 0 — incurring remote NUMA latency for every memory access, potentially halving memory bandwidth. **(1 mark)**

**Better strategy:**
- Each MPI process should initialise and first-touch its own data independently, using a parallel OpenMP loop:
```c
#pragma omp parallel for schedule(static)
for (int i = 0; i < local_N; i++) local_array[i] = initial_value;
```
This ensures memory pages are placed on the socket running that process, so all subsequent OpenMP accesses are local. The MPI communication should send only the boundary data (halos), not the full array — each process owns and initialises its own domain. **(1.5 marks: 1 for parallel init, 0.5 for keeping data local to each process.)**

---

## Section E: Multi-Part Exam Questions

---

### Q19. [12 marks total]

A parallel application solves a 2D heat diffusion equation on a 1000×1000 grid using finite differences. It is currently implemented as pure MPI with one process per core. The cluster has nodes with 2 sockets × 8 cores (16 cores/node), connected by a low-latency interconnect.

**(a)** Describe how domain decomposition is applied in the pure MPI version. What communication pattern is required between neighbouring processes? [3 marks]

**(b)** The developer observes that strong scaling efficiency drops below 50% when using more than 64 cores (4 nodes). Using the concept of halo overhead, explain why this is expected. [3 marks]

**(c)** Propose a hybrid MPI+OpenMP redesign. Specify the number of MPI processes per node and threads per process, and justify your choice with respect to NUMA topology. [3 marks]

**(d)** In the hybrid design, where should the MPI halo exchange calls be placed relative to the OpenMP parallel region? Write a pseudocode skeleton to illustrate. [3 marks]

---

**Model Answers:**

**(a) Domain decomposition and halo exchange:**

The 2D grid is partitioned into subdomains, each owned by one MPI process. For a 1D decomposition, each process owns a horizontal strip of rows; for a 2D decomposition, each owns a rectangular tile. Each process stores extra rows/columns called **halos** that cache the boundary values from neighbouring processes. After each time step, processes exchange halo rows with their north/south (and east/west in 2D) neighbours using `MPI_Sendrecv` or non-blocking `MPI_Isend`/`MPI_Irecv` pairs, before computing the next step. **(3 marks: 1 subdomain + ownership; 1 halo definition; 1 exchange mechanism.)**

**(b) Scaling degradation and halo overhead:**

With a 1000×1000 grid divided across P processes, each subdomain has approximately `1000/sqrt(P)` points per dimension. The number of interior points scales as `~(1000/sqrt(P))^2 = 1,000,000/P`. The halo boundary length scales as `~4 × 1000/sqrt(P)`. The ratio of communication to computation (halo points / interior points) scales as `~4*sqrt(P)/1000`, growing as sqrt(P). At 64 processes, this ratio is `4*8/1000 = 3.2%`; at 256 processes it becomes `~6.4%`, and the communication time grows faster than the computation time shrinks. Additionally, 64+ processes generate more simultaneous messages competing for interconnect bandwidth, increasing queuing latency. Amdahl's Law applied to this communication overhead limits achievable speedup. **(3 marks: 1 for halo ratio grows with P; 1 for quantitative/qualitative reasoning; 1 for connection to Amdahl/overhead.)**

**(c) Hybrid redesign:**

Use **2 MPI processes per node, one per socket**, and **8 OpenMP threads per process**. Rationale:
- Each socket has 8 cores; 8 threads exactly saturates the socket without oversubscription.
- One MPI process per socket ensures its entire address space is allocated on that socket's NUMA domain. OpenMP threads are pinned (`OMP_PROC_BIND=close`) to cores on the same socket, guaranteeing all memory accesses are local.
- Only 2 MPI ranks per node participate in halo exchanges (vs. 16 previously), reducing the number of inter-node messages by 8×, and each message is larger (less latency overhead per byte).
- Set `OMP_NUM_THREADS=8` and use `MPI_Init_thread` with at least `MPI_THREAD_FUNNELED`. **(3 marks: 1 for correct rank/thread count; 1 for NUMA justification; 1 for communication reduction.)**

**(d) Placement of MPI calls — pseudocode skeleton:**

```c
// Time-stepping loop
for (int t = 0; t < T; t++) {

    // Step 1: MPI halo exchange — called by master thread ONLY,
    //         OUTSIDE the OpenMP parallel region
    MPI_Sendrecv(/* send top halo row to north neighbour, */
                 /* receive bottom halo from north neighbour */);
    MPI_Sendrecv(/* send bottom halo row to south neighbour, */
                 /* receive top halo from south neighbour */);

    // Step 2: OpenMP parallelises the stencil computation
    //         over the interior points of this rank's subdomain
    #pragma omp parallel for collapse(2) schedule(static)
    for (int i = 1; i < local_rows - 1; i++) {
        for (int j = 1; j < local_cols - 1; j++) {
            new_grid[i][j] = alpha * (grid[i-1][j] + grid[i+1][j]
                           + grid[i][j-1] + grid[i][j+1]
                           - 4*grid[i][j]);
        }
    }
    // Implicit barrier at end of parallel region — all threads done
    // before next halo exchange
    swap(&grid, &new_grid);
}
```

Key points: MPI calls are outside and before the OpenMP region; the implicit barrier at the end of `#pragma omp parallel for` guarantees all threads have finished before the next halo exchange. **(3 marks: 1 for MPI outside parallel; 1 for correct barrier reasoning; 1 for correct pseudocode structure.)**

---

### Q20. [10 marks total]

**(a)** Compare pure MPI (one process per core) with hybrid MPI+OpenMP (one process per socket) across five dimensions: memory footprint, NUMA behaviour, communication overhead, load balancing ease, and implementation complexity. Present your answer as a structured table. [5 marks]

**(b)** A program has a serial fraction of 5% and a parallel fraction of 95%. Using Amdahl's Law, calculate the maximum theoretical speedup achievable. Then explain why hybrid parallelism may in practice exceed the speedup predicted by Amdahl's Law when communication overhead is included in the model. [3 marks]

**(c)** List three environment variables or runtime parameters a user should set when launching a hybrid MPI+OpenMP job on a SLURM cluster, and explain what each controls. [2 marks]

---

**Model Answers:**

**(a) Comparison table:**

| Dimension | Pure MPI (1 proc/core) | Hybrid (1 proc/socket) |
|---|---|---|
| **Memory footprint** | High — P separate address spaces, P copies of halos and duplicate data | Low — fewer address spaces; threads share data within a process |
| **NUMA behaviour** | Good if each process is pinned to a socket; but many processes per socket compete for memory bandwidth | Excellent — one process owns its socket; threads access only local NUMA memory |
| **Communication overhead** | High — many small MPI messages between all core-level processes, including intra-node | Low — fewer, larger inter-node messages; intra-socket data sharing is via shared memory (no MPI protocol) |
| **Load balancing ease** | Hard — must implement manager-worker in MPI for dynamic load balance | Easier — OpenMP `schedule(dynamic)` handles intra-node imbalance without MPI complexity |
| **Implementation complexity** | Lower (single paradigm, MPI only) | Higher — must manage two parallel models, thread safety levels, and binding |

Award 1 mark per dimension, up to 5, for a correct, well-differentiated comparison.

**(b) Amdahl's Law calculation:**

S_max = 1 / s = 1 / 0.05 = **20×**

The maximum theoretical speedup is **20** regardless of the number of processors. **(1 mark)**

Standard Amdahl's Law models only the serial/parallel split and assumes communication is free. When communication overhead is added (e.g., Amdahl extended: `S_N = 1 / (s + p/N + npv/T_0)`), the denominator grows with N due to message overhead, further reducing speedup. Hybrid parallelism reduces the MPI message count and size (intra-node communication becomes shared-memory), lowering the `npv/T_0` term. In practice, the effective serial fraction — which in pure MPI includes communication waiting time — is smaller in the hybrid model, allowing better-than-Amdahl scaling up to the point where the new communication costs dominate. **(2 marks: 1 for extending Amdahl with overhead term; 1 for how hybrid reduces that overhead term.)**

**(c) Three key environment variables/parameters:**

| Variable / Parameter | What it controls |
|---|---|
| `OMP_NUM_THREADS=N` | Sets the number of OpenMP threads each MPI process forks. Should equal the number of cores per socket (or per rank's allocation). |
| `OMP_PROC_BIND=close` (or `spread`) | Controls thread binding/affinity — `close` keeps threads near each other on the same socket; `spread` distributes them. Essential for NUMA locality. |
| `--cpus-per-task=N` (SLURM) | Allocates N logical CPUs to each MPI task, so each rank has enough cores for its OpenMP threads. Without this, SLURM may not reserve enough cores per task. |

Accept `OMP_PLACES`, `--ntasks-per-socket`, or `--bind-to socket` (mpirun) as alternatives. **(1 mark per variable with correct explanation, max 2 marks.)**

---

### Q21. [8 marks total]

The following question concerns the interaction of NUMA, first-touch, and hybrid parallelism.

**(a)** Explain the first-touch memory allocation policy and why it matters for multi-socket nodes. [2 marks]

**(b)** A programmer initialises a large array sequentially before an OpenMP parallel region and then parallelises the computation. Sketch the memory access pattern and explain the performance consequence. [3 marks]

**(c)** Explain how using one MPI process per socket (rather than one per node) naturally solves the NUMA problem, even without explicit `proc_bind` settings. [3 marks]

---

**Model Answers:**

**(a) First-touch policy:**

Under the first-touch policy, the OS does not physically allocate a memory page when `malloc` is called; instead it maps virtual addresses. The page is physically placed (backed by physical DRAM) on the memory controller of the CPU core that **first writes** to that page. On a multi-socket node, each socket has its own local DRAM. Pages placed on socket 0's DRAM require remote (cross-socket interconnect) access from cores on socket 1, incurring 1.3–2× higher latency and reduced bandwidth. **(2 marks)**

**(b) Sequential init then parallel computation:**

```
Socket 0:   [MASTER THREAD] writes A[0]...A[N-1] → all pages land on socket 0's DRAM
            |
            v
Socket 0 threads:  A[0..N/2-1]  → LOCAL access (fast)
Socket 1 threads:  A[N/2..N-1]  → REMOTE access (slow, crosses interconnect)
```

When the parallel computation loop runs (distributing iterations round-robin or statically), threads on socket 1 must fetch their portion of `A` from socket 0's DRAM across the inter-socket interconnect. This can halve the effective memory bandwidth for those threads, serialising accesses at the interconnect and underutilising socket 1's local DRAM. The result is that half the cores operate at significantly reduced memory throughput, degrading overall parallel performance. **(3 marks: 1 for diagram/description; 1 for penalty mechanism; 1 for quantitative/qualitative impact.)**

**(c) One MPI process per socket — natural NUMA solution:**

When one MPI process is launched per socket (e.g., using `--map-by socket`):
- Each process has its own independent virtual address space.
- When process 0 (on socket 0) allocates and first-touches its array via a parallel `#pragma omp parallel for`, all 8 of its threads are running on socket 0 cores. Pages are first-touched by socket 0 cores → placed on socket 0 DRAM. **(1 mark)**
- When process 1 (on socket 1) does the same, its threads run on socket 1 cores → pages placed on socket 1 DRAM. **(1 mark)**
- The two processes never share memory (separate address spaces), so there is no inter-socket memory traffic at all — NUMA is avoided by construction. The MPI domain boundary data (halos) are exchanged explicitly via `MPI_Send`/`MPI_Recv`, which on the same node typically uses a shared-memory fast path within the MPI library, still avoiding cross-network transfers. **(1 mark)**

---

## Section F: Rapid-Fire Conceptual Questions

*These are suitable for short exam questions worth 1–2 marks each.*

---

### Q22. What is the difference between "flat MPI" and "hierarchical MPI"? [2 marks]

**Answer:** Flat MPI uses one MPI process per core with no threading — a single-level parallelism model. Hierarchical (hybrid) MPI uses one MPI process per node or socket and OpenMP threads within each process — a two-level model that exploits the cluster hierarchy. **(1 mark each.)**

---

### Q23. In a hybrid program, why is it important to call `MPI_Finalize()` only after all OpenMP parallel regions have completed? [1 mark]

**Answer:** `MPI_Finalize` tears down the MPI environment. If called from within or before a parallel region completes, threads may still be executing and could attempt MPI calls after finalization, causing undefined behaviour or program crash.

---

### Q24. Name one scenario where pure MPI is preferable to hybrid MPI+OpenMP, and one scenario where hybrid is preferable. [2 marks]

**Answer:**
- **Pure MPI preferable**: When the application has very coarse-grained independent work units with no shared data per node, or when targeting a distributed-memory cluster with single-core nodes (no shared-memory level exists). Also acceptable: when the team has no OpenMP expertise and the communication overhead is not a bottleneck.
- **Hybrid preferable**: When the per-process memory footprint of pure MPI is too large (e.g., halos dominate memory); when strong scaling has hit a communication bottleneck but more on-node cores are available; when the node has a NUMA topology that penalises many small independent processes.

**(1 mark per valid, well-reasoned scenario.)**

---

### Q25. What does `collapse(2)` achieve in `#pragma omp parallel for collapse(2)`? Why is it useful for 2D stencil computations? [2 marks]

**Answer:** `collapse(2)` merges the iteration space of the two immediately following nested loops into a single, larger iteration space that is then distributed across threads. For a 2D stencil with an outer loop of M and an inner of N, it creates M×N iterations rather than M, giving the scheduler more granularity to distribute work evenly and reducing the likelihood of load imbalance when M is small relative to the number of threads. **(2 marks: 1 for definition; 1 for 2D stencil rationale.)**

---

*End of Week 11 Practice Questions.*

---

**Total questions: 25 (Q1–Q25)**
**Question types covered:**
- Short answer / definition: Q1–Q8, Q22–Q25
- Code analysis: Q9–Q11
- Code writing: Q12–Q15
- Performance analysis and design: Q16–Q18
- Multi-part exam questions: Q19 (12 marks), Q20 (10 marks), Q21 (8 marks)

**Topics covered:** motivation for hybrid parallelism, memory footprint reduction, MPI_THREAD_SINGLE/FUNNELED/SERIALIZED/MULTIPLE, MPI_Init_thread, oversubscription, halo overhead, domain decomposition, NUMA and first-touch policy, proc_bind, OMP_PROC_BIND, MPI_Comm_split, flat vs hierarchical parallelism, thread binding and affinity, Amdahl's Law with overhead, communication patterns, SLURM launch parameters, collapse clause, load balancing, OpenMP scheduling, code correctness and thread safety.
