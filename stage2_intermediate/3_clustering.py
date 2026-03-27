# Lesson 2.3 — k-Means Clustering for Network Anomaly Detection
#
# Goal: Use unsupervised clustering to find anomalous network connections
# WITHOUT using any attack labels. This is a common approach when you
# don't have labelled data — which is most of the time.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

np.random.seed(42)

# ── 1. Generate network traffic WITHOUT labels ─────────────────────────────────
# This simulates what you'd have in a real scenario: just raw connection data.
n_normal = 2000
n_anomaly = 60   # small fraction of anomalies hidden in the data

# Normal traffic — three distinct behavioural groups
web_browsing = pd.DataFrame({
    'bytes_sent':   np.random.lognormal(7, 0.8, n_normal // 3),
    'bytes_recv':   np.random.lognormal(9, 1.0, n_normal // 3),
    'duration_s':   np.random.exponential(20, n_normal // 3).clip(1, 120),
    'packets':      np.random.poisson(40, n_normal // 3).clip(5, 200),
    'dest_port':    np.random.choice([80, 443], n_normal // 3),
})
ssh_sessions = pd.DataFrame({
    'bytes_sent':   np.random.lognormal(8, 1.2, n_normal // 3),
    'bytes_recv':   np.random.lognormal(8, 1.2, n_normal // 3),
    'duration_s':   np.random.normal(600, 300, n_normal // 3).clip(30, 3600),
    'packets':      np.random.poisson(200, n_normal // 3).clip(10, 1000),
    'dest_port':    np.full(n_normal // 3, 22),
})
dns_queries = pd.DataFrame({
    'bytes_sent':   np.random.normal(80, 20, n_normal // 3).clip(20, 200),
    'bytes_recv':   np.random.normal(120, 40, n_normal // 3).clip(30, 400),
    'duration_s':   np.random.exponential(0.1, n_normal // 3).clip(0.01, 1),
    'packets':      np.random.poisson(2, n_normal // 3).clip(1, 6),
    'dest_port':    np.full(n_normal // 3, 53),
})

# Anomalies — data exfiltration signature (large upload, unusual port)
anomalies = pd.DataFrame({
    'bytes_sent':   np.random.lognormal(13, 0.5, n_anomaly),   # very large uploads
    'bytes_recv':   np.random.lognormal(5, 0.5, n_anomaly),
    'duration_s':   np.random.normal(1800, 600, n_anomaly).clip(600, 7200),
    'packets':      np.random.poisson(1500, n_anomaly).clip(500, 5000),
    'dest_port':    np.random.randint(10000, 60000, n_anomaly),
})

normal_df = pd.concat([web_browsing, ssh_sessions, dns_queries], ignore_index=True)
normal_df['true_label'] = 0  # for evaluation only — not used in clustering

anomalies['true_label'] = 1

all_data = pd.concat([normal_df, anomalies], ignore_index=True).sample(frac=1, random_state=42)

feature_cols = ['bytes_sent', 'bytes_recv', 'duration_s', 'packets', 'dest_port']
X_raw  = all_data[feature_cols].values
y_true = all_data['true_label'].values   # only for final evaluation

print("=== Dataset (no labels used in clustering) ===")
print(f"Total connections: {len(all_data)} | Hidden anomalies: {y_true.sum()}")

# ── 2. Scale features (critical for distance-based algorithms) ────────────────
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

# ── 3. Choose k with the Elbow method ─────────────────────────────────────────
print("\n=== Elbow Method ===")
inertias    = []
sil_scores  = []
k_range     = range(2, 10)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X, km.labels_))
    print(f"  k={k}: inertia={km.inertia_:.0f}  silhouette={sil_scores[-1]:.3f}")

# ── 4. Fit with chosen k ───────────────────────────────────────────────────────
best_k = 3  # web browsing, SSH, DNS — matches our data generation
km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
km.fit(X)

all_data['cluster'] = km.labels_

print(f"\n=== Cluster sizes (k={best_k}) ===")
print(all_data['cluster'].value_counts().sort_index())

# ── 5. Anomaly detection via distance to nearest centroid ─────────────────────
distances = km.transform(X).min(axis=1)   # distance to nearest centroid
threshold = np.percentile(distances, 97)  # flag top 3% as anomalous

all_data['distance']   = distances
all_data['flagged']    = (distances > threshold).astype(int)

# Evaluate: of the flagged connections, how many were true anomalies?
flagged    = all_data[all_data['flagged'] == 1]
true_anom  = all_data[all_data['true_label'] == 1]

precision = (flagged['true_label'] == 1).mean()
recall    = flagged['true_label'].sum() / true_anom.shape[0]

print(f"\n=== Anomaly Detection Results (97th percentile threshold) ===")
print(f"Flagged connections : {all_data['flagged'].sum()}")
print(f"True anomalies      : {true_anom.shape[0]}")
print(f"Precision           : {precision:.2f}  ({precision*100:.0f}% of alerts are real)")
print(f"Recall              : {recall:.2f}  ({recall*100:.0f}% of anomalies caught)")

# ── 6. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Elbow plot
axes[0, 0].plot(k_range, inertias, marker='o', color='steelblue')
axes[0, 0].set_xlabel('k (number of clusters)')
axes[0, 0].set_ylabel('Inertia')
axes[0, 0].set_title('Elbow Method — Choose k')

# Silhouette scores
axes[0, 1].plot(k_range, sil_scores, marker='o', color='crimson')
axes[0, 1].set_xlabel('k')
axes[0, 1].set_ylabel('Silhouette Score')
axes[0, 1].set_title('Silhouette Score (higher = better separation)')

# 2D cluster visualisation using PCA
pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for c in range(best_k):
    mask = km.labels_ == c
    axes[1, 0].scatter(X_2d[mask, 0], X_2d[mask, 1], alpha=0.3, s=10,
                       color=colors[c], label=f'Cluster {c}')
anom_mask = y_true == 1
axes[1, 0].scatter(X_2d[anom_mask, 0], X_2d[anom_mask, 1],
                   color='red', s=30, marker='x', label='True anomaly', zorder=5)
axes[1, 0].set_title('Clusters in 2D (PCA) with True Anomalies Marked')
axes[1, 0].legend(fontsize=7)

# Distance distribution
axes[1, 1].hist(distances[y_true == 0], bins=50, alpha=0.6, label='Normal', color='steelblue')
axes[1, 1].hist(distances[y_true == 1], bins=20, alpha=0.8, label='Anomaly', color='crimson')
axes[1, 1].axvline(threshold, color='black', linestyle='--', label=f'Threshold (97th pct)')
axes[1, 1].set_xlabel('Distance to Nearest Centroid')
axes[1, 1].set_title('Anomaly Score Distribution')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_clustering.png')
plt.show()
print("\nPlot saved to stage2_intermediate/lesson3_clustering.png")
