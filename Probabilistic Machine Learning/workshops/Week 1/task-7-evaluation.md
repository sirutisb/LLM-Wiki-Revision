# Task 7 — Evaluation and Analysis

**Notebook cell:** the `model.eval()` / `torch.no_grad()` / accuracy print cell.
**Goal:** Estimate how well the trained model will perform on **new, unseen** data, and produce a single number you can report.

## The intuition

Training tells you how well the model memorised the training data; evaluation tells you how well it learned the *underlying pattern*. The two can differ — that gap is **overfitting**. Evaluation is the only place we look at $X_{\text{te}}, y_{\text{te}}$, and we look at them exactly once.

We also flip the model into a different runtime mode (`eval()`) and disable gradient bookkeeping (`torch.no_grad()`) — these are not just performance optimisations; they change the model's *behaviour* for any layer that has training/eval-specific logic.

## Cell-by-cell

```python
model.eval()
with torch.no_grad():
    pred = model(X_te).argmax(dim=1)
    acc = (pred == y_te).float().mean()

print("Test accuracy:", acc.item())
```

Output:

```
Test accuracy: 0.8999999761581421
```

i.e. 90% — 27 of the 30 test flowers correctly classified.

### `model.eval()`

The counterpart to `model.train()` from [[task-6-training]]. For our bare `Linear` layer it does nothing, but as a habit it ensures:

- Any `Dropout` layer becomes a no-op (we want deterministic predictions, not stochastic ones).
- Any `BatchNorm` layer uses running statistics from training, not statistics computed on the test batch.

Without `model.eval()`, a model with dropout would silently give a *different* prediction every time you called it on the same input — making "test accuracy" a random variable.

### `with torch.no_grad():`

A context manager that turns off the autograd machinery. Inside this block:

- PyTorch does not record operations into the computational graph.
- Tensors do not get a `.grad_fn`.
- `loss.backward()` would fail (but we don't call it).

**Why disable gradients for evaluation?**

1. **Memory.** The autograd graph stores intermediate activations so they can be used for backprop. For a small linear model this is negligible, but for deeper models it can be the difference between fitting in GPU memory and OOM-ing.
2. **Speed.** Skipping graph construction is a meaningful speedup.
3. **Correctness signalling.** Putting evaluation inside `no_grad` is a *contract*: "I am not going to update parameters here." If you accidentally write code that does, PyTorch will error.

### `pred = model(X_te).argmax(dim=1)`

Two operations chained:

1. **Forward pass on the entire test set.** `X_te` has shape `(30, 4)`; `model(X_te)` returns logits of shape `(30, 3)` — one row per test sample, one column per class.
2. **`argmax(dim=1)`** — pick the class with the highest logit for each row. This collapses the `(30, 3)` logit tensor to a `(30,)` predicted-class tensor.

Note we never actually compute softmax probabilities here. Argmax of logits equals argmax of softmax (softmax is monotonic), so taking argmax directly on the logits is correct *and* cheaper. We would only need the softmax if we wanted calibrated probability outputs, e.g. for log-likelihood evaluation or thresholding.

### `acc = (pred == y_te).float().mean()`

Compute classification accuracy element-wise:

1. **`pred == y_te`** — element-wise equality, returning a `(30,)` Boolean tensor (`True` where the prediction matches the true label).
2. **`.float()`** — cast `True/False` to `1.0/0.0`.
3. **`.mean()`** — average — equal to (number correct) / 30.

Mathematically:

$$
\mathrm{acc} = \frac{1}{N_{\text{te}}} \sum_{i=1}^{N_{\text{te}}} \mathbb{1}[\hat y_i = y_i].
$$

### `acc.item()`

`acc` is a 0-dimensional tensor; `.item()` extracts the underlying Python `float`. This is just for clean printing — the value is the same.

## What does 90% accuracy actually tell you?

90% is "good but not great" for Iris — *setosa* is linearly separable from the other two classes, so a perfect classifier of *setosa* alone would already score $\sim 33\%$, and the decision boundary between *versicolor* and *virginica* is the only hard part. Three errors out of 30 is plausibly all on the *versicolor*/*virginica* boundary.

**Confidence interval check.** With $N_{\text{te}} = 30$ and $\hat p = 0.9$, the standard error on the accuracy estimate is

$$
\sqrt{\hat p (1 - \hat p) / N_{\text{te}}} = \sqrt{0.9 \cdot 0.1 / 30} \approx 0.055,
$$

so a rough 95% CI is $0.9 \pm 0.11$ — i.e. anywhere from 79% to 100%. **A single test-accuracy number from a 30-sample test set has a wide CI.** Report it, but don't over-interpret a 1–2% difference between models on this size of test set.

### What is *not* in this cell

A more thorough evaluation would also include:

- **Per-class accuracy** or a **confusion matrix** — to see *which* class is being misclassified.
- **Test-set log-likelihood** — the probabilistic counterpart of accuracy. For a probabilistic model you generally care more about $\sum_i \log p_\theta(y_i \mid x_i)$ than 0/1 accuracy.
- **Calibration check** — does the model say "I'm 90% sure" for things it gets right 90% of the time?
- **Multiple random seeds** — repeat the experiment with different `random_state` and report mean ± std.

These are the natural follow-up analyses for a real report (which is what `Report Outline.docx` is presumably about).

## Why the test set is touched only once

Once you look at the test accuracy, you will be tempted to tweak hyperparameters and re-evaluate. That tweak would, however, use the test set as a model-selection signal — turning it into a validation set and biasing the *next* test accuracy upward. The discipline is:

> Look at the test accuracy. Write it down. Move on.

For iterative experimentation, use the validation set (which this workshop omits because there is no tuning to do).

## Exam-style takeaway

> *"Why are `model.eval()` and `torch.no_grad()` typically used together at evaluation time, and what do they each accomplish?"*
>
> `model.eval()` switches mode-sensitive layers (Dropout, BatchNorm, …) into deterministic inference behaviour, ensuring predictions are reproducible. `torch.no_grad()` disables autograd graph construction, saving memory and time and asserting that no parameter updates will occur. Together they make the forward pass deterministic, efficient, and safe — but they are independent: `eval()` controls layer behaviour, `no_grad()` controls graph construction.

## Connections

- The accuracy here is one estimator of **generalisation**; the [[bic|BIC]] would be a model-selection-friendly alternative if we had multiple candidate models.
- For probabilistic models we often report held-out **log-likelihood** instead of accuracy — see [[mle]] for the connection.
- Repeating evaluation across random splits gives a cross-validated estimate, with smaller variance than a single 80/20 holdout.
