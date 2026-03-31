# =============================================================================
# LESSON 3.9 | WORKSHOP | Exercise 2 of 4
# Build the Network — Layers, Activations, Output Shape
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to choose activation functions: relu for hidden, sigmoid for binary output
# - How to set the output layer shape to match your problem (1 for binary, N for N-class)
# - How to compile a model: optimizer, loss function, and metrics
# - How switching from binary to multi-class changes the architecture
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson9_first_neural_network/workshop/exercise2_build_the_network.py
# =============================================================================

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras

# --- Dataset setup (do not modify) ------------------------------------------
X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)
print(f"Dataset: {X_train.shape[0]} train / {X_test.shape[0]} test samples")
print(f"Class distribution (train): {np.bincount(y_train)}")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Choosing the right activation function is one of the most important design
# decisions in building a neural network.
#
# Hidden layers — use ReLU (Rectified Linear Unit):
#   relu(x) = max(0, x)
#   Fast to compute, avoids vanishing gradients, default choice for hidden layers.
#
# Output layer — depends on your problem:
#   Binary classification (attack vs benign):  1 unit, sigmoid
#     sigmoid(x) = 1 / (1 + e^-x)  → outputs probability ∈ [0, 1]
#     Loss: binary_crossentropy
#
#   Multi-class (N classes):  N units, softmax
#     softmax turns N raw scores into N probabilities that sum to 1.0
#     Loss: sparse_categorical_crossentropy (when y is integer labels)
#           categorical_crossentropy        (when y is one-hot encoded)
#
#   Regression (predict a number):  1 unit, no activation (linear)
#     Loss: mse or mae

# =============================================================================
# TASK 1 — Build the Binary Classifier Network
# =============================================================================
# Build a Sequential model:
#   Input: 10 features
#   Layer 1: Dense(64, relu)
#   Layer 2: Dense(32, relu)
#   Output:  Dense(1, sigmoid)
# Call model.summary() and read the output shape and parameter count.

print("\n" + "=" * 60)
print("TASK 1 — Build the binary classifier")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = keras.Sequential([
#       keras.layers.Dense(64, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(32, activation='relu'),
#       keras.layers.Dense(1,  activation='sigmoid')
#   ])
#   model.summary()

# EXPECTED OUTPUT (approximately):
# Layer 1: Dense(64)  → Output: (None, 64)  → Params: 704
# Layer 2: Dense(32)  → Output: (None, 32)  → Params: 2,080
# Layer 3: Dense(1)   → Output: (None, 1)   → Params: 33
# Total trainable params: ~2,817

# =============================================================================
# TASK 2 — Count Total Trainable Parameters
# =============================================================================
# For each layer compute (inputs × units) + units manually.
# Print the breakdown and verify against model.count_params().

print("\n" + "=" * 60)
print("TASK 2 — Parameter count breakdown")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   l1 = (10 * 64) + 64
#   l2 = (64 * 32) + 32
#   l3 = (32 *  1) +  1
#   print(f"Dense(64): (10×64)+64   = {l1}")
#   print(f"Dense(32): (64×32)+32   = {l2}")
#   print(f"Dense(1):  (32×1) +1    = {l3}")
#   print(f"Total:                    {l1+l2+l3}")
#   print(f"model.count_params():     {model.count_params()}")

# EXPECTED OUTPUT:
# Dense(64): (10×64)+64  = 704
# Dense(32): (64×32)+32  = 2080
# Dense(1):  (32×1) +1   = 33
# Total:                   2817

# =============================================================================
# TASK 3 — Compile the Model
# =============================================================================
# Compile the model with:
#   optimizer: 'adam'
#   loss:      'binary_crossentropy'
#   metrics:   ['accuracy']
# Print confirmation that compilation succeeded.

print("\n" + "=" * 60)
print("TASK 3 — Compile the model")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model.compile(
#       optimizer='adam',
#       loss='binary_crossentropy',
#       metrics=['accuracy']
#   )
#   print("Model compiled successfully.")
#   print(f"Optimizer: {model.optimizer.__class__.__name__}")
#   print(f"Loss:      {model.loss}")

# EXPECTED OUTPUT:
# Model compiled successfully.
# Optimizer: Adam
# Loss: binary_crossentropy

# =============================================================================
# TASK 4 (BONUS) — Switch to 3-Class Problem
# =============================================================================
# Create a new dataset with 3 classes:
#   X3, y3 = make_classification(n_samples=2000, n_features=10, n_classes=3,
#                                 n_informative=6, n_clusters_per_class=1,
#                                 random_state=42)
# Build a new model:
#   Dense(64, relu) → Dense(32, relu) → Dense(3, softmax)
# Compile with loss='sparse_categorical_crossentropy'
# Print model.summary() and count_params().
# Notice: output layer now has 3 units instead of 1.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — 3-class classifier")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   from sklearn.datasets import make_classification
#   X3, y3 = make_classification(n_samples=2000, n_features=10, n_classes=3,
#                                 n_informative=6, n_clusters_per_class=1,
#                                 random_state=42)
#   model3 = keras.Sequential([
#       keras.layers.Dense(64, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(32, activation='relu'),
#       keras.layers.Dense(3,  activation='softmax')
#   ])
#   model3.compile(optimizer='adam',
#                  loss='sparse_categorical_crossentropy',
#                  metrics=['accuracy'])
#   model3.summary()
#   print(f"Output layer for 3-class: {model3.layers[-1].units} units (softmax)")

# EXPECTED OUTPUT:
# Output layer for 3-class: 3 units (softmax)

print("\n--- Exercise 2 complete. Move to exercise3_compile_and_train.py ---")
