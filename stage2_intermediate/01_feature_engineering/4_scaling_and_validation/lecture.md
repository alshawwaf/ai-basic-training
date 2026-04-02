# Exercise 4 — Scaling and Validation

> Back to [README.md](README.md)

## What You Will Learn

- The difference between `StandardScaler` and `MinMaxScaler`
- Why you must fit scalers on training data only
- How to validate that your feature engineering pipeline produces sensible results
- How to assemble a complete feature matrix and verify it is ML-ready

---

## Concept: StandardScaler vs MinMaxScaler

| Scaler | Formula | Output range | Best for |
|--------|---------|--------------|---------|
| `StandardScaler` | z = (x - mean) / std | Unbounded; ~[-3, 3] typical | Linear models, neural networks, features with outliers |
| `MinMaxScaler` | z = (x - min) / (max - min) | Strictly [0, 1] | KNN, when you need bounded output |

```
StandardScaler (z-score)                MinMaxScaler
Before         After                    Before         After
┌─────────┐    ┌─────────┐             ┌─────────┐    ┌─────────┐
│    10   │    │  -0.85  │             │    10   │    │  0.00   │
│   100   │    │  -0.12  │             │   100   │    │  0.02   │
│   150   │    │   0.28  │             │   150   │    │  0.03   │
│   200   │    │   0.69  │             │   200   │    │  0.04   │
│  5000   │───►│   4.57  │  outlier    │  5000   │───►│  1.00   │  outlier
└─────────┘    └─────────┘             └─────────┘    └─────────┘
  mean=0, std=1 (outlier                 [0, 1] range (outlier
  visible but doesn't                    compresses all other
  crush other values)                    values near 0.00)
```

**For network security data:**
- `bytes_per_second` can have extreme outliers (a single large transfer → very high value)
- `StandardScaler` handles outliers better because it uses standard deviation
- `MinMaxScaler` is sensitive to outliers: one extreme value compresses all others

> **Want to go deeper?** [Standard score (Wikipedia)](https://en.wikipedia.org/wiki/Standard_score)

---

## Concept: Fit on Train, Transform Both

This rule cannot be broken:

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # learns mean and std from train
X_test_scaled  = scaler.transform(X_test)          # applies SAME mean/std to test
```

```
                  ┌──────────────┐
  X_train ──────► │ scaler.fit() │  learns mean, std from train ONLY
                  │  then        │
                  │ .transform() │ ───► X_train_scaled
                  └──────┬───────┘
                         │ same mean, std
                  ┌──────▼───────┐
  X_test  ──────► │  .transform()│ ───► X_test_scaled
                  └──────────────┘
                  (NO .fit() here — that would be leakage!)
```

If you fit the scaler on `X_test` or the full dataset, the test set's distribution leaks into the scaling parameters, giving optimistic performance estimates.

**In a pipeline:**
```python
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)      # scaler fits only on X_train inside the pipeline
pipeline.score(X_test, y_test)      # scaler uses train statistics on X_test
```

---

## Concept: Feature Validation Checklist

After engineering features, validate before training:

1. **Shape**: `X.shape` — correct number of rows and features?
2. **Types**: `X.dtypes` — all numeric (float64 or int64)?
3. **Missing values**: `X.isnull().sum()` — any NaN?
4. **Ranges**: `.describe()` — do ranges make physical sense?
5. **Correlations**: `.corr()` — any feature pairs perfectly correlated (multicollinearity)?
6. **Label distribution**: `y.value_counts()` — check class imbalance

---

## What Each Task Asks You to Do

### Task 1 — Assemble the Full Feature Matrix
Combine all derived features (bytes_per_second, packet_rate, bytes_ratio, port_risk_score, protocol dummies) into one DataFrame `X`. Print shape, dtypes, and `.describe()`.

### Task 2 — Scale with StandardScaler
Split into train/test. Fit StandardScaler on training data. Transform both sets. Verify that the mean of each column in the scaled training set is ~0 and std is ~1.

### Task 3 — Compare StandardScaler vs MinMaxScaler
Scale the `bytes_per_second` feature with both scalers. Print summary statistics for each. Show how an outlier affects MinMaxScaler more than StandardScaler.

### Task 4 (BONUS) — Full Pipeline
Use sklearn `Pipeline` to combine scaler and LogisticRegression. Fit on training data. Score on test data. Verify the pipeline handles unseen data correctly.

---

## Expected Outputs

```
TASK 1 — Feature matrix:
Shape: (200, 8)
All dtypes: float64 or int64
Missing values: 0
Sample describe:
  bytes_per_second: mean=3452, min=0, max=45200
  packet_rate:      mean=8.1, max=180
  port_risk_score:  mean=2.1, min=1, max=5

TASK 2 — Scaled training data:
Column means (should all be ~0.00):
  bytes_per_second: 0.000
  packet_rate:      0.000
  ...
Column stds (should all be ~1.00):
  bytes_per_second: 1.000
  ...

TASK 3 — StandardScaler vs MinMaxScaler on bytes_per_second:
StandardScaler: mean=0.0, std=1.0, range=[-1.8, 4.2]  (handles outlier gracefully)
MinMaxScaler:   mean=0.2, range=[0.0, 1.0]  (outlier pulls everything to bottom)

TASK 4 (BONUS) — Pipeline accuracy: 0.875
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| `scaler.fit_transform(X_test)` | Data leakage | Use `scaler.transform(X_test)` |
| Forgetting NaN handling before scaling | `ValueError: Input contains NaN` | Fill or drop NaN before scaling |
| Including the target `y` in `X` | Perfect prediction (data leakage) | Never include target in feature matrix |
| Scaling binary features (0/1) | No harm, but unnecessary | Skip scaling for already-bounded features |

---

> Back to [README.md](README.md) | Next: [Lesson 2.2 Random Forests](../../02_random_forests/README.md)
