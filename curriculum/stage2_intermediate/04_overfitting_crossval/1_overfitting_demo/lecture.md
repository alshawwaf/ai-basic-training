# Exercise 1 — Overfitting Demo

> Back to [README.md](README.md)

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_three_way_split.png" alt="Horizontal stacked bar chart split into three coloured segments. Cyan train segment 1200 samples labelled 'fit the model'; orange validation segment 400 samples labelled 'tune hyperparameters'; red test segment 400 samples labelled 'final evaluation only'. Title: Three-way split: train / validation / test.">
  <div class="vis-caption">Each slice has exactly one job. The test set is sealed in an envelope until the very end — touch it during tuning and you no longer know how the model will behave on new data.</div>
</div>

> **Want to go deeper?** [Overfitting (Wikipedia)](https://en.wikipedia.org/wiki/Overfitting)

---

## Concept: Reading the Divergence

The diagnostic plot shows:
- Training accuracy (solid cyan): rises monotonically with depth
- Validation accuracy (red): rises to a peak, then plateaus or drops

<div class="lecture-visual">
  <img src="/static/lecture_assets/cv_overfit_curve.png" alt="Line chart of accuracy versus max_depth from 1 to 20. The cyan training-accuracy line rises from 0.73 at depth 1 to 1.0 by depth 12 and stays flat. The red validation-accuracy line rises to a peak around 0.84 at depth 6 and stays roughly flat afterwards. A green dashed vertical line marks the sweet spot at depth 6. An orange double-headed arrow at depth 20 labels the train-val gap as 0.18.">
  <div class="vis-caption">Real lab numbers from <code>solution_overfitting_demo.py</code>. Train climbs to 1.000 by depth 12, validation peaks at depth 6 and never recovers. The widening gap on the right is overfitting in plain sight.</div>
</div>

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
Train size:      1200 (60%)
Validation size:  400 (20%)
Test size:        400 (20%)

TASK 2 — Depth sweep:
Depth | Train Acc | Val Acc | Gap
    1 |   0.728   |  0.743  | -0.015
    5 |   0.897   |  0.825  |  0.072
    6 |   0.917   |  0.845  |  0.072  ← best val
   10 |   0.991   |  0.820  |  0.171
   20 |   1.000   |  0.818  |  0.182

TASK 3 — Overfitting point: depth=6
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using test set to pick depth | Leakage — final evaluation is optimistic | Use validation set for hyperparameter tuning |
| Overfitting to the validation set | Same problem, smaller scale | Use cross-validation (Exercise 3) |
| Mistaking training curve plateau for "good" | Training always reaches 100% with enough depth | Focus on the validation curve |
