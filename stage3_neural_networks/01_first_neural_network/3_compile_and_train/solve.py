# Exercise 3 — Compile and Train
#
# Demonstrates the training loop (model.fit), the history object,
# and how to interpret training vs validation curves to detect
# overfitting vs underfitting.
#
# Prerequisite: pip install tensorflow scikit-learn matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 3 — Compile and Train")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup (same as exercise 2) ───────────────────────────────────────────
X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=7, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print(f"Training samples: {len(X_train)} | Test samples: {len(X_test)}")

# ── Build and compile the model (same architecture as exercise 2) ────────────────
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ── TASK 1 — Train for 20 Epochs ────────────────────────────────────────────────
# model.fit() runs the full training loop:
#   For each epoch → shuffle → for each batch → forward → loss → backward → update
# validation_split=0.2: last 20% of X_train held out for validation each epoch
# batch_size=32: 32 samples per gradient update
print("\n" + "=" * 60)
print("TASK 1 — Train for 20 Epochs")
print("=" * 60)

history = model.fit(
    X_train_s, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,   # reserve 20% of training data for validation
    verbose=1               # show per-epoch progress
)

# ── TASK 2 — Extract Final Accuracy ─────────────────────────────────────────────
# history.history is a dict with keys: 'loss', 'accuracy', 'val_loss', 'val_accuracy'
# Each value is a list with one entry per epoch
print("\n" + "=" * 60)
print("TASK 2 — Extract Final Accuracy")
print("=" * 60)

final_train_acc = history.history['accuracy'][-1]
final_val_acc   = history.history['val_accuracy'][-1]
gap = final_train_acc - final_val_acc

print(f"Final train accuracy: {final_train_acc:.4f}")
print(f"Final val accuracy:   {final_val_acc:.4f}")
print(f"Overfit gap:          {gap:.4f}")

# A gap below ~0.02 usually means the model is not significantly overfitting
if gap < 0.02:
    print("Gap is small — model is generalising well.")
elif gap < 0.05:
    print("Gap is moderate — some overfitting, consider regularisation.")
else:
    print("Gap is large — model is overfitting. Add dropout or reduce capacity.")

# ── TASK 3 — Plot Training Curves ───────────────────────────────────────────────
# Side-by-side plots of loss and accuracy, each showing train vs validation.
# Healthy model: both curves converge and track each other closely.
# Overfitting: train keeps improving, val stalls or worsens.
print("\n" + "=" * 60)
print("TASK 3 — Plot Training Curves")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left panel: loss curves
axes[0].plot(history.history['loss'],     label='Train loss')
axes[0].plot(history.history['val_loss'], label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Training & Validation Loss')
axes[0].legend()

# Right panel: accuracy curves
axes[1].plot(history.history['accuracy'],     label='Train accuracy')
axes[1].plot(history.history['val_accuracy'], label='Val accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Training & Validation Accuracy')
axes[1].legend()

plt.tight_layout()
plt.savefig('lesson9_ex3_training_curves.png')
plt.show()
print("Plot saved to lesson9_ex3_training_curves.png")

# ── TASK 4 (BONUS) — Train Longer and Find the Peak ─────────────────────────────
# Training for 100 epochs to see if val accuracy peaks before epoch 100.
# np.argmax finds the epoch with the highest val accuracy.
# The difference between peak and final epoch accuracy = cost of overtraining.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Train Longer and Find the Peak")
print("=" * 60)

# Build a fresh model (reusing a trained model would continue from where it left off)
np.random.seed(42)
tf.random.set_seed(42)

model_long = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model_long.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history_long = model_long.fit(
    X_train_s, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

val_accs = history_long.history['val_accuracy']
best_epoch = int(np.argmax(val_accs)) + 1   # +1 because epochs are 1-indexed
best_val   = val_accs[best_epoch - 1]
final_val  = val_accs[-1]

print(f"Best val accuracy:  {best_val:.4f} at epoch {best_epoch}")
print(f"Final val accuracy: {final_val:.4f} at epoch 100")
print(f"Overtraining cost:  {best_val - final_val:.4f}")
print("(Training beyond the peak epoch gradually overfits.)")

print("\n--- Exercise 3 complete. Move to ../4_evaluate_and_improve/solve.py ---")
