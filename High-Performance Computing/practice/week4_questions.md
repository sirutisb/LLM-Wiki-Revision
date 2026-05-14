---
title: "Week 4 Practice Questions: Introduction to MPI"
tags: [hpc, week-4, mpi, practice]
date: 2026-05-14
---

# Week 4 Practice Questions: Introduction to MPI

> **Coverage:** MPI programming model (SPMD), initialisation/finalisation, communicators, blocking point-to-point, collective operations, non-blocking communication, deadlock, domain decomposition, halo exchange, 1D vs 2D decomposition, alpha-beta communication model.
>
> **Format key:** Questions are grouped by type. Each question is followed by a collapsible model answer block showing key marking points and, where relevant, correct code.

---

## Section A: Short Answer / Definition

### Q1. MPI Execution Model
What does the acronym **SPMD** stand for, and how does it describe the way an MPI program executes?

**Model Answer (3 marks)**
- SPMD = **Single Program, Multiple Data** (1 mark).
- Every MPI process runs the *same* compiled executable simultaneously (1 mark).
- Each process operates on a *different* subset of the data and uses its rank to decide which work to perform (1 mark).

---

### Q2. MPI Initialisation and Finalisation
State the purpose of `MPI_Init` and `MPI_Finalize`, and describe what happens if a program calls an MPI routine before `MPI_Init` or after `MPI_Finalize`.

**Model Answer (3 marks)**
- `MPI_Init(int *argc, char ***argv)` sets up the MPI execution environment; must be the first MPI call in any program (1 mark).
- `MPI_Finalize()` cleanly tears down the MPI runtime; no MPI calls may follow it (1 mark).
- Calling MPI routines before `MPI_Init` or after `MPI_Finalize` produces undefined/erroneous behaviour — the MPI library has not yet been initialised or has already been shut down (1 mark).

---

### Q3. Communicators, Rank, and Size
(a) What is `MPI_COMM_WORLD`?
(b) Write the exact C function calls to obtain the rank of the calling process and the total number of processes in `MPI_COMM_WORLD`, storing the results in `int rank` and `int size`.

**Model Answer (4 marks)**
(a) `MPI_COMM_WORLD` is the predefined default communicator that encompasses *all* MPI processes launched in a given execution (1 mark).

(b)
```c
MPI_Comm_rank(MPI_COMM_WORLD, &rank);   // 1 mark
MPI_Comm_size(MPI_COMM_WORLD, &size);   // 1 mark
```
Ranks range from `0` to `size - 1` (1 mark).

---

### Q4. MPI Data Types
Why does MPI specify message length as a *count of elements of a given datatype* rather than a *number of bytes*? Give two examples of MPI C datatypes and their C equivalents.

**Model Answer (3 marks)**
- MPI uses element counts + datatypes to be portable across architectures where the same C type may have different byte widths (1 mark).
- Examples (1 mark each, max 2):
  - `MPI_INT` ↔ `int`
  - `MPI_DOUBLE` ↔ `double`
  - `MPI_FLOAT` ↔ `float`
  - `MPI_CHAR` ↔ `char`
  - `MPI_LONG` ↔ `long`

---

### Q5. Blocking vs. Non-blocking
Explain the difference between a *blocking* and a *non-blocking* MPI send. In what situation is non-blocking communication particularly valuable?

**Model Answer (4 marks)**
- A **blocking** send (`MPI_Send`) does not return until the send buffer is safe to reuse — i.e., until the message has been buffered or the receiver has posted a matching `MPI_Recv` (1 mark).
- A **non-blocking** send (`MPI_Isend`) posts the send and returns immediately with an `MPI_Request` handle; the buffer must not be modified until the request is confirmed complete via `MPI_Wait` / `MPI_Waitall` (1 mark).
- Non-blocking communication is valuable for **overlapping computation with communication** — a process can start sending boundary data and then compute on interior cells while the transfer is in progress (1 mark).
- It also simplifies **deadlock avoidance** because neither side needs to block waiting for the other (1 mark).

---

### Q6. Collective Semantics
State one rule that all collective MPI operations must obey. What happens if this rule is violated?

**Model Answer (2 marks)**
- Every process in the communicator must call the collective function — collectives are not point-to-point; they are group operations (1 mark).
- If any process fails to call the collective, the others will block indefinitely, causing a **deadlock** (1 mark).

---

