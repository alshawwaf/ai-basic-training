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
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
# Three types of normal traffic + anomalies (data exfiltration).
# The true labels exist for evaluation but are NOT used in clustering.
n_normal  = 2000
n_anomaly = 60   # small fraction hidden in the data

# Normal traffic forms three distinct behavioural groups
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

# Anomalies: data exfiltration — very large uploads on unusual ports
anomalies = pd.DataFrame({
    'bytes_sent':   np.random.lognormal(13, 0.5, n_anomaly),
    'bytes_recv':   np.random.lognormal(5, 0.5, n_anomaly),
    'duration_s':   np.random.normal(1800, 600, n_anomaly).clip(600, 7200),
    'packets':      np.random.poisson(1500, n_anomaly).clip(500, 5000),
    'dest_port':    np.random.randint(10000, 60000, n_anomaly),
})

normal_df = pd.concat([web_browsing, ssh_sessions, dns_queries], ignore_index=True)
normal_df['true_label'] = 0   # for evaluation only

anomalies['true_label'] = 1

all_data = pd.concat([normal_df, anomalies], ignore_index=True).sample(
    frac=1, random_state=42
).reset_index(drop=True)

feature_cols = ['bytes_sent', 'bytes_recv', 'duration_s', 'packets', 'dest_port']
X_raw  = all_data[feature_cols].values
y_true = all_data['true_label'].values   # hidden — only for final evaluation

# ============================================================
# TASK 1 — Load the dataset (no labels)
# ============================================================
# In real security monitoring, you rarely have labels. You just have
# raw connection data and need to find patterns yourself.
print("=" * 60)
print("TASK 1 — Dataset (no labels used)")
print("=" * 60)

print(f"Shape: {X_raw.shape}")
print(f"Features: {feature_cols}")
print(f"\nTotal connections: {len(all_data)}")
print(f"(Hidden anomalies: {y_true.sum()} — but we pretend we don't know this)")
print(f"\nDescriptive statistics (what an analyst would see):")
print(all_data[feature_cols].describe().round(1).to_string())

# ============================================================
# TASK 2 — Show that "no labels" is realistic
# ============================================================
# Print feature distributions. Can you spot anomalies by looking at
# summary statistics alone? (Spoiler: not easily.)
print("\n" + "=" * 60)
print("TASK 2 — Feature distributions (can you spot anomalies?)")
print("=" * 60)

print("Distribution of bytes_sent:")
print(f"  25th percentile: {np.percentile(X_raw[:, 0], 25):.0f}")
print(f"  50th percentile: {np.percentile(X_raw[:, 0], 50):.0f}")
print(f"  75th percentile: {np.percentile(X_raw[:, 0], 75):.0f}")
print(f"  95th percentile: {np.percentile(X_raw[:, 0], 95):.0f}")
print(f"  max:             {X_raw[:, 0].max():.0f}")
print("\nThe max is much larger than the 95th percentile — possible outliers,")
print("but from raw stats alone you can't tell if they're attacks or just")
print("large legitimate transfers.")

print("\nDistribution of dest_port:")
port_counts = pd.Series(X_raw[:, 4]).value_counts().head(5)
print(port_counts.to_string())
print("\nMost traffic goes to well-known ports (443, 80, 22, 53).")
print("The unusual high-numbered ports are spread across many values.")

# ============================================================
# TASK 3 — Hypothesis: normal flows form clusters
# ============================================================
# Diagnostic scatter plot: reveal true labels to confirm that normal
# and anomalous traffic occupy different regions of feature space.
# (In practice you'd only do this if you had labelled data for evaluation.)
print("\n" + "=" * 60)
print("TASK 3 — Diagnostic scatter plot (revealing true labels)")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 6))

normal_mask  = y_true == 0
anomaly_mask = y_true == 1

ax.scatter(all_data.loc[normal_mask, 'bytes_sent'],
           all_data.loc[normal_mask, 'duration_s'],
           alpha=0.3, s=10, color='steelblue', label='Normal')
ax.scatter(all_data.loc[anomaly_mask, 'bytes_sent'],
           all_data.loc[anomaly_mask, 'duration_s'],
           alpha=0.8, s=40, color='crimson', marker='x', label='Anomaly (true)')
ax.set_xlabel('bytes_sent')
ax.set_ylabel('duration_s')
ax.set_title('Diagnostic: Normal vs Anomaly (true labels revealed)')
ax.legend()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson3_unsupervised_framing.png')
plt.close()
print("Diagnostic plot saved.")
print("Anomalies (red X) appear far from the dense normal clusters.")
print("Normal traffic forms 3 visible groups: web, SSH, DNS.")

# ============================================================
# TASK 4 (BONUS) — Describe expected cluster patterns
# ============================================================
# What would different attack types look like as cluster outliers?
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Expected cluster patterns by attack type")
print("=" * 60)

# DoS attacks: extremely high packet rate, very short duration, low bytes per packet
print("1. DoS attack pattern:")
print("   - Very high packets (thousands), very short duration (< 1s)")
print("   - Would appear far from all normal clusters because no normal")
print("     traffic has that packet-to-duration ratio")

# Port scans: many unique destination ports, tiny packets, rapid connections
print("\n2. Port scan pattern:")
print("   - Low bytes_sent, low duration, many unique dest_ports")
print("   - Would NOT cluster with web (port 443) or SSH (port 22)")
print("   - Appears as scattered points across many port values")

# Data exfiltration: very large bytes_sent, long duration, unusual ports
print("\n3. Data exfiltration pattern (what our dataset simulates):")
print("   - Very high bytes_sent (orders of magnitude above normal)")
print("   - Long duration (sustained transfer)")
print("   - Unusual dest_port (not 80/443/22/53)")
print("   - Appears far from all three normal clusters")

print("\n--- Exercise 1 complete. Move to ../2_kmeans_and_visualisation/solution.py ---")
