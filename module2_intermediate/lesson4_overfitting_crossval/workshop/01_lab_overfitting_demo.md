# Lab -- Exercise 1: Overfitting Demo

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_overfitting_demo.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_per = 1000
benign = pd.DataFrame({'connection_rate': np.random.normal(10,3,n_per).clip(1,25),
    'bytes_sent': np.random.normal(5000,1500,n_per).clip(100,15000),
    'bytes_received': np.random.normal(8000,2000,n_per).clip(100,20000),
    'unique_dest_ports': np.random.poisson(3,n_per).clip(1,10),
    'duration_seconds': np.random.normal(30,10,n_per).clip(1,120),
    'failed_connections': np.random.poisson(0.5,n_per), 'label':0})
attack = pd.DataFrame({'connection_rate': np.random.normal(80,25,n_per).clip(10,250),
    'bytes_sent': np.random.normal(30000,15000,n_per).clip(100,200000),
    'bytes_received': np.random.normal(2000,1000,n_per).clip(0,20000),
    'unique_dest_ports': np.random.normal(20,10,n_per).clip(1,60).astype(int),
    'duration_seconds': np.random.normal(10,5,n_per).clip(0.1,60),
    'failed_connections': np.random.poisson(3,n_per), 'label':1})
df = pd.concat([benign, attack], ignore_index=True).sample(frac=1, random_state=42)
FEATURES = ['connection_rate','bytes_sent','bytes_received',
            'unique_dest_ports','duration_seconds','failed_connections']
X = df[FEATURES]
y = df['label']
```

---

## Step 4: Three-Way Split (60/20/20)

Split into train (60%), validation (20%), test (20%). Print sizes of each split.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Three-way split")
print("=" * 60)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
# 0.25 of 80% = 20% of total
print(f"Train size:      {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Validation size: {len(X_val)}  ({len(X_val)/len(X)*100:.0f}%)")
print(f"Test size:       {len(X_test)}  ({len(X_test)/len(X)*100:.0f}%)")
```

Run your file. You should see:
```
Train size:      2400 (60%)
Validation size:  800 (20%)
Test size:        800 (20%)
```

---

## Step 5: Depth Sweep (1 to 20)

Sweep max_depth 1-20. For each, record train accuracy and VALIDATION accuracy. Print a table.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Depth sweep")
print("=" * 60)
depths = range(1, 21)
train_accs, val_accs = [], []
print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>6}")
print("-" * 35)
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42)
    m.fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    va = m.score(X_val,   y_val)
    train_accs.append(tr)
    val_accs.append(va)
    print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr-va:>6.3f}")
```

---

## Step 6: Plot and Identify the Overfitting Point

Plot train and val accuracy curves. Mark the sweet-spot depth.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Overfitting plot")
print("=" * 60)
best_depth = list(depths)[np.argmax(val_accs)]
print(f"Best validation accuracy at depth={best_depth}: {max(val_accs):.3f}")
#
plt.figure(figsize=(10, 6))
plt.plot(list(depths), train_accs, 'b-o', label='Training', markersize=4)
plt.plot(list(depths), val_accs,   'r--s', label='Validation', markersize=4)
plt.axvline(best_depth, color='green', linestyle=':', label=f'Sweet spot (depth={best_depth})')
plt.xlabel('max_depth'), plt.ylabel('Accuracy')
plt.title('Overfitting Demo: Train vs Validation Accuracy')
plt.legend(), plt.grid(True, alpha=0.3), plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Report Gap at Key Depths

Print: train acc, val acc, gap at depths 1, 5, 10, 20.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Gap at key depths")
print("=" * 60)
print("\n--- Exercise 1 complete. Move to exercise2_bias_variance.py ---")
key_depths = [1, 5, 10, 20]
print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>8}")
print("-" * 36)
for d in key_depths:
    tr = train_accs[d-1]
    va = val_accs[d-1]
    print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr-va:>8.3f}")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`01_solution_overfitting_demo.py`) if anything looks different.
