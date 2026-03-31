# =============================================================================
# LESSON 3.9 | WORKSHOP | Exercise 1 of 4
# From NumPy to Keras — What a Dense Layer Actually Does
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How a Keras Sequential model relates to matrix multiply + bias + activation
# - How to build a tiny 2-layer network and read model.summary()
# - How to count parameters manually: units_in × units_out + bias = params/layer
# - How to run a single forward pass with model.predict()
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson9_first_neural_network/workshop/exercise1_from_numpy_to_keras.py
# =============================================================================

import numpy as np
import tensorflow as tf
from tensorflow import keras

# =============================================================================
# BACKGROUND
# =============================================================================
# In the foundations/ folder you built a Dense layer from scratch:
#
#   output = np.dot(inputs, weights) + biases
#
# Keras does exactly the same thing. A Dense(64, activation='relu') layer:
#   1. Stores a weight matrix W of shape (n_inputs, 64)
#   2. Stores a bias vector b of shape (1, 64)
#   3. Computes: output = relu(inputs @ W + b)
#
# A Sequential model chains layers: output of layer N is input to layer N+1.
#
# Parameter count per Dense layer:
#   n_params = (n_inputs × n_units) + n_units
#              ^-- weight matrix --^   ^bias^
#
# Example: Dense(8) taking 4 inputs → 4×8 + 8 = 40 parameters.
# model.summary() shows you this breakdown automatically.

# =============================================================================
# TASK 1 — Build a Tiny Sequential Model
# =============================================================================
# Build a Sequential model with exactly these two layers:
#   - Dense(8, activation='relu', input_shape=(4,))
#   - Dense(1, activation='sigmoid')
# Call model.summary() and read the output.

print("=" * 60)
print("TASK 1 — Build a tiny Sequential model")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = keras.Sequential([
#       keras.layers.Dense(8, activation='relu', input_shape=(4,)),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model.summary()

# EXPECTED OUTPUT (approximately):
# Model: "sequential"
# _________________________________________________________________
#  Layer (type)         Output Shape         Param #
# =================================================================
#  dense (Dense)        (None, 8)            40
#  dense_1 (Dense)      (None, 1)            9
# =================================================================
# Total params: 49  Trainable params: 49

# =============================================================================
# TASK 2 — Verify Parameter Count Manually
# =============================================================================
# For each Dense layer in your model, manually compute the parameter count
# using the formula: (inputs × units) + units
# Compare your calculation to what model.summary() shows.

print("\n" + "=" * 60)
print("TASK 2 — Verify parameter count manually")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   layer1_params = (4 * 8) + 8     # input_features × units + bias
#   layer2_params = (8 * 1) + 1     # previous_units × units + bias
#   total         = layer1_params + layer2_params
#   print(f"Layer 1 (Dense 8):  ({4} × {8}) + {8} = {layer1_params}")
#   print(f"Layer 2 (Dense 1):  ({8} × {1}) + {1} = {layer2_params}")
#   print(f"Total parameters:   {total}")
#   # Verify against model
#   print(f"model.count_params(): {model.count_params()}")
#   print(f"Match: {total == model.count_params()}")

# EXPECTED OUTPUT:
# Layer 1 (Dense 8):  (4 × 8) + 8 = 40
# Layer 2 (Dense 1):  (8 × 1) + 1 = 9
# Total parameters:   49
# model.count_params(): 49
# Match: True

# =============================================================================
# TASK 3 — Single Forward-Pass Prediction
# =============================================================================
# Create a random input array of shape (3, 4) — 3 samples, 4 features each.
# Use model.predict() to get an output.
# Print the input shape, the output shape, and the output values.
# Verify that all outputs are between 0 and 1 (sigmoid output).

print("\n" + "=" * 60)
print("TASK 3 — Single forward-pass prediction")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   np.random.seed(0)
#   sample_input = np.random.randn(3, 4).astype('float32')
#   predictions  = model.predict(sample_input, verbose=0)
#   print(f"Input shape:   {sample_input.shape}")
#   print(f"Output shape:  {predictions.shape}")
#   print(f"Output values: {predictions.flatten().round(4)}")
#   print(f"All between 0-1: {(predictions >= 0).all() and (predictions <= 1).all()}")

# EXPECTED OUTPUT:
# Input shape:   (3, 4)
# Output shape:  (3, 1)
# Output values: [some values between 0 and 1]
# All between 0-1: True

# =============================================================================
# TASK 4 (BONUS) — Watch Parameter Count Change
# =============================================================================
# Build three models with different layer sizes and print their parameter counts.
# Can you find the relationship between layer size and parameter count?
# Models to try:
#   - Dense(4) → Dense(1)
#   - Dense(64) → Dense(32) → Dense(1)
#   - Dense(256) → Dense(128) → Dense(64) → Dense(1)
# Input shape is always (10,) for all three.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Parameter count across architectures")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   configs = [
#       [(4,'relu'), (1,'sigmoid')],
#       [(64,'relu'), (32,'relu'), (1,'sigmoid')],
#       [(256,'relu'), (128,'relu'), (64,'relu'), (1,'sigmoid')],
#   ]
#   for config in configs:
#       layers = []
#       for i, (units, act) in enumerate(config):
#           if i == 0:
#               layers.append(keras.layers.Dense(units, activation=act,
#                                                input_shape=(10,)))
#           else:
#               layers.append(keras.layers.Dense(units, activation=act))
#       m = keras.Sequential(layers)
#       print(f"Architecture {[u for u,a in config]}: {m.count_params():,} params")

# EXPECTED OUTPUT:
# Architecture [4, 1]: ~51 params
# Architecture [64, 32, 1]: ~2,625 params
# Architecture [256, 128, 64, 1]: ~67,393 params

print("\n--- Exercise 1 complete. Move to exercise2_build_the_network.py ---")
