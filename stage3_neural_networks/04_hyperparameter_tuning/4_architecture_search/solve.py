# Exercise 4 — Architecture Search
#
# Systematically tries different network widths and depths to find the
# best architecture for a given dataset. This is a manual grid search:
# for each combination of (units, depth), build, train, and record
# validation accuracy. The winner is the combo with the highest score.
#
# Prerequisite: pip install tensorflow scikit-learn pandas

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 4 — Architecture Search")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup ─────────────────────────────────────────────────────────────
X, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                            n_redundant=5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)

EPOCHS = 30

def build_model(units, depth):
    """Build a model with `depth` hidden layers each containing `units` neurons."""
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential()
    m.add(keras.layers.Input(shape=(20,)))
    for _ in range(depth):
        m.add(keras.layers.Dense(units, activation='relu'))
    m.add(keras.layers.Dense(1, activation='sigmoid'))
    m.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return m

# ── TASK 1 — Define the search space ────────────────────────────────────────
# Three widths (32, 64, 128) and three depths (1, 2, 3) gives 9 combinations.
# This is a small grid — production searches may cover hundreds of configs.
print("\n" + "=" * 60)
print("TASK 1 — Define the search space")
print("=" * 60)

units_options = [32, 64, 128]
depth_options = [1, 2, 3]

print(f"Units options: {units_options}")
print(f"Depth options: {depth_options}")
print(f"Total combinations: {len(units_options) * len(depth_options)}")

# ── TASK 2 — Run the grid search ────────────────────────────────────────────
# For each (units, depth) combination: build, train, measure val_accuracy.
# Also record parameter count to see the cost of larger architectures.
print("\n" + "=" * 60)
print("TASK 2 — Run the grid search")
print("=" * 60)

results = []
for depth in depth_options:
    for units in units_options:
        model = build_model(units, depth)
        model.fit(X_train, y_train, epochs=EPOCHS, batch_size=64,
                  validation_data=(X_val, y_val), verbose=0)
        _, val_acc = model.evaluate(X_val, y_val, verbose=0)
        n_params = model.count_params()
        results.append({
            'units': units,
            'depth': depth,
            'val_acc': round(val_acc, 4),
            'params': n_params
        })
        print(f"  units={units:>3}, depth={depth} | "
              f"val_acc={val_acc:.4f} | params={n_params:,}")

# ── TASK 3 — Print results table ────────────────────────────────────────────
# Sort by validation accuracy to see the ranking. The best architecture
# balances capacity (enough to learn the patterns) against complexity
# (not so many parameters that it overfits or wastes compute).
print("\n" + "=" * 60)
print("TASK 3 — Print results table")
print("=" * 60)

df = pd.DataFrame(results).sort_values('val_acc', ascending=False)
print(df.to_string(index=False))

# ── TASK 4 (BONUS) — Identify the winner ────────────────────────────────────
# Report the best architecture found by the grid search.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Identify the winner")
print("=" * 60)

best = df.iloc[0]
print(f"Best architecture: units={int(best['units'])}, depth={int(best['depth'])}, "
      f"val_accuracy={best['val_acc']:.4f}")
print(f"Parameter count:   {int(best['params']):,}")

print("\nKey insight:")
print("  - Bigger is not always better — diminishing returns set in quickly")
print("  - The simplest model that reaches near-best accuracy is often preferred")
print("  - In security applications, smaller models also mean faster inference")
print("    (important for real-time threat detection)")

print("\n--- Exercise 4 complete. Workshop finished! Open reference_solution.py to compare. ---")
