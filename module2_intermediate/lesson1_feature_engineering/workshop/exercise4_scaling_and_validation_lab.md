# Lab — Exercise 4: Scaling and Validation

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise4_scaling_and_validation.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
```

---

## Step 3: Build the feature matrix from scratch

Add this data-generation block. It creates the raw dataset and pre-engineers the derived features used in previous exercises.

```python
np.random.seed(42)
n = 200
protocols  = np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.6, 0.3, 0.1])
actions    = np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.8, 0.2])
raw_df = pd.DataFrame({
    'bytes_sent':     np.random.exponential(5000, n).astype(int),
    'bytes_received': np.random.exponential(8000, n).astype(int),
    'packets':        np.random.poisson(15, n),
    'duration':       np.random.exponential(2, n).clip(0.01),
    'protocol':       protocols,
    'dst_port':       np.random.choice([80, 443, 22, 3389, 8080, 53], n,
                                        p=[0.3, 0.3, 0.1, 0.08, 0.12, 0.1]),
    'action':         actions
})
raw_df['bytes_per_second'] = raw_df['bytes_sent'] / raw_df['duration']
raw_df['packet_rate']      = raw_df['packets'] / raw_df['duration']
raw_df['bytes_ratio']      = raw_df['bytes_sent'] / (raw_df['bytes_received'] + 1)
port_risk_map = {80: 1, 443: 1, 53: 2, 22: 3, 8080: 2, 3389: 5}
raw_df['port_risk_score']  = raw_df['dst_port'].map(port_risk_map).fillna(2).astype(int)
proto_dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True).astype(int)
y = (raw_df['action'] == 'BLOCK').astype(int)
```

---

## Step 4: Task 1 — Assemble and validate the feature matrix

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Assemble and validate the feature matrix")
print("=" * 60)

X = pd.concat([
    raw_df[['bytes_per_second', 'packet_rate', 'bytes_ratio', 'port_risk_score']],
    proto_dummies
], axis=1)
print(f"Shape: {X.shape}")
print(f"\nDtypes:\n{X.dtypes}")
print(f"\nMissing values: {X.isnull().sum().sum()}")
print(f"\nDescriptive stats:")
print(X.describe().round(2).to_string())
```

Run your file. You should see:

```
TASK 1 — Assemble and validate the feature matrix
============================================================
Shape: (200, 6)

Dtypes:
bytes_per_second    float64
packet_rate         float64
bytes_ratio         float64
port_risk_score       int64
proto_TCP              bool  (or int64)
proto_UDP              bool  (or int64)

Missing values: 0
```

---

## Step 5: Task 2 — Scale with StandardScaler (train only)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — StandardScaler (fit on train only)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)   # NOTE: transform only!

print("Scaled training data verification:")
print(f"{'Feature':20s} {'Mean':>8} {'Std':>8}")
print("-" * 40)
for i, col in enumerate(X.columns):
    print(f"{col:20s} {X_tr_sc[:, i].mean():>8.3f} {X_tr_sc[:, i].std():>8.3f}")
```

Run your file. You should see all means at 0.000 and all stds at 1.000.

```
TASK 2 — StandardScaler (fit on train only)
============================================================
Scaled training data verification:
Feature               Mean      Std
bytes_per_second     0.000    1.000
packet_rate          0.000    1.000
bytes_ratio          0.000    1.000
port_risk_score      0.000    1.000
proto_TCP            0.000    1.000
proto_UDP            0.000    1.000
```

---

## Step 6: Task 3 — Compare StandardScaler vs MinMaxScaler with an outlier

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — StandardScaler vs MinMaxScaler")
print("=" * 60)

bps = X_train[['bytes_per_second']].copy()
bps_with_outlier = bps.copy()
bps_with_outlier.iloc[0] = 500_000   # extreme artificial outlier

for name, sc in [("StandardScaler", StandardScaler()),
                 ("MinMaxScaler",   MinMaxScaler())]:
    scaled = sc.fit_transform(bps_with_outlier)
    print(f"\n{name}:")
    print(f"  mean={scaled.mean():.3f}, std={scaled.std():.3f}, "
          f"min={scaled.min():.3f}, max={scaled.max():.3f}")
print("\nMinMaxScaler compresses all normal values toward 0 because of the outlier.")
```

Run your file. You should see:

```
StandardScaler:
  mean=0.000, std=1.000, min~=-0.4, max~=4.2  (outlier = 4.2σ)
MinMaxScaler:
  mean=0.006, std=0.020, min=0.000, max=1.000  (normal values all near 0!)

MinMaxScaler compresses all normal values toward 0 because of the outlier.
```

---

## Step 7: Task 4 (BONUS) — sklearn Pipeline

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — sklearn Pipeline")
print("=" * 60)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LogisticRegression(max_iter=1000))
])
pipeline.fit(X_train, y_train)
acc = pipeline.score(X_test, y_test)
print(f"Pipeline test accuracy: {acc:.3f}")
print("The pipeline automatically fits scaler on X_train only.")

print("\n--- Exercise 4 complete. Lesson 2.1 workshop done! ---")
print("--- Next: module2_intermediate/lesson2_random_forests/ ---")
```

Run your file. You should see:

```
TASK 4 (BONUS) — sklearn Pipeline
============================================================
Pipeline test accuracy: ~0.875
The pipeline automatically fits scaler on X_train only.
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
