# Exercise 4 — Tune the Forest

> Back to [README.md](README.md)

## What You Will Learn

- How `n_estimators` affects accuracy and training time
- How `max_features` controls tree diversity vs individual tree quality
- When adding more trees stops helping (the learning curve plateau)
- How to pick the most cost-effective forest size

---

## Concept: n_estimators — More Trees, Diminishing Returns

Adding trees always reduces variance — but the improvement shrinks quickly:

| n_estimators | Typical accuracy gain | Training time |
|-------------|----------------------|---------------|
| 1 → 10 | +3–5% | Low |
| 10 → 50 | +1–2% | Moderate |
| 50 → 100 | +0.3–0.5% | Moderate |
| 100 → 500 | +0.1% | High |
| 500 → 1000 | < 0.05% | Very high |

```
Test Accuracy vs n_estimators (conceptual shape):

  n_estimators =   1  -->  ~0.89  (steep improvement zone starts here)
                   5  -->  ~0.92
                  10  -->  ~0.93
                  25  -->  ~0.94
                  50  -->  ~0.94+
                 100  -->  ~0.95   <-- elbow (accuracy plateaus here)
                 200  -->  ~0.95
                 500  -->  ~0.95

  Steep gains from 1-50 trees, then diminishing returns.
  Elbow at ~100 trees: beyond this, you pay CPU time for tiny gains.
```

The "elbow" of the learning curve — where accuracy plateaus — is usually around 100–200 trees. Beyond that, you are paying CPU time for tiny gains.

> **Want to go deeper?** [Random forest (Wikipedia)](https://en.wikipedia.org/wiki/Random_forest)

---

## Concept: max_features — Diversity vs Quality

| max_features | Trees use | Effect |
|-------------|---------|--------|
| `None` (all) | All features at every split | Trees are similar → less diversity → worse ensemble |
| `'sqrt'` (default) | √n_features ≈ 2-3 | Good diversity; most common choice |
| `'log2'` | log₂(n_features) ≈ 3 | More aggressive diversity |
| `0.5` | 50% of features | More diversity for high-dimensional data |

For PE file features (7 features), `max_features='sqrt'` → 2-3 features per split. Increasing to `max_features=5` makes trees more powerful individually but more correlated with each other — reducing the ensemble benefit.

---

## What Each Task Asks You to Do

### Task 1 — n_estimators Learning Curve
Train forests with n_estimators = [1, 5, 10, 25, 50, 100, 200, 500]. Record test accuracy and training time for each. Print a table and plot accuracy vs n_estimators.

### Task 2 — Find the Elbow
From the learning curve, identify the n_estimators value where adding more trees gives less than 0.1% improvement. Print this "recommended minimum" value.

### Task 3 — max_features Comparison
For n_estimators=100, compare accuracy at max_features = [1, 2, 3, 4, 5, 'sqrt', 'log2']. Print results sorted by accuracy.

### Task 4 (BONUS) — Training Time vs Accuracy Tradeoff
Create a 2D scatter plot with training time on x-axis and test accuracy on y-axis. Label each point with n_estimators. Identify the "sweet spot" (high accuracy, low training time).

---

## Expected Outputs

```
TASK 1 — Learning curve:
n_estimators | Test Acc | Train Time (s)
           1 |   0.891  |   0.01
           5 |   0.921  |   0.04
          10 |   0.933  |   0.08
          25 |   0.940  |   0.18
          50 |   0.942  |   0.35
         100 |   0.943  |   0.65
         200 |   0.944  |   1.28
         500 |   0.944  |   3.15

TASK 2 — Elbow:
Recommended minimum n_estimators: 100
(Beyond 100, accuracy improvement < 0.1%)

TASK 3 — max_features comparison:
max_features | Accuracy
        sqrt |  0.943   ← default, best
        log2 |  0.941
           3 |  0.941
           4 |  0.939
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using n_estimators=10 | High variance, unreliable predictions | Use at least 100 |
| Using max_features=None | Trees are correlated — no diversity benefit | Use 'sqrt' or 'log2' |
| Picking n_estimators based on training time alone | May sacrifice accuracy | Use the elbow of the accuracy curve |
| Forgetting n_jobs=-1 for the timing test | Timing on 1 core; misleading for production | Use n_jobs=-1 consistently |
