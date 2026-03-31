# =============================================================================
# LESSON 3.11 | WORKSHOP | Exercise 1 of 4
# Why Dense Fails on Images — Spatial Blindness
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why treating image pixels as a flat vector loses spatial information
# - How Dense layers achieve reasonable accuracy on MNIST despite spatial blindness
# - How to count parameters for a Dense baseline and compare to CNN (covered later)
# - Why spatial invariance matters: shuffled pixels still fool a Dense model
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson11_convolutional_networks/workshop/exercise1_why_dense_fails_on_images.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# --- MNIST setup (do not modify) --------------------------------------------
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
X_test  = X_test.reshape(-1,  28, 28, 1).astype('float32') / 255.0
print(f"MNIST loaded: {X_train.shape[0]} train, {X_test.shape[0]} test")
print(f"Image shape: 28×28×1 (height × width × channels)")
# Flatten for Dense models
X_train_flat = X_train.reshape(-1, 784)
X_test_flat  = X_test.reshape(-1, 784)
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# A 28×28 grayscale image has 784 pixels. If we flatten it to a 1D vector,
# a Dense(128) layer creates 784 × 128 + 128 = 100,480 parameters.
# For MNIST (60,000 images), this is manageable.
#
# The fundamental problem: Dense(128) treats pixel at position (0,0) completely
# independently from pixel at position (0,1). It has no concept of "adjacent
# pixels form edges". It must learn from scratch that pixels nearby each other
# tend to co-activate for the same shape.
#
# A Conv2D filter, by contrast, physically slides across the image.
# The same filter (same weights) is applied at every position.
# A filter that detects "horizontal edge" learns ONCE that an edge looks like:
#   [dark, dark, dark]    (one row)
#   [bright, bright, bright]  (next row)
# ...and then detects that pattern EVERYWHERE in the image.
#
# Dense needs 784 × 128 = 100,352 weights to process one image.
# Conv2D(32, (3,3)) needs only 3 × 3 × 1 × 32 = 288 weights — shared across positions.

# =============================================================================
# TASK 1 — Flatten MNIST and Build Dense Baseline
# =============================================================================
# Build a Dense-only model that takes flat 784-pixel input:
#   Flatten (or use pre-flattened X_train_flat)
#   Dense(128, relu)
#   Dense(10, softmax)   ← 10 output units for 10 digit classes
# Compile with adam + sparse_categorical_crossentropy.
# Train for 3 epochs. Print test accuracy.

print("=" * 60)
print("TASK 1 — Dense baseline on flattened MNIST")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_dense = keras.Sequential([
#       keras.layers.Dense(128, activation='relu', input_shape=(784,)),
#       keras.layers.Dense(10,  activation='softmax')
#   ])
#   model_dense.compile(optimizer='adam',
#                       loss='sparse_categorical_crossentropy',
#                       metrics=['accuracy'])
#   model_dense.fit(X_train_flat, y_train, epochs=3, batch_size=128, verbose=1,
#                   validation_split=0.1)
#   _, dense_acc = model_dense.evaluate(X_test_flat, y_test, verbose=0)
#   print(f"\nDense baseline test accuracy (3 epochs): {dense_acc:.4f}")

# EXPECTED OUTPUT (approximately):
# Dense baseline test accuracy (3 epochs): ~0.970

# =============================================================================
# TASK 2 — Count Parameters in Dense Baseline
# =============================================================================
# Print the parameter count for the Dense model using model.summary().
# Manually calculate: (784 × 128) + 128 + (128 × 10) + 10 = ?
# This is the "cost" of not sharing weights spatially.

print("\n" + "=" * 60)
print("TASK 2 — Dense model parameter count")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_dense.summary()
#   l1 = 784 * 128 + 128
#   l2 = 128 * 10  + 10
#   print(f"\nManual calculation: {l1} + {l2} = {l1+l2} parameters")
#   print(f"model.count_params(): {model_dense.count_params()}")

# EXPECTED OUTPUT:
# Layer 1: 100,480 params
# Layer 2:   1,290 params
# Total:   101,770 params

# =============================================================================
# TASK 3 — Visualise a Flattened Image
# =============================================================================
# Take the first training image (X_train[0], shape 28×28×1).
# Display it as a 28×28 grid (its natural form).
# Also display its flattened version as a 1D bar chart.
# This illustrates what Dense "sees" — just a sequence of pixel values.

print("\n" + "=" * 60)
print("TASK 3 — Original 28×28 vs flattened 1D view")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
#
#   ax1.imshow(X_train[0].squeeze(), cmap='gray')
#   ax1.set_title('Image as 28×28 grid\n(CNN sees this — spatial structure intact)')
#   ax1.axis('off')
#
#   ax2.bar(range(784), X_train_flat[0], width=1, color='steelblue', alpha=0.7)
#   ax2.set_title('Image as 784 flat pixels\n(Dense sees this — no spatial structure)')
#   ax2.set_xlabel('Pixel index (0-783)')
#   ax2.set_ylabel('Pixel value (0-1)')
#   ax2.set_xlim(0, 784)
#
#   plt.tight_layout()
#   plt.show()
#   print(f"Flattened shape: {X_train_flat[0].shape}")
#   print("Dense learns: 'pixel 401 correlates with label 3'")
#   print("CNN learns:   'a horizontal edge at row 14 correlates with label 3'")

# =============================================================================
# TASK 4 (BONUS) — Shuffle Pixels and Test Dense Accuracy
# =============================================================================
# Create a fixed pixel permutation and apply it to all images.
# (This completely destroys spatial structure — edges are shattered.)
# Retrain the Dense model on shuffled images.
# Remarkably, the Dense model STILL gets similar accuracy on shuffled data!
# This proves Dense has NO spatial awareness — it just learns pixel correlations.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Dense model survives pixel shuffle")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   perm = np.random.permutation(784)
#   X_train_shuffled = X_train_flat[:, perm]
#   X_test_shuffled  = X_test_flat[:, perm]
#   model_shuffled = keras.Sequential([
#       keras.layers.Dense(128, activation='relu', input_shape=(784,)),
#       keras.layers.Dense(10,  activation='softmax')
#   ])
#   model_shuffled.compile(optimizer='adam',
#                          loss='sparse_categorical_crossentropy',
#                          metrics=['accuracy'])
#   model_shuffled.fit(X_train_shuffled, y_train, epochs=3, batch_size=128,
#                      verbose=0, validation_split=0.1)
#   _, shuffled_acc = model_shuffled.evaluate(X_test_shuffled, y_test, verbose=0)
#   print(f"Dense on normal pixels:   {dense_acc:.4f}")
#   print(f"Dense on shuffled pixels: {shuffled_acc:.4f}")
#   print("The accuracy is similar — Dense does NOT use spatial structure!")
#   print("A CNN trained on shuffled pixels would fail completely.")

print("\n--- Exercise 1 complete. Move to exercise2_conv_and_pooling.py ---")
