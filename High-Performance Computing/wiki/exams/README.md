---
title: "Past Exam Papers — Worked Answers"
tags: [hpc, exams, revision]
date: 2026-05-08
---

# Past Exam Papers — Worked Answers

This directory contains worked, exam-focused answers to every past paper available in `raw/past_exam_papers/`. Each question links back to the relevant wiki concept page so the underlying material can be revised in depth.

## Papers Available

| File | Module | Year | Format | Notes |
| :--- | :--- | :--- | :--- | :--- |
| [ECM3446-23May.md](ECM3446-23May.md) | ECM3446 | May 2023 | Closed book, 2 hrs | Current module |
| [ECM3446-24May.md](ECM3446-24May.md) | ECM3446 | May 2024 | Closed book, 2 hrs | Current module |
| [ECM3446-25May.md](ECM3446-25May.md) | ECM3446 | May 2025 | Closed book, 2 hrs | Current module — most recent |
| [ECMM461-21May.md](ECMM461-21May.md) | ECMM461 | May 2021 | Open book, 2 hrs + 30 min | Older equivalent module — overlaps heavily with ECM3446 |

## How to Use

1. Read the question first, attempt your own answer, then check against the worked answer.
2. Each question is annotated with mark allocation and a *Concepts* footer that links to wiki pages used in answering.
3. Calculations show all working — pay attention to units (TFlop/s vs PFlop/s, GB/s vs Gb/s, bytes vs values).
4. See [Past Paper Analysis](../exercises/Past_Paper_Analysis.md) (if present) for cross-paper themes and likely future questions.

## Recurring High-Value Topics

The same question structures reappear year after year:

- **Top500 / LINPACK** — efficiency calculation, single-core peak, MPP vs commodity classification.
- **Compute node peak performance** — `R_peak = sockets × cores × clock × ops_per_cycle`.
- **Strong vs weak scaling** — Amdahl's Law, Gustafson's Law, parallel efficiency.
- **Halo exchange** — values per halo, bytes, transmission time `t = L + M/B`.
- **Sparse matrix in CSR** — three-array representation with 1-indexed row/col.
- **OpenMP loop analysis** — identify dependency type, choose correct directives.
- **OpenMP vs MPI** — shared vs distributed memory, when to use each.
- **CFL / diffusion stability** — scaling of computational cost with resolution.
