# =============================================================================
# LESSON 1.4 | WORKSHOP | Exercise 1 of 4
# How Trees Make Decisions
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How a decision tree builds if/else rules from data
# - What Gini impurity measures
# - How information gain selects the best split
# - What the network traffic dataset looks like
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson4_decision_trees/workshop/exercise1_how_trees_make_decisions.py
# =============================================================================

import numpy as np
import pandas as pd

# =============================================================================
# BACKGROUND
# =============================================================================
# A decision tree classifies by asking yes/no questions:
#   "Is connection_rate > 50? YES → port_scan; NO → benign"
# The tree learns which questions to ask by finding splits that best separate
# the classes. The measure of "separation quality" is Gini impurity:
#
#   Gini = 1 - sum(p_i^2)   where p_i = fraction of class i in the node
#
# A Gini of 0 means the node is pure (all one class) — perfect.
# A Gini near 0.75 means maximum confusion (4 classes equally mixed).
# Information gain = Gini(parent) - weighted_avg(Gini(children))
# The tree always picks the split with the highest information gain.

# --- Dataset generation (do not modify) -------------------------------------
np.random.seed(42)
n_per_class = 500

benign = pd.DataFrame({
    'connection_rate':    np.random.normal(10, 3, n_per_class).clip(1, 25),
    'bytes_sent':         np.random.normal(5000, 1500, n_per_class).clip(100, 15000),
    'bytes_received':     np.random.normal(8000, 2000, n_per_class).clip(100, 20000),
    'unique_dest_ports':  np.random.poisson(3, n_per_class).clip(1, 10),
    'duration_seconds':   np.random.normal(30, 10, n_per_class).clip(1, 120),
    'failed_connections': np.random.poisson(0.5, n_per_class),
    'label': 0
})
port_scan = pd.DataFrame({
    'connection_rate':    np.random.normal(25, 8, n_per_class).clip(5, 60),
    'bytes_sent':         np.random.normal(500, 200, n_per_class).clip(50, 2000),
    'bytes_received':     np.random.normal(300, 100, n_per_class).clip(0, 1000),
    'unique_dest_ports':  np.random.normal(45, 10, n_per_class).clip(20, 100).astype(int),
    'duration_seconds':   np.random.normal(5, 2, n_per_class).clip(1, 20),
    'failed_connections': np.random.poisson(8, n_per_class),
    'label': 1
})
exfil = pd.DataFrame({
    'connection_rate':    np.random.normal(8, 2, n_per_class).clip(1, 20),
    'bytes_sent':         np.random.normal(80000, 25000, n_per_class).clip(20000, 250000),
    'bytes_received':     np.random.normal(1000, 300, n_per_class).clip(100, 5000),
    'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
    'duration_seconds':   np.random.normal(180, 60, n_per_class).clip(60, 600),
    'failed_connections': np.random.poisson(0.2, n_per_class),
    'label': 2
})
dos = pd.DataFrame({
    'connection_rate':    np.random.normal(200, 40, n_per_class).clip(80, 500),
    'bytes_sent':         np.random.normal(200, 80, n_per_class).clip(40, 600),
    'bytes_received':     np.random.normal(100, 40, n_per_class).clip(0, 400),
    'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
    'duration_seconds':   np.random.normal(0.5, 0.2, n_per_class).clip(0.1, 2),
    'failed_connections': np.random.poisson(3, n_per_class),
    'label': 3
})
df = pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(
    frac=1, random_state=42
)
FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
CLASS_NAMES = ['benign', 'port_scan', 'exfil', 'DoS']
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Compute Gini Impurity Manually
# =============================================================================
# Scenario A: A node with 40 benign, 30 port_scan, 20 exfil, 10 DoS samples.
# Scenario B: A pure node with 100% benign.
# For each, compute Gini = 1 - sum(p_i^2).
# Print the result and interpret it.

print("=" * 60)
print("TASK 1 — Gini impurity calculations")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   counts_a = np.array([40, 30, 20, 10])
#   total_a  = counts_a.sum()
#   probs_a  = counts_a / total_a
#   gini_a   = 1 - np.sum(probs_a ** 2)
#   print(f"Mixed node: Gini = {gini_a:.3f}")
#
#   counts_b = np.array([100, 0, 0, 0])
#   probs_b  = counts_b / counts_b.sum()
#   gini_b   = 1 - np.sum(probs_b ** 2)
#   print(f"Pure node:  Gini = {gini_b:.3f}")

