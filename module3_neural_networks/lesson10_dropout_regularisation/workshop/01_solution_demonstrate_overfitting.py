# Exercise 1 — Demonstrate Overfitting
#
# Shows how a model with too much capacity relative to the training
# data memorises noise instead of learning real patterns. The signature
# is diverging train/val loss curves.
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
print("EXERCISE 1 — Demonstrate Overfitting")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup ────────────────────────────────────────────────────────────────
# 8000 samples, 15 features, 8% attacks — more imbalanced than lesson 9
X, y = make_classification(
    n_samples=8000, n_features=15, n_informative=10, n_redundant=3,
    weights=[0.92, 0.08], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

input_dim = X_train_s.shape[1]
print(f"Training samples: {len(X_train)} | Input features: {input_dim}")
print(f"Attack rate: {y.mean()*100:.1f}%")

# ── TASK 1 — Build and Train the Large Network ──────────────────────────────────
# 3 x Dense(256) = ~133k parameters trained on ~5,100 samples (after val split).
# That is ~26 parameters per sample — the model has enough capacity to
# memorise every training example, including random noise.
print("\n" + "=" * 60)
print("TASK 1 — Build and Train the Large Network (3 x Dense(256))")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
], name='large_no_regularisation')

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(f"Total parameters: {model.count_params():,}")

# Train for 50 epochs — enough to see clear divergence
history = model.fit(
    X_train_s, y_train,
    epochs=50,
    batch_size=64,
    validation_split=0.15,
    verbose=0
)

final_train_acc = history.history['accuracy'][-1]
final_val_acc   = history.history['val_accuracy'][-1]
print(f"Final train accuracy: {final_train_acc:.4f}")
print(f"Final val accuracy:   {final_val_acc:.4f}")

# ── TASK 2 — Plot the Diverging Curves ───────────────────────────────────────────
# In a healthy run, train and val loss track each other.
# Here, val_loss starts rising after ~10-20 epochs while train_loss keeps falling.
# This divergence IS the overfitting signal.
print("\n" + "=" * 60)
print("TASK 2 — Plot the Diverging Curves")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history.history['loss'],     label='Train loss')
axes[0].plot(history.history['val_loss'], label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Train vs Val Loss — Overfitting Signature')
axes[0].legend()

axes[1].plot(history.history['accuracy'],     label='Train accuracy')
axes[1].plot(history.history['val_accuracy'], label='Val accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Train vs Val Accuracy')
axes[1].legend()

plt.tight_layout()
plt.savefig('lesson10_ex1_overfitting.png')
plt.show()
print("Plot saved to lesson10_ex1_overfitting.png")

# ── TASK 3 — Measure the Gap ────────────────────────────────────────────────────
# Accuracy gap > 0.03 is significant. Loss gap > 0.05 is clearly overfitting.
# These numbers become your baseline to compare against in exercises 2-4.
print("\n" + "=" * 60)
print("TASK 3 — Measure the Gap")
print("=" * 60)

acc_gap  = final_train_acc - final_val_acc
loss_gap = history.history['val_loss'][-1] - history.history['loss'][-1]

print(f"Train accuracy:  {final_train_acc:.4f}  | Val accuracy:  {final_val_acc:.4f}")
print(f"Accuracy gap (train - val): {acc_gap:.4f}")
print(f"Loss gap (val - train):     {loss_gap:.4f}")

if acc_gap > 0.03:
    print("Accuracy gap > 0.03 — significant overfitting detected.")
if loss_gap > 0.05:
    print("Loss gap > 0.05 — model is clearly overfitting.")

# ── TASK 4 (BONUS) — More Depth = More Overfit ──────────────────────────────────
# Adding 2 more Dense(256) layers (5 total) increases capacity further.
# With no regularisation, deeper = more memorisation = worse generalisation.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — More Depth = More Overfit (5 x Dense(256))")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_deep = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
], name='deeper_no_regularisation')

model_deep.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(f"Total parameters (5-layer): {model_deep.count_params():,}")

history_deep = model_deep.fit(
    X_train_s, y_train,
    epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

deep_train_acc = history_deep.history['accuracy'][-1]
deep_val_acc   = history_deep.history['val_accuracy'][-1]
deep_gap       = deep_train_acc - deep_val_acc

print(f"3-layer accuracy gap: {acc_gap:.4f}")
print(f"5-layer accuracy gap: {deep_gap:.4f}")
print("Deeper without regularisation = worse generalisation gap.")

print("\n--- Exercise 1 complete. Move to 02_solution_add_dropout.py ---")
