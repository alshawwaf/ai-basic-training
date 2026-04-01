# Exercise 4 — Threshold Tuning

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- How to retrieve probability scores with `predict_proba()`
- Why the default 0.5 threshold is not always optimal for security
- How changing the threshold affects precision and recall
- How to choose a threshold based on operational priorities

---

## Concept: predict_proba() vs predict()

> **Want to go deeper?** [Precision and recall — Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall)

`model.predict(X)` returns hard labels (0 or 1) using the default 0.5 threshold.

`model.predict_proba(X)` returns a 2-column array: `[:, 0]` is P(legitimate), `[:, 1]` is P(phishing). You can then apply any threshold yourself:

```python
probs = model.predict_proba(X_test_scaled)[:, 1]   # P(phishing) for each URL
threshold = 0.3
y_pred_custom = (probs >= threshold).astype(int)
```

---

## Concept: The Precision-Recall Tradeoff

When you lower the threshold:
- More URLs are flagged as phishing
- You catch more real phishing (higher recall)
- But you also flag more legitimate URLs (lower precision)

When you raise the threshold:
- Fewer URLs are flagged
- You only flag URLs you are very confident about (higher precision)
- But you miss more actual phishing (lower recall)

This is a **fundamental tradeoff** — you cannot have both perfect precision and perfect recall simultaneously (unless your model is perfect).

| Priority | Preferred threshold | Effect |
|---------|--------------------|-|
| Catch every phishing URL (security-first) | Low (0.2–0.3) | High recall, lower precision |
| Minimise analyst alert fatigue | High (0.6–0.7) | High precision, lower recall |
| Balance both | Medium (0.4–0.5) | Moderate recall and precision |

---

## Concept: The Tradeoff Table

A useful operational tool is a table that shows how metrics change across thresholds:

| Threshold | Precision | Recall | F1 | Flagged |
|-----------|-----------|--------|----|----|
| 0.2 | 0.79 | 0.98 | 0.87 | 124 |
| 0.3 | 0.84 | 0.96 | 0.90 | 114 |
| 0.5 | 0.93 | 0.91 | 0.92 | 98 |
| 0.7 | 0.97 | 0.82 | 0.89 | 85 |

You present this to stakeholders and they decide what to optimise for.

---

## Concept: Cost Asymmetry in Security

In phishing detection, the two types of errors have very different costs:

| Error | Name | Consequence |
|-------|------|-------------|
| Miss a phishing URL | False Negative | User visits the site, credentials stolen |
| Block a legitimate URL | False Positive | User gets a warning; slight inconvenience |

The cost of a False Negative is typically **much higher** than a False Positive. This asymmetry justifies using a **lower threshold** than 0.5, accepting more false alarms to catch more real attacks.

---

## What Each Task Asks You to Do

### Task 1 — Get Probability Scores
Call `predict_proba()` and inspect the output. Print the probability scores and default labels for the first 10 test samples. Note which ones are "close calls" (probability near 0.5).

### Task 2 — Apply Custom Thresholds
Test thresholds 0.2, 0.3, 0.5, 0.7 and 0.8. For each, print precision, recall, F1, and the number of URLs flagged. Build a comparison table.

### Task 3 — Choose a Threshold for Your Use Case
You are a security analyst. Your manager says: "We must catch at least 95% of phishing attempts; alert fatigue is a secondary concern." Find the lowest threshold that achieves recall >= 0.95 and print it.

### Task 4 (BONUS) — Plot the Precision-Recall Curve
Use sklearn's `precision_recall_curve()` to plot how precision and recall change across all possible thresholds. Mark the 0.5 threshold point on the curve.

---

## Expected Outputs

```
TASK 1 — Probability scores (first 10):
   P(phishing)  predicted_label  actual
0     0.04           0             0
1     0.87           1             1
2     0.51           1             0    ← close call, wrong!
...

TASK 2 — Threshold comparison table:
Threshold | Precision | Recall  | F1    | Flagged
    0.20  |   0.785   | 0.980   | 0.872 |  124
    0.30  |   0.838   | 0.960   | 0.895 |  114
    0.50  |   0.930   | 0.910   | 0.920 |   98
    0.70  |   0.970   | 0.820   | 0.889 |   85
    0.80  |   0.988   | 0.790   | 0.878 |   80

TASK 3 — Threshold for 95% recall:
Threshold 0.22 achieves recall = 0.95
At this threshold: precision = 0.79, flagged = 120/200
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `predict_proba(X)[:, 0]` | Gets P(legitimate), not P(phishing) | Use `[:, 1]` for the positive class |
| Forgetting to re-scale X_test | Wrong probabilities | Always pass `X_test_scaled` to the scaled model |
| Maximising accuracy when choosing threshold | Accuracy ignores cost asymmetry | Optimise for recall or F1 depending on business need |
| Choosing threshold on test data | Data leakage | Ideally choose threshold on a validation set |

---

> Back to [1_lab_guide.md](1_lab_guide.md) | Next lesson: [Lesson 1.4 Decision Trees](../../lesson4_decision_trees/workshop/1_lab_guide.md)
