---
title: "Maintainability"
type: concept
sources: [data-intensive-applications, review]
related: [reliability, scalability]
updated: 2026-05-02
---

# Maintainability

*The overall cost to keep a system operational and updated — broken down into operability (running it), simplicity (understanding it), and evolvability (changing it).*

## Definition

**Maintainability** is the cost — across the full life of the system — of keeping it running and adapting it to new requirements. Dr Barbosa decomposes it into three properties:

- **Operability** — how easy it is for the operations team to keep the system running.
- **Simplicity** — how easy it is for new engineers to understand the system.
- **Evolvability** — how easy it is to make changes (new requirements, increased load).

## Why it matters

Most of a system's cost over its lifetime is in maintenance, not initial development. A system that's [[reliability|reliable]] and [[scalability|scalable]] but unmaintainable accumulates technical debt until it can't change with the business — at which point it must be rewritten, often at enormous cost.

## Mechanism — operability

Make life predictable for the ops team:
- Provide visibility into runtime behaviour and internals (good monitoring, dashboards, traces).
- Support automation and integration with standard tools (config-as-code, deployment pipelines).
- Avoid dependency on individual machines — *anyone* should be able to lose any node without firefighting.
- Exhibit predictable behaviour, minimising surprises (no unexplained latency spikes; no hidden background jobs).

## Mechanism — simplicity

Distinguish **essential complexity** (inherent in the problem) from **accidental complexity** (introduced by the implementation). Examples of accidental complexity:
- Inconsistent architecture across services.
- Obscure or implicit dependencies.
- Poor styling or documentation.
- Tightly coupled modules where a change in one ripples through ten others.

Strategy: **abstraction** — hide the messy bits behind clean interfaces. A well-chosen abstraction lets new engineers reason about a small surface, not the whole system.

> Simplicity is *not* the same as reducing functionality.

## Mechanism — evolvability

Evolvability is downstream of simplicity. Easy-to-understand systems are easy to change. Concretely: small, decoupled modules; well-named abstractions; tests that document behaviour and catch regressions; schemas that allow migration ([[schema-on-read|schema-on-read]] is one such mechanism).

## Trade-offs

- **Abstraction has a cost.** Each new layer hides things, which is good for the reader but bad for the debugger. Bad abstractions are worse than none.
- **Operability often pulls against latency.** Logging, tracing and audit trails add overhead.
- **Evolvability pulls against rigid schemas.** [[document-model|Document]] models trade consistency for flexibility precisely so the system can evolve.

## Examples in the syllabus

- The choice of [[document-model|document]] vs [[relational-model|relational]] data models is largely a maintainability argument: schema-on-read is easier to evolve, schema-on-write is easier to operate.
- [[virtualisation]] and [[containerisation]] are maintainability technologies — they make deployments reproducible and the runtime environment uniform.

## Common exam framing

- "Define maintainability and break it into its three sub-properties."
- "Explain the difference between essential and accidental complexity. Give an example of each from a data-intensive system."
- "Why might a startup choose a NoSQL database for a fast-changing product, despite the loss of relational guarantees?" → [[schema-on-read]] / evolvability.

## See also

- [[reliability]]
- [[scalability]]
- [[document-model]]
- [[schema-on-read]]
