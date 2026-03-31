# =============================================================================
# LESSON 3.10 | WORKSHOP | Exercise 1 of 4
# Demonstrate Overfitting — Large Unregularised Network
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How an oversized network overfits on relatively small training data
# - How train loss and validation loss diverge as a visual signal of overfitting
# - How to measure the overfitting gap (train accuracy - val accuracy) at epoch 50
# - How adding more layers amplifies the overfitting problem
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson10_dropout_regularisation/workshop/exercise1_demonstrate_overfitting.py
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
print(f"Training samples: {X_train.shape[0]}")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Overfitting happens when a model has far more parameters than necessary to
# represent the underlying pattern. With 3 layers of 256 units each, this
# model has over 130,000 parameters to fit 1,600 training samples.
#
# That ratio — parameters/samples — is a rough risk indicator.
# A 256×256×256 network has far more capacity than needed for 10 input features.
#
# During training the model can memorise training examples including their noise.
# The train loss keeps decreasing, but when the model sees new data (val set),
# the memorised noise patterns don't apply → val loss stops decreasing or rises.
#
# The overfitting gap = train_accuracy - val_accuracy
# In a healthy model this gap should stay under 2-3%.
# In an overfitting model this gap can exceed 10-20%.

# =============================================================================
# TASK 1 — Build and Train a Large Unregularised Network
# =============================================================================
# Build this architecture (no Dropout, no BatchNorm, no regularisation):
#   Dense(256, relu) → Dense(256, relu) → Dense(256, relu) → Dense(1, sigmoid)
# Compile with adam + binary_crossentropy.
# Train for 50 epochs with validation_split=0.2, batch_size=32.
# Store the history object.

print("=" * 60)
print("TASK 1 — Large network, 50 epochs, no regularisation")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(1,   activation='sigmoid')
#   ])
#   model.compile(optimizer='adam', loss='binary_crossentropy',
#                 metrics=['accuracy'])
#   print(f"Total parameters: {model.count_params():,}")
#   history = model.fit(X_train, y_train, validation_split=0.2,
#                       epochs=50, batch_size=32, verbose=0)
#   print(f"Final train accuracy: {history.history['accuracy'][-1]:.4f}")
#   print(f"Final val accuracy:   {history.history['val_accuracy'][-1]:.4f}")

# EXPECTED OUTPUT:
# Total parameters: ~133,633
# Final train accuracy: ~0.985+
# Final val accuracy:   ~0.940

# =============================================================================
# TASK 2 — Plot Diverging Train vs Val Loss
# =============================================================================
# Plot training loss and validation loss on the same graph.
# The divergence (val loss rising while train loss keeps falling) is the
# visual signature of overfitting. Add a title, axis labels, legend, and grid.

print("\n" + "=" * 60)
print("TASK 2 — Plot diverging loss curves")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   plt.figure(figsize=(10, 5))
#   plt.plot(history.history['loss'],     label='Train loss',      color='blue')
#   plt.plot(history.history['val_loss'], label='Validation loss', color='red')
#   plt.xlabel('Epoch')
#   plt.ylabel('Loss (binary crossentropy)')
#   plt.title('Overfitting: Train vs Validation Loss (No Regularisation)')
#   plt.legend()
#   plt.grid(True, alpha=0.3)
#   plt.tight_layout()
#   plt.show()

# =============================================================================
# TASK 3 — Measure the Overfitting Gap at Epoch 50
# =============================================================================
# Compute and print:
#   - Final train loss and train accuracy
#   - Final val loss and val accuracy
#   - Accuracy gap (train - val)
#   - Loss gap (val_loss - train_loss)

print("\n" + "=" * 60)
print("TASK 3 — Measure overfitting gap")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   train_acc = history.history['accuracy'][-1]
#   val_acc   = history.history['val_accuracy'][-1]
#   train_loss = history.history['loss'][-1]
#   val_loss   = history.history['val_loss'][-1]
#   print(f"Train accuracy:  {train_acc:.4f}  | Val accuracy:  {val_acc:.4f}")
#   print(f"Train loss:      {train_loss:.4f}  | Val loss:      {val_loss:.4f}")
#   print(f"Accuracy gap (train - val): {train_acc - val_acc:.4f}")
#   print(f"Loss gap (val - train):     {val_loss - train_loss:.4f}")

# EXPECTED OUTPUT:
# Train accuracy:  ~0.990+  | Val accuracy:  ~0.938
# Accuracy gap (train - val): ~0.050+
# Loss gap (val - train):     ~0.100+

# =============================================================================
# TASK 4 (BONUS) — Add Even More Layers and Watch It Get Worse
# =============================================================================
# Build a deeper network: 5 Dense(256) layers instead of 3.
# Train for 50 epochs. Compare the final overfitting gap to Task 3.
# The deeper model should show an even larger gap.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Even deeper network, bigger overfit")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_deep = keras.Sequential([
#       keras.layers.Dense(256, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(256, activation='relu'),
#       keras.layers.Dense(1,   activation='sigmoid')
#   ])
#   model_deep.compile(optimizer='adam', loss='binary_crossentropy',
#                      metrics=['accuracy'])
#   hist_deep = model_deep.fit(X_train, y_train, validation_split=0.2,
#                               epochs=50, batch_size=32, verbose=0)
#   gap_original = (history.history['accuracy'][-1] -
#                   history.history['val_accuracy'][-1])
#   gap_deep     = (hist_deep.history['accuracy'][-1] -
#                   hist_deep.history['val_accuracy'][-1])
#   print(f"3-layer gap: {gap_original:.4f}")
#   print(f"5-layer gap: {gap_deep:.4f}  (deeper → more overfit)")

print("\n--- Exercise 1 complete. Move to exercise2_add_dropout.py ---")
