# Exercise 1 — What Are Hyperparameters? Parameters vs Hyperparameters
#
# Parameters (weights/biases) are learned by the optimiser during training.
# Hyperparameters (learning rate, batch size, layer widths, dropout rate)
# are chosen by the engineer BEFORE training begins. Different hyperparameter
# choices can produce dramatically different model performance.
#
# Prerequisite: pip install tensorflow scikit-learn

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("EXERCISE 1 — What Are Hyperparameters?")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup ─────────────────────────────────────────────────────────────
# Imbalanced binary classification (90/10 split) — common in security
# scenarios like malware detection where malicious samples are rare.
X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)
print("Dataset ready.")

# ── TASK 1 — Weights before and after training ───────────────────────────────
# Weights start as small random values (initialisation). After training,
# they shift to values that minimise the loss. These are PARAMETERS —
# they are learned, not chosen by the engineer.
print("\n" + "=" * 60)
print("TASK 1 — Weights before and after training")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(10,)),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])

# Capture weights BEFORE training (random initialisation)
weights_before = model.layers[0].get_weights()[0].copy()  # shape (10, 8)
print("Layer 1 weights BEFORE training (first row):")
print(weights_before[0].round(4))

# Train for 10 epochs
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

# Capture weights AFTER training (optimised values)
weights_after = model.layers[0].get_weights()[0]
print("\nLayer 1 weights AFTER training (first row):")
print(weights_after[0].round(4))
print(f"\nWeights changed: {not np.allclose(weights_before, weights_after)}")
print(f"Mean absolute change: {np.abs(weights_after - weights_before).mean():.4f}")

# ── TASK 2 — Complete hyperparameter inventory ───────────────────────────────
# Every choice you make before calling model.fit() is a hyperparameter.
# This table catalogues them by category so you know what you can tune.
print("\n" + "=" * 60)
print("TASK 2 — Complete hyperparameter inventory")
print("=" * 60)

hyperparams = {
    'Architecture': {
        'n_hidden_layers': 1,
        'units_layer_1': 8,
        'activation_hidden': 'relu',
        'output_units': 1,
        'activation_output': 'sigmoid',
    },
    'Regularisation': {
        'dropout_rate': 0.0,
        'l1_penalty': 0.0,
        'l2_penalty': 0.0,
    },
    'Optimiser': {
        'optimizer': 'adam',
        'learning_rate': 0.001,
        'beta_1': 0.9,
        'beta_2': 0.999,
    },
    'Training': {
        'epochs': 10,
        'batch_size': 32,
        'validation_split': 0.0,
    }
}

print(f"{'Category':>16} | {'Hyperparameter':>20} | {'Value'}")
print("-" * 52)
for category, params in hyperparams.items():
    for name, val in params.items():
        print(f"{category:>16} | {name:>20} | {val}")
    print("-" * 52)

# ── TASK 3 — Different hyperparameters, different results ────────────────────
# Same data, same task — only hyperparameters differ. Model B has a wider
# network and a higher learning rate, which often helps it converge faster
# and find a better solution for this dataset.
print("\n" + "=" * 60)
print("TASK 3 — Different hyperparameters, different results")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_a = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(10,)),
    keras.layers.Dense(1, activation='sigmoid')
])
model_a.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='binary_crossentropy', metrics=['accuracy'])
model_a.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
_, acc_a = model_a.evaluate(X_test, y_test, verbose=0)

model_b = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model_b.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
                loss='binary_crossentropy', metrics=['accuracy'])
model_b.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
_, acc_b = model_b.evaluate(X_test, y_test, verbose=0)

print(f"Model A (Dense(8),  lr=0.001): test accuracy = {acc_a:.4f}")
print(f"Model B (Dense(64,32), lr=0.01): test accuracy = {acc_b:.4f}")
print(f"Difference:                       {abs(acc_b - acc_a):.4f}")

# ── TASK 4 (BONUS) — Reproducibility with random seeds ──────────────────────
# Without seeds, weight initialisation and data shuffling vary between runs,
# producing slightly different results. Setting both np and tf seeds locks
# down the randomness so results are identical across runs.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Reproducibility with random seeds")
print("=" * 60)

def make_model_and_train():
    m = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(10,)),
        keras.layers.Dense(1,  activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    m.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    _, acc = m.evaluate(X_test, y_test, verbose=0)
    return acc

# Without seed — results differ between runs
acc1 = make_model_and_train()
acc2 = make_model_and_train()
print(f"Without seed: {acc1:.4f}, {acc2:.4f} — same? {abs(acc1-acc2) < 0.001}")

# With seed — results identical
tf.random.set_seed(99); np.random.seed(99)
acc3 = make_model_and_train()
tf.random.set_seed(99); np.random.seed(99)
acc4 = make_model_and_train()
print(f"With seed:    {acc3:.4f}, {acc4:.4f} — same? {abs(acc3-acc4) < 0.001}")

print("\n--- Exercise 1 complete. Move to ../2_learning_rate_sensitivity/solution.py ---")
