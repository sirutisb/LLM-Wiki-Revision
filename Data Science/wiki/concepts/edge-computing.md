---
title: "Edge computing"
type: concept
sources: [software-hardware-co-design]
related: [software-hardware-codesign, virtualisation, containerisation]
updated: 2026-05-02
---

# Edge computing

*Moving computation from centralised cloud data centres to the devices and local nodes where data is generated — reducing latency, enabling personalisation, and requiring specialised co-designed hardware.*

## Definition

**Edge computing** places computation at or near the source of data (end devices, local gateways) rather than sending all data to a central cloud. Computation happens "at the edge" of the network.

## Why it matters

As AI/ML models become more personalised, cloud-based processing faces limits:
- **Latency** — round-trip to cloud and back adds delay unacceptable for real-time applications.
- **Privacy** — sensitive data (health, location) should not leave the device.
- **Bandwidth** — sending raw video or sensor data to the cloud is expensive.
- **Offline operation** — devices need to function without a network connection.

## Requirements

Edge hardware must be:
- **Power-constrained** — smartphones, IoT sensors, cars have limited batteries.
- **Small and cheap** — cannot install full server hardware.
- **Capable** — must run ML inference (and sometimes training adaptation).

This creates demand for **co-designed** neural processing units (NPUs), mobile GPUs, and model compression techniques (quantisation, pruning).

## Examples in the syllabus

- Software-hardware co-design s. 5: edge computing introduced as the driver for on-device ML specialisation.

## Common exam framing

- "Why is edge computing relevant to data science at scale?"
- "What hardware constraints does edge computing impose compared to cloud computing?"

## See also

- [[software-hardware-codesign]]
- [[virtualisation]]
- [[containerisation]]
