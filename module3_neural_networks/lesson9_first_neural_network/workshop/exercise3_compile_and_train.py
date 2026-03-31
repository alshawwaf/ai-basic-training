# =============================================================================
# LESSON 3.9 | WORKSHOP | Exercise 3 of 4
# Compile and Train — Epochs, Batch Size, History Object
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to call model.fit() with validation_split and capture the history object
# - What epochs and batch_size mean and how they affect training
# - How to extract final accuracy from history.history
# - How to plot training curves: loss and accuracy, train vs validation
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson9_first_neural_network/workshop/exercise3_compile_and_train.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
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

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("Model built and compiled.")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# model.fit() is where learning happens. Key parameters:
#
# epochs — how many times the model sees the entire training set.
#   Too few: model hasn't converged (high loss).
#   Too many: model overfits (val loss rises while train loss keeps falling).
#
# batch_size — how many samples are processed before updating weights.
#   Each batch: compute loss → compute gradients → update weights.
#   With 1600 training samples and batch_size=32: 50 gradient updates per epoch.
#
# validation_split=0.2 — reserves the last 20% of training data for validation.
#   Keras uses this to report val_loss and val_accuracy each epoch.
#   This is NOT the same as X_test — test data is never seen during training.
#
# history = model.fit(...)  — the returned History object stores:
#   history.history['loss']         — list of train loss per epoch
#   history.history['val_loss']     — list of val loss per epoch
#   history.history['accuracy']     — list of train accuracy per epoch
#   history.history['val_accuracy'] — list of val accuracy per epoch

# =============================================================================
# TASK 1 — Train with validation_split and capture history
# =============================================================================
# Call model.fit() with:
#   X_train, y_train
#   validation_split=0.2
#   epochs=20
#   batch_size=32
#   verbose=1  (to see training progress)
# Store the result in a variable called 'history'.

print("\n" + "=" * 60)
print("TASK 1 — Train the model for 20 epochs")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   history = model.fit(
#       X_train, y_train,
#       validation_split=0.2,
#       epochs=20,
#       batch_size=32,
#       verbose=1
#   )

# EXPECTED OUTPUT (last epoch approximately):
# Epoch 20/20
# ... loss: ~0.15 — accuracy: ~0.95 — val_loss: ~0.17 — val_accuracy: ~0.94

# =============================================================================
# TASK 2 — Print Final Train and Val Accuracy
# =============================================================================
# From history.history, extract:
#   - Final training accuracy  (last value in history.history['accuracy'])
#   - Final validation accuracy (last value in history.history['val_accuracy'])
# Print both.

print("\n" + "=" * 60)
print("TASK 2 — Final accuracy from history")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   final_train_acc = history.history['accuracy'][-1]
#   final_val_acc   = history.history['val_accuracy'][-1]
#   print(f"Final train accuracy: {final_train_acc:.4f}")
#   print(f"Final val accuracy:   {final_val_acc:.4f}")
#   print(f"Overfit gap: {final_train_acc - final_val_acc:.4f}")

# EXPECTED OUTPUT (approximately):
# Final train accuracy: ~0.955
# Final val accuracy:   ~0.940
# Overfit gap: ~0.015

# =============================================================================
# TASK 3 — Plot Training Curves
# =============================================================================
# Create a 2-panel matplotlib figure:
#   Left panel:  Training loss and validation loss per epoch
#   Right panel: Training accuracy and validation accuracy per epoch
# Add legend, grid, axis labels, and title to both panels.

print("\n" + "=" * 60)
print("TASK 3 — Plot loss and accuracy training curves")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
#
#   ax1.plot(history.history['loss'],     label='Train loss')
#   ax1.plot(history.history['val_loss'], label='Val loss')
#   ax1.set_xlabel('Epoch')
#   ax1.set_ylabel('Loss')
#   ax1.set_title('Training vs Validation Loss')
#   ax1.legend()
#   ax1.grid(True, alpha=0.3)
#
#   ax2.plot(history.history['accuracy'],     label='Train accuracy')
#   ax2.plot(history.history['val_accuracy'], label='Val accuracy')
#   ax2.set_xlabel('Epoch')
#   ax2.set_ylabel('Accuracy')
#   ax2.set_title('Training vs Validation Accuracy')
#   ax2.legend()
#   ax2.grid(True, alpha=0.3)
#
#   plt.tight_layout()
#   plt.show()

# =============================================================================
# TASK 4 (BONUS) — Train Longer and Observe Overfitting
# =============================================================================
# Rebuild and recompile the same architecture (fresh random weights).
# Train with epochs=100.
# After training, find the epoch where val_accuracy was highest.
# Print: best_val_epoch, best_val_accuracy, and final_val_accuracy.
# This shows that training beyond the optimum hurts generalisation.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Train for 100 epochs, find when val peaks")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model2 = keras.Sequential([
#       keras.layers.Dense(64, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(32, activation='relu'),
#       keras.layers.Dense(1,  activation='sigmoid')
#   ])
#   model2.compile(optimizer='adam', loss='binary_crossentropy',
#                  metrics=['accuracy'])
#   history2 = model2.fit(X_train, y_train, validation_split=0.2,
#                         epochs=100, batch_size=32, verbose=0)
#   val_accs = history2.history['val_accuracy']
#   best_epoch = int(np.argmax(val_accs)) + 1
#   print(f"Best val accuracy: {max(val_accs):.4f} at epoch {best_epoch}")
#   print(f"Final val accuracy: {val_accs[-1]:.4f}")
#   print(f"Difference (overtraining effect): {max(val_accs) - val_accs[-1]:.4f}")

# EXPECTED OUTPUT (approximately):
# Best val accuracy: ~0.945 at epoch ~15-25
# Final val accuracy: ~0.938
# Difference (overtraining effect): ~0.007

print("\n--- Exercise 3 complete. Move to exercise4_evaluate_and_improve.py ---")
