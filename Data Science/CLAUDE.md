# Data Science at Scale — Wiki Schema

This is an LLM-maintained revision wiki for **COM3021 / COMM115 Data Science at Scale** (Exeter, Dr Hugo Barbosa). The exam is May 2026 and weighted 70%, so the wiki exists to support deep, durable revision — not generic note-taking.

You (the LLM agent) own everything under `wiki/`. The user owns `raw/`. Read on for conventions.

## Layout

```
raw/                          # Source PDFs — IMMUTABLE, never edit
  *.pdf                       # Lecture slide decks
  text/                       # Extracted plaintext (one .txt per PDF, page-marked with "--- page N ---")
extract_pdfs.py               # Re-runnable extractor; idempotent
wiki/                         # LLM-owned. Everything below this line.
  index.md                    # Catalog of every wiki page, grouped by category
  log.md                      # Append-only chronological record of ingests / queries / lints
  lectures/                   # One page per source lecture deck
    <slug>.md                 # e.g. consistency-2025.md
  concepts/                   # Reusable concept pages, one idea per page
    <slug>.md                 # e.g. cap-theorem.md, eventual-consistency.md
  comparisons/                # Side-by-side comparisons (these are exam gold)
    <slug>.md                 # e.g. acid-vs-base.md, batch-vs-stream.md
  topics/                     # Higher-level themes that group concepts
    <slug>.md                 # e.g. distributed-systems.md, storage.md
  exam/                       # Revision-focused pages
    likely-questions.md       # Anticipated exam questions with worked answers
    cheatsheet.md             # One-page formula / definition reference
    glossary.md               # Compact term -> definition list
```

Don't add new top-level dirs without telling the user first.

## Page conventions

Every wiki page starts with YAML frontmatter:

```yaml
---
title: <Human-readable title>
type: lecture | concept | comparison | topic | exam
sources: [<lecture-slug>, ...]   # Which raw decks contributed. Empty if synthesised.
related: [<page-slug>, ...]      # Hand-picked related pages. Used for the "See also" section.
updated: YYYY-MM-DD
---
```

After the frontmatter:

- **H1** matching the title.
- **One-line summary** under the H1 (italicised, ≤25 words). This is what `index.md` quotes.
- Body sections appropriate to the page type (see below).
- **See also** section at the bottom listing `related` pages as wikilinks.

Use Obsidian-style `[[page-slug]]` wikilinks throughout the body — never bare paths. Wikilinks resolve case-insensitively to any file in the wiki, so you don't need directory prefixes. When you mention a defined concept, link it on first mention in each page.

### Page-type templates

