# =============================================================================
# LESSON 2.4 | WORKSHOP | Exercise 1 of 4
# Overfitting Demo
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to create a 3-way train/val/test split for hyperparameter tuning
# - How to watch train vs validation accuracy diverge as tree depth increases
# - How to identify the overfitting point
# - Why the validation set (not test set) is used to pick hyperparameters
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson4_overfitting_crossval/workshop/exercise1_overfitting_demo.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# --- Network intrusion dataset (do not modify) ------------------------------
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
X = df[FEATURES]
y = df['label']
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Three-Way Split (60/20/20)
# =============================================================================
# Split into train (60%), validation (20%), test (20%).
# Print sizes of each split.

print("=" * 60)
print("TASK 1 — Three-way split")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#   X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
#   # 0.25 of 80% = 20% of total
#   print(f"Train size:      {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
#   print(f"Validation size: {len(X_val)}  ({len(X_val)/len(X)*100:.0f}%)")
#   print(f"Test size:       {len(X_test)}  ({len(X_test)/len(X)*100:.0f}%)")

# EXPECTED OUTPUT:
# Train size:      2400 (60%)
# Validation size:  800 (20%)
# Test size:        800 (20%)

# =============================================================================
# TASK 2 — Depth Sweep (1 to 20)
# =============================================================================
# Sweep max_depth 1-20. For each, record train accuracy and VALIDATION accuracy.
# Print a table.

print("\n" + "=" * 60)
print("TASK 2 — Depth sweep")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   depths = range(1, 21)
#   train_accs, val_accs = [], []
#   print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>6}")
#   print("-" * 35)
#   for d in depths:
#       m = DecisionTreeClassifier(max_depth=d, random_state=42)
#       m.fit(X_train, y_train)
#       tr = m.score(X_train, y_train)
#       va = m.score(X_val,   y_val)
#       train_accs.append(tr)
#       val_accs.append(va)
#       print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr-va:>6.3f}")

# =============================================================================
# TASK 3 — Plot and Identify the Overfitting Point
# =============================================================================
# Plot train and val accuracy curves. Mark the sweet-spot depth.

print("\n" + "=" * 60)
print("TASK 3 — Overfitting plot")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   best_depth = list(depths)[np.argmax(val_accs)]
#   print(f"Best validation accuracy at depth={best_depth}: {max(val_accs):.3f}")
#
#   plt.figure(figsize=(10, 6))
#   plt.plot(list(depths), train_accs, 'b-o', label='Training', markersize=4)
#   plt.plot(list(depths), val_accs,   'r--s', label='Validation', markersize=4)
#   plt.axvline(best_depth, color='green', linestyle=':', label=f'Sweet spot (depth={best_depth})')
#   plt.xlabel('max_depth'), plt.ylabel('Accuracy')
#   plt.title('Overfitting Demo: Train vs Validation Accuracy')
#   plt.legend(), plt.grid(True, alpha=0.3), plt.show()

# =============================================================================
# TASK 4 (BONUS) — Report Gap at Key Depths
# =============================================================================
# Print: train acc, val acc, gap at depths 1, 5, 10, 20.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Gap at key depths")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   key_depths = [1, 5, 10, 20]
#   print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>8}")
#   print("-" * 36)
#   for d in key_depths:
#       tr = train_accs[d-1]
#       va = val_accs[d-1]
#       print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr-va:>8.3f}")

print("\n--- Exercise 1 complete. Move to exercise2_bias_variance.py ---")
