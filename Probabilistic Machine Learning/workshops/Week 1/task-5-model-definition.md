# Task 5 — Model Definition and Parameter Settings

**Notebook cell:** the `torch.nn.Linear`, `torch.optim.Adam`, `CrossEntropyLoss` cell.
**Goal:** Specify three things — the **model**, the **optimiser**, and the **loss** — that together determine what "training" actually does.

## The intuition

These three objects are the architecture of the experiment. Every later cell just turns the crank:

| Object | Answers the question |
|---|---|
| Model | "What family of functions am I searching over?" |
| Loss  | "How do I measure how wrong a candidate function is?" |
| Optimiser | "How do I move towards a less-wrong candidate?" |

Choose all three and a deterministic gradient-descent run is fully specified.

## Cell-by-cell

```python
model = torch.nn.Linear(4, 3)   # 4 features, 3 classes
opt = torch.optim.Adam(model.parameters(), lr=0.05)
loss_fn = torch.nn.CrossEntropyLoss()
```

### `torch.nn.Linear(4, 3)` — the model

This is one affine map:

$$
z = W x + b, \qquad W \in \mathbb{R}^{3 \times 4}, \; b \in \mathbb{R}^{3}.
$$

Inputs $x \in \mathbb{R}^4$ (the four standardised features), outputs $z \in \mathbb{R}^3$ (one logit per class). There is no hidden layer, no activation, nothing nonlinear — it is the simplest possible neural network.

**This is multinomial [[logistic-regression]]** in PyTorch clothing. The softmax that turns logits into probabilities,

$$
p(y = k \mid x) = \frac{\exp(z_k)}{\sum_{j=1}^{3} \exp(z_j)},
$$

is *not* applied here — it is folded into the loss function below for numerical stability.

PyTorch initialises $W$ and $b$ with small random values from a uniform distribution. Those are the parameters $\theta$ that the optimiser will update.

### `torch.optim.Adam(model.parameters(), lr=0.05)` — the optimiser

`model.parameters()` returns the iterator over $\{W, b\}$ — the things the optimiser is allowed to touch.

**Why Adam?** It is the workhorse first-order optimiser:

- Per-parameter adaptive learning rates (uses first and second moments of gradients).
- Robust to bad learning-rate choices on small problems like this.
- Almost always trains faster than vanilla SGD on small datasets without tuning.

**Why `lr=0.05`?** This is *aggressive* — typical defaults are 0.001 to 0.01. For a 4-input, 3-output linear layer with only 15 parameters and 120 training rows, the loss landscape is well-conditioned and a large learning rate gets you to the optimum in a handful of epochs. On a deeper model 0.05 would diverge.

The optimiser holds internal state (running estimates of gradient moments). That state is what makes it stateful between `step()` calls.

### `torch.nn.CrossEntropyLoss()` — the loss

Cross-entropy for multi-class classification:

$$
\mathcal{L}(\theta) = -\frac{1}{B} \sum_{i=1}^{B} \log p_\theta(y_i \mid x_i)
= -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(z_{i, y_i})}{\sum_{j} \exp(z_{i, j})}.
$$

Two important facts about PyTorch's `CrossEntropyLoss`:

1. **It includes the softmax**, so the model returns raw logits and you do not (and should not) softmax before passing to the loss. Doing softmax twice would silently break things.
2. **Minimising cross-entropy is exactly [[mle]]** under a categorical likelihood. That is, $\mathcal{L}(\theta)$ is the negative log-likelihood of the data under the model $p_\theta(y \mid x)$, averaged over the batch.

So the workshop is, in disguise, doing maximum likelihood estimation on a categorical model — which is precisely the technique covered in lecture-w1. See [[mle]] and [[cross-entropy]].

## The probabilistic reading

Wearing the Week-1 hat, the model is:

$$
p_\theta(y = k \mid x) = \mathrm{softmax}_k(W x + b).
$$

Training minimises

$$
-\sum_i \log p_\theta(y_i \mid x_i),
$$

which is the negative log-likelihood. There is **no prior** on $W, b$, so this is pure MLE — not [[map]] and not [[bayesian-inference]]. From Week 3 onwards the workshops will replace this with Bayesian variants ([[laplace-approximation]], variational, MCMC), but the model architecture and loss conceptually stay the same.

## Why these three pieces decouple

A common mistake is to think of "the model" and "the loss" as a single object. Keeping them separate matters because:

- The same architecture (linear layer) can be trained with different losses (cross-entropy for classification, MSE for regression). Same model, different probabilistic interpretation.
- The same loss can be minimised with different optimisers (SGD, Adam, L-BFGS). Same objective, different path through parameter space.

This factorisation is what makes the PyTorch idiom so flexible.

## Hyperparameters in this cell

There are exactly two hyperparameters chosen here:

- **Optimiser type and its `lr`.** Set above.
- **Model architecture.** A bare linear layer — chosen because the problem is linearly separable enough that nothing fancier is needed.

There are also implicit "hyperparameters" left at PyTorch defaults:

- Adam's $(\beta_1, \beta_2, \epsilon) = (0.9, 0.999, 10^{-8})$ — almost never worth changing.
- `Linear` weight init (Kaiming uniform) — irrelevant for this size of problem.

## Exam-style takeaway

> *"Show that minimising the cross-entropy loss for multinomial logistic regression is equivalent to maximum-likelihood estimation under a categorical likelihood."*
>
> Write the categorical log-likelihood: $\log p_\theta(y \mid x) = \log \mathrm{softmax}_y(Wx + b)$. The negative average over the dataset is the cross-entropy loss. Maximising likelihood is therefore minimising cross-entropy — they are the same objective up to a sign and a constant factor (the $1/N$). See [[mle]] and [[cross-entropy]].

## Connections

- This is multinomial [[logistic-regression]] without explicit softmax-ing in the model.
- Adding a Gaussian prior on $W, b$ would convert MLE into [[map]] estimation — the loss would gain an L2 regularisation term.
- Going further, treating $W, b$ as random variables with a posterior distribution gives [[bayesian-linear-regression]] (the regression analogue) or its classification cousin (Week 3 onwards).
