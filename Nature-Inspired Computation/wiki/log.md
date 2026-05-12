# Wiki Log

Append-only record of ingests, queries, and maintenance passes.
Each entry: `## [YYYY-MM-DD] type | title`

---

## [2026-05-12] query | NSGA-II — clarify motivation & purpose

User asked what NSGA-II is *for*. Existing `concepts/nsga-ii.md` covered the mechanics (sort + crowding + elitism) but lacked an explicit motivation section explaining the two NSGA-I problems it fixed. Cross-referenced lecture transcript (auto-caption) with `raw/text/13-14-emo.txt` to extract the motivational framing.

Edits to `concepts/nsga-ii.md`:
- New **Motivation / Why it exists** section: (1) niche radius is instance-specific and hard to set → replaced by parameter-free crowding distance; (2) NSGA-I sort was $O(MN^3)$ → fast ND sort is $O(MN^2)$; (3) elitism keeps good parents; explicit "why it took over" bullets (off-the-shelf, library support, ~70k citations)
- **Crowding distance** section: added perimeter-of-cuboid intuition with emphasis on extremes-preservation; clarified it is L1/Manhattan not Hamming (transcript auto-caption error); noted it is only computed on the *one splitting rank*
- **Exam notes** rewritten to lead with "what it's for" and the two-problem framing

No new concept pages needed — fully covered by the strengthened section.

## [2026-05-11] ingest+amend | Older papers (2015–2018) + prep-doc amendment

Ingested 4 older exam papers in parallel: 2015, 2016, 2017, 2018. Older format (Q1 compulsory + 2-of-3 elective) differs from 2019+ (all 3 compulsory). Created:
- `wiki/exam/ecm3412-15may.md` — weather-forecasting NN design, AntNet, SI terminology
- `wiki/exam/ecm3412-16may.md` — premature convergence, convergence indicators, $p_m=0$/$p_c=0$ effects
- `wiki/exam/ecm3412-17may.md` — exhaustive search, GP bloat + 7 countermeasures, NETtalk (OoS), Widrow-Hoff (OoS), SOM 3-phase
- `wiki/exam/ecm3412-18may.md` — hypervolume (worked), SMS-EMOA (OoS), ZDT (OoS), 12-solution sort, sigmoid backprop $o(1-o)$ form

Appended Section 13 "Older Papers (2015–2018)" to `likely-questions-and-checklist.md`:
- New topics promoted to Tier 2/3: premature convergence, GP bloat, hypervolume, SOM 3-phase decomposition, sigmoid backprop explicit form, time-series NN design, exhaustive search pros/cons
- Out-of-syllabus tagged & deprioritised: NETtalk, Widrow-Hoff, ZDT, SMS-EMOA, fractals
- Tier amendments: AIS confirmed as single-paper anomaly; SOM promoted (now seen 6 times); premature convergence promoted from missing to Tier 2
- Equation card extended with sigmoid derivative, hypervolume, SOM Gaussian neighbourhood, parsimony pressure

## [2026-05-11] query | Likely-questions synthesis & exam-prep checklist

Cross-paper synthesis of the 7 walkthroughs (2019, 2020, 2021, 2022, 2023, 2024, R-25) plus the 2024–25 lecture set. Wrote `wiki/exam/likely-questions-and-checklist.md` containing:
- Paper structure pattern (Q1 40-mark mixed; Q2/Q3 30-mark deep dives)
- Topic frequency matrix (7 papers × 30+ topics, with worked-calc flag)
- 4-tier likelihood ranking (Tier 1 almost certain → Tier 4 new syllabus)
- 12 worked-calculation drills with cross-references to past papers
- Open-ended design problem 7-step template
- Master must-know checklist (~80 ticks across 11 categories)
- Quick-reference equation card
- Exam-day strategy (time budgeting, partial credit, table use)

Flagged as Tier 4 (new syllabus, not yet examined but in current lectures): SNN, neuromorphic computing, MOPSO, Sörensen metaphor critique.

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2019

Ingested `raw/past_exam_papers/ECM3412-19May.pdf` (9 pages, 4 questions, 100 marks total).

Created: `wiki/exam/ecm3412-19may.md` with full verbatim questions and worked answers calibrated to marks.

