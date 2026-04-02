# Exercise 4 — Depth and Overfitting

> Back to [README.md](README.md)

## What You Will Learn

- How tree depth controls the complexity of the model
- Why deep trees overfit (memorise training data) and shallow trees underfit
- How to find the "sweet spot" depth using a train/test accuracy sweep
- How to read a learning curve plot

---

## Concept: Depth Controls Complexity

> **Want to go deeper?** [Overfitting — Wikipedia](https://en.wikipedia.org/wiki/Overfitting)

Every additional level in a decision tree allows the model to create finer and finer distinctions:

| Depth | Behaviour | Risk |
|-------|-----------|------|
| 1 | Single yes/no question — predicts the majority class on each side | Underfit — too simple |
| 3–5 | Captures major patterns without memorising noise | Good generalisation |
| 10+ | Creates tiny leaf nodes that may represent individual training samples | Overfit — memorises training data |
| None (unlimited) | Tree will grow until all leaves are pure | Severe overfitting |

---

## Concept: Overfitting in Decision Trees

An unlimited decision tree will achieve ~100% training accuracy by creating a separate leaf for every unique combination of feature values in the training set. But when tested on new data, those hyper-specific rules generalise poorly.

```
  Underfit vs Good fit vs Overfit

  Depth=1 (underfit)     Depth=5 (good)        Depth=15 (overfit)
  ┌───────────┐         ┌───────────┐          ┌───────────┐
  │ One split │         │ Captures  │          │ Memorises │
  │ only      │         │ real      │          │ every     │
  │           │         │ patterns  │          │ training  │
  │ Too       │         │           │          │ sample    │
  │ simple    │         │ Ignores   │          │           │
  │           │         │ noise     │          │ Fails on  │
  │           │         │           │          │ new data  │
  └───────────┘         └───────────┘          └───────────┘
  Train: 65%             Train: 99%             Train: 100%
  Test:  65%             Test:  97%             Test:  94%
  Gap:   0%              Gap:   2%              Gap:   6%
```

**Signs of overfitting:**
- Training accuracy >> Test accuracy
- The gap grows as depth increases
- The tree has many leaf nodes relative to training samples

**Signs of underfitting:**
- Both training and test accuracy are low
- The tree is very shallow (depth=1 or 2)
- The model cannot separate classes even in training data

---

## Concept: The Depth Sweep Plot

By training models at every depth from 1 to 15 and plotting both accuracies, you get a diagnostic chart:

```
Accuracy
1.00 |                      ________ Training
0.95 |              ____----
0.90 |         ____/        ________ Test
0.85 |    ____/         ----
0.80 |___/
      1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
                              Tree Depth
```

- At depth 1–3: both curves rise together (underfitting region)
- At depth 4–6: the gap begins to open (sweet spot is usually just before the gap widens)
- At depth 7+: training accuracy ≈ 1.0, test accuracy plateaus or drops (overfitting)

---

## Concept: Choosing the Best Depth

Two common approaches:

1. **Visual inspection**: Plot the curve and pick the depth where test accuracy first reaches its plateau. This is the "elbow" of the test curve.

2. **Cross-validation** (more robust): Use `cross_val_score()` to evaluate each depth on multiple train/test folds and pick the depth with highest mean CV score. (Covered in Lesson 2.4.)

For this dataset the sweet spot is typically around depth 5–7, where test accuracy is highest before overfitting sets in.

---

## What Each Task Asks You to Do

### Task 1 — Depth Sweep
Train models with `max_depth` from 1 to 15. Record training and test accuracy for each. Print a formatted table.

### Task 2 — Find the Sweet Spot
Identify the depth with the highest test accuracy. Also find the smallest gap between train and test accuracy. Print your findings.

### Task 3 — Plot the Depth Sweep
Create a line plot with depth on the x-axis and accuracy on the y-axis. Plot training accuracy (blue solid) and test accuracy (red dashed). Mark the sweet-spot depth with a vertical dotted line.

### Task 4 (BONUS) — Compare Models
Train three models: depth=1 (underfit), depth=sweet_spot (good), depth=15 (overfit). Print classification reports for all three. Show how generalisation collapses at depth=15.

---

## Expected Outputs

```
TASK 1 — Depth sweep:
Depth | Train Acc | Test Acc | Gap
  1   |   0.652   |  0.648   | 0.004
  2   |   0.839   |  0.832   | 0.007
  3   |   0.921   |  0.912   | 0.009
  4   |   0.978   |  0.962   | 0.016
  5   |   0.990   |  0.967   | 0.023
  6   |   0.996   |  0.965   | 0.031
  7   |   0.999   |  0.960   | 0.039
  ...
 15   |   1.000   |  0.943   | 0.057

TASK 2 — Sweet spot:
Best test accuracy: 0.967 at depth=5
Best train/test gap: 0.004 at depth=1 (but accuracy is too low)
Recommended depth: 5

TASK 3 — Plot created.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Only plotting training accuracy | Cannot see overfitting | Always plot both train and test |
| Using `max_depth=None` (unlimited) | Severe overfitting | Always set a depth limit |
| Picking the depth with the lowest gap | May choose a depth with poor accuracy | Pick the depth with the highest *test* accuracy |
| Not re-fitting a new model for each depth | Reusing the same fitted model | Create a new `DecisionTreeClassifier` in each loop iteration |

---

> Back to [README.md](README.md) | Next lesson: [Lesson 1.5 Model Evaluation](../../05_model_evaluation/README.md)
