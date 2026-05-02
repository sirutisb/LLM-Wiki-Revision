---
title: "Lecture: Virtualisation and Containerisation"
type: lecture
sources: [virtualisation-and-containerisation, review]
related: [virtualisation, containerisation, container-orchestration]
updated: 2026-05-02
---

# Lecture: Virtualisation and Containerisation

*Two layers of resource abstraction: virtualisation creates full virtual machines via a hypervisor; containerisation shares the host OS while isolating processes. Both enable efficient, reproducible deployment in distributed systems.*

## Slide-by-slide notes

- **(s. 2)** **Motivation**: virtualisation and containerisation abstract resources at different levels. Both make it easier to deploy updates and improve efficiency and availability.
- **(s. 3–5)** **[[virtualisation|Virtualisation]]**:
  - Creates a software-based virtual machine (VM) that acts like a real computer — has its own hardware, OS, peripherals.
  - A **hypervisor** (also called virtual machine monitor or virtualiser) runs on the physical host, allowing one or more guest VMs to run independently.
  - Examples: VMWare Workstation, VirtualBox (open-source/Oracle), Hyper-V (Microsoft).
  - **Not emulation**: in emulation the guest does not interact with host hardware directly; in virtualisation the guest does interact with host hardware (via the hypervisor abstraction).
- **(s. 6)** **Snapshots**:
  - A snapshot captures the exact state of a VM at a point in time.
  - Enables rollback to a previous state.
  - Snapshots can be copied to another host machine.
- **(s. 7)** **VM drawbacks**:
  - Significant overhead — each VM runs a full OS, including kernel, system libraries, daemons.
  - Lots of redundancy — multiple VMs on the same host duplicate the OS and config files.
- **(s. 8–10)** **[[containerisation|Containerisation]]** (OS-level virtualisation):
  - Abstracts at the *operating system* level — multiple containers share the host OS kernel and binaries while remaining isolated from each other.
  - Containers can only use resources allocated to them.
  - A container is a fully packaged, portable computing environment.
  - Key properties: **portable, scalable, easy to build/deploy/manage, isolated**.
- **(s. 11)** **[[container-orchestration|Container orchestration]]**:
  - Automates deployment, management, scaling, and networking of containers.
  - **PaaS** (Platform as a Service): third-party provider delivers a platform so developers can build and run applications without managing infrastructure. Container orchestration (e.g. Kubernetes) is the enabling technology.

## Key takeaways

1. **Virtualisation = full OS isolation** via hypervisor. Heavyweight — each VM has its own kernel. Enables true hardware-level separation.
2. **Containerisation = OS-level isolation** — shares the host kernel, packages only the application and its dependencies. Lightweight, fast to start.
3. **VMs are more isolated but heavier**; **containers are lighter but share the OS kernel** — if the kernel is compromised, all containers are affected.
4. **Snapshots** make VMs easy to restore and migrate.
5. **Container orchestration** (Kubernetes, Docker Swarm) is the layer that manages many containers across many machines.
6. **PaaS** abstracts away infrastructure entirely — developers push code, the platform handles containers, scaling, and networking.

## Concepts introduced

- [[virtualisation]]
- [[containerisation]]
- [[container-orchestration]]

## Open questions / things to clarify

- Type 1 vs Type 2 hypervisors (bare-metal vs hosted) not distinguished in the slides.
- Specific orchestration tools (Kubernetes vs Docker Swarm) not named in the slides.

## See also

- [[edge-computing]]
- [[scalability]]
- [[replication]]
