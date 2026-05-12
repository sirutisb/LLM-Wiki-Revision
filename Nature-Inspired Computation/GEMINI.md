# NIC Wiki — Schema & Conventions

## What this is
A personal revision wiki for the module **ECM3412/ECMM409 – Nature-Inspired Computation** at the University of Exeter (Autumn 2025). The wiki is built and maintained by Gemini; the human curates sources and asks questions.

## Directory layout

```
raw/                   # Immutable source PDFs + extracted text (never modify)
  text/                # One .txt per PDF — page boundaries as "--- page N ---"
wiki/                  # LLM-generated markdown (you own this entirely)
  index.md             # Master catalog — updated on every ingest
  log.md               # Append-only chronological record
  overview.md          # High-level module map
  concepts/            # One page per algorithm, technique, or concept
  sources/             # One page per source (lecture or paper)
  comparisons/         # Cross-cutting comparison and synthesis pages
GEMINI.md              # This file — conventions and workflows
```

## Page formats

### Concept page (`concepts/*.md`)
```
# [Concept Name]

**Type:** algorithm | framework | principle | technique
**Related:** [[other-concept]], [[another-concept]]
**Source lectures:** [[lecture-NN]]

## What it is
One clear definition sentence.

## Motivation / Why it exists
The problem it solves and why naive approaches fail.

## How it works
Step-by-step description or pseudocode. Key equations in LaTeX.

## Key parameters & their effects
Table or bullet list: parameter → what happens if you increase/decrease it.

## Variants
Named variants with brief differences.

## Pros & Cons
| Advantage | Disadvantage |
|-----------|--------------|

## Connections
- Builds on [[fitness-landscapes]]
- Compare with [[pso]]

## Exam notes
Bullet points of things most likely to appear in exam questions.
```

### Source page (`sources/*.md`)
```
# Lecture N — [Title]

**File:** `raw/text/[filename].txt`
**Lecturer:** [name]
**Concepts introduced:** [[concept-1]], [[concept-2]]

## Summary
2–4 sentence summary of the lecture's main contribution.

## Key content
### [Heading from lecture]
Concise notes.

## Key takeaways
Bullet points.

## Links to concepts
- [[concept-1]]: introduced here
- [[concept-2]]: expanded from [[lecture-NN]]
```

### Comparison page (`comparisons/*.md`)
```
# [A] vs [B] (or: [Topic] — Synthesis)

## Overview
What is being compared and why the comparison matters.

## Comparison table
| Dimension | A | B |
|-----------|---|---|

## When to use which
...

## Synthesis
What deeper insight does this comparison reveal?
```

## Index conventions
`index.md` has three sections: Concepts, Sources, Comparisons. Each entry is one line: `- [[filename]] — one-line summary`.

## Log conventions
Each log entry starts with `## [YYYY-MM-DD] type | title` where type is `ingest`, `query`, or `lint`. This makes it greppable.

## Ingest workflow
1. Read the source `.txt` file
2. Create a source page in `sources/`
3. Update or create affected concept pages in `concepts/`
4. Update `index.md`
5. Append to `log.md`

## Query workflow
1. Read `index.md` to find relevant pages
2. Read the relevant concept/source/comparison pages
3. Synthesise an answer
4. If the answer is broadly useful, file it as a new comparison or synthesis page

## Lint checklist
- Orphan pages (no inbound links from index or other pages)
- Concept pages missing "Exam notes" section
- Broken `[[wikilinks]]` (links to non-existent pages)
- Source pages without linked concept pages

## Wikilinks
Use `[[filename-without-extension]]` for internal links. Filenames are lowercase hyphenated.

## Equations
Use `$...$` for inline and `$$...$$` for display math.
