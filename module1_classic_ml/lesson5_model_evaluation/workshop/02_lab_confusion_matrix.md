# Lab -- Exercise 2: Confusion Matrix

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_confusion_matrix.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_total, n_attack, n_benign = 10_000, 500, 9_500
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
model   = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_tr_sc, y_train)
y_pred  = model.predict(X_te_sc)
```

---

## Step 4: Compute TN, FP, FN, TP Manually

Using boolean operations on y_test and y_pred arrays, compute each cell. Print each value with its security meaning.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Manual confusion matrix values")
print("=" * 60)
TP = np.sum((y_pred == 1) & (y_test == 1))
TN = np.sum((y_pred == 0) & (y_test == 0))
FP = np.sum((y_pred == 1) & (y_test == 0))
FN = np.sum((y_pred == 0) & (y_test == 1))
print(f"True Negatives  (TN) = {TN:4d}  — benign correctly ignored")
print(f"False Positives (FP) = {FP:4d}  — benign falsely flagged (alert fatigue)")
print(f"False Negatives (FN) = {FN:4d}  — ATTACKS MISSED! (most dangerous)")
print(f"True Positives  (TP) = {TP:4d}  — attacks correctly caught")
print(f"\nTotal: {TP+TN+FP+FN} (should be {len(y_test)})")
```

Run your file. You should see:
```
True Negatives  (TN) = 1888  — benign correctly ignored
False Positives (FP) =   12  — benign falsely flagged
False Negatives (FN) =   28  — ATTACKS MISSED!
True Positives  (TP) =   72  — attacks correctly caught
Total: 2000
```

---

## Step 5: Verify with sklearn

Use sklearn's confusion_matrix() to get the 2x2 array. Print it as a labelled table. Verify it matches Task 1's values.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — sklearn confusion matrix")
print("=" * 60)
cm = confusion_matrix(y_test, y_pred)
print("              Predicted Benign  Predicted Attack")
print(f"Actual Benign      {cm[0,0]:6d}            {cm[0,1]:6d}")
print(f"Actual Attack      {cm[1,0]:6d}            {cm[1,1]:6d}")
matches = (cm[0,0]==TN and cm[0,1]==FP and cm[1,0]==FN and cm[1,1]==TP)
print(f"\nMatches manual calculation: {matches} {'✓' if matches else '✗'}")
```

Run your file. You should see:
```
Predicted Benign  Predicted Attack
Actual Benign        1888               12
Actual Attack          28               72
Matches manual calculation: True ✓
```

---

## Step 6: Derive All Metrics from TP/TN/FP/FN

Using only TP, TN, FP, FN (the variables from Task 1), compute: accuracy, precision, recall, specificity, F1 Print each with its formula as a comment.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Metrics derived from confusion matrix")
print("=" * 60)
accuracy    = (TP + TN) / (TP + TN + FP + FN)
precision   = TP / (TP + FP)
recall      = TP / (TP + FN)
specificity = TN / (TN + FP)
f1          = 2 * precision * recall / (precision + recall)
print(f"Accuracy    = (TP+TN)/(TP+TN+FP+FN) = {accuracy:.3f}")
print(f"Precision   = TP/(TP+FP)             = {precision:.3f}")
print(f"Recall      = TP/(TP+FN)             = {recall:.3f}")
print(f"Specificity = TN/(TN+FP)             = {specificity:.3f}")
print(f"F1          = 2*P*R/(P+R)            = {f1:.3f}")
```

Run your file. You should see:
```
Accuracy    = 0.980
Precision   = 0.857
Recall      = 0.720
Specificity = 0.994
F1          = 0.783
```

---

## Step 7: TASK 4 (BONUS) — Confusion Matrix Heatmap

Create a seaborn heatmap of the confusion matrix. Annotate each cell with its count AND percentage of total. Label axes: "Predicted" (x) and "Actual" (y).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Heatmap visualisation")
print("=" * 60)
print("\n--- Exercise 2 complete. Move to exercise3_precision_recall_f1.py ---")
if HAS_SEABORN:
    labels = [['TN', 'FP'], ['FN', 'TP']]
    pcts   = cm / cm.sum() * 100
    annots = [[f"{cm[i,j]}\n({pcts[i,j]:.1f}%)" for j in range(2)] for i in range(2)]
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=annots, fmt='', cmap='Blues',
                xticklabels=['Benign', 'Attack'],
                yticklabels=['Benign', 'Attack'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix — Intrusion Detector')
    plt.tight_layout()
    plt.show()
else:
    print("seaborn not installed — skipping heatmap")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
