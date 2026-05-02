# Lecture 2 — The Motivation for Evolutionary Algorithms

**File:** `raw/text/2024NICLecture2.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[evolutionary-algorithms]]

---

## Summary

Introduces the generic EA loop, motivates EAs through the lens of optimisation complexity, and distinguishes exact algorithms from approximate algorithms. EAs are positioned as approximate algorithms for hard (NP-hard) problems.

## Key content

### Generic EA

Generate population P of random solutions → loop: (1) Select parents, (2) Apply genetic operators, (3) Replace some old with new.

### Types of EA (overview)
- **Selection:** top 10%, fitness-proportionate, rank-based, tournament
- **Variation:** encoding-dependent operators
- **Population update:** replace entire population, or merge and choose best |P|

### Optimisation context
- Find $s^*$ with max/min $f(s^*)$
- Hard problems (NP-hard): huge search space; exact algorithms infeasible
- Approximate algorithms: no guarantee of optimal; but fast and find "good enough" solutions

### EA as approximate algorithm
EAs are approximate algorithms applicable to hard (combinatorial, NP-hard) problems.

## Key takeaways
- EA = select → vary → replace, iterated
- Fitness function $f(s)$ can measure anything that can be computed from a candidate solution
- Population size typically 100–500

## Links to concepts
- [[evolutionary-algorithms]]: full treatment of the EA framework
- [[selection]]: covers the selection step
- [[crossover-mutation]]: covers the variation step
