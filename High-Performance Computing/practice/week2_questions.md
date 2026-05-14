---
title: "Week 2 Practice Questions: Introduction to OpenMP"
tags: [hpc, week-2, openmp, practice]
date: 2026-05-14
---

# Week 2 Practice Questions: Introduction to OpenMP

**Covers:** Fork-join model, `#pragma omp parallel`, `#pragma omp for`, `num_threads`, variable scoping (`shared`, `private`, `firstprivate`, `lastprivate`, `reduction`, `default(none)`), data races, loop-carried dependencies (flow/anti/output), `critical` and `atomic`, `schedule` clause (static/dynamic/guided), implicit and explicit barriers, `nowait`.

**Source pages:** [OpenMP](../wiki/concepts/OpenMP.md) · [Parallel Loops](../wiki/concepts/Parallel_Loops_OpenMP.md) · [Variable Scoping](../wiki/concepts/Variable_Scoping_OpenMP.md) · [Data Dependencies](../wiki/concepts/Data_Dependencies.md) · [Barriers and Synchronization](../wiki/concepts/Barriers_and_Synchronization.md) · [Load Balancing and Scheduling](../wiki/concepts/Load_Balancing_and_Scheduling.md)

---

## Section A: Short Answer / Definition

### Q1. Define OpenMP and state the programming model it implements. (3 marks)

> **Model Answer**
>
> OpenMP (Open Multi-Processing) is an open standard API for **shared-memory parallel programming** in C, C++, and Fortran. It provides three extensions to the base language:
> 1. **Compiler directives** (`#pragma omp ...`) — instruct the compiler where to introduce parallelism.
> 2. **Runtime library routines** (e.g. `omp_get_thread_num()`) — enabled by including `<omp.h>`.
> 3. **Environment variables** (e.g. `OMP_NUM_THREADS`) — control runtime behaviour without recompiling.
>
> The execution model is **fork-join**: a single master thread forks a team of worker threads at a parallel region; all threads execute the region concurrently; threads rejoin (synchronise and terminate) at the region's end.
>
> **Marking points (1 mark each):** correct definition of shared-memory only / three component types named / fork-join model described.

---

### Q2. What is the `OMP_NUM_THREADS` environment variable and how does it interact with the `num_threads` clause? (2 marks)

> **Model Answer**
>
> `OMP_NUM_THREADS` is an environment variable that sets the **default number of threads** spawned when a parallel region is entered. It is consulted if no `num_threads(n)` clause is present on a `#pragma omp parallel` directive.
>
> The `num_threads(n)` **clause takes precedence** over `OMP_NUM_THREADS` for that specific parallel region. For example:
> ```c
> // This spawns exactly 4 threads regardless of OMP_NUM_THREADS
> #pragma omp parallel num_threads(4)
> { ... }
> ```
>
> **Marking points:** environment variable explained (1) / clause overrides it for that region (1).

---

### Q3. State the default scoping rule for variables declared outside a parallel region in OpenMP. Give one exception to this rule. (2 marks)

> **Model Answer**
>
> **Default rule:** Variables declared *outside* a parallel region are `shared` — all threads access the same memory location.
>
> **Exception:** The **loop iteration variable** (e.g. `i` in `for (int i = 0; ...)`) of a `#pragma omp for` construct is implicitly made `private` to each thread, even though it is declared outside the loop body. This is necessary to prevent threads from overwriting each other's loop counter.
>
> **Marking points:** shared by default (1) / loop iterator implicitly private (1).

---

### Q4. Explain the difference between `private` and `firstprivate`. When would you use `firstprivate` instead of `private`? (3 marks)

> **Model Answer**
>
> | Clause | Thread receives | Initial value |
> |---|---|---|
> | `private(x)` | Own copy of `x` | **Uninitialized** (garbage) |
> | `firstprivate(x)` | Own copy of `x` | **Initialized to x's value at region entry** |
>
> `firstprivate` is used when the computation inside the parallel region needs to **read the original value of the variable** as a starting point, but must not share writes back to the original. A common use case is OpenMP *tasks*: because a task may be scheduled long after the creating thread has moved on, if the loop variable `i` is merely `private`, its captured value may already have changed. `firstprivate(i)` captures the value at task-creation time.
>
> **Marking points:** private is uninitialized (1) / firstprivate copies the entry value (1) / valid use-case given, e.g. tasks or read-then-compute pattern (1).

---

### Q5. Define `lastprivate`. What category of loop-carried dependency does it resolve? (2 marks)

