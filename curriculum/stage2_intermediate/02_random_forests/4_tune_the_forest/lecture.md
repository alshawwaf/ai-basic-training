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

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_learning_curve.png" alt="Line chart of test accuracy versus n_estimators on a log x-axis with markers at 1, 5, 10, 25, 50, 100, 200, 500. The line jumps steeply from 0.823 at n=1 to 0.918 at n=10, climbs more slowly to 0.940 at n=100, then plateaus around 0.94 through n=500. A vertical orange dashed line marks the elbow at n=100.">
  <div class="vis-caption">Real lab learning curve. The first 50 trees do almost all the work; everything past the elbow at <code>n_estimators=100</code> is paying CPU for hundredths of a percent.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_max_features.png" alt="Bar chart of test accuracy for max_features in {1, 2, 3, 4, 5, sqrt, log2}. The 'sqrt' bar is highlighted in cyan; the others are grey. All bars sit between 0.935 and 0.943. The bars at 2 and 4 are slightly higher, but the differences are within a single percentage point.">
  <div class="vis-caption">Real lab numbers. Across 7 sensible <code>max_features</code> choices the spread is under one percentage point — the default <code>sqrt</code> sits comfortably in the top group.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_time_vs_accuracy.png" alt="Scatter plot with training time (seconds) on the x-axis and test accuracy on the y-axis. Eight cyan dots, each annotated with its n_estimators (1, 5, 10, 25, 50, 100, 200, 500). The leftmost dots cluster on the left at high accuracy; the n=500 dot is to the far right (1.9 seconds) at the same accuracy as n=100. Title: Sweet spot — cheapest training time at the accuracy plateau.">
  <div class="vis-caption">The same data plotted as cost vs benefit. The sweet spot is the lowest-time dot already at the plateau — for this dataset, <code>n_estimators=100</code>.</div>
</div>

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
           1 |   0.823  |   0.02
           5 |   0.903  |   0.04
          10 |   0.918  |   0.06
          25 |   0.930  |   0.11
          50 |   0.933  |   0.21
         100 |   0.940  |   0.41
         200 |   0.938  |   0.77
         500 |   0.942  |   1.92

TASK 2 — Elbow:
Recommended minimum n_estimators: 100
(Beyond 100, accuracy improvement < 0.1%)

TASK 3 — max_features comparison (n_estimators=100):
max_features | Accuracy
           2 |  0.943
           4 |  0.942
           3 |  0.940
        sqrt |  0.940  <- default
        log2 |  0.940
           5 |  0.937
           1 |  0.935
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using n_estimators=10 | High variance, unreliable predictions | Use at least 100 |
| Using max_features=None | Trees are correlated — no diversity benefit | Use 'sqrt' or 'log2' |
| Picking n_estimators based on training time alone | May sacrifice accuracy | Use the elbow of the accuracy curve |
| Forgetting n_jobs=-1 for the timing test | Timing on 1 core; misleading for production | Use n_jobs=-1 consistently |
