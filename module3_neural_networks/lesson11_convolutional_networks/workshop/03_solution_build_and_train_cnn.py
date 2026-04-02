# Exercise 3 — Build and Train a Full CNN on MNIST
#
# Combines two Conv2D+MaxPooling2D blocks with a Dense classifier head.
# Block 1 (32 filters) detects low-level features like edges.
# Block 2 (64 filters) combines those into higher-level patterns.
# The Dense head maps detected patterns to digit probabilities.
#
# Prerequisite: pip install tensorflow matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("EXERCISE 3 — Build and Train a Full CNN on MNIST")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Load MNIST and reshape for CNN input ──────────────────────────────────────
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0

# CNN needs explicit channel dimension: (28, 28) -> (28, 28, 1)
X_train = X_train[..., np.newaxis]
X_test  = X_test[..., np.newaxis]

print(f"Training images: {X_train.shape}")
print(f"Test images:     {X_test.shape}")

# Dense baseline accuracy from Exercise 1 (for comparison)
DENSE_BASELINE_ACC = 0.970

# ── TASK 1 — Build and compile the CNN ────────────────────────────────────────
# Architecture:
#   Conv2D(32) -> Pool -> Conv2D(64) -> Pool -> Flatten -> Dense(128) -> Dense(10)
# Each Conv2D layer learns filters that detect increasingly complex patterns.
# Flatten converts 2D feature maps to a 1D vector for the Dense classifier.
print("\n" + "=" * 60)
print("TASK 1 — Build and compile the CNN")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10,  activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# ── TASK 2 — Train and compare to Dense baseline ─────────────────────────────
# 5 epochs is enough for the CNN to reach ~99% on MNIST.
# The Dense baseline from Exercise 1 reached ~97% in 3 epochs.
# CNN wins because it exploits spatial structure (edges, curves, etc.).
print("\n" + "=" * 60)
print("TASK 2 — Train and compare to Dense baseline")
print("=" * 60)

history = model.fit(X_train, y_train, epochs=5, batch_size=128,
                    validation_split=0.1, verbose=1)

_, cnn_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nCNN test accuracy (5 epochs):   {cnn_acc:.4f}")
print(f"Dense baseline (3 epochs):      {DENSE_BASELINE_ACC:.4f}")
print(f"CNN improvement:                {cnn_acc - DENSE_BASELINE_ACC:+.4f}")

# ── TASK 3 — Plot training curves ────────────────────────────────────────────
# Loss should drop quickly; accuracy should climb toward 99%.
# If val curves track train curves closely, the model is not overfitting.
print("\n" + "=" * 60)
print("TASK 3 — Plot training curves")
print("=" * 60)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(history.history['loss'],     label='Train')
ax1.plot(history.history['val_loss'], label='Val')
ax1.set_title('CNN Training Loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(history.history['accuracy'],     label='Train')
ax2.plot(history.history['val_accuracy'], label='Val')
ax2.set_title('CNN Training Accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.suptitle('CNN on MNIST — Training Curves')
plt.tight_layout()
plt.show()

# ── TASK 4 (BONUS) — 3-conv-layer CNN ────────────────────────────────────────
# Adding a third Conv2D layer lets the network detect even more complex
# combinations of features. On MNIST the improvement is marginal because
# the dataset is already easy, but on harder tasks deeper CNNs help a lot.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — 3-conv-layer CNN")
print("=" * 60)

model_deep = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10,  activation='softmax')
])

model_deep.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
model_deep.fit(X_train, y_train, epochs=5, batch_size=128,
               validation_split=0.1, verbose=0)

_, deep_acc = model_deep.evaluate(X_test, y_test, verbose=0)
print(f"2-conv CNN accuracy: {cnn_acc:.4f}")
print(f"3-conv CNN accuracy: {deep_acc:.4f}")

print("\n--- Exercise 3 complete. Move to 04_solution_malware_visualisation_context.py ---")
