High Performance Conjugate Gradients (HPCG)

NUMA - Non-Uniform Memory Access


#pragma omp target teams distribute parallel for
for (...) {}


  The Manager-Worker (or Master-Slave) model is a high-level parallel programming pattern used to achieve dynamic load balancing. In OpenMP, it is implemented in two primary ways depending on the type of work:

  1. For Loops: schedule(dynamic)
  This is the analogue of the manager-worker model for loop-based parallelism.
   * The "Manager" is the OpenMP runtime.
   * The "Workers" are the threads in the team.
   * The "Work Units" are chunks of loop iterations.
   * Whichever thread finishes its chunk first asks the runtime for another, preventing idle time when work-per-iteration is irregular (e.g., in the Mandelbrot set).

  2. For Irregular Work: OpenMP Tasks (#pragma omp task)
  For workloads that aren't simple loops (like recursive algorithms, tree traversals, or processing linked lists), OpenMP Tasks are the direct implementation of the Manager-Worker model.
   * The Manager: Usually one thread (wrapped in #pragma omp single) that generates/enqueues tasks.
   * The Workers: The rest of the thread team, which pulls tasks from the internal queue as soon as they are free.
   * This matches the classic MPI Manager-Worker skeleton more closely than loop scheduling does, as it separates the "generation" of work from the "execution."

  Comparison Table

  ┌─────────────┬──────────────────────────────┬──────────────────────────────────┬───────────────────────────────────┐
  │ Aspect      │ MPI Manager-Worker           │ OpenMP Loop (dynamic)            │ OpenMP Tasks                      │
  ├─────────────┼──────────────────────────────┼──────────────────────────────────┼───────────────────────────────────┤
  │ Manager     │ Dedicated process (Rank 0)   │ OpenMP Runtime                   │ One thread (in omp single)        │
  │ Worker pool │ All other processes          │ All threads in the team          │ All threads (including generator) │
  │ Best for... │ Distributed Memory           │ Regular loops with variable work │ Irregular or recursive work       │
  │ Work Unit   │ Explicit (e.g., a row index) │ Implicit (loop chunk)            │ Explicit (the task block)         │
  └─────────────┴──────────────────────────────┴──────────────────────────────────┴───────────────────────────────────┘