### Q7. MPI_Reduce vs. MPI_Allreduce
Explain the difference between `MPI_Reduce` and `MPI_Allreduce`. Give an example use-case for each.

**Model Answer (4 marks)**
- `MPI_Reduce` performs a global reduction (e.g., sum, max) and delivers the result **only to the root process** (1 mark). Use-case: computing a global error norm at the end of a timestep, only needed by process 0 for output (1 mark).
- `MPI_Allreduce` performs the same reduction but delivers the result **to every process** in the communicator (1 mark). Use-case: computing the minimum global stable timestep in a PDE solver so that all processes can advance by the same `dt` (1 mark).

---

### Q8. Halo Exchange
Define "halo" (ghost region) in the context of domain decomposition. Why must a halo exchange be performed after every timestep in a finite-difference PDE solver?

**Model Answer (4 marks)**
- A **halo** is an extra layer of grid cells stored by each process that holds a copy of the boundary data from its neighbouring sub-domain (1 mark).
- Finite-difference stencils at the edge of a sub-domain require values from the adjacent sub-domain; the halo provides local access to those values without a mid-stencil communication (1 mark).
- After each timestep, boundary values change; without a fresh halo exchange the edge cells of each sub-domain would use stale (outdated) neighbour data, producing an incorrect solution (1 mark).
- The exchange is typically implemented with `MPI_Isend`/`MPI_Irecv` to overlap the transfer with interior computation (1 mark).

---

## Section B: Code Analysis

### Q9. Identify the Output
Study the following MPI program. Assuming it is run with 4 processes (`mpirun -np 4`), describe exactly what output is produced and why.

```c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        printf("Root process: total processes = %d\n", size);
    } else {
        printf("Worker process rank = %d\n", rank);
    }

    MPI_Finalize();
    return 0;
}
```

**Model Answer (4 marks)**
- Four independent processes each execute the program simultaneously (1 mark).
- Process 0 prints: `Root process: total processes = 4` (1 mark).
- Processes 1, 2, 3 each print: `Worker process rank = 1` / `= 2` / `= 3` (1 mark).
- The *order* of the four lines is **non-deterministic** because OS scheduling determines when each process's `printf` executes; all four lines will appear, but interleaved unpredictably (1 mark).

---

### Q10. Trace the Communication
Consider the following code fragment run on exactly 2 processes.

```c
int rank, value;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

if (rank == 0) {
    value = 42;
    MPI_Send(&value, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    MPI_Recv(&value, 1, MPI_INT, 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    printf("Process 0 received: %d\n", value);
} else {
    MPI_Recv(&value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    value = value * 2;
    MPI_Send(&value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
}
```

(a) Trace the sequence of messages and show the final value printed by process 0.
(b) Will this code deadlock? Justify your answer.

**Model Answer (6 marks)**
(a)
1. Process 0 sends `value = 42` to process 1 with tag 0 (1 mark).
2. Process 1 receives it; computes `value = 84`; sends `84` back to process 0 with tag 1 (1 mark).
3. Process 0 receives `84` and prints `Process 0 received: 84` (1 mark).

(b) No deadlock — the ordering is safe (1 mark). Process 1 posts its `MPI_Recv` before process 0's `MPI_Send` completes, so the receive is ready when the send arrives. Process 0's second call (`MPI_Recv` from 1) will not block indefinitely because process 1 will eventually reach its `MPI_Send` (2 marks for reasoning — 1 for correct conclusion, 1 for explanation).

---

### Q11. Spot the Bug
The following code is intended to distribute an array of 8 integers from process 0 to processes 1–3 (one segment of 2 integers each) using collective operations, run with `mpirun -np 4`. Identify the bug and explain its effect.

```c
int rank;
int sendbuf[8] = {1,2,3,4,5,6,7,8};
int recvbuf[2];
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

if (rank == 0) {
    MPI_Scatter(sendbuf, 2, MPI_INT, recvbuf, 2, MPI_INT, 0, MPI_COMM_WORLD);
}
printf("Process %d got: %d %d\n", rank, recvbuf[0], recvbuf[1]);
```

