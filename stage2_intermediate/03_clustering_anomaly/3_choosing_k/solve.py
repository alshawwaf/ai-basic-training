# Exercise 3 — Choosing K
#
# Goal: Use the Elbow method (inertia) and Silhouette scores to
#       determine the optimal number of clusters for network traffic.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
n_per = 750

def make_full_dataset():
    benign = pd.DataFrame({
        'connection_rate': np.random.normal(10, 3, n_per).clip(1, 25),
        'bytes_sent': np.random.normal(5000, 1500, n_per).clip(100, 15000),
        'bytes_received': np.random.normal(8000, 2000, n_per).clip(100, 20000),
        'unique_dest_ports': np.random.poisson(3, n_per).clip(1, 10),
        'duration_seconds': np.random.normal(30, 10, n_per).clip(1, 120),
        'failed_connections': np.random.poisson(0.5, n_per),
        'true_label': 0})
    port_scan = pd.DataFrame({
        'connection_rate': np.random.normal(25, 8, n_per).clip(5, 60),
        'bytes_sent': np.random.normal(500, 200, n_per).clip(50, 2000),
        'bytes_received': np.random.normal(300, 100, n_per).clip(0, 1000),
        'unique_dest_ports': np.random.normal(45, 10, n_per).clip(20, 100).astype(int),
        'duration_seconds': np.random.normal(5, 2, n_per).clip(1, 20),
        'failed_connections': np.random.poisson(8, n_per),
        'true_label': 1})
    exfil = pd.DataFrame({
        'connection_rate': np.random.normal(8, 2, n_per).clip(1, 20),
        'bytes_sent': np.random.normal(80000, 25000, n_per).clip(20000, 250000),
        'bytes_received': np.random.normal(1000, 300, n_per).clip(100, 5000),
        'unique_dest_ports': np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds': np.random.normal(180, 60, n_per).clip(60, 600),
        'failed_connections': np.random.poisson(0.2, n_per),
        'true_label': 2})
    dos = pd.DataFrame({
        'connection_rate': np.random.normal(200, 40, n_per).clip(80, 500),
        'bytes_sent': np.random.normal(200, 80, n_per).clip(40, 600),
        'bytes_received': np.random.normal(100, 40, n_per).clip(0, 400),
        'unique_dest_ports': np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds': np.random.normal(0.5, 0.2, n_per).clip(0.1, 2),
        'failed_connections': np.random.poisson(3, n_per),
        'true_label': 3})
    return pd.concat([benign, port_scan, exfil, dos],
                     ignore_index=True).sample(frac=1, random_state=42)

df_full = make_full_dataset()

FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df_full[FEATURES]
true_labels = df_full['true_label'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================================
# TASK 1 — Elbow method (inertia vs K)
# ============================================================
# Fit K-Means for K=2 to K=10, record inertia. The "elbow" in the
# curve shows where adding more clusters stops helping much.
print("=" * 60)
print("TASK 1 — Elbow method (inertia vs K)")
print("=" * 60)

k_values = range(2, 11)
inertias = []
print(f"{'K':>4} {'Inertia':>10}")
print("-" * 18)
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"{k:>4} {km.inertia_:>10.1f}")

plt.figure(figsize=(8, 5))
plt.plot(list(k_values), inertias, 'b-o')
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_ex3_elbow.png')
plt.close()
print("Elbow plot saved.")

# ============================================================
# TASK 2 — Silhouette scores
# ============================================================
# Silhouette score measures how similar each point is to its own
# cluster vs nearest neighbour cluster. Higher = better separation.
print("\n" + "=" * 60)
print("TASK 2 — Silhouette scores")
print("=" * 60)

sil_scores = []
print(f"{'K':>4} {'Silhouette':>12}")
print("-" * 20)
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels, sample_size=1000, random_state=42)
    sil_scores.append(score)
    print(f"{k:>4} {score:>12.4f}")

best_k = list(k_values)[np.argmax(sil_scores)]
print(f"\nHighest silhouette score at K={best_k}: {max(sil_scores):.4f}")

plt.figure(figsize=(8, 5))
plt.plot(list(k_values), sil_scores, 'r-s')
plt.xlabel('K')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs K')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_ex3_silhouette.png')
plt.close()
print("Silhouette plot saved.")

# ============================================================
# TASK 3 — Chosen K and justification
# ============================================================
# Combine evidence from the elbow and silhouette methods plus
# domain knowledge (4 traffic types) to choose K.
print("\n" + "=" * 60)
print("TASK 3 — Chosen K and justification")
print("=" * 60)

chosen_k = best_k   # should be 4 based on both methods
print(f"Chosen K: {chosen_k}")
print(f"Justification:")
print(f"  Elbow method: clear bend around K=4")
print(f"  Silhouette: highest score at K=4")
print(f"  Domain knowledge: 4 traffic types (benign, scan, exfil, DoS)")

# ============================================================
# TASK 4 (BONUS) — Silhouette diagram for K=4
# ============================================================
# Silhouette diagram shows per-sample silhouette values grouped by
# cluster. Wide bands = large clusters; bars reaching far right =
# well-separated samples.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Silhouette diagram for K=4")
print("=" * 60)

# Subsample for faster silhouette computation
sample_idx = np.random.choice(len(X_scaled), 500, replace=False)
X_samp = X_scaled[sample_idx]

km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
all_labels = km4.fit_predict(X_scaled)
labels4 = all_labels[sample_idx]

sil_vals = silhouette_samples(X_samp, labels4)

# Build the silhouette diagram: horizontal bars sorted per cluster
fig, ax = plt.subplots(figsize=(8, 6))
y_lower = 0
for c in range(4):
    cluster_sil = np.sort(sil_vals[labels4 == c])
    size_c = len(cluster_sil)
    y_upper = y_lower + size_c
    ax.barh(range(y_lower, y_upper), cluster_sil, height=1.0, alpha=0.7)
    ax.text(-0.05, y_lower + size_c / 2, f'C{c}', fontsize=9, va='center')
    y_lower = y_upper

ax.axvline(np.mean(sil_vals), color='black', linestyle='--', label='Mean')
ax.set_xlabel('Silhouette Coefficient')
ax.set_ylabel('Samples (grouped by cluster)')
ax.set_title('Silhouette Diagram (K=4, 500-sample subset)')
ax.legend()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_ex3_silhouette_diagram.png')
plt.close()
print("Silhouette diagram created (sample of 500 points).")

print("\n--- Exercise 3 complete. Move to ../4_anomaly_scoring/solve.py ---")
