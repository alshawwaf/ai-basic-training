# =============================================================================
# LESSON 2.4 | WORKSHOP | Exercise 4 of 4
# Validation Curve — Automatic Parameter Sweep
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How validation_curve() sweeps a parameter range using cross-validation
# - How to plot train vs validation score with standard deviation bands
# - How to identify the complexity sweet spot from the curve shape
# - How the bias-variance tradeoff is visualised directly on the curve
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson4_overfitting_crossval/workshop/exercise4_validation_curve.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, validation_curve

# --- Dataset (do not modify) ------------------------------------------------
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
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# validation_curve() automates what you did manually in exercises 1-3.
# Instead of writing your own loop over parameter values, you pass:
#   - the estimator
#   - the parameter NAME (a string matching the constructor argument)
#   - the parameter RANGE (an array of values to try)
#   - cv (number of folds)
#
# It returns two 2D arrays: train_scores and val_scores, shape (n_params, cv).
# Each row corresponds to one parameter value; each column to one CV fold.
# Take the mean across columns to get the average score, std for the error band.
#
# The resulting curve reveals three regions:
#   LEFT  (low complexity):  both train and val low → underfitting (high bias)
#   MIDDLE (sweet spot):     val score peaks, small gap → best generalisation
#   RIGHT (high complexity): train keeps rising, val falls → overfitting
#
# This is the bias-variance tradeoff visualised in a single chart.

# =============================================================================
# TASK 1 — Run validation_curve() for DecisionTreeClassifier max_depth
# =============================================================================
# Use validation_curve() with:
#   - estimator: DecisionTreeClassifier(random_state=42)
#   - param_name: 'max_depth'
#   - param_range: np.arange(1, 21)   (depths 1 to 20)
#   - cv=5, scoring='accuracy'
# Print the mean train score and mean val score for each depth.

print("=" * 60)
print("TASK 1 — validation_curve() for max_depth 1-20")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   param_range = np.arange(1, 21)
#   train_scores, val_scores = validation_curve(
#       DecisionTreeClassifier(random_state=42),
#       X_train, y_train,
#       param_name='max_depth',
#       param_range=param_range,
#       cv=5, scoring='accuracy')
#   train_mean = train_scores.mean(axis=1)
#   val_mean   = val_scores.mean(axis=1)
#   print(f"{'Depth':>6} | {'Train mean':>10} | {'Val mean':>10}")
#   print("-" * 34)
#   for d, tr, va in zip(param_range, train_mean, val_mean):
#       print(f"{d:>6} | {tr:>10.3f} | {va:>10.3f}")

# EXPECTED OUTPUT:
#  Depth | Train mean |   Val mean
# ----------------------------------
#      1 |      0.648 |      0.643
#      5 |      0.989 |      0.967
#     10 |      1.000 |      0.962
#     20 |      1.000 |      0.962

# =============================================================================
# TASK 2 — Plot train vs val score with std bands
# =============================================================================
# Using the results from Task 1, create a matplotlib plot showing:
#   - Mean train score (blue line)
#   - Mean val score   (orange line)
#   - Shaded ±1 std band for each (use plt.fill_between)
#   - Vertical dashed line at the depth with the highest val score
# Label axes, add title, legend, and grid.

print("\n" + "=" * 60)
print("TASK 2 — Plot validation curve with std bands")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   train_std = train_scores.std(axis=1)
#   val_std   = val_scores.std(axis=1)
#   plt.figure(figsize=(10, 6))
#   plt.plot(param_range, train_mean, 'b-o', label='Training score')
#   plt.fill_between(param_range, train_mean - train_std, train_mean + train_std,
#                    alpha=0.15, color='blue')
#   plt.plot(param_range, val_mean, 'r-o', label='Validation score')
#   plt.fill_between(param_range, val_mean - val_std, val_mean + val_std,
#                    alpha=0.15, color='red')
#   best_depth = param_range[np.argmax(val_mean)]
#   plt.axvline(best_depth, color='green', linestyle='--',
#               label=f'Best depth = {best_depth}')
#   plt.xlabel('max_depth')
#   plt.ylabel('Accuracy')
#   plt.title('Validation Curve — DecisionTreeClassifier (max_depth)')
#   plt.legend()
#   plt.grid(True, alpha=0.3)
#   plt.tight_layout()
#   plt.show()

# =============================================================================
# TASK 3 — Identify the depth where val score peaks
# =============================================================================
# From your results array:
#   1. Find the depth with the highest mean validation score
#   2. Print the train score and val score at that depth
#   3. Print the overfitting gap at that depth (train - val)
#   4. Also print the gap at depth=20 to show how large overfitting becomes

print("\n" + "=" * 60)
print("TASK 3 — Find optimal depth and measure overfitting gap")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   best_idx   = np.argmax(val_mean)
#   best_depth = param_range[best_idx]
#   print(f"Best depth: {best_depth}")
#   print(f"  Train accuracy: {train_mean[best_idx]:.3f}")
#   print(f"  Val accuracy:   {val_mean[best_idx]:.3f}")
#   print(f"  Overfit gap:    {train_mean[best_idx] - val_mean[best_idx]:.3f}")
#   print()
#   print(f"At depth=20:")
#   print(f"  Train accuracy: {train_mean[-1]:.3f}")
#   print(f"  Val accuracy:   {val_mean[-1]:.3f}")
#   print(f"  Overfit gap:    {train_mean[-1] - val_mean[-1]:.3f}")

# EXPECTED OUTPUT:
# Best depth: 5  (or nearby — may vary slightly)
#   Train accuracy: ~0.989
#   Val accuracy:   ~0.967
#   Overfit gap:    ~0.022
#
# At depth=20:
#   Train accuracy: 1.000
#   Val accuracy:   ~0.962
#   Overfit gap:    ~0.038

# =============================================================================
# TASK 4 (BONUS) — Run validation_curve() for RandomForest n_estimators
# =============================================================================
# Repeat Tasks 1-2 but for RandomForestClassifier with:
#   - param_name: 'n_estimators'
#   - param_range: [10, 25, 50, 75, 100, 150, 200]
# Does validation score still drop at high values, or does it plateau?
# (Random forests are less prone to overfitting than single trees.)

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Validation curve for RandomForest n_estimators")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   rf_range = [10, 25, 50, 75, 100, 150, 200]
#   train_rf, val_rf = validation_curve(
#       RandomForestClassifier(random_state=42),
#       X_train, y_train,
#       param_name='n_estimators',
#       param_range=rf_range,
#       cv=5, scoring='accuracy')
#   train_rf_mean = train_rf.mean(axis=1)
#   val_rf_mean   = val_rf.mean(axis=1)
#   print(f"{'Trees':>6} | {'Train':>7} | {'Val':>7}")
#   print("-" * 26)
#   for n, tr, va in zip(rf_range, train_rf_mean, val_rf_mean):
#       print(f"{n:>6} | {tr:>7.3f} | {va:>7.3f}")
#   # Plot
#   plt.figure(figsize=(10, 5))
#   plt.plot(rf_range, train_rf_mean, 'b-o', label='Train')
#   plt.plot(rf_range, val_rf_mean,   'r-o', label='Validation')
#   plt.xlabel('n_estimators'), plt.ylabel('Accuracy')
#   plt.title('Validation Curve — RandomForest (n_estimators)')
#   plt.legend(), plt.grid(True, alpha=0.3), plt.tight_layout(), plt.show()

print("\n--- Workshop complete. Open reference_solution.py ---")
