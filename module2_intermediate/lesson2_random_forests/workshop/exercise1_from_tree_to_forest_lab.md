# Lab — Exercise 1: From Tree to Forest

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_from_tree_to_forest.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
```

---

## Step 3: Generate the PE file malware dataset

Add this data-generation block. It creates 2000 samples — 1000 benign and 1000 malware PE files with realistic feature distributions.

```python
np.random.seed(42)
n = 2000
benign = pd.DataFrame({
    'file_entropy':       np.random.normal(5.5, 0.8, n//2).clip(3, 7.9),
    'num_sections':       np.random.poisson(4, n//2).clip(2, 10),
    'num_imports':        np.random.normal(80, 25, n//2).clip(5, 200).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.05).astype(int),
    'virtual_size_ratio': np.random.normal(1.2, 0.3, n//2).clip(0.8, 3),
    'code_section_size':  np.random.normal(50000, 20000, n//2).clip(1000, 200000).astype(int),
    'import_entropy':     np.random.normal(4.2, 0.6, n//2).clip(1, 6),
    'label': 0
})
malware = pd.DataFrame({
    'file_entropy':       np.random.normal(7.2, 0.4, n//2).clip(5, 8),
    'num_sections':       np.random.poisson(6, n//2).clip(2, 15),
    'num_imports':        np.random.normal(35, 20, n//2).clip(0, 150).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.68).astype(int),
    'virtual_size_ratio': np.random.normal(2.8, 0.8, n//2).clip(0.5, 8),
    'code_section_size':  np.random.normal(15000, 10000, n//2).clip(500, 100000).astype(int),
    'import_entropy':     np.random.normal(3.1, 0.9, n//2).clip(0.5, 5.5),
    'label': 1
})
df = pd.concat([benign, malware], ignore_index=True).sample(frac=1, random_state=42)
FEATURES = ['file_entropy', 'num_sections', 'num_imports', 'has_packer_sig',
            'virtual_size_ratio', 'code_section_size', 'import_entropy']
X = df[FEATURES]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Step 4: Task 1 — Single unlimited decision tree

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Single unlimited decision tree")
print("=" * 60)

single_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
single_tree.fit(X_train, y_train)
train_acc = single_tree.score(X_train, y_train)
test_acc  = single_tree.score(X_test,  y_test)
print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")
print(f"Overfit gap:       {train_acc - test_acc:.3f}")
```

Run your file. You should see:

```
TASK 1 — Single unlimited decision tree
============================================================
Training accuracy: 1.000
Test accuracy:     ~0.891
Overfit gap:       ~0.109
```

---

## Step 5: Task 2 — Manual bagging with 10 trees

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Manual bagging (10 trees, bootstrap sampling)")
print("=" * 60)

n_trees = 10
all_preds = []
n_train   = len(X_train)
for i in range(n_trees):
    idx = np.random.choice(n_train, n_train, replace=True)   # bootstrap
    X_boot = X_train.iloc[idx]
    y_boot = y_train.iloc[idx]
    t = DecisionTreeClassifier(max_depth=None, random_state=i)
    t.fit(X_boot, y_boot)
    all_preds.append(t.predict(X_test))
# Majority vote
stacked = np.array(all_preds)   # shape (10, n_test)
y_pred_ensemble = np.array([np.bincount(stacked[:, j]).argmax()
                             for j in range(stacked.shape[1])])
ensemble_acc = np.mean(y_pred_ensemble == y_test.values)
print(f"Single tree test accuracy:  {test_acc:.3f}")
print(f"Manual ensemble (10 trees): {ensemble_acc:.3f}")
```

Run your file. You should see:

```
TASK 2 — Manual bagging (10 trees, bootstrap sampling)
============================================================
Single tree test accuracy:  ~0.891
Manual ensemble (10 trees): ~0.931
```

---

## Step 6: Task 3 — Variance comparison (20 trees vs 20 forests)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Single tree vs forest: variance comparison")
print("=" * 60)

tree_accs, forest_accs = [], []
for seed in range(20):
    t = DecisionTreeClassifier(max_depth=None, random_state=seed)
    t.fit(X_train, y_train)
    tree_accs.append(t.score(X_test, y_test))
    rf = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
    rf.fit(X_train, y_train)
    forest_accs.append(rf.score(X_test, y_test))
print(f"20 single trees:   mean={np.mean(tree_accs):.3f}, std={np.std(tree_accs):.3f}")
print(f"20 random forests: mean={np.mean(forest_accs):.3f}, std={np.std(forest_accs):.3f}")
```

Run your file. You should see:

```
TASK 3 — Single tree vs forest: variance comparison
============================================================
20 single trees:   mean=~0.888, std=~0.031  (high variance)
20 random forests: mean=~0.943, std=~0.005  (much more stable)
```

---

## Step 7: Task 4 (BONUS) — OOB score

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — OOB score as free validation estimate")
print("=" * 60)

rf_oob = RandomForestClassifier(n_estimators=200, oob_score=True,
                                 random_state=42, n_jobs=-1)
rf_oob.fit(X_train, y_train)
oob  = rf_oob.oob_score_
test = rf_oob.score(X_test, y_test)
print(f"OOB score:   {oob:.3f}")
print(f"Test score:  {test:.3f}")
print(f"Difference:  {abs(oob - test):.3f}  <- small = OOB is reliable")

print("\n--- Exercise 1 complete. Move to exercise2_train_random_forest.py ---")
```

Run your file. You should see:

```
TASK 4 (BONUS) — OOB score as free validation estimate
============================================================
OOB score:   ~0.941
Test score:  ~0.943
Difference:  ~0.002
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