**Model Answer (4 marks)**
- **Bug:** `MPI_Scatter` is called *only* by process 0. Collective operations require **all** processes to participate (1 mark).
- Processes 1, 2, 3 never call `MPI_Scatter`, so they block or execute undefined behaviour while process 0 sits in the collective call waiting for the other processes to join — resulting in a **deadlock** (2 marks).
- **Fix:** Move `MPI_Scatter` outside the `if (rank == 0)` guard so all four processes call it:
```c
MPI_Scatter(sendbuf, 2, MPI_INT, recvbuf, 2, MPI_INT, 0, MPI_COMM_WORLD);
```
Note that `sendbuf` is only meaningful on the root (process 0) for scatter; other processes may pass `NULL` for it or any buffer (1 mark).

---

### Q12. Analyse the Non-blocking Pattern
What does the following code do? Identify any potential error in the usage pattern.

```c
double buf[N];
MPI_Request req;

// ... fill buf with data ...

MPI_Isend(buf, N, MPI_DOUBLE, dest, 0, MPI_COMM_WORLD, &req);

// Modify buf here immediately:
for (int i = 0; i < N; i++) buf[i] = 0.0;

MPI_Wait(&req, MPI_STATUS_IGNORE);
```

**Model Answer (4 marks)**
- The code initiates a non-blocking send of `buf` to `dest`, then immediately zeroes `buf`, then waits for the send to complete (1 mark).
- **Error:** The send buffer `buf` is modified *before* `MPI_Wait` confirms the transfer is complete (1 mark). The MPI standard prohibits modifying the send buffer between `MPI_Isend` and the matching `MPI_Wait`; doing so produces **undefined behaviour** — the receiver may receive zeros or a mixture of the original and modified data (1 mark).
- **Fix:** Perform `MPI_Wait` before modifying `buf`, or use a separate buffer for the modification (1 mark).

---

## Section C: Code Writing

### Q13. Hello World in MPI
Write a complete, compilable C MPI program that prints `Hello from process X of Y` for each process, where X is the rank and Y is the total number of processes.

**Model Answer**
```c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {
    int rank, size;

    MPI_Init(&argc, &argv);                          // initialise MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);            // get this process's rank
    MPI_Comm_size(MPI_COMM_WORLD, &size);            // get total number of processes

    printf("Hello from process %d of %d\n", rank, size);

    MPI_Finalize();                                  // shut down MPI
    return 0;
}
```

**Marking points (4 marks):** `MPI_Init` present and first (1); `MPI_Finalize` present and last (1); correct use of `MPI_Comm_rank` and `MPI_Comm_size` (1); correct printf format (1).

---

### Q14. Ring Communication
Write an MPI C program where each process sends its rank to the *next* process in a logical ring (process `p` sends to process `(p+1) % size`) and receives from the previous process (`(p-1+size) % size`). Each process should print its own rank and the value it received.

**Model Answer**
```c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {
    int rank, size;
    int send_val, recv_val;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    send_val = rank;
    int dest   = (rank + 1) % size;
    int source = (rank - 1 + size) % size;

    // Use Sendrecv to avoid deadlock in the ring
    MPI_Sendrecv(&send_val, 1, MPI_INT, dest,   0,
                 &recv_val, 1, MPI_INT, source, 0,
                 MPI_COMM_WORLD, &status);

    printf("Process %d: sent %d, received %d (from process %d)\n",
           rank, send_val, recv_val, source);

    MPI_Finalize();
    return 0;
}
```

**Marking points (5 marks):** Correct ring index arithmetic with modulo including wrap-around (1); use of `MPI_Sendrecv` *or* carefully ordered `MPI_Send`/`MPI_Recv` that does not deadlock (2); correct send/recv buffers and datatypes (1); output prints own rank and received value (1).

---

### Q15. Broadcast and Use
Write MPI C code (not necessarily a full program) that:
1. Has process 0 read an integer `n` from standard input.
2. Broadcasts `n` to all processes using the correct MPI collective call.
3. Has every process print `n`.

**Model Answer**
```c
int n;
if (rank == 0) {
    scanf("%d", &n);
}
MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
printf("Process %d: n = %d\n", rank, n);
```

**Marking points (4 marks):** Only rank 0 reads input (1); `MPI_Bcast` called by ALL processes including rank 0 (1); correct arguments — buffer, count, type, root, comm (1); print after broadcast so all processes have the value (1).

---

### Q16. Global Sum with MPI_Reduce
Each of P processes holds a local `double sum`. Write the single MPI call that computes the global sum across all processes and stores the result in `global_sum` on process 0 only. Then write the call that would deliver the result to ALL processes instead.

