# Task 4 — Data Normalisation and DataLoader

**Notebook cells:** the `StandardScaler` cell + the `DataLoader(TensorDataset(...))` cell.
**Goal:** Put the features on a common scale and wrap the training data into the iterator that the training loop will consume.

## The intuition

### Why normalise?

Suppose feature 1 ranges over $[0, 1]$ and feature 2 over $[0, 10000]$. The model — especially a linear one trained by gradient descent — will see "wiggling weight 2 by 0.01" as a huge change in output, but "wiggling weight 1 by 0.01" as a tiny change. The optimiser then takes wildly different effective step sizes in different directions; convergence becomes slow and unstable.

Normalisation rescales every feature to roughly $[-2, 2]$, so all weights start on equal footing. Concretely **standardisation** subtracts the mean and divides by the standard deviation:

$$
\tilde{x}_j = \frac{x_j - \mu_j}{\sigma_j}, \qquad \mu_j, \sigma_j \text{ computed per-feature.}
$$

After this, every feature has empirical mean 0 and variance 1 *on the training set*.

### Why a DataLoader?

PyTorch's training loop runs on **mini-batches**, not single examples or the full dataset:

- Single examples → too noisy, no GPU parallelism.
- Full dataset → too memory-heavy for large data; one gradient step per epoch.
- Mini-batches → stochastic gradients (good regularisation effect) plus efficient parallelism.

A `DataLoader` is the iterator that yields these mini-batches in shuffled order each epoch.

## Cell-by-cell

### Fitting and applying the scaler

```python
scaler = StandardScaler()
X_tr = scaler.fit_transform(X_tr)
X_te = scaler.transform(X_te)
```

Three lines, three different operations:

1. `StandardScaler()` — instantiate. No data has been seen yet.
2. `scaler.fit_transform(X_tr)` — **fit** computes $\mu_j$ and $\sigma_j$ from `X_tr`, **transform** applies $\tilde{x} = (x - \mu) / \sigma$. Combined for convenience.
3. `scaler.transform(X_te)` — apply the *same* $\mu_j, \sigma_j$ (from training!) to the test set. **Crucially we do not call `.fit` here.**

This is the **leakage-avoidance pattern** the workflow keeps coming back to. If we had done `scaler.fit_transform(X_te)`, the test set would be normalised to its *own* mean and variance, which:

- Uses test-set statistics in the pipeline (leakage).
- Means a `setosa` flower in the test set would be standardised differently than the same flower in the training set, breaking the i.i.d. assumption.

After standardisation, `X_tr` has mean $\approx 0$ and std $\approx 1$ per column. `X_te` has mean and std *near* 0 and 1 but not exactly — that small mismatch is the honest reflection of the train/test gap.

### Convert to tensors

```python
X_tr = torch.tensor(X_tr, dtype=torch.float32)
y_tr = torch.tensor(y_tr, dtype=torch.long)

X_te = torch.tensor(X_te, dtype=torch.float32)
y_te = torch.tensor(y_te, dtype=torch.long)
```

Two type choices that look fussy but matter:

- **Features as `float32`.** PyTorch defaults to `float32` everywhere; mixing in `float64` causes silent dtype-mismatch errors in matmul.
- **Labels as `long` (`int64`).** `CrossEntropyLoss` requires class indices to be `int64`. If you pass `float32` labels you get a runtime error.

This conversion is the boundary between the **scikit-learn / NumPy world** (used for data prep) and the **PyTorch world** (used for the model and training). After this cell, everything is a tensor and gradient-tracking becomes possible.

### Wrap into a DataLoader

```python
train_dl = DataLoader(TensorDataset(X_tr, y_tr), batch_size=16, shuffle=True)
```

Three things happen here:

1. **`TensorDataset(X_tr, y_tr)`** — a thin wrapper that pairs feature tensor and label tensor row-by-row. Indexing it with `i` returns `(X_tr[i], y_tr[i])`.
2. **`DataLoader(...)`** — turns that dataset into an iterator that yields batches.
3. **`batch_size=16`** — each iteration yields 16 rows of features and 16 labels. With 120 training rows, that's 7 full batches plus a partial final batch of 8 rows per epoch.
4. **`shuffle=True`** — at the start of each epoch, the order of examples is reshuffled. This decorrelates gradient updates and avoids the optimiser seeing the data in the same order every epoch (which can cause cyclic patterns in the loss).

### Why no DataLoader for the test set?

Notice the workshop never wraps `X_te, y_te` in a DataLoader. That is because at evaluation we want to:

- Run the whole test set through the model in one forward pass (it's small).
- *Not* shuffle (the order doesn't matter).
- *Not* compute gradients.

A DataLoader is overkill — passing the raw tensors directly is simpler. For larger test sets you would still wrap them in a DataLoader (just with `shuffle=False`).

## Why batch size 16?

The choice is heuristic. Some considerations:

- **Smaller batches** → noisier gradients, more updates per epoch, sometimes better generalisation.
- **Larger batches** → smoother gradients, more parallelism, fewer updates per epoch.
- **Powers of 2** (16, 32, 64, …) align with GPU memory layout — pure ergonomics, no theoretical reason.

For a 120-row training set, batch size 16 means 7–8 gradient steps per epoch × 100 epochs = 700–800 total updates. That is enough for a tiny linear model to converge.

## Putting it together

After this step the data side of the experiment is fully prepared:

- `train_dl` — yields (feature batch, label batch) pairs, ready to feed the training loop.
- `X_te, y_te` — held back, normalised with training-set statistics, ready for the final evaluation.

Nothing more on the data side will change.

## Exam-style takeaway

> *"Why is feature standardisation fit on the training set only?"*
>
> Because $\mu, \sigma$ are *parameters* learned from data. Fitting them on the test set leaks test-set statistics into the modelling pipeline, biasing the reported test loss to be lower than the true generalisation loss. The same principle underlies the train/test split itself — anything that learns from data must learn from training data only.

## Connections

- This step is the operational counterpart of an i.i.d. assumption — see [[task-3-dataset-splitting]].
- For [[bayesian-linear-regression]] in Week 2 the same pattern applies: priors and posteriors are conditioned only on training data; the test set is fresh.
- For larger models, batch size becomes a hyperparameter that interacts with learning rate (the *linear scaling rule*).
