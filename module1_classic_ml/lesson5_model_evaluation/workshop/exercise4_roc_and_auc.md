# Exercise 4 — ROC Curve and AUC

> Back to [1_lab_guide.md](1_lab_guide.md)
> Exercise file: [exercise4_roc_and_auc.py](exercise4_roc_and_auc.py)

## What You Will Learn

- What the ROC curve plots and what it tells you about a classifier
- What AUC (Area Under the Curve) measures
- How to compare multiple models on a single ROC plot
- How to interpret AUC values in a security context

---

## Concept: The ROC Curve

The ROC (Receiver Operating Characteristic) curve plots:
- **x-axis**: False Positive Rate (FPR) = FP / (FP + TN) = 1 - Specificity
- **y-axis**: True Positive Rate (TPR) = TP / (TP + FN) = Recall

At every possible threshold, you get one (FPR, TPR) point. Connecting all those points gives the ROC curve.

**Key points on the curve:**
- **(0, 0)**: Threshold = 1.0 — predict nothing as positive; no TP, no FP
- **(1, 1)**: Threshold = 0.0 — predict everything as positive; all TP, all FP
- **(0, 1)**: Perfect classifier — catches all attacks, no false alarms
- **Diagonal line**: Random classifier (AUC = 0.5) — no better than chance

A good classifier's curve bulges toward the upper-left corner.

---

## Concept: AUC — Area Under the ROC Curve

AUC is the area under the ROC curve, ranging from 0 to 1.

| AUC | Interpretation |
|-----|----------------|
| 1.0 | Perfect classifier |
| 0.9–1.0 | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Acceptable |
| 0.5–0.7 | Poor |
| 0.5 | No better than random guessing |
| < 0.5 | Worse than random (predictions are inverted) |

**Probabilistic interpretation:** AUC = P(random attack scores higher than random benign). An AUC of 0.95 means that if you pick a random attack and a random benign sample, there is a 95% chance the model assigns a higher probability of being an attack to the actual attack.

---

## Concept: Why AUC is Better Than Accuracy for Imbalanced Data

AUC evaluates the model across **all possible thresholds**, not just the default 0.5. This means it is not affected by class imbalance — a model that always predicts "benign" has AUC = 0.5, not 0.95.

AUC is threshold-independent, making it useful for comparing models before you have decided on an operational threshold.

---

## Concept: Using sklearn for ROC

```python
from sklearn.metrics import roc_curve, roc_auc_score

fpr, tpr, thresholds = roc_curve(y_test, y_scores)  # y_scores = P(attack)
auc = roc_auc_score(y_test, y_scores)

plt.plot(fpr, tpr, label=f'Model (AUC = {auc:.2f})')
plt.plot([0,1], [0,1], 'k--', label='Random')
```

---

## What Each Task Asks You to Do

### Task 1 — ROC Curve for One Model
Plot the ROC curve for LogisticRegression. Mark the operating point at threshold=0.5. Print the AUC score.

### Task 2 — Compare Three Models
Plot ROC curves for DummyClassifier, LogisticRegression, and DecisionTreeClassifier on the same axes. Label each with its AUC. Identify which model wins.

### Task 3 — Find the Optimal Threshold on the ROC Curve
The "optimal" threshold is where TPR is highest and FPR is lowest. One heuristic is the threshold closest to the top-left corner: minimise `sqrt((1-TPR)² + FPR²)`. Find and print that threshold.

### Task 4 (BONUS) — AUC for All Three Models in a Table
Print a formatted summary table of all three models' accuracy, precision, recall, F1, and AUC. This is the complete model evaluation scorecard.

---

## Expected Outputs

```
TASK 1 — AUC:
LogisticRegression AUC: 0.983

TASK 2 — Model comparison:
DummyClassifier    AUC: 0.500  (random)
LogisticRegression AUC: 0.983
DecisionTree       AUC: 0.966
Winner: LogisticRegression

TASK 3 — Optimal threshold:
Optimal threshold (closest to top-left): 0.37
At this threshold: TPR=0.860, FPR=0.012

TASK 4 (BONUS) — Full evaluation scorecard:
Model               Accuracy  Precision  Recall    F1   AUC
DummyClassifier       0.950     0.000    0.000  0.000  0.500
LogisticRegression    0.980     0.857    0.720  0.783  0.983
DecisionTree          0.977     0.812    0.780  0.796  0.966
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Passing hard labels (0/1) to roc_auc_score | Score will be wrong | Pass probability scores `predict_proba()[:, 1]` |
| DummyClassifier has no predict_proba | AttributeError | Use `decision_function` or assign constant scores |
| Confusing AUC of ROC with AUC of PR curve | Different metrics | Specify which AUC you mean |
| Claiming a model is good based on AUC alone | Ignores threshold selection | AUC is a ranking metric; still need to pick a threshold for deployment |

---

> Next: [exercise5_threshold_tuning.md](exercise5_threshold_tuning.md)
