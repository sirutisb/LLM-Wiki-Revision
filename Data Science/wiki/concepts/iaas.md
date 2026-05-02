---
title: "IaaS — Infrastructure as a Service"
type: concept
sources: [introduction]
related: [big-data-era, virtualisation, containerisation]
updated: 2026-05-02
---

# IaaS — Infrastructure as a Service

*Cloud delivery model in which compute, storage, and networking are rented as virtualised resources, removing the up-front capital cost of physical infrastructure.*

## Definition

**Infrastructure as a Service** offers raw, on-demand virtual hardware (VMs, block storage, virtual networks, load balancers) over the internet, billed by usage. The customer manages the OS and everything above; the provider manages the physical layer.

## Why it matters

IaaS is *how* the [[big-data-era|Big Data era]] became operationally accessible to organisations that couldn't afford their own data centres. It is also the layer on which [[virtualisation]] and [[containerisation]] sit.

## Mechanism

The provider runs hyperscale data centres and exposes resources via APIs:

- **Compute**: VMs (EC2, Compute Engine), often with managed kernels and pre-baked images.
- **Storage**: block (EBS, persistent disk), object (S3, GCS), file (EFS).
- **Networking**: VPCs, load balancers, CDN.

Customers pay per second / per GB / per request — converting CapEx to OpEx.

## Trade-offs

- **For**: zero up-front cost, elastic scaling, geographic reach, managed reliability.
- **Against**: vendor lock-in, egress fees, sometimes worse $/FLOP than on-prem at steady-state scale.

## Examples in the syllabus

- **GCP** and **AWS** are explicitly named (Introduction s. 11). Workshops use GCP for hands-on exercises.

## Common exam framing

- "Explain how IaaS contributed to the rise of large-scale data analytics."

## See also

- [[big-data-era]]
- [[virtualisation]]
- [[containerisation]]
