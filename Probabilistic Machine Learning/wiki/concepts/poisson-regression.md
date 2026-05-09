# Poisson Regression

**Type:** model
**Week:** 2
**Related:** [[generalised-linear-models]], [[linear-regression]]
**Source:** [[lecture-w2]]

## Definition
Poisson regression is a Generalised Linear Model (GLM) specifically used for modelling count data, where the output is assumed to follow a Poisson distribution.

## Motivation
Standard [[linear-regression]] assumes Gaussian noise and predicts continuous, unbounded outputs ($-\infty$ to $+\infty$). However, when predicting count data (e.g., number of emails, website clicks, or traffic accidents), the output must be a non-negative integer ($0, 1, 2, \dots$). If standard linear regression is used for counts, the linear predictor ($\mathbf{w}^\top \mathbf{x}$) could output negative values, which makes no physical or mathematical sense. Poisson regression solves this by using a distribution and link function appropriate for counts.

## How it works
Poisson regression uses the **Poisson distribution**, which is defined by a single parameter $\lambda$ (the rate or mean). Because a mean count cannot be negative, we must enforce $\lambda > 0$.

To connect the unbounded linear predictor $\eta_i = \mathbf{w}^\top \mathbf{x}_i$ to the strictly positive mean $\lambda_i$, we use the **log link function**:
$$ \log(\lambda_i) = \mathbf{w}^\top \mathbf{x}_i $$

By applying the inverse link function (the exponential), we guarantee that the predicted mean is always positive, regardless of the values of $\mathbf{w}$ or $\mathbf{x}$:
$$ \lambda_i = \exp(\mathbf{w}^\top \mathbf{x}_i) $$

### The Generative Process
1. **Linear predictor:** Calculate $\eta_i = \mathbf{w}^\top \mathbf{x}_i$ (can be any value).
2. **Activation (Inverse Link):** Map $\eta_i$ to the rate parameter $\lambda_i = \exp(\eta_i)$ (guaranteed $> 0$).
3. **Observation:** Sample the observed count $y_i \sim \text{Poisson}(\lambda_i)$.

## Key derivation
There is no closed-form solution (like the Normal Equations) for finding the optimal weights $\mathbf{w}$ in Poisson regression because $\mathbf{w}$ appears inside the non-linear exponential function.

The log-likelihood for the Poisson distribution is:
$$ \ell(\mathbf{w}) = \sum_{i=1}^N \left( y_i (\mathbf{w}^\top \mathbf{x}_i) - \exp(\mathbf{w}^\top \mathbf{x}_i) - \log(y_i!) \right) $$

Maximum likelihood estimation (MLE) requires **iterative optimization** methods such as:
- **Gradient ascent**
- **Newton-Raphson**
- **Iteratively Reweighted Least Squares (IRLS)**

⚠️ *No formula given in exam. Understand the concept.*

## Parameters & intuition
- $\lambda$: The expected count or rate. Represents both the mean and the variance in a Poisson distribution.
- $\mathbf{w}$: The weights. Because of the log link, a one-unit change in $x_j$ multiplies the expected count by $\exp(w_j)$ (a multiplicative effect, rather than the additive effect seen in standard linear regression).

## Worked example sketch
If predicting the number of phone calls received at a call centre based on the number of active agents ($x_1$) and the time of day ($x_2$), Poisson regression ensures the model will never predict a negative number of calls.

## Connections
- A specific instance of [[generalised-linear-models]].
- Contrasts with standard [[linear-regression]] which uses an identity link and Gaussian distribution.

## Exam notes
- Understand why standard linear regression is inappropriate for count data.
- Know the link function (log link) and inverse link (exponential) for Poisson regression.
- Recall that MLE for Poisson regression requires iterative optimisation.

## Breakdown of an Example:

![[MLE_Poisson_Regression_SLIDE.png]]

This slide shows the mathematical engine of how we train a Poisson regression model. The overarching goal here is Maximum Likelihood Estimation (MLE): we are trying to find the specific set of weights ($w$) that make the data we actually observed ($y$) as highly probable as possible.