> **Model Answer**
>
> `lastprivate(x)` gives each thread a private, uninitialized copy of `x` during the parallel region, but **after the region ends** it writes back the value that `x` held during the **sequentially last loop iteration** into the original (master thread's) variable.
>
> It resolves an **output dependency (write-after-write)** where multiple iterations write to the same scalar variable and serial correctness requires the final state to reflect the last iteration's write.
>
> **Marking points:** correct description of the write-back mechanism (1) / output dependency identified (1).

---

### Q6. What is a data race? State the three conditions that must all hold for a data race to occur. (3 marks)

> **Model Answer**
>
> A data race is a non-deterministic bug in which the final value of a memory location depends on the unpredictable scheduling order of threads.
>
> Three necessary conditions:
> 1. Two or more threads **access the same memory location** simultaneously.
> 2. At least one of those accesses is a **write** operation.
> 3. There is **no synchronization mechanism** (no lock, atomic, or barrier) protecting the access.
>
> If all three conditions hold, the result is undefined. Removing *any one* condition eliminates the race.
>
> **Marking points:** 1 mark per condition correctly stated.

---

### Q7. Name and describe the three types of loop-carried dependency. For each, state whether the loop is directly parallelisable and how the dependency can be resolved. (6 marks)

> **Model Answer**
>
> | Type | Pattern | Parallelisable? | Resolution |
> |---|---|---|---|
> | **Flow (Read-after-Write)** | `a[i] = a[i-1] + 1` — iteration `i` reads a value *produced* by iteration `i-1`. | **No** — true dependency; the algorithm requires the chain of prior outputs. Writing to a new array gives the wrong answer (reads original, not propagated, values). | The algorithm itself must change (e.g. prefix-sum algorithms, wave-front parallelism). |
> | **Anti (Write-after-Read)** | `a[i] = a[i+1] * 2` — iteration `i` overwrites `a[i]`, which iteration `i-1` still needs to read as `a[i+1]`. | **Yes** — the dependency is caused by *reusing storage*, not by a true data relationship. | Allocate a new output array `b[]`, read from `a[]`, write to `b[]`. All threads can then read `a` simultaneously without conflict. |
> | **Output (Write-after-Write)** | Multiple iterations write to the **same scalar** variable. | **Yes** — use `lastprivate`. | Declare the variable `lastprivate(x)` so each thread has a private copy and the sequentially-last iteration's value is preserved after the region. |
>
> **Marking points:** 2 marks per dependency type (1 for correct description/pattern, 1 for correct resolution).

---

### Q8. List the four OpenMP constructs that carry an **implicit barrier** at their end. How can the barrier be suppressed, and when should you *not* suppress it? (3 marks)

> **Model Answer**
>
> Constructs with an implicit barrier at their end:
> 1. `#pragma omp parallel` (cannot be suppressed)
> 2. `#pragma omp for`
> 3. `#pragma omp single`
> 4. `#pragma omp sections`
>
> The barrier on constructs 2–4 is suppressed by adding the **`nowait`** clause (e.g. `#pragma omp for nowait`).
>
> You should **not** suppress a barrier when subsequent code in the same parallel region reads data that was written inside the construct — doing so creates a data race. `nowait` is safe only when the work that follows is completely independent of the loop's results.
>
> **Marking points:** four constructs listed (1) / `nowait` named and applied correctly (1) / valid reason not to suppress given (1).

---

## Section B: Code Analysis

### Q9. What does the following program print? Explain your reasoning. (4 marks)

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    int x = 10;

    #pragma omp parallel num_threads(4) private(x)
    {
        x = omp_get_thread_num() * 2;
        printf("Thread %d: x = %d\n", omp_get_thread_num(), x);
    }

    printf("After region: x = %d\n", x);
    return 0;
}
```

> **Model Answer**
>
> Inside the parallel region, `x` is **private** — each thread receives its own **uninitialized** copy of `x` (the initial value of 10 is *not* copied in; `private` does not inherit the outer value). Each thread then assigns `x = thread_id * 2` and prints it.
>
> Expected output (order of the first four lines may vary):
> ```
> Thread 0: x = 0
> Thread 1: x = 2
> Thread 2: x = 4
> Thread 3: x = 6
> After region: x = 10
> ```
>
> The last line prints **10** because: (a) private variables are discarded at region exit — they are not written back to the outer `x`; (b) the outer `x` was never modified.
>
> **Marking points:** correct per-thread output values explained (2) / outer `x` unchanged after region explained (1) / note that ordering of per-thread lines is non-deterministic (1).

---

### Q10. State whether each of the following loops can be safely parallelised with `#pragma omp parallel for`. Justify your answer by identifying any dependency. (2 marks each, 8 marks total)

**(a)**
```c
for (int i = 0; i < N; i++)
    a[i] = b[i] * 2.0;
```

**(b)**
```c
for (int i = 1; i < N; i++)
    a[i] = a[i-1] + c;
```

**(c)**
```c
for (int i = 0; i < N-1; i++)
    a[i] = a[i+1] - a[i];
```

**(d)**
```c
double result = 0.0;
for (int i = 0; i < N; i++)
    result += a[i];
```

> **Model Answer**
>
> **(a) Yes — safe to parallelise.**
> Each iteration reads `b[i]` and writes `a[i]`. No iteration reads or writes an element accessed by another. No dependency exists. Add `#pragma omp parallel for` directly.
>
> **(b) No — flow dependency (Read-after-Write).**
> Iteration `i` reads `a[i-1]`, which is *produced* by iteration `i-1`. In parallel, iteration 5 might execute before iteration 4 has updated `a[4]`, giving the wrong result. This is a true (flow) dependency and cannot be removed by changing storage.
>
> **(c) No — anti-dependency (Write-after-Read).**
> Iteration `i` writes `a[i]`, while iteration `i-1` needs to read `a[i]` (as its `a[i+1]`). In parallel, iteration `i` could overwrite `a[i]` before iteration `i-1` reads it. Fix: write results to a separate array `b[i] = a[i+1] - a[i]`, reading only the original `a`.
>
> **(d) Yes — but requires a `reduction` clause.**
> Multiple threads write to the shared `result` variable simultaneously — this creates a data race as written. It is parallelisable once scoped correctly:
> ```c
> #pragma omp parallel for reduction(+:result)
> for (int i = 0; i < N; i++)
>     result += a[i];
> ```
> Each thread accumulates privately; the runtime combines at the end.
>
> **Marking points (2 each):** correct yes/no (1) + correct dependency identification or fix (1).

---

### Q11. Trace through the following code. What is the value of `total` printed at the end, and why? (4 marks)

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    int total = 0;

    #pragma omp parallel for num_threads(4) shared(total)
    for (int i = 1; i <= 16; i++) {
        total += i;
    }

    printf("total = %d\n", total);
    return 0;
}
```

> **Model Answer**
>
> The **correct** answer should be `total = 136` (sum of 1..16 = 16*17/2 = 136). However, the code as written almost certainly does **not** print 136. It prints an **incorrect, non-deterministic value** that is typically less than 136.
>
> **Why:** `total` is declared `shared`, and the statement `total += i` is a **non-atomic read-modify-write** sequence: load `total`, add `i`, store back. When 4 threads execute this concurrently, two threads can both load the same stale value of `total`, independently add their `i`, and the later store overwrites the earlier one — losing one increment. This is a classic **data race**.
>
> **Fix:** Replace `shared(total)` with `reduction(+:total)`:
> ```c
> #pragma omp parallel for num_threads(4) reduction(+:total)
> for (int i = 1; i <= 16; i++) {
>     total += i;
> }
> ```
>
> **Marking points:** identifies non-deterministic/incorrect output (1) / data race explained (2) / correct fix given (1).

---

### Q12. What does the `#ifdef _OPENMP` preprocessor guard achieve? When would you use it? (2 marks)