Topics covered: emergence definition and importance for PSO, tournament selection procedure and selection pressure analysis (effect of increasing t), roulette wheel vs tournament selection (4 advantages), local search vs hill-climbing (Monte Carlo/Tabu) on multi-modal landscapes, single-layer perceptron OR gate (weight settings w1=w2=1, threshold activation, McCulloch–Pitts neuron), overfitting diagram (training error monotonically decreasing, generalisation error U-shaped, underfitting/overfitting regions labelled), Conway's Game of Life rules (death = <2 or >3 neighbours, birth = exactly 3, survival = 2 or 3), Wloch & Bentley 2004 F1 GA paper (representation, fitness via race simulation, variation operators, findings), exploration–exploitation parameters in GA (mutation rate, crossover rate, tournament size, population size), PSO (c1/c2 balance, neighbourhood size), ACO (alpha/beta/evaporation rate), Pareto dominance definition (minimisation), non-dominated sorting worked 10-solution example (Rank 0: x1,x3,x5,x10; Rank 1: x2,x7,x9; Rank 2: x6,x8; Rank 3: x4; worst = x4), convergence challenges (deceptive landscapes, disconnected fronts, multimodality), diversity challenges (non-uniform/concave/disconnected fronts, extreme spread), curse of dimensionality causes (exponential search space, objective space proliferation), decision space challenges (exponential growth, epistasis), objective space challenges (dominance resistance, exponential Pareto front solution count), EA optimisation of perceptron weights (real vector encoding, MAE fitness, tournament selection, Gaussian mutation, experimental design), MLP extension (longer chromosome, epistasis, landscape complexity), ACO 4-city TSP (pheromone matrix 1/12 uniform, heuristic matrix 1/d, P_AB=1/6 P_AC=2/3 P_AD=1/6, tau_BA=19/42≈0.4524, tau_CD=7/24≈0.2917, tau_DC=7/18≈0.3889).

Updated: `wiki/index.md` (Past Exam Papers count 4 → 5).

---

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2024

Ingested `raw/past_exam_papers/ECM3412-24May.pdf` (May 2024, Module Leader: Ayah Helal, 3 questions, 100 marks total).

Created `wiki/exam/ecm3412-24may.md` with full verbatim questions and worked answers calibrated to marks:
- Q1 (40 marks, 9 parts): NIC advantages, roulette wheel selection mechanics and disadvantages, ML optimisation applications (hyperparameter tuning + NAS/feature selection), GA vs GP fitness evaluation, PSO pbest/gbest roles and velocity equation, Pareto dominance definition, early stopping principle, SOM weight update (competition/cooperation/adaptation), CA state transition simultaneity.
- Q2 (30 marks): swarm intelligence properties (6 properties + ACO/PSO examples), ACO multi-machine job scheduling — construction graph design with constraints (no duplicate assignment, capacity constraint, sequential execution), total tardiness fitness function $F = \sum \max(0, C_j - d_j)$, fully worked lateness calculation for M1(ACDE)/M2(BFGH) giving F = 21.5 hours (jobs G+H responsible for 16 of 21.5 hours due to tight early deadlines placed last).
- Q3 (30 marks): PSO velocity/position full worked calculation → x(t+1)=(0.481, 1.003, 1.551); NSGA-II selection — non-dominated sorting (rank 0: {E,I,K}; rank 1: {B,C,F,H}) + crowding distance tiebreak drops C → retained {E,I,K,B,F,H}; graceful degradation principle + ablation experiment; Conway's Game of Life evolved 3 timesteps (L-tetromino → t=1 → t=2 2×3 block → t=3 diamond ring).

Updated `index.md` to add entry under Past Exam Papers section.

---

## [2026-05-11] ingest | Past exam paper — ECM3412 R-Paper May 2025

Ingested `raw/past_exam_papers/R-paper/ECM3412-R-25May.pdf` (5 pages, 3 questions, 100 marks total).

Created: `wiki/exam/ecm3412-r-25may.md` with full verbatim questions and worked answers calibrated to marks.

Topics covered: exploration vs exploitation and selection method effects (roulette/rank/tournament), GA component effects (population size, mutation rate, crossover operator, selection pressure) with examples, GP vs GA comparison (tree vs fixed-length, subtree operators, program execution cost), Boids three rules (separation/alignment/cohesion) and why Boids is a good flock model, PSO velocity (three components: inertia + cognitive + social, role of z1/z2 randomness), NSGA-II dual requirement (non-dominated sort for convergence rank + crowding distance for diversity within rank), neural network generalisation and graceful degradation, cellular automata properties (localism/parallelism/homogeneity), ACO construction graph for pipe-diameter assignment (layered vs TSP fully-connected, comparison table), ACO objective function design with penalty function for pressure violations, ACO heuristic design (inverse cost × flow-capacity proxy), ACO parameter justification (ant count, evaporation rate, α, β, pheromone init, stopping criterion), PSO parameter experiment design (benchmark functions + grid search + 30 independent runs + statistical test), multi-objective feature selection design (binary representation, maximise accuracy + minimise feature count, NSGA-II application), RNN/Elman network identification and use case (sequence modelling), SOM sizing for Iris dataset (2×2 grid, 3 classes in 4D space).

---

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2020

Ingested `raw/past_exam_papers/ECM3412-20May.pdf` (4 pages, 3 questions, 100 marks total).

Created: `wiki/exam/ecm3412-20may.md` with full verbatim questions and worked answers calibrated to marks.

