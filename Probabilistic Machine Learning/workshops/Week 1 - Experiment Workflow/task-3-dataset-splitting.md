# Task 3 — Dataset Splitting

**Notebook cell:** `train_test_split(X, y, test_size=0.2, random_state=0)`
**Goal:** Hold out a portion of the data the model is never trained on, so we can estimate its generalisation performance honestly.

## The intuition

If you train a model and evaluate it on the *same* data, you measure how well the model **memorised** — not how well it **generalised**. A nearest-neighbour memoriser would score 100%. So we partition:

- **Training set** — used to fit parameters $\theta$ (the [[mle]] / [[map]] objective is computed on this).
- **Test set** — used **once**, after all training and tuning, to report a final unbiased accuracy.
- **Validation set** (not used in this workshop, but mentioned in the markdown) — a *third* slice used during training for hyperparameter selection and early stopping. Without it, hyperparameters would be tuned on the test set, defeating its purpose.

## Cell-by-cell

```python
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
```

Four arguments — each one is a deliberate choice:

### `X, y`

The features and labels are passed together so that `train_test_split` can keep them aligned. After the call, `X_tr[i]` and `y_tr[i]` still correspond to the same flower; the split is row-wise and synchronised across the two arrays.

### `test_size=0.2`

20% of $N=150$ rows go to the test set, so:

- `X_tr.shape == (120, 4)`
- `X_te.shape == (30, 4)`

**Why 20%?** This is a heuristic, not a theorem. The trade-off:

- A larger test set gives a more *precise* accuracy estimate (smaller standard error on the mean).
- A larger train set gives a more *accurate* model.

Common splits:

| Split | When to use |
|---|---|
| 90 / 10 | Very large dataset (millions of samples) — even 10% is statistically plenty |
| 80 / 20 | Medium dataset (this workshop) — the "default" |
| 70 / 30 | Small dataset where you need a lot of evaluation power |
| k-fold CV | Small dataset where you cannot afford to waste any rows |

For Iris with 150 rows, 80/20 leaves 30 test rows. The standard error on a 90% accuracy estimate is then $\sqrt{0.9 \cdot 0.1 / 30} \approx 5.5\%$ — wide enough that you should not over-interpret the final number.

### `random_state=0`

This **seeds the shuffle**, making the split reproducible. Two reasons it is non-negotiable:

1. **Reproducibility.** Anyone re-running your notebook gets the same split, the same training run, the same final accuracy. Without it, you would get a different test set every time and could not debug or compare results.
2. **Comparing models fairly.** If you swap in a different model later, you want it evaluated on the *same* test set. Setting `random_state=0` everywhere guarantees this.

The choice of `0` (versus `42` or anything else) is arbitrary; what matters is that it is *fixed*.

### Implicit: `shuffle=True` (the default)

`train_test_split` shuffles by default. This is critical here because **the Iris dataset is sorted by class** — rows 0–49 are *setosa*, 50–99 *versicolor*, 100–149 *virginica*. If you took the last 30 rows as a test set without shuffling, your test set would be 100% *virginica* and your training set would have only two classes. The model could never learn to predict class 2.

You should generally always shuffle for i.i.d. data. The exception is **time series**, where shuffling destroys temporal structure — there you want a chronological split (train on early data, test on later).

### Implicit: no `stratify`

A more careful version would use `stratify=y`, which forces the split to preserve class proportions in both partitions. With Iris being perfectly balanced and 150 samples, random shuffling will get *near*-balanced splits anyway — but on imbalanced data `stratify=y` is recommended.

## What this step does *not* do

It does not normalise. It does not convert to tensors. It just produces four NumPy arrays. Normalisation and tensor-conversion happen in [[task-4-normalisation-and-dataloader]] — and they happen *after* the split, which is the whole point.

## Where validation sets would slot in

The workshop's markdown notes "A validation set may be required when tuning hyperparameters". You'd implement this with a *second* split:

```python
X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
X_tr, X_val, y_tr, y_val = train_test_split(X_tmp, y_tmp, test_size=0.2, random_state=0)
```

This gives a 64/16/20 train/val/test partition. The validation set is used to choose hyperparameters (learning rate, number of epochs, regularisation strength) by evaluating on it during training. The test set stays untouched until the very end.

This workshop has *no* hyperparameter tuning (lr and epochs are hard-coded), so the validation set is omitted — but you will need it from Week 2 onwards when comparing models.

## Exam-style takeaway

> *"Distinguish the roles of training, validation, and test sets in a probabilistic model selection workflow."*
>
> Training set fits $\theta$ via [[mle]] or [[map]]. Validation set selects between candidate models / hyperparameters (e.g. by [[bic|BIC]] or held-out log-likelihood). Test set produces a single final unbiased estimate of generalisation, used **once**. Reusing the test set for model selection turns it into another validation set and biases the reported number upward.

## Connections

- The probabilistic justification for splitting is the i.i.d. assumption: with $\{(x_i, y_i)\} \sim p(x, y)$, the test set is a fresh sample from the same distribution and so its empirical loss is an unbiased estimator of the population loss.
- The **k-fold cross-validation** generalisation reuses every row as both train and test — useful when $N$ is too small to spare a 20% holdout.
