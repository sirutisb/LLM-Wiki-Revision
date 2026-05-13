---
title: "Wiki Log"
tags: [log, hpc]
date: 2026-05-05
---

## [2026-05-13] final_prep | Compute node architecture — core/processor/socket/node hierarchy, memory controllers, NUMA, first-touch, MPI-per-socket pattern
## [2026-05-13] comparison | Finite difference stencils — forward/backward vs centered: accuracy, stability, FTCS instability, upwind CFL condition
# Operation Log

## [2026-05-05] init | Wiki initialization
## [2026-05-05] ingest | Week 1 Materials
## [2026-05-05] ingest | Week 2 Materials
## [2026-05-05] ingest | Week 3 Materials
## [2026-05-05] ingest | Week 4 Materials
## [2026-05-05] ingest | Week 5 Materials
## [2026-05-05] ingest | Week 6 Materials
## [2026-05-05] ingest | Week 7 Materials
## [2026-05-05] ingest | Week 8 Materials
## [2026-05-05] ingest | Week 9 Materials
## [2026-05-05] ingest | Week 10 Materials
## [2026-05-06] update | Enriched Parallel Scaling concept
- Added detailed first-principle derivations for Amdahl's and Gustafson's Laws.
- Included comparison table between Strong and Weak scaling.
- Added Amdahl's Law with parallel overheads.

## [2026-05-07] update | Added Performance Analysis and Cache Blocking concepts
- Created dedicated page for Cache Blocking (Loop Tiling).
- Created dedicated page for Problem Size and Memory Footprint in performance analysis.
- Linked new concepts to Memory Hierarchy and updated the index.

## [2026-05-08] creation | Strong vs. Weak Scaling Comparison
*   Created `wiki/comparisons/Strong_vs_Weak_Scaling.md` to provide a detailed side-by-side comparison of scaling types and their governing laws (Amdahl and Gustafson).
*   Updated `wiki/index.md` to include the new comparison page.

## [2026-05-08] query | Barrier Methods in OpenMP and MPI
*   Created [Barriers and Synchronization](concepts/Barriers_and_Synchronization.md) to synthesize barrier usage across both paradigms.
*   Updated [Index](index.md) and [Load Balancing](concepts/Load_Balancing_and_Scheduling.md) with links.

## [2026-05-05] ingest | Week 11 Materials

## [2026-05-08] ingest | Past Exam Papers — created wiki/exams/ with worked answers
- Created `wiki/exams/` directory with a README index of papers.
- Walked through every question of all four available papers (ECM3446 May 2023, May 2024, May 2025, and the older ECMM461 May 2021) with full worked answers.
- Each question links back to the relevant wiki concept page(s) so the answers are grounded in the lecture material.
- Calculations show full working (LINPACK efficiency, peak performance, scaling laws with and without overheads, halo transmission times, CSR encodings, computational-cost scaling for advection vs diffusion).
- Cross-paper observation: the same question structures (Top500 efficiency, compute-node R_peak, halo transmission, CSR, OpenMP loop analysis, Amdahl/Gustafson) recur every year — see exams/README.md for a list of recurring themes.

## [2026-05-07] update | Updated Arithmetic Intensity concept
- Added formal formula for Arithmetic Intensity and quantified examples (Vector Addition vs Matrix Multiplication).
- Added summary table contrasting Memory-Bound vs Compute-Bound.
- Added section on the Cache-Aware Roofline Model (L1, L2, L3 bandwidth ceilings).