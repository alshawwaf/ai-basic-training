# Lesson 2.3 — Workshop Guide
## Network Anomaly Detection with K-Means Clustering

> Read first: [../3_clustering_anomaly_detection.md](../3_clustering_anomaly_detection.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will apply K-Means clustering to unlabelled network traffic to discover behavioural groups. Normal traffic forms tight, predictable clusters; attacks become outliers with high distance to any centroid. You will choose the right number of clusters, score anomalies by centroid distance, and verify that your anomalies overlap with the known attack labels.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_unsupervised_framing.md](exercise1_unsupervised_framing.md) | [exercise1_unsupervised_framing.py](exercise1_unsupervised_framing.py) | No labels available, what clustering finds |
| 2 | [exercise2_kmeans_and_visualisation.md](exercise2_kmeans_and_visualisation.md) | [exercise2_kmeans_and_visualisation.py](exercise2_kmeans_and_visualisation.py) | KMeans, PCA to 2D, colour-coded cluster plot |
| 3 | [exercise3_choosing_k.md](exercise3_choosing_k.md) | [exercise3_choosing_k.py](exercise3_choosing_k.py) | Elbow method, silhouette score |
| 4 | [exercise4_anomaly_scoring.md](exercise4_anomaly_scoring.md) | [exercise4_anomaly_scoring.py](exercise4_anomaly_scoring.py) | Distance from centroid, threshold, flag top anomalies |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson3_clustering_anomaly/workshop/exercise1_unsupervised_framing.py
```

## Next Lesson

[Lesson 2.4 — Overfitting and Cross-Validation](../../lesson4_overfitting_crossval/workshop/1_lab_guide.md)
