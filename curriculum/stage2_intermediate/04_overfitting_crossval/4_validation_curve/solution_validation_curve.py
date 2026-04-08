# Exercise 4 — Validation Curve (Automatic Parameter Sweep)
#
# Goal: Use sklearn's validation_curve() to automatically sweep
#       max_depth for a decision tree and n_estimators for a random
#       forest, identifying the optimal hyperparameter values.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, validation_curve

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
X = df[FEATURES].astype(float).values
y = df['label'].values

# Inject Gaussian noise so the validation curve actually shows three regions.
rng = np.random.default_rng(13)
X = X + rng.normal(0, X.std(axis=0) * 1.5, X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ============================================================
# TASK 1 — validation_curve() for max_depth 1-20
# ============================================================
# validation_curve() handles the CV loop internally — it fits the
# model at each parameter value across all folds and returns arrays
# of shape (n_params, n_folds).
print("=" * 60)
print("TASK 1 — validation_curve() for max_depth 1-20")
print("=" * 60)

param_range = np.arange(1, 21)
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=42),
    X_train, y_train,
    param_name='max_depth',
    param_range=param_range,
    cv=5, scoring='accuracy')

train_mean = train_scores.mean(axis=1)
val_mean   = val_scores.mean(axis=1)

print(f"{'Depth':>6} | {'Train mean':>10} | {'Val mean':>10}")
print("-" * 34)
for d, tr, va in zip(param_range, train_mean, val_mean):
    print(f"{d:>6} | {tr:>10.3f} | {va:>10.3f}")

# ============================================================
# TASK 2 — Plot validation curve with std bands
# ============================================================
# The shaded bands show +/- 1 standard deviation across folds.
# Where the gap between train and val is small = good generalisation.
# Where train is perfect but val drops = overfitting.
print("\n" + "=" * 60)
print("TASK 2 — Plot validation curve with std bands")
print("=" * 60)

train_std = train_scores.std(axis=1)
val_std   = val_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, 'b-o', label='Training score')
plt.fill_between(param_range, train_mean - train_std,
                 train_mean + train_std, alpha=0.15, color='blue')
plt.plot(param_range, val_mean, 'r-o', label='Validation score')
plt.fill_between(param_range, val_mean - val_std,
                 val_mean + val_std, alpha=0.15, color='red')

best_depth = param_range[np.argmax(val_mean)]
plt.axvline(best_depth, color='green', linestyle='--',
            label=f'Best depth = {best_depth}')
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Validation Curve — DecisionTreeClassifier (max_depth)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson4_ex4_val_curve_tree.png')
plt.close()
print("Validation curve plot saved.")

# ============================================================
# TASK 3 — Find optimal depth and measure overfitting gap
# ============================================================
# Compare the best depth (peak validation score) with a very deep
# tree (depth=20) to quantify how much performance is lost to
# overfitting.
print("\n" + "=" * 60)
print("TASK 3 — Find optimal depth and measure overfitting gap")
print("=" * 60)

best_idx   = np.argmax(val_mean)
best_depth = param_range[best_idx]

print(f"Best depth: {best_depth}")
print(f"  Train accuracy: {train_mean[best_idx]:.3f}")
print(f"  Val accuracy:   {val_mean[best_idx]:.3f}")
print(f"  Overfit gap:    {train_mean[best_idx] - val_mean[best_idx]:.3f}")
print()
print(f"At depth=20:")
print(f"  Train accuracy: {train_mean[-1]:.3f}")
print(f"  Val accuracy:   {val_mean[-1]:.3f}")
print(f"  Overfit gap:    {train_mean[-1] - val_mean[-1]:.3f}")

# ============================================================
# TASK 4 (BONUS) — Validation curve for RandomForest n_estimators
# ============================================================
# Random Forests are less prone to overfitting than single trees.
# More trees generally improve performance and then plateau — you
# rarely see validation score decrease with more trees.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Validation curve for RandomForest n_estimators")
print("=" * 60)

rf_range = [10, 25, 50, 75, 100, 150, 200]
train_rf, val_rf = validation_curve(
    RandomForestClassifier(random_state=42),
    X_train, y_train,
    param_name='n_estimators',
    param_range=rf_range,
    cv=5, scoring='accuracy')

train_rf_mean = train_rf.mean(axis=1)
val_rf_mean   = val_rf.mean(axis=1)

print(f"{'Trees':>6} | {'Train':>7} | {'Val':>7}")
print("-" * 26)
for n, tr, va in zip(rf_range, train_rf_mean, val_rf_mean):
    print(f"{n:>6} | {tr:>7.3f} | {va:>7.3f}")

plt.figure(figsize=(10, 5))
plt.plot(rf_range, train_rf_mean, 'b-o', label='Train')
plt.plot(rf_range, val_rf_mean, 'r-o', label='Validation')
plt.xlabel('n_estimators')
plt.ylabel('Accuracy')
plt.title('Validation Curve — RandomForest (n_estimators)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson4_ex4_val_curve_rf.png')
plt.close()
print("RandomForest validation curve plot saved.")

print("\n--- Exercise 4 complete. Lesson 2.4 workshop done! ---")
