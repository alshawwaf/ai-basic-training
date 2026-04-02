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

| Model | Bias | Variance | Train Acc | Val Acc | Gap |
|-------|------|----------|-----------|---------|-----|
| depth=1 | High | Low | ~65% | ~65% | Small |
| depth=5 | Medium | Medium | ~99% | ~97% | Small |
| depth=50 | Low | High | 100% | ~92% | Large |

```
UNDERFIT (depth=1)         GOOD FIT (depth=5)         OVERFIT (depth=50)
High bias, low variance    Low bias, low variance      Low bias, high variance

Train: 65%  Val: 65%       Train: 99%  Val: 97%       Train: 100%  Val: 92%
  gap: ~0%                   gap: ~2%                    gap: ~8%

┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│ . x . x . .  │           │ .   | x x x  │           │ ._/\  |x x/\ │
│ . x . . x .  │           │ . . |  x x   │           │ ./   \_| x/  │
│ . . x . x .  │           │ . . | x x x  │           │ . . .  |x x  │
│  (draws a    │           │ (clean split) │           │ (wiggly line│
│   flat line) │           │              │           │  around noise│
└──────────────┘           └──────────────┘           └──────────────┘
 Too simple to              Captures the real           Memorises every
 learn the pattern          decision boundary           training point
```

**The sweet spot** is the depth where both bias and variance are low enough — validation accuracy is highest.

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
depth=1  (UNDERFIT):  train=0.652, val=0.648, gap=0.004
depth=5  (GOOD FIT):  train=0.990, val=0.969, gap=0.021
depth=50 (OVERFIT):   train=1.000, val=0.941, gap=0.059
```

---

> Next: [../3_kfold_crossval/lecture.md](../3_kfold_crossval/lecture.md)
