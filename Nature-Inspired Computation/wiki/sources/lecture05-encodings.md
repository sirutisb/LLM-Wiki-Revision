# Lecture 5 — Encodings and Applications

**File:** `raw/text/2024NICLecture5.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[representations]], [[crossover-mutation]]

---

## Summary

Deep dive into encoding issues — why standard operators break on permutations, how to fix crossover for TSP, direct vs indirect encodings, and real EA applications including antenna design (patented result).

## Key content

### Permutation encoding problem
Standard single-gene mutation on TSP: change one city → invalid (visits one city twice, skips another). Must use **swap** operator instead.

Standard 1-point crossover on permutation: creates invalid children. Two fixes:
1. Use a smarter crossover operator from the start (e.g. Order Crossover)
2. Use 1-point crossover + repair: copy prefix from parent 1, fill remaining slots from parent 2 skipping already-included cities

### Direct encoding examples
- **Water distribution network:** k-ary encoding of pipe diameters; mutation = change diameter of one pipe
- **Exam timetabling (direct):** chromosome = [slot for exam 1, slot for exam 2, ...]; mutation = change one exam slot
- **Generalised assignment:** chromosome = [worker for job 1, job 2, ...]; constraints handled by fitness penalty

### Indirect encoding example: timetabling
Instead of encoding "Exam 1 in slot 4", encode "Use the 4th clash-free slot for Exam 1". Mutation changes the index; the decoder always builds a clash-free solution. Greatly reduces the invalid region of the search space.

### Direct vs Indirect
| | Direct | Indirect |
|--|--------|---------|
| What gene = | Problem variable | Constructive heuristic parameter |
| Invalid solutions | Common (penalised) | Rare (handled by decoder) |
| Search space | Larger | Smaller |
| Landscape | Smoother | Potentially rugged |
| Decoding speed | Fast | Slower |

### Applications — EA as innovation tool
- **Pipe bend optimisation (Rechenberg, 1960s):** first EA application; evolved jet nozzle shape outperforming engineered designs
- **Antenna design (Altshuler & Linden, 1998):** 105-bit chromosome, NEC simulation for fitness → US Patent 5,719,794
- **Genetic programming:** evolve programs as trees

## Key takeaways
- Encoding determines which operators are valid and how difficult the landscape is
- Permutation problems require specialised mutation (swap) and crossover (order-based or with repair)
- Indirect encodings exploit domain knowledge to shrink the effective search space
- EAs can discover novel designs beyond human intuition

## Links to concepts
- [[representations]]: direct vs indirect, encoding types
- [[crossover-mutation]]: permutation-specific operators, repair approach
- [[genetic-programming]]: tree encoding introduced here as a lead-in
