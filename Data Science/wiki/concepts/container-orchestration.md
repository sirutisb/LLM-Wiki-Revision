---
title: "Container orchestration"
type: concept
sources: [virtualisation-and-containerisation]
related: [containerisation, virtualisation, scalability]
updated: 2026-05-02
---

# Container orchestration

*Automated management of many containers across many machines — handling deployment, scaling, networking, and failure recovery so operators don't have to do it manually.*

## Definition

**Container orchestration** is the automated management of containerised applications at scale. It handles: deploying containers to appropriate machines, scaling the number of containers up or down, managing inter-container networking, and recovering from container or node failures.

## Why it matters

Running a handful of containers manually is feasible. Running thousands of containers across hundreds of nodes is not — a single Kubernetes cluster may manage millions of container restarts per day. Orchestration makes this operationally manageable.

## Key functions

- **Scheduling** — decide which node runs which container based on available resources and constraints.
- **Scaling** — automatically add or remove container replicas in response to load.
- **Service discovery** — containers find each other by name, not by IP address.
- **Health monitoring** — restart failed containers; reroute traffic away from unhealthy nodes.
- **Rolling updates** — deploy new container versions without downtime.

## PaaS connection

**PaaS (Platform as a Service)** builds on container orchestration to provide an even higher-level abstraction: developers push code (or a container image), and the platform handles running, scaling, and networking. The developer never manages individual machines.

```
Developer → code/image → PaaS platform
                              ↓
                    Orchestrator (e.g. Kubernetes)
                              ↓
                    Container runtime on nodes
```

## Examples in the syllabus

- Virtualisation s. 11: orchestration and PaaS defined together.

## Common exam framing

- "What is container orchestration and why is it needed?"
- "How does PaaS relate to container orchestration?"

## See also

- [[containerisation]]
- [[virtualisation]]
- [[scalability]]
