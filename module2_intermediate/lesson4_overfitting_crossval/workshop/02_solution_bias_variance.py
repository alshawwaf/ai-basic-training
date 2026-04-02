# Exercise 2 — Bias-Variance Tradeoff
#
# Goal: Compare three decision-tree regimes (underfit, good, overfit),
#       visualise their decision boundaries in PCA space, and plot
#       learning curves to see the bias-variance tradeoff in action.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
n_per = 1000

benign = pd.DataFrame({
    'connection_rate': np.random.normal(10, 3, n_per).clip(1, 25),
    'bytes_sent': np.random.normal(5000, 1500, n_per).clip(100, 15000),
    'bytes_received': np.random.normal(8000, 2000, n_per).clip(100, 20000),
    'unique_dest_ports': np.random.poisson(3, n_per).clip(1, 10),
    'duration_seconds': np.random.normal(30, 10, n_per).clip(1, 120),
    'failed_connections': np.random.poisson(0.5, n_per),
    'label': 0})

attack = pd.DataFrame({
    'connection_rate': np.random.normal(80, 25, n_per).clip(10, 250),
    'bytes_sent': np.random.normal(30000, 15000, n_per).clip(100, 200000),
    'bytes_received': np.random.normal(2000, 1000, n_per).clip(0, 20000),
    'unique_dest_ports': np.random.normal(20, 10, n_per).clip(1, 60).astype(int),
    'duration_seconds': np.random.normal(10, 5, n_per).clip(0.1, 60),
    'failed_connections': np.random.poisson(3, n_per),
    'label': 1})

df = pd.concat([benign, attack], ignore_index=True).sample(frac=1, random_state=42)

FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df[FEATURES]
y = df['label']

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

# ============================================================
# TASK 1 — Three regimes: underfit vs good vs overfit
# ============================================================
# depth=1 is too simple (high bias, low variance — underfit).
# depth=5 is just right (balanced bias-variance — good fit).
# depth=50 memorises the training data (low bias, high variance — overfit).
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
    va = m.score(X_val, y_val)
    models[depth] = m
    print(f"{depth:>5} {label:>10} | {tr:>7.3f} | {va:>7.3f} | {tr - va:>6.3f}")

# ============================================================
# TASK 2 — Classification reports
# ============================================================
# Detailed precision/recall/f1 for each regime on the validation set.
# Watch how attack recall changes: underfit misses attacks, good fit
# catches them, overfit starts to lose some due to noise memorisation.
print("\n" + "=" * 60)
print("TASK 2 — Classification reports")
print("=" * 60)

for depth, label in configs:
    y_pred = models[depth].predict(X_val)
    print(f"\n--- depth={depth} ({label}) ---")
    print(classification_report(y_val, y_pred, target_names=['benign', 'attack']))

# ============================================================
# TASK 3 — Decision boundaries in PCA space
# ============================================================
# Reduce to 2D with PCA, then train fresh trees on the 2D data and
# plot decision regions with meshgrid + contourf. The underfit model
# has a single straight boundary, the overfit model has many jagged ones.
print("\n" + "=" * 60)
print("TASK 3 — Decision boundaries in PCA space")
print("=" * 60)

pca = PCA(n_components=2, random_state=42)
X_train_2d = pca.fit_transform(X_train)
X_val_2d   = pca.transform(X_val)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (depth, label) in zip(axes, configs):
    # Train a new tree on the 2D PCA features for visualisation
    m2 = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m2.fit(X_train_2d, y_train)

    # Create a mesh grid covering the PCA feature space
    xx, yy = np.meshgrid(
        np.linspace(X_train_2d[:, 0].min() - 0.5,
                    X_train_2d[:, 0].max() + 0.5, 200),
        np.linspace(X_train_2d[:, 1].min() - 0.5,
                    X_train_2d[:, 1].max() + 0.5, 200))
    Z = m2.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    ax.scatter(X_val_2d[:, 0], X_val_2d[:, 1], c=y_val, alpha=0.3,
               s=5, cmap='RdBu')
    acc = m2.score(X_val_2d, y_val)
    ax.set_title(f'depth={depth} ({label})\nVal acc={acc:.3f}')

plt.suptitle('Decision Boundaries: Underfit / Good / Overfit')
plt.tight_layout()
plt.savefig('module2_intermediate/lesson4_ex2_boundaries.png')
plt.close()
print("Decision boundary plot saved.")

# ============================================================
# TASK 4 (BONUS) — Learning curves
# ============================================================
# learning_curve() trains the model on increasing fractions of the
# training set. Underfit: both curves stay low (high bias). Overfit:
# training curve is perfect but validation lags behind (high variance).
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Learning curves")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for ax, (depth, label) in zip(axes, configs):
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    sizes, tr_scores, val_scores = learning_curve(
        m, X_train, y_train, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy')
    ax.plot(sizes, tr_scores.mean(1), 'b-', label='Train')
    ax.plot(sizes, val_scores.mean(1), 'r--', label='Val')
    ax.fill_between(sizes,
                    tr_scores.mean(1) - tr_scores.std(1),
                    tr_scores.mean(1) + tr_scores.std(1),
                    alpha=0.1, color='b')
    ax.set_title(f'depth={depth} ({label})')
    ax.set_xlabel('Training set size')
    ax.legend(fontsize=8)

axes[0].set_ylabel('Accuracy')
plt.suptitle('Learning Curves')
plt.tight_layout()
plt.savefig('module2_intermediate/lesson4_ex2_learning_curves.png')
plt.close()
print("Learning curves plot saved.")

print("\n--- Exercise 2 complete. Move to 03_solution_kfold_crossval.py ---")
