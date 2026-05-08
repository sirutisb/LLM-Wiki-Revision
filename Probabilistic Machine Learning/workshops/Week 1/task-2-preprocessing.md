# Task 2 — Preprocessing

**Notebook cell:** the `pd.DataFrame(...)` / `df.isnull().sum()` cell.
**Goal:** Catch problems in the raw data before they corrupt the rest of the pipeline.

## The intuition

A model is a function from features to predictions. If a feature is `NaN`, the function is undefined. If a feature has the wrong type (a string where the model expects a float), the model will crash or — worse — silently coerce things into nonsense.

Preprocessing is a **defensive step**: you are looking for the silent failures *now*, not after a 30-minute training run.

For Iris this step is almost a no-op (sklearn ships a clean dataset), but the workshop walks through it deliberately so the *habit* generalises to messier datasets later in the module.

## Cell-by-cell

### Wrap into a DataFrame and rename columns

```python
df = pd.DataFrame(X, columns=iris.feature_names)
df["target"] = y

df.columns = ["sepal_len", "sepal_wid", "petal_len", "petal_wid", "target"]
print(df.head())
```

Two things are happening:

1. **Wrap the NumPy array as a `pandas.DataFrame`.** Raw `X` is a $150 \times 4$ NumPy array — the columns are anonymous integers. A DataFrame attaches *names* to columns, which makes `df.head()` readable and lets you reason about features by name.
2. **Rename to short, snake_case names.** The original `iris.feature_names` are strings like `'sepal length (cm)'` — fine for a printout, painful to type. Renaming to `sepal_len`, etc. is purely ergonomic.

The output of `df.head()`:

```
   sepal_len  sepal_wid  petal_len  petal_wid  target
0        5.1        3.5        1.4        0.2       0
1        4.9        3.0        1.4        0.2       0
...
```

What you should *eyeball* from this:

- All four features are on **similar but not identical scales** (lengths roughly 0.2 – 7, widths 2 – 4). They differ enough that we will want to standardise (step 4), but no feature is wildly off.
- All targets shown are `0`. **The dataset is sorted by class.** This is the reason `train_test_split` *must* shuffle — see [[task-3-dataset-splitting]].

### Check for missing values

```python
print(df.isnull().sum())
```

Output:

```
sepal_len    0
sepal_wid    0
petal_len    0
petal_wid    0
target       0
```

`df.isnull()` returns a same-shape Boolean DataFrame. `.sum()` counts the `True`s **column-wise**. Zero everywhere means no `NaN`s — the dataset is clean.

**Why does this matter?** If any column had non-zero counts, you would face a decision:

- Drop the offending rows (`df.dropna()`) — fine if missingness is rare and random.
- Impute (mean / median / model-based) — preserves $N$ but introduces bias.
- Treat "missing" as its own category — only meaningful for categorical features.

For real datasets this decision is one of the most consequential modelling choices you make, and it has a probabilistic interpretation: imputation is implicitly modelling $p(x_{\text{missing}} \mid x_{\text{observed}})$. Done badly, it leaks information and breaks i.i.d. assumptions.

### What is *not* done here (but might be in a real workshop)

The notebook deliberately stops at "no missing values, move on". A more thorough preprocessing step would also include:

- **Outlier detection** — features in Iris are roughly $\mathcal{N}$-distributed; a value of 50 cm petal length would be a data-entry error.
- **Type coercion** — confirm every numeric column actually has dtype `float64`, not `object`.
- **Class-balance check** — `df["target"].value_counts()` would confirm 50/50/50.
- **Duplicate detection** — `df.duplicated().sum()`.

All of these are zero in Iris, which is why the workshop omits them. Add them when you move to messier data.

## Why preprocessing is "before splitting" but normalisation is "after"

This is the conceptual subtlety of the workflow:

- **Preprocessing** (cleaning, removing NaNs, fixing types) is data-*independent* surgery — there is no model parameter being fitted, so doing it on the full dataset is fine.
- **Normalisation** (zero-mean / unit-variance) *is* a parameter fit (you compute $\mu, \sigma$). Computing those on the full dataset would leak test-set statistics into training. So normalisation goes *after* the split.

The notebook respects this distinction. So should you.

## Exam-style takeaway

> *"Why is data leakage a concern in the experimental workflow, and which preprocessing operations are safe to do before train/test splitting?"*
>
> Operations that don't fit any parameters from the data (renaming columns, dropping known-bad rows, type coercion) are safe pre-split. Anything that *learns* from the data — scaling, PCA, imputation by mean — must be fit on the training set only and then applied to the test set, otherwise the test-set distribution leaks into model selection and the reported accuracy is optimistically biased.

## Connections

- This step interacts with [[task-4-normalisation-and-dataloader]] — together they form the "data hygiene" stage.
- The principle (fit on train, apply on test) is the same as the principle behind not peeking at test set during model selection. Both are about preserving the **i.i.d. assumption** that the [[mle]] derivation depends on.