**lecture/** — Mirrors the structure of the slide deck. Sections:
- *Slide-by-slide notes* (or topic-by-topic if the deck is non-linear) — keep it terse, one bullet per slide where possible. Cite slide numbers as `(s. 12)`.
- *Key takeaways* — 3–7 bullets. The thing the user must remember.
- *Concepts introduced* — wikilinks to every `concepts/` page this lecture seeds or updates.
- *Open questions / things to clarify* — anything ambiguous in the slides worth flagging.

**concepts/** — One idea, deeply explained. Sections:
- *Definition* (1–2 sentences, examiner-quality).
- *Why it matters* — what problem does this concept solve?
- *Mechanism / how it works* — the actual content. Diagrams as ASCII or mermaid if useful.
- *Trade-offs* — when to use, when not to.
- *Examples in the syllabus* — concrete systems / case studies from the lectures.
- *Common exam framing* — how examiners typically ask about it.

**comparisons/** — A markdown table is usually the spine. Sections:
- *Summary* — one paragraph telling the reader which to pick when.
- *Comparison table* — dimensions × options. Keep dimensions consistent (cost, fault tolerance, scalability, consistency, complexity, when-to-use).
- *Key differences explained* — the nuance the table can't capture.
- *Decision rule* — a 1-line heuristic.

**topics/** — Light-touch index pages that *group* concepts. Mostly wikilinks plus a few sentences of glue. Don't duplicate concept content here.

**exam/** — Tailored to revision:
- `likely-questions.md` — list of anticipated questions, each with a brief answer skeleton + links to the relevant concept pages. Include past exam framings if the user shares them.
- `cheatsheet.md` — one-page condensed reference (formulas, definitions, key trade-offs).
- `glossary.md` — `**term**: one-line definition. → [[concept-page]]` per line, alphabetised.

## Workflows

### Ingest (single lecture)

1. Read `raw/text/<lecture>.txt` end-to-end. If text is sparse (slides are mostly figures), say so and ask the user to skim the original PDF for missing context.
2. Discuss the lecture's main themes with the user before writing — confirm what to emphasise.
3. Write `wiki/lectures/<slug>.md` using the lecture template.
4. For every concept the lecture introduces or extends:
   - If `wiki/concepts/<concept>.md` doesn't exist, create it.
   - If it does exist, *update* it: add new examples, refine the definition, add cross-references. Note any contradictions with previous sources inline (`> ⚠ Conflicts with [[other-page]]: ...`).
5. Touch any `comparisons/` and `topics/` pages affected.
6. Update `wiki/index.md` (add new pages, refresh one-line summaries if changed).
7. Append a `log.md` entry: `## [YYYY-MM-DD] ingest | <Lecture Title>` followed by a short bullet list of pages created/updated.

Default to **one lecture per ingest, with the user in the loop**. Only batch-ingest if explicitly asked.

### Query

1. Read `wiki/index.md` first to find candidate pages.
2. Read those pages. Pull from `raw/text/` only if the wiki is thin on the topic (and if so, *update the wiki afterwards* so the gap closes).
3. Answer with citations to wiki pages (`[[page-slug]]`) and slide numbers where relevant.
4. If the answer is itself reusable (a comparison the user asked for, an exam answer skeleton), offer to file it as a new wiki page. Don't file silently — confirm first.
5. Append a `log.md` entry: `## [YYYY-MM-DD] query | <short question>` with a one-line summary of the answer.

### Lint

When asked, audit the wiki for:
- **Contradictions** — claims on different pages that disagree. Flag and propose resolution.
- **Orphans** — pages with no inbound wikilinks. Either link them in or propose deletion.
- **Stubs** — pages under ~150 words or missing required sections.
- **Missing concepts** — terms referenced but never defined. Propose new concept pages.
- **Stale `updated:` dates** — pages whose related sources have been updated since.
- **Broken wikilinks** — links to slugs that don't resolve.

Report findings as a checklist; let the user pick what to fix.

## Conventions and house style

- **Slugs**: kebab-case, ASCII only, no dates unless disambiguating versions (e.g. `consistency-2025.md` is fine, `concept-drift-detection.md` is fine).
- **Tone**: examiner-quality. Precise definitions, no marketing fluff. Prefer the wording the lecturer used (these are *his* exam questions).
- **Length**: concept pages 200–600 words. Lectures pages can run longer. Comparisons live or die by the table — keep prose tight.
- **Citations**: `(s. 12)` for a slide reference; `[[lecture-slug]] s. 12` if disambiguation is needed.
- **Diagrams**: mermaid when structural (architectures, sequence diagrams). ASCII art is fine for small things. Don't waste tokens on mermaid for trivial 3-node sketches.
- **Frontmatter `sources:`** is the source-of-truth for which decks fed a page. Keep it accurate — the lint pass uses it.
- **Version conflicts**: where two decks cover the same topic (e.g. `Storage and Retrieval.pdf` vs `Storage and Retrieval_2024.pdf`), treat the un-dated / `_2025` deck as canonical and only pull from the older one to fill genuine gaps. List both in `sources:` if both contributed.
- **Don't write code unless asked.** This is a revision wiki, not an implementation. If an algorithm matters, give pseudocode and the cost/complexity, not a working implementation.

## Initial scope (the 22 source decks)

Roughly mapped to the syllabus from the Module Overview:

| Syllabus block | Source decks |
|---|---|
| Foundations | Module Overview, Introduction, Data Intensive Applications |
| Storage & retrieval | Storage and Retrieval (+ 2024), Data Models and NoSQL databases |
| Consistency | Consistency |
| Distributed systems | Distributed Architectures Replication / Partitioning / part 2 |
| Batch & stream | Batch Processing, Stream Processing (+ 2025) |
| Large-scale ML | Distributed Machine Learning, Online Learning, Concept Drift Detection |
| Future architectures | High Performance Computing, TLP, tensor, Software-hardware co-design |
| Virtualisation | Virtualisation and Containerisation |
| Recap | Review |

Process the **Review** deck *last* — it's the lecturer's own end-of-module synthesis and is the best signal for what's exam-relevant. Use it as a lint pass against the wiki we've built.
