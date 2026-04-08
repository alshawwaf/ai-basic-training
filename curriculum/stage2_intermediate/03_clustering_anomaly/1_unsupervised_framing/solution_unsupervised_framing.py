# Exercise 1 — Unsupervised Framing
#
# Goal: Understand why labels are often unavailable in security monitoring,
#       explore the dataset WITHOUT labels, and see why normal traffic
#       naturally clusters while attacks appear as outliers.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
# Four traffic types: benign, port_scan, exfil, DoS — 750 samples each.
# The true labels exist for evaluation but are NOT used in clustering.
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
X       = df_full[FEATURES]
y_true  = df_full['true_label'].values    # hidden — for final evaluation only
classes = df_full['true_class'].values    # hidden — for final evaluation only

# ============================================================
# TASK 1 — Load the dataset (no labels)
# ============================================================
# In real security monitoring, you rarely have labels. You just have
# raw connection data and need to find patterns yourself.
print("=" * 60)
print("TASK 1 — Dataset (no labels used)")
print("=" * 60)

print(f"Shape: {X.shape}")
print(f"Features: {FEATURES}")
print(f"\nTotal connections: {len(df_full)}")
print(f"(Hidden attacks: {(y_true != 0).sum()} — but we pretend we don't know this)")
print(f"\nDescriptive statistics (what an analyst would see):")
print(X.describe().round(1).to_string())

# ============================================================
# TASK 2 — Show that "no labels" is realistic
# ============================================================
# Print feature distributions. Can you spot anomalies by looking at
# summary statistics alone? (Spoiler: not easily.)
print("\n" + "=" * 60)
print("TASK 2 — Feature distributions (can you spot anomalies?)")
print("=" * 60)

print("Distribution of bytes_sent:")
print(f"  25th percentile: {np.percentile(X['bytes_sent'], 25):.0f}")
print(f"  50th percentile: {np.percentile(X['bytes_sent'], 50):.0f}")
print(f"  75th percentile: {np.percentile(X['bytes_sent'], 75):.0f}")
print(f"  95th percentile: {np.percentile(X['bytes_sent'], 95):.0f}")
print(f"  max:             {X['bytes_sent'].max():.0f}")
print("\nThe right tail is much larger than the 75th percentile — possible")
print("outliers, but from raw stats alone you can't tell if they're attacks")
print("or just large legitimate transfers.")

print("\nDistribution of connection_rate:")
print(f"  25th percentile: {np.percentile(X['connection_rate'], 25):.1f}")
print(f"  50th percentile: {np.percentile(X['connection_rate'], 50):.1f}")
print(f"  75th percentile: {np.percentile(X['connection_rate'], 75):.1f}")
print(f"  95th percentile: {np.percentile(X['connection_rate'], 95):.1f}")
print(f"  max:             {X['connection_rate'].max():.1f}")
print("\nMost connections are slow, but a long tail of very fast connections")
print("hints at automated traffic — could be a scan, could be a benign cron job.")

# ============================================================
# TASK 3 — Hypothesis: normal flows form clusters
# ============================================================
# Diagnostic scatter plot: reveal true labels to confirm that traffic types
# occupy different regions of feature space.
# (In practice you'd only do this if you had labelled data for evaluation.)
print("\n" + "=" * 60)
print("TASK 3 — Diagnostic scatter plot (revealing true labels)")
print("=" * 60)

class_colours = {'benign': 'steelblue', 'port_scan': 'orange',
                 'exfil': 'green', 'DoS': 'red'}

fig, ax = plt.subplots(figsize=(8, 6))
for cls in ['benign', 'port_scan', 'exfil', 'DoS']:
    mask = classes == cls
    ax.scatter(X.loc[mask, 'bytes_sent'],
               X.loc[mask, 'connection_rate'],
               alpha=0.4, s=12, color=class_colours[cls], label=cls)
ax.set_xlabel('bytes_sent')
ax.set_ylabel('connection_rate')
ax.set_xscale('log')
ax.set_title('Diagnostic: Traffic types by bytes vs connection rate')
ax.legend()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_unsupervised_framing.png')
plt.close()
print("Diagnostic plot saved.")
print("Each traffic type occupies a different region of feature space —")
print("that natural separation is exactly what K-Means will exploit.")

# ============================================================
# TASK 4 (BONUS) — Describe expected cluster patterns
# ============================================================
# What does each traffic type look like in feature space?
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Expected cluster patterns by traffic type")
print("=" * 60)

print("1. Benign:")
print("   - Moderate connection_rate, moderate bytes, few failed connections")
print("   - The largest, densest cluster")

print("\n2. Port scan:")
print("   - Moderate connection_rate, very low bytes, MANY unique dest_ports")
print("   - High failed_connections (closed ports)")

print("\n3. Data exfiltration:")
print("   - Low connection_rate, VERY high bytes_sent, sustained duration")
print("   - Stands out on bytes_sent alone")

print("\n4. DoS:")
print("   - Very high connection_rate, low bytes per connection, sub-second")
print("   - Stands out on connection_rate alone")

print("\n--- Exercise 1 complete. Move to ../2_kmeans_and_visualisation/solution.py ---")
