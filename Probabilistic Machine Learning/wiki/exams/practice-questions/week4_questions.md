# Week 4 Practice Questions — Variational Inference & ELBO

> ⚠️ **Formula policy:** No formulas are provided in the exam for Week 4. All expressions must be recalled from memory.

---

## Conceptual / Bookwork

### Q1. Why is variational inference needed?

**(a)** Explain why exact Bayesian inference is often intractable. What quantity are we trying to compute, and what makes it hard?
*(3 marks)*

**(b)** State the variational inference objective. In your answer, write down the expression being minimised and define all symbols.
*(3 marks)*

**(c)** Variational inference uses the **reverse** KL divergence $\text{KL}(q \| p)$ rather than the forward KL $\text{KL}(p \| q)$. Give **two** reasons why the forward KL is impractical in this setting, and describe in words the qualitative behaviour of an approximation $q$ that minimises the reverse KL.
*(4 marks)*

---

### Q2. Properties of the ELBO

**(a)** Write down the Evidence Lower Bound $\mathcal{L}(q)$ in **two** equivalent forms:

1. In terms of $\mathbb{E}_q[\log p(\mathcal{D}, \theta)]$ and $\mathbb{E}_q[\log q(\theta)]$.
2. In terms of an expected log-likelihood and a KL divergence from $q$ to the prior.

For each form, identify what each term represents conceptually.
*(4 marks)*

**(b)** The ELBO is called a "lower bound." Prove this claim in one or two lines using the decomposition

$$\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q(\theta) \| p(\theta|\mathcal{D}))$$

and a standard property of KL divergence.
*(2 marks)*

**(c)** Under what condition does the lower bound become **tight** (i.e. $\mathcal{L}(q) = \log p(\mathcal{D})$)? What is the significance of this condition?
*(2 marks)*

---

### Q3. Variational Inference vs Laplace Approximation

Compare variational inference and the Laplace approximation as methods for approximating an intractable posterior $p(\theta|\mathcal{D})$.

**(a)** Describe how the Laplace approximation constructs its approximation $q(\theta)$, and state **two** key limitations it has for realistic posteriors.
*(3 marks)*

**(b)** In what sense is variational inference a **global** approximation while the Laplace approximation is **local**? Why does this distinction matter in practice?
*(3 marks)*

**(c)** Both methods produce a Gaussian approximation in common settings. Despite this, they can give very different results. Briefly explain why.
*(2 marks)*

---

## Derivations

### Q4. Full ELBO Derivation ⚠️ *No formula given*

This question requires you to derive the Evidence Lower Bound from first principles.

**(a)** Write down the KL divergence from the variational distribution $q(\theta)$ to the true posterior $p(\theta|\mathcal{D})$ as an integral. Then express it as an expectation under $q$.
*(2 marks)*

**(b)** The true posterior $p(\theta|\mathcal{D})$ is intractable. Apply Bayes' rule to substitute it, writing the posterior in terms of the joint $p(\mathcal{D}, \theta)$ and the evidence $p(\mathcal{D})$. Show that the KL divergence becomes:

$$\text{KL}(q(\theta) \| p(\theta|\mathcal{D})) = \log p(\mathcal{D}) + \mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\mathcal{D}, \theta)]$$

Justify why $\log p(\mathcal{D})$ may be taken outside the expectation.
*(4 marks)*

**(c)** Rearrange the expression from part (b) to obtain:

$$\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q(\theta) \| p(\theta|\mathcal{D}))$$

and identify $\mathcal{L}(q)$ explicitly.
*(2 marks)*

**(d)** Using the decomposition in part (c), explain why maximising $\mathcal{L}(q)$ with respect to $q$ is equivalent to minimising $\text{KL}(q(\theta) \| p(\theta|\mathcal{D}))$. Be precise about what quantity is being held constant.
*(2 marks)*

**(e)** Starting from $\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}, \theta)] - \mathbb{E}_q[\log q(\theta)]$, use the factorisation $p(\mathcal{D}, \theta) = p(\mathcal{D}|\theta)\,p(\theta)$ to rewrite the ELBO in the form:

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta) \| p(\theta))$$

Interpret each term.
*(3 marks)*

---

## Practical / Calculation

### Q5. Computing KL Divergence between Gaussians ⚠️ *No formula given*

Let $q(\theta) = \mathcal{N}(\theta \mid \mu_q, \sigma_q^2)$ and $p(\theta) = \mathcal{N}(\theta \mid \mu_p, \sigma_p^2)$ be univariate Gaussians.

