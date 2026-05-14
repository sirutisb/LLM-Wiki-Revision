---
title: "Week 7 Practice Questions: Factors Affecting Parallel Performance"
tags: [hpc, week-7, scaling, performance, practice]
date: 2026-05-14
---

# Week 7 Practice Questions: Factors Affecting Parallel Performance

> **Coverage:** Strong/weak scaling, Amdahl's Law, Gustafson's Law, parallel efficiency,
> SLOW overhead model, OpenMP scheduling, barriers, network topologies (fat-tree, torus/mesh,
> ring), the alpha-beta latency/bandwidth model, and domain decomposition communication scaling.
>
> Each question is followed by a model answer. For calculation questions, full working is shown.

---

## Section A: Short Answer / Definition

**Q1.** Define *parallel speedup* and *parallel efficiency*. What values do these metrics take for a perfectly parallelised program running on 8 processors?

> **Model Answer:**
> - **Speedup:** `S(N) = T_0 / T_N`, where `T_0` is serial execution time and `T_N` is parallel execution time on `N` processors.
> - **Efficiency:** `E(N) = S(N) / N`. Normalises speedup by the number of processors.
> - For a perfectly parallel program on 8 processors: `S(8) = 8` (linear speedup), `E(8) = 8/8 = 1.0` (100%). [1 mark each]

---

**Q2.** What is the SLOW acronym used to categorise sources of parallel performance degradation? Give one concrete example of each category.

> **Model Answer:**
> - **S — Starvation:** Insufficient or unevenly distributed work. Example: one thread processes 90% of loop iterations while others sit idle.
> - **L — Latency:** Delays from memory hierarchy or network. Example: a cache miss causing a main-memory fetch; waiting for a remote MPI message to arrive.
> - **O — Overhead:** Extra work introduced by parallelism itself. Example: OpenMP thread creation cost; MPI message envelope processing.
> - **W — Waiting:** Contention for shared resources. Example: multiple threads competing for a lock on a critical section; processes blocked at a barrier.
> [1 mark per category, 0.5 mark for a valid example]

---

**Q3.** State Amdahl's Law. Define every symbol you use and state the physical meaning of the law's limit as the number of processors tends to infinity.

> **Model Answer:**
> `S_max = 1 / s`
>
> where:
> - `S_max` = maximum achievable speedup
> - `s` = the strictly sequential (non-parallelisable) fraction of the total serial runtime (`0 < s <= 1`)
>
> The full form is: `S(N) = 1 / (s + p/N)`, where `p = 1 - s` is the parallelisable fraction and `N` is the number of processors.
>
> As `N -> infinity`, `p/N -> 0`, so `S(N) -> 1/s`. This means that no matter how many processors are used, the speedup is bounded by the reciprocal of the serial fraction. A program that is 5% serial can never exceed 20x speedup regardless of hardware.

---

**Q4.** Distinguish between *strong scaling* and *weak scaling*. For each, state (i) what is kept constant, (ii) what changes, and (iii) a typical scientific use case.

