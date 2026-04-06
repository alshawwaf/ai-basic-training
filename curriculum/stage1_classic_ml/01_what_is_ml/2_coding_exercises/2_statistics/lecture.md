# Exercise 2 — Shape, Statistics, and Missing Values

> Read this guide fully before opening the lab.

---

## What You Will Learn

- Why checking statistics is the very first step of every ML project
- How `.describe()` summarises an entire dataset in one call
- What zero-variance features are and why they are useless
- How to find and handle missing values — a near-universal problem in security data

---

## Concept: Why Statistics Before Modelling

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

It is tempting to skip straight to training a model. Don't.

Problems hidden in data that are not caught here will cause the model to fail later — silently, in ways that are hard to trace back to the root cause. Every experienced ML practitioner checks these things first, every time.

**What you are protecting against:**

| Problem | Symptom if missed | How statistics catches it |
|---------|-------------------|--------------------------|
| Wrong data loaded | Model behaves strangely | `.shape` doesn't match expectation |
| Features on wildly different scales | Algorithms that use distance (KNN, SVM, k-means) behave poorly | `.describe()` shows one feature ranging 0–16, another 0–1,000,000 |
| Zero-variance features | Model wastes capacity on useless inputs | `std = 0` in `.describe()` |
| Missing values | Silent NaN propagation, wrong predictions | `.isnull().sum()` > 0 |
| Outliers / data entry errors | Model skewed by impossible values | `.describe()` max/min looks wrong |

In security data **all five of these are common.** Logs come from multiple sensors with inconsistent formats, sensor outages leave gaps, and network metrics like `bytes_sent` span many orders of magnitude.

---

## Concept: `.describe()` — One Call, Everything

`df.describe()` returns a table of summary statistics for every numeric column:

```
           pixel_0   pixel_32   target
count      1797.00    1797.00  1797.00    <- how many non-null values
mean          0.00       5.19     4.49    <- average
std           0.00       4.54     2.87    <- standard deviation (spread)
min           0.00       0.00     0.00    <- smallest value
25%           0.00       0.00     2.00    <- 25th percentile
50%           0.00       5.00     4.00    <- median
75%           0.00       9.00     7.00    <- 75th percentile
max           0.00      16.00     9.00    <- largest value
```

**Reading this table:**

- `pixel_0` has `mean=0` and `std=0` — it **never changes**. It is always white background. Feeding it to the model is harmless but wasteful — it carries zero predictive information.
- `pixel_32` (the centre of the 8×8 grid) has `std=4.54` — it varies a lot. That variation is signal the model can learn from.
- `target` ranges from 0 to 9 as expected — confirms labels loaded correctly.

---

## Concept: Standard Deviation and Feature Usefulness

Standard deviation measures **how much a feature varies across samples**.

```
High std  →  the feature takes many different values  →  potentially informative
Low std   →  the feature is nearly constant            →  little or no information
Zero std  →  the feature never changes                 →  completely useless
```

**Feature usefulness spectrum**

| Standard deviation | Verdict | Example | Why |
|:---:|:---:|---|---|
| `std = 0`    | **USELESS**     | `pixel_0`       | always 0 — never changes |
| `std ≈ 4.5`  | **SOME SIGNAL** | `pixel_32`      | varies 0–16 across samples |
| `std = 16`   | **HIGH SIGNAL** | *(hypothetical)* | maximum possible variation |

A feature that is always the same value for every sample tells the model nothing at all. When you are working with real data, removing zero-variance features before training is standard practice.

In this dataset the corner pixels (pixel_0, pixel_8, pixel_63, pixel_55) are always white — they are the corners of a hand-drawn digit. You could drop them safely.

---

## Concept: Missing Values

pandas represents missing data as `NaN` (Not a Number). Most ML algorithms cannot handle NaN directly — they will either crash or produce wrong predictions silently.

The two-step check:

