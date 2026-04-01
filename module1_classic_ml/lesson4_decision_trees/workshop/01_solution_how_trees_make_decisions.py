import numpy as np
import pandas as pd

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

print("=" * 60)
print("TASK 1 — Gini impurity calculations")
print("=" * 60)
counts_a = np.array([40, 30, 20, 10])
total_a  = counts_a.sum()
probs_a  = counts_a / total_a
gini_a   = 1 - np.sum(probs_a ** 2)
print(f"Mixed node: Gini = {gini_a:.3f}")
#
counts_b = np.array([100, 0, 0, 0])
probs_b  = counts_b / counts_b.sum()
gini_b   = 1 - np.sum(probs_b ** 2)
print(f"Pure node:  Gini = {gini_b:.3f}")

print("\n" + "=" * 60)
print("TASK 2 — Information gain for a split")
print("=" * 60)
def gini(counts):
    counts = np.array(counts)
    p = counts / counts.sum()
    return 1 - np.sum(p**2)
#
g_parent = gini([60, 40])
g_left   = gini([58, 2])
g_right  = gini([2, 38])
w_left, w_right = 60/100, 40/100
weighted_avg = w_left * g_left + w_right * g_right
gain = g_parent - weighted_avg
print(f"Parent Gini:         {g_parent:.3f}")
print(f"Left child Gini:     {g_left:.3f}  (weight={w_left:.2f})")
print(f"Right child Gini:    {g_right:.3f}  (weight={w_right:.2f})")
print(f"Weighted child Gini: {weighted_avg:.3f}")
print(f"Information Gain:    {gain:.3f}")

print("\n" + "=" * 60)
print("TASK 3 — Dataset inspection")
print("=" * 60)
print(f"Shape: {df.shape}")
counts = df['label'].value_counts().sort_index()
for label, count in counts.items():
    print(f"  {CLASS_NAMES[label]:10s}: {count} ({count/len(df)*100:.1f}%)")
print("\nFeature means by class:")
print(df.groupby('label')[FEATURES].mean().round(1).to_string())

connections = [
    {"name": "A", "connection_rate": 80,  "unique_dest_ports": 25, "bytes_sent": 1000},
    {"name": "B", "connection_rate": 20,  "unique_dest_ports": 3,  "bytes_sent": 200},
    {"name": "C", "connection_rate": 60,  "unique_dest_ports": 5,  "bytes_sent": 150000},
]
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Manual rule-based classification")
print("=" * 60)
