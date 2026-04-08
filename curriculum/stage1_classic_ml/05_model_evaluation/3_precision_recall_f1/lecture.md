# Exercise 3 — Precision, Recall, and F1

> Back to [README.md](README.md)

## What You Will Learn

- The precise definitions of precision, recall, and F1
- The precision-recall tradeoff and why it matters in security
- When to prioritise precision vs recall for different security tools
- How to use `classification_report` effectively

---

## Concept: Precision vs Recall

> **Want to go deeper?** [Precision and recall — Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall)

**Precision** answers: "Of all the alerts my system raised, what fraction were real attacks?"
- High precision = low false alarm rate = analysts can trust alerts
- Low precision = alert fatigue = analysts start ignoring alerts

**Recall** answers: "Of all the real attacks that occurred, what fraction did my system catch?"
- High recall = few missed attacks
- Low recall = attackers slip through undetected

These two metrics pull in opposite directions:
- To increase recall: lower the decision threshold → more alerts → more true positives → but also more false alarms → lower precision
- To increase precision: raise the threshold → fewer, more confident alerts → fewer true positives → lower recall

**Precision and Recall -- which cells they use**

|  | Predicted Benign | Predicted Attack | |
|--|------------------|------------------|-|
| **Actual Benign** | TN | FP | Precision = TP / (TP + FP) -- "Of all alerts, how many were real attacks?" |
| **Actual Attack** | FN | TP | Recall = TP / (TP + FN) -- "Of all real attacks, how many did we catch?" |

F1 = 2 * Precision * Recall / (Precision + Recall) -- balances both; punishes if either is low

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_pr_tradeoff.png" alt="Line plot of precision (violet), recall (red) and F1 (cyan dashed) against decision threshold from 0.05 to 0.95. Precision rises monotonically from 0.4 to 0.95 as threshold increases. Recall falls from 0.95 to 0.6. F1 peaks around threshold 0.5 at about 0.83. A vertical orange line marks the max-F1 threshold and a grey dotted line marks the default 0.5">
  <div class="vis-caption">Real precision-recall tradeoff from the trained LogisticRegression. Pushing the threshold up trades recall for precision — every threshold is effectively a different model.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_f1_f2_compare.png" alt="Grouped bar chart comparing F1 (cyan) and F2 (red) across three models. DummyClassifier scores 0.00 on both. LogisticRegression: F1=0.83, F2=0.83. DecisionTree: F1=0.77, F2=0.75. The F2 score nudges down for the DecisionTree because its recall is lower">
  <div class="vis-caption">F1 vs F2 on the three lab models. F2 weighs recall higher — when a model loses recall (DecisionTree), its F2 drops faster than its F1.</div>
</div>

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
LogisticRegression        0.822    0.830   0.826
DecisionTree              0.804    0.740   0.771

TASK 2 — Full report for LogisticRegression:
              precision  recall  f1-score  support
benign          0.991     0.991     0.991     1900
attack          0.822     0.830   0.826       100
accuracy                            0.983     2000

For catching every attack: focus on Recall (0.830 → lower threshold for more)
For minimising false alarms: focus on Precision (0.822 → raise threshold)

TASK 3 — Precision-recall vs threshold:
(Line chart showing precision rising as threshold increases,
 recall falling as threshold increases)

TASK 4 (BONUS) — F1 vs F2 score:
Model                       F1      F2
DummyClassifier          0.000   0.000
LogisticRegression       0.826   0.828
DecisionTree             0.771   0.752
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Reading macro-average recall instead of attack-class recall | Hides poor attack detection | Always check per-class metrics |
| Optimising F1 when recall is what matters | Some attacks still slip through | Use F2 score or explicit recall threshold |
| Reporting precision without recall | Misleading — high precision with low recall is still bad | Always report both |
| Using `average='macro'` in precision_score for attack class | Gets average over both classes | Use `pos_label=1` or read the report |
