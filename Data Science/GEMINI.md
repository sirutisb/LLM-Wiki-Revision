# Data Science at Scale — Revision Wiki

This workspace is an LLM-maintained revision wiki for **COM3021 / COMM115 Data Science at Scale** (Exeter, Dr Hugo Barbosa). The exam is May 2026 and weighted 70%. The wiki is designed for deep, durable revision.

As Gemini CLI, you are responsible for maintaining and expanding the `wiki/` directory. The `raw/` directory contains immutable source material.

## Layout & Architecture

```
raw/                          # Source PDFs (IMMUTABLE)
  *.pdf                       # Lecture slide decks
  text/                       # Extracted plaintext (page-marked)
wiki/                         # LLM-maintained revision content
  index.md                    # Catalog of wiki pages by category
  log.md                      # Chronological record of actions
  lectures/                   # One page per source lecture deck
  concepts/                   # Deep dives into single ideas
  comparisons/                # Side-by-side exam-focused comparisons
  topics/                     # Higher-level thematic groupings
  exam/                       # Exam-specific prep (cheatsheets, glossary)
```

## Page Conventions

Every wiki page must include YAML frontmatter:

```yaml
---
title: <Human-readable title>
type: lecture | concept | comparison | topic | exam
sources: [<lecture-slug>, ...]
related: [<page-slug>, ...]
updated: YYYY-MM-DD
---
```

### Linking & Style
- Use Obsidian-style `[[page-slug]]` wikilinks.
- Wikilinks are case-insensitive and don't require directory prefixes.
- Link concepts on their first mention per page.
- **Tone:** Precise, examiner-quality, and technical. Use the lecturer's specific terminology.
- **Citations:** Always cite slide numbers as `(s. 12)`.

### Templates
- **Lectures:** Terse slide-by-slide notes, key takeaways (3-7 bullets), and seeded concepts.
- **Concepts:** Formal definition, rationale, mechanism (ASCII/Mermaid), trade-offs, and exam framing.
- **Comparisons:** Spine is a comparison table (dimensions: cost, fault tolerance, scalability, consistency, complexity).
- **Exam:** `likely-questions.md` (answer skeletons), `cheatsheet.md` (formulas/definitions), and `glossary.md`.

## Workflows

### 1. Ingest (New Material)
- Read `raw/text/` source.
- Update `wiki/lectures/` and create/refine `wiki/concepts/`.
- Cross-reference with existing pages; flag any contradictions (`> ⚠ Conflicts with [[other-page]]`).
- Update `wiki/index.md` and append to `wiki/log.md`.

### 2. Query (Revision Help)
- Check `wiki/index.md` first.
- Synthesize answers from existing wiki content.
- Update the wiki if a query reveals a gap or a reusable synthesis.

### 3. Lint (Quality Control)
- Periodically audit for orphans, stubs, contradictions, and broken links.
- Ensure all mentioned concepts have a corresponding page in `concepts/`.

## Syllabus Focus
- **Foundations:** 3Vs, Big Data era, UNIX philosophy.
- **Storage:** B-Trees, LSM-Trees, Hash Indexes, SSTables.
- **Distributed Systems:** Replication, Partitioning, CAP Theorem, Consensus, 2PC.
- **Processing:** MapReduce, Batch vs. Stream, Messaging Systems.
- **ML at Scale:** Parallel SGD, All-Reduce, Concept Drift, Online Learning.
- **Infrastructure:** HPC, TLP, Virtualisation, Containerisation.

Process the **Review** deck last—it serves as the final synthesis and a check against the entire wiki.