Here is the step-by-step breakdown of exactly what is happening in the math.

### 1. The Starting Point: The Likelihood Function
$$p(\mathbf{y} \mid X, w) = \prod_{i=1}^n \frac{\lambda_i^{y_i} e^{-\lambda_i}}{y_i!}$$
* **What this means:** This is the probability of observing our entire dataset (all $y$'s). Because each observation is assumed to be independent, we calculate the total probability by multiplying ($\prod$) the individual probabilities together.
* **Where it comes from:** The fraction $\frac{\lambda^y e^{-\lambda}}{y!}$ is just the standard formula for the Poisson distribution (the probability of getting exactly $y$ events when the average rate is $\lambda$).

### 2. The Substitution: Connecting the Model to the Math
$$Substitute \ \lambda_i = \exp(w^\top x_i)$$
* **Why are we doing this?** In the first equation, we just have $\lambda_i$ (an abstract rate parameter). But we are building a regression model! We want our features ($x$) and our learnable weights ($w$) to predict that rate.
* **Where did it come from?** This is the **inverse link function** (the "activation function") we discussed earlier. We use $\exp(w^\top x_i)$ to ensure our predicted rate is always a positive number.
* **The resulting equation:** By plugging $\exp(w^\top x_i)$ in place of every $\lambda_i$ in the Poisson formula, we get:
  $$p(\mathbf{y} \mid X, w) = \prod_{i=1}^n \frac{\exp(y_i w^\top x_i) \exp(-\exp(w^\top x_i))}{y_i!}$$
  (Note: $\lambda_i^{y_i}$ became $(\exp(w^\top x_i))^{y_i}$, which simplifies to $\exp(y_i w^\top x_i)$).

### 3. The Log-Likelihood: Making the Math Solvable
$$\ell(w) = \log p(\mathbf{y} \mid X, w)$$
* **What are we trying to accomplish?** The equation in Step 2 is a massive product ($\prod$) of fractions and exponents. If you try to find the maximum of that by taking the derivative, the calculus is a nightmare (the product rule applied $n$ times). Furthermore, computers struggle with it because multiplying hundreds of tiny probabilities together results in "numerical underflow" (the computer just rounds it to zero).
* **The trick:** We take the natural logarithm ($\log$) of the whole thing. Logarithms have magical properties: they turn products into sums ($\log(A \times B) = \log(A) + \log(B)$), and they cancel out exponentials ($\log(e^x) = x$). Because the logarithm is a strictly increasing function, the weights $w$ that maximize the log-likelihood are the exact same weights that maximize the original likelihood.

Let's apply the log rules to one data point:
$$ \log \left( \frac{\exp(y_i w^\top x_i) \cdot \exp(-\exp(w^\top x_i))}{y_i!} \right) $$
$$ = \log(\exp(y_i w^\top x_i)) + \log(\exp(-\exp(w^\top x_i))) - \log(y_i!) $$
$$ = y_i w^\top x_i - \exp(w^\top x_i) - \log(y_i!) $$

When we sum this over all $n$ data points, we get the elegant objective function shown on the slide:
$$\ell(w) = \sum_{i=1}^n \left[ y_i w^\top x_i - \exp(w^\top x_i) - \log(y_i!) \right]$$

### 4. The Final Goal
$$\widehat{w}_{MLE} = \arg\max_w \ell(w)$$
* **What this means:** "Find the specific values for the weights ($\widehat{w}$) that result in the absolute maximum possible value ($\arg\max$) for our log-likelihood function ($\ell(w)$)."
* **How we accomplish it:** To find the peak of this curve, we would take the derivative with respect to $w$ and set it to zero. As mentioned earlier, because $w$ is trapped inside that $-\exp(w^\top x_i)$ term, we can't solve it with basic algebra, so we hand this log-likelihood function over to an iterative algorithm (like Gradient Ascent) to find the top of the hill.