# Week 6 Revision Plan - Information Theory

**Scope:** [[information-content]], [[entropy]], [[cross-entropy]], [[kl-divergence]], [[mutual-information]], [[maximum-entropy-principle]]
**Source:** [[lecture-w6]], [[examinable-topics]], [[week6_questions]]
**Formula status:** Week 6 information theory formulas will be provided. The exam tests whether you can recognise the correct formula, apply it cleanly, interpret the result, and explain the intuition. Derivations are not examinable, but you should understand why the definitions behave the way they do.

Week 6 is lower priority than Weeks 1-5 and 7 in the revision order, but it is compact and calculation-friendly. Likely questions are short conceptual explanations, entropy or KL calculations from small tables, comparisons of entropy, and interpreting KL divergence, cross-entropy, mutual information, and maximum entropy.

---

## What To Know Cold

### Formula status
- [ ] You do not need to memorise every Week 6 formula exactly, because formulas are provided.
- [ ] You do need to recognise which formula applies to each problem: self-information, entropy, joint entropy, conditional entropy, mutual information, cross-entropy, or KL divergence.
- [ ] You do need to know the meaning of each quantity without looking it up.
- [ ] You do need to know standard results: uniform distributions maximise discrete entropy; Gaussian distributions maximise differential entropy for fixed mean and variance; KL divergence is non-negative and asymmetric.
- [ ] You should understand derivations as intuition only: entropy as expected self-information, cross-entropy as entropy plus KL, and mutual information as uncertainty reduction or KL from independence.

### Core definitions
- [ ] Information content: surprise of one observed outcome. Rare events carry more information; certain events carry zero information.
- [ ] Entropy: expected information content, or average surprise, of a distribution.
- [ ] Conditional entropy: remaining uncertainty in one variable after observing another.
- [ ] Mutual information: reduction in uncertainty about one variable after observing another.
- [ ] Cross-entropy: expected coding cost when data come from $p$ but the code/model is based on $q$.
- [ ] KL divergence: expected extra coding cost from using $q$ instead of $p$.
- [ ] Maximum entropy principle: choose the highest-entropy distribution subject to the known constraints, because it makes the fewest extra assumptions.

### Formulas to recognise and apply
- [ ] Self-information:
$$
I(x) = -\log p(x).
$$
- [ ] Discrete entropy:
$$
H(X) = -\sum_x p(x)\log p(x).
$$
- [ ] Joint entropy:
$$
H(X,Y) = -\sum_{x,y} p(x,y)\log p(x,y).
$$
- [ ] Conditional entropy:
$$
H(X|Y) = -\sum_{x,y} p(x,y)\log p(x|y).
$$
- [ ] Chain rule:
$$
H(X,Y) = H(Y) + H(X|Y).
$$
- [ ] Mutual information:
$$
I(X;Y) = H(X) - H(X|Y)
= D_{\mathrm{KL}}(p(x,y)\|p(x)p(y)).
$$
- [ ] KL divergence:
$$
D_{\mathrm{KL}}(p\|q) = \sum_x p(x)\log\frac{p(x)}{q(x)}.
$$
- [ ] Cross-entropy:
$$
H(p,q) = -\sum_x p(x)\log q(x)
= H(p) + D_{\mathrm{KL}}(p\|q).
$$
- [ ] Differential entropy:
$$
h(X) = -\int p(x)\log p(x)\,dx.
$$
- [ ] Gaussian differential entropy:
$$
h(X) = \frac{1}{2}\log(2\pi e\sigma^2).
$$

### Properties and interpretations
- [ ] Entropy is zero for a deterministic discrete variable.
- [ ] Entropy is maximised by the uniform distribution over a fixed finite support.
- [ ] For $K$ equally likely outcomes, $H(X)=\log K$.
- [ ] Differential entropy can be negative and depends on scale.
- [ ] Gaussian differential entropy depends on variance, not mean.
- [ ] KL divergence is always non-negative and equals zero iff the two distributions are identical.
- [ ] KL divergence is asymmetric: $D_{\mathrm{KL}}(p\|q)$ and $D_{\mathrm{KL}}(q\|p)$ answer different questions.
- [ ] Reverse KL $D_{\mathrm{KL}}(q\|p)$ is mode-seeking in variational inference.
- [ ] Forward KL $D_{\mathrm{KL}}(p\|q)$ is mass-covering and appears naturally in cross-entropy / MLE settings.
- [ ] Mutual information is zero iff the variables are independent.
- [ ] Mutual information is symmetric, even though KL divergence is not generally symmetric.
- [ ] Cross-entropy loss in classification is negative log-likelihood and minimising it is equivalent to minimising KL when the true distribution is fixed.

