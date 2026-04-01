# Exercise 3 — Choosing K

> Back to [1_lab_guide.md](1_lab_guide.md)

## What You Will Learn

- What the inertia (elbow) method shows when choosing K
- What silhouette score measures and how to use it
- How to combine both methods to choose a defensible K value
- Why the "right" K depends on your security goals, not just the metrics

---

## Concept: Elbow Method (Inertia)

Inertia = sum of squared distances from each sample to its nearest centroid. Lower inertia = tighter clusters, but K=N (every point is its own cluster) has inertia=0 trivially.

Plot inertia vs K. Look for the "elbow" where inertia drops steeply then flattens. The elbow suggests the K where adding more clusters gives diminishing improvement.

> **Want to go deeper?** [k-means clustering (Wikipedia)](https://en.wikipedia.org/wiki/K-means_clustering)

---

## Concept: Silhouette Score

For each sample:
- a = mean distance to other samples in same cluster
- b = mean distance to samples in the nearest other cluster
- s = (b - a) / max(a, b)

Ranges from -1 (wrong cluster) to +1 (perfect cluster). Mean silhouette score across all samples is a single quality number.

Higher = better. Typical values for good clustering: 0.3–0.7.

---

## What Each Task Asks You to Do

### Task 1 — Compute Inertia for K=2 to K=10
Run K-Means for each K. Record inertia. Plot the elbow curve.

### Task 2 — Compute Silhouette Score for K=2 to K=10
Compute mean silhouette score for each K. Plot. Identify the K with the highest score.

### Task 3 — Pick K
Based on both methods, choose K and justify your choice in a print statement.

### Task 4 (BONUS) — Silhouette Plot
Create a full silhouette diagram for your chosen K (visualise per-sample silhouette values grouped by cluster).

---

## Expected Outputs

```
TASK 1 — Inertia (elbow):
K=2: 8234.1
K=3: 6012.3
K=4: 4218.5  ← elbow here
K=5: 3891.2
...

TASK 2 — Silhouette scores:
K=2: 0.412
K=3: 0.531
K=4: 0.618  ← highest
K=5: 0.601
...

TASK 3 — Chosen K:
Both methods suggest K=4. This matches the 4 known traffic types.
Recommended K: 4
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Not scaling before computing silhouette | Score is meaningless | Scale first |
| Choosing K based solely on elbow | Elbow can be ambiguous | Always also compute silhouette |
| Expecting K to perfectly match true classes | K-Means may split or merge classes | Use domain knowledge to validate |

---

> Next: [exercise4_anomaly_scoring.md](exercise4_anomaly_scoring.md)
