---
title: "Reliability"
type: concept
sources: [data-intensive-applications, review]
related: [fault-vs-failure, scalability, maintainability]
updated: 2026-05-02
---

# Reliability

*A reliable system performs the function the user expects, tolerates user mistakes and unusual usage, has good-enough performance under expected load, and prevents unauthorised access — even in the presence of component faults.*

## Definition

A system is **reliable** when it continues to deliver its expected behaviour despite adversity. Adversity comes from four sources Dr Barbosa highlights:

1. The user makes a mistake or uses the software in an unexpected way.
2. Load and data volume vary within the expected range.
3. Hardware components fail.
4. Adversaries attempt unauthorised access.

The shorthand he uses is **"resilient systems."**

## Why it matters

Reliability is the bedrock of every data-intensive application. Without it, [[scalability]] and [[maintainability]] are moot — a system that gives wrong answers fast and is easy to change still loses the user's trust. The CrowdStrike outage (8.5M systems, ~£4.1bn losses) is a single-incident reminder that reliability gaps have direct economic consequences.

## Mechanism — how reliable systems are built

The core distinction: a [[fault-vs-failure|fault]] is a *component* misbehaving; a *failure* is the *whole system* failing. The engineering goal is to keep faults from cascading into failures.

- **Hardware faults** are independent and probabilistic. Mitigations: RAID, redundant PSUs, hot-swap CPUs — *and* infrastructure-level redundancy ([[replication]], multi-zone deployment) once the cluster is large enough that faults are continuous.
- **Software faults** are correlated and harder to anticipate (a bad monitoring daemon, a runaway process). Mitigations: thorough testing, careful rollouts, isolation, monitoring, the ability to roll back fast.
- **Human errors** are inevitable. Mitigations: well-designed abstractions, clear UIs, sandboxed environments, recovery options.
- **Security** is part of reliability — a system that's been compromised isn't doing what the user expected.

## Trade-offs

- **Cost.** More replicas, redundant hardware, and monitoring infrastructure all cost money. Beyond a point, additional reliability has rapidly diminishing returns.
- **Latency.** Synchronous replication, distributed consensus and audit logging add response time.
- **Complexity.** Reliability mechanisms increase moving parts, so they trade against [[maintainability]].

## Examples in the syllabus

- 10,000-HDD cluster averaging one failed disk per day (Data-Intensive Applications s. 13).
- CrowdStrike Jul 2024 update — a correlated software fault that took down 8.5M systems.
- Replication architectures ([[replication]]) tolerate node failures; [[partitioning]] tolerates capacity spikes; [[stream-processing]] tolerates bursty load.

## Common exam framing

- "Define reliability and explain how it differs from scalability and maintainability."
- "What is the difference between a fault and a failure? Give a hardware and a software example of each."
- "Discuss two strategies a distributed database can use to remain reliable in the face of node failures." → expect [[replication]], failover, [[two-phase-commit|2PC]] / consensus.

## See also

- [[fault-vs-failure]]
- [[scalability]]
- [[maintainability]]
- [[replication]]
- [[cap-theorem]]
