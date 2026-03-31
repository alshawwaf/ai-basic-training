# =============================================================================
# LESSON 3.10 | WORKSHOP | Exercise 3 of 4
# Batch Normalisation — Stabilise Training, Allow Higher Learning Rates
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How BatchNormalization normalises activations within each mini-batch
# - Why BatchNorm makes training faster and more stable (smoother loss curves)
# - How to combine BatchNorm + Dropout in a single architecture
# - How removing BatchNorm from one layer affects the training curve
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson10_dropout_regularisation/workshop/exercise3_batch_normalisation.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
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
# When activations pass through many layers, their scale can shift and grow.
# This is called "internal covariate shift" — the distribution of each layer's
# inputs changes as weights in previous layers are updated.
#
# BatchNormalization (Ioffe & Szegedy, 2015) fixes this by:
#   1. Computing mean and variance of activations within each mini-batch
#   2. Normalising: z = (x - mean) / sqrt(variance + epsilon)
#   3. Scaling and shifting with learned parameters gamma and beta
#
# Benefits:
#   - More stable training (smoother, less spiky loss curves)
#   - Allows higher learning rates → faster convergence
#   - Provides slight regularisation (noise from batch statistics)
#   - Reduces sensitivity to weight initialisation
#
# Standard placement: Dense(units, no activation) → BatchNorm → Activation
# Or simpler (also common): Dense(units, activation) → BatchNorm
# In practice both placements work — the second is more common in tutorials.

# =============================================================================
# TASK 1 — Add BatchNormalization After Each Dense Layer
# =============================================================================
# Architecture:
#   Dense(256, relu) → BatchNormalization
#   Dense(256, relu) → BatchNormalization
#   Dense(256, relu) → BatchNormalization
#   Dense(1, sigmoid)
# Train for 50 epochs. Record the loss curve — it should be smoother.

print("=" * 60)
print("TASK 1 — Train with BatchNormalization")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_bn = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model_bn.compile(optimizer='adam', loss='binary_crossentropy',
#                    metrics=['accuracy'])
#   history_bn = model_bn.fit(X_train, y_train, validation_split=0.2,
#                              epochs=50, batch_size=32, verbose=0)
#   print(f"Final val_loss: {history_bn.history['val_loss'][-1]:.4f}")
#   print(f"Final val_acc:  {history_bn.history['val_accuracy'][-1]:.4f}")

# =============================================================================
# TASK 2 — Compare Training Stability (Smoother Loss Curve)
# =============================================================================
# Build a baseline WITHOUT BatchNorm (same architecture, just no BN layers).
# Plot both training loss curves side by side.
# The BN version should converge faster and have a smoother curve.

print("\n" + "=" * 60)
print("TASK 2 — Compare training stability")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_no_bn = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model_no_bn.compile(optimizer='adam', loss='binary_crossentropy',
#                       metrics=['accuracy'])
#   history_no_bn = model_no_bn.fit(X_train, y_train, validation_split=0.2,
#                                    epochs=50, batch_size=32, verbose=0)
#
#   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
#   ax1.plot(history_no_bn.history['loss'], label='Train', color='blue')
#   ax1.plot(history_no_bn.history['val_loss'], label='Val', color='red')
#   ax1.set_title('No BatchNorm')
#   ax1.set_xlabel('Epoch'), ax1.set_ylabel('Loss')
#   ax1.legend(), ax1.grid(True, alpha=0.3)
#
#   ax2.plot(history_bn.history['loss'], label='Train', color='blue')
#   ax2.plot(history_bn.history['val_loss'], label='Val', color='red')
#   ax2.set_title('With BatchNorm')
#   ax2.set_xlabel('Epoch'), ax2.set_ylabel('Loss')
#   ax2.legend(), ax2.grid(True, alpha=0.3)
#
#   plt.suptitle('Training Stability: No BatchNorm vs BatchNorm')
#   plt.tight_layout()
#   plt.show()

# =============================================================================
# TASK 3 — Combine BatchNorm + Dropout in One Model
# =============================================================================
# Build the combined architecture:
#   Dense(256, relu) → BatchNorm → Dropout(0.3)
#   Dense(256, relu) → BatchNorm → Dropout(0.3)
#   Dense(256, relu) → BatchNorm → Dropout(0.3)
#   Dense(1, sigmoid)
# Train for 50 epochs. Compare val_accuracy to BN-only and Dropout-only models.

print("\n" + "=" * 60)
print("TASK 3 — Combined BatchNorm + Dropout")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_combined = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dropout(0.3),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dropout(0.3),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dropout(0.3),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model_combined.compile(optimizer='adam', loss='binary_crossentropy',
#                           metrics=['accuracy'])
#   history_combined = model_combined.fit(X_train, y_train, validation_split=0.2,
#                                          epochs=50, batch_size=32, verbose=0)
#   print(f"BatchNorm only  val_acc: {history_bn.history['val_accuracy'][-1]:.4f}")
#   print(f"Combined BN+DO  val_acc: {history_combined.history['val_accuracy'][-1]:.4f}")

# =============================================================================
# TASK 4 (BONUS) — Remove BatchNorm from the Middle Layer
# =============================================================================
# Build an asymmetric model: BN on layers 1 and 3 but NOT on layer 2.
# Train and observe whether the loss at epoch 5-10 shows more noise compared
# to the fully normalised model. Print the std of the training loss over
# the first 20 epochs for both models.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Asymmetric BatchNorm placement")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_asym = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dense(256, activation='relu'),  # no BN here
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.BatchNormalization(),
#       keras.layers.Dense(1, activation='sigmoid')
#   ])
#   model_asym.compile(optimizer='adam', loss='binary_crossentropy',
#                      metrics=['accuracy'])
#   history_asym = model_asym.fit(X_train, y_train, validation_split=0.2,
#                                  epochs=50, batch_size=32, verbose=0)
#   loss_full = np.array(history_bn.history['loss'][:20])
#   loss_asym = np.array(history_asym.history['loss'][:20])
#   print(f"Full BN train loss std (first 20 epochs): {loss_full.std():.4f}")
#   print(f"Asymm train loss std (first 20 epochs):   {loss_asym.std():.4f}")
#   print("(Higher std = noisier training = less stable)")

print("\n--- Exercise 3 complete. Move to exercise4_early_stopping.py ---")
