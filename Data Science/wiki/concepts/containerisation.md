---
title: "Containerisation"
type: concept
sources: [virtualisation-and-containerisation, review]
related: [virtualisation, container-orchestration, edge-computing]
updated: 2026-05-02
---

# Containerisation

*OS-level virtualisation that packages an application and its dependencies into an isolated, portable unit — lighter than a VM because the host OS kernel is shared.*

## Definition

**Containerisation** (OS-level virtualisation) abstracts at the operating system level. Containers share the host OS kernel and system libraries but are isolated from each other in terms of processes, networking, and filesystem. A container packages an application with everything it needs to run (code, runtime, libraries, config).

## Why it matters

VMs are heavy — each has a full OS. Containers are lightweight: starting a container takes milliseconds (no kernel boot), and multiple containers on one host share the kernel, reducing redundancy dramatically.

## VM vs Container

| Dimension | Virtual Machine | Container |
|---|---|---|
| Isolation level | Hardware-level (hypervisor) | OS-level (kernel namespaces/cgroups) |
| Kernel | Each VM has its own | Shared host kernel |
| OS overhead | Full OS per VM | Only app + dependencies |
| Startup time | Seconds–minutes | Milliseconds |
| Portability | VM image (large) | Container image (small) |
| Security isolation | Stronger | Weaker (shared kernel) |

## Key properties of containers

- **Portable** — run identically on any host with the container runtime.
- **Scalable** — spin up or down quickly to meet load.
- **Isolated** — containers cannot interfere with each other or the host (within their resource limits).
- **Easy to build and deploy** — declarative image definitions (Dockerfile).
- **Reproducible** — same image → same behaviour everywhere.

## Mechanism

The host OS uses:
- **Namespaces** — isolate process trees, network interfaces, filesystem mounts.
- **cgroups** — limit CPU, memory, and I/O resources per container.

```
Host OS kernel
  ├── Container 1 (App A + libs)
  ├── Container 2 (App B + libs)
  └── Container 3 (App C + libs)
```

## Examples in the syllabus

- Virtualisation s. 8–10: definition, properties, OS-level virtualisation framing.
- Review s. 35–36.

## Common exam framing

- "How does containerisation differ from virtualisation?"
- "List three desirable properties of containers."
- "Why is containerisation considered more lightweight than virtualisation?"

## See also

- [[virtualisation]]
- [[container-orchestration]]
