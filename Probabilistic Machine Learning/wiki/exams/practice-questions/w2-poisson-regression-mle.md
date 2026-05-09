# Practice Question: Poisson Regression & GLMs

**Topic:** Poisson Regression, Generalised Linear Models (GLMs), Maximum Likelihood Estimation (MLE)
**Week:** 2
**Related Concepts:** [[poisson-regression]], [[generalised-linear-models]], [[mle]]

## Question

A retail company wants to model the number of customer purchases per hour at their store, denoted as $y_i$, based on a set of features $\mathbf{x}_i$ (such as time of day, day of the week, and active promotions). They have collected a dataset $\mathcal{D} = \{(\mathbf{x}_1, y_1), \dots, (\mathbf{x}_N, y_N)\}$. The data scientist decides to model this using a Generalised Linear Model (GLM).

**(a)** Explain why standard linear regression is inappropriate for modelling the number of customer purchases, and state the appropriate distribution and link function the data scientist should use for this task. *(3 marks)*

**(b)** Let $\mathbf{w}$ be the weight vector. Write down the equation that connects the linear predictor $\eta_i = \mathbf{w}^\top\mathbf{x}_i$ to the expected number of purchases $\lambda_i = \mathbb{E}[y_i|\mathbf{x}_i]$. *(2 marks)*

**(c)** The probability mass function for the Poisson distribution is given by:
$$ P(y_i | \lambda_i) = \frac{\lambda_i^{y_i} \exp(-\lambda_i)}{y_i!} $$
Derive the complete log-likelihood function $\ell(\mathbf{w})$ for the dataset $\mathcal{D}$ in terms of the weights $\mathbf{w}$, the features $\mathbf{x}_i$, and the targets $y_i$. *(5 marks)*

**(d)** By differentiating the log-likelihood function with respect to $\mathbf{w}$, explain why finding the Maximum Likelihood Estimate (MLE) for $\mathbf{w}$ cannot be solved with a closed-form formula (like the Normal Equations in linear regression) and state how one would solve it in practice. *(4 marks)*

---

## Solution

### Part (a)
Standard linear regression assumes that the target variable $y_i$ is continuous and unbounded (can range from $-\infty$ to $+\infty$), and that the noise follows a Gaussian distribution. However, the number of customer purchases $y_i$ is **count data**, meaning it must be a non-negative integer ($0, 1, 2, \dots$). Standard linear regression could predict negative purchases, which is physically impossible. 

To model this appropriately as a GLM, we should assume the target follows a **Poisson distribution** and use the **log link function** ($\eta_i = \log \lambda_i$) to connect the linear predictor to the mean.

### Part (b)
The link function is $\log(\lambda_i) = \mathbf{w}^\top\mathbf{x}_i$. 
To find the equation for the expected number of purchases $\lambda_i$, we apply the inverse link function (the exponential):
$$ \lambda_i = \exp(\mathbf{w}^\top\mathbf{x}_i) $$

### Part (c)
First, write down the likelihood function for the dataset, assuming independent and identically distributed (i.i.d.) observations:
$$ \mathcal{L}(\mathbf{w}) = \prod_{i=1}^N P(y_i | \mathbf{x}_i, \mathbf{w}) = \prod_{i=1}^N \frac{\lambda_i^{y_i} \exp(-\lambda_i)}{y_i!} $$

Next, take the natural logarithm to get the log-likelihood:
$$ \ell(\mathbf{w}) = \log \mathcal{L}(\mathbf{w}) = \sum_{i=1}^N \left( y_i \log \lambda_i - \lambda_i - \log(y_i!) \right) $$

Finally, substitute the inverse link function $\lambda_i = \exp(\mathbf{w}^\top\mathbf{x}_i)$ into the log-likelihood:
$$ \ell(\mathbf{w}) = \sum_{i=1}^N \left( y_i (\mathbf{w}^\top\mathbf{x}_i) - \exp(\mathbf{w}^\top\mathbf{x}_i) - \log(y_i!) \right) $$

### Part (d)
To find the MLE, we need to take the gradient of the log-likelihood with respect to $\mathbf{w}$ and set it to zero. 
Taking the derivative of $\ell(\mathbf{w})$ with respect to $\mathbf{w}$:
$$ \nabla_\mathbf{w} \ell(\mathbf{w}) = \sum_{i=1}^N \left( y_i \mathbf{x}_i - \exp(\mathbf{w}^\top\mathbf{x}_i) \mathbf{x}_i \right) = \sum_{i=1}^N (y_i - \lambda_i)\mathbf{x}_i $$

Setting this gradient to zero:
$$ \sum_{i=1}^N y_i \mathbf{x}_i = \sum_{i=1}^N \exp(\mathbf{w}^\top\mathbf{x}_i) \mathbf{x}_i $$

We cannot isolate $\mathbf{w}$ algebraically on one side of this equation because $\mathbf{w}$ appears inside the non-linear exponential function $\exp(\mathbf{w}^\top\mathbf{x}_i)$ on the right-hand side, alongside linear terms. Therefore, there is **no closed-form analytical solution**. 

In practice, we must find the optimal weights $\mathbf{w}_{MLE}$ using **iterative numerical optimisation algorithms**, such as gradient ascent or the Newton-Raphson method.
