# =============================================================================
# LESSON 3.12 | WORKSHOP | Exercise 1 of 4
# What Are Hyperparameters? — Parameters vs Hyperparameters
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - The distinction between model parameters (learned) and hyperparameters (set by you)
# - How to inspect actual weight values before and after training
# - How to list all hyperparameters in a standard Keras model
# - How two models with different hyperparameters produce different results
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson12_hyperparameter_tuning/workshop/exercise1_what_are_hyperparameters.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras

tf.random.set_seed(42)
np.random.seed(42)

# --- Dataset setup (do not modify) ------------------------------------------
X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)
print("Dataset ready.")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Parameters (also called model weights or learned weights):
#   - Stored inside the model (layer.weights)
#   - Start as random initialisation
#   - Updated by gradient descent every batch during training
#   - Not set by you — the training algorithm adjusts them
#   - Example: the 704 weight values in Dense(64) taking 10-feature input
#
# Hyperparameters:
#   - Set by YOU before training starts
#   - Cannot be learned by gradient descent (they define the training process)
#   - Different hyperparameters → different parameters after training
#   - Must be chosen wisely — wrong values lead to slow training or failure
#
# Complete list for a standard Keras model:
#   Architecture:   n_layers, units per layer, activation functions
#   Regularisation: dropout_rate, L1/L2 penalty
#   Optimiser:      learning_rate, beta1, beta2 (Adam parameters)
#   Training:       epochs, batch_size, validation_split
#   Initialisation: kernel_initializer, bias_initializer

# =============================================================================
# TASK 1 — Inspect Weights Before and After Training
# =============================================================================
# Build a simple model: Dense(8, relu, input_shape=(10,)) → Dense(1, sigmoid)
# Print the first layer's weight matrix BEFORE training (random initialisation).
# Train for 10 epochs.
# Print the same weight matrix AFTER training.
# Verify the weights changed — this is what "training" means.

print("=" * 60)
print("TASK 1 — Weights before and after training")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = keras.Sequential([
#       keras.layers.Dense(8, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model.compile(optimizer='adam', loss='binary_crossentropy',
#                 metrics=['accuracy'])
#   # Weights BEFORE training
#   weights_before = model.layers[0].get_weights()[0].copy()  # shape (10, 8)
#   print("Layer 1 weights BEFORE training (first row):")
#   print(weights_before[0].round(4))
#   # Train
#   model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
#   # Weights AFTER training
#   weights_after = model.layers[0].get_weights()[0]
#   print("\nLayer 1 weights AFTER training (first row):")
#   print(weights_after[0].round(4))
#   print(f"\nWeights changed: {not np.allclose(weights_before, weights_after)}")
#   print(f"Mean absolute change: {np.abs(weights_after - weights_before).mean():.4f}")

# EXPECTED OUTPUT:
# Layer 1 weights BEFORE: [some random small values near 0]
# Layer 1 weights AFTER:  [different values, some larger, some smaller]
# Weights changed: True

# =============================================================================
# TASK 2 — List All Hyperparameters in a Keras Model
# =============================================================================
# Print a formatted table of all hyperparameters with their categories and values.
# Use the model from Task 1 (or rebuild it) with its specific settings.

print("\n" + "=" * 60)
print("TASK 2 — Complete hyperparameter inventory")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   hyperparams = {
#       'Architecture': {
#           'n_hidden_layers': 1,
#           'units_layer_1': 8,
#           'activation_hidden': 'relu',
#           'output_units': 1,
#           'activation_output': 'sigmoid',
#       },
#       'Regularisation': {
#           'dropout_rate': 0.0,
#           'l1_penalty': 0.0,
#           'l2_penalty': 0.0,
#       },
#       'Optimiser': {
#           'optimizer': 'adam',
#           'learning_rate': 0.001,
#           'beta_1': 0.9,
#           'beta_2': 0.999,
#       },
#       'Training': {
#           'epochs': 10,
#           'batch_size': 32,
#           'validation_split': 0.0,
#       }
#   }
#   print(f"{'Category':>16} | {'Hyperparameter':>20} | {'Value'}")
#   print("-" * 52)
#   for category, params in hyperparams.items():
#       for name, val in params.items():
#           print(f"{category:>16} | {name:>20} | {val}")
#       print("-" * 52)

# =============================================================================
# TASK 3 — Two Models, Different Hyperparameters, Different Results
# =============================================================================
# Build Model A: Dense(8, relu) → Dense(1, sigmoid), lr=0.001, epochs=20
# Build Model B: Dense(64, relu) → Dense(32, relu) → Dense(1, sigmoid), lr=0.01, epochs=20
# Train both. Print test accuracy for each.
# Show that different hyperparameters produce different final accuracy.

print("\n" + "=" * 60)
print("TASK 3 — Different hyperparameters, different results")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_a = keras.Sequential([
#       keras.layers.Dense(8, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model_a.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
#                   loss='binary_crossentropy', metrics=['accuracy'])
#   model_a.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
#   _, acc_a = model_a.evaluate(X_test, y_test, verbose=0)
#
#   model_b = keras.Sequential([
#       keras.layers.Dense(64, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(32, activation='relu'),
#       keras.layers.Dense(1,  activation='sigmoid')
#   ])
#   model_b.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
#                   loss='binary_crossentropy', metrics=['accuracy'])
#   model_b.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
#   _, acc_b = model_b.evaluate(X_test, y_test, verbose=0)
#
#   print(f"Model A (Dense(8),  lr=0.001): test accuracy = {acc_a:.4f}")
#   print(f"Model B (Dense(64,32), lr=0.01): test accuracy = {acc_b:.4f}")
#   print(f"Difference:                       {abs(acc_b - acc_a):.4f}")

# EXPECTED OUTPUT (approximately):
# Model A: test accuracy = ~0.910
# Model B: test accuracy = ~0.940
# Different hyperparameters → different results!

# =============================================================================
# TASK 4 (BONUS) — Set Random Seed for Reproducibility
# =============================================================================
# Train the same model TWICE without a seed. Print both test accuracies.
# Then train twice WITH tf.random.set_seed() and np.random.seed().
# Show that setting the seed makes results identical.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Reproducibility with random seeds")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   def make_model_and_train():
#       m = keras.Sequential([
#           keras.layers.Dense(32, activation='relu', input_shape=(10,)),
#           keras.layers.Dense(1,  activation='sigmoid')
#       ])
#       m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#       m.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
#       _, acc = m.evaluate(X_test, y_test, verbose=0)
#       return acc
#
#   # Without seed — results differ
#   acc1 = make_model_and_train()
#   acc2 = make_model_and_train()
#   print(f"Without seed: {acc1:.4f}, {acc2:.4f} — same? {abs(acc1-acc2) < 0.001}")
#
#   # With seed — results identical
#   tf.random.set_seed(99); np.random.seed(99)
#   acc3 = make_model_and_train()
#   tf.random.set_seed(99); np.random.seed(99)
#   acc4 = make_model_and_train()
#   print(f"With seed:    {acc3:.4f}, {acc4:.4f} — same? {abs(acc3-acc4) < 0.001}")

print("\n--- Exercise 1 complete. Move to exercise2_learning_rate_sensitivity.py ---")