```c
#ifdef _OPENMP
    int nthreads = omp_get_num_threads();
    printf("Running with %d threads\n", nthreads);
#else
    printf("Running serially\n");
#endif
```

> **Model Answer**
>
> The `_OPENMP` macro is **defined by the compiler when OpenMP is enabled** (e.g. via `-fopenmp` flag in GCC). The `#ifdef` guard allows the same source file to compile correctly whether or not OpenMP is available:
> - With `-fopenmp`: the `omp_get_num_threads()` call is valid and the OpenMP branch compiles.
> - Without `-fopenmp`: the compiler never sees the OpenMP library call, so it does not fail on an undefined symbol.
>
> Use it to protect calls to `<omp.h>` functions that have no serial equivalent, ensuring portability and serial correctness.
>
> **Marking points:** `_OPENMP` is defined by compiler when enabled (1) / enables single source to compile serially or with OpenMP (1).

---

## Section C: Code Writing

### Q13. Write an OpenMP parallel loop that computes the dot product of two arrays `a[]` and `b[]` of length N. Use `default(none)` and declare all clauses explicitly. (4 marks)

> **Model Answer**
>
> ```c
> #include <omp.h>
>
> double dot_product(double *a, double *b, int N) {
>     double dot = 0.0;
>
>     #pragma omp parallel for default(none) shared(a, b, N) reduction(+:dot)
>     for (int i = 0; i < N; i++) {
>         dot += a[i] * b[i];
>     }
>
>     return dot;
> }
> ```
>
> **Key marking points:**
> - `reduction(+:dot)` — avoids data race on the accumulator (2 marks; without this the answer is fundamentally wrong).
> - `default(none)` present and all variables accounted for: `shared(a, b, N)` (1 mark).
> - Loop structure and return value correct (1 mark).

---

### Q14. Write a complete OpenMP parallel region that uses `omp_get_thread_num()` and `omp_get_num_threads()` to print a line from each thread identifying itself and the total team size. Explain why the output order is non-deterministic. (3 marks)

> **Model Answer**
>
> ```c
> #include <stdio.h>
> #include <omp.h>
>
> int main(void) {
>     #pragma omp parallel
>     {
>         int tid  = omp_get_thread_num();
>         int nthr = omp_get_num_threads();
>         printf("Hello from thread %d of %d\n", tid, nthr);
>     }
>     return 0;
> }
> ```
>
> Output ordering is non-deterministic because `printf` calls from all threads execute **concurrently with no synchronization** between them. The OS scheduler may run threads in any order, and context-switches can occur between successive prints. The content of each line is correct, but the order varies between runs.
>
> **Marking points:** correct use of both runtime functions inside a parallel region (1) / correct code compiles and runs (1) / non-determinism explained (1).

---

### Q15. Write an OpenMP parallel loop to initialise an array `c[N]` where `c[i] = i * i`. Use `schedule(static, 16)`. Explain what `schedule(static, 16)` means in terms of how work is assigned to threads. (4 marks)

> **Model Answer**
>
> ```c
> #include <omp.h>
>
> void init_squares(int *c, int N) {
>     #pragma omp parallel for schedule(static, 16) shared(c) firstprivate(N)
>     for (int i = 0; i < N; i++) {
>         c[i] = i * i;
>     }
> }
> ```
>
> **What `schedule(static, 16)` means:**
> The N iterations are divided into contiguous **chunks of 16 iterations** and assigned to threads in a **round-robin** fashion at compile time (before execution begins). For example, with 4 threads and N = 64:
> - Thread 0: iterations 0–15, 48–63 ... (wrapped round-robin)
>
> Wait — static round-robin: Thread 0 gets chunk 0 (iters 0–15), Thread 1 gets chunk 1 (iters 16–31), Thread 2 gets chunk 2 (iters 32–47), Thread 3 gets chunk 3 (iters 48–63), then Thread 0 would get chunk 4 if N > 64, etc.
>
> Static scheduling has **low overhead** (assignment computed once) but gives **poor load balance** if iterations have unequal cost (this particular loop is uniform, so static is ideal here).
>
> **Marking points:** correct parallel for loop (1) / `schedule(static, 16)` clause correctly placed (1) / chunk-based round-robin assignment explained (1) / low overhead characteristic noted (1).

---

### Q16. Write an OpenMP parallel loop to find the **maximum value** in an array `a[N]`. Use a `reduction` clause. (3 marks)

> **Model Answer**
>
> ```c
> #include <omp.h>
> #include <float.h>   // for -DBL_MAX
>
> double find_max(double *a, int N) {
>     double max_val = -DBL_MAX;
>
>     #pragma omp parallel for reduction(max:max_val) shared(a) firstprivate(N)
>     for (int i = 0; i < N; i++) {
>         if (a[i] > max_val)
>             max_val = a[i];
>     }
>
>     return max_val;
> }
> ```
>
> The `reduction(max:max_val)` clause: each thread maintains a private `max_val` initialised to the identity element for `max` (effectively `-DBL_MAX`), updates it locally, then the runtime takes the maximum across all thread-local values.
>
> **Marking points:** `reduction(max:max_val)` correctly used (2) / correct loop logic (1).

---

### Q17. Write a parallel loop using `schedule(dynamic, 4)` to process a work array where each iteration `i` takes `i` units of time (i.e. workload is highly non-uniform). Explain why `dynamic` is the correct choice here over `static`. (4 marks)

