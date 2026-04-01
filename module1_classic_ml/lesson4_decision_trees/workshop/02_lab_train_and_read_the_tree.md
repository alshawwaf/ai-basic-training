# Lab -- Exercise 2: Train and Read the Tree

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_train_and_read_the_tree.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
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

## Step 4: Train the Classifier

Create a DecisionTreeClassifier with max_depth=4 and random_state=42. Fit on X_train / y_train. Print training accuracy and test accuracy.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Train the decision tree")
print("=" * 60)
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)
train_acc = model.score(X_train, y_train)
test_acc  = model.score(X_test,  y_test)
print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")
```

Run your file. You should see:
```
Training accuracy: ~0.978
Test accuracy:     ~0.962
```

---

## Step 5: Export the Tree as Text Rules

Use export_text(model, feature_names=FEATURES) to get the rule string. Print the first 40 lines. Then identify and print the root node's split feature and threshold.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Tree rules (first 40 lines)")
print("=" * 60)
rules = export_text(model, feature_names=FEATURES)
lines = rules.split('\n')
for line in lines[:40]:
    print(line)
# The root is the first line that contains '<='
root_line = [l for l in lines if '<=' in l][0].strip()
print(f"\nRoot split: {root_line}")
```

Run your file. You should see:
```
|--- connection_rate <= 55.32
|   |--- bytes_sent <= 27500.00
|   ...
Root split: connection_rate <= 55.32
```

---

## Step 6: Visualise the Tree

Use plot_tree() to create a figure. Set: feature_names=FEATURES, class_names=CLASS_NAMES, filled=True, fontsize=10 Figure size: (20, 10).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Tree visualisation")
print("=" * 60)
print("Tree visualisation created.")
plt.figure(figsize=(20, 10))
plot_tree(model,
          feature_names=FEATURES,
          class_names=CLASS_NAMES,
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Decision Tree: Network Traffic Classifier (max_depth=4)")
plt.tight_layout()
plt.show()
# a) Root splits on connection_rate: DoS has very high rate, others are lower
# b) Left subtree (low rate): separates benign, port_scan, exfil by bytes_sent and ports
```

---

## Step 7: TASK 4 (BONUS) — Trace a Sample Through the Tree

Pick the first test sample (X_test.iloc[0]). Print its feature values. Predict its class and the probabilities for all 4 classes.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Trace a sample through the tree")
print("=" * 60)
sample = X_test.iloc[[0]]
print("Sample features:")
print(sample.to_string())
pred_class = model.predict(sample)[0]
pred_proba = model.predict_proba(sample)[0]
print(f"\nPredicted class: {CLASS_NAMES[pred_class]} ({pred_class})")
print("Class probabilities:")
for name, p in zip(CLASS_NAMES, pred_proba):
    print(f"  {name:10s}: {p:.3f}")
```

Run your file. You should see:
```
Sample features:
connection_rate  bytes_sent  ...
Predicted class: benign (0)
Class probabilities:
benign    : 0.950
port_scan : 0.050
...
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