**(a)** Write down the general definition of $\text{KL}(q \| p)$ as an integral.
*(1 mark)*

**(b)** For the specific case $q(\theta) = \mathcal{N}(1, 1)$ and $p(\theta) = \mathcal{N}(0, 4)$ (i.e. $\mu_q=1$, $\sigma_q^2=1$, $\mu_p=0$, $\sigma_p^2=4$), compute $\text{KL}(q \| p)$ using the closed-form result for KL between univariate Gaussians:

$$\text{KL}(q \| p) = \log\frac{\sigma_p}{\sigma_q} + \frac{\sigma_q^2 + (\mu_q - \mu_p)^2}{2\sigma_p^2} - \frac{1}{2}$$

Show all substitution steps clearly.
*(3 marks)*

**(c)** Is $\text{KL}(q\|p) = \text{KL}(p\|q)$ in general? Compute $\text{KL}(p \| q)$ for the same distributions above and verify that they differ. What does this asymmetry mean for variational inference?
*(3 marks)*

---

### Q6. Manipulating the ELBO ⚠️ *No formula given*

Suppose we use a Gaussian variational family $q(\theta|\lambda) = \mathcal{N}(\theta \mid \mu, \sigma^2)$ with variational parameters $\lambda = (\mu, \sigma^2)$, and the model has a Gaussian prior $p(\theta) = \mathcal{N}(\theta \mid 0, 1)$.

**(a)** Write down the ELBO in the form $\mathcal{L}(\lambda) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta|\lambda) \| p(\theta))$. Identify which term is tractable analytically and which typically requires numerical approximation.
*(2 marks)*

**(b)** The KL term can be computed analytically. Using the formula from Q5(b), write out $\text{KL}(\mathcal{N}(\mu, \sigma^2) \| \mathcal{N}(0, 1))$ in simplified form.
*(2 marks)*

**(c)** Consider varying $\sigma^2$ while holding $\mu$ fixed. Sketch (or describe in words) how the KL term $\text{KL}(q \| p(\theta))$ behaves as $\sigma^2 \to 0$ and as $\sigma^2 \to \infty$, and explain the intuition in terms of the ELBO objective.
*(3 marks)*

---

## Answers / Mark Schemes

---

### A1. Why is variational inference needed?

**(a)** *(3 marks)*
The target quantity is the posterior $p(\theta|\mathcal{D})$. By Bayes' rule:

$$p(\theta|\mathcal{D}) = \frac{p(\mathcal{D}|\theta)\,p(\theta)}{p(\mathcal{D})}, \qquad p(\mathcal{D}) = \int p(\mathcal{D}|\theta)\,p(\theta)\,d\theta$$

The denominator $p(\mathcal{D})$ — the marginal likelihood or evidence — requires integrating over all possible parameter values. For most realistic models (e.g. non-conjugate likelihoods, high-dimensional $\theta$) this integral is analytically intractable.

*Mark: 1 mark for stating the posterior; 1 mark for identifying the evidence integral as the problem; 1 mark for explaining why it is intractable (no closed form, high-dimensional integral).*

**(b)** *(3 marks)*
The VI objective is:

$$q^* = \arg\min_{q \in \mathcal{Q}} \text{KL}(q(\theta) \| p(\theta|\mathcal{D}))$$

$$\text{KL}(q(\theta) \| p(\theta|\mathcal{D})) = \int q(\theta) \log \frac{q(\theta)}{p(\theta|\mathcal{D})}\,d\theta = \mathbb{E}_q\!\left[\log q(\theta) - \log p(\theta|\mathcal{D})\right]$$

where $q \in \mathcal{Q}$ is a variational distribution chosen from a tractable family, and the goal is to find the member of that family closest (in KL) to the true posterior.

*Mark: 1 mark for the argmin form; 1 mark for the KL integral/expectation; 1 mark for defining symbols (q family, true posterior).*

**(c)** *(4 marks)*
Two reasons forward KL is impractical:

1. $\text{KL}(p\|q) = \int p(\theta|\mathcal{D}) \log \frac{p(\theta|\mathcal{D})}{q(\theta)}\,d\theta$ — the expectation is taken **under** $p(\theta|\mathcal{D})$, which we cannot sample from (it is the quantity we are trying to approximate).
2. Evaluating $p(\theta|\mathcal{D})$ pointwise requires the intractable evidence $p(\mathcal{D})$.

