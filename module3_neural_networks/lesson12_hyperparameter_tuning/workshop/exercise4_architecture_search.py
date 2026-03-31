# =============================================================================
# LESSON 3.12 | WORKSHOP | Exercise 4 of 4
# Architecture Search
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to define and search over architecture hyperparameters (width × depth)
# - How to run a manual grid search and store results in a DataFrame
# - How to read results to identify the best configuration
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson12_hyperparameter_tuning/workshop/exercise4_architecture_search.py
# =============================================================================

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

tf.random.set_seed(42)
np.random.seed(42)

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
# Architecture = number of layers (depth) + units per layer (width).
# This is also a hyperparameter — and often has a larger effect than lr or batch size.
#
# Grid search: try every (units, depth) combination, record val_accuracy.
# Sort by accuracy. Pick the winner.
#
# units_options = [32, 64, 128]
# depth_options = [1, 2, 3]
# Total: 9 models to train.

def build_model(units, depth):
    """
    Build a fully-connected network with:
      - `depth` hidden layers, each with `units` neurons and ReLU activation
      - 1 output neuron with sigmoid activation
    """
    tf.random.set_seed(42)
    np.random.seed(42)
    layers = [keras.layers.Dense(units, activation='relu', input_shape=(20,))]
    for _ in range(depth - 1):
        layers.append(keras.layers.Dense(units, activation='relu'))
    layers.append(keras.layers.Dense(1, activation='sigmoid'))
    m = keras.Sequential(layers)
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return m

# =============================================================================
# TASK 1 — Define the search space
# =============================================================================
# Create:
#   units_options = [32, 64, 128]
#   depth_options = [1, 2, 3]
#
# Print a message: "Searching 9 architectures (units × depth)..."

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Run the grid search
# =============================================================================
# Nested loop over depth_options and units_options.
# For each combination:
#   1. Build the model with build_model(units, depth)
#   2. Train for 20 epochs with verbose=0
#   3. Evaluate on (X_val, y_val) to get val_acc
#   4. Append a dict to a `results` list:
#      {"units": units, "depth": depth, "val_acc": val_acc, "params": model.count_params()}
#   5. Print a progress line: "  units=64, depth=2 → val_acc=0.9150"
#
# Use verbose=0 in model.fit() to keep output clean.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Print results table
# =============================================================================
# Convert `results` to a DataFrame.
# Sort by "val_acc" descending.
# Print with: print(df.to_string(index=False))
#
# EXPECTED OUTPUT (approximate):
#  units  depth  val_acc  params
#    128      2   0.9200   10625
#     64      2   0.9150    4929
#    128      1   0.9100    5505
#   ...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Identify the winner (BONUS)
# =============================================================================
# Print: "Best architecture: units=X, depth=Y, val_accuracy=Z.ZZZZ"
# Use df.iloc[0] after sorting.

# >>> YOUR CODE HERE


print("\n--- Exercise 4 complete. Workshop finished! Open reference_solution.py to compare. ---")