> **Model Answer**
>
> ```c
> #include <omp.h>
> extern void process(int i);   // takes O(i) time
>
> void parallel_process(int N) {
>     #pragma omp parallel for schedule(dynamic, 4) firstprivate(N)
>     for (int i = 0; i < N; i++) {
>         process(i);
>     }
> }
> ```
>
> **Why dynamic over static:**
>
> `schedule(static)` divides iterations into equal-sized contiguous chunks assigned upfront. Here iteration `i = N-1` takes nearly N times longer than `i = 0`. If thread 0 gets the last chunk (high-index iterations), all other threads finish and sit **idle at the implicit barrier** while thread 0 finishes — this is *starvation*.
>
> `schedule(dynamic, 4)` assigns threads a chunk of 4 iterations **on demand at runtime**: when a thread finishes its chunk it immediately requests the next available chunk. This naturally balances load because idle threads are never waiting for one overloaded thread to finish a pre-assigned range. The cost is higher **scheduling overhead** (each chunk request requires a shared counter update), but for non-uniform work this is worthwhile.
>
> **Marking points:** correct dynamic schedule clause (1) / explanation of why static causes starvation for this workload (2) / dynamic overhead trade-off mentioned (1).

---

## Section D: Bug Identification and Fixing

### Q18. The following code intends to find the sum of all elements in array `a[N]` using OpenMP. It contains a bug. Identify the bug, explain why it produces incorrect results, and write a corrected version. (5 marks)

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    int N = 1000;
    double a[1000], sum = 0.0;

    for (int i = 0; i < N; i++) a[i] = (double)i;

    #pragma omp parallel for shared(sum, a, N)
    for (int i = 0; i < N; i++) {
        sum += a[i];
    }

    printf("Sum = %.1f\n", sum);
    return 0;
}
```

> **Model Answer**
>
> **Bug:** `sum` is declared `shared`, so all threads simultaneously read-modify-write the same memory location. The compound statement `sum += a[i]` is **not atomic**: it decomposes into load-add-store. Two threads can load the same stale `sum`, each add their `a[i]`, and the second store overwrites the first's addition — a **data race**. The result is non-deterministic and typically less than 499500.0 (the correct value: sum of 0..999 = 999*1000/2).
>
> **Corrected version:**
> ```c
> #pragma omp parallel for reduction(+:sum) shared(a) firstprivate(N)
> for (int i = 0; i < N; i++) {
>     sum += a[i];
> }
> ```
>
> `reduction(+:sum)` gives each thread a private copy of `sum` initialised to 0.0. Each thread accumulates its portion of `a[]` privately, then the runtime adds all private copies into the global `sum` atomically after the loop.
>
> **Marking points:** bug correctly named as data race (1) / explains read-modify-write is non-atomic (2) / corrected code with `reduction` (2).

---

### Q19. The following code has a scoping error. Identify the problem and fix it. (4 marks)

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    int N = 10;
    int tmp;

    #pragma omp parallel for shared(tmp, N)
    for (int i = 0; i < N; i++) {
        tmp = i * i;
        printf("i=%d, tmp=%d\n", i, tmp);
    }
    return 0;
}
```

> **Model Answer**
>
> **Problem:** `tmp` is declared `shared`. Every thread reads and writes the **same `tmp` variable**. Thread A may compute `tmp = i_A * i_A` and then be preempted; Thread B overwrites `tmp = i_B * i_B`; when Thread A resumes and prints, it reads Thread B's value. The printed pairs are non-deterministic and incorrect.
>
> **Fix:** Declare `tmp` as `private` so each thread has its own isolated copy:
>
> ```c
> #pragma omp parallel for private(tmp) firstprivate(N)
> for (int i = 0; i < N; i++) {
>     tmp = i * i;
>     printf("i=%d, tmp=%d\n", i, tmp);
> }
> ```
>
> Or alternatively, remove `tmp` entirely and compute inline:
> ```c
> #pragma omp parallel for firstprivate(N)
> for (int i = 0; i < N; i++) {
>     printf("i=%d, tmp=%d\n", i, i * i);
> }
> ```
>
> **Marking points:** identifies `shared(tmp)` as the error (1) / explains the race: multiple threads writing the same location (2) / correct fix with `private(tmp)` (1).

---

### Q20. The following loop is claimed to have an anti-dependency that prevents parallelisation. Is this claim correct? If so, explain why and show a fix. If not, explain why it is actually safe to parallelise. (4 marks)

```c
for (int i = 0; i < N-1; i++)
    b[i] = a[i+1] * 3.0;
```

> **Model Answer**
>
> **The claim is incorrect — this loop is safe to parallelise as written.**
>
> Analysis:
> - Each iteration reads `a[i+1]` — a read from `a`.
> - Each iteration writes `b[i]` — a write to `b`.
>
> Since `a` and `b` are **different arrays**, there is no write to any element that another iteration reads. There is no loop-carried dependency of any type. The compiler can safely distribute iterations across threads:
>
> ```c
> #pragma omp parallel for shared(a, b) firstprivate(N)
> for (int i = 0; i < N-1; i++)
>     b[i] = a[i+1] * 3.0;
> ```
>
> Anti-dependency *would* arise if `a` and `b` were the **same array**: `a[i] = a[i+1] * 3.0`. Then iteration `i` writes `a[i]`, which iteration `i-1` needs to read as `a[i]` (i.e. its `a[(i-1)+1]`). In that case, writing to a new output array restores independence.
>
> **Marking points:** correctly states the loop is safe (1) / explanation: writes to `b`, reads from separate `a` (2) / contrast with the problematic in-place version (1).

---

### Q21. Identify and fix all bugs in the following code, which is intended to compute in parallel the running maximum seen so far: `mx[i] = max(a[0], ..., a[i])`. (5 marks)

```c
#include <omp.h>
#include <stdio.h>

void running_max(double *a, double *mx, int N) {
    #pragma omp parallel for shared(mx, a, N)
    for (int i = 0; i < N; i++) {
        mx[i] = (i == 0) ? a[0] : (a[i] > mx[i-1] ? a[i] : mx[i-1]);
    }
}
```

