# Exercise 3 — Choosing K

> Back to [README.md](README.md)

## What You Will Learn

- What the inertia (elbow) method shows when choosing K
- What silhouette score measures and how to use it
- How to combine both methods to choose a defensible K value
- Why the "right" K depends on your security goals, not just the metrics

---

## Concept: Elbow Method (Inertia)

Inertia = sum of squared distances from each sample to its nearest centroid. Lower inertia = tighter clusters, but K=N (every point is its own cluster) has inertia=0 trivially.

**The same dataset measured two ways across `K = 2..7` (real lab numbers)**

| K | Inertia (lower is tighter clusters) | Silhouette (higher is better) | What this row tells you |
|---:|---:|---:|---|
| 2 | 22 465 | 0.232 | too few clusters; both metrics weak |
| 3 | 17 685 | 0.264 | improving but still merging real groups |
| **4** | **13 484** | **0.309** | the **elbow** in inertia *and* the peak silhouette — chosen K |
| 5 | 12 831 | 0.229 | adding clusters barely tightens fit and silhouette drops |
| 6 | 12 221 | 0.208 | inertia plateaus, silhouette keeps falling |
| 7 | 11 715 | 0.163 | clearly past the elbow |

Both metrics agree: `K = 4` is the sweet spot. **Inertia** is the curve that drops steeply then flattens — its "elbow" marks the K where extra clusters stop buying tightness. **Silhouette** is a separate score that peaks at the K where samples sit nicely inside their own cluster and far from neighbouring clusters. When the two methods agree, you have a defensible choice; when they disagree, lean on domain knowledge.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_elbow_curve.png" alt="Line chart of inertia versus K from K=2 to K=10 with cyan circle markers. The line drops steeply from about 22500 at K=2 to 13500 at K=4, then flattens almost horizontally through K=10. An orange dashed vertical line marks the elbow at K=4.">
  <div class="vis-caption">Real lab elbow curve. Inertia is roughly halved going from K=2 to K=4, then barely moves — adding clusters past 4 buys almost nothing.</div>
</div>

> **Want to go deeper?** [k-means clustering (Wikipedia)](https://en.wikipedia.org/wiki/K-means_clustering)

---

## Concept: Silhouette Score

For each sample:
- a = mean distance to other samples in same cluster
- b = mean distance to samples in the nearest other cluster
- s = (b - a) / max(a, b)

Ranges from -1 (wrong cluster) to +1 (perfect cluster). Mean silhouette score across all samples is a single quality number.

Higher = better. Typical values for good clustering: 0.3–0.7.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_silhouette_curve.png" alt="Line chart of silhouette score versus K from K=2 to K=10 with violet square markers. The score climbs from 0.23 at K=2 to a peak of 0.31 at K=4 (highlighted with an orange ring), then falls steadily to 0.13 at K=10.">
  <div class="vis-caption">Silhouette score across the same K range. The peak at K=4 sits exactly where the elbow says — two independent metrics, same answer.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_silhouette_diagram.png" alt="Silhouette diagram for K=4 showing four horizontal bands of bars, one per cluster, coloured cyan, orange, green, red. Within each band the bars are sorted ascending; most bars extend well past 0.3 to the right of a vertical dashed mean line.">
  <div class="vis-caption">Per-sample silhouette diagram for K=4. Each band is one cluster; bars extending well past the dashed mean line are samples comfortably inside their cluster.</div>
</div>

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
K=2: 22464.9
K=3: 17685.0
K=4: 13483.5  ← elbow here
K=5: 12830.9
K=6: 12220.7
...

TASK 2 — Silhouette scores:
K=2: 0.232
K=3: 0.264
K=4: 0.309  ← highest
K=5: 0.229
K=6: 0.208
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
