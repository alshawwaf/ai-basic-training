# Lab — Exercise 3: Categorical Encoding

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_categorical_encoding.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
```

---

## Step 3: Generate the dataset

Add this data-generation block. Do not modify it.

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
    'dst_port':       np.random.choice([80, 443, 22, 3389, 8080, 53], n),
    'action':         actions
})
y = (raw_df['action'] == 'BLOCK').astype(int)
```

---

## Step 4: Task 1 — LabelEncoder

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — LabelEncoder on protocol")
print("=" * 60)

le = LabelEncoder()
labels_encoded = le.fit_transform(raw_df['protocol'])
print("LabelEncoder mapping:")
for cls, code in zip(le.classes_, range(len(le.classes_))):
    print(f"  {cls} → {code}")
print(f"\nFirst 10 encoded values: {labels_encoded[:10]}")
# Comment: logistic regression will treat code 2 (UDP) as "2x" more than
# code 1 (TCP), which has no semantic meaning for protocols.
```

Run your file. You should see:

```
TASK 1 — LabelEncoder on protocol
============================================================
LabelEncoder mapping:
  ICMP → 0
  TCP  → 1
  UDP  → 2

First 10 encoded values: [1 2 1 ...]
```

---

## Step 5: Task 2 — OneHotEncoder

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — OneHotEncoder (drop first category)")
print("=" * 60)

ohe = OneHotEncoder(drop='first', sparse_output=False)
proto_encoded = ohe.fit_transform(raw_df[['protocol']])
feature_names = ohe.get_feature_names_out(['protocol'])
print(f"Feature names: {list(feature_names)}")
print("(First category dropped is the reference = ICMP)")
encoded_df = pd.DataFrame(proto_encoded, columns=feature_names)
encoded_df['original'] = raw_df['protocol'].values
print("\nFirst 5 rows:")
print(encoded_df.head().to_string(index=False))
```

Run your file. You should see:

```
TASK 2 — OneHotEncoder (drop first category)
============================================================
Feature names: ['protocol_TCP', 'protocol_UDP']
(First category dropped is the reference = ICMP)

First 5 rows:
  protocol_TCP  protocol_UDP  original
       1.0           0.0          TCP
       0.0           1.0          UDP
       ...
```

---

## Step 6: Task 3 — pd.get_dummies comparison

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — pd.get_dummies comparison")
print("=" * 60)

dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)
print("get_dummies result (first 5 rows):")
print(dummies.head().to_string(index=False))

# Check if they match OHE (values should be the same)
ohe_df = pd.DataFrame(proto_encoded.astype(int), columns=['TCP', 'UDP'])
dum_df = dummies.astype(int)
dum_df.columns = ['TCP', 'UDP']
match = ohe_df.equals(dum_df)
print(f"\nget_dummies matches OneHotEncoder: {match}")
```

Run your file. You should see:

```
TASK 3 — pd.get_dummies comparison
============================================================
get_dummies result (first 5 rows):
  proto_TCP  proto_UDP
      1          0
      0          1
      ...
get_dummies matches OneHotEncoder: True
```

---

## Step 7: Task 4 (BONUS) — Compare model accuracy

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — LabelEncoded vs OneHotEncoded model accuracy")
print("=" * 60)

base_features = raw_df[['bytes_sent', 'packets', 'duration']].copy()

# Label encoded version
X_label = base_features.copy()
X_label['protocol'] = labels_encoded

# OHE version
X_ohe = pd.concat([base_features, dummies.astype(int)], axis=1)

for name, X in [("LabelEncoded", X_label), ("OneHotEncoded", X_ohe)]:
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    acc = m.score(X_te, y_te)
    print(f"{name:18s} accuracy: {acc:.3f}")

print("\n--- Exercise 3 complete. Move to 04_scaling_and_validation.py ---")
```

Run your file. You should see:

```
TASK 4 (BONUS) — LabelEncoded vs OneHotEncoded model accuracy
============================================================
LabelEncoded       accuracy: ~0.847
OneHotEncoded      accuracy: ~0.863
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
