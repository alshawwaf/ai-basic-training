# =============================================================================
# LESSON 3.12 | WORKSHOP | Exercise 3 of 4
# Batch Size Effects
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How batch size affects gradient noise and training stability
# - The small-batch generalisation advantage (flat minima)
# - How to time training and compare wall-clock performance
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson12_hyperparameter_tuning/workshop/exercise3_batch_size_effects.py
# =============================================================================

import time
import numpy as np
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
# batch_size controls how many training samples are used per gradient update.
#
#   batch_size=32   → 50 updates per epoch, noisy gradients → implicit regularisation
#   batch_size=512  → ~3 updates per epoch, stable gradients → faster but sharper minima
#   batch_size=full → 1 update per epoch, cleanest gradient → often overfits more
#
# Real-world rule: start with 32 or 64. Go larger only if training is too slow and
# you have a GPU that can handle it.

def build_model():
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return m

EPOCHS = 30

# =============================================================================
# TASK 1 — Small batch: batch_size=32
# =============================================================================
# Build a fresh model with build_model().
# Record the start time with time.time().
# Train for EPOCHS epochs with batch_size=32, validation_data=(X_val, y_val), verbose=0.
# Record elapsed time.
# Print: "batch_size=  32 | val_accuracy: X.XXXX | time: X.Xs"
#
# EXPECTED OUTPUT (approximate):
#   batch_size=  32 | val_accuracy: 0.9150 | time: 4.1s

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Large batch: batch_size=512
# =============================================================================
# Repeat with batch_size=512.
# Print the same formatted line.
#
# EXPECTED OUTPUT (approximate):
#   batch_size= 512 | val_accuracy: 0.9000 | time: 1.7s

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Full batch: batch_size=len(X_train)
# =============================================================================
# Use the entire training set as a single batch.
# Print the same formatted line.
# Does accuracy drop? Is it noticeably faster?
#
# EXPECTED OUTPUT (approximate):
#   batch_size=1600 | val_accuracy: 0.8850 | time: 0.9s

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Summary comparison (BONUS)
# =============================================================================
# Print a table showing all three results side by side, including:
#   - batch_size
#   - val_accuracy
#   - training time
#   - number of gradient updates per epoch (= ceil(len(X_train) / batch_size))

# >>> YOUR CODE HERE


print("\n--- Exercise 3 complete. Move to exercise4_architecture_search.py ---")
