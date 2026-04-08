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

The result: K clusters, each with a centroid. Distance from centroid = "how typical" a sample is for its cluster. High distance = anomalous.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_kmeans_iterations.png" alt="Four side-by-side scatter panels labelled Iteration 0 through Iteration 3 showing the same 240 toy points coloured by cluster assignment. Black X markers show centroid positions. The centroids start in poor positions and migrate to the centre of each colour group across iterations.">
  <div class="vis-caption">K-Means in action on a four-blob toy dataset. Centroids (black X) start in deliberately bad positions and converge in three iterations: assign → recompute → assign → done.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_kmeans_pca.png" alt="2D PCA scatter plot of 3000 connections coloured by K-Means cluster. Four overlapping but distinct clusters in cyan, orange, green, and red. Four black X markers mark the centroids in PCA space.">
  <div class="vis-caption">Real lab K-Means run with K=4 on the 6-D scaled features, projected to 2-D with PCA. Four clusters, four centroids — and they roughly correspond to the four traffic types.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/cluster_purity_grid.png" alt="4x4 heatmap showing how K-Means clusters split into true classes. Rows are clusters C0 to C3 each labelled with their dominant class; columns are benign, port_scan, exfil, DoS. The diagonal cells are dark blue and contain values around 700; off-diagonal cells are pale and contain small numbers.">
  <div class="vis-caption">Cluster vs true-class confusion grid. The dark diagonal means each cluster is dominated by one traffic type — purities range from 91% to 98% on the real lab data.</div>
</div>

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
Cluster sizes: [781, 723, 720, 776]  (roughly equal — good sign)

TASK 2 — PCA cluster plot created.

TASK 3 — True labels revealed:
Cluster 0 → mostly 'benign'    (purity 91.4%)
Cluster 1 → mostly 'exfil'     (purity 96.4%)
Cluster 2 → mostly 'port_scan' (purity 98.2%)
Cluster 3 → mostly 'DoS'       (purity 92.7%)

TASK 4 (BONUS) — Cluster purity:
Cluster | Dominant class | Purity
      0 | benign         | 91.4%
      1 | exfil          | 96.4%
      2 | port_scan      | 98.2%
      3 | DoS            | 92.7%
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Running K-Means without scaling | bytes_sent (0-250000) dominates; clusters ignore other features | Always StandardScale before K-Means |
| Using K-Means result as ground truth | K-Means clusters ≠ true classes (labels unknown) | Validate clusters with domain knowledge |
| Expecting perfect purity | Real data overlaps; K-Means is approximate | Purity > 85% is good |