**Model Answer**
```c
double local_sum;   // each process has this
double global_sum;  // result variable

// Sum to root only:
MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

// Sum to all processes:
MPI_Allreduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
```

**Marking points (4 marks):** Correct use of `MPI_Reduce` with `MPI_SUM` operator and root 0 (2); correct use of `MPI_Allreduce` (note: no root argument) (2).

---

### Q17. Non-blocking Halo Exchange
Write a C code fragment (not a full program) that implements a 1D halo exchange for a process that:
- Has left neighbour `left` and right neighbour `right` (use `MPI_PROC_NULL` if at a boundary).
- Stores its local data in `double local[N+2]` where `local[0]` is the left halo and `local[N+1]` is the right halo.
- `local[1]` is the leftmost owned cell; `local[N]` is the rightmost owned cell.
- Uses non-blocking sends/receives and waits for all transfers to complete before returning.

**Model Answer**
```c
MPI_Request reqs[4];
MPI_Status  stats[4];

// Post non-blocking receives first to avoid deadlock
MPI_Irecv(&local[0],   1, MPI_DOUBLE, left,  0, MPI_COMM_WORLD, &reqs[0]);
MPI_Irecv(&local[N+1], 1, MPI_DOUBLE, right, 0, MPI_COMM_WORLD, &reqs[1]);

// Post non-blocking sends
MPI_Isend(&local[1], 1, MPI_DOUBLE, left,  0, MPI_COMM_WORLD, &reqs[2]);
MPI_Isend(&local[N], 1, MPI_DOUBLE, right, 0, MPI_COMM_WORLD, &reqs[3]);

// Wait for all four operations to complete
MPI_Waitall(4, reqs, stats);
```

**Marking points (6 marks):** Receives posted before sends (best practice / deadlock-safe) (1); correct buffer addresses for halos and boundary cells (2); correct neighbour ranks `left` and `right` used consistently (1); `MPI_Request` array and `MPI_Waitall` with correct count (2).

---

## Section D: Deadlock Analysis

### Q18. Classic Send-Send Deadlock
The following code runs on exactly 2 processes. Explain why it deadlocks and provide a corrected version.

```c
int rank, value = 0;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

if (rank == 0) {
    MPI_Send(&value, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    MPI_Recv(&value, 1, MPI_INT, 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
} else {
    MPI_Send(&value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    MPI_Recv(&value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}
```

**Model Answer (6 marks)**

**Why it deadlocks (3 marks):**
- Both process 0 and process 1 call `MPI_Send` first.
- `MPI_Send` is blocking; for large messages it will not return until a matching `MPI_Recv` has been posted on the other side.
- Since neither process ever reaches its `MPI_Recv` (both are stuck in their respective `MPI_Send`), a **cyclic dependency** forms: process 0 waits for process 1 to receive, and process 1 waits for process 0 to receive. Neither can proceed — deadlock.

*(Note: For small messages, MPI implementations may buffer the send internally and return, which can mask the deadlock — but this is implementation-dependent and not guaranteed.)*

**Fix option 1 — Swap send/recv order on one process (2 marks):**
```c
if (rank == 0) {
    MPI_Send(&value, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    MPI_Recv(&value, 1, MPI_INT, 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
} else {                                           // rank == 1
    MPI_Recv(&value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Send(&value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
}
```

**Fix option 2 — Use MPI_Sendrecv (1 mark):**
```c
MPI_Sendrecv(&value, 1, MPI_INT, (rank+1)%2, 0,
             &value, 1, MPI_INT, (rank+1)%2, 0,
             MPI_COMM_WORLD, MPI_STATUS_IGNORE);
```

---

### Q19. Collective Deadlock
Four processes run the code below. Identify all potential deadlock scenarios and explain what causes them.

```c
int rank;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

if (rank < 2) {
    MPI_Barrier(MPI_COMM_WORLD);
}
printf("Process %d past barrier\n", rank);
```

**Model Answer (4 marks)**
- `MPI_Barrier` is a collective operation that requires **all** processes in `MPI_COMM_WORLD` to call it (1 mark).
- Only processes 0 and 1 enter the `if (rank < 2)` branch and call `MPI_Barrier`; processes 2 and 3 skip the barrier and continue to `printf` (1 mark).
- Processes 0 and 1 will block at the barrier indefinitely waiting for processes 2 and 3 to arrive — **deadlock** (1 mark).
- **Fix:** All processes must call the collective, so remove the conditional guard around `MPI_Barrier` (1 mark).

