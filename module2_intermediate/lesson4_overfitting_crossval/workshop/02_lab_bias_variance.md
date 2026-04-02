# Lab -- Exercise 2: Bias-Variance Tradeoff

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_bias_variance.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
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
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
```

---

## Step 4: Train Three Models: Underfit, Good Fit, Overfit

depth=1 (underfit), depth=5 (good), depth=50 (overfit). Print a 3-row table: model | train acc | val acc | gap | regime

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Three regimes: underfit vs good vs overfit")
print("=" * 60)
configs = [(1, "UNDERFIT"), (5, "GOOD FIT"), (50, "OVERFIT")]
models = {}
print(f"{'Depth':>5} {'Regime':>10} | {'Train':>7} | {'Val':>7} | {'Gap':>6}")
print("-" * 50)
for depth, label in configs:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    va = m.score(X_val,   y_val)
    models[depth] = m
    print(f"{depth:>5} {label:>10} | {tr:>7.3f} | {va:>7.3f} | {tr-va:>6.3f}")
```

Run your file. You should see:
```
depth=1  UNDERFIT:  train=0.652, val=0.648, gap=0.004
depth=5  GOOD FIT:  train=0.990, val=0.969, gap=0.021
depth=50 OVERFIT:   train=1.000, val=0.941, gap=0.059
```

---

## Step 5: Classification Reports for All Three

Print classification_report on val set for all three models. Comment on how recall for attack class changes across regimes.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Classification reports")
print("=" * 60)
for depth, label in configs:
    y_pred = models[depth].predict(X_val)
    print(f"\n--- depth={depth} ({label}) ---")
    print(classification_report(y_val, y_pred, target_names=['benign','attack']))
```

Run your file. You should see:
```
depth=1: attack recall ~0.65 (misses many attacks — too simple)
depth=5: attack recall ~0.97 (good detection)
depth=50: attack recall ~0.94 (overfit but still decent on val)
```

---

## Step 6: Visualise Decision Boundaries in PCA Space

Reduce X to 2D PCA. Create a 1×3 subplot showing decision regions for depth=1, 5, 50. (Use meshgrid + contourf on 2D PCA space)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Decision boundaries in PCA space")
print("=" * 60)
print("Decision boundary plot created.")
from sklearn.pipeline import Pipeline
pca = PCA(n_components=2, random_state=42)
X_train_2d = pca.fit_transform(X_train)
X_val_2d   = pca.transform(X_val)
#
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (depth, label) in zip(axes, configs):
    m2 = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m2.fit(X_train_2d, y_train)
    # meshgrid for contour
    xx, yy = np.meshgrid(np.linspace(X_train_2d[:,0].min()-0.5, X_train_2d[:,0].max()+0.5, 200),
                          np.linspace(X_train_2d[:,1].min()-0.5, X_train_2d[:,1].max()+0.5, 200))
    Z = m2.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    ax.scatter(X_val_2d[:,0], X_val_2d[:,1], c=y_val, alpha=0.3, s=5, cmap='RdBu')
    acc = m2.score(X_val_2d, y_val)
    ax.set_title(f'depth={depth} ({label})\nVal acc={acc:.3f}')
plt.suptitle('Decision Boundaries: Underfit / Good / Overfit')
plt.tight_layout()
plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Learning Curves

Use learning_curve() to plot train vs val score as training size increases. Compare depth=1 vs depth=5 vs depth=50.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Learning curves")
print("=" * 60)
print("\n--- Exercise 2 complete. Move to exercise3_kfold_crossval.py ---")
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for ax, (depth, label) in zip(axes, configs):
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    sizes, tr_scores, val_scores = learning_curve(
        m, X_train, y_train, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy')
    ax.plot(sizes, tr_scores.mean(1), 'b-', label='Train')
    ax.plot(sizes, val_scores.mean(1), 'r--', label='Val')
    ax.fill_between(sizes, tr_scores.mean(1)-tr_scores.std(1),
                    tr_scores.mean(1)+tr_scores.std(1), alpha=0.1, color='b')
    ax.set_title(f'depth={depth} ({label})')
    ax.legend(fontsize=8)
plt.suptitle('Learning Curves')
plt.tight_layout()
plt.show()
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_bias_variance.py`) if anything looks different.
