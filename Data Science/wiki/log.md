# Data Science at Scale — Log

Append-only chronological record. Most-recent entries at the bottom. Each entry begins `## [YYYY-MM-DD] <action> | <subject>`.

## [2026-05-02] bootstrap | wiki initialised

- Extracted 22 PDFs from `raw/` to `raw/text/` (421 pages total) via `extract_pdfs.py`.
- Authored `CLAUDE.md` schema: directory layout, page templates (lecture / concept / comparison / topic / exam), ingest / query / lint workflows, house style.
- Created `wiki/index.md` (skeleton) and `wiki/log.md` (this file).
- Identified two near-duplicate deck pairs: `Storage and Retrieval` (+ `_2024`), `Stream Processing` (+ `_2025`). Schema treats undated / `_2025` decks as canonical.
- Plan: ingest one lecture as a worked example, get user feedback, then proceed lecture-by-lecture in syllabus order, processing `Review.pdf` last as a lint pass.

## [2026-05-02] ingest | Introduction

- Created `lectures/introduction.md` — slide-by-slide notes (24 slides, but ≈4.2 KB extracted text — diagram-heavy deck, flagged for user).
- Seeded 4 concept pages: `3vs-of-big-data.md`, `big-data-era.md`, `data-sources-timeline.md`, `iaas.md`.
- Updated `index.md` to list the new pages and mark Introduction as ingested.
- No comparison or topic pages yet — waiting for more lectures to have enough critical mass.
- Open question for user: confirm the figure-heavy slides (s. 9–10, s. 15–21) don't carry assessable content beyond the captions.

## [2026-05-02] ingest | Bulk ingest — all 20 remaining decks

Complete bulk ingest of all remaining lecture material. Lectures created:
- `lectures/data-intensive-applications.md` — reliability, scalability, maintainability, fault vs failure, Twitter fan-out, vertical/horizontal scaling.
- `lectures/storage-and-retrieval.md` — log, hash index, SSTables, LSM-tree, B-tree, OLTP vs OLAP.
- `lectures/data-models-nosql.md` — relational, document, graph models; NoSQL families; schema-on-read.
- `lectures/consistency.md` — CAP, ACID, eventual consistency, linearizability, consensus, 2PC.
- `lectures/replication.md` — leader-follower, sync/async, failover, replication lag.
- `lectures/partitioning.md` — key-range, hash, secondary indexes, rebalancing (merged Partitioning + Part 2 2025 decks).
- `lectures/batch-processing.md` — three system classes, Unix philosophy, MapReduce, distributed filesystems, reduce-side join.
- `lectures/stream-processing.md` — events, messaging systems, broker vs direct, load balancing vs fan-out, acks, event time.
- `lectures/distributed-machine-learning.md` — communication patterns, SGD with all-reduce, parallel k-means.
- `lectures/online-learning.md` — full batch / mini-batch / online learning; three data shifts.
- `lectures/concept-drift-detection.md` — drift types; ADWIN, DDM, EDDM.
- `lectures/high-performance-computing.md` — FLOPS, Moore's Law, Amdahl's Law, SLURM.
- `lectures/thread-level-parallelism.md` — SISD/SIMD/MIMD, OpenMP, MPI.
- `lectures/tensors.md` — tensor orders, data shapes, sparse tensors, DOK/COO/CSR.
- `lectures/software-hardware-codesign.md` — bottom-up/top-down/co-design, partitioning, edge computing.
- `lectures/virtualisation-and-containerisation.md` — hypervisors, VMs, containers, orchestration, PaaS.
- `lectures/review.md` — lecturer's synthesis; exam-relevance signal.

Concept pages created (50+): see `index.md` Concepts section for full list.

Comparisons created: `batch-vs-stream.md`, `vms-vs-containers.md`, `replication-vs-partitioning.md`, `relational-vs-document-vs-graph.md`.

Topics created: `distributed-systems.md`, `storage.md`, `machine-learning-at-scale.md`.

Exam pages created: `likely-questions.md` (27 questions with answer skeletons), `cheatsheet.md`, `glossary.md`.

Updated `index.md` to list all pages and mark all 20 decks as ingested.

Notes:
- Distributed Architectures Part 2 (2025) merged into `partitioning.md` (duplicate content + secondary index expansion).
- Batch Processing text cuts off at page 13 — deeper MapReduce content and Spark alternatives may be in figure slides.
- Concept Drift lecture: EDDM specifics sparse in extracted text — check original PDF for detail.
- Review deck explicitly covers: Reliability, Scalability, Maintainability, CAP, ACID, Eventual consistency, NoSQL/Document, Scaling, Replication, Partitioning, Batch, Stream, Event time, Tensors, Virtualisation, Containerisation. Topics NOT in Review are lower-confidence exam items.
