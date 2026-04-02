# Lab -- Exercise 1: How Trees Make Decisions

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_how_trees_make_decisions.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
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
```

---

## Step 4: Compute Gini Impurity Manually

Scenario A: A node with 40 benign, 30 port_scan, 20 exfil, 10 DoS samples. Scenario B: A pure node with 100% benign. For each, compute Gini = 1 - sum(p_i^2).

Add this to your file:

```python
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
```

Run your file. You should see:
```
Mixed node (40b, 30ps, 20ex, 10dos): Gini = 0.700
Pure node  (100b):                   Gini = 0.000
```

---

## Step 5: Compute Information Gain for a Split

Parent: 60 benign, 40 DoS (n=100) Split on connection_rate > 50: Left child  (rate <= 50): 58 benign,  2 DoS  (n=60)

Add this to your file:

```python
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
```

Run your file. You should see:
```
Parent Gini:         0.480
Left child Gini:     0.065  (weight=0.60)
Right child Gini:    0.095  (weight=0.40)
Weighted child Gini: 0.077
Information Gain:    0.403
```

---

## Step 6: Inspect the Network Traffic Dataset

Print: shape, class distribution (counts and percentages), feature means by class (use df.groupby('label').mean()).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Dataset inspection")
print("=" * 60)
print(f"Shape: {df.shape}")
counts = df['label'].value_counts().sort_index()
for label, count in counts.items():
    print(f"  {CLASS_NAMES[label]:10s}: {count} ({count/len(df)*100:.1f}%)")
print("\nFeature means by class:")
print(df.groupby('label')[FEATURES].mean().round(1).to_string())
```

Run your file. You should see:
```
Shape: (2000, 7)
benign    : 500 (25.0%)
port_scan : 500 (25.0%)
exfil     : 500 (25.0%)
DoS       : 500 (25.0%)
Feature means show very different profiles per class.
```

---

## Step 7: TASK 4 (BONUS) — Manual Classification

Using these rules (from a simplified tree): If connection_rate > 100: DoS Else if unique_dest_ports > 20: port_scan

Add this to your file:

```python
connections = [
    {"name": "A", "connection_rate": 80,  "unique_dest_ports": 25, "bytes_sent": 1000},
    {"name": "B", "connection_rate": 20,  "unique_dest_ports": 3,  "bytes_sent": 200},
    {"name": "C", "connection_rate": 60,  "unique_dest_ports": 5,  "bytes_sent": 150000},
]
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Manual rule-based classification")
print("=" * 60)
```

Run your file. You should see:
```
Connection A (rate=80, ports=25, bytes=1000): port_scan
Connection B (rate=20, ports=3,  bytes=200):  benign
Connection C (rate=60, ports=5,  bytes=150000): exfil
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `01_solution_how_trees_make_decisions.py` file if anything looks different.
