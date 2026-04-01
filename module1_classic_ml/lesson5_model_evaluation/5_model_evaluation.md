# Lesson 1.5 — Model Evaluation

**Workshop:** [workshop/1_lab_guide.md](workshop/1_lab_guide.md)

---

## Why Accuracy Is Misleading in Security

Imagine your network has 10,000 connections per hour. 100 are attacks (1%). If your model *always* predicts "benign", its accuracy is **99%** — but it catches zero attacks.

This is the **class imbalance problem**, and it's everywhere in security. You need better metrics.

---

## The Four Outcomes

Every prediction falls into one of four buckets:

|                    | Predicted: Attack | Predicted: Benign |
|--------------------|-------------------|-------------------|
| **Actual: Attack** | True Positive (TP) | False Negative (FN) — missed attack |
| **Actual: Benign** | False Positive (FP) — false alarm | True Negative (TN) |

---

## The Metrics

### Precision
> "Of all the alerts my model fires, how many are real attacks?"

```
Precision = TP / (TP + FP)
```

Low precision = analyst fatigue from false alarms. High precision = every alert is worth investigating.

### Recall (Sensitivity)
> "Of all real attacks, how many did my model catch?"

```
Recall = TP / (TP + FN)
```

Low recall = attacks slipping through. In security, this is often the more critical metric.

### F1 Score
> The harmonic mean of precision and recall — a single number that balances both.

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Use F1 when you need to balance catching attacks vs generating false alarms.

### ROC AUC
> Measures how well the model separates the two classes across *all* thresholds.

- AUC = 1.0: perfect separation
- AUC = 0.5: no better than random (coin flip)
- A good model: AUC > 0.85

---

## The Precision-Recall Tradeoff

Lowering the decision threshold catches more attacks (higher recall) but generates more false alarms (lower precision):

```
      Precision
  1.0 |*
      | **
  0.8 |   ***
      |      ****
  0.6 |          ****
      |              *****
  0.4 |                   ******
      |                         ******
  0.2 |                               ****
      +--+--+--+--+--+--+--+--+--+--+--> Recall
        0.1  0.3  0.5  0.7  0.9  1.0

  Threshold HIGH -----> LOW
  (catch less, be sure)  (catch more, accept false alarms)
```

The right balance depends on your organisation:

- **SOC with large team:** can handle more false alarms → lower threshold, higher recall
- **Automated block rule:** must be high confidence → higher threshold, higher precision

---

## Confusion Matrix

A visual summary of all four outcomes. You want the diagonal (TP, TN) to be large and the off-diagonal (FP, FN) to be small.

---

## Key sklearn API

```python
from sklearn.metrics import (classification_report, confusion_matrix,
                              ConfusionMatrixDisplay, roc_auc_score,
                              RocCurveDisplay)

print(classification_report(y_test, y_pred))
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")
RocCurveDisplay.from_predictions(y_test, y_proba).plot()
```

---

## What to Notice When You Run It

1. The confusion matrix — where are the misclassifications?
2. Precision vs recall for the "Attack" class — which is higher? What does that mean?
3. The ROC curve — the further into the top-left corner, the better
4. The threshold sensitivity table — see how precision/recall shift

---

## Next: Milestone Project

**[milestone_phishing.py](../milestone/milestone_phishing.py):** Put it all together — full pipeline from raw features to a trained, evaluated phishing URL classifier.


---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/1_lab_guide.md](workshop/1_lab_guide.md)**
