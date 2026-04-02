# Exercise 2 — K-Means and Visualisation
#
# Goal: Fit K-Means (k=4) on network traffic data, visualise clusters
#       in 2D PCA space, compare cluster assignments to true labels,
#       and measure cluster purity.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
# Four traffic types: benign, port_scan, exfil, DoS — 750 samples each.
n_per = 750

def make_full_dataset():
    benign = pd.DataFrame({
        'connection_rate': np.random.normal(10, 3, n_per).clip(1, 25),
        'bytes_sent': np.random.normal(5000, 1500, n_per).clip(100, 15000),
        'bytes_received': np.random.normal(8000, 2000, n_per).clip(100, 20000),
        'unique_dest_ports': np.random.poisson(3, n_per).clip(1, 10),
        'duration_seconds': np.random.normal(30, 10, n_per).clip(1, 120),
        'failed_connections': np.random.poisson(0.5, n_per),
        'true_label': 0, 'true_class': 'benign'})
    port_scan = pd.DataFrame({
        'connection_rate': np.random.normal(25, 8, n_per).clip(5, 60),
        'bytes_sent': np.random.normal(500, 200, n_per).clip(50, 2000),
        'bytes_received': np.random.normal(300, 100, n_per).clip(0, 1000),
        'unique_dest_ports': np.random.normal(45, 10, n_per).clip(20, 100).astype(int),
        'duration_seconds': np.random.normal(5, 2, n_per).clip(1, 20),
        'failed_connections': np.random.poisson(8, n_per),
        'true_label': 1, 'true_class': 'port_scan'})
    exfil = pd.DataFrame({
        'connection_rate': np.random.normal(8, 2, n_per).clip(1, 20),
        'bytes_sent': np.random.normal(80000, 25000, n_per).clip(20000, 250000),
        'bytes_received': np.random.normal(1000, 300, n_per).clip(100, 5000),
        'unique_dest_ports': np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds': np.random.normal(180, 60, n_per).clip(60, 600),
        'failed_connections': np.random.poisson(0.2, n_per),
        'true_label': 2, 'true_class': 'exfil'})
    dos = pd.DataFrame({
        'connection_rate': np.random.normal(200, 40, n_per).clip(80, 500),
        'bytes_sent': np.random.normal(200, 80, n_per).clip(40, 600),
        'bytes_received': np.random.normal(100, 40, n_per).clip(0, 400),
        'unique_dest_ports': np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds': np.random.normal(0.5, 0.2, n_per).clip(0.1, 2),
        'failed_connections': np.random.poisson(3, n_per),
        'true_label': 3, 'true_class': 'DoS'})
    return pd.concat([benign, port_scan, exfil, dos],
                     ignore_index=True).sample(frac=1, random_state=42)

df_full = make_full_dataset()

FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df_full[FEATURES]
true_labels  = df_full['true_label'].values
true_classes = df_full['true_class'].values

# ============================================================
# TASK 1 — K-Means clustering (k=4)
# ============================================================
# Scale features (critical for distance-based algorithms) then
# fit K-Means with 4 clusters — one per expected traffic type.
print("=" * 60)
print("TASK 1 — K-Means clustering (k=4)")
print("=" * 60)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

unique, counts = np.unique(cluster_labels, return_counts=True)
print("Cluster sizes:")
for c, n in zip(unique, counts):
    print(f"  Cluster {c}: {n} samples")

# ============================================================
# TASK 2 — PCA visualisation of clusters
# ============================================================
# Reduce to 2D with PCA so we can plot the clusters. Mark centroids
# with black 'X' markers.
print("\n" + "=" * 60)
print("TASK 2 — PCA visualisation of clusters")
print("=" * 60)

pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X_scaled)
print(f"PCA explained variance: {pca.explained_variance_ratio_}")

colours = ['steelblue', 'red', 'green', 'orange']
plt.figure(figsize=(9, 7))
for c in range(4):
    mask = cluster_labels == c
    plt.scatter(X_2d[mask, 0], X_2d[mask, 1], alpha=0.2, s=8,
                color=colours[c], label=f'Cluster {c}')

# Project centroids into PCA space and plot them
centroids_2d = pca.transform(kmeans.cluster_centers_)
plt.scatter(centroids_2d[:, 0], centroids_2d[:, 1],
            c='black', marker='X', s=150, zorder=10, label='Centroids')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('K-Means Clusters in PCA Space')
plt.legend()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_ex2_clusters.png')
plt.close()
print("Cluster scatter plot saved.")

# ============================================================
# TASK 3 — Reveal true labels for comparison
# ============================================================
# Same 2D PCA view, but coloured by the actual traffic class.
# Compare to TASK 2 to see how well K-Means recovered the groups.
print("\n" + "=" * 60)
print("TASK 3 — Reveal true labels for comparison")
print("=" * 60)

class_colours = {'benign': 'steelblue', 'port_scan': 'orange',
                 'exfil': 'green', 'DoS': 'red'}
plt.figure(figsize=(9, 7))
for cls in ['benign', 'port_scan', 'exfil', 'DoS']:
    mask = true_classes == cls
    plt.scatter(X_2d[mask, 0], X_2d[mask, 1], alpha=0.2, s=8,
                color=class_colours[cls], label=cls)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('True Class Labels in PCA Space')
plt.legend()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_ex2_true_labels.png')
plt.close()
print("True label scatter plot saved.")

# ============================================================
# TASK 4 (BONUS) — Cluster purity analysis
# ============================================================
# For each cluster, find the dominant true class and compute purity
# (= majority_class_count / cluster_size). High purity means K-Means
# successfully separated the traffic types.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Cluster purity analysis")
print("=" * 60)

print(f"{'Cluster':>7} | {'Dominant class':>14} | {'Purity':>7} | {'Size':>5}")
print("-" * 45)
for c in range(4):
    mask = cluster_labels == c
    classes_in_cluster = true_classes[mask]
    dominant = pd.Series(classes_in_cluster).value_counts().idxmax()
    count    = pd.Series(classes_in_cluster).value_counts().max()
    total    = mask.sum()
    purity   = count / total
    print(f"{c:>7} | {dominant:>14} | {purity:>7.1%} | {total:>5}")

print("\n--- Exercise 2 complete. Move to ../3_choosing_k/solve.py ---")
