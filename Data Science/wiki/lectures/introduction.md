---
title: "Lecture: Introduction — the Big Data era"
type: lecture
sources: [introduction]
related: [3vs-of-big-data, big-data-era, data-intensive-applications]
updated: 2026-05-02
---

# Lecture: Introduction — the Big Data era

*Sets the scene for the module: how we got to "big data," what's driving it, where it's transforming work, and the headline challenges that the rest of the module will solve.*

## Slide-by-slide notes

- **(s. 1–2)** Module COM3021 / COMM115, taught by Dr Hugo Barbosa.
- **(s. 3)** Companies have shifted to be more *social*, *customer-oriented*, *dynamic* over the last decade — not just tech firms.
- **(s. 4)** The data-to-value loop: `data → uncover insights → support actions → create value`. Workflows now embed **monitoring, collecting, understanding, learning, responding, improving, adapting**.
- **(s. 5)** Scale of generation: **463 EB in 2021**, projected **495.9 EB in 2025** (Statista). EB = exabyte = 10⁶ TB.
- **(s. 6–8)** Three enabling forces: **cheap storage and processing**, **free open-source tools**, **faster networks**. Cited via StackOverflow trends and the Nielsen Norman "law of bandwidth."
- **(s. 11)** Hyperscalers (Google, Amazon, Microsoft) push the envelope; the resulting **IaaS** offerings (GCP, AWS) democratise access.
- **(s. 12)** "Big Data era" as an equation: *massive data + cheaper, more powerful processing → better models* (generalisation, prediction, inference) — *and* solutions to entirely new problems, not just better solutions to existing ones.
- **(s. 13)** **Data sources timeline** — see [[data-sources-timeline]] for the full breakdown.
  - Pre-1980: machines.
  - 1980–2000: employees / business processes (payroll, transactions, sales).
  - 2000–2005: end users (videos, blogs, photos).
  - 2005–: devices / sensors / IoT (mobiles, telemetry, logs).
- **(s. 14)** Concrete examples: IoT, CCTV, call-centre logs, *several TB per flight* for an aircraft, smart meters reading every 15 min → **350 billion transactions / year**.
- **(s. 15–21)** Domains transformed: **AI**, **marketing** (Walmart, Netflix, Amazon — profiling, targeted ads, recommendations), **healthcare** (personalised treatment, drug discovery, causal inference), **smart cities** (transport optimisation, traffic forecasting, autonomous vehicles), **disaster response** (evacuation routing, human-rights monitoring, resource allocation).
- **(s. 22–24)** Challenges: the **[[3vs-of-big-data|3Vs]]** — Volume, Velocity, Variety — and two further dimensions, **Veracity** and **Value**.

## Key takeaways

1. The Big Data era was *enabled* (cheap storage, OSS tooling, fast networks) and *demanded* (volume, velocity, variety of new data sources).
2. The economic argument is not "do the same things faster" — it is "**solve problems that were previously unsolvable**."
3. **Volume** alone breaks single-machine analysis → motivates [[distributed-systems|distributed systems]] and [[horizontal-scaling]].
4. **Velocity** breaks batch-only thinking → motivates [[stream-processing]].
5. **Variety** breaks the relational model's rigid schemas → motivates [[nosql-databases]] and document / key-value / graph models.
6. The "more Vs" (Veracity, Value) anticipate later modules on data quality, ML, and the link from analytics to business outcomes.

## Concepts introduced

- [[3vs-of-big-data]] — Volume, Velocity, Variety (+ Veracity, Value).
- [[big-data-era]] — definition and the enabling-forces argument.
- [[data-sources-timeline]] — who/what generated data over time.
- [[iaas]] — Infrastructure-as-a-Service as a delivery model.

## Open questions / things to clarify

- **Slides are diagram-heavy** (≈4.2 KB of extracted text for 24 slides). Several slides are mostly imagery — confirm with the original PDF whether anything beyond captions is intended for assessment, especially s. 9–10 (no extracted text) and the domain-transformation visuals (s. 15–21).
- The "more Vs" list is truncated at Veracity and Value. Some textbooks add Variability and Visualization — worth checking if Dr Barbosa expects only 5.

## See also

- [[3vs-of-big-data]]
- [[big-data-era]]
- [[data-sources-timeline]]
- [[data-intensive-applications]] — the formal vocabulary (reliability, scalability, maintainability) introduced in the next deck.
