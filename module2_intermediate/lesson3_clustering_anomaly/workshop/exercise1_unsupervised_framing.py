# =============================================================================
# LESSON 2.3 | WORKSHOP | Exercise 1 of 4
# Unsupervised Framing
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why labels are unavailable in many real security scenarios
# - What clustering discovers without labels
# - Why normal traffic forms dense clusters while attacks are outliers
# - How to set up an unsupervised anomaly detection problem
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson3_clustering_anomaly/workshop/exercise1_unsupervised_framing.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# BACKGROUND
# =============================================================================
# Supervised ML requires labelled data. In practice, security analysts cannot
# label every network connection. K-Means clustering finds natural groupings
# in feature space — no labels needed. Normal behaviour is repetitive and
# forms dense, stable clusters. Attacks are unusual and appear as outliers far
# from any cluster centre. We will "hide" the true labels and only reveal them
# for diagnostic purposes after clustering.

# --- Dataset (labels hidden during unsupervised analysis) -------------------
np.random.seed(42)
n_per = 750   # 750 per class × 4 classes = 3000 total

def make_full_dataset():
    benign = pd.DataFrame({
        'connection_rate':    np.random.normal(10, 3, n_per).clip(1, 25),
        'bytes_sent':         np.random.normal(5000, 1500, n_per).clip(100, 15000),
        'bytes_received':     np.random.normal(8000, 2000, n_per).clip(100, 20000),
        'unique_dest_ports':  np.random.poisson(3, n_per).clip(1, 10),
        'duration_seconds':   np.random.normal(30, 10, n_per).clip(1, 120),
        'failed_connections': np.random.poisson(0.5, n_per),
        'true_label': 0, 'true_class': 'benign'
    })
    port_scan = pd.DataFrame({
        'connection_rate':    np.random.normal(25, 8, n_per).clip(5, 60),
        'bytes_sent':         np.random.normal(500, 200, n_per).clip(50, 2000),
        'bytes_received':     np.random.normal(300, 100, n_per).clip(0, 1000),
        'unique_dest_ports':  np.random.normal(45, 10, n_per).clip(20, 100).astype(int),
        'duration_seconds':   np.random.normal(5, 2, n_per).clip(1, 20),
        'failed_connections': np.random.poisson(8, n_per),
        'true_label': 1, 'true_class': 'port_scan'
    })
    exfil = pd.DataFrame({
        'connection_rate':    np.random.normal(8, 2, n_per).clip(1, 20),
        'bytes_sent':         np.random.normal(80000, 25000, n_per).clip(20000, 250000),
        'bytes_received':     np.random.normal(1000, 300, n_per).clip(100, 5000),
        'unique_dest_ports':  np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds':   np.random.normal(180, 60, n_per).clip(60, 600),
        'failed_connections': np.random.poisson(0.2, n_per),
        'true_label': 2, 'true_class': 'exfil'
    })
    dos = pd.DataFrame({
        'connection_rate':    np.random.normal(200, 40, n_per).clip(80, 500),
        'bytes_sent':         np.random.normal(200, 80, n_per).clip(40, 600),
        'bytes_received':     np.random.normal(100, 40, n_per).clip(0, 400),
        'unique_dest_ports':  np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds':   np.random.normal(0.5, 0.2, n_per).clip(0.1, 2),
        'failed_connections': np.random.poisson(3, n_per),
        'true_label': 3, 'true_class': 'DoS'
    })
    return pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(frac=1, random_state=42)

df_full = make_full_dataset()
FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']

# UNSUPERVISED: X has NO label columns
X = df_full[FEATURES]
# True labels kept separately for diagnostic use ONLY
true_labels  = df_full['true_label'].values
true_classes = df_full['true_class'].values
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Inspect the Unlabelled Dataset
# =============================================================================
# Print X.shape, X.dtypes, X.describe().
# Confirm: no label column in X.

