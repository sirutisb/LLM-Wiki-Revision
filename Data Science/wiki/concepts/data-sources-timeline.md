---
title: "Data sources timeline"
type: concept
sources: [introduction]
related: [big-data-era, 3vs-of-big-data]
updated: 2026-05-02
---

# Data sources timeline

*Who or what generated the world's data, and when. The shift from machine-generated to user-generated to device-generated data is the demand-side driver of the Big Data era.*

## Definition

A four-phase periodisation (per Introduction s. 13) of the dominant *producer* of data:

| Period | Dominant producer | Examples |
|---|---|---|
| Pre-1980 | Machines | Industrial control, scientific instruments |
| 1980–2000 | Employees / business processes | Payroll, bank transactions, sales records |
| 2000–2005 | End users | Videos, blog posts, photos |
| 2005– | Devices, hardware, applications (IoT) | Mobile phones, remote sensors, application logs |

## Why it matters

Each shift changed the **shape** of the data, not just the **volume**:

- The user phase introduced **variety** (unstructured text, images, video) — pressure on the relational model → [[nosql-databases]].
- The device phase introduced **velocity** (continuous telemetry) — pressure on batch ETL → [[stream-processing]].
- Together they multiplied **volume** beyond single-machine capacity → pressure on [[horizontal-scaling]], [[partitioning]], [[replication]].

So the timeline maps almost cleanly onto the [[3vs-of-big-data|3Vs]].

## Examples in the syllabus

- IoT, CCTV, call-centre logs, aircraft telemetry, smart meters (Introduction s. 14).

## Common exam framing

- "Describe how the dominant source of data has shifted over the last 40 years and explain the architectural pressures each shift created."

## See also

- [[big-data-era]]
- [[3vs-of-big-data]]