Topics covered: PSO algorithm elements (velocity = inertia + cognitive + social), PSO parameters (swarm size, c1, c2, neighbourhood), Boids flocking model (separation/alignment/cohesion, Reynolds 1987), neural network variants vs MLP (perceptron = no hidden layer, SOM = unsupervised 2D grid, RNN = feedback connections), fitness landscape definition (search space + fitness function + mutation defines neighbourhood), hillclimbing failure on complex landscapes (local optima, single solution, no crossover), emergence in Conway's Game of Life (3 birth/survival/death rules → gliders/oscillators/universal computation), fractal dimension between 2 and 3 (Menger sponge d≈2.727), Koch curve construction (divide→remove middle third→equilateral bump, 5 steps) and infinite length ($L=(4/3)^n \to \infty$), AntNet algorithm (Di Caro & Dorigo 1998: forward/backward ants, routing table updates, adaptive routing, better than Bellman-Ford/Q-routing under dynamic traffic), construction graph definition and 5-variable/3-choice example, ACO experimental design (30 runs, parameter sweeps of ρ/α/β/ant count, variant comparison AS/MMAS/Elitist, statistical testing), generic EA loop and parameters, GA vs GP comparison (fixed vector vs variable tree, subtree operators, program execution cost), direct vs indirect timetabling encoding (slot assignment vs clash-free index), Pareto front definition and dominance, desirable Pareto front properties (convergence + diversity) and their benefit to decision-makers.

---

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2022

Ingested `raw/past_exam_papers/ECM3412-22May.pdf` (5 pages, 3 questions, 100 marks).

Created: `wiki/exam/ecm3412-22may.md` with full verbatim questions and worked answers calibrated to marks.

Topics covered: EA algorithmic elements and parameter settings (population size, mutation rate, crossover rate, tournament size, generations), direct vs indirect encoding with examples, exploration–exploitation tradeoff, GA vs GP comparison table (chromosome, crossover, mutation, fitness evaluation), swarm intelligence definition and three examples (ant pheromone/ACO, bird flocking/PSO, Boids/MAS), neural network weight initialisation (symmetry-breaking problem — zero init is poor), Conway's Game of Life rules (birth/survival/death/overpopulation with exact neighbour counts), roulette wheel selection (worked: fitnesses 3/4/0/2/7, total 16, probabilities 3/16 to 7/16), single-point crossover at position 3|4 (worked: 001011 × 101001 → 001001 + 101011), bit-flip mutation mechanism, airline scheduling GA design (chromosome representation, fitness function with constraint penalties, search space size 8^5 or P(8,5)=6720, scalability argument), perceptron learning rule (worked three patterns, initial boundary x1=0.5, final boundary x2=-0.5), MLP architecture for non-linearly separable 2D data (2→4→1, justification of hidden layer and node count).

Updated: `wiki/index.md` (Past Exam Papers count 2 → 3; page count 38 → 39).

---

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2023

Ingested `raw/past_exam_papers/ECM3412-23May.pdf` (4 pages, 3 questions, 100 marks).

Created: `wiki/exam/ecm3412-23may.md` with full worked answers calibrated to marks.

Topics covered: exact vs approximate algorithms, direct/indirect encoding, swarm intelligence properties, PSO parameters and equations, flocking benefits (V-formation, schooling, murmurations), AIS properties (4: uniqueness, diversity, adaptability, memory), hillclimbing + two improvements (Monte Carlo / Tabu Search), tournament selection pressure analysis (t=5 in N=5000 vs N=20), roulette wheel selection (worked: 110010/111001/101010/111100), parent selection (worked: P1=111100, P2=111001), uniform crossover with mask 101010 (worked), Pareto front definition + wind farm example, supervised vs unsupervised learning (SOM), perceptron decision boundary (w0=1, w1=1, w2=-1) + full 4-pattern validation.

Updated: `wiki/index.md` (Past Exam Papers section, count 1 → 2).

---

## [2026-05-11] ingest | Past exam paper — ECM3412 May 2021

Ingested `raw/past_exam_papers/ECM3412-21May.pdf` (3 questions, 100 marks total).
Created `wiki/exam/ecm3412-21may.md` with verbatim questions and full worked answers.

Topics covered: representations (binary/permutation/k-ary), mutation operators, crossover validity, exploration–exploitation (tournament size, population size, PSO c2), MLP vs SOM differences, timetabling design problem (constraints, objective function, GA representation, parameter tuning, success criteria), perceptron arithmetic and decision boundary derivation, MLP architecture and backpropagation.

Updated `index.md`: added Past Exam Papers section; page count 37 → 38.

---

## [2026-05-02] ingest | Initial build — all 19 sources

Ingested all available source material in one pass:
- 8 NIC lecture files (2024/2025 series, lectures 1–8 covering EA, landscapes, GP, ACO)
- 7 topic-specific lectures (11 flocking, 12 PSO, 13-14 EMO, 15 MOPSO, 16 ANN, 17 SNN)
- 3 ECM3412/ECMM409 course files (lectures 18 neuromorphic, 19 SOM, 20 A-life)
- 1 research paper (Metaphor Exposed — Sörensen 2013)
- 1 practical notebook (ACO Jupyter implementation)

Created: overview, 20 concept pages, 19 source pages, 3 comparison pages.