### Maximum entropy results
- [ ] No constraint beyond finite support over $K$ outcomes: uniform distribution.
- [ ] Bounded continuous support with no other constraint: uniform distribution.
- [ ] Fixed mean on non-negative support: exponential distribution.
- [ ] Fixed mean and variance: Gaussian distribution.
- [ ] More constraints mean less freedom and usually lower maximum possible entropy.

---

## Revision Schedule

### Pass 1 - 35 minutes: concept map
- [ ] Read [[lecture-w6]] summary and the exam relevance section.
- [ ] Write one sentence each for [[information-content]], [[entropy]], [[cross-entropy]], [[kl-divergence]], [[mutual-information]], and [[maximum-entropy-principle]].
- [ ] For each quantity, write what it measures in plain English before writing any equation.
- [ ] Build the relationship chain:
$$
\text{information content} \rightarrow \text{entropy} \rightarrow \text{cross-entropy and KL} \rightarrow \text{mutual information}.
$$
- [ ] Explain why Week 6 formulas are provided but Week 6 is still examinable: the skill is choosing, applying, and interpreting formulas.

### Pass 2 - 45 minutes: entropy mechanics
- [ ] Do [[week6_questions]] Q1 and Q4.
- [ ] Practise entropy calculations with probabilities such as $1/2$, $1/4$, $1/8$, and $1/3$.
- [ ] Compare a uniform distribution with a skewed distribution over the same support.
- [ ] Explain why a distribution with one outcome of probability 1 has entropy 0.
- [ ] Explain why a Gaussian with larger variance has larger differential entropy, while changing only the mean does not change entropy.

### Pass 3 - 50 minutes: KL and cross-entropy mechanics
- [ ] Do [[week6_questions]] Q2, Q5, and Q6.
- [ ] For every KL calculation, label the expectation distribution first: in $D_{\mathrm{KL}}(p\|q)$, weight terms by $p(x)$.
- [ ] For every cross-entropy calculation, compute $-\log q(x)$ first, then weight by $p(x)$.
- [ ] Verify the identity $H(p,q)=H(p)+D_{\mathrm{KL}}(p\|q)$ numerically.
- [ ] Practise explaining KL as extra coding cost, not just "distance".

### Pass 4 - 45 minutes: joint tables and mutual information
- [ ] Do [[week6_questions]] Q7.
- [ ] From a joint table, compute marginals before attempting mutual information.
- [ ] Compute $H(X)$, $H(Y)$, $H(X,Y)$, and use the chain rule to find conditional entropy.
- [ ] Interpret $I(X;Y)=0$ as independence.
- [ ] Interpret high mutual information as strong reduction in uncertainty, not necessarily linear correlation.

### Pass 5 - 25 minutes: maximum entropy principle
- [ ] Do [[week6_questions]] Q3.
- [ ] Memorise the constraint-to-distribution table in this page.
- [ ] Explain why maximum entropy means least biased, not "most random for no reason".
- [ ] Give one Bayesian/ML example: Gaussian noise is a conservative assumption when only mean and variance are known.

### Final 15-minute check
- [ ] Given a problem statement, identify the required Week 6 quantity in under 10 seconds.
- [ ] Solve one entropy calculation, one KL calculation, and one mutual-information calculation from a table.
- [ ] Explain "KL divergence is asymmetric" using a concrete sentence about which distribution supplies the expectation.
- [ ] Explain the maximum entropy principle without using equations.

---

## Worked Example 1 - Entropy and Information Content

### Question

A discrete random variable $X$ takes values $a$, $b$, and $c$ with probabilities:

| Outcome | Probability |
|---------|-------------|
| $a$ | $1/2$ |
| $b$ | $1/4$ |
| $c$ | $1/4$ |

1. Compute the information content of each outcome in bits.
2. Compute $H(X)$.
3. Compare this entropy with a uniform distribution over three outcomes.

### Solution

Information content is $I(x)=-\log_2 p(x)$.

For $a$:
$$
I(a)=-\log_2(1/2)=1 \text{ bit}.
$$

For $b$ and $c$:
$$
I(b)=I(c)=-\log_2(1/4)=2 \text{ bits}.
$$

Entropy is the expected information content:
$$
H(X)
= \frac{1}{2}(1) + \frac{1}{4}(2) + \frac{1}{4}(2)
= 1.5 \text{ bits}.
$$