Qualitative behaviour of reverse-KL solution: $q$ is **mode-seeking**. If $q(x) > 0$ where $p(x|\mathcal{D}) \approx 0$, then $\log(q/p)$ becomes very large, creating a heavy penalty. So $q$ concentrates on regions where $p$ has high mass, potentially latching onto a single mode and **underestimating** the spread/uncertainty of the posterior.

*Mark: 1 mark each for two valid reasons (2 marks total); 2 marks for correct description of mode-seeking behaviour with explanation of the zero-forcing penalty.*

---

### A2. Properties of the ELBO

**(a)** *(4 marks)*

Form 1 (joint form):
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}, \theta)] - \mathbb{E}_q[\log q(\theta)]$$
— the first term is the expected log-joint; the second is the (negative) entropy of $q$.

Form 2 (likelihood–KL form):
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$
— the first term measures data fit (expected log-likelihood); the second penalises deviation of $q$ from the prior (complexity penalty / regularisation).

*Mark: 1 mark per form correctly written; 1 mark per correct conceptual interpretation (2 marks for interpretations).*

**(b)** *(2 marks)*
From the decomposition: $\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q\|p(\theta|\mathcal{D}))$.

Since $\text{KL}(q\|p(\theta|\mathcal{D})) \geq 0$ (non-negativity of KL, with equality iff $q = p(\theta|\mathcal{D})$), we have $\mathcal{L}(q) \leq \log p(\mathcal{D})$.

*Mark: 1 mark for invoking KL $\geq 0$; 1 mark for concluding the bound.*

**(c)** *(2 marks)*
The bound is tight ($\mathcal{L}(q) = \log p(\mathcal{D})$) if and only if $\text{KL}(q\|p(\theta|\mathcal{D})) = 0$, which holds iff $q(\theta) = p(\theta|\mathcal{D})$ almost everywhere. This means $q$ perfectly recovers the true posterior — the ELBO objective achieves its global maximum precisely when the approximation is exact.

*Mark: 1 mark for the condition $q = p(\theta|\mathcal{D})$; 1 mark for the significance (ELBO at global max, bound exact).*

---

### A3. VI vs Laplace Approximation

**(a)** *(3 marks)*
The Laplace approximation locates the MAP estimate $\hat\theta = \arg\max_\theta p(\theta|\mathcal{D})$, then fits a Gaussian at that point using the local curvature (second-order Taylor expansion of the log-posterior):

$$q(\theta) = \mathcal{N}(\theta \mid \hat\theta,\ [-\nabla^2 \log p(\hat\theta|\mathcal{D})]^{-1})$$

Two key limitations:
1. **Captures only one mode**: if the posterior is multimodal, Laplace ignores all but the mode at $\hat\theta$.
2. **Assumes near-Gaussian shape**: it forces symmetry; fails for skewed or heavy-tailed posteriors.

*Mark: 1 mark for correct description; 1 mark per limitation.*

**(b)** *(3 marks)*
**Local**: Laplace uses only information at and immediately around the mode — the curvature $\nabla^2 \log p$ is evaluated at $\hat\theta$ alone. If the posterior has interesting structure away from the mode (other peaks, long tails), Laplace misses it entirely.

**Global**: VI solves an optimisation problem that considers the entire posterior surface via the KL objective. The optimal $q^*$ minimises the average (expected) log ratio over all of parameter space, so it accounts for the global shape of $p(\theta|\mathcal{D})$.

This matters because realistic posteriors are often multimodal or skewed; a global approximation can represent these features better (at least partially), whereas Laplace will always return a symmetric unimodal fit.

*Mark: 1 mark for explaining "local" correctly; 1 mark for explaining "global" correctly; 1 mark for why the distinction matters.*

**(c)** *(2 marks)*
Although both can produce Gaussian approximations, they are found by different mechanisms: Laplace matches the mode and local curvature (no explicit optimisation over a distributional criterion), while VI minimises KL divergence globally. For a skewed posterior, Laplace will be symmetric around the mode; the VI Gaussian (especially with reverse KL, mode-seeking) may shift its mean slightly and adjust variance to better cover high-probability regions, potentially giving a different mean and variance than Laplace.

*Mark: 1 mark for identifying different criteria; 1 mark for noting the practical consequence (different mean/variance for non-Gaussian posteriors).*

---

### A4. Full ELBO Derivation

**(a)** *(2 marks)*

$$\text{KL}(q(\theta) \| p(\theta|\mathcal{D})) = \int q(\theta) \log \frac{q(\theta)}{p(\theta|\mathcal{D})}\,d\theta = \mathbb{E}_q\!\left[\log q(\theta) - \log p(\theta|\mathcal{D})\right]$$

