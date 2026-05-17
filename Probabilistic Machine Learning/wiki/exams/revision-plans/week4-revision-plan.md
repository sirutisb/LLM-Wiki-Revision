# Week 4 Revision Plan - Variational Approximation

**Scope:** [[variational-inference]], [[elbo]], [[kl-divergence]], [[mean-field-vi]], [[forward-vs-reverse-kl]], [[laplace-approximation]]
**Source:** [[lecture-w4]], [[supp-elbo]], [[elbo-derivation]], [[examinable-topics]], [[topics-and-formulas]], [[week4_questions]]
**Formula status:** No formula sheet for Week 4. The ELBO derivation is examinable and must be reproducible from memory. Know the KL definition, VI objective, both ELBO forms, the log-evidence decomposition, the lower-bound argument, the equivalence between ELBO maximisation and reverse-KL minimisation, and the mean-field/CAVI update idea.

Week 4 is one of the highest-priority exam topics. The likely questions are: derive the ELBO from the KL divergence, explain why the ELBO is a lower bound, compare reverse and forward KL, explain mode-seeking behaviour, compare VI with the Laplace approximation, and describe mean-field VI or coordinate ascent updates.

---

## What To Know Cold

### Core purpose
- [ ] Exact Bayesian inference targets:
$$
p(\theta|\mathcal{D})
=
\frac{p(\mathcal{D}|\theta)p(\theta)}{p(\mathcal{D})},
\qquad
p(\mathcal{D})
=
\int p(\mathcal{D}|\theta)p(\theta)\,d\theta.
$$
- [ ] The evidence integral $p(\mathcal{D})$ is usually intractable because it is high-dimensional or has no closed form.
- [ ] VI replaces the true posterior with a tractable distribution $q(\theta)$ chosen from a family $\mathcal{Q}$.
- [ ] VI is optimisation-based and deterministic, unlike [[mcmc]], which approximates expectations using samples.
- [ ] VI is global in objective, unlike [[laplace-approximation]], which fits a local Gaussian around the MAP.

### Variational objective
- [ ] The direct VI objective is:
$$
q^*
=
\arg\min_{q\in\mathcal{Q}}
\mathrm{KL}\!\left(q(\theta)\,\|\,p(\theta|\mathcal{D})\right).
$$
- [ ] KL divergence definition:
$$
\mathrm{KL}(q\|p)
=
\int q(\theta)\log\frac{q(\theta)}{p(\theta)}\,d\theta
=
\mathbb{E}_q[\log q(\theta)-\log p(\theta)].
$$
- [ ] KL is non-negative and equals zero iff the two distributions match almost everywhere.
- [ ] KL is asymmetric: $\mathrm{KL}(q\|p)\neq \mathrm{KL}(p\|q)$.
- [ ] The direct objective is not computable because $p(\theta|\mathcal{D})$ contains the intractable evidence.

### Reverse vs forward KL
- [ ] Reverse KL, $\mathrm{KL}(q\|p)$, is used in VI because the expectation is under $q$, which we choose.
- [ ] Reverse KL is zero-forcing / mode-seeking: it heavily penalises $q(\theta)>0$ where $p(\theta)\approx 0$.
- [ ] Reverse KL can underestimate posterior uncertainty and may choose one mode in a multimodal posterior.
- [ ] Forward KL, $\mathrm{KL}(p\|q)$, is mass-covering / zero-avoiding.
- [ ] Forward KL is impractical for VI because it requires expectations under the true posterior and pointwise access to the normalised posterior.

### ELBO forms
- [ ] Joint form:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$
- [ ] Ratio form:
$$
\mathcal{L}(q)
=
\mathbb{E}_q\!\left[
\log\frac{p(\mathcal{D},\theta)}{q(\theta)}
\right].
$$
- [ ] Data-fit minus complexity form:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\mathrm{KL}(q(\theta)\|p(\theta)).
$$
- [ ] Interpret the terms:
  - Expected log-likelihood rewards data fit.
  - KL to the prior penalises complexity / deviation from the prior.
- [ ] Key identity:
$$
\log p(\mathcal{D})
=
\mathcal{L}(q)
+
\mathrm{KL}(q(\theta)\|p(\theta|\mathcal{D})).
$$
- [ ] The gap between log evidence and ELBO is the KL from $q$ to the true posterior.
- [ ] Since KL is non-negative, $\mathcal{L}(q)\leq \log p(\mathcal{D})$.
- [ ] The bound is tight iff $q(\theta)=p(\theta|\mathcal{D})$.

