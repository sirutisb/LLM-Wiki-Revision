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


### Q3. List the six steps in the standard recipe for creating a new MPI communicator from a subset of `MPI_COMM_WORLD`.

**Model Answer:**

1. **`MPI_Comm_group`** — obtain the group object associated with `MPI_COMM_WORLD`.
2. **`MPI_Group_incl` or `MPI_Group_excl`** — build a new group by specifying which ranks to include or exclude.
3. **`MPI_Comm_create`** — create a new communicator from the new group (called collectively by all processes in the parent communicator).
4. **`MPI_Comm_rank`** — determine the calling process's rank within the new communicator.
5. **Do work** — use the new communicator for collective or point-to-point operations restricted to the group.
6. **`MPI_Comm_free` and `MPI_Group_free`** — release the communicator and group objects to avoid resource leaks.

*(1 mark per step; must be in correct order for full credit.)*


### Q10. In one sentence each, state when you would choose (a) `sections`, (b) `task`, and (c) `parallel for` in OpenMP.

**Model Answer:**

**(a) `sections`:** Use when you have a **small, fixed number of independent, heterogeneous code blocks** that can run concurrently (e.g. initialising two different arrays simultaneously).

**(b) `task`:** Use when the work is **irregular, recursive, or has an unknown trip count** at compile time (e.g. linked list traversal, tree recursion, while loops, Mandelbrot where each column's cost varies wildly).

**(c) `parallel for`:** Use when you have a **loop with a known trip count and roughly uniform work per iteration** — it maps directly to the parallel loop model with optional `schedule` clause for minor load imbalance.

*(1 mark each.)*


## Section C: OpenMP Offloading

### Q12. What does the following OpenMP directive do? Identify and explain the role of each component.

```c
#pragma omp target teams distribute parallel for
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

**Model Answer (5 marks)**

- `target` — offloads the following code block from the host CPU to the device (GPU). Execution moves to the GPU for the duration of the loop. [1]
- `teams` — spawns a **league of thread teams** on the device. Each team is analogous to a set of thread blocks that can each run independently on different SMs. [1]
- `distribute` — distributes the loop iterations across the league of teams, so each team handles a subset of the `i` values. [1]
- `parallel for` — within each team, this further distributes iterations across individual threads within that team using a parallel work-sharing loop, so the full GPU thread hierarchy is exploited. [1]
- Combined effect: the loop body `c[i] = a[i] + b[i]` is executed on the GPU, with iterations distributed first across teams (thread blocks / SMs) and then across threads within each team. This is the standard pattern for offloading a simple parallel loop to a GPU with OpenMP. [1]