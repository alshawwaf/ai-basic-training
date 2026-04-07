# Exercise 2 — Confusion Matrix

> Back to [README.md](README.md)

## What You Will Learn

- What TP, TN, FP, and FN mean in a security context
- How to compute a confusion matrix manually and with sklearn
- How to interpret and visualise a confusion matrix heatmap
- How to derive accuracy, precision, recall, and F1 directly from the matrix

---

## Concept: The Four Outcomes

> **Want to go deeper?** [Confusion matrix — Wikipedia](https://en.wikipedia.org/wiki/Confusion_matrix)

Every prediction for a binary security classifier falls into one of four cells:

|  | Predicted: Benign | Predicted: Attack |
|--|-------------------|-------------------|
| **Actual: Benign** | TN (True Negative) | FP (False Positive) |
| **Actual: Attack** | FN (False Negative) | TP (True Positive) |

| Outcome | Security meaning | Cost |
|---------|-----------------|------|
| **TP** True Positive | Attack correctly flagged | Low — this is what we want |
| **TN** True Negative | Benign traffic correctly passed | Low — no action needed |
| **FP** False Positive | Legitimate traffic falsely blocked | Medium — analyst time wasted |
| **FN** False Negative | Attack missed entirely | High — user/system compromised |

In security, FN cost >> FP cost. A missed attack is almost always more damaging than a false alarm.

---

## Concept: Deriving All Metrics from the Matrix

Once you have TP, TN, FP, FN, every metric follows:

**Confusion matrix with metric zones**

|              | Predicted **Benign** | Predicted **Attack** |
|---           |---:                  |---:                  |
| **Actual Benign** | TN = 1,888           | FP = 12              |
| **Actual Attack** | FN = 28              | TP = 72              |

- **Precision** uses the *Predicted Attack* column → `TP / (FP + TP)`
- **Recall** uses the *Actual Attack* row → `TP / (FN + TP)`
- **Accuracy** uses the diagonal → `(TN + TP) / total`

| Metric | Formula |
|--------|---------|
| Accuracy | (TP + TN) / (TP + TN + FP + FN) |
| Precision | TP / (TP + FP) |
| Recall (Sensitivity) | TP / (TP + FN) |
| Specificity | TN / (TN + FP) |
| F1 | 2 × Precision × Recall / (Precision + Recall) |
| False Positive Rate | FP / (FP + TN) |

**Example:** If TP=72, TN=1888, FP=12, FN=28:
- Accuracy = (72+1888) / 2000 = 0.980
- Precision = 72 / (72+12) = 0.857
- Recall = 72 / (72+28) = 0.720

---

## Concept: Visualising the Confusion Matrix

A heatmap makes the matrix easier to read at a glance. Color intensity indicates the magnitude of each cell. The diagonal (TN, TP) should be dark — good predictions. Off-diagonal cells (FP, FN) should be light — errors.

Using seaborn:
```python
import seaborn as sns
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=['Benign', 'Attack'],
            yticklabels=['Benign', 'Attack'],
            cmap='Blues')
```

---

## What Each Task Asks You to Do

### Task 1 — Compute Manually
From the test predictions, manually extract TP, TN, FP, FN using boolean masking (no sklearn). Print each value with a label and security interpretation.

### Task 2 — Verify with sklearn
Use `confusion_matrix(y_test, y_pred)` to get the matrix. Verify it matches your manual calculation. Print the matrix with labelled rows/columns.

### Task 3 — Derive Metrics from the Matrix
Using only TP, TN, FP, FN (not sklearn.metrics functions), compute accuracy, precision, recall, and F1. Print each with its formula as a comment.

### Task 4 (BONUS) — Confusion Matrix Heatmap
Create a seaborn heatmap of the confusion matrix. Annotate with both counts and percentages.

---

## Expected Outputs

```
TASK 1 — Manual confusion matrix:
True Negatives  (TN) = 1888  — benign correctly ignored
False Positives (FP) =   12  — benign falsely flagged (analyst alert fatigue)
False Negatives (FN) =   28  — ATTACKS MISSED! (most dangerous)
True Positives  (TP) =   72  — attacks correctly caught

TASK 2 — sklearn confusion matrix:
              Predicted Benign  Predicted Attack
Actual Benign        1888              12
Actual Attack          28              72
Matches manual: True ✓

TASK 3 — Metrics from matrix:
Accuracy  = (TP+TN)/(TP+TN+FP+FN) = 1960/2000 = 0.980
Precision = TP/(TP+FP)             = 72/84     = 0.857
Recall    = TP/(TP+FN)             = 72/100    = 0.720
F1        = 2*P*R/(P+R)            = 0.783
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| sklearn confusion matrix row/column order | Row 0 = class 0 (benign), row 1 = class 1 (attack) | Print with explicit labels to confirm |
| Confusing precision and recall | Wrong metric optimised | Precision = of what we flagged, how many were real; Recall = of all real attacks, how many we flagged |
| Reading FP as missed attacks | FP are false alarms; FN are missed attacks | FN = actual attacks predicted as benign |
| Ignoring TN count | TN also matters for specificity | Report specificity (TN rate) for completeness |