---

### Q20. Ring Deadlock
The following 4-process ring communication uses only blocking sends and receives. Identify whether it deadlocks, explain the reason, and suggest a fix.

```c
int rank, size, send_val, recv_val;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);

send_val = rank;
int right = (rank + 1) % size;
int left  = (rank - 1 + size) % size;

MPI_Recv(&recv_val, 1, MPI_INT, left,  0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
MPI_Send(&send_val, 1, MPI_INT, right, 0, MPI_COMM_WORLD);
```

**Model Answer (5 marks)**
- **Deadlock:** Yes (1 mark).
- Every process calls `MPI_Recv` first, waiting to receive from its left neighbour (1 mark).
- Since every process is blocked in `MPI_Recv`, no process ever reaches `MPI_Send` — no messages are sent, so no receives can complete — classic cyclic deadlock (2 marks).
- **Fix — use non-blocking operations:**
```c
MPI_Request reqs[2];
MPI_Irecv(&recv_val, 1, MPI_INT, left,  0, MPI_COMM_WORLD, &reqs[0]);
MPI_Isend(&send_val, 1, MPI_INT, right, 0, MPI_COMM_WORLD, &reqs[1]);
MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
```
(1 mark for a valid fix with correct reasoning)

---

## Section E: Calculation Questions

### Q21. Alpha-Beta Communication Model
The **alpha-beta** (or latency-bandwidth) model estimates the time to transfer a message of `n` bytes as:

```
T_comm = alpha + n * beta
```

where `alpha` is the latency (seconds) and `beta = 1/bandwidth` (seconds/byte).

A cluster has `alpha = 2 µs` and a bandwidth of `10 GB/s` (`beta = 0.1 ns/byte`).

(a) Calculate the time to send a single `MPI_DOUBLE` (8 bytes).
(b) Calculate the time to send an array of 1000 doubles (8000 bytes).
(c) At what message size does the bandwidth term equal the latency term?

**Model Answer (6 marks)**

Given: `alpha = 2 × 10^-6 s`, `beta = 1 / (10 × 10^9) = 10^-10 s/byte`

(a) `T = 2×10^-6 + 8 × 10^-10 = 2×10^-6 + 8×10^-10 ≈ 2.0008 µs`
Latency dominates for small messages. (2 marks)

(b) `T = 2×10^-6 + 8000 × 10^-10 = 2×10^-6 + 8×10^-7 = 2.8 µs` (2 marks)

(c) Set `alpha = n * beta`:
`n = alpha / beta = (2×10^-6) / (10^-10) = 20,000 bytes = 20 KB` (2 marks)

---

### Q22. Halo Exchange Cost
A 1D domain decomposition divides a 1D array of `N = 10,000` doubles across `P = 10` processes. Each process owns `n = N/P = 1000` elements and must exchange one double with each of its two neighbours per timestep.

Using the alpha-beta model with `alpha = 1 µs` and bandwidth `B = 8 GB/s` (so `beta = 1.25 × 10^-10 s/byte`):

(a) How many bytes are sent per halo message?
(b) Calculate the total halo exchange time per timestep for a non-boundary process (two messages, assumed sequential).
(c) How would using non-blocking communication reduce the effective cost?

**Model Answer (6 marks)**

(a) 1 double = 8 bytes per message (1 mark).

(b) Time per message: `T = 1×10^-6 + 8 × 1.25×10^-10 = 1×10^-6 + 10^-9 ≈ 1.001 µs`
Total for two sequential messages: `2 × 1.001 µs ≈ 2.002 µs` (2 marks).

(c) With non-blocking (`MPI_Isend`/`MPI_Irecv`), both halo messages can be posted simultaneously and the process can compute on interior elements while the transfers proceed. The effective communication overhead is overlapped with computation, reducing the *visible* delay to at most one message time rather than the sum — potentially halving the exposed latency for small halos (3 marks: posting both simultaneously (1), overlapping with interior computation (1), net effect on exposed cost (1)).

---

### Q23. 1D vs 2D Decomposition Communication Volume
A square 2D grid of size `N × N` points is distributed across `P` processes.

(a) In a **1D (row) decomposition**, each process owns `N/P` rows. Assuming a 5-point stencil, how many doubles are exchanged per neighbour per halo exchange?
(b) In a **2D decomposition** (sqrt(P) × sqrt(P) blocks), each process owns `(N/sqrt(P)) × (N/sqrt(P))` cells. How many doubles are exchanged per neighbour per halo exchange? (Each process now has up to 4 neighbours.)
(c) For `N = 1000`, `P = 100`: compute the halo message size in each case and state which decomposition sends smaller messages.

