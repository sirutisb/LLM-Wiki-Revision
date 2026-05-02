---
title: "Fault vs Failure"
type: concept
sources: [data-intensive-applications, review]
related: [reliability, replication]
updated: 2026-05-02
---

# Fault vs Failure

*A fault is one component misbehaving; a failure is the whole system going down. Fault-tolerance is the engineering practice of preventing the former from cascading into the latter.*

## Definition

- **Fault** — when one component of the system works in an unexpected way (hardware or software).
- **Failure** — when the entire system stops providing the service.

The two are **not** the same. A reliable system *will* have faults; the goal is to prevent those faults from becoming failures.

## Why it matters

In any sufficiently large system, faults happen *constantly*. A 10,000-disk cluster averages roughly one dead disk per day. If every fault became a failure, the system would never be up. The art of [[reliability]] is recognising this and engineering for graceful degradation.

## Mechanism — fault categories

| Category | Property | Examples | Mitigations |
|---|---|---|---|
| **Hardware** | Mostly **uncorrelated**, probabilistic | Failed HDDs, RAM, PSUs | RAID, redundant PSUs, hot-swap, multi-zone [[replication]] |
| **Software** | Often **correlated** across nodes | Bad monitoring agent, runaway process, OS bug | Testing, isolation, slow rollouts, kill switches |
| **Human** | Frequent and creative | Bad config, accidental delete | Sandboxes, undo, code review, automated checks |

Software faults are the dangerous ones. Because they correlate across nodes, replication doesn't help — every replica fails identically.

## Mechanism — cascading failure

A localised fault becomes a system-wide failure when it overloads other components, who then fail in turn. Classic example: a bad monitoring agent saturates the network, which causes leader-election timeouts, which trigger leader churn, which corrupts state.

## Examples in the syllabus

- **CrowdStrike Jul 2024** — a software update fault that crashed 8.5M Windows systems (~£4.1bn losses). Correlated, simultaneous, all replicas affected. The textbook software fault.
- **Disk failures in large data centres** — uncorrelated, continuous, and tolerated by [[replication]].

## Common exam framing

- "Define fault and failure and explain how they relate."
- "Give a hardware example and a software example of each. Explain why software faults are harder to mitigate."
- "Why are hardware-only redundancy measures (RAID, hot-swap PSUs) insufficient at large scale?"

## See also

- [[reliability]]
- [[replication]]
- [[consistency]]
