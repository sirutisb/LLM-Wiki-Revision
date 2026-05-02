# Flocking and Boids

**Type:** model / simulation
**Related:** [[swarm-intelligence]], [[pso]], [[neural-networks]]
**Source lectures:** [[lecture11-flocking]]

---

## What it is

**Flocking** is coordinated collective movement of a group (birds, fish, insects) with no central leader — emergent behaviour from local interactions. Craig Reynolds (1987) created the **Boids** model to simulate this computationally, motivated by realistic 3D animation.

---

## Characteristics of real flocking

- Rapid, directed movement of the whole flock
- Reactivity to predators (flash expansion, fountain effect)
- No collision between flock members
- Flock coalescence and splitting
- No dedicated leader
- Occurs in all media (air, water, land) across animal families
- Ranges from tiny groups to enormous (herring shoals 17 miles long)

---

## Benefits of flocking (biology)

| Benefit | Example |
|---------|---------|
| Extended range | Geese in V-formation travel 70% further |
| Reduced turbulence | Fish cast off slime reducing energy needed |
| Predator confusion | Flash expansion; pronging (antelopes); schooling in fish |

---

## Reynolds' Three Rules (Boids, 1987)

Every boid follows three simple local rules:

| Rule | Description | Effect |
|------|-------------|--------|
| **1. Separation** | Steer to avoid crowding local flockmates | Prevents collisions |
| **2. Alignment** | Steer toward the average heading of flockmates | Synchronises direction |
| **3. Cohesion** | Steer toward the average position of local flockmates | Keeps group together |

**Sensory system:** omni-directional, within a fixed radius neighbourhood. Boids detect position and bearing of all neighbours (no occlusion). Homogeneous system — all boids identical. Immediate response (no memory).

**Emergent behaviours from these three rules:**
- Spontaneous polarisation
- Synchronised direction changes
- Flash expansion if startled
- Flock merging and splitting

---

## Agents and environments (lecture 11 broader context)

An **agent** perceives its environment via sensors and acts via actuators.
- **Percept:** agent's current sensory input
- **Percept sequence:** full history of everything perceived

**Environment characteristics:**
- **Observability:** can the agent see the full state?
- **Determinism:** does the same action always produce the same result?
- **Dynamism:** does the environment change independently?
- **Episodic vs. sequential:** are actions independent or do they depend on history?

**Multi-agent systems (MAS):**
- Multiple agents solving complex tasks cooperatively or competitively
- Scalable (agents communicate only with neighbours)
- Applications: autonomous cars, robot factories, automated trading, games

**Agent organisations:**
- Flat, hierarchical, team-based, coalitions

---

## From flocking to optimisation

The key insight Kennedy & Eberhart (1995) exploited: if food source = optimal solution, and each bird has some idea of where it smelled food best, the flock converges on the food. This gives [[pso]].

---

## Connections

- [[pso]] — formalises flocking into an optimisation algorithm
- [[swarm-intelligence]] — Boids is a canonical SI example
- [[ant-colony-optimization]] — another SI-inspired algorithm (different mechanism: pheromone vs. velocity)

---

## Exam notes

- Reynolds' **3 rules**: Separation, Alignment, Cohesion
- Complex flocking emerges from just these 3 local rules — no central control
- Boids was created for **animation**, not optimisation — PSO was the optimisation derivative
- Agent = sensor + actuator + decision rule
- MAS: agents communicate only locally → scalable; fault detection is a challenge
