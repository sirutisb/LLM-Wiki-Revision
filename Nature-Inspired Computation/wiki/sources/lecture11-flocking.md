# Lecture 11 — Swarm Intelligence II: Flocking

**File:** `raw/text/11-flocking.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[flocking-boids]], [[swarm-intelligence]], [[pso]]

---

## Summary

Covers collective movement in animals (flocking/swarming), Reynolds' Boids model (1987), then broadens to agents and environments. Concludes by previewing PSO as the optimisation derivative of flocking.

## Key content

### Collective movement types
- Flocking/shoaling, swarming, formation travelling
- Distinguished from non-coordinated swarming (e.g. fruit flies)
- Natural flocking: 2D or 3D

### Flocking characteristics
- Rapid directed group movement
- Reactivity to predators (flash expansion, fountain effect)
- No collisions, no dedicated leader
- Coalescing and splitting
- Occurs across all animal families and scales

### Benefits of flocking
- Geese in V-formation: 70% range extension + faster individual speeds
- Fish: slime reduces turbulence → less energy to swim
- Predator confusion: visual confusion from flash expansion/pronging

### Reynolds' Boids (1987)
Three local rules:
1. **Separation:** steer to avoid crowding local flockmates
2. **Alignment:** steer toward average heading of flockmates
3. **Cohesion:** steer toward average position of flockmates

Sensory system: omni-directional within fixed radius; detects position & bearing of all neighbours. Homogeneous (all boids identical). No noise. Immediate response.

Emergent properties: spontaneous polarisation, synchronised turns, flash expansion, flock merging.

### Agents and environments
- **Agent:** perceives via sensors, acts via actuators; action = f(percept sequence)
- **Environment characteristics:** observability, determinism, dynamism, episodic vs sequential
- **MAS:** multiple agents; scalable (communicate with direct neighbours only); competitive or cooperative

### Agent organisations
Flat, hierarchical, team, coalition.

### Fault detection in MAS
- Centralised approaches introduce single point of failure
- Monitor inter-agent communications; classify expected vs unexpected
- Focus on homogeneous agents; isolation of faulty agents is challenging

## Key takeaways
- 3 simple local rules → realistic emergent flocking behaviour
- Agent = sensor + actuator + decision rule
- MAS scales well (local communication only) but fault detection is hard

## Links to concepts
- [[flocking-boids]]: full Boids model treatment
- [[swarm-intelligence]]: the broader SI framework
- [[pso]]: previewed at end of lecture as the optimisation application of flocking principles
