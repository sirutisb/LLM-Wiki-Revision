# Task 6 — Training

**Notebook cell:** the `model.train()` / nested `for` loop with `zero_grad`, `backward`, `step`.
**Goal:** Iteratively adjust the model's parameters to reduce the loss on the training data.

## The intuition

Training is just **stochastic gradient descent in disguise**. Every iteration:

1. Pick a mini-batch of training examples.
2. Compute the loss on that batch.
3. Compute the gradient of the loss with respect to the parameters.
4. Take a small step in the direction that decreases the loss.

Repeat for many epochs. The parameters drift from their random initialisation toward a (local) minimum of the loss surface. Because we showed in [[task-5-model-definition]] that the loss is the negative log-likelihood, this is doing **maximum likelihood estimation** by gradient descent — equivalent to the analytic [[mle]] derivations from lecture-w1, but solved numerically.

## Cell-by-cell

```python
model.train()
for _ in range(100):
    for xb, yb in train_dl:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
```

### `model.train()`

This puts the model into **training mode**. For a bare `Linear` layer this is a no-op — it changes nothing — but for layers like `Dropout` or `BatchNorm` it controls behaviour:

- `Dropout` is *active* in train mode (randomly zeros activations) and *off* in eval mode.
- `BatchNorm` uses *batch* statistics in train mode and *running* statistics in eval mode.

Calling `model.train()` here is therefore a **defensive habit**, not a functional necessity. The pair `model.train()` / `model.eval()` is something you should always include even when the current model has no mode-sensitive layers, because you (or your future self) might add one later.

### Outer loop: epochs

```python
for _ in range(100):
```

100 epochs — meaning the entire training set is passed through the model 100 times. With batch size 16 and 120 training rows, that is roughly $100 \times 8 = 800$ gradient steps in total.

**Why 100?** Hard-coded heuristic. The loss landscape for a 15-parameter linear classifier on 120 datapoints is shallow and easy; 100 epochs is far more than needed but cheap. There is no early stopping, no convergence check — the training simply runs for a fixed budget.

### Inner loop: mini-batches

```python
for xb, yb in train_dl:
```

Each iteration of the outer loop walks the `train_dl` once. Because `shuffle=True` was set, the order is reshuffled every epoch, so the same model sees mini-batches in different orderings each pass.

### The four-line gradient step

This is the canonical PyTorch training step. Each line matters:

#### `opt.zero_grad()`

PyTorch **accumulates** gradients into `parameter.grad` by default rather than overwriting. That design is deliberate (it makes gradient accumulation across multiple backward passes possible), but it means you must explicitly clear gradients at the start of every step. **Forgetting this is the most common silent bug in PyTorch code** — gradients from past batches keep being added in, so the optimiser's effective gradient grows unboundedly and training diverges.

#### `loss = loss_fn(model(xb), yb)`

Two things happen:

1. **Forward pass:** `model(xb)` computes logits $z = W x_b + b$ for the batch. PyTorch records the operations on the autograd graph so it knows how to differentiate them later.
2. **Loss:** `loss_fn(z, y_b)` applies softmax-cross-entropy and returns a single scalar — the average negative log-likelihood across the batch. It is a tensor (not a Python float) because the autograd graph has to flow through it.

Connection back to lecture-w1: this scalar is exactly the empirical [[mle]] objective evaluated on the current mini-batch.

#### `loss.backward()`

This triggers **autograd**: PyTorch walks the computational graph backward from `loss` and computes $\partial \mathcal{L} / \partial W$, $\partial \mathcal{L} / \partial b$ via the chain rule. The gradients are deposited into `model.weight.grad` and `model.bias.grad`.

For our linear-softmax-CE setup, the gradient has a clean closed form:

$$
\frac{\partial \mathcal{L}}{\partial z_k} = p_k - \mathbb{1}[y = k],
$$

where $p_k$ is the predicted probability of class $k$. The classic "predicted minus actual" residual you may remember from lecture-w1 derivations falls out automatically. We just don't have to derive it by hand because autograd has done it.

#### `opt.step()`

The optimiser uses the freshly computed gradients to update parameters. For Adam, the update for parameter $\theta$ is roughly:

$$
\theta \leftarrow \theta - \mathrm{lr} \cdot \frac{\hat{m}}{\sqrt{\hat{v}} + \epsilon},
$$

where $\hat m, \hat v$ are bias-corrected running estimates of the first and second moments of the gradient. The detail is buried inside `opt.step()`; you just call it.

After this line, $\theta$ has moved one small step closer to a loss minimum.

## What is *not* in this cell

The minimal training loop deliberately omits things that real experiments need:

- **No loss logging.** You cannot tell whether training is converging, oscillating, or diverging. In your own experiments, append `loss.item()` to a list each step and plot.
- **No validation pass.** Without it, there is no signal for early stopping, no learning curve, no hyperparameter feedback.
- **No gradient clipping.** Fine for this small linear model; needed for RNNs or large transformers where gradients explode.
- **No learning-rate scheduling.** A constant `lr=0.05` for 100 epochs.

These are the obvious extensions to make in your own pipeline.

## Why the test set is not touched here

Even though `X_te, y_te` exist and could in principle be passed through `model(...)`, the training loop never references them. This is the firewall between training and evaluation: as long as the test set is never an input to anything inside this loop, the final test accuracy in [[task-7-evaluation]] is an unbiased estimate of generalisation.

## Exam-style takeaway

> *"What is the role of `optimizer.zero_grad()` in a PyTorch training loop, and what would happen if it were omitted?"*
>
> PyTorch accumulates gradients into `param.grad` rather than overwriting. Without `zero_grad()`, gradients from previous mini-batches would persist and be added to the new ones, so the effective gradient at step $t$ would be $\sum_{s \le t} g_s$ rather than $g_t$. The parameter updates would grow unboundedly and the loss would diverge.

## Connections

- The objective being minimised is the negative log-likelihood — this loop is numerical [[mle]].
- Adding an L2 penalty `0.5 * lambda * sum(p**2 for p in model.parameters())` to the loss converts this into [[map]] estimation under a Gaussian prior.
- In Week 3 we replace point estimates of $\theta$ with a posterior distribution — see [[laplace-approximation]] and [[bayesian-linear-regression]].