*Mark: 1 mark for integral form; 1 mark for expectation form.*

**(b)** *(4 marks)*

Apply Bayes' rule: $p(\theta|\mathcal{D}) = \dfrac{p(\mathcal{D},\theta)}{p(\mathcal{D})}$.

Substitute:

$$\text{KL}(q\|p(\theta|\mathcal{D})) = \int q(\theta)\log\frac{q(\theta)}{p(\mathcal{D},\theta)/p(\mathcal{D})}\,d\theta = \int q(\theta)\left[\log q(\theta) + \log p(\mathcal{D}) - \log p(\mathcal{D},\theta)\right]d\theta$$

Since $\log p(\mathcal{D})$ does not depend on $\theta$, and $\int q(\theta)\,d\theta = 1$:

$$= \log p(\mathcal{D}) + \int q(\theta)\log q(\theta)\,d\theta - \int q(\theta)\log p(\mathcal{D},\theta)\,d\theta$$

$$= \log p(\mathcal{D}) + \mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\mathcal{D},\theta)]$$

*Mark: 1 mark for applying Bayes' rule correctly; 1 mark for expanding the log of a ratio; 1 mark for factoring out $\log p(\mathcal{D})$ with justification; 1 mark for the final expectation form.*

**(c)** *(2 marks)*

Rearrange the expression from (b):

$$\log p(\mathcal{D}) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)]}_{\mathcal{L}(q)} + \text{KL}(q(\theta)\|p(\theta|\mathcal{D}))$$

So:
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)]$$

*Mark: 1 mark for correct rearrangement; 1 mark for correctly identifying $\mathcal{L}(q)$.*

**(d)** *(2 marks)*

From the decomposition: $\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q\|p(\theta|\mathcal{D}))$.

$\log p(\mathcal{D})$ is a constant with respect to $q$ (it is the marginal likelihood, determined entirely by the model and data, not by our choice of $q$). Therefore, increasing $\mathcal{L}(q)$ must decrease $\text{KL}(q\|p(\theta|\mathcal{D}))$ by the same amount, and vice versa. Hence:

$$\arg\max_q \mathcal{L}(q) \iff \arg\min_q \text{KL}(q(\theta)\|p(\theta|\mathcal{D}))$$

*Mark: 1 mark for identifying $\log p(\mathcal{D})$ as constant w.r.t. $q$; 1 mark for the equivalence argument.*

**(e)** *(3 marks)*

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)]$$

Use $p(\mathcal{D},\theta) = p(\mathcal{D}|\theta)\,p(\theta)$:

$$= \mathbb{E}_q[\log p(\mathcal{D}|\theta) + \log p(\theta)] - \mathbb{E}_q[\log q(\theta)]$$

$$= \mathbb{E}_q[\log p(\mathcal{D}|\theta)] + \mathbb{E}_q[\log p(\theta)] - \mathbb{E}_q[\log q(\theta)]$$

$$= \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \left(\mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\theta)]\right)$$

$$= \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$

Interpretation:
- $\mathbb{E}_q[\log p(\mathcal{D}|\theta)]$: **data fit** — reward for $q$ placing mass on parameters that explain the data well.
- $\text{KL}(q(\theta)\|p(\theta))$: **complexity penalty** — penalises $q$ for deviating from the prior; prevents overfitting.

*Mark: 1 mark for the factorisation step; 1 mark for algebraic grouping into KL form; 1 mark for correct interpretation of both terms.*

---

### A5. Computing KL Divergence between Gaussians

**(a)** *(1 mark)*

$$\text{KL}(q\|p) = \int q(\theta)\log\frac{q(\theta)}{p(\theta)}\,d\theta$$

*Mark: 1 mark for correct integral definition.*

**(b)** *(3 marks)*

Given: $\mu_q = 1$, $\sigma_q^2 = 1$, $\mu_p = 0$, $\sigma_p^2 = 4$ (so $\sigma_p = 2$, $\sigma_q = 1$).

$$\text{KL}(q\|p) = \log\frac{\sigma_p}{\sigma_q} + \frac{\sigma_q^2 + (\mu_q - \mu_p)^2}{2\sigma_p^2} - \frac{1}{2}$$

$$= \log\frac{2}{1} + \frac{1 + (1-0)^2}{2 \times 4} - \frac{1}{2}$$

$$= \log 2 + \frac{1 + 1}{8} - \frac{1}{2}$$

$$= \log 2 + \frac{2}{8} - \frac{1}{2}$$

$$= \log 2 + \frac{1}{4} - \frac{1}{2}$$