A uniform distribution over three outcomes has entropy:
$$
\log_2 3 \approx 1.585 \text{ bits}.
$$

The uniform distribution has larger entropy because, over a fixed finite support, entropy is maximised when all outcomes are equally likely. The given distribution is more predictable because outcome $a$ is more likely than the others.

---

## Worked Example 2 - KL Divergence and Cross-Entropy

### Question

Let $p$ and $q$ be distributions over $\{A,B,C\}$:

| Outcome | $p(x)$ | $q(x)$ |
|---------|--------|--------|
| $A$ | $1/2$ | $1/4$ |
| $B$ | $1/4$ | $1/2$ |
| $C$ | $1/4$ | $1/4$ |

1. Compute $D_{\mathrm{KL}}(p\|q)$ in bits.
2. Compute $H(p,q)$.
3. Verify $H(p,q)=H(p)+D_{\mathrm{KL}}(p\|q)$.

### Solution

For $D_{\mathrm{KL}}(p\|q)$, weight every term by $p(x)$:

| Outcome | $p(x)$ | $q(x)$ | $\log_2(p/q)$ | Term |
|---------|--------|--------|----------------|------|
| $A$ | $1/2$ | $1/4$ | $1$ | $1/2$ |
| $B$ | $1/4$ | $1/2$ | $-1$ | $-1/4$ |
| $C$ | $1/4$ | $1/4$ | $0$ | $0$ |

So:
$$
D_{\mathrm{KL}}(p\|q)
= \frac{1}{2}-\frac{1}{4}+0
= 0.25 \text{ bits}.
$$

For cross-entropy, use $q$ inside the log but still weight by $p$:

$$
H(p,q)
= -\sum_x p(x)\log_2 q(x).
$$

The code costs under $q$ are:
$$
-\log_2(1/4)=2,\quad -\log_2(1/2)=1,\quad -\log_2(1/4)=2.
$$

Therefore:
$$
H(p,q)
= \frac{1}{2}(2)+\frac{1}{4}(1)+\frac{1}{4}(2)
= 1.75 \text{ bits}.
$$

Entropy of $p$ is:
$$
H(p)
= \frac{1}{2}(1)+\frac{1}{4}(2)+\frac{1}{4}(2)
= 1.5 \text{ bits}.
$$

Thus:
$$
H(p)+D_{\mathrm{KL}}(p\|q)
= 1.5 + 0.25
= 1.75
= H(p,q).
$$

The interpretation is that $1.5$ bits is the irreducible average coding cost under the true distribution, while the extra $0.25$ bits is the penalty for using the wrong model $q$.

---

## Worked Example 3 - Mutual Information from a Joint Table

### Question

Two binary random variables have joint distribution:

| | $Y=0$ | $Y=1$ |
|-|-------|-------|
| $X=0$ | $1/2$ | $0$ |
| $X=1$ | $0$ | $1/2$ |

1. Compute $H(X)$.
2. Compute $H(X|Y)$.
3. Compute $I(X;Y)$ and interpret it.

### Solution

The marginals are:
$$
p(X=0)=1/2,\quad p(X=1)=1/2.
$$

So:
$$
H(X)
= -\frac{1}{2}\log_2\frac{1}{2}
-\frac{1}{2}\log_2\frac{1}{2}
= 1 \text{ bit}.
$$

Given $Y=0$, $X=0$ with probability 1. Given $Y=1$, $X=1$ with probability 1. Therefore observing $Y$ removes all uncertainty about $X$:
$$
H(X|Y)=0.
$$

Thus:
$$
I(X;Y)=H(X)-H(X|Y)=1-0=1 \text{ bit}.
$$

Interpretation: $Y$ perfectly determines $X$, so the mutual information equals the full entropy of $X$.

---

## Worked Example 4 - Maximum Entropy Short Answer

### Question

You know only that a continuous variable has mean $\mu$ and variance $\sigma^2$. Which distribution should be chosen by the maximum entropy principle, and why?

### Model answer

The maximum entropy distribution is the Gaussian distribution $\mathcal{N}(\mu,\sigma^2)$. The maximum entropy principle says to choose the distribution with the largest entropy among all distributions satisfying the known constraints. Here the known constraints are only the mean and variance, so the Gaussian is the least biased choice: it matches those two facts while adding the least extra structure.

Do not answer that maximum entropy means "most accurate" or "most confident". It means most conservative given the information available.

---

## Extra Practice To Work On

### Drill A - Entropy comparison

Compute entropy in bits for:

