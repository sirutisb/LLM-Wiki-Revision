---
title: "Advanced OpenMP Work Sharing"
tags: [hpc, week-8, openmp]
date: 2026-05-05
---

# Advanced OpenMP Work Sharing

While `#pragma omp for` is the most common work-sharing construct, OpenMP provides others for different forms of parallelism.

## Sections
`#pragma omp sections` is used when there are discrete, independent blocks of code that can be executed concurrently, rather than iterations of a loop.
```c
#pragma omp parallel
{
    #pragma omp sections
    {
        #pragma omp section
        { /* Task A */ }
        #pragma omp section
        { /* Task B */ }
    }
}
```

## Single
`#pragma omp single` specifies that the enclosed block of code should be executed by **only one** thread in the parallel team. 
*   It does not guarantee *which* thread will execute it (usually whichever thread reaches it first).
*   There is an implicit barrier at the end of the `single` construct (unless `nowait` is used), ensuring all threads wait until the single thread completes the block.
*   This is often used for I/O operations or setting up tasks within a parallel region.