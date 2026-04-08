# Exercise 2 — Bias-Variance Tradeoff

> Back to [README.md](README.md)

## What You Will Learn

- What "high bias" (underfitting) and "high variance" (overfitting) mean
- How to visualise all three regimes: underfit, good fit, overfit
- How to describe bias-variance in terms of security model behaviour

---

## Concept: Bias and Variance

**Bias** is the error from wrong assumptions. A high-bias model is too simple to capture the true pattern — it underfits. Every time you train it on different data, you get the same wrong answer.

**Variance** is the error from sensitivity to small fluctuations in training data. A high-variance model is too complex — it overfits. Train it on different data subsets and you get wildly different models.

| Regime | Depth | Bias | Variance | Train | Val | Gap | Decision boundary |
|--------|-------|------|----------|-------|-----|-----|-------------------|
| **UNDERFIT** | 1 | High | Low | 0.73 | 0.74 | ~0 | Draws one flat line — too simple to learn the pattern |
| **GOOD FIT** | 5 | Low | Low | 0.90 | 0.83 | 0.07 | Clean split — captures the real decision boundary |
| **OVERFIT** | 50 | Low | High | 1.00 | 0.82 | 0.18 | Wiggly line around noise — memorises every training point |

**The sweet spot** is the depth where both bias and variance are low enough — validation accuracy is highest.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_decision_boundaries.png" alt="Three side-by-side scatter plots in 2D PCA space showing the decision boundary for depth 1, depth 5, and depth 50. Cyan benign and red attack points overlay coloured background regions. depth=1 has one straight boundary; depth=5 has a clean curved boundary; depth=50 has many small jagged regions wrapping individual points.">
  <div class="vis-caption">Same data, three depth regimes. depth=1 cuts the plane in two — high bias. depth=5 carves out the natural attack region — sweet spot. depth=50 wraps individual training points — high variance.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_learning_curves.png" alt="Three side-by-side line charts of accuracy versus training set size. depth=1: train and val both flat at about 0.74 (high bias — adding data does not help). depth=5: train at 0.90, val at 0.83, small gap. depth=50: train at 1.00, val at 0.82, large gap that does not close even with more data.">
  <div class="vis-caption">Learning curves are the textbook bias-variance fingerprint. Both lines flat and low → bias. Both lines climbing toward each other → good fit. Wide stable gap → variance.</div>
</div>

> **Want to go deeper?** [Bias-variance tradeoff (Wikipedia)](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff)

---

## Concept: Security Implications

| Regime | Security impact |
|--------|----------------|
| Underfit (high bias) | Misses most attacks — model is too simple to learn the pattern |
| Good fit | Balanced detection and false-positive rates |
| Overfit (high variance) | Works on training data but fails on new attack variants |

An overfitted intrusion detector may perform well in testing but miss novel attacks in production because it has memorised the training set's specific noise, not the general attack pattern.

---

## What Each Task Asks You to Do

### Task 1 — Train Three Models
Train depth=1 (underfit), depth=5 (good fit), depth=50 (overfit). Print train and val accuracy for each.

### Task 2 — Compare Classification Reports
Print classification_report for all three on the validation set. Show how each regime manifests in per-class metrics.

### Task 3 — Visualise the Three Regimes in PCA Space
Use PCA to project to 2D. Plot three side-by-side scatter plots showing the decision boundary for each depth.

### Task 4 (BONUS) — Learning Curves
Use `learning_curve()` from sklearn to show how training set size affects bias/variance for depth=1 vs depth=5 vs depth=50.

---

## Expected Outputs

```
TASK 1:
depth=1  (UNDERFIT):  train=0.728, val=0.743, gap=-0.015
depth=5  (GOOD FIT):  train=0.897, val=0.825, gap= 0.072
depth=50 (OVERFIT):   train=1.000, val=0.818, gap= 0.182
```
