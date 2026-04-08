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
| **Actual Benign** | TN = 1,882           | FP = 18              |
| **Actual Attack** | FN = 17              | TP = 83              |

- **Precision** uses the *Predicted Attack* column → `TP / (FP + TP)`
- **Recall** uses the *Actual Attack* row → `TP / (FN + TP)`
- **Accuracy** uses the diagonal → `(TN + TP) / total`

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_metric_zones.png" alt="Diagram of the 2x2 confusion matrix. Top-left TN=1882 (cyan), top-right FP=18 (orange), bottom-left FN=17 (red), bottom-right TP=83 (green). A red dashed rectangle outlines the bottom row labelled Recall = TP/(TP+FN). A violet dashed rectangle outlines the right column labelled Precision = TP/(TP+FP)">
  <div class="vis-caption">Real lab numbers laid out as a confusion matrix. Each metric uses a different slice — recall reads the *actual attack* row, precision reads the *predicted attack* column.</div>
</div>

| Metric | Formula |
|--------|---------|
| Accuracy | (TP + TN) / (TP + TN + FP + FN) |
| Precision | TP / (TP + FP) |
| Recall (Sensitivity) | TP / (TP + FN) |
| Specificity | TN / (TN + FP) |
| F1 | 2 × Precision × Recall / (Precision + Recall) |
| False Positive Rate | FP / (FP + TN) |

**Example:** If TP=83, TN=1882, FP=18, FN=17:
- Accuracy = (83+1882) / 2000 = 0.983
- Precision = 83 / (83+18) = 0.822
- Recall = 83 / (83+17) = 0.830

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_confusion_heatmap.png" alt="Confusion matrix heatmap from the trained LogisticRegression. Top-left TN=1882 (dark blue), top-right FP=18 (very light blue), bottom-left FN=17 (very light blue), bottom-right TP=83 (light blue). Each cell labelled with its security meaning">
  <div class="vis-caption">Real <code>confusion_matrix(y_test, y_pred)</code> rendered as a heatmap. Diagonal cells (TN, TP) are dark — those are the predictions the model gets right.</div>
</div>

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
True Negatives  (TN) = 1882  — benign correctly ignored
False Positives (FP) =   18  — benign falsely flagged (analyst alert fatigue)
False Negatives (FN) =   17  — ATTACKS MISSED! (most dangerous)
True Positives  (TP) =   83  — attacks correctly caught

TASK 2 — sklearn confusion matrix:
              Predicted Benign  Predicted Attack
Actual Benign        1882              18
Actual Attack          17              83
Matches manual: True ✓

TASK 3 — Metrics from matrix:
Accuracy  = (TP+TN)/(TP+TN+FP+FN) = 1965/2000 = 0.983
Precision = TP/(TP+FP)             = 83/101    = 0.822
Recall    = TP/(TP+FN)             = 83/100    = 0.830
F1        = 2*P*R/(P+R)            = 0.826
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| sklearn confusion matrix row/column order | Row 0 = class 0 (benign), row 1 = class 1 (attack) | Print with explicit labels to confirm |
| Confusing precision and recall | Wrong metric optimised | Precision = of what we flagged, how many were real; Recall = of all real attacks, how many we flagged |
| Reading FP as missed attacks | FP are false alarms; FN are missed attacks | FN = actual attacks predicted as benign |
| Ignoring TN count | TN also matters for specificity | Report specificity (TN rate) for completeness |
