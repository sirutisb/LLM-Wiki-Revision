# Swarm Intelligence

**Type:** framework / principle
**Related:** [[ant-colony-optimization]], [[pso]], [[flocking-boids]]
**Source lectures:** [[lecture07-aco-intro]], [[lecture11-flocking]]

---

## What it is

**Swarm Intelligence (SI)** is the study and use of collective behaviours that emerge from populations of simple agents interacting locally, producing complex and often intelligent group-level behaviour that no individual could achieve alone.

> "Individuals of the swarm are incapable of X, or could do X with only low probability. However, the swarm as a unit is able to do X with high probability."
> The ability to do X is an **emergent property** of the swarm.

---

## Core principles

Every swarm system has:
1. **Simple individual agents** — each follows a small rule set
2. **Local interactions** — agents only interact with immediate neighbours or environment
3. **No central controller** — every agent is equal; no leader gives instructions
4. **Emergent collective behaviour** — intelligence arises bottom-up from local rules

---

## Stigmergy

**Stigmergy** is indirect communication via modification of the environment (Grassé, 1959):

| Type | Description | Example |
|------|-------------|---------|
| **Sematonic** | Agent's action directly stimulates behaviour of other agents | Ants orient to form a bridge |
| **Sign-based** | Agent modifies environment; others respond to that modification | Pheromone trails |

Stigmergy is the mechanism behind ACO — ants don't communicate directly; they read the pheromone landscape.

---

## Real biological examples

| System | Emergent behaviour |
|--------|------------------|
| Lasius Niger ants | Find shortest path to food; regulate nest temperature within 1°C; build living bridges |
| Termites | Build complex mounds with ventilation |
| Slime mould | Individual amoebae → multicellular slug capable of coordinated movement when food scarce |
| Bird flocks | Coordinated evasion of predators; V-formation flight (up to 70% range extension) |
| Fish schools | Flash expansion, fountain effect to confuse predators |

---

## Swarm algorithms derived from SI

| Algorithm | Biological inspiration | Problem type |
|-----------|----------------------|-------------|
| [[ant-colony-optimization]] | Ant pheromone trail following | Discrete combinatorial optimisation |
| [[pso]] | Bird/fish swarming | Continuous optimisation |
| [[flocking-boids]] | Bird flocking (Reynolds 1987) | Simulation / multi-agent systems |

---

## Why swarm algorithms work for optimisation

The **collective search** explores many solutions simultaneously. Positive feedback (pheromone reinforcement in ACO, global-best pull in PSO) amplifies good solutions. Negative feedback (pheromone evaporation, velocity update noise) prevents premature convergence.

---

## Connections

- [[ant-colony-optimization]] — stigmergy-based, graph traversal
- [[pso]] — velocity-based, continuous space
- [[flocking-boids]] — simulation focus, agents and environments
- [[multi-objective-optimization]] — MOPSO extends PSO to multi-objective problems
- [[evolutionary-algorithms]] — population-based but not strictly swarm (no local interaction rule; central fitness evaluation)

---

## Exam notes

- Key property: **emergent behaviour** — the group does what no individual can
- Key mechanism: **stigmergy** — indirect communication via environment modification
- Distinguish from EAs: in SI, agents interact with each other/environment continuously; in standard EAs, individuals don't directly communicate except through selection
- Real ant experiments: Deneubourg double-bridge experiment — ants naturally find the shorter path through pheromone feedback