**Model Answer (6 marks)**

(a) 1D: each process exchanges one full row of `N` doubles with each neighbour. Halo message size = `N` doubles (1 mark).

(b) 2D: each process has blocks of `(N/sqrt(P))` columns wide. The top/bottom neighbours require exchanging a row of `N/sqrt(P)` doubles; the left/right neighbours require a column of `N/sqrt(P)` doubles. Halo size per neighbour = `N/sqrt(P)` doubles (2 marks).

(c) `N = 1000`, `P = 100`, `sqrt(P) = 10`:
- 1D: `N = 1000` doubles per message × 2 neighbours = 2000 doubles total per exchange.
- 2D: `N/sqrt(P) = 100` doubles per message × 4 neighbours = 400 doubles total per exchange.
- **2D decomposition sends smaller messages**, reducing total communication volume by a factor of 5 in this case; it scales better as P increases because message size grows as `O(N/sqrt(P))` vs `O(N)` (3 marks).

---

## Section F: Multi-Part Exam Questions

### Q24. MPI PDE Solver Design [15 marks]
A finite-difference solver for the 1D heat equation `du/dt = D * d²u/dx²` is to be parallelised using MPI across `P` processes. The global domain has `N` grid points; the timestep is constrained by the CFL condition: `dt ≤ (dx²) / (2D)`.

**(a)** [3 marks] Describe how you would distribute the initial data from process 0 to all other processes at the start of the simulation. Which MPI collective(s) would you use and why?

**(b)** [4 marks] Explain the halo exchange required at each timestep. Write pseudocode (or C code) showing the non-blocking pattern. State why non-blocking is preferred over blocking here.

**(c)** [3 marks] Each process independently computes the locally stable timestep `local_dt = dx^2 / (2D)` (which may differ if `dx` is non-uniform). Write the MPI call that synchronises all processes on the global minimum stable `dt`.

**(d)** [2 marks] After the simulation completes, process 0 must collect all sub-domain results to write output. Which collective operation should be used?

**(e)** [3 marks] Comment on how you would transition from pure MPI to a hybrid MPI+OpenMP approach for this solver. What part of the code would OpenMP parallelise, and what would MPI still handle?

---

**Model Answer**

**(a)** Use `MPI_Bcast` to broadcast global parameters (N, D, dx, number of timesteps) from process 0 to all processes. Use `MPI_Scatter` to distribute the initial condition array: process 0 holds the full `u[N]` array and `MPI_Scatter` sends a contiguous block of `N/P` elements to each process. `MPI_Scatter` is appropriate here because each process needs a *different* segment of the data, unlike `MPI_Bcast` which sends the same data to all. (3 marks: Bcast for params (1), Scatter for IC (1), reason Scatter vs Bcast (1))

**(b)** At each timestep, each process must share its leftmost and rightmost owned grid point values with its left and right neighbours respectively. Non-blocking preferred because:
- Both the left- and right-directed sends can be posted simultaneously.
- The process can compute on interior points while boundary data is in transit.
- Eliminates risk of deadlock from symmetric blocking send/recv patterns.

```c
MPI_Request reqs[4];
// Post receives first
MPI_Irecv(&u_local[0],       1, MPI_DOUBLE, left,  0, MPI_COMM_WORLD, &reqs[0]);
MPI_Irecv(&u_local[n_loc+1], 1, MPI_DOUBLE, right, 0, MPI_COMM_WORLD, &reqs[1]);
// Post sends
MPI_Isend(&u_local[1],     1, MPI_DOUBLE, left,  0, MPI_COMM_WORLD, &reqs[2]);
MPI_Isend(&u_local[n_loc], 1, MPI_DOUBLE, right, 0, MPI_COMM_WORLD, &reqs[3]);

// Compute interior stencil while messages in flight ...

MPI_Waitall(4, reqs, MPI_STATUSES_IGNORE);
// Now compute boundary stencil using updated halos
```
(4 marks: correct Irecv/Isend pattern (2), compute interior while waiting (1), Waitall before using halos (1))