> **Model Answer**
>
> **Bug 1 — Flow (Read-after-Write) dependency:**
> Iteration `i` reads `mx[i-1]`, which is *written* by iteration `i-1`. In parallel, iteration 5 may execute before iteration 4 has written `mx[4]`, giving a stale or garbage value. This is a **true dependency** — the algorithm inherently requires the previous result.
>
> **Bug 2 — The algorithm is fundamentally non-parallelisable as specified:**
> The running maximum is a **prefix operation** (scan). It cannot be computed element-by-element in parallel in a straightforward loop. No scoping change fixes a flow dependency.
>
> **Correct approach** — either:
> - Accept serial execution for this step:
>   ```c
>   // Serial: no parallelism possible for this formulation
>   for (int i = 0; i < N; i++)
>       mx[i] = (i == 0) ? a[0] : (a[i] > mx[i-1] ? a[i] : mx[i-1]);
>   ```
> - Or find the **global maximum** in parallel (a different but often sufficient result):
>   ```c
>   double global_max = a[0];
>   #pragma omp parallel for reduction(max:global_max) shared(a) firstprivate(N)
>   for (int i = 1; i < N; i++) {
>       if (a[i] > global_max) global_max = a[i];
>   }
>   // global_max now holds max(a[0..N-1])
>   ```
>
> **Marking points:** flow dependency identified (2) / explanation that no scoping fix resolves a flow dependency (1) / correct serial alternative shown (1) / correct parallel alternative (global max with reduction) shown (1).

---

## Section E: Multi-Part Exam Questions

### Q22. [Multi-part] OpenMP Execution Model and Variable Scoping (12 marks)

A researcher has the following serial C code:

```c
#include <stdio.h>
#include <math.h>

int main(void) {
    int N = 1000000;
    double *x = malloc(N * sizeof(double));
    double *y = malloc(N * sizeof(double));
    double norm = 0.0;
    int i;

    /* Initialise */
    for (i = 0; i < N; i++) {
        x[i] = (double)i / N;
        y[i] = (double)(N - i) / N;
    }

    /* Compute squared norm of x - y */
    for (i = 0; i < N; i++) {
        double diff = x[i] - y[i];
        norm += diff * diff;
    }
    norm = sqrt(norm);
    printf("norm = %f\n", norm);

    free(x); free(y);
    return 0;
}
```

#### (a) Describe the fork-join model and explain how it applies to an OpenMP parallel region. (3 marks)

> **Model Answer**
>
> The fork-join model has three phases:
> 1. **Fork:** The program begins as a single master thread executing sequentially. When a `#pragma omp parallel` directive is encountered, the master thread spawns (forks) a **team of worker threads**. The number of threads is controlled by `OMP_NUM_THREADS` or the `num_threads` clause.
> 2. **Parallel execution:** All threads in the team execute the body of the parallel region concurrently, sharing access to the program's heap and global memory.
> 3. **Join:** At the closing `}` of the parallel region there is an **implicit barrier** — all threads synchronize (wait for the slowest) and the worker threads terminate (join). The master thread then continues with sequential execution after the region.
>
> In OpenMP this means parallel work must be expressed within delimited regions; the programmer does not manage thread lifecycle directly.
>
> **Marking points:** fork description (1) / parallel execution description (1) / join/barrier description (1).

---

#### (b) Parallelise the initialisation loop using OpenMP. State which clauses you add and why each variable needs its particular scope. (4 marks)

> **Model Answer**
>
> ```c
> #pragma omp parallel for default(none) shared(x, y, N) private(i)
> for (i = 0; i < N; i++) {
>     x[i] = (double)i / N;
>     y[i] = (double)(N - i) / N;
> }
> ```
>
> | Variable | Scope | Reason |
> |---|---|---|
> | `x`, `y` | `shared` | Arrays allocated on the heap; each thread writes a different element — no conflict. |
> | `N` | `shared` | Read-only constant; safe for all threads to read the same value. |
> | `i` | `private` | Loop iterator — each thread must track its own iteration count independently. (Note: if declared as `int i` in the `for` initializer, it is automatically private.) |
>
> **Marking points:** correct directive (1) / `shared` arrays justified (1) / N shared justified (1) / i private justified (1).

---

#### (c) Parallelise the norm computation loop. Explain what would go wrong without your chosen clause and how the clause fixes it. (5 marks)

> **Model Answer**
>
> ```c
> #pragma omp parallel for default(none) shared(x, y, N) private(i) reduction(+:norm)
> for (i = 0; i < N; i++) {
>     double diff = x[i] - y[i];
>     norm += diff * diff;
> }
> ```
>
> Note: `diff` is declared *inside* the loop body, so it is automatically private.
>
> **Without `reduction(+:norm)`:** `norm` would be `shared` (by the `default(none)` rule, if omitted it would be a compile error; if written `shared(norm)` instead, we get a data race). The statement `norm += diff * diff` is a non-atomic read-modify-write. With multiple threads, two threads can simultaneously read the current `norm`, each add their partial contribution, and then both store back — the second store overwrites the first, losing one contribution. The result is incorrect and non-deterministic.
>
> **How `reduction(+:norm)` fixes it:**
> 1. Each thread receives a **private copy of `norm`** initialised to the identity element for `+` (i.e. 0.0).
> 2. Each thread accumulates into its private copy with no contention.
> 3. At the end of the loop, the OpenMP runtime **atomically combines** all private copies using the `+` operator into the original `norm` variable.
>
> **Marking points:** correct directive with reduction (1) / `diff` correctly handled (it is local/auto) (1) / data race explained without reduction (2) / mechanism of reduction explained (1).

---

### Q23. [Multi-part] Schedule Clause and Load Balancing (10 marks)

Consider a loop where the work per iteration increases linearly with `i`:

```c
for (int i = 0; i < 1000; i++) {
    expensive_work(i);   /* takes time proportional to i */
}
```

#### (a) Describe what `schedule(static)` (no chunk size) does with this loop on 4 threads. Draw a table showing which iterations each thread handles and explain whether load is balanced. (4 marks)

