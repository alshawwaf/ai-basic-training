# =============================================================================
# LESSON 3.12 | WORKSHOP | Exercise 2 of 4
# Learning Rate Sensitivity
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How learning rate controls step size in gradient descent
# - Visual difference between too-small, correct, and too-large lr
# - How to diagnose training problems from loss curves
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson12_hyperparameter_tuning/workshop/exercise2_learning_rate_sensitivity.py
# =============================================================================

import numpy as np
import tensorflow as tf
from tensorflow import keras

tf.random.set_seed(42)
np.random.seed(42)

# --- Data (same synthetic dataset used throughout this workshop) ---
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                            n_redundant=5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)

# =============================================================================
# BACKGROUND
# =============================================================================
# The learning rate (lr) controls how far the optimizer steps each update:
#
#   new_weight = old_weight - lr * gradient
#
# lr=0.001  → safe default for Adam, usually converges smoothly
# lr=0.1    → too large: loss may spike or oscillate
# lr=0.00001 → too small: loss barely moves in 30 epochs
#
# This exercise trains the same architecture three times — only lr changes.

def build_model(learning_rate):
    """Build and compile the same architecture with a given learning rate."""
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ])
    m.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return m

# =============================================================================
# TASK 1 — Baseline: lr = 0.001
# =============================================================================
# Build a model using build_model(0.001).
# Train it for 30 epochs with validation_data=(X_val, y_val) and verbose=0.
# Store the History object in a variable called history1.
# Print the final val_accuracy.
#
# EXPECTED OUTPUT (approximate):
#   lr=0.001000 | final val_accuracy: 0.9150
#   Loss trajectory: smooth decline from ~0.65 to ~0.20

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Too large: lr = 0.1
# =============================================================================
# Repeat with build_model(0.1). Store history in history2.
# Print the final val_accuracy.
# Observe: does the loss curve oscillate or spike?
#
# EXPECTED OUTPUT (approximate):
#   lr=0.100000 | final val_accuracy: ~0.75-0.88 (varies more between runs)
#   Loss trajectory: erratic, may spike upward mid-training

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Too small: lr = 0.00001
# =============================================================================
# Repeat with build_model(0.00001). Store history in history3.
# Print the final val_accuracy.
# Observe: has the loss actually moved much?
#
# EXPECTED OUTPUT (approximate):
#   lr=0.000010 | final val_accuracy: ~0.55-0.65 (barely above random)
#   Loss trajectory: almost flat — very slow descent

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Compare loss trajectories (BONUS)
# =============================================================================
# Print the loss at epochs 1, 5, 10, 20, 30 for all three runs side by side.
# Format: "Epoch 10 | lr=0.001: 0.2834  lr=0.1: 0.3912  lr=0.00001: 0.6891"
#
# The histories store per-epoch loss in history.history['loss'] as a Python list.

# >>> YOUR CODE HERE


print("\n--- Exercise 2 complete. Move to exercise3_batch_size_effects.py ---")