**(c)**
```c
double local_dt  = (dx * dx) / (2.0 * D);
double global_dt;
MPI_Allreduce(&local_dt, &global_dt, 1, MPI_DOUBLE, MPI_MIN, MPI_COMM_WORLD);
```
`MPI_Allreduce` with `MPI_MIN` ensures every process gets the same (most restrictive) timestep, maintaining synchronised timestepping. (3 marks: Allreduce not Reduce (1), MPI_MIN operator (1), result delivered to all processes (1))

**(d)** `MPI_Gather` — collects `N/P` elements from each process into a contiguous array on process 0 for file output. (2 marks: correct collective (1), correct justification (1))

**(e)** In a hybrid approach:
- **MPI** continues to own domain decomposition: each MPI rank handles one sub-domain, all inter-node halo exchanges remain as MPI messages.
- **OpenMP** parallelises the inner loop over grid points within each sub-domain: `#pragma omp parallel for` over the stencil computation `for (i = 1; i <= n_loc; i++)`.
- Benefit: reduces the number of MPI ranks (fewer, larger messages), lowers MPI overhead, and better utilises multi-core nodes. The OpenMP threads share memory within a node, avoiding unnecessary MPI traffic for intra-node data. (3 marks: MPI handles inter-node (1), OpenMP parallelises inner loop (1), benefit articulated (1))

---

### Q25. Blocking vs. Non-blocking Communication [12 marks]
**(a)** [2 marks] Write the full function signatures (in C) for `MPI_Send` and `MPI_Isend`, and label each parameter.

**(b)** [3 marks] Under what conditions can a blocking `MPI_Send` return before the receiver has called `MPI_Recv`? What risks does this create?

**(c)** [4 marks] The following exchange between process 0 and process 1 uses blocking sends/receives. Does it deadlock? Rewrite it using non-blocking operations with proper completion.

```c
// Both processes:
int rank, buf_send = rank, buf_recv;
if (rank == 0) {
    MPI_Send(&buf_send, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    MPI_Recv(&buf_recv, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
} else {
    MPI_Send(&buf_send, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    MPI_Recv(&buf_recv, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}
```

**(d)** [3 marks] Describe the `MPI_Request` object. What functions use it and what happens if you free a request without waiting for it to complete?

---

**Model Answer**

**(a)**
```c
int MPI_Send(void *buf,         // send buffer
             int count,         // number of elements
             MPI_Datatype dtype,// element type
             int dest,          // destination rank
             int tag,           // message tag
             MPI_Comm comm);    // communicator

int MPI_Isend(void *buf,        // send buffer (do not modify until Wait)
              int count,        // number of elements
              MPI_Datatype dtype,
              int dest,
              int tag,
              MPI_Comm comm,
              MPI_Request *req);// handle to track completion
```
(2 marks: correct signatures with all parameters (1 each))

**(b)** `MPI_Send` may return early if the MPI runtime buffers the message internally (eager protocol for small messages). However:
- This is implementation-dependent and not guaranteed by the standard.
- If the buffer is reused before the message is actually transferred, the receiver may receive corrupted data.
- For large messages, MPI typically uses a rendezvous protocol requiring a matching receive, meaning `MPI_Send` blocks regardless.
(3 marks: internal buffering (1), risk of corruption on buffer reuse (1), size-dependent behaviour (1))

**(c)** This code **will deadlock for large messages** for the same reason as Q18 — both processes call `MPI_Send` before `MPI_Recv`, creating cyclic blocking.

Non-blocking rewrite:
```c
MPI_Request reqs[2];
MPI_Irecv(&buf_recv, 1, MPI_INT, (rank+1)%2, 0, MPI_COMM_WORLD, &reqs[0]);
MPI_Isend(&buf_send, 1, MPI_INT, (rank+1)%2, 0, MPI_COMM_WORLD, &reqs[1]);
MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
```
(4 marks: correct deadlock identification (1), Irecv before Isend (1), correct peer rank (1), Waitall (1))

**(d)** An `MPI_Request` is an opaque handle returned by non-blocking operations (`MPI_Isend`, `MPI_Irecv`). It tracks the state of the communication and is used as input to `MPI_Wait`, `MPI_Waitall`, `MPI_Test`, etc., to check or await completion. If the request is freed or ignored without calling `MPI_Wait`, the associated resources may leak and the send buffer remains logically "in use" — modifying it leads to undefined behaviour. `MPI_Request_free` marks the request for deallocation but does not cancel the underlying operation. (3 marks: opaque handle for tracking (1), used by Wait/Test functions (1), consequence of not waiting (1))

