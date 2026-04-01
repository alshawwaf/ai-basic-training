# Exercise 3 — K-Fold Cross-Validation

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- Why a single train/test split gives unreliable performance estimates
- How K-fold cross-validation uses all data for both training and validation
- How 5-fold vs 10-fold CV differ in variance of estimates
- How to use `cross_val_score()` from sklearn

---

## Concept: Why Single Splits Are Unreliable

With a single 80/20 split, your test set is one random 20% sample. If that 20% happened to be "easy" examples, your score is optimistically high. If it was "hard", it's pessimistically low. You can't tell which.

**K-fold CV solution:**
1. Divide data into K equal folds
2. For k=1 to K: train on K-1 folds, evaluate on fold k
3. Average the K evaluation scores

Every sample is used as both training and test exactly once. The K scores give you a distribution — mean and std — that is far more reliable than a single split.

---

## Concept: 5-fold vs 10-fold

| Setting | Bias | Variance | Compute |
|---------|------|----------|---------|
| 5-fold | Slightly higher (each model uses 80% of data) | Lower | Fast |
| 10-fold | Lower (each model uses 90%) | Higher | 2× slower |

For datasets with 2000+ samples, 5-fold is usually sufficient. 10-fold is used when data is scarce.

---

## What Each Task Asks You to Do

### Task 1 — Single Split vs K-Fold
Compare a single 80/20 split score to 5-fold CV mean±std. Show the confidence you gain from CV.

### Task 2 — 5-Fold vs 10-Fold Comparison
Run both. Compare mean and std of scores. Show that 10-fold has slightly lower variance.

### Task 3 — CV for Multiple Depths
Run 5-fold CV for depths 1-10. Plot mean CV accuracy ± std. Compare to the single-split validation curve from Exercise 1.

### Task 4 (BONUS) — StratifiedKFold
Verify that `cross_val_score` preserves class balance in each fold. Print the class ratio for 5 folds.

---

## Expected Outputs

```
TASK 1:
Single split score:    0.969
5-fold CV: 0.968 ± 0.008
Single split is within 1 CV std — OK. But std of CV (0.008) shows the range.

TASK 2:
5-fold  CV: 0.968 ± 0.008
10-fold CV: 0.969 ± 0.006  (slightly lower variance)

TASK 3:
Depth | CV Mean | CV Std
    1 |  0.648  | 0.009
    5 |  0.968  | 0.008  ← best
   10 |  0.961  | 0.010
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Not using stratify in CV | Folds may have different class ratios | Use `StratifiedKFold` (default in cross_val_score for classifiers) |
| Using test set in CV loop | Leakage | CV uses only training data |
| Reporting CV mean without std | Hides reliability concerns | Always report mean ± std |

---

> Next: [exercise4_validation_curve.md](exercise4_validation_curve.md)
