# K-Fold Cross-Validation

> Back to [README.md](README.md)

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

**5-fold cross-validation — each chunk takes a turn as the test set**

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_kfold_diagram.png" alt="Diagram of 5 rows of 5 coloured cells. Each row is labelled Fold 1 through Fold 5 and contains 4 cyan 'train' cells and exactly one orange 'TEST' cell. The TEST cell shifts one position to the right with each row, so by row 5 every chunk has been the test set exactly once.">
  <div class="vis-caption">5-fold layout: rotate the test chunk through every position. Five model fits, five scores, one mean ± std at the end.</div>
</div>

Final estimate: **mean ± std** of the five scores (e.g. `0.828 ± 0.023`). Every sample serves as test exactly once and as training in K−1 iterations, so the score is averaged over the entire dataset and the spread (`std`) tells you how reliable that average is.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_single_vs_kfold.png" alt="Bar chart comparing three measurement methods at depth=5. Grey bar: single 80/20 split, single number 0.812. Cyan bar: 5-fold CV mean 0.828 with orange error bars and 5 individual fold dots. Violet bar: 10-fold CV mean 0.825 with orange error bars and 10 individual fold dots.">
  <div class="vis-caption">Real lab numbers. The single split happened to land at 0.812; CV reveals the true distribution is 0.828 ± 0.023. The single number was misleading by more than one standard deviation.</div>
</div>

Every sample is used as both training and test exactly once. The K scores give you a distribution — mean and std — that is far more reliable than a single split.

> **Want to go deeper?** [Cross-validation (Wikipedia)](https://en.wikipedia.org/wiki/Cross-validation_(statistics))

---

## Concept: 5-fold vs 10-fold

| Setting | Bias | Variance | Compute |
|---------|------|----------|---------|
| 5-fold | Slightly higher (each model uses 80% of data) | Lower | Fast |
| 10-fold | Lower (each model uses 90%) | Higher | 2× slower |

For datasets with 2000+ samples, 5-fold is usually sufficient. 10-fold is used when data is scarce.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_depth_sweep.png" alt="Line chart of 5-fold cross-validation accuracy versus max_depth from 1 to 15. Cyan line with markers; light cyan ±1 std band wrapping it. The mean climbs from 0.74 at depth 1 to a peak around 0.83 at depth 8, then plateaus. A green dashed vertical line marks the best depth at 8.">
  <div class="vis-caption">CV-based depth sweep on the same lab data. The shaded ±1σ band shows you not just the best depth but how confident the answer is — a depth where the band is narrow is a more trustworthy choice.</div>
</div>

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
Single split score:    0.812
5-fold CV: 0.828 ± 0.023
Single split is below the CV mean by ~1 std — exactly the kind of misleading
single number CV is meant to expose.

TASK 2:
5-fold  CV: 0.828 ± 0.023
10-fold CV: 0.825 ± 0.025  (very similar; both are reliable)

TASK 3:
Depth | CV Mean | CV Std
    1 |  0.738  | 0.018
    5 |  0.828  | 0.023
    8 |  0.831  | 0.022  ← best
   15 |  0.825  | 0.020
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Not using stratify in CV | Folds may have different class ratios | Use `StratifiedKFold` (default in cross_val_score for classifiers) |
| Using test set in CV loop | Leakage | CV uses only training data |
| Reporting CV mean without std | Hides reliability concerns | Always report mean ± std |
