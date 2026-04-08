# Exercise 5 — Threshold Tuning for Your Use Case

> Back to [README.md](README.md)

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

**Sliding the threshold — the operational tradeoff**

|  | Scenario A — "Catch all attacks" | Scenario B — "Trusted alerts" |
|---|---|---|
| Threshold        | low (0.2 – 0.4)                 | high (0.7 – 0.9)              |
| Recall           | **HIGH**                        | LOW                           |
| Precision        | LOW                             | **HIGH**                      |
| Alerts produced  | MANY                            | FEW                           |
| False negatives  | few attacks missed              | more attacks missed           |
| False positives  | many false alarms               | few false alarms              |

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_scenario_compare.png" alt="Two side-by-side bar charts comparing operating points. Left panel 'Scenario A · catch every attack' at threshold 0.04: 235 total alerts, 96 attacks caught, 139 false alarms, 4 attacks missed. Right panel 'Scenario B · trusted alerts only' at threshold 0.92: 62 total alerts, 59 attacks caught, 3 false alarms, 41 attacks missed">
  <div class="vis-caption">Real lab numbers for the two extreme operating points. Scenario A floods the SOC with alerts but misses almost nothing; Scenario B sends only confident alerts but lets 4-in-10 attacks slip through.</div>
</div>

---

## Concept: Threshold Selection Table

A useful deliverable for stakeholders is a table showing what they get at each threshold:

| Threshold | Alerts (test set) | True attacks caught | False alarms | Recall |
|-----------|------------------:|--------------------:|-------------:|------:|
| 0.20 | 139 | 89 | 50 | 0.89 |
| 0.30 | 117 | 84 | 33 | 0.84 |
| 0.50 | 101 | 83 | 18 | 0.83 |
| 0.70 |  79 | 72 |  7 | 0.72 |
| 0.90 |  66 | 62 |  4 | 0.62 |

This makes the tradeoff concrete: "Do we want 139 alerts/day with 89% catch rate, or 66 alerts/day with 62% catch rate?"

<div class="lecture-visual">
  <img src="/static/lecture_assets/me_threshold_table.png" alt="Grouped bar chart at five thresholds (0.20, 0.30, 0.50, 0.70, 0.90). For each threshold three bars: total alerts (grey), true attacks caught (green) and false alarms (orange). Bars shrink from left to right: at 0.20 the alerts bar is highest, at 0.90 it is lowest. A red dashed horizontal line marks the 100 actual attacks in the test set">
  <div class="vis-caption">Sliding the threshold reshapes the SOC's daily alert load. The grey bars (total alerts) shrink as threshold rises; the orange (false alarms) shrinks faster, but green (caught attacks) shrinks too.</div>
</div>

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
  0.05     0.435    0.940  0.595    216
  0.10     0.544    0.920  0.684    169
  0.20     0.640    0.890  0.745    139
  0.30     0.718    0.840  0.774    117
  0.40     0.764    0.840  0.800    110
  0.50     0.822    0.830  0.826    101   ← max F1
  0.60     0.844    0.760  0.800     90
  0.70     0.911    0.720  0.804     79
  0.80     0.932    0.690  0.793     74
  0.90     0.939    0.620  0.747     66

TASK 2 — Scenario A (recall >= 0.95):
Threshold: 0.04
Recall:    0.960, Precision: 0.409
Test alerts: 235 / 2000 (Daily ≈ 1175)

TASK 3 — Scenario B (precision >= 0.95):
Threshold: 0.92
Precision: 0.952, Recall: 0.590
Test alerts: 62 / 2000 (Daily ≈ 310)

TASK 4 (BONUS) — Stakeholder report:
Scenario A (Catch All) — threshold 0.04:
  Attacks caught per day:    480 / 500
  Attacks missed per day:     20
  False alarms per day:      695
  Total reviews/day:        1175
  Estimated analyst time:    ~98 hours/day

Scenario B (Trusted Alerts) — threshold 0.92:
  Attacks caught per day:    295 / 500
  Attacks missed per day:    205
  False alarms per day:       15
  Total reviews/day:         310
  Estimated analyst time:   ~25 hours/day
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Picking threshold to maximise accuracy | Wrong objective for security | Optimise recall or F1 instead |
| Choosing threshold on test data without holdout | Optimistic — overfits the threshold | Ideally use a validation set for threshold tuning |
| Not documenting the chosen threshold | Model behaviour unclear in production | Always document threshold with justification |
| Treating threshold as fixed forever | Attack patterns change | Plan for periodic recalibration |
