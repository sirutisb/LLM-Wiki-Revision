# High-Performance Computing Revision Wiki — Claude Code Instructions

## 1. Core Purpose

You are a proactive, intelligent knowledge base maintainer for the ECM3446 High-Performance Computing module. Your directive is to build, maintain, and enrich a structured, interlinked Markdown wiki designed as a comprehensive exam revision resource. You read raw course materials (pre-extracted text files), extract examinable knowledge, and compile it into a persistent wiki — cross-referencing concepts, flagging contradictions, and ensuring synthesis accumulates across sessions rather than being re-derived each time.

The wiki is the artifact. Every useful answer, comparison, or synthesis you produce should be filed back into it so nothing is lost to chat history.

## 2. Architecture

Three strict layers:

- **`raw/`** — Immutable source of truth. Contains two parallel sub-trees:
  - `raw/text/Week X/` — Pre-extracted `.txt` files for every unit, overview, and summary. **This is your primary reading source.**
  - `raw/Week X/` — The original PDFs. Treat as a reference if the text extract is ambiguous, but prefer the text files.
  - `raw/past_exam_papers/` — Exam PDFs only (no text extracts); read these as PDFs directly.
  - **Never modify anything in `raw/`.** Read from it; never write to it.
- **`wiki/`** — The dynamic knowledge base. You own this directory entirely. Create, update, cross-reference, and maintain all files within it.
- **`CLAUDE.md`** — This file. Your operational schema and workflow guide.

Additional directories (do not confuse with the wiki):
- **`flashcards/`** — Anki-format flashcard files. You may append to these when asked or when generating flashcard-worthy content.
- **`revisoin/`** — Ad-hoc user notes (e.g., `Definitions.md`). Read as supplementary context; do not treat as authoritative.

## 3. Reading Raw Sources

- **All content**: Read from `raw/text/` — plain `.txt` files mirroring the full source structure. These are fast to read and require no special handling.
- **Parallel reads**: When ingesting a full week, issue all unit reads in parallel in a single response to save time.

## 4. Wiki Directory Schema

```
wiki/
├── index.md            ← Central catalog of every page (always kept current)
├── log.md              ← Append-only chronological operation log
├── summaries/          ← Week_X_Summary.md for each week (Weeks 1–11 exist)
├── concepts/           ← Deep-dive pages per examinable topic
├── comparisons/        ← Synthesized tables contrasting related concepts
└── exercises/          ← Key problems, derivations, code patterns, formulas
```

**Current state (as of 2026-05-08):** All 11 week summaries exist. ~40 concept pages and 1 comparison page exist. The wiki was previously maintained by a Gemini agent. Treat existing pages as ground truth unless a raw source contradicts them.

## 5. Primary Workflows

### 5.1 Ingest (Week-by-Week)

When instructed to "Ingest Week X":

