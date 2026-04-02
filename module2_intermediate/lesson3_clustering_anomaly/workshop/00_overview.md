# Lesson 2.3 — Workshop Guide
## Network Anomaly Detection with K-Means Clustering

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_unsupervised_framing.py`)

## What This Workshop Covers

You will apply K-Means clustering to unlabelled network traffic to discover behavioural groups. Normal traffic forms tight, predictable clusters; attacks become outliers with high distance to any centroid. You will choose the right number of clusters, score anomalies by centroid distance, and verify that your anomalies overlap with the known attack labels.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_unsupervised_framing.md](01_guide_unsupervised_framing.md) | [01_lab_unsupervised_framing.md](01_lab_unsupervised_framing.md) | No labels available, what clustering finds |
| 2 | [02_guide_kmeans_and_visualisation.md](02_guide_kmeans_and_visualisation.md) | [02_lab_kmeans_and_visualisation.md](02_lab_kmeans_and_visualisation.md) | KMeans, PCA to 2D, colour-coded cluster plot |
| 3 | [03_guide_choosing_k.md](03_guide_choosing_k.md) | [03_lab_choosing_k.md](03_lab_choosing_k.md) | Elbow method, silhouette score |
| 4 | [04_guide_anomaly_scoring.md](04_guide_anomaly_scoring.md) | [04_lab_anomaly_scoring.md](04_lab_anomaly_scoring.md) | Distance from centroid, threshold, flag top anomalies |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson3_clustering_anomaly/workshop/01_solution_unsupervised_framing.py
```

## Next Lesson

[Lesson 2.4 — Overfitting and Cross-Validation](../../lesson4_overfitting_crossval/workshop/00_overview.md)
