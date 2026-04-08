# Exercise 4 — Anomaly Scoring

> Back to [README.md](README.md)

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

**Anomaly score = distance from each sample to its nearest centroid**

| Sample | Sits inside cluster? | Distance to nearest centroid | Verdict |
|---|---|---:|---|
| Normal sample near Centroid 0 | yes | **0.8** | low score → benign |
| Normal sample near Centroid 1 | yes | **0.6** | low score → benign |
| Outlier far from every centroid | no | **6.2** | high score → **anomaly** |

The reasoning is purely geometric: K-Means already pulled the dense, repetitive behaviours into tight balls around their centroids, so anything that lives in the empty space *between* the balls is by definition far from any known pattern — a candidate to investigate.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_distance_concept.png" alt="2D scatter plot showing two cyan and violet point clouds, each with a black X marker labelled centroid A and centroid B. A green circular point near centroid A is connected to it with a short solid green line labelled 'normal — short distance'. A red star far from both centroids has a long dashed red line connecting it to centroid A labelled 'anomaly — far from every centroid'.">
  <div class="vis-caption">The geometric intuition. Normal points hug a centroid; anomalies sit in empty space between them. The score is just "how far is your nearest centroid?".</div>
</div>

`kmeans.transform(X_scaled)` returns an (n, K) matrix of distances from each sample to each centroid. `np.min(..., axis=1)` gives the distance to the nearest centroid.

> **Want to go deeper?** [Anomaly detection (Wikipedia)](https://en.wikipedia.org/wiki/Anomaly_detection)

---

## Concept: Setting the Threshold

Choose a percentile threshold:
- Top 5% of distances are flagged as anomalous
- This is calibrated to your false-positive budget

**Anomaly score distribution at a glance (real lab numbers)**

| Score range | Share of samples | Status |
|---|---:|---|
| 0.0 – 2.0 | majority of the dataset | obvious normals — sit right on top of a centroid |
| 2.0 – 3.09 | the long right tail of the bell | grey zone — far-ish but inside the threshold |
| **> 3.09 (95th percentile)** | **top 5%** | **flagged as anomalies** |

The threshold (`3.09` here) is the 95th-percentile of the score distribution. Sliding it left raises the alert volume; sliding it right is more conservative. A purely statistical alternative is `mean + 2σ`, which assumes a roughly Gaussian tail.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_anomaly_histogram.png" alt="Histogram of anomaly scores for 3000 connections. Cyan bars on the left form a roughly Gaussian bell, red bars on the right show the top 5% flagged anomalies. A black dashed vertical line marks the 95th percentile threshold at 3.09. An annotation box reports flagged 150/3000, true positives 123, precision 82%, recall 5.5%.">
  <div class="vis-caption">Real lab anomaly score distribution. The red tail past the threshold contains 150 connections — 123 of them are real attacks, the rest are unusual but legitimate.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_pr_recall_tradeoff.png" alt="Line chart with threshold percentile from 80 to 99 on the x-axis. A cyan line labelled Precision rises from about 0.6 to 0.95. An orange line labelled Recall falls from about 0.20 down to 0.02. A black dashed vertical line at the 95th percentile marks the default threshold.">
  <div class="vis-caption">Sweep the threshold and you trade alert volume for purity. Recall stays painfully low at every setting — the takeaway is that K-Means anomaly scoring catches outliers, not whole attack clusters.</div>
</div>

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
mean: 2.03, std: 0.61, max: 5.12

TASK 2 — Threshold at 95th percentile: 3.09
Flagged anomalies: 150 / 3000 (5.0%)

TASK 3 — Verification:
Of 150 flagged: 123 are true attacks
Precision (anomalies that are attacks): 82.0%
Recall  (attacks that were flagged):    5.5%

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