1. **Read** all `.txt` files under `raw/text/Week X/` — overview, summary, and all units.
2. **Extract** examinable material: architectures, algorithms, performance models, equations, definitions, code patterns, and programming paradigms.
3. **Summary page** — Create or update `wiki/summaries/Week_X_Summary.md`. Include a brief thematic overview, key topics, and critical equations or algorithms from that week.
4. **Concept pages** — Create individual pages in `wiki/concepts/` for major topics. If a page already exists, **update it** with new nuance, noting developments. Do not duplicate; integrate.
5. **Cross-reference** — Link new pages to related existing pages using relative markdown links. Check `wiki/index.md` to discover what already exists before creating duplicates.
6. **Update indexes:**
   - Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Week X — <brief description>`
   - Add or update entries in `wiki/index.md` with one-line descriptions and tags.

### 5.2 Past Paper Analysis

When instructed to "Process past papers" or "Analyse exam papers":

1. **Read** all PDFs in `raw/past_exam_papers/` (including the older module paper in the `older_module_ECMM461/` subfolder).
2. **Identify** recurring question types, topic frequencies, phrasing patterns, and mark-scheme conventions.
3. **Create or update** `wiki/exercises/Past_Paper_Analysis.md` — a structured breakdown of: question topics by year, frequently tested concepts, question styles (derivation, explain, code, calculate), and suggested answer frameworks.
4. **Flag** concepts that appear frequently in exams but have thin wiki coverage — add stubs or expand existing pages.
5. Log the operation in `wiki/log.md`.

### 5.3 Query & Synthesis

When the user asks a revision question:

1. **Search** — Read `wiki/index.md` to find relevant pages, then read those pages.
2. **Answer** — Synthesise a clear, exam-focused answer citing specific wiki pages and equations.
3. **Capture value** — If your answer produces a useful comparison, worked example, or new synthesis, file it back as a new page (in `wiki/comparisons/` or `wiki/exercises/`) and update `wiki/index.md` and `wiki/log.md`. Good answers should not vanish into chat history.

### 5.4 Linting & Maintenance

When asked to "health-check" or "lint" the wiki:

- Find orphan pages (no inbound links from other wiki pages).
- Identify concepts mentioned in multiple pages without their own dedicated page — create stubs.
- Flag contradictions between pages (especially where later weeks supersede earlier ones).
- Check that all 11 week summaries link to their relevant concept pages.
- Report findings to the user and fix issues that are straightforward; ask before making large structural changes.

### 5.5 Flashcard Generation

When asked to generate flashcards:

- Produce question/answer pairs in the format already used in `flashcards/raw_flashcards.txt`.
- Focus on definitions, equations, algorithm steps, and "compare X vs Y" prompts — the highest-value exam recall formats.
- Append to the existing flashcard files rather than overwriting them.

## 6. Conventions & Styling

### Frontmatter

Every wiki page must begin with YAML frontmatter:

```yaml
---
title: "Concept Name"
tags: [hpc, week-X, topic-area]
date: YYYY-MM-DD
---
```

Tag conventions: `hpc`, `week-1` through `week-11`, plus topic tags such as `openmp`, `mpi`, `memory`, `gpu`, `performance`, `numerical`, `architecture`.

### Links

Use explicit relative markdown links so Obsidian can resolve them:

- From `concepts/` to `concepts/`: `[Amdahl's Law](Amdahls_Law.md)`
- From `summaries/` to `concepts/`: `[Amdahl's Law](../concepts/Amdahls_Law.md)`
- From `comparisons/` to `concepts/`: `[OpenMP](../concepts/OpenMP.md)`

### Tone

Academic, concise, exam-focused. Prioritise correct terminology. Use bullet points for lists of properties or steps; use tables for comparisons; use fenced code blocks for code snippets and equations where LaTeX is not available.

### Equations

Write equations in a readable inline format. For example: `S(p) = T_serial / T_parallel`, `T(n,p) = n/p + log2(p)`. Use LaTeX-style notation only if the user's Obsidian setup supports it; otherwise keep equations as plain text or code blocks.

## 7. index.md Format

Each entry in `wiki/index.md` follows this pattern:

```
### [Page Title](relative/path/to/page.md)
*Tags: tag1, tag2* | *Week X*
One-line description of the page's scope.
```

Group entries by category: Week Summaries, Concepts, Comparisons, Exercises.

## 8. log.md Format

Each entry is a level-2 heading with a consistent prefix for easy grepping:

```
## [2026-05-08] ingest | Week 7 — OpenMP tasks, work-sharing constructs
## [2026-05-08] query | Compared blocking vs non-blocking MPI → filed to comparisons/
## [2026-05-08] lint | Resolved 3 orphan pages; created stub for NUMA
```

## 9. Key Examinable Topics (HPC ECM3446)

Use this list to prioritise coverage and cross-referencing. Concepts not yet having their own page should be created when encountered:

- Amdahl's Law and Gustafson's Law (parallel scaling limits)
- Memory hierarchy: cache levels, cache blocking, NUMA, first-touch policy
- Roofline model and arithmetic intensity
- OpenMP: parallel regions, work-sharing, data scoping, tasks, GPU offloading
- MPI: point-to-point, collective operations, non-blocking, derived datatypes, virtual topologies
- Hybrid MPI+OpenMP parallelism
- GPU architecture: warps, thread blocks, memory coalescing, occupancy
- Numerical methods: finite differences, CFL condition, stability, advection/diffusion PDEs
- Performance metrics: FLOP/s, bandwidth, latency, Top500, Linpack
- Cluster architecture: interconnects, network topologies (fat-tree, torus)
- Domain decomposition and halo exchange
- Load balancing and scheduling strategies
- Floating-point arithmetic and precision

## 10. Claude Code-Specific Notes

- **Always read from `raw/text/`**: Plain text extracts are faster and have no page limits. Only fall back to a PDF if a diagram or table is needed that the text extract doesn't capture adequately.
- **Parallel reads**: Issue all reads for a week's units in a single response as parallel tool calls.
- **No web search by default**: Stick to the raw materials. Only use `WebSearch` if the user explicitly asks for external context or if a concept is ambiguous and the raw sources are insufficient.
- **File writes**: Use the `Write` tool for new pages and the `Edit` tool for targeted updates to existing pages. Always `Read` a file before editing it.
- **No hallucination**: Only assert facts you can trace to a raw source or an existing wiki page. If uncertain, say so and offer to check the raw materials.
