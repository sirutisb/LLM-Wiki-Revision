# Metaheuristics — The Metaphor Critique

**Type:** critical perspective / research paper
**Related:** [[evolutionary-algorithms]], [[swarm-intelligence]], [[ant-colony-optimization]], [[pso]]
**Source lectures:** [[metaphor-exposed]]

---

## What it is

This page summarises Kenneth Sörensen's paper **"Metaheuristics — The Metaphor Exposed"** (2013, *International Transactions in Operational Research*). The paper argues that a significant proportion of published metaheuristics research consists of **hollow metaphor-based methods** that do not constitute genuine scientific contributions.

> The field of metaheuristics has witnessed a "tsunami of novel methods, most of them based on a metaphor of some natural or man-made process." Sörensen argues this is threatening scientific rigour.

---

## The core argument

### The analogy

Sörensen opens with a hypothetical: imagine a paper in *Nature* proposing a "food-based theory of particle physics" where quarks = "meat", electrons = "vegetables", atoms = "dishes", Higgs boson = "salt". The scientific community would ridicule this. Yet, in metaheuristics research, analogous papers are published and cited frequently.

### What counts as a "novel" metaphor method?

Any paper that:
1. Bases a new optimisation algorithm on a metaphor (frogs jumping, water flowing, bats flying, sperm cells, galaxies spiralling, etc.)
2. Claims superiority over existing methods
3. Attracts follow-up papers testing it on many problems "with strikingly good results"

---

## Historical context: why metaphors proliferated

1. **Heuristics were not accepted as serious science** — long viewed as engineering shortcuts rather than rigorous algorithms
2. **Nature-inspired framing was a marketing device** — association with evolutionary biology, physics, etc. gave heuristics scientific credibility
3. **Early successes were genuine:** SA (1983), GA (1975), TS (1989), EA (1960s-70s), ACO (1992), PSO (1995) — these introduced genuinely new algorithmic concepts

As the field matured, new papers continued adding metaphors but **stopped adding new algorithmic ideas**.

---

## The main fallacies

### Fallacy 1: A new metaphor = a new algorithm

Most "novel" metaphor methods are **renamings or minor variants** of existing algorithms (SA, GA, tabu search, etc.) with new terminology. The metaphor adds vocabulary but not mathematical insight.

### Fallacy 2: Good experimental results prove superiority

"Good results" can always be found by:
- **Cherry-picking benchmark problems** on which the algorithm happens to perform well
- **Tuning parameters** for the test set specifically
- **Incomplete comparisons** — only comparing against poorly-tuned baselines

The **No Free Lunch theorem** (Wolpert & Macready, 1997) proves: no algorithm outperforms all others on all possible problems. Any algorithm can be made to look good on some problems.

### Fallacy 3: Peer review filters this out

Peer review in this area has been insufficiently rigorous. Reviewers often:
- Accept novel metaphors as novelty
- Accept "better results on these benchmarks" as proof of general superiority
- Do not demand proofs of convergence, complexity analysis, or theoretical grounding

---

## What Sörensen considers genuinely innovative research

High-quality metaheuristics research:
1. **Formal analysis:** convergence proofs, complexity analysis, theoretical characterisation
2. **Problem structure exploitation:** understanding why an algorithm works on a specific problem class (e.g. exploiting graph properties in ACO for routing)
3. **Unified frameworks:** work that synthesises disparate methods (e.g. showing SA is a special case of a broader framework)
4. **Algorithmic innovation:** new operators, new search strategies, new data structures
5. **Rigorous empirical methodology:** proper statistical testing, wide comparison, public benchmark results

---

## Implication for NIC students

The module includes this paper as a **critical perspective** — it trains you to evaluate claims about NIC algorithms:

| Claim | Critical question |
|-------|-----------------|
| "Algorithm X outperforms Y on these benchmarks" | Were the benchmarks cherry-picked? Was comparison fair? |
| "Algorithm X is inspired by [unusual metaphor]" | Does the metaphor add algorithmic insight or just new terminology? |
| "Algorithm X is novel" | Is it genuinely different from SA, GA, ACO, PSO — or a minor variant? |
| "X solves NP-hard problem Y effectively" | Effective on which instances? Compared to what baselines? |

---

## Well-established algorithms (pre-proliferation era)

These are considered the legitimate foundational metaheuristics:
- **Simulated Annealing (SA)** — 1983
- **Genetic Algorithms (GA)** — Holland 1975
- **Tabu Search (TS)** — Glover 1989
- **Evolutionary Strategies (ES)** — Rechenberg 1960s
- **Ant Colony Optimisation (ACO)** — Dorigo 1992
- **Particle Swarm Optimisation (PSO)** — Kennedy & Eberhart 1995

---

## Connections

- [[evolutionary-algorithms]] — one of the legitimate foundational metaheuristics
- [[ant-colony-optimization]] — legitimate SI; genuine algorithmic concept (stigmergy)
- [[pso]] — legitimate SI; genuine algorithmic concept (velocity-based swarm)
- [[swarm-intelligence]] — area most affected by metaphor proliferation

---

## Exam notes

- Sörensen's argument: new metaphors do not constitute new algorithms; most are renamings of SA/GA/TS/ACO/PSO
- **No Free Lunch**: no algorithm is universally best; experimental results on benchmarks are insufficient proof
- Genuine innovation requires: formal analysis, theoretical grounding, or truly novel algorithmic mechanisms
- Good critical question: "What does this metaphor add beyond existing algorithmic components?"
- The paper is a **call for scientific rigour**, not an attack on the legitimate foundational algorithms