### Mean-field VI
- [ ] Mean-field assumption:
$$
q(\boldsymbol{\theta})
=
\prod_{j=1}^{d}q_j(\theta_j).
$$
- [ ] The assumption makes optimisation tractable by ignoring posterior correlations.
- [ ] CAVI update:
$$
\log q_j^*(\theta_j)
=
\mathbb{E}_{q_{-j}}[\log p(\mathcal{D},\boldsymbol{\theta})]
+
\mathrm{const}.
$$
- [ ] Equivalent proportional form:
$$
q_j^*(\theta_j)
\propto
\exp\!\left(
\mathbb{E}_{q_{-j}}[\log p(\mathcal{D},\boldsymbol{\theta})]
\right).
$$
- [ ] CAVI updates one factor while holding all others fixed; each update increases or preserves the ELBO.
- [ ] Main limitation: factorisation cannot represent posterior correlations and often underestimates uncertainty.

---

## Derivations To Master

### Derivation 1 - ELBO from reverse KL
- [ ] Start from:
$$
\mathrm{KL}(q(\theta)\|p(\theta|\mathcal{D}))
=
\mathbb{E}_q\!\left[
\log\frac{q(\theta)}{p(\theta|\mathcal{D})}
\right].
$$
- [ ] Substitute Bayes' rule:
$$
p(\theta|\mathcal{D})
=
\frac{p(\mathcal{D},\theta)}{p(\mathcal{D})}.
$$
- [ ] Expand the log ratio:
$$
\mathrm{KL}(q\|p(\theta|\mathcal{D}))
=
\mathbb{E}_q[\log q(\theta)]
+
\log p(\mathcal{D})
-
\mathbb{E}_q[\log p(\mathcal{D},\theta)].
$$
- [ ] Justify taking $\log p(\mathcal{D})$ outside the expectation because it does not depend on $\theta$ and $\int q(\theta)d\theta=1$.
- [ ] Rearrange:
$$
\log p(\mathcal{D})
=
\underbrace{
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)]
}_{\mathcal{L}(q)}
+
\mathrm{KL}(q(\theta)\|p(\theta|\mathcal{D})).
$$
- [ ] Conclude that maximising $\mathcal{L}(q)$ minimises reverse KL because $\log p(\mathcal{D})$ is constant with respect to $q$.

