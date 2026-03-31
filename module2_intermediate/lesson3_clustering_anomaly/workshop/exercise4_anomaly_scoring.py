# =============================================================================
# LESSON 2.3 | WORKSHOP | Exercise 4 of 4
# Anomaly Scoring
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How distance from centroid creates an anomaly score without labels
# - How to set a percentile threshold to flag the top-N% most unusual samples
# - How to verify flagged anomalies against true attack labels
# - The limitations of K-Means anomaly detection
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson3_clustering_anomaly/workshop/exercise4_anomaly_scoring.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- Dataset (do not modify) ------------------------------------------------
np.random.seed(42)
n_per = 750
def make_full_dataset():
    benign = pd.DataFrame({'connection_rate': np.random.normal(10,3,n_per).clip(1,25),
        'bytes_sent': np.random.normal(5000,1500,n_per).clip(100,15000),
        'bytes_received': np.random.normal(8000,2000,n_per).clip(100,20000),
        'unique_dest_ports': np.random.poisson(3,n_per).clip(1,10),
        'duration_seconds': np.random.normal(30,10,n_per).clip(1,120),
        'failed_connections': np.random.poisson(0.5,n_per), 'true_label':0})
    port_scan = pd.DataFrame({'connection_rate': np.random.normal(25,8,n_per).clip(5,60),
        'bytes_sent': np.random.normal(500,200,n_per).clip(50,2000),
        'bytes_received': np.random.normal(300,100,n_per).clip(0,1000),
        'unique_dest_ports': np.random.normal(45,10,n_per).clip(20,100).astype(int),
        'duration_seconds': np.random.normal(5,2,n_per).clip(1,20),
        'failed_connections': np.random.poisson(8,n_per), 'true_label':1})
    exfil = pd.DataFrame({'connection_rate': np.random.normal(8,2,n_per).clip(1,20),
        'bytes_sent': np.random.normal(80000,25000,n_per).clip(20000,250000),
        'bytes_received': np.random.normal(1000,300,n_per).clip(100,5000),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(180,60,n_per).clip(60,600),
        'failed_connections': np.random.poisson(0.2,n_per), 'true_label':2})
    dos = pd.DataFrame({'connection_rate': np.random.normal(200,40,n_per).clip(80,500),
        'bytes_sent': np.random.normal(200,80,n_per).clip(40,600),
        'bytes_received': np.random.normal(100,40,n_per).clip(0,400),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(0.5,0.2,n_per).clip(0.1,2),
        'failed_connections': np.random.poisson(3,n_per), 'true_label':3})
    return pd.concat([benign,port_scan,exfil,dos],ignore_index=True).sample(frac=1,random_state=42)

df_full = make_full_dataset()
FEATURES = ['connection_rate','bytes_sent','bytes_received',
            'unique_dest_ports','duration_seconds','failed_connections']
X = df_full[FEATURES]
true_labels = df_full['true_label'].values
scaler  = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Fit K-Means with k=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Compute Anomaly Scores
# =============================================================================
# Use kmeans.transform(X_scaled) to get distances to all centroids.
# Take np.min(..., axis=1) to get distance to nearest centroid.
# Print: mean, std, min, max, 95th percentile of anomaly scores.

print("=" * 60)
print("TASK 1 — Anomaly score distribution")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   all_distances = kmeans.transform(X_scaled)   # shape (3000, 4)
#   anomaly_scores = np.min(all_distances, axis=1)
#   print(f"Mean:       {anomaly_scores.mean():.3f}")
#   print(f"Std:        {anomaly_scores.std():.3f}")
#   print(f"Min:        {anomaly_scores.min():.3f}")
#   print(f"Max:        {anomaly_scores.max():.3f}")
#   print(f"95th pct:   {np.percentile(anomaly_scores, 95):.3f}")

# EXPECTED OUTPUT:
# Mean: ~1.82, Std: ~0.94, Max: ~8.21

# =============================================================================
# TASK 2 — Flag Anomalies at 95th Percentile
# =============================================================================
# Set threshold = 95th percentile of anomaly_scores.
# Flag samples where anomaly_score > threshold.
# Print: threshold value, number flagged, percentage flagged.

print("\n" + "=" * 60)
print("TASK 2 — Flag top-5% anomalies")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   threshold = np.percentile(anomaly_scores, 95)
#   flagged   = anomaly_scores > threshold
#   print(f"Threshold (95th pct): {threshold:.3f}")
#   print(f"Flagged anomalies:    {flagged.sum()} / {len(anomaly_scores)} ({flagged.mean()*100:.1f}%)")

# EXPECTED OUTPUT:
# Threshold: ~3.87
# Flagged anomalies: ~150 / 3000 (5.0%)

# =============================================================================
# TASK 3 — Verify Against True Labels
# =============================================================================
# Of the flagged anomalies, compute:
#   precision = fraction that are true attacks (true_label != 0)
#   recall    = fraction of ALL attacks that were flagged
# Print both. Comment on the K-Means limitation (attacks form their own clusters).

print("\n" + "=" * 60)
print("TASK 3 — Verification: flagged anomalies vs true attacks")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   is_attack = true_labels != 0
#   true_positives = np.sum(flagged & is_attack)
#   precision = true_positives / flagged.sum()
#   recall    = true_positives / is_attack.sum()
#   print(f"Total attacks in dataset: {is_attack.sum()}")
#   print(f"Flagged anomalies:        {flagged.sum()}")
#   print(f"True attacks in flagged:  {true_positives}")
#   print(f"Precision: {precision:.3f}  (of flagged, fraction are real attacks)")
#   print(f"Recall:    {recall:.3f}  (of all attacks, fraction were flagged)")
#   print(f"\nNote: recall is low because attacks form their own clusters.")
#   print(f"K-Means detects isolated outliers, not attack clusters.")

# EXPECTED OUTPUT:
# Precision: ~0.79 (most flagged items are truly anomalous)
# Recall:    ~0.05 (most attacks form their own dense cluster, are not flagged)

# =============================================================================
# TASK 4 (BONUS) — Anomaly Score Distribution Plot
# =============================================================================
# Plot histogram of anomaly_scores.
# Mark the threshold with a vertical red line.
# Shade the flagged region red, normal region blue.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Anomaly score histogram")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, ax = plt.subplots(figsize=(9, 5))
#   ax.hist(anomaly_scores[~flagged], bins=60, color='steelblue', alpha=0.7, label='Normal')
#   ax.hist(anomaly_scores[flagged],  bins=30, color='red',       alpha=0.7, label='Flagged anomalies')
#   ax.axvline(threshold, color='black', linestyle='--', label=f'Threshold={threshold:.2f}')
#   ax.set_xlabel('Anomaly Score (distance to nearest centroid)')
#   ax.set_ylabel('Count')
#   ax.set_title('Anomaly Score Distribution')
#   ax.legend()
#   plt.show()

print("\n--- Exercise 4 complete. Lesson 2.3 workshop done! ---")
print("--- Next: module2_intermediate/lesson4_overfitting_crossval/ ---")