> **Model Answer**
>
> With no chunk size specified, `static` divides iterations into **4 equal contiguous blocks** (one per thread):
>
> | Thread | Iterations | Work proportional to |
> |---|---|---|
> | Thread 0 | 0 – 249 | sum(0..249) = 31 125 |
> | Thread 1 | 250 – 499 | sum(250..499) = 93 625 |
> | Thread 2 | 500 – 749 | sum(500..749) = 156 125 |
> | Thread 3 | 750 – 999 | sum(750..999) = 218 625 |
>
> **Load is severely imbalanced.** Thread 3's workload is approximately 7× that of Thread 0. Threads 0, 1, 2 finish and **idle at the implicit barrier** while Thread 3 completes, wasting almost 75% of potential parallel capacity for this loop.
>
> **Marking points:** correct iteration ranges (1) / recognition that contiguous blocks give increasing work per thread (1) / thread 3 is the bottleneck (1) / idle-at-barrier / starvation mentioned (1).

---

#### (b) Describe how `schedule(dynamic, 10)` distributes the same loop. Why does it produce better load balance? What is the cost? (3 marks)

> **Model Answer**
>
> `schedule(dynamic, 10)` does not pre-assign iterations. Instead:
> - A **shared work queue** holds all 100 chunks of 10 iterations.
> - Whenever a thread finishes its current chunk, it **requests the next available chunk** at runtime.
> - Faster threads (those assigned low-index iterations) finish quickly and immediately pick up more work.
>
> This balances load because **no thread sits idle while work remains**. In the example, Thread 0 can process many chunks of low-index iterations in the time Thread 3 processes one high-index chunk; threads self-schedule dynamically to equalise wall-clock time.
>
> **Cost:** Each chunk request requires updating a **shared atomic counter**, introducing higher **scheduling overhead** compared to static. If iterations are uniform in cost, this overhead is wasted. Use dynamic only for non-uniform workloads.
>
> **Marking points:** runtime demand-driven assignment explained (1) / load balance mechanism (threads pick up more low-cost work) (1) / overhead/trade-off stated (1).

---

#### (c) Describe `schedule(guided, 10)`. Why might it be preferred over `schedule(dynamic, 10)` for this particular loop? (3 marks)

> **Model Answer**
>
> `schedule(guided, 10)` is similar to dynamic but the chunk size is **not fixed** — it starts large and **shrinks exponentially** (roughly: remaining_iterations / nthreads) down to the minimum chunk size (here 10).
>
> **Early in the loop:** large chunks reduce scheduling overhead (fewer requests to the shared counter).
> **Later in the loop:** smaller chunks fine-tune load balance as remaining work is limited.
>
> For this particular loop (work ∝ i), the **high-cost iterations are at the end**, where guided's small chunks provide fine-grained rebalancing. The early large chunks are low-cost anyway, so the reduced overhead early on carries little risk of imbalance. Guided therefore offers a **better overhead/balance trade-off** than dynamic for this workload shape.
>
> **Marking points:** chunk size starts large and shrinks to minimum (1) / reduces overhead vs dynamic (1) / rationale applied to this specific non-uniform loop (1).

---

### Q24. [Multi-part] Critical Sections, Atomic, and Barrier (8 marks)

#### (a) Explain the difference between `#pragma omp critical` and `#pragma omp atomic`. When should each be used? (4 marks)

> **Model Answer**
>
> **`#pragma omp critical`**
> - Defines a **mutual exclusion region**: only one thread may execute the block at a time; all other threads block until it exits.
> - The block can contain **arbitrary statements** — any C/C++ code.
> - Example: updating a complex data structure (e.g. linked list insertion, histogram update).
> - **Higher overhead**: implemented via a lock; involves OS-level blocking when contended.
>
> ```c
> #pragma omp critical
> {
>     if (a[i] > max_val) max_val = a[i];
> }
> ```
>
> **`#pragma omp atomic`**
> - Applies to a **single, specific memory operation** on a scalar variable (read, write, update, or capture).
> - Implemented using a **hardware atomic instruction** (e.g. `LOCK ADD` on x86) — no explicit locking.
> - Only valid for a restricted set of operators (`+`, `-`, `*`, `/`, `&`, `|`, `^`, `<<`, `>>`).
> - **Lower overhead**: no blocking; uses hardware support.
>
> ```c
> #pragma omp atomic
> sum += a[i];
> ```
>
> **Rule of thumb:** use `atomic` for simple scalar updates; use `critical` when the protected code is complex or uses non-supported operators.
>
> **Marking points:** critical for arbitrary blocks / uses locking (1) / atomic for single scalar operation / uses hardware support (1) / overhead comparison (1) / clear use-case guidance (1).

---

#### (b) The following code uses `nowait`. Is this correct or does it introduce a bug? Justify your answer. (4 marks)

```c
double A[N], B[N], C[N];

#pragma omp parallel
{
    #pragma omp for nowait
    for (int i = 0; i < N; i++)
        A[i] = compute_A(i);

    #pragma omp for
    for (int i = 0; i < N; i++)
        C[i] = A[i] + B[i];
}
```

> **Model Answer**
>
> **This is a bug.** The `nowait` on the first loop means threads that finish computing their portion of `A` do **not** wait at the implicit barrier before entering the second loop. A fast thread might start computing `C[i] = A[i] + B[i]` for elements of `A` that a slower thread has **not yet written**.
>
> For example, suppose the first loop is split so Thread 0 handles `i = 0..N/2-1` and Thread 1 handles `i = N/2..N-1`. With `nowait`, Thread 0 finishes early and immediately starts the second loop. If Thread 0's second-loop iteration needs `A[N-1]` (which Thread 1 hasn't computed yet), it reads a **stale or garbage value**.
>
> **Fix:** Remove `nowait` from the first loop, restoring the implicit barrier so all threads have written their portion of `A` before any thread begins reading it:
>
> ```c
> #pragma omp for   /* barrier here ensures A is fully written */
> for (int i = 0; i < N; i++)
>     A[i] = compute_A(i);
>
> #pragma omp for
> for (int i = 0; i < N; i++)
>     C[i] = A[i] + B[i];
> ```
>
> **Marking points:** identifies it as a bug (1) / explains that A may not be fully written when second loop starts reading it (2) / correct fix shown (1).

