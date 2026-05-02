---
title: "Virtualisation"
type: concept
sources: [virtualisation-and-containerisation, review]
related: [containerisation, container-orchestration, edge-computing]
updated: 2026-05-02
---

# Virtualisation

*Creating a software-based virtual machine that behaves as a complete computer — the hypervisor multiplexes physical hardware into independent, isolated guests.*

## Definition

**Virtualisation** is the creation of a software-based virtual machine (VM) that presents the full abstraction of a physical computer — CPU, memory, storage, networking, peripherals — to a guest operating system. A **hypervisor** (virtual machine monitor) running on the host machine enables multiple VMs to share the underlying physical hardware.

## Why it matters

Virtualisation allows one physical server to run multiple independent environments — different OSes, isolated applications — improving resource utilisation, enabling easy migration (snapshot + copy), and providing strong isolation between tenants.

## Mechanism

```
Physical host hardware
    └── Hypervisor (VMWare / Hyper-V / VirtualBox)
          ├── Guest VM 1 (Windows + App A)
          ├── Guest VM 2 (Linux + App B)
          └── Guest VM 3 (Linux + App C)
```

Each VM has its own OS, kernel, libraries, and application stack. The hypervisor handles hardware access — CPU scheduling, memory allocation, I/O virtualisation.

## Virtualisation vs emulation

- **Emulation**: the guest software does not interact directly with host hardware — the emulator translates all instructions (slow but enables running code for a different CPU architecture).
- **Virtualisation**: the guest does interact with host hardware (via the hypervisor), making it much faster. The guest CPU architecture must match the host.

## Snapshots

A **snapshot** captures the full state of a VM (memory, disk, CPU registers) at a moment in time. It enables:
- Rollback after a failed update.
- Cloning: copy the snapshot to a different host machine.
- Testing: snapshot before a risky operation, restore if it fails.

## Drawbacks

- **Overhead**: each VM runs a full kernel and OS — memory and CPU overhead even at idle.
- **Redundancy**: 10 VMs on one host = 10 copies of similar OS installations.
- **Boot time**: VMs take seconds to minutes to start (full OS boot).

## Examples in the syllabus

- Virtualisation s. 3–7: definition, hypervisor, snapshots, drawbacks.
- Review s. 33–34.

## Common exam framing

- "What is a hypervisor and what role does it play in virtualisation?"
- "Distinguish virtualisation from emulation."
- "What is a VM snapshot and what can it be used for?"

## See also

- [[containerisation]]
- [[container-orchestration]]
