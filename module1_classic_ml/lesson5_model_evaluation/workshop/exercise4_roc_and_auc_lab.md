# Lab -- Exercise 4: ROC Curve and AUC

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise4_roc_and_auc.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (roc_curve, roc_auc_score,
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
dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
lr    = LogisticRegression(max_iter=1000, random_state=42).fit(X_tr_sc, y_train)
dt    = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train)
```

---

## Step 4: ROC Curve and AUC for LogisticRegression

Get probability scores: lr.predict_proba(X_te_sc)[:, 1] Compute roc_curve() and roc_auc_score(). Plot the ROC curve. Mark the default threshold=0.5 operating point.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — ROC curve for LogisticRegression")
print("=" * 60)
lr_scores = lr.predict_proba(X_te_sc)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, lr_scores)
auc_lr = roc_auc_score(y_test, lr_scores)
print(f"LogisticRegression AUC: {auc_lr:.3f}")
#
plt.figure(figsize=(7, 6))
plt.plot(fpr, tpr, label=f'LR (AUC={auc_lr:.3f})')
plt.plot([0,1], [0,1], 'k--', label='Random (AUC=0.50)')
# Mark threshold=0.5 point
idx_05 = np.argmin(np.abs(thresholds - 0.5))
plt.scatter(fpr[idx_05], tpr[idx_05], color='red', zorder=5, label='threshold=0.5')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate (Recall)')
plt.title('ROC Curve — Intrusion Detector')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

Run your file. You should see:
```
LogisticRegression AUC: ~0.983
```

---

## Step 5: Compare Three Models on One ROC Plot

Plot ROC curves for all three models on the same axes. Note: DummyClassifier always predicts 0 — use np.zeros or predict_proba fallback. Label each with its AUC. Identify the winner.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — ROC curves for three models")
print("=" * 60)
dummy_scores = np.zeros(len(y_test))  # always predicts benign
#
dt_scores = dt.predict_proba(X_test)[:, 1]
#
models_info = [
    ("DummyClassifier",    dummy_scores),
    ("LogisticRegression", lr_scores),
    ("DecisionTree",       dt_scores),
]
plt.figure(figsize=(8, 6))
for name, scores in models_info:
    fpr_m, tpr_m, _ = roc_curve(y_test, scores)
    auc_m = roc_auc_score(y_test, scores)
    plt.plot(fpr_m, tpr_m, label=f'{name} (AUC={auc_m:.3f})')
    print(f"{name:25s} AUC: {auc_m:.3f}")
plt.plot([0,1],[0,1],'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

Run your file. You should see:
```
DummyClassifier           AUC: 0.500
LogisticRegression        AUC: ~0.983
DecisionTree              AUC: ~0.966
(Plot shows LR curve above DT curve, both well above the diagonal)
```

---

## Step 6: Find the Optimal Threshold

For LogisticRegression, find the threshold that minimises the distance to the top-left corner of the ROC curve: sqrt((1 - TPR)^2 + FPR^2) Print the optimal threshold, its TPR, and its FPR.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Optimal threshold from ROC curve")
print("=" * 60)
lr_scores = lr.predict_proba(X_te_sc)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, lr_scores)
distances = np.sqrt((1 - tpr)**2 + fpr**2)
best_idx  = np.argmin(distances)
opt_thresh = thresholds[best_idx]
opt_tpr    = tpr[best_idx]
opt_fpr    = fpr[best_idx]
print(f"Optimal threshold (min distance to top-left): {opt_thresh:.3f}")
print(f"At this threshold: TPR={opt_tpr:.3f}, FPR={opt_fpr:.3f}")
```

Run your file. You should see:
```
Optimal threshold: ~0.37
TPR=~0.860, FPR=~0.012
```

---

## Step 7: TASK 4 (BONUS) — Full Evaluation Scorecard

Print a table with columns: Model | Accuracy | Precision | Recall | F1 | AUC for all three models. This is the complete comparison.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Full evaluation scorecard")
print("=" * 60)
then loop through and compute each metric.
```

Run your file. You should see:
```
Model                  Accuracy  Precision  Recall    F1     AUC
DummyClassifier          0.950     0.000    0.000  0.000  0.500
LogisticRegression        0.980     ~0.857   ~0.720 ~0.783 ~0.983
DecisionTree              0.977     ~0.812   ~0.780 ~0.796 ~0.966
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