| Distribution | Probabilities |
|--------------|---------------|
| $p_1$ | $(1/2,1/2)$ |
| $p_2$ | $(3/4,1/4)$ |
| $p_3$ | $(1,0)$ |
| $p_4$ | $(1/4,1/4,1/4,1/4)$ |

Tasks:
- [ ] Rank the distributions from lowest entropy to highest entropy.
- [ ] State which distribution is deterministic.
- [ ] State which distribution is uniform.
- [ ] Explain why support size matters when comparing maximum possible entropy.

### Drill B - KL direction

Let:
$$
p=(0.8,0.2), \quad q=(0.5,0.5).
$$

Tasks:
- [ ] Compute $D_{\mathrm{KL}}(p\|q)$.
- [ ] Compute $D_{\mathrm{KL}}(q\|p)$.
- [ ] Identify which distribution weights the terms in each calculation.
- [ ] Explain in one sentence why KL is not a distance metric.

### Drill C - Cross-entropy and classification

A binary classifier predicts $\hat{p}=0.9$ for class 1.

Tasks:
- [ ] Compute the cross-entropy loss if the true label is $y=1$.
- [ ] Compute the cross-entropy loss if the true label is $y=0$.
- [ ] Explain why confident wrong predictions are heavily penalised.
- [ ] Explain why minimising cross-entropy is equivalent to maximising likelihood for Bernoulli classification.

### Drill D - Mutual information cases

For each case, decide whether mutual information is zero, positive but not maximal, or maximal:

- [ ] $X$ and $Y$ are independent fair coin flips.
- [ ] $Y=X$ exactly.
- [ ] $Y$ is a noisy copy of $X$.
- [ ] $Y$ is independent of $X$ but has the same marginal distribution.

### Drill E - Maximum entropy table

Fill in the missing distribution:

| Known facts | Max-entropy distribution |
|-------------|--------------------------|
| $K$ discrete outcomes, no other facts | ? |
| Support $[a,b]$, no other facts | ? |
| Non-negative support and fixed mean | ? |
| Fixed mean and variance | ? |

---

## Common Mistakes

- [ ] Treating Week 6 as pure memorisation because formulas are provided. The exam still tests formula selection, calculation, and interpretation.
- [ ] Forgetting the negative sign in entropy and cross-entropy.
- [ ] Mixing log bases. Use base 2 for bits if the question asks for bits; use natural logs for nats if stated.
- [ ] Thinking rare events have low information because they occur rarely. Rare events have high information when they occur.
- [ ] Saying entropy is the surprise of one outcome. That is information content; entropy is average surprise.
- [ ] Claiming the distribution with the largest variance always has largest entropy without checking the family or constraints. For Gaussian comparisons, larger variance means larger differential entropy.
- [ ] Forgetting that differential entropy can be negative.
- [ ] Treating KL divergence as symmetric or as a true distance.
- [ ] In $D_{\mathrm{KL}}(p\|q)$, weighting terms by $q$ instead of $p$.
- [ ] In cross-entropy $H(p,q)$, putting $p$ inside the log instead of $q$.
- [ ] Saying $D_{\mathrm{KL}}(p\|q)=0$ when the distributions are merely similar. It is zero only when they are identical.
- [ ] Forgetting that $I(X;Y)=0$ means independence, not just low correlation.
- [ ] Confusing maximum entropy with maximum likelihood. MaxEnt chooses a least-biased distribution under constraints; MLE chooses parameters that maximise data likelihood.
- [ ] Giving unjustified low-entropy distributions when asked for a maximum entropy distribution.

---

## Exam-Ready Checklist

You are Week 6-ready when you can:

- [ ] Read a question and immediately identify which information-theory quantity is being tested.
- [ ] Compute information content and entropy for a small discrete distribution.
- [ ] Explain why a uniform distribution maximises entropy on a fixed finite support.
- [ ] Compare Gaussian entropies by variance and state that the mean does not affect Gaussian differential entropy.
- [ ] Compute KL divergence from a small table and keep the direction correct.
- [ ] Explain KL divergence as extra coding cost and state that it is asymmetric.
- [ ] Compute cross-entropy and verify $H(p,q)=H(p)+D_{\mathrm{KL}}(p\|q)$.
- [ ] Explain why cross-entropy loss is negative log-likelihood in classification.
- [ ] Compute mutual information from entropy or from a joint table.
- [ ] State that mutual information is zero iff variables are independent.
- [ ] State the maximum entropy distribution for no constraints, fixed mean on non-negative support, and fixed mean plus variance.
- [ ] Distinguish formulas to apply from derivations to understand: Week 6 derivations are not examinable, but the interpretations are.