### Derivation 2 - Data-fit minus complexity
- [ ] Start from:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$
- [ ] Factorise the joint:
$$
p(\mathcal{D},\theta)
=
p(\mathcal{D}|\theta)p(\theta).
$$
- [ ] Expand and regroup:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
+
\mathbb{E}_q[\log p(\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$
- [ ] Recognise the prior KL:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\left(
\mathbb{E}_q[\log q(\theta)]
-
\mathbb{E}_q[\log p(\theta)]
\right)
$$
$$
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\mathrm{KL}(q(\theta)\|p(\theta)).
$$
- [ ] State the interpretation of each term in words.

### Derivation 3 - Lower-bound argument
- [ ] Use the decomposition:
$$
\log p(\mathcal{D})
=
\mathcal{L}(q)
+
\mathrm{KL}(q\|p(\theta|\mathcal{D})).
$$
- [ ] Since $\mathrm{KL}\geq 0$:
$$
\mathcal{L}(q)
\leq
\log p(\mathcal{D}).
$$
- [ ] Equality holds iff $\mathrm{KL}(q\|p(\theta|\mathcal{D}))=0$, i.e. $q(\theta)=p(\theta|\mathcal{D})$ almost everywhere.

### Derivation 4 - Mean-field update logic
- [ ] Know the CAVI update formula from memory.
- [ ] Be able to explain it without a full functional derivative: update one factor by exponentiating the expected log joint under all other factors.
- [ ] State that the full CAVI derivation is not the main Week 4 derivation, but the update and intuition are examinable.

---

## Revision Schedule

### Pass 1 - 45 minutes: memory setup
- [ ] Read [[lecture-w4]], [[supp-elbo]], [[elbo]], and [[elbo-derivation]].
- [ ] From a blank page, write the VI objective.
- [ ] Write the KL definition as both an integral and an expectation.
- [ ] Write both ELBO forms from memory.
- [ ] Write the log-evidence decomposition from memory.
- [ ] Define "lower bound", "tight bound", and "ELBO gap" in one sentence each.
- [ ] Explain why $\log p(\mathcal{D})$ is constant with respect to $q$.

### Pass 2 - 60 minutes: full ELBO derivation
- [ ] Do [[week4_questions]] Q4 without notes.
- [ ] Mark every algebraic move: KL definition, Bayes substitution, log expansion, expectation split, rearrangement.
- [ ] Redo Q4 until the derivation fits on one clean page.
- [ ] Practise deriving the data-fit minus complexity form from the joint form.
- [ ] Practise proving $\mathcal{L}(q)\leq \log p(\mathcal{D})$ in two lines.

### Pass 3 - 45 minutes: KL behaviour and conceptual answers
- [ ] Read [[kl-divergence]] and [[forward-vs-reverse-kl]].
- [ ] Do [[week4_questions]] Q1.
- [ ] Explain reverse KL as mode-seeking using the penalty $q(\theta)>0$ where $p(\theta)\approx 0$.
- [ ] Explain forward KL as mass-covering using the penalty $q(\theta)\approx 0$ where $p(\theta)>0$.
- [ ] Prepare a two-column comparison table for reverse vs forward KL from memory.

### Pass 4 - 45 minutes: VI vs Laplace and mean-field
- [ ] Do [[week4_questions]] Q3.
- [ ] Explain why Laplace is local: MAP plus Hessian at one point.
- [ ] Explain why VI is global: optimisation over a distributional family using the ELBO.
- [ ] Read [[mean-field-vi]].
- [ ] Write the mean-field factorisation and CAVI update from memory.
- [ ] State one benefit and two limitations of mean-field VI.

### Pass 5 - 40 minutes: calculations and manipulation
- [ ] Do [[week4_questions]] Q5.
- [ ] Do [[week4_questions]] Q6.
- [ ] Practise substituting into a Gaussian KL formula if one is provided in the question.
- [ ] For any ELBO manipulation, identify which term is data fit and which term is regularisation.
- [ ] Check sign discipline: ELBO maximises expected log-likelihood minus KL, not plus KL.

### Final 20-minute check
- [ ] Derive the ELBO from KL without notes.
- [ ] Write both ELBO forms without notes.
- [ ] Prove the lower-bound property without notes.
- [ ] Explain why maximising ELBO is equivalent to minimising reverse KL.
- [ ] Explain reverse vs forward KL using a bimodal-posterior example.
- [ ] Write the mean-field assumption and CAVI update.
- [ ] Compare VI, Laplace, and MCMC in four sentences.

---

## Practice Priorities

### Highest priority
- [ ] [[week4_questions]] Q4: full ELBO derivation. This is the must-master item.
- [ ] [[week4_questions]] Q2: ELBO forms, lower-bound property, tightness condition.
- [ ] [[week4_questions]] Q1: why VI is needed and why reverse KL is used.

### Medium priority
- [ ] [[week4_questions]] Q3: VI vs Laplace approximation.
- [ ] [[week4_questions]] Q6: manipulate the ELBO and interpret data-fit versus KL terms.
- [ ] Explain mean-field VI and CAVI from [[mean-field-vi]].

### Lower priority but useful
- [ ] [[week4_questions]] Q5: Gaussian KL calculation.
- [ ] Rehearse a short comparison with [[mcmc]]: VI is fast and biased; MCMC is slower but asymptotically exact.
- [ ] Connect Week 4 ELBO to [[variational-autoencoder]] only at a high level unless Week 8 is being revised.

---

## Worked Example 1 - ELBO Decomposition

### Question

Starting from:
$$
\mathrm{KL}(q(\theta)\|p(\theta|\mathcal{D}))
=
\mathbb{E}_q\!\left[
\log\frac{q(\theta)}{p(\theta|\mathcal{D})}
\right],
$$
derive the identity:
$$
\log p(\mathcal{D})
=
\mathcal{L}(q)
+
\mathrm{KL}(q(\theta)\|p(\theta|\mathcal{D})).
$$

### Solution

Use Bayes' rule:
$$
p(\theta|\mathcal{D})
=
\frac{p(\mathcal{D},\theta)}{p(\mathcal{D})}.
$$

Substitute:
$$
\mathrm{KL}(q\|p(\theta|\mathcal{D}))
=
\mathbb{E}_q\!\left[
\log\frac{q(\theta)p(\mathcal{D})}{p(\mathcal{D},\theta)}
\right].
$$

Expand:
$$
=
\mathbb{E}_q[\log q(\theta)]
+
\log p(\mathcal{D})
-
\mathbb{E}_q[\log p(\mathcal{D},\theta)].
$$

Rearrange:
$$
\log p(\mathcal{D})
=
\underbrace{
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)]
}_{\mathcal{L}(q)}
+
\mathrm{KL}(q\|p(\theta|\mathcal{D})).
$$

Therefore:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$

---

## Worked Example 2 - Why The ELBO Is A Lower Bound

### Question

Use the identity
$$
\log p(\mathcal{D})
=
\mathcal{L}(q)
+
\mathrm{KL}(q\|p(\theta|\mathcal{D}))
$$
to prove that $\mathcal{L}(q)$ is a lower bound on $\log p(\mathcal{D})$.

### Solution