$$= \log 2 - \frac{1}{4} \approx 0.693 - 0.25 = 0.443$$

*Mark: 1 mark for correct substitution; 1 mark for correct arithmetic; 1 mark for final numerical answer (accept $\ln 2 - 1/4$ or decimal approximation).*

**(c)** *(3 marks)*

No, $\text{KL}(q\|p) \neq \text{KL}(p\|q)$ in general — KL divergence is asymmetric.

Compute $\text{KL}(p\|q)$ with $\mu_p=0$, $\sigma_p^2=4$, $\mu_q=1$, $\sigma_q^2=1$:

$$\text{KL}(p\|q) = \log\frac{\sigma_q}{\sigma_p} + \frac{\sigma_p^2 + (\mu_p - \mu_q)^2}{2\sigma_q^2} - \frac{1}{2}$$

$$= \log\frac{1}{2} + \frac{4 + (0-1)^2}{2 \times 1} - \frac{1}{2}$$

$$= -\log 2 + \frac{4 + 1}{2} - \frac{1}{2}$$

$$= -\log 2 + \frac{5}{2} - \frac{1}{2}$$

$$= -\log 2 + 2 \approx -0.693 + 2 = 1.307$$

Since $0.443 \neq 1.307$, the divergences differ. The asymmetry matters because in VI we minimise $\text{KL}(q\|p(\theta|\mathcal{D}))$ (reverse KL), which leads to mode-seeking behaviour. If we minimised $\text{KL}(p\|q)$ (forward KL), we would get a mass-covering approximation — but this is computationally infeasible because it requires expectations under the intractable true posterior.

*Mark: 1 mark for stating asymmetry; 1 mark for correct computation of $\text{KL}(p\|q)$; 1 mark for explaining the implication for VI.*

---

### A6. Manipulating the ELBO

**(a)** *(2 marks)*

$$\mathcal{L}(\lambda) = \mathbb{E}_{q(\theta|\lambda)}[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta|\lambda)\|p(\theta))$$

- The **KL term** $\text{KL}(\mathcal{N}(\mu,\sigma^2)\|\mathcal{N}(0,1))$ is analytically tractable (closed form for Gaussians).
- The **expected log-likelihood** $\mathbb{E}_q[\log p(\mathcal{D}|\theta)]$ typically requires numerical approximation (e.g. Monte Carlo sampling) unless the likelihood is also Gaussian.

*Mark: 1 mark for correctly writing the ELBO; 1 mark for correctly identifying which term is analytic.*

**(b)** *(2 marks)*

Using the formula with $\mu_q=\mu$, $\sigma_q^2=\sigma^2$, $\mu_p=0$, $\sigma_p^2=1$:

$$\text{KL}(\mathcal{N}(\mu,\sigma^2)\|\mathcal{N}(0,1)) = \log\frac{1}{\sigma} + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2} = -\frac{1}{2}\log\sigma^2 + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2}$$

Or equivalently: $\tfrac{1}{2}(\mu^2 + \sigma^2 - 1 - \log\sigma^2)$.

*Mark: 1 mark for correct substitution; 1 mark for correct simplification.*

**(c)** *(3 marks)*

With $\mu$ fixed, the KL term as a function of $\sigma^2$ is $\tfrac{1}{2}(\mu^2 + \sigma^2 - 1 - \log\sigma^2)$.

- As $\sigma^2 \to 0$: $-\log\sigma^2 \to +\infty$, so $\text{KL} \to +\infty$. A vanishing variance places all mass at a point mass; the prior $\mathcal{N}(0,1)$ has non-negligible spread, so the KL penalty for being too narrow becomes unbounded.
- As $\sigma^2 \to \infty$: the $\sigma^2$ term dominates and $\text{KL} \to +\infty$. A very diffuse $q$ also incurs a large penalty for deviating far from the prior's scale.

The KL is minimised at a finite $\sigma^2 = 1$ (when $\mu = 0$, $q = p$). In the ELBO objective, the KL acts as a regulariser: it prevents $q$ from collapsing to a point mass (which could overfit) or spreading too broadly (which ignores the prior's information). The data-fit term $\mathbb{E}_q[\log p(\mathcal{D}|\theta)]$ balances against the KL to determine the optimal $\sigma^2$.

*Mark: 1 mark for $\sigma^2 \to 0$ behaviour with justification; 1 mark for $\sigma^2 \to \infty$ behaviour with justification; 1 mark for interpretation in terms of ELBO balance between data fit and regularisation.*