---

### Q25. [Multi-part] OpenMP vs MPI and Architectural Constraints (6 marks)

An HPC cluster has 200 compute nodes, each node having 32 cores and 256 GB of RAM.

#### (a) A researcher wants to parallelise a simulation using OpenMP. What is the maximum number of threads they can use and why? (2 marks)

> **Model Answer**
>
> **Maximum: 32 threads.**
>
> OpenMP is a **shared-memory programming model** — all threads in a team must share the same address space. A single process on this cluster is confined to one compute node, which has 32 cores sharing one pool of RAM. OpenMP threads cannot cross the network to other nodes because there is no shared memory between nodes (each node's RAM is physically independent).
>
> **Marking points:** 32 (1) / explained by shared-memory restriction to one node (1).

---

#### (b) The simulation requires more parallelism than one node can provide. Describe two strategies the researcher could adopt, one using only a single parallel programming paradigm and one using a hybrid approach. (4 marks)

> **Model Answer**
>
> **Strategy 1 — Pure MPI:**
> Replace OpenMP with MPI (Message Passing Interface). MPI processes each have their own independent address space and communicate by **explicit message passing** over the network interconnect. The researcher can launch one or more MPI ranks per node, scaling up to 200 × 32 = 6 400 cores across the whole cluster. The code requires restructuring: the domain/data must be explicitly distributed, and halo/gather/scatter communication must be coded manually.
>
> **Strategy 2 — Hybrid MPI + OpenMP:**
> Use **one MPI rank per node** (or one per socket) to handle inter-node communication via message passing, while OpenMP threads parallelise computation across the 32 cores *within* each node. Benefits:
> - Fewer MPI ranks → fewer network messages → reduced communication overhead.
> - OpenMP handles intra-node fine-grained parallelism without MPI message overhead.
> - Memory per rank is the full 256 GB rather than 256/32 GB (MPI requires data duplication or extra communication for halo overlap).
>
> **Marking points:** MPI explanation — explicit message passing, scales across nodes (2) / hybrid explanation — MPI between nodes + OpenMP within (2).

---

*End of Week 2 Practice Questions — 25 questions across 5 sections.*

---

## Section F: Exam-Style Questions (2023 Paper)

### Q26. [Exam-style] Multiple reduction clauses on a single pragma *(5 marks)*

Consider the following serial C code that computes the sum, sum of squares, and maximum of a float array `x[N]`:

```c
float sum = 0.0f, sum2 = 0.0f, max_val = x[0];
for (int i = 0; i < N; i++) {
    sum  += x[i];
    sum2 += x[i] * x[i];
    if (x[i] > max_val) max_val = x[i];
}
```

**(a)** Parallelise this loop with a single `#pragma omp parallel for` directive using `default(none)`. Use multiple reduction clauses to accumulate all three variables safely. Write the complete pragma and loop header. *(3 marks)*

**(b)** Explain why each of `sum`, `sum2`, and `max_val` must appear in a reduction clause rather than being declared `shared`. *(2 marks)*

> **Model Answer:**
>
> **(a)** Multiple reductions can appear on a single pragma — each as a separate `reduction(op:var-list)` clause, or multiple variables listed inside one clause when the operator is the same:
>
> ```c
> #pragma omp parallel for default(none) shared(x, N) \
>         reduction(+:sum, sum2) reduction(max:max_val)
> for (int i = 0; i < N; i++) {
>     sum  += x[i];
>     sum2 += x[i] * x[i];
>     if (x[i] > max_val) max_val = x[i];
> }
> ```
>
> Key points:
> - `sum` and `sum2` share the same operator `+` so they can be listed together: `reduction(+:sum,sum2)`.
> - `max_val` uses a different operator `max`, so it requires a separate clause: `reduction(max:max_val)`.
> - `default(none)` forces explicit declaration of all variable scopes.
> - `x` and `N` are read-only and correctly declared `shared`.
>
> [3 marks: correct `reduction(+:sum,sum2)` (1); correct `reduction(max:max_val)` (1); `default(none)` with `shared(x,N)` (1)]
>
> **(b)** All three variables are **accumulated across iterations** — every iteration writes a new value derived from reading the current value:
>
> - `sum += x[i]` and `sum2 += x[i]*x[i]` are non-atomic read-modify-write operations on a scalar. If declared `shared`, multiple threads execute the load-add-store sequence concurrently, causing **lost updates** (data race): thread A and thread B both read the same stale `sum`, add their contributions, and the second store overwrites the first.
> - `max_val` has the same problem: `if (x[i] > max_val) max_val = x[i]` is a compare-and-conditionally-update — not atomic. Two threads could both read `max_val`, both decide their `x[i]` is larger, and the last write survives regardless of which was truly largest.
>
> A `reduction` clause gives each thread a **private copy** initialised to the identity element (0.0 for `+`; `-FLT_MAX` for `max`) which it updates without contention. The runtime combines all private copies atomically at the end of the loop.
>
> [2 marks: data race on shared scalar accumulator explained (1); private copy + atomic combination mechanism of reduction described (1)]

---

---

## Section G: Exam-Style Questions (ECMM461 May 2021 Paper)

### Q27 — Variable scoping analysis: Gaussian PDF loop *(6 marks)*

A researcher is computing a Gaussian probability density function over a grid. The serial C code below uses two outer variables `x` and `z`, and writes results into array `a`:

```c
double x, z;
double a[NPOINTS];
double normConst = 1.0 / sqrt(2.0 * M_PI);

for (int i = 0; i < NPOINTS; i++) {
    x = dx * i;
    z = (x - mean) / sigma;
    a[i] = normConst * exp(-0.5 * z * z);
}
```

**(a)** Identify all variables that must appear in the OpenMP clause list if `default(none)` is used. For each variable, state the correct scope (`shared`, `private`, or `lastprivate`) and justify your choice. *(4 marks)*

**(b)** One of the scope choices is `lastprivate` rather than `private`. Explain what `lastprivate` achieves here and why plain `private` would be incorrect if the value of `x` (or `z`) is needed after the loop. *(2 marks)*

> **Model Answer:**
>
> **(a)** With `default(none)`, every variable referenced inside the loop body must be explicitly declared:
>
> | Variable | Scope | Justification |
> |---|---|---|
> | `i` | `private` (implicit for loop index) | Each thread needs its own loop counter. |
> | `x` | `lastprivate` | Written every iteration (`x = dx*i`); no iteration reads a prior iteration's `x`, so it is not a flow dependency. Serial correctness requires `x` to hold the value from the last iteration `i = NPOINTS-1` after the loop completes. |
> | `z` | `private` | Intermediate per-iteration scalar. No value from `z` is needed after the loop; `private` suffices. |
> | `a` | `shared` | Array output; each iteration writes a distinct element `a[i]`, so no conflict. Entire array must be visible to all threads and the caller. |
> | `normConst`, `dx`, `mean`, `sigma` | `shared` | Read-only constants; safe to read from all threads. |
> | `NPOINTS` | `shared` (or `firstprivate`) | Read-only. |
>
> Correct directive:
> ```c
> #pragma omp parallel for default(none) \
>     shared(a, normConst, dx, mean, sigma, NPOINTS) \
>     private(z) lastprivate(x)
> ```
>
> [4 marks: 1 for correct identification of `lastprivate(x)` vs `private`; 1 for `private(z)`; 1 for `shared(a)`; 1 for shared read-only constants]
>
> **(b)** `lastprivate(x)` gives each thread a private copy of `x` during the parallel region (so threads do not race on the variable), but **after the parallel region ends**, the runtime writes back the value that `x` held during the **sequentially last iteration** (i = NPOINTS-1) into the outer variable.
>
> If plain `private(x)` were used instead, all per-thread copies of `x` are discarded at the end of the parallel region. Code that uses `x` after the loop (e.g., printing `x` or using it in subsequent computation) would read the original, unmodified outer `x` rather than the expected final value. `lastprivate` preserves the semantically correct post-loop value while still enabling parallelism.
>
> [2 marks: 1 for mechanism of lastprivate (write-back from sequentially last iteration); 1 for why private(x) would give wrong post-loop value]

---

### Q28 — `collapse(2)` for a nested loop with a small outer count *(4 marks)*

A researcher parallelises a 2D loop that generates NCURVES = 4 curves, each with 1001 sample points:

```c
double curves[NCURVES][NPOINTS];  // NCURVES = 4, NPOINTS = 1001

for (int c = 0; c < NCURVES; c++) {
    for (int i = 0; i < NPOINTS; i++) {
        curves[c][i] = evaluate_curve(c, i);
    }
}
```

**(a)** If `#pragma omp parallel for` is applied to the outer loop only, how many iterations does the parallelised loop expose? Assuming 8 threads, what is the maximum number of threads that can do useful work? *(2 marks)*

**(b)** Write the OpenMP pragma that uses `collapse(2)` to parallelise both loops together. How many total iterations does this expose? How does this benefit performance? *(2 marks)*

> **Model Answer:**
>
> **(a)** The outer loop has only **NCURVES = 4 iterations**. With `#pragma omp parallel for` on the outer loop, at most **4 threads** can be assigned work — the remaining 4 threads (out of 8) have no iterations and sit idle at the barrier, wasting half the available parallelism. This is the classic "small outer loop" problem where parallelising only the outermost dimension severely limits scalability.
>
> [2 marks: 4 iterations exposed (1); at most 4 threads useful (1)]
>
> **(b)**
> ```c
> #pragma omp parallel for collapse(2) default(none) \
>     shared(curves, NCURVES, NPOINTS)
> for (int c = 0; c < NCURVES; c++) {
>     for (int i = 0; i < NPOINTS; i++) {
>         curves[c][i] = evaluate_curve(c, i);
>     }
> }
> ```
>
> `collapse(2)` merges the two loop iteration spaces into a single iteration space of **NCURVES × NPOINTS = 4 × 1001 = 4004 iterations**. All 8 threads can now receive approximately 500 iterations each, achieving much better load balance and utilising all available threads. The only requirement for `collapse` to be correct is that the loops are **perfectly nested** (no code between them) and **independent** (no loop-carried dependency across both indices).
>
> [2 marks: 4004 iterations stated (1); benefit of full thread utilisation explained (1)]

---

## Quick Reference: Key Clauses and Directives

| Directive / Clause | Purpose |
|---|---|
| `#pragma omp parallel` | Open a parallel region; fork thread team |
| `#pragma omp for` | Distribute loop iterations across threads |
| `#pragma omp parallel for` | Combined shorthand |
| `num_threads(n)` | Set thread count for this region |
| `shared(x)` | All threads share one copy (default for outer vars) |
| `private(x)` | Each thread gets own uninitialized copy |
| `firstprivate(x)` | Each thread gets own copy initialized from outer value |
| `lastprivate(x)` | Private, but outer gets value from last sequential iteration |
| `reduction(op:x)` | Private accumulation, combined at end with `op` |
| `default(none)` | Force explicit declaration of all variable scopes |
| `schedule(static, c)` | Assign c-sized chunks round-robin at compile time |
| `schedule(dynamic, c)` | Assign c-sized chunks on demand at runtime |
| `schedule(guided, c)` | Exponentially shrinking chunks down to min c |
| `nowait` | Suppress implicit barrier at end of work-sharing construct |
| `#pragma omp barrier` | Explicit barrier — all threads wait |
| `#pragma omp critical` | Mutual exclusion block |
| `#pragma omp atomic` | Hardware atomic scalar update |
| `omp_get_thread_num()` | Returns this thread's ID (master = 0) |
| `omp_get_num_threads()` | Returns total threads in current team |
| `OMP_NUM_THREADS` | Env variable: default thread count |