```python
df.isnull().sum()        # count of NaN per column
df.isnull().sum().sum()  # total NaN across the whole DataFrame
```

If you find missing values, your options are:

| Strategy | When to use it |
|----------|---------------|
| **Drop rows** with NaN | When few rows are affected and data is plentiful |
| **Fill with median** | For numeric features — robust to outliers |
| **Fill with mode** | For categorical features |
| **Fill with a separate indicator** | When "missing" is itself meaningful (e.g., a field that only appears in certain attack types) |
| **Impute with a model** | Advanced — use when data is scarce and missingness pattern is random |

In security data, "the field is missing" is sometimes a signal — an endpoint that stops sending heartbeats may be compromised. Dropping that information can cost you detections.

---

## Concept: Value Ranges and Feature Scaling

Look at `.describe()` and ask: do the features all live on similar scales?

This matters because many algorithms treat features as if they represent distances in space:

```
Feature A:  bytes_sent         range 0 – 2,000,000,000
Feature B:  unique_ports       range 0 – 65,535
Feature C:  syn_flag_ratio     range 0.0 – 1.0
```

An algorithm using Euclidean distance will be dominated entirely by `bytes_sent` — one feature will overwhelm all others simply because its numbers are bigger. This is not what you want.

**Three features on wildly different scales:**

| Feature | Range |
|---|---|
| `bytes_sent`     | 0 – 2,000,000,000 |
| `unique_ports`   | 0 – 65,535        |
| `syn_flag_ratio` | 0 – 1.0           |

**Two data points fed into a distance calculation:**

| Point | bytes_sent | unique_ports | syn_flag_ratio |
|---|---:|---:|---:|
| Point 1 | 1,000,000,000 | 443 | 0.8 |
| Point 2 | 1,000,000,500 |  80 | 0.1 |

**Euclidean distance ≈ 500** — and that 500 comes almost entirely from `bytes_sent`. The differences in `unique_ports` and `syn_flag_ratio` are invisible to the math, even though they may be the most important signals.

The fix is **normalisation** (also called scaling) — you will apply it properly in Stage 2. For now, notice the problem exists.

In the digits dataset all features share the same 0–16 scale, so this is not an issue here. It very often is in real security logs.

---

## What Each Task Asks You to Do

### Task 1 — Print shape and class information
Print the number of samples, number of features (excluding target), and the list of class labels.

Use:
- `digits.data.shape[0]` — rows
- `digits.data.shape[1]` — columns
- `digits.target_names` — label list

### Task 2 — Print value range
Use `digits.data.min()` and `digits.data.max()` — these operate on the entire array and return a single number each.

### Task 3 — Summary statistics with `.describe()`
Select just 5 columns (`pixel_0`, `pixel_10`, `pixel_32`, `pixel_63`, `target`) to keep the output readable. Call `.describe()` then `.round(2)` on the result.

Look for:
- Which pixels have `std = 0`? Those are always blank.
- Is `target` min/max within the expected 0–9 range?

### Task 4 — Check for missing values
Two calls chained:
```python
df.isnull().sum()           # per column
df.isnull().sum().sum()     # total
```

**Bonus — find zero-variance features**
`df.drop(columns=["target"]).std()` gives you the standard deviation of every pixel. Sort ascending to see which are least useful.

---

## Common Mistakes

**All `std` values show as `0.00` for every column**
You may have called `.describe()` on the wrong variable. Make sure you are describing the subset DataFrame, not just the target column.

**`AttributeError: 'DataFrame' object has no attribute 'min'` is not the issue — but `digits.data.min()` vs `df.min()` behave differently**
`digits.data.min()` returns a single scalar (min across all values). `df.min()` returns a Series (min per column). Both are useful; make sure you are using the right one for each task.

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../3_class_balance/lecture.md](../3_class_balance/lecture.md) — the most dangerous problem in security ML: class imbalance and the naive accuracy trap.
