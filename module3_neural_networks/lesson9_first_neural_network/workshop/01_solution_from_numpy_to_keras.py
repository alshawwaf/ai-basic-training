# Exercise 1 — From NumPy to Keras
#
# Shows how Keras Dense layers are the same matrix-multiply-plus-bias
# operation you built from scratch in the foundations, but wrapped in
# a high-level API that handles shapes and activations automatically.
#
# Prerequisite: pip install tensorflow

import numpy as np
import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("EXERCISE 1 — From NumPy to Keras")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── TASK 1 — Build the Model ────────────────────────────────────────────────────
# A Sequential model chains layers: output of layer N feeds into layer N+1.
# Dense(8, relu) = matrix multiply (4 inputs x 8 neurons) + bias + ReLU.
# Dense(1, sigmoid) = maps to a single probability output in [0, 1].
print("\n" + "=" * 60)
print("TASK 1 — Build the Model")
print("=" * 60)

model = keras.Sequential([
    # input_shape=(4,) tells Keras the first layer receives 4-feature input
    keras.layers.Dense(8, activation='relu', input_shape=(4,)),
    # sigmoid squashes output to [0, 1] — interpret as P(positive class)
    keras.layers.Dense(1, activation='sigmoid')
])

# model.summary() prints layer names, output shapes, and parameter counts
model.summary()

# ── TASK 2 — Manual Parameter Count ─────────────────────────────────────────────
# Each Dense layer has: weight matrix W of shape (n_inputs, n_units)
#                       bias vector b of shape (n_units,)
# Total params per layer = (n_inputs x n_units) + n_units
print("\n" + "=" * 60)
print("TASK 2 — Manual Parameter Count")
print("=" * 60)

# Layer 1: Dense(8) receives 4 inputs
layer1_params = (4 * 8) + 8   # 32 weights + 8 biases = 40
print(f"Layer 1 (Dense 8):  (4 x 8) + 8 = {layer1_params}")

# Layer 2: Dense(1) receives 8 inputs (from previous layer's 8 units)
layer2_params = (8 * 1) + 1   # 8 weights + 1 bias = 9
print(f"Layer 2 (Dense 1):  (8 x 1) + 1 = {layer2_params}")

total_manual = layer1_params + layer2_params
total_keras = model.count_params()
print(f"Total (manual): {total_manual}")
print(f"Total (Keras):  {total_keras}")
print(f"Match: {total_manual == total_keras}")

# ── TASK 3 — Run a Prediction (Forward Pass) ────────────────────────────────────
# model.predict() pushes data through each layer's weights and activations.
# Before training the weights are random, so the output is meaningless —
# but the shape tells you the architecture is wired up correctly.
print("\n" + "=" * 60)
print("TASK 3 — Run a Prediction (Forward Pass)")
print("=" * 60)

# Create 3 random samples, each with 4 features
# Input must be 2D: (n_samples, n_features)
X_dummy = np.random.randn(3, 4).astype('float32')
output = model.predict(X_dummy, verbose=0)

print(f"Input shape:   {X_dummy.shape}")
print(f"Output shape:  {output.shape}")
print(f"Output values: {output.flatten()}")
# Because the last layer is sigmoid, all outputs must be between 0 and 1
print(f"All values between 0 and 1: {bool(np.all((output >= 0) & (output <= 1)))}")

# ── TASK 4 (BONUS) — Architecture Comparison ────────────────────────────────────
# Parameter count grows rapidly with layer width.
# A 256-unit first layer with 10 inputs already has (10*256)+256 = 2,816 params.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Architecture Comparison")
print("=" * 60)

architectures = {
    'Tiny  [4 → 4 → 1]':       [4, 1],
    'Small [4 → 64 → 32 → 1]': [64, 32, 1],
    'Large [10 → 256 → 128 → 64 → 1]': [256, 128, 64, 1],
}

# Build each model and compare total parameter counts
for name, units_list in architectures.items():
    # Use input_shape=(10,) for the large model, (4,) for the others
    input_dim = 10 if '10' in name else 4
    layers = []
    for i, u in enumerate(units_list):
        if i == 0:
            act = 'sigmoid' if u == 1 else 'relu'
            layers.append(keras.layers.Dense(u, activation=act,
                                             input_shape=(input_dim,)))
        else:
            act = 'sigmoid' if u == 1 else 'relu'
            layers.append(keras.layers.Dense(u, activation=act))

    m = keras.Sequential(layers)
    print(f"  {name:45s} → {m.count_params():>7,} params")

print("\n--- Exercise 1 complete. Move to 02_solution_build_the_network.py ---")
