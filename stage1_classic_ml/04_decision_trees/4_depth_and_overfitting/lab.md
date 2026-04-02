# Lab -- Exercise 4: Depth and Overfitting

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_depth_and_overfitting.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_per_class = 500
def make_traffic():
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
    return pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(
        frac=1, random_state=42
    )
df = make_traffic()
FEATURES    = ['connection_rate', 'bytes_sent', 'bytes_received',
               'unique_dest_ports', 'duration_seconds', 'failed_connections']
CLASS_NAMES = ['benign', 'port_scan', 'exfil', 'DoS']
X = df[FEATURES]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Step 4: Depth Sweep (Depths 1 to 15)

For each depth from 1 to 15: - Train a new DecisionTreeClassifier with that max_depth - Record training accuracy and test accuracy

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Depth sweep (max_depth 1 to 15)")
print("=" * 60)
depths = range(1, 16)
train_accs, test_accs = [], []
print(f"{'Depth':>5} | {'Train Acc':>9} | {'Test Acc':>8} | {'Gap':>6}")
print("-" * 40)
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42)
    m.fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    te = m.score(X_test,  y_test)
    train_accs.append(tr)
    test_accs.append(te)
    print(f"{d:>5} | {tr:>9.3f} | {te:>8.3f} | {tr-te:>6.3f}")
```

Run your file. You should see:
```
Depth | Train Acc | Test Acc |    Gap
----------------------------------------
1 |     0.652 |    0.648 |  0.004
2 |     0.839 |    0.832 |  0.007
...
15 |     1.000 |    0.943 |  0.057
```

---

## Step 5: Find the Sweet Spot

Identify: 1. The depth with the highest test accuracy 2. The depth with the smallest train/test gap (ignoring depth=1 if accuracy < 0.8)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Find the optimal depth")
print("=" * 60)
best_test_depth = depths[np.argmax(test_accs)]   # need to run Task 1 first
best_test_acc   = max(test_accs)
print(f"Best test accuracy: {best_test_acc:.3f} at depth={best_test_depth}")
print(f"Recommended max_depth: {best_test_depth}")
```

Run your file. You should see:
```
Best test accuracy: ~0.967 at depth=5
Recommended max_depth: 5
```

---

## Step 6: Plot the Depth Sweep

Create a line plot: - x-axis: depth (1 to 15) - y-axis: accuracy (0 to 1)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Train vs test accuracy plot")
print("=" * 60)
print("Depth sweep plot created.")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(list(depths), train_accs, 'b-o', label='Training accuracy', markersize=4)
ax.plot(list(depths), test_accs,  'r--o', label='Test accuracy', markersize=4)
ax.axvline(x=best_test_depth, color='green', linestyle=':', label=f'Sweet spot (depth={best_test_depth})')
ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy')
ax.set_title('Decision Tree: Depth vs Accuracy (Overfitting Diagnostic)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Compare Underfit vs Good Fit vs Overfit

Train three models: depth=1 (underfit), depth=5 (good), depth=15 (overfit). Print classification_report for each on the test set. Comment on how the per-class metrics change.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Underfit vs good fit vs overfit")
print("=" * 60)
for depth, label in [(1, "Underfit"), (5, "Good fit"), (15, "Overfit")]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    print(f"\n--- depth={depth} ({label}) ---")
    print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))
```

Run your file. You should see:
```
--- depth=1 (Underfit) ---
accuracy ~0.65; classes confused
--- depth=5 (Good fit) ---
accuracy ~0.97; all classes well-separated
--- depth=15 (Overfit) ---
accuracy ~0.94; slightly worse than depth=5; DoS and exfil have more confusion
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `solve.py` file if anything looks different.