---

### Q26. Domain Decomposition Design [10 marks]
A team is parallelising a 2D N×N grid simulation (finite differences, 5-point stencil) across P MPI processes.

**(a)** [2 marks] Describe a **1D column decomposition**. How many neighbours does each (non-boundary) process have and what data must be exchanged?

**(b)** [2 marks] Describe a **2D block decomposition** (assuming P is a perfect square). How does the number of neighbours change, and how does the total halo volume compare to the 1D case for large P?

**(c)** [3 marks] For the 2D case, process 0 must construct a 2D process grid (a Cartesian topology). Name the MPI function used for this and list the key arguments. What advantage does MPI provide by using Cartesian topology functions?

**(d)** [3 marks] In a time-stepping loop, outline the **correct ordering** of operations within one timestep to maximise computation/communication overlap.

---

**Model Answer**

**(a)** 1D column decomposition assigns each process a contiguous block of `N/P` columns of the full N×N grid. Each non-boundary process has **2 neighbours** (left and right). At each timestep the process must exchange one column of N doubles with each neighbour — a message of N × 8 bytes. (2 marks)

**(b)** 2D block decomposition: each process owns a `(N/sqrt(P)) × (N/sqrt(P))` block and has **up to 4 neighbours** (left, right, above, below; corner processes have 2, edge processes have 3). Each halo message is of size `N/sqrt(P)` doubles per neighbour. Total halo volume per exchange = `4 × N/sqrt(P)` doubles, vs `2N` doubles for 1D, giving a reduction factor of approximately `sqrt(P)/2` — 2D decomposition has significantly lower communication volume for large P. (2 marks)

**(c)** `MPI_Cart_create(MPI_Comm comm_old, int ndims, int *dims, int *periods, int reorder, MPI_Comm *comm_cart)` creates a new communicator with Cartesian topology metadata attached:
- `ndims = 2`, `dims = {sqrt(P), sqrt(P)}`, `periods` = wrap or no-wrap.
- MPI can then use `MPI_Cart_shift` to find neighbour ranks automatically.
- Advantage: the library can map ranks to a physical topology optimally (reorder=1), and `MPI_Cart_shift` provides convenient neighbour rank lookup, reducing programmer error. (3 marks: function name and key args (1), MPI_Cart_shift convenience (1), topology-aware rank ordering benefit (1))

**(d)** Correct ordering to maximise overlap:
1. Post all non-blocking receives (`MPI_Irecv`) for halo data from neighbours.
2. Post all non-blocking sends (`MPI_Isend`) of this process's boundary rows/columns to neighbours.
3. **Compute the interior stencil** (all points not depending on halo data) — this work overlaps with the ongoing message transfers.
4. Call `MPI_Waitall` to ensure all halo data has arrived.
5. **Compute the boundary stencil** (points that depend on halo values) — only safe after Wait.
(3 marks: Irecv/Isend first (1), interior computation before Wait (1), boundary computation after Wait (1))

---

*End of Week 4 Practice Questions*

---

**Compilation and Execution Reference**
```bash
# Compile an MPI C program
mpicc -o my_program my_program.c

# Run with 4 processes
mpirun -np 4 ./my_program
```

**Key MPI Functions Quick Reference**

| Function | Description |
| :--- | :--- |
| `MPI_Init` | Initialise MPI environment |
| `MPI_Finalize` | Shut down MPI environment |
| `MPI_Comm_rank` | Get calling process rank |
| `MPI_Comm_size` | Get total process count |
| `MPI_Send` | Blocking send |
| `MPI_Recv` | Blocking receive |
| `MPI_Isend` | Non-blocking send |
| `MPI_Irecv` | Non-blocking receive |
| `MPI_Wait` | Wait for single request |
| `MPI_Waitall` | Wait for multiple requests |
| `MPI_Bcast` | Broadcast from root to all |
| `MPI_Scatter` | Distribute segments from root |
| `MPI_Gather` | Collect segments to root |
| `MPI_Allgather` | Gather and distribute to all |
| `MPI_Reduce` | Reduction to root |
| `MPI_Allreduce` | Reduction to all |
| `MPI_Barrier` | Synchronise all processes |
| `MPI_Sendrecv` | Simultaneous send and receive |
| `MPI_Cart_create` | Create Cartesian topology communicator |
