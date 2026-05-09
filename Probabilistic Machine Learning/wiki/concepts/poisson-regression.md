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