> **Model Answer:**
>
> | | Strong Scaling | Weak Scaling |
> |---|---|---|
> | **Fixed** | Total problem size | Work per processor |
> | **Changes** | Time-to-solution decreases | Total problem size increases |
> | **Goal** | Reduce wall-clock time (latency) | Solve larger problems in fixed time (throughput) |
> | **Use case** | Fixed-dataset processing, real-time simulations | CFD, weather modelling, molecular dynamics |
>
> [2 marks per scaling type; 1 for each of what's fixed/changes, 1 for use case]

---

**Q5.** Explain what an *implicit barrier* is in OpenMP and list three constructs that generate one.

> **Model Answer:**
> An implicit barrier is a synchronisation point that OpenMP inserts **automatically** at the end of certain constructs. All threads in the team must arrive at the barrier before any thread is allowed to continue beyond it.
>
> Constructs that generate an implicit barrier:
> 1. `#pragma omp parallel` — end of the parallel region.
> 2. `#pragma omp for` — end of the worksharing loop.
> 3. `#pragma omp single` — end of the single block.
> 4. `#pragma omp sections` — end of the sections construct.
> (Any three of the four above accepted.)

---

**Q6.** What does the `nowait` clause do in OpenMP? Give a code example and explain the risk of using it incorrectly.

> **Model Answer:**
> `nowait` removes the implicit barrier at the end of a worksharing construct, allowing threads that finish their chunk to proceed immediately rather than waiting for all threads.
>
> Example:
> ```c
> #pragma omp for nowait
> for (int i = 0; i < N; i++) {
>     A[i] = compute(i);
> }
> // Threads that finish early proceed here immediately
> // without waiting for other threads
> do_independent_work();
> ```
>
> **Risk:** If subsequent code depends on the loop having fully completed (e.g., reading values from `A` written by other threads), a data race occurs because some threads may not have written their results yet. `nowait` is only safe when there is no data dependency between the worksharing construct and the subsequent code.

---

**Q7.** Describe the three OpenMP loop scheduling strategies — `static`, `dynamic`, and `guided` — and state when each is most appropriate.

> **Model Answer:**
> - **`schedule(static, chunk)`:** Iterations are divided into blocks of size `chunk` and assigned to threads in round-robin order **at compile time** (before execution). Overhead is minimal. Best when each iteration takes roughly equal time (balanced workload).
> - **`schedule(dynamic, chunk)`:** Threads request a new chunk of `chunk` iterations from a runtime queue as soon as they finish their current chunk. Excellent load balancing for irregular workloads, but has higher runtime overhead due to the dynamic assignment mechanism.
> - **`schedule(guided, chunk)`:** Like dynamic, but the chunk size **starts large and shrinks exponentially** down to the specified minimum `chunk`. Reduces the number of scheduler interactions (lower overhead than pure dynamic) while still providing good load balance.
>
> Rule of thumb: static for uniform loops, dynamic for highly irregular loops, guided as a compromise.

---

**Q8.** Explain how the communication-to-computation ratio scales with sub-domain size during strong scaling of a 2D domain decomposition.

> **Model Answer:**
> For a 2D sub-domain of size `N x N`:
> - Computation is proportional to the **area**: `~N^2`
> - Communication (halo exchange) is proportional to the **perimeter**: `~4N`
> - Ratio: `communication / computation ~ 4N / N^2 = 4/N`
>
> As the number of processors increases during strong scaling, the total domain is fixed so each sub-domain shrinks (N decreases). Therefore `4/N` **increases** — communication overhead becomes a progressively larger fraction of total work. This is why strong scaling eventually saturates even in the absence of a serial bottleneck.

---

**Q9.** Define *bisection bandwidth* for a network. Why is it an important metric for HPC clusters?

> **Model Answer:**
> Bisection bandwidth is the **minimum total bandwidth** across any cut that divides the network into two equal halves. It represents the worst-case aggregate communication capacity between two halves of the machine.
>
> It is important because many parallel algorithms (e.g., all-to-all reductions, FFT, matrix transpose) require data to cross the network boundary. If the bisection bandwidth is low, these communications become a bottleneck regardless of the bandwidth within each half. A high bisection bandwidth indicates a well-connected, non-blocking network.

---

**Q10.** What is *super-linear speedup*? Is it theoretically possible under Amdahl's Law? Give a practical mechanism that causes it.

> **Model Answer:**
> Super-linear speedup occurs when `S(N) > N`, i.e., efficiency `E(N) > 1`. Under Amdahl's Law (which only models computation division), speedup is always `<= N`, so it is **not theoretically predicted** by the law alone.
>
> In practice it occurs due to **cache effects**: when strong scaling reduces the sub-domain assigned to each processor, a critical working set that previously did not fit in cache may now fit entirely in L1/L2 cache. The dramatic reduction in cache misses can accelerate computation far beyond the linear expectation from work division alone.

---

## Section B: Amdahl's Law Calculations

**Q11.** A parallel program has a serial fraction `s = 0.05` (5% of the total runtime is strictly sequential). Calculate:
- (a) The maximum theoretical speedup.
- (b) The speedup and efficiency when run on 16 processors.
- (c) The speedup and efficiency when run on 64 processors.
- (d) Comment on how efficiency changes as N increases.

> **Model Answer:**
>
> Given: `s = 0.05`, so `p = 1 - 0.05 = 0.95`
>
> **(a) Maximum speedup:**
> ```
> S_max = 1/s = 1/0.05 = 20
> ```
> No matter how many processors are used, speedup cannot exceed **20x**.
>
> **(b) N = 16:**
> ```
> S(16) = 1 / (s + p/N)
>        = 1 / (0.05 + 0.95/16)
>        = 1 / (0.05 + 0.059375)
>        = 1 / 0.109375
>        ≈ 9.14
>
> E(16) = S(16)/16 = 9.14/16 ≈ 0.571 (57.1%)
> ```
>
> **(c) N = 64:**
> ```
> S(64) = 1 / (0.05 + 0.95/64)
>        = 1 / (0.05 + 0.014844)
>        = 1 / 0.064844
>        ≈ 15.42
>
> E(64) = S(64)/64 = 15.42/64 ≈ 0.241 (24.1%)
> ```
>
> **(d) Comment:**
> As `N` increases from 16 to 64 (4x more processors), speedup only increases from 9.14 to 15.42 (not 4x). Efficiency drops from 57% to 24%. This illustrates the Amdahl ceiling: the serial fraction increasingly dominates, and additional processors yield diminishing returns. The parallel portion of the work is quickly divided to near-zero, but the serial floor `sT_0` cannot be reduced.

---

**Q12.** A program runs in 400 seconds on a single processor. When run on 20 processors it completes in 30 seconds. Calculate:
- (a) The observed speedup.
- (b) The parallel efficiency.
- (c) Using Amdahl's Law, estimate the serial fraction `s`.
- (d) What is the maximum speedup this program could theoretically achieve?

> **Model Answer:**
>
> Given: `T_0 = 400 s`, `T_20 = 30 s`, `N = 20`
>
> **(a) Observed speedup:**
> ```
> S(20) = T_0 / T_20 = 400 / 30 ≈ 13.33
> ```
>
> **(b) Parallel efficiency:**
> ```
> E(20) = S(20) / N = 13.33 / 20 ≈ 0.667 (66.7%)
> ```
>
> **(c) Estimating serial fraction using Amdahl:**
> ```
> S(N) = 1 / (s + p/N) = 1 / (s + (1-s)/N)
>
> 13.33 = 1 / (s + (1-s)/20)
>
> s + (1-s)/20 = 1/13.33 = 0.075
>
> 20s + (1-s) = 20 * 0.075 = 1.5
>
> 20s + 1 - s = 1.5
>
> 19s = 0.5
>
> s = 0.5/19 ≈ 0.0263 (approximately 2.6%)
> ```
>
> **(d) Maximum speedup:**
> ```
> S_max = 1/s = 1/0.0263 ≈ 38.0
> ```

---

**Q13.** A developer claims that by re-engineering 80% of a program's serial code, they will reduce the serial fraction from 20% to 4%. Using Amdahl's Law, calculate the maximum speedup before and after the re-engineering effort.

> **Model Answer:**
>
> **Before re-engineering (`s = 0.20`):**
> ```
> S_max = 1/0.20 = 5x
> ```
>
> **After re-engineering (`s = 0.04`):**
> ```
> S_max = 1/0.04 = 25x
> ```
>
> **Conclusion:** Reducing the serial fraction from 20% to 4% (a 5x reduction in serial code) increases the theoretical maximum speedup from 5x to 25x — a 5x improvement in ceiling. This demonstrates that even small reductions in the serial fraction yield large gains in scalability.

---

**Q14.** Amdahl's Law with overhead. A program has serial fraction `s = 0.02`. It runs 8 parallel regions and each introduces a fixed overhead of `v = 0.001 * T_0`. Using the extended Amdahl formula `S(N) = 1 / (s + p/N + V/T_0)`, calculate the speedup on 32 processors.

> **Model Answer:**
>
> Given: `s = 0.02`, `p = 0.98`, `N = 32`, `n_p = 8` parallel regions, `v = 0.001 * T_0` per region.
>
> Total overhead: `V = n_p * v = 8 * 0.001 * T_0 = 0.008 * T_0`
>
> So `V/T_0 = 0.008`
>
> ```
> S(32) = 1 / (s + p/N + V/T_0)
>        = 1 / (0.02 + 0.98/32 + 0.008)
>        = 1 / (0.02 + 0.030625 + 0.008)
>        = 1 / 0.058625
>        ≈ 17.06
> ```
>
> Without overhead (basic Amdahl): `S(32) = 1/(0.02 + 0.030625) = 1/0.050625 ≈ 19.75`
>
> The parallelisation overhead reduces the speedup from ~19.75 to ~17.06 on 32 processors.

---

## Section C: Gustafson's Law and Weak Scaling

**Q15.** State Gustafson's Law. Derive the expression for scaled speedup `S(N) = s + pN`, defining all terms. Why is this considered a more optimistic view of parallel scaling than Amdahl's Law?

> **Model Answer:**
>
> **Derivation:**
> Assume that on `N` processors the total parallel wall-clock time is normalised to 1:
> ```
> T_N = s + p = 1
> ```
> where `s` is the sequential fraction of the *parallel* runtime and `p` is the parallel fraction.
>
> If the same (larger) workload were run on a single processor, the parallel part would take `N` times longer:
> ```
> T_0 = s + p*N
> ```
>
> Speedup is then:
> ```
> S(N) = T_0 / T_N = (s + pN) / 1 = s + pN
> ```
>
> **Why more optimistic than Amdahl:**
> Amdahl fixes the total problem size, so as `N` grows, the work-per-processor shrinks and the serial floor dominates. Gustafson instead argues that practitioners use more processors to tackle *larger* problems. The serial portion `s` is roughly constant in absolute time while the parallel work grows linearly. Speedup therefore scales linearly with `N` with no ceiling (beyond practical communication limits).

---

**Q16.** A parallel program is observed to spend 3% of its parallel runtime on serial tasks (`s = 0.03`) when run on 64 processors. Calculate the Gustafson scaled speedup.

> **Model Answer:**
>
> Given: `s = 0.03`, `p = 1 - 0.03 = 0.97`, `N = 64`
>
> ```
> S(64) = s + pN
>        = 0.03 + 0.97 * 64
>        = 0.03 + 62.08
>        = 62.11
> ```
>
> The scaled speedup is **62.11**, very close to the ideal 64. Parallel efficiency under Gustafson's model: `E = 62.11 / 64 ≈ 0.971 (97.1%)`.

---

**Q17.** A CFD simulation runs a test case with 1 million grid cells per processor. On 1 processor it takes 200 seconds. On 64 processors (64 million total cells), it takes 202 seconds.
- (a) Is this a strong scaling or weak scaling experiment? Justify.
- (b) Calculate the parallel efficiency under the weak scaling definition.
- (c) What does this result imply about the program's scalability?

> **Model Answer:**
>
> **(a) Weak scaling:** The problem size per processor is held constant at 1 million cells; the total problem size grows from 1M to 64M cells as processors increase from 1 to 64. This matches the weak scaling definition.
>
> **(b) Weak scaling efficiency:**
> The ideal weak scaling result is that `T_N = T_1` (constant wall-clock time). Efficiency is defined as:
> ```
> E_weak(N) = T_1 / T_N = 200 / 202 ≈ 0.990 (99.0%)
> ```
>
> **(c) Implication:** An efficiency of 99% is excellent. The 2-second increase (1% overhead) as the system scales from 1 to 64 processors suggests the communication overhead and synchronisation costs are very small relative to computation. The program scales near-ideally for weak scaling, making it suitable for running on very large machines with proportionally large datasets.

---

**Q18.** Compare and contrast what happens to parallel efficiency in a strong scaling experiment versus a weak scaling experiment as `N` increases. Use equations where appropriate.

> **Model Answer:**
>
> **Strong Scaling (Amdahl):**
> ```
> E_strong(N) = S(N)/N = 1 / (N * (s + p/N)) = 1 / (Ns + p)
> ```
> As `N` increases, `Ns` grows while `p` remains fixed. Therefore `E_strong(N)` **decreases** monotonically toward 0. Even a tiny serial fraction eventually dominates.
>
> **Weak Scaling (Gustafson):**
> ```
> E_weak(N) = S(N)/N = (s + pN)/N = s/N + p
> ```
> As `N` increases, `s/N -> 0`, so `E_weak(N) -> p`. In the ideal case where `s` is negligibly small, efficiency approaches 1.0 and **remains near-constant**. In practice, communication overhead grows with cluster size, causing slight degradation.
>
> **Summary:** Strong scaling efficiency always degrades; weak scaling efficiency can remain near-constant, which is why weak scaling is the preferred test for large HPC systems designed to tackle growing problem sizes.

---

## Section D: Network Topologies and Communication Modelling

**Q19.** The transmission time for an MPI message is modelled as `t = L + M/B`.
- (a) Define each term with typical units.
- (b) A cluster has `L = 2 µs` and `B = 10 GB/s`. Calculate the time to transmit a 50 MB message and a 100-byte message.
- (c) For each case, identify which term dominates and explain the implication for MPI programming style.

> **Model Answer:**
>
> **(a) Definitions:**
> - `L` = Latency — fixed startup/setup cost to initiate a transfer. Typical units: microseconds (µs).
> - `M` = Message size — number of bytes transmitted. Units: bytes (B), kilobytes (KB), megabytes (MB).
> - `B` = Bandwidth — data transfer rate. Units: bytes per second (GB/s, MB/s).
>
> **(b) Calculations:**
>
> Converting: `L = 2 µs = 2e-6 s`, `B = 10 GB/s = 10e9 B/s`
>
> **50 MB message (`M = 50e6 bytes`):**
> ```
> t = L + M/B
>   = 2e-6 + (50e6 / 10e9)
>   = 2e-6 + 5e-3
>   = 0.000002 + 0.005
>   ≈ 5.002 ms
> ```
>
> **100-byte message (`M = 100 bytes`):**
> ```
> t = L + M/B
>   = 2e-6 + (100 / 10e9)
>   = 2e-6 + 1e-8
>   = 0.000002 + 0.00000001
>   ≈ 2.01 µs
> ```
>
> **(c) Dominance and implications:**
> - **50 MB:** Bandwidth term (5 ms) >> Latency term (0.002 ms). **Bandwidth-dominated.** Implication: to improve performance, increase network bandwidth or reduce message count by aggregating data.
> - **100 bytes:** Latency term (2 µs) >> Bandwidth term (0.01 µs). **Latency-dominated.** Implication: the bottleneck is the fixed startup cost. Sending many small messages is expensive. MPI programming should batch small messages or use non-blocking communication to overlap latency with computation.

---

**Q20.** Describe the fat-tree network topology used in HPC clusters. In your answer, explain:
- (a) The physical structure and the role of leaf switches vs. core switches.
- (b) What a "blocking factor" of 2:1 means.
- (c) The implication of a 2:1 blocking factor for application performance.

> **Model Answer:**
>
> **(a) Structure:**
> A fat-tree is a hierarchical network arranged like an upside-down tree. **Compute nodes** (leaves) connect to **leaf (edge) switches**. Leaf switches connect upward to **aggregation switches**, which connect to **core (root) switches**. The defining feature is that the link bandwidth **increases (gets "fatter") towards the top** of the tree to avoid bottlenecks when traffic from many leaf nodes converges.
>
> **(b) 2:1 blocking factor:**
> A 2:1 blocking factor means that the **uplink bandwidth leaving a switch is half the downlink bandwidth** entering it. For example, if 16 compute nodes connect to a leaf switch with a combined downlink bandwidth of 320 Gb/s, the uplink to the aggregation layer may only be 160 Gb/s. Up to 2 nodes must share each unit of uplink bandwidth.
>
> **(c) Performance implication:**
> Communication between nodes on the **same leaf switch** is non-blocking (full bandwidth available internally). Communication between nodes on **different switches** — particularly across racks — is limited by the uplink bandwidth. Applications with heavy cross-rack communication (e.g., global all-reduce in distributed training, MPI collective operations) will see lower effective bandwidth and higher latency compared to applications where most traffic is local. Benchmarks or placement strategies that co-locate communicating processes on the same switch improve performance.

---

**Q21.** Compare the ring, 2D torus/mesh, and fat-tree topologies across the following properties: diameter, bisection bandwidth, and typical use case. Present your answer as a table.

> **Model Answer:**
>
> For a network of `P` nodes:
>
> | Property | Ring | 2D Mesh (sqrt(P) x sqrt(P)) | 2D Torus | Fat Tree |
> |---|---|---|---|---|
> | **Diameter** | P/2 | 2*(sqrt(P) - 1) | sqrt(P) - 1 (wrap-around) | 2*log_k(P) |
> | **Bisection BW** | 2 links | sqrt(P) links | 2*sqrt(P) links | Scales with P (design-dependent) |
> | **Node degree** | 2 | 2-4 (corner vs. interior) | 4 (uniform) | switch-dependent |
> | **Cost** | Low | Medium | Medium | High |
> | **Use case** | Small rings, token-ring protocols | Early parallel machines, 3D stencil codes | Tightly coupled stencil computations | General-purpose HPC clusters (InfiniBand) |
>
> Key insight: The fat-tree offers the best bisection bandwidth for a general workload but is expensive. Torus/mesh topologies exploit spatial locality in stencil codes (halo exchange goes to nearest neighbours). The ring has a very low bisection bandwidth (only 2 links regardless of P), making it poorly suited for large-scale all-to-all communication.

---

## Section E: Multi-Part Exam Questions

**Q22 [Multi-part].** A weather simulation code is profiled and found to have a serial fraction of `s = 0.10` and a parallelisable fraction of `p = 0.90`. The code uses domain decomposition on a 3D grid.

**(a)** Using Amdahl's Law, calculate the maximum speedup achievable regardless of processor count. [2 marks]

**(b)** Calculate the speedup and parallel efficiency when 32 processors are used. [3 marks]

**(c)** A new version of the code increases the parallelisable fraction to `p = 0.98` by re-writing the I/O routines. What is the new maximum speedup? [2 marks]

**(d)** For the 3D domain decomposition, if the full domain is `128 x 128 x 128` cells and it is decomposed across 64 processors, each sub-domain is `32 x 32 x 32`. Write expressions for computation and communication (halo) volume per sub-domain and compute the communication-to-computation ratio. [3 marks]

**(e)** Explain how the ratio computed in (d) changes as the number of processors doubles to 128, and what effect this has on performance. [2 marks]

> **Model Answer:**
>
> **(a) Maximum speedup (`s = 0.10`):**
> ```
> S_max = 1/s = 1/0.10 = 10x
> ```
> [2 marks]
>
> **(b) N = 32 processors:**
> ```
> S(32) = 1 / (s + p/N) = 1 / (0.10 + 0.90/32)
>        = 1 / (0.10 + 0.028125)
>        = 1 / 0.128125
>        ≈ 7.80
>
> E(32) = S(32)/32 = 7.80/32 ≈ 0.244 (24.4%)
> ```
> [3 marks: 1 for correct formula, 1 for S, 1 for E]
>
> **(c) New maximum speedup (`s = 0.02`):**
> ```
> S_max = 1/0.02 = 50x
> ```
> [2 marks]
>
> **(d) Communication-to-computation ratio for 32 x 32 x 32 sub-domain:**
> ```
> Computation ∝ Volume = 32^3 = 32768 cells
> Communication ∝ Surface area = 6 * 32^2 = 6 * 1024 = 6144 cells
>
> Ratio = Communication / Computation = 6144 / 32768 = 6/32 = 3/16 ≈ 0.1875
>
> General expression: 6N^2 / N^3 = 6/N (here N=32, ratio = 6/32)
> ```
> [3 marks: 1 for volume expression, 1 for surface expression, 1 for ratio]
>
> **(e) Effect of doubling to 128 processors:**
> With 128 processors the total domain `128^3` is divided into 128 sub-domains. Each sub-domain is `128^3 / 128 = 16384` cells. If arranged as a cube: `N_sub = 128/128^(1/3)` — more precisely each linear dimension is `128 / 128^(1/3) ≈ 128/5.04 ≈ 25.4`. For a cleaner analysis: sub-domain linear size halves from 32 to ~22 (factor `2^(1/3)`).
>
> Using the general formula `6/N` with `N` halved (approximately): ratio doubles. More communication is required relative to computation. This increased communication overhead means:
> - Processors spend a greater fraction of time waiting for halo data.
> - Network latency and bandwidth become more significant bottlenecks.
> - Parallel efficiency degrades beyond what Amdahl's Law alone predicts, because the communication overhead is not captured in the simple serial fraction model.
> [2 marks: 1 for ratio increases, 1 for performance consequence]

---

**Q23 [Multi-part].** A student runs a strong scaling benchmark on a cluster and collects the following data:

| Processors (N) | Wall-clock time (s) |
|---|---|
| 1 | 3200 |
| 4 | 900 |
| 16 | 280 |
| 64 | 120 |

**(a)** Calculate the speedup S(N) and efficiency E(N) for each row. [3 marks]

**(b)** Using the data points for N=4 and N=64, estimate the serial fraction `s` using Amdahl's Law for each and comment on whether they agree. [4 marks]

**(c)** The efficiency at N=64 is notably lower than at N=16. Suggest two reasons beyond Amdahl's Law that could explain this degradation. [2 marks]

**(d)** A colleague argues the program would benefit more from weak scaling. Explain this argument in the context of your results. [2 marks]

> **Model Answer:**
>
> **(a) Speedup and efficiency table:**
>
> | N | T(N) (s) | S(N) = 3200/T(N) | E(N) = S(N)/N |
> |---|---|---|---|
> | 1 | 3200 | 1.00 | 1.000 (100%) |
> | 4 | 900 | 3.56 | 0.889 (88.9%) |
> | 16 | 280 | 11.43 | 0.714 (71.4%) |
> | 64 | 120 | 26.67 | 0.417 (41.7%) |
>
> [3 marks: award marks for correct S and E at each row, 0.5 per correct row pair]
>
> **(b) Estimating serial fraction `s`:**
>
> Using `S(N) = 1/(s + (1-s)/N)` => `1/S(N) = s + (1-s)/N`
>
> **From N=4, S=3.56:**
> ```
> 1/3.56 = s + (1-s)/4
> 0.2809 = s + 0.25 - 0.25s
> 0.2809 = 0.75s + 0.25
> 0.0309 = 0.75s
> s ≈ 0.041 (4.1%)
> ```
>
> **From N=64, S=26.67:**
> ```
> 1/26.67 = s + (1-s)/64
> 0.03750 = s + 0.015625 - 0.015625s
> 0.03750 = 0.984375s + 0.015625
> 0.02188 = 0.984375s
> s ≈ 0.0222 (2.2%)
> ```
>
> The estimates differ (4.1% vs 2.2%), suggesting the simple Amdahl model does not perfectly fit the data. The discrepancy likely arises because Amdahl's Law does not account for communication overhead, which grows with N and is already felt at N=64 but not as strongly at N=4. [4 marks: 1.5 for each calculation, 1 for commentary]
>
> **(c) Two reasons for degradation beyond Amdahl:**
> 1. **Communication overhead (Latency/Waiting):** At 64 processors, inter-node communication (e.g., halo exchange, MPI collectives) becomes a larger fraction of runtime. The alpha-beta model `t = L + M/B` shows that even small messages incur fixed latency `L` per exchange, and with 64 nodes there are far more boundary exchanges.
> 2. **Load imbalance (Starvation):** At 64 processors, any unevenness in work distribution — arising from irregular grid regions, OS jitter, or imperfect decomposition — causes faster processors to stall at barriers while waiting for the slowest.
> [1 mark each for any two valid SLOW-category reasons]
>
> **(d) Argument for weak scaling:**
> The strong scaling results show efficiency collapsing from 89% at N=4 to 42% at N=64. If the problem size is fixed, the program cannot scale efficiently beyond ~30 processors (given `S_max ≈ 1/0.03 ~ 33`). However, if a larger problem is available (a real operational weather model, for example), weak scaling allows each processor to retain the same sub-domain size as N grows. Efficiency under weak scaling can remain near-constant, meaning the cluster is useful for solving problems 64x larger in the same wall-clock time, even if it cannot solve the same problem 64x faster. [2 marks: 1 for explaining the efficiency ceiling, 1 for the weak-scaling benefit]

---

**Q24 [Multi-part].** A shared-memory parallel loop is implemented in OpenMP as follows:

```c
#pragma omp parallel for schedule(static, 1)
for (int i = 0; i < 100; i++) {
    work[i] = expensive_compute(i);  // work[i] takes (i+1) milliseconds
}
```

The loop contains 100 iterations. Iteration `i` takes exactly `(i+1)` ms (so iteration 0 takes 1 ms, iteration 99 takes 100 ms).

**(a)** If there are 4 threads and `schedule(static, 1)` is used, list which iterations each thread receives and calculate the total runtime (time of the slowest thread). [3 marks]

**(b)** Repeat with `schedule(static, 25)` (chunk of 25 consecutive iterations). Which thread is slowest? [2 marks]

**(c)** Explain qualitatively how `schedule(dynamic, 1)` would differ and why it would produce better load balance. [2 marks]

**(d)** The implicit barrier after the loop is removed with `nowait`. A subsequent loop immediately reads from `work[]`. Is this safe? Justify. [2 marks]

> **Model Answer:**
>
> **(a) `schedule(static, 1)` — round-robin assignment:**
>
> With chunk size 1, iterations are assigned cyclically: thread 0 gets {0, 4, 8, ..., 96}, thread 1 gets {1, 5, 9, ..., 97}, etc.
>
> Thread 0 iterations: 0, 4, 8, ..., 96 (iterations 0,4,8,...,96; 25 iterations)
> ```
> Time(T0) = sum of (i+1) for i in {0,4,8,...,96}
>           = 1+5+9+...+97
>           = 25 * (1+97)/2 = 25 * 49 = 1225 ms
> ```
>
> Thread 1 iterations: 1, 5, 9, ..., 97
> ```
> Time(T1) = 2+6+10+...+98 = 25 * (2+98)/2 = 25 * 50 = 1250 ms
> ```
>
> Thread 2: 3+7+11+...+99 = 25*(3+99)/2 = 25*51 = 1275 ms
>
> Thread 3: 4+8+12+...+100 — wait: thread 3 gets {3,7,...,99}:
> ```
> Time(T3) = 4+8+...+100 = 25*(4+100)/2 = 25*52 = 1300 ms
> ```
>
> **Runtime = max(1225, 1250, 1275, 1300) = 1300 ms** (Thread 3 is slowest).
> Note: Static round-robin distributes work fairly evenly here (range 1225–1300 ms). [3 marks]
>
> **(b) `schedule(static, 25)` — chunks of 25 consecutive iterations:**
>
> Thread 0: iterations 0–24, time = sum(1..25) = 25*26/2 = 325 ms
> Thread 1: iterations 25–49, time = sum(26..50) = 25*38 = ... = (26+50)*25/2 = 950 ms
> Thread 2: iterations 50–74, time = sum(51..75) = (51+75)*25/2 = 126*25/2 = 1575 ms
> Thread 3: iterations 75–99, time = sum(76..100) = (76+100)*25/2 = 2200 ms
>
> **Runtime = 2200 ms.** Thread 3 is by far the slowest. This is much worse than `static,1` because the high-cost iterations (near i=99) are all packed onto thread 3. [2 marks: 1 for identifying thread 3, 1 for correct reasoning]
>
> **(c) `schedule(dynamic, 1)` behaviour:**
> With dynamic scheduling and chunk size 1, each thread requests the next available iteration only when it finishes its current one. Since later iterations are slower, threads that finish early iterations quickly will pick up more total iterations, while the thread handling iteration 99 (100 ms) will naturally handle fewer iterations overall. The runtime approaches the ideal of `total_work / N_threads = 5050/4 ≈ 1263 ms`. This is better load balance than static scheduling, at the cost of higher runtime overhead from repeated scheduler calls. [2 marks]
>
> **(d) Safety of `nowait` before a read of `work[]`:**
> **Not safe.** Removing the implicit barrier with `nowait` allows threads that have finished their iterations to proceed to the next loop before all threads have written to `work[]`. If the next loop reads `work[i]` for values of `i` that a still-running thread has not yet computed and written, a **data race** occurs: the reading thread may observe stale, uninitialised, or partially-written values. The implicit barrier is required here to guarantee that all writes to `work[]` are complete before any reads begin. [2 marks: 1 for "not safe", 1 for correct race condition explanation]

---

**Q25 [Multi-part].** Consider an MPI program that decomposes a 1D array of 1,000,000 elements across `N` processes. Each process must exchange boundary elements (halos) with its neighbours before each time step. Assume `L = 1 µs`, `B = 5 GB/s`, and each element is a 64-bit double (8 bytes). Each process sends 1 halo element to each neighbour (2 neighbours).

**(a)** Calculate the time to send one halo element to one neighbour using the alpha-beta model. [2 marks]

**(b)** If the computation per time step is proportional to the number of elements per process, and 1,000,000 elements takes 50 ms to compute, calculate the computation time and the communication-to-computation ratio for N=10 and N=100. [4 marks]

**(c)** At what approximate value of N does communication time equal computation time, and what does this imply? [3 marks]

> **Model Answer:**
>
> **(a) Time to send 1 halo element (8 bytes):**
> ```
> t = L + M/B
>   = 1e-6 + 8 / (5e9)
>   = 1e-6 + 1.6e-9
>   = 1.0000016e-6 s
>   ≈ 1.0 µs
> ```
> The bandwidth term (1.6 ns) is negligible for a single double — this is entirely **latency-dominated**. [2 marks]
>
> **(b) Computation and ratio for N=10 and N=100:**
>
> Computation time scales as `T_comp(N) = 50 ms / N` (problem splits evenly).
>
> Communication time per time step = 2 neighbours * `t_halo` = 2 * 1.0 µs = 2.0 µs (constant regardless of N for 1 element per side).
>
> **N=10:**
> ```
> T_comp(10) = 50/10 = 5.0 ms = 5000 µs
> T_comm(10) = 2.0 µs
> Ratio = 2.0 / 5000 = 0.0004 (0.04%)
> ```
>
> **N=100:**
> ```
> T_comp(100) = 50/100 = 0.5 ms = 500 µs
> T_comm(100) = 2.0 µs
> Ratio = 2.0 / 500 = 0.004 (0.4%)
> ```
>
> [4 marks: 1 per correct computation time, 1 per correct ratio]
>
> **(c) When does communication time equal computation time?**
>
> Set `T_comm = T_comp`:
> ```
> 2.0 µs = 50,000 µs / N
> N = 50,000 / 2.0 = 25,000
> ```
>
> At approximately **N = 25,000 processors**, the halo communication time equals the computation time per step. Beyond this point, communication overhead dominates and adding more processors will degrade rather than improve performance (adding processors reduces computation but cannot reduce the fixed latency of halo exchanges). In practice this limit would be reached much sooner once multi-hop network latency, contention, and collective communication costs are included. [3 marks: 1 for setting up equation, 1 for correct N, 1 for interpretation]

---

## Section F: True/False with Justification

**Q26.** State whether each claim is TRUE or FALSE and give a one-sentence justification.

**(a)** Amdahl's Law predicts that a program with no serial fraction (`s = 0`) achieves infinite speedup on infinite processors.

**(b)** Under Gustafson's Law, parallel efficiency can remain near 1.0 as N grows to infinity.

**(c)** Removing an implicit OpenMP barrier with `nowait` always improves performance.

**(d)** In a fat-tree network with a 2:1 blocking factor, communication between two nodes on the same leaf switch is limited by the uplink bottleneck.

**(e)** Super-linear speedup can never occur in a real system because it violates conservation of computation.

**(f)** For a 3D domain decomposition, the communication-to-computation ratio is proportional to `1/N` where `N` is the linear dimension of the sub-domain.

> **Model Answer:**
>
> **(a) TRUE.** With `s = 0`, `S_max = 1/0 = ∞`. If no part of the program is serial, the speedup grows without bound as processors are added.
>
> **(b) TRUE (approximately).** Under Gustafson's model `E(N) = s/N + p`. As `N -> ∞`, `s/N -> 0` and `E -> p ≈ 1` if `p` is close to 1. In practice, increasing network overhead prevents perfect efficiency.
>
> **(c) FALSE.** `nowait` can improve performance when threads do not have data dependencies across the barrier, but it introduces data races if subsequent code reads data written by the nowait loop. Unsafe use of `nowait` produces incorrect results.
>
> **(d) FALSE.** Communication within the same leaf switch uses the **internal switch fabric** (non-blocking at full bandwidth). The uplink bottleneck only affects traffic that must leave the switch to reach nodes on other switches.
>
> **(e) FALSE.** Super-linear speedup does occur in real systems, most commonly due to cache effects. When sub-domains shrink enough to fit in fast cache, the effective computation rate increases beyond what work-division alone would predict, resulting in `S(N) > N`.
>
> **(f) TRUE.** For a sub-domain of linear dimension `N`: computation `∝ N^3` (volume) and communication `∝ 6N^2` (surface area), giving ratio `6N^2/N^3 = 6/N ∝ 1/N`.

---

*End of Week 7 Practice Questions*

---
**Related wiki pages:**
- [Parallel Scaling](../wiki/concepts/Parallel_Scaling.md)
- [Load Balancing and Scheduling](../wiki/concepts/Load_Balancing_and_Scheduling.md)
- [Barriers and Synchronization](../wiki/concepts/Barriers_and_Synchronization.md)
- [Interconnects and Network Topologies](../wiki/concepts/Interconnects_and_Network_Topologies.md)
- [Domain Decomposition Overheads](../wiki/concepts/Domain_Decomposition_Overheads.md)
- [Strong vs Weak Scaling (comparison)](../wiki/comparisons/Strong_vs_Weak_Scaling.md)
- [Week 7 Summary](../wiki/summaries/Week_7_Summary.md)
