# Lab -- Exercise 3: K-Fold Cross-Validation

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_kfold_crossval.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import (train_test_split, cross_val_score,
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
X = df[FEATURES]; y = df['label']
X_train_all, X_test, y_train_all, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

---

## Step 4: Single Split vs K-Fold

1. Train depth=5 tree on X_train_all, evaluate on X_test → single score 2. Run cross_val_score with cv=5 on X_train_all Print both. Show the std from CV tells you how reliable the single split is.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Single split vs 5-fold CV")
print("=" * 60)
m = DecisionTreeClassifier(max_depth=5, random_state=42)
m.fit(X_train_all, y_train_all)
single_score = m.score(X_test, y_test)
cv5_scores   = cross_val_score(
    DecisionTreeClassifier(max_depth=5, random_state=42),
    X_train_all, y_train_all, cv=5, scoring='accuracy')
print(f"Single test split score: {single_score:.3f}")
print(f"5-fold CV mean:          {cv5_scores.mean():.3f} ± {cv5_scores.std():.3f}")
print(f"Individual fold scores:  {cv5_scores.round(3)}")
```

Run your file. You should see:
```
Single test split score: ~0.969
5-fold CV mean:          ~0.968 ± 0.008
```

---

## Step 5: 5-Fold vs 10-Fold

Compare cv=5 and cv=10 for the same model. Print mean and std for each.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — 5-fold vs 10-fold CV")
print("=" * 60)
model = DecisionTreeClassifier(max_depth=5, random_state=42)
for cv_k in [5, 10]:
    scores = cross_val_score(model, X_train_all, y_train_all, cv=cv_k)
    print(f"{cv_k}-fold CV: mean={scores.mean():.3f}, std={scores.std():.4f}")
```

Run your file. You should see:
```
5-fold  CV: mean=~0.968, std=~0.0080
10-fold CV: mean=~0.969, std=~0.0062
```

---

## Step 6: CV for Multiple Depths

Run 5-fold CV for max_depth 1-15. Plot mean ± std for each depth.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — 5-fold CV across depths")
print("=" * 60)
depths = range(1, 16)
cv_means, cv_stds = [], []
for d in depths:
    scores = cross_val_score(DecisionTreeClassifier(max_depth=d, random_state=42),
                              X_train_all, y_train_all, cv=5)
    cv_means.append(scores.mean())
    cv_stds.append(scores.std())
best_d = list(depths)[np.argmax(cv_means)]
print(f"Best depth by CV: {best_d} (mean CV acc = {max(cv_means):.3f})")
#
cv_means_arr = np.array(cv_means)
cv_stds_arr  = np.array(cv_stds)
plt.figure(figsize=(10, 6))
plt.plot(list(depths), cv_means_arr, 'b-o', label='CV mean')
plt.fill_between(list(depths),
                 cv_means_arr - cv_stds_arr,
                 cv_means_arr + cv_stds_arr,
                 alpha=0.2, color='b', label='±1 std')
plt.axvline(best_d, color='green', linestyle=':', label=f'Best (depth={best_d})')
plt.xlabel('max_depth'), plt.ylabel('CV Accuracy')
plt.title('5-Fold CV Accuracy vs Tree Depth')
plt.legend(), plt.grid(True, alpha=0.3), plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Verify Class Balance in Folds

Use StratifiedKFold to manually iterate over folds. For each fold, print the fraction of attack samples. Show all folds have approximately the same class ratio.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Verify stratification")
print("=" * 60)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print(f"Overall attack rate: {y_train_all.mean():.3f}")
print(f"\nFold | Attack rate")
print("-" * 22)
for i, (train_idx, val_idx) in enumerate(skf.split(X_train_all, y_train_all)):
    fold_rate = y_train_all.iloc[val_idx].mean()
    print(f"   {i+1} | {fold_rate:.3f}")
```

Run your file. You should see:
```
Overall attack rate: 0.500
Fold | Attack rate
1 | ~0.500
2 | ~0.500
...  (all ≈ 0.500 — stratified)
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
