# Week 1 Workshop — Overview: The Experimental Workflow

**Notebook:** `Experiment_workflow.ipynb`
**Topic:** A scaffold for *every* ML experiment you will run in this module.

## What the workshop is actually about

This first workshop is not really about Bayesian methods at all — it is a **dry run of the experimental pipeline** you will reuse in later weeks (BNNs, VI, MCMC, VAEs, …). The lecture content for Week 1 covers [[bayesian-inference]], [[mle]], [[map]], and [[conjugate-priors]], but the workshop deliberately picks a trivial classification task (Iris, with a single linear layer) so that *the workflow itself* is the lesson.

Think of this as learning the **skeleton** that every later experiment will inherit. When Week 4 asks you to train a [[variational-autoencoder]] or Week 8 a [[variational-inference]] model, only the model definition and loss change — every other step in this notebook stays the same.

## The seven steps

The notebook explicitly enumerates the workflow:

1. **Data Overview** — see [[task-1-data-overview]]
2. **Preprocessing** — see [[task-2-preprocessing]]
3. **Dataset Splitting** — see [[task-3-dataset-splitting]]
4. **Data Normalisation** (and DataLoader construction) — see [[task-4-normalisation-and-dataloader]]
5. **Model Definition and Parameter Settings** — see [[task-5-model-definition]]
6. **Training** — see [[task-6-training]]
7. **Evaluation and Analysis** — see [[task-7-evaluation]]

## Why this ordering matters

The order is not arbitrary. Each step depends on decisions made in the previous one, and **getting the order wrong is the single most common source of subtle bugs** in ML experiments. Two examples that this workshop highlights:

- **Splitting before normalising.** If you fit the scaler on the full dataset and *then* split, the scaler has already "seen" the test set. This is **data leakage** — your test accuracy will be optimistically biased. The notebook fits the `StandardScaler` on `X_tr` only, then *transforms* `X_te`. This is the canonical fix.
- **Shuffling before splitting.** `train_test_split` shuffles by default; if you split a sorted file by hand without shuffling you will get a training set with only classes 0 and 1 and a test set entirely of class 2. The Iris file is sorted by class, so this matters here.

## The dataset: Iris

- 150 examples, 4 features (sepal length/width, petal length/width), 3 classes (setosa, versicolor, virginica).
- Continuous numeric features, no missing values, balanced classes — chosen so that *nothing about the data* will derail the workflow demo.
- Loaded from `sklearn.datasets.load_iris()`.

## The model: a single linear layer

```python
torch.nn.Linear(4, 3)
```

This is **multinomial [[logistic-regression]]** in disguise — a linear map from 4 features to 3 class scores (logits), trained with [[cross-entropy]] loss. There are no hidden layers, no priors, nothing Bayesian. Again: the *model* is intentionally minimal so the *workflow* is the focus.

When you reach Week 2 the same Iris setup will be the substrate for proper [[linear-regression]] and [[logistic-regression]] discussion, and from Week 3 onwards we replace `torch.nn.Linear` with [[laplace-approximation]] / [[variational-inference]] / [[mcmc]] versions.

## How to use these walkthrough files

Each `task-N-*.md` walks you through one section of the notebook cell-by-cell. They are written so you can read the markdown and the notebook side-by-side; every code snippet is annotated with **what it does**, **why this approach was chosen**, and **what the output is telling you**.

## Exam relevance

The workshop itself will not be examined directly, but the **rationales** for each step (especially leakage avoidance, train/val/test discipline, and what `model.eval()` / `torch.no_grad()` actually do) are fair game in conceptual questions. See the "Exam-style takeaway" section at the bottom of each task file.
