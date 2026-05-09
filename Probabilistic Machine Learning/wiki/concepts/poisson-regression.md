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
1. Calculate the linear predictor: $\eta_i = \mathbf{w}^\top \mathbf{x}_i$
2. Map to the rate parameter using the inverse link: $\lambda_i = \exp(\eta_i)$
3. Sample the observed count: $y_i \sim \text{Poisson}(\lambda_i)$

## Key derivation
There is no closed-form solution (like the Normal Equations) for finding the optimal weights $\mathbf{w}$ in Poisson regression. 
The log-likelihood for the Poisson distribution is:
$$ \ell(\mathbf{w}) = \sum_{i=1}^N \left( y_i \log \lambda_i - \lambda_i - \log(y_i!) \right) $$
Substituting $\lambda_i = \exp(\mathbf{w}^\top \mathbf{x}_i)$, the maximum likelihood estimation (MLE) requires iterative gradient-based optimization methods (e.g., gradient ascent or Newton-Raphson). 

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
