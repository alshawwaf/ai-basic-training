# Exercise 1 — Overfitting Demo

> Back to [1_lab_guide.md](1_lab_guide.md)
> Exercise file: [exercise1_overfitting_demo.py](exercise1_overfitting_demo.py)

## What You Will Learn

- How to generate an overfitting diagnostic plot (train vs validation accuracy vs depth)
- At which depth the model transitions from generalising to memorising
- Why the validation curve peaks before training accuracy does
- How to identify the overfitting point programmatically

---

## Concept: The Train/Validation Split for Hyperparameter Selection

When tuning hyperparameters (like tree depth), you cannot use the test set — that would make the test set information influence your model selection (a form of leakage). Instead:

- **Training set** (60%): the model learns from this
- **Validation set** (20%): used to choose hyperparameters
- **Test set** (20%): final evaluation ONLY — never touched during tuning

This three-way split ensures the test set truly measures generalisation to unseen data.

---

## Concept: Reading the Divergence

The diagnostic plot shows:
- Training accuracy (solid blue): rises monotonically with depth
- Validation accuracy (dashed red): rises to a peak, then plateaus or drops

The **overfitting point** is where the gap between training and validation becomes "too large" — typically where validation accuracy starts to decline or plateau while training continues to rise.

---

## What Each Task Asks You to Do

### Task 1 — Three-Way Split
Split the intrusion detection dataset into 60% train, 20% validation, 20% test. Print sizes.

### Task 2 — Depth Sweep
Sweep max_depth 1–20. Record train accuracy and validation accuracy for each. Print table.

### Task 3 — Plot and Identify Overfitting Point
Plot the two curves. Identify the depth where validation accuracy is highest. Mark it on the plot.

### Task 4 (BONUS) — Report the Gap at Key Depths
Print the train-val gap at depths 1, 5 (sweet spot), 10, and 20. Show how the gap grows.

---

## Expected Outputs

```
TASK 1 — Three-way split:
Train size:      2400 (60%)
Validation size:  800 (20%)
Test size:        800 (20%)

TASK 2 — Depth sweep:
Depth | Train Acc | Val Acc | Gap
    1 |   0.652   |  0.648  | 0.004
    5 |   0.990   |  0.969  | 0.021  ← best val
   10 |   1.000   |  0.958  | 0.042
   20 |   1.000   |  0.941  | 0.059

TASK 3 — Overfitting point: depth=5
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using test set to pick depth | Leakage — final evaluation is optimistic | Use validation set for hyperparameter tuning |
| Overfitting to the validation set | Same problem, smaller scale | Use cross-validation (Exercise 3) |
| Mistaking training curve plateau for "good" | Training always reaches 100% with enough depth | Focus on the validation curve |

---

> Next: [exercise2_bias_variance.md](exercise2_bias_variance.md)