print("=" * 60)
print("TASK 1 — Unlabelled dataset inspection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print(f"Shape: {X.shape}")
#   print(f"Columns: {list(X.columns)}")
#   print(f"\nNote: NO label column — this is unsupervised!")
#   print(f"\nDescriptive stats:")
#   print(X.describe().round(1).to_string())

# EXPECTED OUTPUT:
# Shape: (3000, 6)
# Columns: ['connection_rate', 'bytes_sent', ...]
# Note: NO label column — this is unsupervised!

# =============================================================================
# TASK 2 — Look at Feature Distributions
# =============================================================================
# Plot histograms of all 6 features (2 rows × 3 cols figure).
# From looking at these, can you identify separate attack groups by eye?
# Write a comment with your observation.

print("\n" + "=" * 60)
print("TASK 2 — Feature distributions (can you spot attacks?)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, axes = plt.subplots(2, 3, figsize=(12, 7))
#   for ax, col in zip(axes.flat, FEATURES):
#       X[col].hist(ax=ax, bins=40, color='steelblue', alpha=0.7)
#       ax.set_title(col)
#   plt.suptitle('Feature Distributions (all traffic, no labels)')
#   plt.tight_layout()
#   plt.show()
#   print("Observation: some features show multimodal distributions (e.g., bytes_sent)")
#   print("suggesting multiple natural groups exist — even without labels.")

print("Distribution plots created.")

# =============================================================================
# TASK 3 — Diagnostic Scatter (Reveal Labels)
# =============================================================================
# Plot connection_rate (x) vs bytes_sent (y).
# Colour each point by true_classes (benign/port_scan/exfil/DoS).
# Add a legend. Use alpha=0.3 for overlapping point clarity.
# Observe: do the 4 classes form visually distinct regions?

print("\n" + "=" * 60)
print("TASK 3 — Diagnostic scatter (labels revealed for visualisation only)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   colours = {'benign':'steelblue', 'port_scan':'orange', 'exfil':'green', 'DoS':'red'}
#   plt.figure(figsize=(9, 6))
#   for cls in ['benign', 'port_scan', 'exfil', 'DoS']:
#       mask = true_classes == cls
#       plt.scatter(X.loc[mask, 'connection_rate'],
#                   X.loc[mask, 'bytes_sent'],
#                   alpha=0.2, s=10, label=cls, color=colours[cls])
#   plt.xlabel('connection_rate')
#   plt.ylabel('bytes_sent')
#   plt.title('Diagnostic: True Class Labels Revealed')
#   plt.legend()
#   plt.yscale('log')
#   plt.show()

print("Diagnostic scatter created.")

# =============================================================================
# TASK 4 (BONUS) — Describe Expected Cluster Patterns
# =============================================================================
# Based on the scatter from Task 3, write comments describing:
#   a) Where you expect the DoS cluster (high rate, low bytes)
#   b) Where you expect the exfil cluster (low rate, very high bytes)
#   c) Where you expect port_scan (moderate rate, very low bytes)
#   d) Where benign sits relative to the others

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Expected cluster descriptions")
print("=" * 60)

# >>> YOUR CODE HERE
# a) DoS cluster: top-left (high connection_rate ~200, low bytes_sent ~200)
# b) Exfil cluster: bottom-right (low rate ~8, very high bytes_sent ~80000)
# c) Port scan: middle-left (moderate rate ~25, very low bytes ~500)
# d) Benign: centre (moderate rate ~10, moderate bytes ~5000)

expected = {
    'DoS cluster':        'high connection_rate (>100), low bytes_sent (<600)',
    'Exfil cluster':      'low connection_rate (<20), very high bytes_sent (>20000)',
    'Port scan cluster':  'moderate rate (5-60), very low bytes (<2000), many ports',
    'Benign cluster':     'low rate (<25), moderate bytes (100-15000), few ports',
}
for name, desc in expected.items():
    print(f"  {name:22s}: {desc}")

print("\n--- Exercise 1 complete. Move to exercise2_kmeans_and_visualisation.py ---")
