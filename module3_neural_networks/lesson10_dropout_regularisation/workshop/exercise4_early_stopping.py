# =============================================================================
# LESSON 3.10 | WORKSHOP | Exercise 4 of 4
# Early Stopping — Automatic Training Termination at the Best Point
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How EarlyStopping monitors val_loss and stops when it stops improving
# - How patience controls the number of non-improving epochs before stopping
# - How restore_best_weights resets the model to its best state automatically
# - How patience value affects the stop point and final model quality
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson10_dropout_regularisation/workshop/exercise4_early_stopping.py
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

def build_model():
    """Returns a fresh compiled model (call this before each experiment)."""
    m = keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(10,)),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return m
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# EarlyStopping is a Keras callback — a function called automatically at the
# end of each epoch. When the monitored metric stops improving, it stops training.
#
# Key parameters:
#   monitor='val_loss'      — which metric to watch (always monitor val, not train)
#   patience=5              — how many epochs of no improvement before stopping
#   restore_best_weights=True — resets weights to the epoch with the best val_loss
#   min_delta=0.001         — minimum improvement to count as "improving"
#   mode='min'              — inferred automatically (min for loss, max for accuracy)
#
# Without restore_best_weights=True: the model has the weights from the LAST epoch,
# which may be worse than the best epoch.
# With restore_best_weights=True: the model has the BEST weights after training.
#
# How many epochs actually ran is available at:
#   len(history.history['loss'])
#   OR history.epoch[-1] + 1

# =============================================================================
# TASK 1 — Add EarlyStopping Callback
# =============================================================================
# Create an EarlyStopping callback with:
#   monitor='val_loss', patience=5, restore_best_weights=True
# Pass it to model.fit() via the callbacks argument.
# Set epochs=200 (we want the callback to stop it early).
# Print how many epochs actually ran.

print("=" * 60)
print("TASK 1 — Train with EarlyStopping(patience=5)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   early_stop = keras.callbacks.EarlyStopping(
#       monitor='val_loss',
#       patience=5,
#       restore_best_weights=True,
#       verbose=1
#   )
#   model = build_model()
#   history = model.fit(
#       X_train, y_train,
#       validation_split=0.2,
#       epochs=200,
#       batch_size=32,
#       callbacks=[early_stop],
#       verbose=0
#   )
#   actual_epochs = len(history.history['loss'])
#   print(f"Stopped at epoch: {actual_epochs} out of 200")
#   print(f"Final val_loss: {history.history['val_loss'][-1]:.4f}")
#   print(f"Final val_acc:  {history.history['val_accuracy'][-1]:.4f}")

# EXPECTED OUTPUT (approximately):
# Restoring model weights from the end of the best epoch.
# Stopped at epoch: ~20-35 (much less than 200)
# Final val_loss: ~0.160
# Final val_acc:  ~0.945

# =============================================================================
# TASK 2 — Plot Loss Curves Showing Early Stop Point
# =============================================================================
# Plot train_loss and val_loss.
# Add a vertical dashed line at the epoch where training stopped.
# Add a marker at the minimum val_loss point.

print("\n" + "=" * 60)
print("TASK 2 — Plot with early stop marker")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   best_epoch = int(np.argmin(history.history['val_loss']))
#   plt.figure(figsize=(10, 5))
#   plt.plot(history.history['loss'],     label='Train loss', color='blue')
#   plt.plot(history.history['val_loss'], label='Val loss',   color='red')
#   plt.axvline(actual_epochs - 1, color='green', linestyle='--',
#               label=f'Early stop (epoch {actual_epochs})')
#   plt.scatter([best_epoch], [history.history['val_loss'][best_epoch]],
#               color='gold', s=100, zorder=5, label=f'Best val_loss (epoch {best_epoch+1})')
#   plt.xlabel('Epoch')
#   plt.ylabel('Loss')
#   plt.title('Early Stopping — Training Halted Automatically')
#   plt.legend()
#   plt.grid(True, alpha=0.3)
#   plt.tight_layout()
#   plt.show()

# =============================================================================
# TASK 3 — Print How Many Epochs Actually Ran
# =============================================================================
# Without EarlyStopping this would have run 200 epochs.
# Print: epochs_scheduled, epochs_ran, epochs_saved, and time_saved_estimate.
# Assume each epoch takes ~0.3 seconds.

print("\n" + "=" * 60)
print("TASK 3 — Training efficiency report")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   epochs_ran   = len(history.history['loss'])
#   epochs_saved = 200 - epochs_ran
#   time_saved   = epochs_saved * 0.3
#   print(f"Scheduled epochs: 200")
#   print(f"Epochs ran:       {epochs_ran}")
#   print(f"Epochs saved:     {epochs_saved}")
#   print(f"Estimated time saved: {time_saved:.1f} seconds")
#   print(f"(On a large dataset this could save hours of training)")

# =============================================================================
# TASK 4 (BONUS) — Compare patience=1, patience=5, patience=20
# =============================================================================
# Train three models with different patience values.
# Record: actual epochs run, final val_accuracy for each.
# patience=1 stops very aggressively (may stop too early).
# patience=20 is lenient (may allow some overfitting).
# Print a comparison table.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare patience values")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print(f"{'Patience':>10} | {'Epochs ran':>10} | {'Val accuracy':>12}")
#   print("-" * 38)
#   for p in [1, 5, 20]:
#       m = build_model()
#       es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=p,
#                                          restore_best_weights=True)
#       h = m.fit(X_train, y_train, validation_split=0.2, epochs=200,
#                 batch_size=32, callbacks=[es], verbose=0)
#       ep = len(h.history['loss'])
#       acc = h.history['val_accuracy'][-1]
#       print(f"{p:>10} | {ep:>10} | {acc:>12.4f}")

# EXPECTED OUTPUT (approximately):
#   Patience | Epochs ran | Val accuracy
#          1 |         ~8 |      ~0.930   (stops too early)
#          5 |        ~25 |      ~0.945   (good balance)
#         20 |        ~50 |      ~0.943   (allows slight overfit)

print("\n--- Workshop complete. Open reference_solution.py ---")
