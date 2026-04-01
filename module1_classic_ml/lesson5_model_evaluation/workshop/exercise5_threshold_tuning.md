# Exercise 5 — Threshold Tuning for Your Use Case

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- How changing the decision threshold shifts precision and recall simultaneously
- How to pick a threshold for two opposite operational goals
- How to summarise the complete precision-recall-threshold tradeoff in a table
- How to communicate threshold decisions to stakeholders

---

## Concept: The Operational Decision

> **Want to go deeper?** [Precision and recall — Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall)

Once you have selected a model, you still have one more decision: what threshold to use for deployment. This is not a technical question — it is a business question:

> What is the cost of a missed attack vs the cost of a false alarm in your environment?

In a large enterprise SOC with hundreds of analysts, a high false-positive rate might be manageable. In a small team of 3, analyst fatigue quickly leads to analysts ignoring alerts entirely — making even a "good" model useless.

---

## Concept: Two Scenarios

**Scenario A — Maximum Coverage ("Catch All Attacks")**
- Goal: Miss as few attacks as possible
- Accept: Higher false alarm rate
- Choose: Lower threshold (0.2–0.3)
- Measure: Recall on attack class

**Scenario B — High Fidelity ("Trusted Alerts Only")**
- Goal: When we alert, we want to be right
- Accept: Some attacks may slip through
- Choose: Higher threshold (0.6–0.8)
- Measure: Precision on attack class

---

## Concept: Threshold Selection Table

A useful deliverable for stakeholders is a table showing what they get at each threshold:

| Threshold | Alerts/day | True attacks caught | False alarms | Analyst hours |
|-----------|------------|---------------------|--------------|---------------|
| 0.20 | 248 | 98 | 150 | 4.1 hrs |
| 0.30 | 212 | 97 | 115 | 2.9 hrs |
| 0.50 | 144 | 91 | 53 | 1.5 hrs |
| 0.70 | 85 | 75 | 10 | 0.6 hrs |

This makes the tradeoff concrete: "Do we want 4 hours of review with 98% catch rate, or 36 minutes with 75% catch rate?"

---

## Concept: Communicating to Non-Technical Stakeholders

Instead of saying "recall is 0.92", say:
> "At this threshold, we catch 92 out of every 100 attacks, and generate 8 false alarms per 100 benign events."

Instead of "precision is 0.85", say:
> "For every 100 alerts we raise, 85 are real attacks and 15 are false alarms."

This translation makes threshold decisions accessible to managers and executives.

---

## What Each Task Asks You to Do

### Task 1 — Full Precision-Recall-Threshold Table
For thresholds 0.1 to 0.9 (step 0.05), compute precision, recall, F1, and number of alerts. Print as a table. Mark the row that maximises F1.

### Task 2 — Scenario A: Maximum Coverage
Find the threshold that achieves recall >= 0.95 while minimising false positives. Print the threshold and the resulting precision, recall, and daily alert count (assume 10,000 events/day).

### Task 3 — Scenario B: High Fidelity
Find the threshold that achieves precision >= 0.95 while maximising recall. Print the threshold and the resulting metrics.

### Task 4 (BONUS) — Stakeholder Report
For both thresholds (Scenario A and B), print a human-readable paragraph describing the operational impact: attacks caught, false alarms, analyst time required (assume 5 min/alert).

---

## Expected Outputs

```
TASK 1 — Threshold table:
Thresh  Precision  Recall    F1    Alerts
  0.10     0.741    0.990  0.848    267
  0.20     0.784    0.980  0.871    250
  0.30     0.838    0.960  0.895    229
  ...
  0.50     0.930    0.910  0.920    196   ← max F1
  ...
  0.90     0.992    0.700  0.819    141

TASK 2 — Scenario A (recall >= 0.95):
Threshold: 0.20
Recall:    0.980, Precision: 0.784
Daily alerts: 250 (of which ~196 are true attacks, ~54 are false alarms)

TASK 3 — Scenario B (precision >= 0.95):
Threshold: 0.68
Precision: 0.951, Recall: 0.760
Daily alerts: 80 (of which ~76 are true attacks, ~4 are false alarms)

TASK 4 (BONUS) — Stakeholder report:
Scenario A (low threshold = catch-all):
  We catch 490 of 500 daily attacks (98% detection rate).
  We generate 54 false alarms per 500 benign events reviewed.
  Analyst time: ~4.2 hours/day reviewing 250 total alerts.

Scenario B (high threshold = trusted alerts):
  We catch 380 of 500 daily attacks (76% detection rate).
  We generate only 4 false alarms per 500 benign events.
  Analyst time: ~0.7 hours/day reviewing 80 total alerts.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Picking threshold to maximise accuracy | Wrong objective for security | Optimise recall or F1 instead |
| Choosing threshold on test data without holdout | Optimistic — overfits the threshold | Ideally use a validation set for threshold tuning |
| Not documenting the chosen threshold | Model behaviour unclear in production | Always document threshold with justification |
| Treating threshold as fixed forever | Attack patterns change | Plan for periodic recalibration |

---

> Back to [1_lab_guide.md](1_lab_guide.md) | Next: [Module 2 Feature Engineering](../../../module2_intermediate/lesson1_feature_engineering/workshop/1_lab_guide.md)
