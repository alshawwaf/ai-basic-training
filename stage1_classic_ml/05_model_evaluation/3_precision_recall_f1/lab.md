# Lab -- Exercise 3: Precision, Recall, and F1

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_precision_recall_f1.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (precision_score, recall_score, f1_score,
                             classification_report, fbeta_score)
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_benign, n_attack = 9_500, 500
benign_data = np.column_stack([
    np.random.normal(10, 3, n_benign),
    np.random.normal(5000, 1500, n_benign),
    np.random.poisson(3, n_benign)
])
attack_data = np.column_stack([
    np.random.normal(80, 30, n_attack),
    np.random.normal(500, 300, n_attack),
    np.random.poisson(30, n_attack)
])
X = np.vstack([benign_data, attack_data])
y = np.array([0]*n_benign + [1]*n_attack)
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)
```

---

## Step 4: Compare All Three Models on Attack-Class Metrics

Train DummyClassifier, LogisticRegression, and DecisionTreeClassifier(max_depth=5). For each, compute precision, recall, and F1 for the ATTACK class (pos_label=1). Print a comparison table.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Model comparison: attack-class metrics")
print("=" * 60)
dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
lr    = LogisticRegression(max_iter=1000, random_state=42).fit(X_tr_sc, y_train)
dt    = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train)
#
models_and_preds = [
    ("DummyClassifier",     dummy.predict(X_test)),
    ("LogisticRegression",  lr.predict(X_te_sc)),
    ("DecisionTree",        dt.predict(X_test)),
]
print(f"{'Model':25s} {'Precision':>9} {'Recall':>7} {'F1':>7}")
print("-" * 55)
for name, y_pred in models_and_preds:
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred)
    print(f"{name:25s} {p:>9.3f} {r:>7.3f} {f:>7.3f}")
```

Run your file. You should see:
```
Model                   Precision  Recall     F1
DummyClassifier             0.000   0.000  0.000
LogisticRegression          ~0.857  ~0.720 ~0.783
DecisionTree                ~0.812  ~0.780 ~0.796
```

---

## Step 5: Full Classification Report for LogisticRegression

Print the full classification_report for LogisticRegression. Then answer in print statements: a) Which metric would you focus on to catch every attack?

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Full classification report")
print("=" * 60)
y_pred_lr = lr.predict(X_te_sc)
print(classification_report(y_test, y_pred_lr, target_names=['benign', 'attack']))
print("To catch every attack: optimise RECALL for attack class")
print("To minimise false alarms: optimise PRECISION for attack class")
```

Run your file. You should see:
```
precision  recall  f1-score  support
benign          ~0.994   ~0.994    ~0.994     1900
attack          ~0.857   ~0.720    ~0.783      100
accuracy                           ~0.980     2000
```

---

## Step 6: Precision-Recall vs Threshold

For LogisticRegression, compute precision and recall at thresholds: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] Plot both as lines with threshold on the x-axis.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Precision and recall across thresholds")
print("=" * 60)
print("Precision-recall vs threshold plot created.")
probs = lr.predict_proba(X_te_sc)[:, 1]
thresholds = np.arange(0.1, 1.0, 0.1)
precisions, recalls = [], []
for t in thresholds:
    y_pred_t = (probs >= t).astype(int)
    precisions.append(precision_score(y_test, y_pred_t, zero_division=0))
    recalls.append(recall_score(y_test, y_pred_t))
plt.figure(figsize=(9, 5))
plt.plot(thresholds, precisions, 'b-o', label='Precision')
plt.plot(thresholds, recalls,    'r-s', label='Recall')
plt.axvline(0.5, color='grey', linestyle='--', alpha=0.7, label='Default threshold')
plt.xlabel('Decision Threshold')
plt.ylabel('Score')
plt.title('Precision and Recall vs Threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## Step 7: TASK 4 (BONUS) — F2 Score

Compute the F2 score (beta=2) for each model. F2 weights recall twice as much as precision. Print F1 and F2 side by side for all three models.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — F1 vs F2 score")
print("=" * 60)
print(f"{'Model':25s} {'F1':>7} {'F2':>7}")
print("-" * 42)
for name, y_pred in models_and_preds:
    f1 = f1_score(y_test, y_pred, zero_division=0)
    f2 = fbeta_score(y_test, y_pred, beta=2, zero_division=0)
    print(f"{name:25s} {f1:>7.3f} {f2:>7.3f}")
# F2 is better for security tools where missing an attack
# (low recall) is more costly than investigating a false alarm (low precision).
```

Run your file. You should see:
```
Model                       F1      F2
DummyClassifier           0.000   0.000
LogisticRegression        ~0.783  ~0.745 (F2 lower because recall isn't great)
DecisionTree              ~0.796  ~0.789
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file `solve.py` if anything looks different.
