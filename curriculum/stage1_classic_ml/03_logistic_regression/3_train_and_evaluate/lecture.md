# Exercise 3 — Train and Evaluate the Phishing Classifier

> Back to [README.md](README.md)

## What You Will Learn

- How to scale features before logistic regression and why it matters
- How to train a multi-feature logistic regression classifier
- How to interpret a classification report (precision, recall, F1)
- How to read a confusion matrix in a security context

---

## Concept: Feature Scaling

> **Want to go deeper?** [Logistic regression — Wikipedia](https://en.wikipedia.org/wiki/Logistic_regression)

Logistic regression uses a numerical optimiser (gradient descent) to find the best weights. If features are on very different scales (e.g., `url_length` ranges 10–250 while `has_at_symbol` is 0/1), the optimiser converges slowly and some features dominate unfairly.

`StandardScaler` fixes this by transforming each feature to have **mean=0 and std=1**:

```
z = (x - mean) / std
```

**Critical rule:** Fit the scaler on training data only, then apply (transform) to both training and test data:

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fits AND transforms
X_test_scaled  = scaler.transform(X_test)         # transforms only (no fit!)
```

If you fit the scaler on `X_test` or the full dataset, you leak information about the test distribution into the model.

**Correct scaling workflow**

| Step | Train side | Test side |
|---|---|---|
| 1. Start with | `X_train` (raw values) | `X_test` (raw values) |
| 2. Call | `scaler.fit_transform(X_train)` — *learns* mean/std *and* scales | `scaler.transform(X_test)` — uses **train's** mean/std, no fitting |
| 3. End with | `X_train_scaled` (mean ≈ 0, std ≈ 1) | `X_test_scaled` (same scale as train) |

The scaler is fitted exactly once, on training data only. The test set is then squeezed through that **same** scaler — never re-fitted — so the model meets test inputs on the same scale it learned during training.

---

## Concept: Classification Report

`classification_report()` prints a table of per-class and aggregate metrics:

```
              precision  recall  f1-score  support
legitimate       0.91     0.93      0.92      100
phishing         0.93     0.91      0.92      100
accuracy                           0.92      200
macro avg        0.92     0.92      0.92      200
```

| Metric | Formula | Security meaning |
|--------|---------|-----------------|
| **Precision** | TP / (TP + FP) | Of all URLs flagged as phishing, what fraction actually were? (low = analyst alert fatigue) |
| **Recall** | TP / (TP + FN) | Of all actual phishing URLs, what fraction did we catch? (low = missed attacks) |
| **F1-score** | 2 × P × R / (P + R) | Harmonic mean; balances both concerns |
| **Support** | count of true labels in that class | Shows class balance |

---

## Concept: Confusion Matrix

> **Want to go deeper?** [Confusion matrix — Wikipedia](https://en.wikipedia.org/wiki/Confusion_matrix)

The confusion matrix shows the 4 possible outcomes for a binary classifier:

```
                    Predicted: Legitimate    Predicted: Phishing
Actual: Legitimate        TN                       FP
Actual: Phishing          FN                       TP
```

| Cell | Name | Security meaning |
|------|------|-----------------|
| TN | True Negative | Legitimate URL correctly ignored |
| FP | False Positive | Legitimate URL wrongly blocked (analyst wastes time) |
| FN | False Negative | Phishing URL missed! (most dangerous) |
| TP | True Positive | Phishing URL correctly caught |

A good phishing detector **minimises FN** (missed phishing) even at the cost of higher FP (more analyst work).

**Confusion matrix — security perspective**

|              | Predicted **Legit** | Predicted **Phishing** | Operational meaning |
|---           |---:                 |---:                    |---|
| **Actual Legit**    | **TN = 93** (correct) | FP = 7 (false alarm) | FPs cost analyst time investigating legit URLs |
| **Actual Phishing** | **FN = 9** (MISSED ATTACK) | **TP = 91** (correct) | FNs are the dangerous cell — real phishing slipped through |

Read the rows as *what really happened* and the columns as *what the model said*. The diagonal (TN, TP) is the "got it right" cells. The off-diagonal cells are where the costs live — and in a security context, the FN cell is almost always the most expensive.

---

## Concept: Model Coefficients

After fitting, `model.coef_[0]` contains a weight for each feature. Positive weights push the model toward phishing, negative toward legitimate. Larger absolute values indicate stronger influence.

This interpretability is one reason logistic regression is valued in security: you can explain to a stakeholder *why* a URL was flagged ("the model flagged it primarily due to url_length=184 and has_at_symbol=1").

---

## What Each Task Asks You to Do

### Task 1 — Scale Features
Split the dataset (80/20), fit a `StandardScaler` on training data, transform both sets. Print the mean and std of a raw feature vs the scaled version to confirm the transformation worked.

### Task 2 — Fit the Model and Print Coefficients
Fit `LogisticRegression(max_iter=1000)` on scaled training data. Print each feature's coefficient sorted by absolute magnitude. Write a comment identifying the most influential features.

### Task 3 — Evaluate: Classification Report and Confusion Matrix
Call `predict()` on the test set. Print `classification_report()`. Then print the confusion matrix and label each cell (TP, TN, FP, FN).

### Task 4 (BONUS) — Compare Scaled vs Unscaled
Train a second logistic regression *without* scaling. Compare accuracy and convergence warnings. Show why scaling matters.

---

## Expected Outputs

```
TASK 1 — Feature scaling:
raw url_length: mean=71.6, std=32.1
scaled url_length: mean=0.00, std=1.00

TASK 2 — Model coefficients (sorted by importance):
url_length       1.52
path_length      1.31
num_dots         0.98
num_subdomains   0.87
...
uses_https      -0.61   ← negative: HTTPS is more common in legitimate sites

TASK 3 — Classification report:
              precision  recall  f1-score  support
legitimate       0.91     0.93      0.92      100
phishing         0.93     0.91      0.92      100
accuracy                           0.92      200

Confusion matrix:
              Predicted Legit  Predicted Phishing
Actual Legit        93 (TN)          7 (FP)
Actual Phish         9 (FN)         91 (TP)

TASK 4 (BONUS):
Scaled model accuracy:   0.920
Unscaled model accuracy: 0.905  ← slightly worse; may show ConvergenceWarning
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| `scaler.fit_transform(X_test)` | Data leakage | Use `scaler.transform(X_test)` |
| Low `max_iter` | `ConvergenceWarning`; model may be sub-optimal | Set `max_iter=1000` or higher |
| Ignoring FN count | Missing phishing attacks seems acceptable until it isn't | Always check FN in security classifiers |
| Reading confusion matrix rows as predicted | Rows are actual labels; columns are predicted | Remember: rows = actual, columns = predicted |

---

> Next: [../4_threshold_tuning/lecture.md](../4_threshold_tuning/lecture.md)
