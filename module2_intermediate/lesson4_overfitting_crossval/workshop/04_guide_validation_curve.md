# Exercise 4 — Validation Curve

> Read this guide fully before opening the lab.

## What You Will Learn

- How `validation_curve()` automates a cross-validated parameter sweep
- How to interpret the three regions of a validation curve (underfit, sweet spot, overfit)
- How to plot train vs validation score with standard deviation bands
- Why overfitting boundary identification matters for model selection

---

## Concept: What is a Validation Curve?

A validation curve answers the question: **"How does model performance change as I vary one hyperparameter?"**

In Exercise 1 you wrote a manual loop over `max_depth` values. `validation_curve()` does the same thing but:
1. Uses cross-validation (not a single split) for each parameter value
2. Returns both train and validation scores
3. Handles the loop internally — you just specify the parameter name and range

```python
from sklearn.model_selection import validation_curve

train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=42),
    X_train, y_train,
    param_name='max_depth',
    param_range=np.arange(1, 21),
    cv=5,
    scoring='accuracy'
)
```

The result shapes are both `(n_param_values, n_cv_folds)`. Take `.mean(axis=1)` and `.std(axis=1)` for summary statistics.

> **Want to go deeper?** [Cross-validation (Wikipedia)](https://en.wikipedia.org/wiki/Cross-validation_(statistics))

---

## Concept: Reading the Three Regions

```
Accuracy
  1.0 |                  train __________
      |               ../
  0.9 |             ./
      |   val ____./     <- val score peaks here = sweet spot
  0.8 |  /
      | /  <- both low = underfitting (high bias)
  0.7 |/
      |                           val \___  <- overfitting (high variance)
      +---+---+---+---+---+---+---+---+---> max_depth
       1   2   3   4   5   6  ...        20
```

| Region | Train score | Val score | Diagnosis |
|--------|------------|-----------|-----------|
| Left (low depth) | Low | Low | High bias — model too simple |
| Middle | High | Peaks | Best complexity — choose this depth |
| Right (high depth) | 1.000 | Drops | High variance — model memorises training data |

The gap between train and val score at any point shows how much the model is overfitting. A large gap means the model learned noise that does not generalise.

---

## Concept: std Bands Tell You About Stability

The shaded ±1 std region shows how much the score varies across CV folds.

- **Narrow band**: score is stable — model behaves consistently on different data subsets
- **Wide band**: score is noisy — model is sensitive to which data it sees

When choosing between two depths with similar mean val scores, prefer the one with the narrower band.

---

## Concept: RandomForest vs Decision Tree on Validation Curves

A single decision tree overfits dramatically as depth increases — the validation curve drops sharply on the right.

RandomForests are resistant to this because averaging many trees cancels out individual tree noise. The RandomForest validation curve for `n_estimators` typically shows:
- Score improving at small n_estimators values
- Score plateauing — adding more trees stops helping after a point
- Score never dropping significantly

This is why Random Forests are often described as "easier to tune" than single trees.

---

## What Each Task Asks You to Do

### Task 1 — Run validation_curve() for max_depth 1-20
Call `validation_curve()` and print a table of mean train and val scores for each depth. See how training accuracy rises to 1.000 while validation peaks and levels off.

### Task 2 — Plot with std bands
Use `plt.fill_between()` to add a shaded ±1 std region around each curve. Add a vertical dashed line at the best depth. This plot visualises the entire bias-variance tradeoff in one chart.

### Task 3 — Identify the optimal depth and measure overfitting gap
Extract the best depth by finding `np.argmax(val_mean)`. Print the exact train score, val score, and overfit gap at the best depth. Compare this gap to depth=20 where overfitting is severe.

### Task 4 (BONUS) — RandomForest n_estimators validation curve
Run the same analysis for `RandomForestClassifier` sweeping `n_estimators`. Observe that the validation curve plateaus rather than dropping — Random Forests do not overfit the way single trees do.

---

## Common Mistakes

- **Passing X (all data) instead of X_train**: `validation_curve` should only see training data. The test set must remain untouched for final evaluation.
- **Using `param_range` as a list of strings**: sklearn expects numeric values for numeric parameters. `np.arange(1, 21)` works; `['1','2',...]` does not.
- **Ignoring std bands**: A depth where val score is 0.970 ± 0.001 is more trustworthy than 0.972 ± 0.015. Always look at the band width.
- **Confusing train_scores and val_scores shapes**: Both are `(n_params, n_folds)` — use `axis=1` for the mean across folds, not `axis=0`.

---

## Now Open the Lab

[04_lab_validation_curve.md](04_lab_validation_curve.md)

## Next

Workshop complete — open the matching `_solution_` file for each exercise to compare your approach.