# EXPECTED OUTPUT:
# Mixed node (40b, 30ps, 20ex, 10dos): Gini = 0.700
# Pure node  (100b):                   Gini = 0.000

# =============================================================================
# TASK 2 — Compute Information Gain for a Split
# =============================================================================
# Parent: 60 benign, 40 DoS (n=100)
# Split on connection_rate > 50:
#   Left child  (rate <= 50): 58 benign,  2 DoS  (n=60)
#   Right child (rate > 50):   2 benign, 38 DoS  (n=40)
#
# Compute:
#   1. Gini of parent
#   2. Gini of left child, Gini of right child
#   3. Weighted average = (60/100)*Gini_left + (40/100)*Gini_right
#   4. Information gain = Gini_parent - weighted_average

print("\n" + "=" * 60)
print("TASK 2 — Information gain for a split")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   def gini(counts):
#       counts = np.array(counts)
#       p = counts / counts.sum()
#       return 1 - np.sum(p**2)
#
#   g_parent = gini([60, 40])
#   g_left   = gini([58, 2])
#   g_right  = gini([2, 38])
#   w_left, w_right = 60/100, 40/100
#   weighted_avg = w_left * g_left + w_right * g_right
#   gain = g_parent - weighted_avg
#   print(f"Parent Gini:         {g_parent:.3f}")
#   print(f"Left child Gini:     {g_left:.3f}  (weight={w_left:.2f})")
#   print(f"Right child Gini:    {g_right:.3f}  (weight={w_right:.2f})")
#   print(f"Weighted child Gini: {weighted_avg:.3f}")
#   print(f"Information Gain:    {gain:.3f}")

# EXPECTED OUTPUT:
# Parent Gini:         0.480
# Left child Gini:     0.065  (weight=0.60)
# Right child Gini:    0.095  (weight=0.40)
# Weighted child Gini: 0.077
# Information Gain:    0.403

# =============================================================================
# TASK 3 — Inspect the Network Traffic Dataset
# =============================================================================
# Print: shape, class distribution (counts and percentages),
# feature means by class (use df.groupby('label').mean()).

print("\n" + "=" * 60)
print("TASK 3 — Dataset inspection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print(f"Shape: {df.shape}")
#   counts = df['label'].value_counts().sort_index()
#   for label, count in counts.items():
#       print(f"  {CLASS_NAMES[label]:10s}: {count} ({count/len(df)*100:.1f}%)")
#   print("\nFeature means by class:")
#   print(df.groupby('label')[FEATURES].mean().round(1).to_string())

# EXPECTED OUTPUT:
# Shape: (2000, 7)
#   benign    : 500 (25.0%)
#   port_scan : 500 (25.0%)
#   exfil     : 500 (25.0%)
#   DoS       : 500 (25.0%)
# Feature means show very different profiles per class.

# =============================================================================
# TASK 4 (BONUS) — Manual Classification
# =============================================================================
# Using these rules (from a simplified tree):
#   If connection_rate > 100: DoS
#   Else if unique_dest_ports > 20: port_scan
#   Else if bytes_sent > 40000: exfil
#   Else: benign
#
# Classify these three connections manually and print your answers:
connections = [
    {"name": "A", "connection_rate": 80,  "unique_dest_ports": 25, "bytes_sent": 1000},
    {"name": "B", "connection_rate": 20,  "unique_dest_ports": 3,  "bytes_sent": 200},
    {"name": "C", "connection_rate": 60,  "unique_dest_ports": 5,  "bytes_sent": 150000},
]

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Manual rule-based classification")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint: implement the rules as if/elif/else and print the result for each connection.

# EXPECTED OUTPUT:
# Connection A (rate=80, ports=25, bytes=1000): port_scan
# Connection B (rate=20, ports=3,  bytes=200):  benign
# Connection C (rate=60, ports=5,  bytes=150000): exfil

print("\n--- Exercise 1 complete. Move to exercise2_train_and_read_the_tree.py ---")
