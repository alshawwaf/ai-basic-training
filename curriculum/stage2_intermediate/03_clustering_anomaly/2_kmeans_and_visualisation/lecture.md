# Exercise 2 — K-Means and Visualisation

> Back to [README.md](README.md)

## What You Will Learn

- How K-Means assigns every sample to one of K clusters
- How to use PCA to reduce 6D feature space to 2D for visualisation
- How to plot clusters and reveal the true labels after clustering
- How well K-Means clusters align with actual traffic types

---

## Concept: K-Means Algorithm

K-Means iteratively:
1. Randomly initialise K centroid positions
2. Assign each sample to the nearest centroid
3. Recompute centroids as the mean of their assigned samples
4. Repeat until centroids stop moving

```
Step 1: Random centroids    Step 2: Assign nearest    Step 3: Recompute centroids
                                                        (repeat until stable)

    ·  ·                        ·  ·                        ·  ·
  ·  ★  ·  ·                  · [★] ·  ·                  ·  ★  ·  ·
    ·  ·                        ·  ·                        ·  ·
                ·                        ·                          ·
         ·  ·                     ·  ·                       ·  ·
   ·      ★    ·  ·         ·     [★]   ·  ·           ·      ★   ·  ·
         ·  ·                     ·  ·                       ·  ·

  ★ = centroid               [★] = centroid              ★ = centroid (moved)
  · = data point              ·  = assigned to             · = re-assigned
                                   nearest ★                    to new nearest ★
```

The result: K clusters, each with a centroid. Distance from centroid = "how typical" a sample is for its cluster. High distance = anomalous.

> **Want to go deeper?** [k-means clustering (Wikipedia)](https://en.wikipedia.org/wiki/K-means_clustering)

---

## Concept: PCA for Visualisation

Our feature space is 6D — impossible to plot directly. PCA (Principal Component Analysis) projects to 2D by finding the two directions of maximum variance. This is only for **visualisation** — the actual K-Means runs on all 6 features.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)
# X_2d.shape = (3000, 2)
```

---

## What Each Task Asks You to Do

### Task 1 — Scale and Fit K-Means
Scale X with StandardScaler. Fit `KMeans(n_clusters=4, random_state=42)`. Print cluster sizes. Check if they roughly match the 750-per-class distribution.

### Task 2 — PCA to 2D and Plot Clusters
Reduce to 2D with PCA. Plot each cluster with a different colour. Add centroids marked with a star. Title: "K-Means Clusters (before revealing labels)".

### Task 3 — Reveal True Labels
Colour the same 2D scatter by true class labels (not cluster assignments). Compare visually to Task 2. Compute the overlap: what fraction of each true class ended up in a single dominant cluster?

### Task 4 (BONUS) — Cluster Purity
For each cluster, count how many samples of each true class it contains. Compute purity = (majority class count) / (cluster size). Print purity for each cluster.

---

## Expected Outputs

```
TASK 1 — K-Means clustering:
Cluster sizes: [~752, ~749, ~751, ~748]  (roughly equal — good sign)

TASK 2 — PCA cluster plot created.

TASK 3 — True labels revealed:
Cluster 0 → mostly 'benign'    (purity ~91%)
Cluster 1 → mostly 'DoS'       (purity ~95%)
Cluster 2 → mostly 'exfil'     (purity ~89%)
Cluster 3 → mostly 'port_scan' (purity ~87%)

TASK 4 (BONUS) — Cluster purity:
Cluster | Dominant class | Purity
      0 | benign         | 91.2%
      1 | DoS            | 95.3%
      2 | exfil          | 89.1%
      3 | port_scan      | 87.4%
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Running K-Means without scaling | bytes_sent (0-250000) dominates; clusters ignore other features | Always StandardScale before K-Means |
| Using K-Means result as ground truth | K-Means clusters ≠ true classes (labels unknown) | Validate clusters with domain knowledge |
| Expecting perfect purity | Real data overlaps; K-Means is approximate | Purity > 85% is good |

---

> Next: [../3_choosing_k/lecture.md](../3_choosing_k/lecture.md)
