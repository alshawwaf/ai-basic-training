# Exercise 3 — Precision, Recall, and F1

> Back to [1_lab_guide.md](1_lab_guide.md)
> Exercise file: [exercise3_precision_recall_f1.py](exercise3_precision_recall_f1.py)

## What You Will Learn

- The precise definitions of precision, recall, and F1
- The precision-recall tradeoff and why it matters in security
- When to prioritise precision vs recall for different security tools
- How to use `classification_report` effectively

---

## Concept: Precision vs Recall

**Precision** answers: "Of all the alerts my system raised, what fraction were real attacks?"
- High precision = low false alarm rate = analysts can trust alerts
- Low precision = alert fatigue = analysts start ignoring alerts

**Recall** answers: "Of all the real attacks that occurred, what fraction did my system catch?"
- High recall = few missed attacks
- Low recall = attackers slip through undetected

These two metrics pull in opposite directions:
- To increase recall: lower the decision threshold → more alerts → more true positives → but also more false alarms → lower precision
- To increase precision: raise the threshold → fewer, more confident alerts → fewer true positives → lower recall

---

## Concept: F1 Score

F1 is the harmonic mean of precision and recall:

```
F1 = 2 × Precision × Recall / (Precision + Recall)
```

It gives a single number that balances both. The harmonic mean penalises imbalance: a model with P=0.99 and R=0.01 has F1 = 0.02, not 0.50. Both metrics must be reasonable for F1 to be high.

**Fbeta score** generalises this: `F_beta = (1 + β²) × P × R / (β²P + R)`
- β=1: equal weight (standard F1)
- β=2: recall weighted twice as heavily (good for catch-all security tools)
- β=0.5: precision weighted twice as heavily (good for high-fidelity alerting)

---

## Concept: Security Use Case Guidelines

| Use case | Priority | Metric to optimise |
|---------|----------|--------------------|
| Email phishing filter | Catch all phishing, FP is acceptable | High recall |
| High-fidelity threat intelligence feed | Only flag confirmed threats | High precision |
| IDS (intrusion detection) | Balance both | F1 or F2 score |
| Incident response auto-escalation | High confidence required | High precision |
| Malware sandbox submission | Cast wide net | High recall |

---

## Concept: Per-class vs Macro vs Weighted Average

`classification_report` shows several average types:

| Average | How it's computed | When to use |
|---------|-------------------|-------------|
| Per-class | Metrics for each individual class | Always check attack class specifically |
| Macro avg | Unweighted mean across classes | When both classes matter equally |
| Weighted avg | Average weighted by class support | When class imbalance exists |

For security with class imbalance: **always read per-class metrics for the attack class**, not the macro average.

---

## What Each Task Asks You to Do

### Task 1 — Compare Models on Precision and Recall
Train DummyClassifier, LogisticRegression, and DecisionTreeClassifier. Print a summary table with precision, recall, and F1 for the attack class only.

### Task 2 — F1 Score Breakdown
For the LogisticRegression model, print the full `classification_report`. Identify which metric you would focus on if your goal is (a) to catch every attack, (b) to minimise false alarms.

### Task 3 — The Tradeoff Illustrated
For LogisticRegression, compute precision and recall at five different thresholds (0.2, 0.3, 0.5, 0.7, 0.9). Plot precision and recall as two lines on the same chart with threshold on the x-axis.

### Task 4 (BONUS) — F2 Score
Compute the F2 score (recall-weighted F1) for each model. Explain why F2 is often more appropriate than F1 for security applications.

---

## Expected Outputs

```
TASK 1 — Model comparison (attack class only):
Model                  Precision  Recall     F1
DummyClassifier           0.000    0.000   0.000
LogisticRegression        0.857    0.720   0.783
DecisionTree              0.812    0.780   0.796

TASK 2 — Full report for LogisticRegression:
              precision  recall  f1-score  support
benign          0.994     0.994     0.994     1900
attack          0.857     0.720     0.783      100
accuracy                            0.980     2000

For catching every attack: focus on Recall (0.720 → need to lower threshold)
For minimising false alarms: focus on Precision (0.857 → acceptable)

TASK 3 — Precision-recall vs threshold:
(Line chart showing precision rising as threshold increases,
 recall falling as threshold increases)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Reading macro-average recall instead of attack-class recall | Hides poor attack detection | Always check per-class metrics |
| Optimising F1 when recall is what matters | Some attacks still slip through | Use F2 score or explicit recall threshold |
| Reporting precision without recall | Misleading — high precision with low recall is still bad | Always report both |
| Using `average='macro'` in precision_score for attack class | Gets average over both classes | Use `pos_label=1` or read the report |

---

> Next: [exercise4_roc_and_auc.md](exercise4_roc_and_auc.md)
