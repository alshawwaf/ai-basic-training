# Exercise 1 — Overfitting Demo
#
# Goal: See how a decision tree overfits as max_depth increases.
#       Use a three-way split (train/val/test) and a depth sweep to
#       find the sweet-spot depth before overfitting kicks in.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

np.random.seed(42)

# ── Generate network traffic dataset (self-contained) ────────────────────────
# Binary classification: benign (0) vs attack (1), 1000 samples each.
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

# Add per-feature Gaussian noise so the two classes overlap. Without this
# the synthetic distributions are too clean — depth=1 already scores 99.8 %
# and there is no overfitting story to teach.
rng = np.random.default_rng(13)
X = X + rng.normal(0, X.std(axis=0) * 1.5, X.shape)

# ============================================================
# TASK 1 — Three-way split
# ============================================================
# Split into 60% train, 20% validation, 20% test.
# The validation set is used to tune hyperparameters (depth).
# The test set is held out for final evaluation only.
print("=" * 60)
print("TASK 1 — Three-way split")
print("=" * 60)

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
# 0.25 of 80% = 20% of total

print(f"Train size:      {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Validation size: {len(X_val)}  ({len(X_val)/len(X)*100:.0f}%)")
print(f"Test size:       {len(X_test)}  ({len(X_test)/len(X)*100:.0f}%)")

# ============================================================
# TASK 2 — Depth sweep
# ============================================================
# Train a decision tree for each depth 1-20. Record training and
# validation accuracy. As depth increases, training accuracy goes
# toward 1.0 but validation accuracy plateaus or drops — overfitting.
print("\n" + "=" * 60)
print("TASK 2 — Depth sweep")
print("=" * 60)

depths = range(1, 21)
train_accs, val_accs = [], []

print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>6}")
print("-" * 35)
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42)
    m.fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    va = m.score(X_val, y_val)
    train_accs.append(tr)
    val_accs.append(va)
    print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr - va:>6.3f}")

# ============================================================
# TASK 3 — Overfitting plot
# ============================================================
# Plot train vs validation accuracy across depths. The green dotted
# line marks the sweet-spot depth (highest validation accuracy).
print("\n" + "=" * 60)
print("TASK 3 — Overfitting plot")
print("=" * 60)

best_depth = list(depths)[np.argmax(val_accs)]
print(f"Best validation accuracy at depth={best_depth}: {max(val_accs):.3f}")

plt.figure(figsize=(10, 6))
plt.plot(list(depths), train_accs, 'b-o', label='Training', markersize=4)
plt.plot(list(depths), val_accs, 'r--s', label='Validation', markersize=4)
plt.axvline(best_depth, color='green', linestyle=':',
            label=f'Sweet spot (depth={best_depth})')
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Overfitting Demo: Train vs Validation Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson4_ex1_overfitting.png')
plt.close()
print("Overfitting plot saved.")

# ============================================================
# TASK 4 (BONUS) — Gap at key depths
# ============================================================
# Summarise the train-val gap at specific depths to see how
# overfitting grows with model complexity.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Gap at key depths")
print("=" * 60)

key_depths = [1, 5, 10, 20]
print(f"{'Depth':>5} | {'Train':>7} | {'Val':>7} | {'Gap':>8}")
print("-" * 36)
for d in key_depths:
    tr = train_accs[d - 1]
    va = val_accs[d - 1]
    print(f"{d:>5} | {tr:>7.3f} | {va:>7.3f} | {tr - va:>8.3f}")

print("\n--- Exercise 1 complete. Move to ../2_bias_variance/solution.py ---")
