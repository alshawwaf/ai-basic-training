# Exercise 1 — Why Dense Fails on Images
#
# Flattening a 28x28 image to 784 pixels destroys spatial structure.
# Dense layers still get ~97% on MNIST because the dataset is easy,
# but they use massive parameter counts and have zero spatial awareness.
# The proof: shuffling all pixels randomly barely changes Dense accuracy.
#
# Prerequisite: pip install tensorflow matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("EXERCISE 1 — Why Dense Fails on Images")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Load MNIST ───────────────────────────────────────────────────────────────────
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Normalise pixel values from 0-255 to 0-1 (helps gradient-based training)
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0

print(f"Training images: {X_train.shape}  (60000 images, 28x28 pixels)")
print(f"Test images:     {X_test.shape}")
print(f"Classes:         {np.unique(y_train)}  (digits 0-9)")

# Flatten to 1D vectors for Dense input
# Dense has no concept of 2D structure — it sees 784 independent numbers
X_train_flat = X_train.reshape(-1, 784)   # (60000, 784)
X_test_flat  = X_test.reshape(-1, 784)    # (10000, 784)

# ── TASK 1 — Build and Train Dense Baseline ─────────────────────────────────────
# Dense(128, relu) → Dense(10, softmax) on flat 784-pixel input.
# 10 outputs with softmax = one probability per digit class, summing to 1.0.
print("\n" + "=" * 60)
print("TASK 1 — Build and Train Dense Baseline")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_dense = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10,  activation='softmax')    # 10 digit classes
], name='dense_baseline')

# sparse_categorical_crossentropy: integer labels (0-9), not one-hot
model_dense.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train for just 3 epochs — Dense learns fast on MNIST
model_dense.fit(X_train_flat, y_train, epochs=3, batch_size=128,
                validation_split=0.1, verbose=1)

_, dense_acc = model_dense.evaluate(X_test_flat, y_test, verbose=0)
print(f"\nDense baseline test accuracy (3 epochs): {dense_acc:.4f}")

# ── TASK 2 — Count Dense Parameters ─────────────────────────────────────────────
# (784 x 128) + 128 = 100,480 parameters in the first layer alone.
# This massive count is the cost of not using spatial structure.
print("\n" + "=" * 60)
print("TASK 2 — Count Dense Parameters")
print("=" * 60)

model_dense.summary()

# Manual verification
l1_params = (784 * 128) + 128   # 100,480
l2_params = (128 * 10) + 10     #   1,290
total     = l1_params + l2_params

print(f"\nManual calculation:")
print(f"  Dense(128): (784 x 128) + 128 = {l1_params:,}")
print(f"  Dense(10):  (128 x 10)  + 10  = {l2_params:,}")
print(f"  Total:                          {total:,}")
print(f"  Keras reports:                  {model_dense.count_params():,}")
print(f"  Match: {total == model_dense.count_params()}")

# ── TASK 3 — Visualise the Two Representations ──────────────────────────────────
# Plot one image as a 28x28 grid (what a human sees) and as a flat bar chart
# (what Dense sees). This makes concrete why Dense misses spatial structure.
print("\n" + "=" * 60)
print("TASK 3 — Visualise the Two Representations")
print("=" * 60)

sample_idx = 0
sample_image = X_test[sample_idx]          # 28x28
sample_flat  = X_test_flat[sample_idx]     # 784

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# Left: 2D image — spatial structure visible
axes[0].imshow(sample_image, cmap='gray')
axes[0].set_title(f'28x28 Image (digit: {y_test[sample_idx]})')
axes[0].axis('off')

# Right: flat vector — just 784 numbers, no spatial meaning
axes[1].bar(range(784), sample_flat, width=1.0, color='steelblue')
axes[1].set_xlabel('Pixel Index (0-783)')
axes[1].set_ylabel('Pixel Value')
axes[1].set_title('Flattened to 784 Values (what Dense sees)')

plt.tight_layout()
plt.savefig('lesson11_ex1_dense_vs_spatial.png')
plt.show()
print("Plot saved to lesson11_ex1_dense_vs_spatial.png")
print("Dense sees the right plot — 784 numbers with no spatial relationship.")

# ── TASK 4 (BONUS) — Shuffle Pixels ─────────────────────────────────────────────
# Apply a random permutation to all pixels (same permutation for train + test).
# Dense accuracy barely changes — proving it has zero spatial awareness.
# A CNN trained on shuffled data would fail badly because filter patterns break.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Shuffle Pixels")
print("=" * 60)

# Create a fixed random permutation of pixel indices
perm = np.random.permutation(784)

# Apply the same permutation to every image
X_train_shuffled = X_train_flat[:, perm]
X_test_shuffled  = X_test_flat[:, perm]

np.random.seed(42)
tf.random.set_seed(42)

# Train a fresh Dense model on shuffled pixels
model_shuffled = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10,  activation='softmax')
], name='dense_shuffled')

model_shuffled.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_shuffled.fit(X_train_shuffled, y_train, epochs=3, batch_size=128,
                   validation_split=0.1, verbose=0)

_, shuffled_acc = model_shuffled.evaluate(X_test_shuffled, y_test, verbose=0)

print(f"Dense on normal pixels:   {dense_acc:.4f}")
print(f"Dense on shuffled pixels: {shuffled_acc:.4f}")
print(f"Difference:               {abs(dense_acc - shuffled_acc):.4f}")
print("Nearly identical — Dense truly has no spatial awareness.")
print("Pixel positions are arbitrary to it.")

print("\n--- Exercise 1 complete. Move to ../2_conv_and_pooling/solve.py ---")
