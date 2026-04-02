# Exercise 2 — Train/Test Split

> Back to [README.md](README.md)

## What You Will Learn

- Why evaluating a model on training data gives falsely optimistic results
- How `train_test_split()` works and what its parameters mean
- How to verify a split is proportionally correct
- The concept of data leakage and why it matters in security ML

---

## Concept: The Problem With Evaluating on Training Data

> **Want to go deeper?** [Cross-validation — Wikipedia](https://en.wikipedia.org/wiki/Cross-validation_(statistics))

Imagine you study for an exam using a practice test, then take the *exact same* test as the real exam. Your score looks great — but it does not tell you whether you actually *learned* the material, only that you *memorised* the questions.

The same problem applies to ML models. If you train and evaluate on the same data:

- The model has already "seen" those examples during training
- It can memorise specific data points rather than learn general patterns
- Your error metric will be far lower (better) than it would be on unseen data
- The model may completely fail in production

This is called **overfitting to the training set** and is one of the most common errors in beginner ML.

---

## Concept: Train/Test Split

The fix is to hold out a portion of your data *before* training and never touch it until final evaluation.

```
Full dataset (500 rows)
├── Training set  (80% = 400 rows)  ← model learns from this
└── Test set      (20% = 100 rows)  ← model evaluated on this, ONCE, at the end
```

```
  ┌──────────────────────────────────────────────────┐
  │                Full dataset (500 rows)           │
  └──────────────────────────────────────────────────┘
                         │
              train_test_split(test_size=0.2)
                         │
           ┌─────────────┴──────────────┐
           ▼                            ▼
  ┌────────────────────────┐   ┌──────────────┐
  │  Training set (400)    │   │ Test set(100)│
  │  model.fit(X_train,    │   │ LOCKED until │
  │           y_train)     │   │ final eval   │
  └────────────────────────┘   └──────────────┘
           │                            │
           ▼                            ▼
     Model learns               model.score(X_test,
     patterns here                       y_test)
```

sklearn provides `train_test_split()`:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,           # features array
    y,           # target array
    test_size=0.2,     # 20% goes to test set
    random_state=42    # reproducible shuffle
)
```

| Parameter | Purpose |
|-----------|---------|
| `test_size` | Fraction (0–1) or row count of test data |
| `random_state` | Fix the random shuffle for reproducibility |
| `shuffle` | Default True; set False for time-series data |
| `stratify` | Pass the label column to keep class ratios equal in both splits |

---

## Concept: Why the Split Must Be Random

If your data has a natural order (e.g., time-sorted logs), taking the last 20% as test gives a test set that is systematically different from training. The model trains on older traffic and is tested on newer traffic — realistic but often harder. Using `shuffle=True` (default) avoids accidentally encoding any ordering.

**Security exception:** For time-series anomaly detection, you *sometimes* want a chronological split to simulate real deployment. In that case, set `shuffle=False` and take the most recent data as your test set.

---

## Concept: Data Leakage

Data leakage means information from the test set "leaks" into the training process, making results unrealistically good. Common sources:

| Leakage type | Example | Fix |
|-------------|---------|-----|
| Direct leakage | Evaluating on training data | Always split first |
| Feature leakage | Computing statistics (mean, std) on the full dataset before splitting | Fit scalers/encoders on train only |
| Temporal leakage | Using future data to predict the past | Use chronological splits |
| Label leakage | Features derived from the target | Audit feature construction |

In a security context, data leakage can make a model look 99% accurate on your benchmark but fail completely on live traffic.

```
  Data leakage — what NOT to do

  ┌─────────────────────────────┐
  │      Full dataset           │
  │  ┌────────┐  ┌──────────┐   │
  │  │ Train  │  │  Test    │   │
  │  └───┬────┘  └────┬─────┘   │
  └──────┼────────────┼─────────┘
         │            │
    scaler.fit()  scaler.fit()    ← WRONG: test stats leak in
         │            │
    ┌────▼────────────▼────┐
    │  Model sees test     │      Result: 99% accuracy in lab,
    │  distribution info   │      fails on real traffic
    └──────────────────────┘
```

---

## What Each Task Asks You to Do

### Task 1 — Evaluate on Training Data (the Wrong Way)
Intentionally fit a model on all 500 rows and evaluate on the same 500 rows. Record the R² score. This shows the dangerously optimistic result you get without a proper split.

### Task 2 — Perform the Split
Use `train_test_split(X, y, test_size=0.2, random_state=42)`. Print the shape of all four arrays. Verify that train + test = 500 rows.

### Task 3 — Compare Train vs Test Evaluation
Fit a model on `X_train`/`y_train`. Evaluate it on `X_train` (training R²) and on `X_test` (test R²). Print both. The gap between them reveals how much the model has overfit.

### Task 4 (BONUS) — Stratified Split Exploration
The `stratify` parameter is used for classification. Create a binary column `high_load` (True if `requests_per_second > 100`) and demonstrate that `stratify=high_load` keeps the same proportion of high-load samples in both splits.

---

## Expected Outputs

```
TASK 1 — Evaluating on training data (WRONG):
R² on full dataset (train=test): 0.978  ← looks great but is misleading

TASK 2 — Train/test split shapes:
X_train: (400, 1)   y_train: (400,)
X_test:  (100, 1)   y_test:  (100,)
Total rows: 500 ✓

TASK 3 — Train vs Test R²:
Training R²: 0.977
Test R²:     0.973
Gap (overfit indicator): 0.004  ← small gap means model generalises well

TASK 4 (BONUS) — Stratified split:
High-load proportion in full set:  ~50%
High-load proportion in train set: ~50%
High-load proportion in test set:  ~50%
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Fitting on all data, evaluating on test | Still data leakage (model saw test during fit) | Fit on `X_train` only |
| Forgetting `random_state` | Different split each run; irreproducible results | Always set `random_state=42` |
| Reshaping X incorrectly | `ValueError: Expected 2D array` | Use `X.values.reshape(-1, 1)` |
| Computing feature statistics on full dataset before splitting | Feature leakage | Split first, then compute statistics on train set only |

---

> Next: [../3_fit_and_predict/guide.md](../3_fit_and_predict/guide.md)
