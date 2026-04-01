# Exercise 4 — Anomaly Scoring

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- How distance from centroid functions as an anomaly score
- How to set a threshold on the anomaly score to flag suspicious connections
- How to verify that flagged anomalies overlap with true attack labels
- The limitations of K-Means for anomaly detection

---

## Concept: Distance as Anomaly Score

After K-Means, every sample belongs to a cluster. Its **anomaly score** = its distance from its assigned centroid.

- Normal samples are close to their centroid (low anomaly score)
- Attack samples that don't fit any normal cluster are far from all centroids (high score)

```python
# Distance from each sample to its own centroid
distances = np.min(kmeans.transform(X_scaled), axis=1)
```

`kmeans.transform(X_scaled)` returns an (n, K) matrix of distances from each sample to each centroid. `np.min(..., axis=1)` gives the distance to the nearest centroid.

---

## Concept: Setting the Threshold

Choose a percentile threshold:
- Top 5% of distances are flagged as anomalous
- This is calibrated to your false-positive budget

Or use a statistical approach: mean + 2σ of distances.

---

## What Each Task Asks You to Do

### Task 1 — Compute Anomaly Scores
Fit K-Means with K=4 on X_scaled. Compute the distance from each sample to its nearest centroid. Print distribution statistics.

### Task 2 — Flag Anomalies
Set the threshold at the 95th percentile. Flag the top 5% as anomalous. Print how many flagged.

### Task 3 — Verify with True Labels
Of the flagged anomalies, how many are actually attacks (true_label != 0)? Print: precision (fraction flagged that are attacks) and recall (fraction of all attacks that were flagged).

### Task 4 (BONUS) — Plot Anomaly Score Distribution
Plot a histogram of anomaly scores. Mark the threshold. Shade flagged anomalies in red.

---

## Expected Outputs

```
TASK 1 — Anomaly scores:
mean: 1.82, std: 0.94, max: 8.21

TASK 2 — Threshold at 95th percentile: 3.87
Flagged anomalies: 150 / 3000 (5.0%)

TASK 3 — Verification:
Of 150 flagged: 118 are true attacks
Precision (anomalies that are attacks): 78.7%
Recall  (attacks that were flagged):    5.2%

Note: K-Means anomaly scoring has low recall because attacks form their OWN
dense clusters (e.g., DoS has many samples → forms its own cluster).
It detects samples that don't belong to ANY cluster — true outliers.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using raw X (not scaled) for transform | Distances are biased | Use X_scaled |
| Expecting K-Means to catch all attacks | Many attacks form clusters themselves | K-Means detects isolation, not all attack types |
| Setting threshold too low | Too many false alarms | Use 90th-95th percentile |

---

> Back to [1_lab_guide.md](1_lab_guide.md) | Next: [Lesson 2.4 Overfitting](../../lesson4_overfitting_crossval/workshop/1_lab_guide.md)
