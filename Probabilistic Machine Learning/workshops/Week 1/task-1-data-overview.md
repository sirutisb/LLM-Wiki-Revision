# Task 1 — Data Overview

**Notebook cells:** imports + `load_iris` cell.
**Goal:** Before touching a model, *know what you are modelling*. Inspect the dataset's size, feature space, and label space.

## The intuition

You can think of any supervised learning problem as a function $f: \mathcal{X} \to \mathcal{Y}$ that we want to learn from samples $\{(x_i, y_i)\}_{i=1}^{N}$. Until you know:

- **$N$** (how many samples you have),
- **$\dim \mathcal{X}$** (how many features each sample has),
- **$\mathcal{Y}$** (whether the target is continuous, binary, multi-class, …),

you cannot pick a sensible model, loss, or evaluation metric. So step 1 is always: print the shapes, look at a few rows, look at the target.

## Cell-by-cell

### Imports

```python
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
```

This single cell pulls in everything the workshop needs:

| Import | Used in step | Purpose |
|---|---|---|
| `torch`, `TensorDataset`, `DataLoader` | 4–7 | Mini-batch training pipeline |
| `load_iris` | 1 | Built-in toy dataset |
| `train_test_split` | 3 | Random train/test partition |
| `StandardScaler` | 4 | Zero-mean, unit-variance feature scaling |
| `pandas` | 2 | Tabular inspection (`.head()`, `.isnull()`) |

There is nothing to *do* here — but notice that the imports already telegraph the entire workflow. The shape of your imports is often the shape of your experiment.

### Loading and shape inspection

```python
iris = load_iris()
X, y = iris.data, iris.target
print(X.shape, y.shape)
```

Output:

```
(150, 4) (150,)
```

This tells us:

- $N = 150$ samples.
- Each sample $x_i \in \mathbb{R}^4$ — 4 continuous features.
- $y_i$ is a **1-D vector** of length 150, one label per sample.

**Why a 1-D `y` (and not a one-hot $150 \times 3$ matrix)?**
PyTorch's `CrossEntropyLoss` expects integer class indices, not one-hot vectors — it does the one-hot conversion implicitly inside the loss. So we leave `y` as `(150,)` of integers in $\{0, 1, 2\}$. If we were using a different framework (e.g. raw Keras with `categorical_crossentropy`) we'd need to one-hot encode here.

### What the Iris dataset actually contains

From the scikit-learn API docs:

- **Features** ($x \in \mathbb{R}^4$): sepal length, sepal width, petal length, petal width — all in cm.
- **Target** ($y \in \{0, 1, 2\}$): species — *setosa*, *versicolor*, *virginica*.
- 50 samples per class — perfectly balanced.

The class balance matters: with balanced classes, **accuracy** is a reasonable evaluation metric. On imbalanced data we would need precision/recall/F1 or a balanced-accuracy variant. We will use plain accuracy in step 7 because of this.

## Why this step exists at all

Skipping data overview is the most common rookie mistake. Without it you end up:

- Building a binary-classification head for what turns out to be 3 classes.
- Discovering halfway through training that 30% of your features are NaN.
- Reporting accuracy on a dataset where 95% of labels are one class (so a constant predictor scores 95%).

The cost of this step is one minute; the cost of skipping it is sometimes a whole afternoon.

## Exam-style takeaway

> *"Before fitting any probabilistic model, why is it important to inspect the data?"*
>
> Because the choice of likelihood (and therefore the form of the [[mle]] / [[map]] objective) depends on the data type. A Gaussian likelihood is appropriate for continuous targets; a Bernoulli likelihood for binary; a categorical likelihood for multi-class. Picking the wrong likelihood gives you a coherent-looking but meaningless posterior.

## Connections

- This step sets up everything later: the dimensionality (4) becomes the input size of `Linear(4, 3)` in [[task-5-model-definition]], and the number of classes (3) becomes its output size.
- The probabilistic counterpart of "what is the data type?" is "what is the [[bayesian-inference|likelihood]]?" — see lecture-w1.