KL divergence is non-negative:
$$
\mathrm{KL}(q\|p(\theta|\mathcal{D}))\geq 0.
$$

Therefore:
$$
\log p(\mathcal{D})
=
\mathcal{L}(q)
+
\mathrm{KL}(q\|p(\theta|\mathcal{D}))
\geq
\mathcal{L}(q).
$$

So:
$$
\mathcal{L}(q)\leq \log p(\mathcal{D}).
$$

The bound is tight iff the KL term is zero, which occurs iff $q(\theta)=p(\theta|\mathcal{D})$ almost everywhere.

---

## Worked Example 3 - Converting ELBO Forms

### Question

Show that:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D},\theta)]
-
\mathbb{E}_q[\log q(\theta)]
$$
is equivalent to:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\mathrm{KL}(q(\theta)\|p(\theta)).
$$

### Solution

Use $p(\mathcal{D},\theta)=p(\mathcal{D}|\theta)p(\theta)$:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)+\log p(\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$

Split the expectation:
$$
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
+
\mathbb{E}_q[\log p(\theta)]
-
\mathbb{E}_q[\log q(\theta)].
$$

Regroup the last two terms:
$$
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\left(
\mathbb{E}_q[\log q(\theta)]
-
\mathbb{E}_q[\log p(\theta)]
\right).
$$

Recognise:
$$
\mathrm{KL}(q(\theta)\|p(\theta))
=
\mathbb{E}_q[\log q(\theta)-\log p(\theta)].
$$

Thus:
$$
\mathcal{L}(q)
=
\mathbb{E}_q[\log p(\mathcal{D}|\theta)]
-
\mathrm{KL}(q(\theta)\|p(\theta)).
$$

---

## Common Mistakes

- [ ] Forgetting that no formula sheet is provided for Week 4.
- [ ] Treating the ELBO formula as "given" instead of something to derive.
- [ ] Starting the ELBO derivation from the prior KL $\mathrm{KL}(q\|p(\theta))$ instead of the posterior KL $\mathrm{KL}(q\|p(\theta|\mathcal{D}))$.
- [ ] Dropping the expectation notation too early and losing which distribution the average is under.
- [ ] Forgetting that $\log p(\mathcal{D})$ can leave the expectation because it is constant with respect to $\theta$.
- [ ] Getting the ELBO sign wrong: it is expected log-likelihood minus KL to the prior.
- [ ] Saying the ELBO equals the evidence. It is only equal when $q$ is the exact posterior.
- [ ] Saying minimising reverse KL is directly tractable. It becomes tractable only through the ELBO.
- [ ] Confusing reverse and forward KL behaviours: reverse KL is mode-seeking; forward KL is mass-covering.
- [ ] Explaining mode-seeking only as "chooses a mode" without naming the zero-forcing penalty.
- [ ] Saying VI is always better than Laplace. VI is global and flexible, but it is still limited by the variational family and KL direction.
- [ ] Saying mean-field VI means parameters are truly independent. It means the approximation assumes independence, even if the real posterior has correlations.
- [ ] Forgetting that CAVI updates one factor at a time while holding the others fixed.
- [ ] Claiming the mean-field update derivation is the core examinable Week 4 derivation. The ELBO derivation is the core examinable derivation.

---

## Exam-Ready Checklist

You are Week 4-ready when you can:

- [ ] State why exact Bayesian inference is intractable for realistic models.
- [ ] Write the VI objective $q^*=\arg\min_{q\in\mathcal{Q}}\mathrm{KL}(q\|p(\theta|\mathcal{D}))$ from memory.
- [ ] Write the KL definition as an integral and expectation from memory.
- [ ] Derive the ELBO from reverse KL without notes.
- [ ] Write both ELBO forms from memory.
- [ ] Prove $\mathcal{L}(q)\leq\log p(\mathcal{D})$ using KL non-negativity.
- [ ] State when the lower bound is tight.
- [ ] Explain why maximising ELBO is equivalent to minimising reverse KL.
- [ ] Explain reverse KL vs forward KL, including mode-seeking and mass-covering behaviour.
- [ ] Explain why VI commonly underestimates uncertainty.
- [ ] Compare VI with Laplace approximation in terms of objective, locality, posterior shape, and limitations.
- [ ] Write the mean-field factorisation and CAVI update from memory.
- [ ] Explain the main limitation of mean-field VI: ignored posterior correlations.
- [ ] Complete [[week4_questions]] Q4 cleanly in exam-style working.
- [ ] State that Week 4 has no formula sheet and the ELBO derivation is examinable.
- [ ] Similar past-paper calibration: state reverse vs forward KL and name practical VI optimisation methods such as CAVI and gradient-based ELBO optimisation.
