# =============================================================================
# LESSON 3.11 | WORKSHOP | Exercise 2 of 4
# Conv2D and MaxPooling2D — Filters, Sliding Windows, Downsampling
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How Conv2D(filters, kernel_size) slides a filter window across an image
# - How MaxPooling2D(pool_size) downsamples feature maps
# - How to trace shape changes through conv and pooling layers
# - How the parameter count compares between Conv2D and equivalent Dense
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson11_convolutional_networks/workshop/exercise2_conv_and_pooling.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# --- MNIST setup (do not modify) --------------------------------------------
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
X_test  = X_test.reshape(-1,  28, 28, 1).astype('float32') / 255.0
print(f"MNIST loaded. Input shape: {X_train[0].shape}")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Conv2D(32, (3,3), activation='relu'):
#   - Creates 32 filters, each of size 3×3×1 (3×3 spatial, 1 channel for greyscale)
#   - Each filter slides across the image with stride=1 (default)
#   - At each position, the filter computes: sum(filter × patch) + bias
#   - Output size: (28 - 3 + 1) × (28 - 3 + 1) = 26 × 26 per filter → 32 feature maps
#   - Parameter count: 3 × 3 × 1 × 32 + 32 = 320 (MUCH less than Dense!)
#
# MaxPooling2D((2,2)):
#   - Divides each feature map into non-overlapping 2×2 blocks
#   - Takes the maximum value from each block
#   - Halves both spatial dimensions: 26×26 → 13×13
#   - No learnable parameters (just a max operation)
#   - Effect: spatial down-sampling, small translations become invariant
#
# Shape arithmetic (with 'valid' padding, stride=1):
#   output_size = floor((input_size - kernel_size) / stride) + 1
#   After conv:    (28 - 3 + 1) = 26
#   After pooling: 26 / 2 = 13

# =============================================================================
# TASK 1 — Build Conv2D + MaxPooling2D and Trace Shape Changes
# =============================================================================
# Build a model with just:
#   Input shape: (28, 28, 1)
#   Conv2D(32, (3,3), relu)
#   MaxPooling2D((2,2))
# Call model.summary() and trace the output shape at each layer.
# Print the shape manually: what is the output shape after each operation?

print("=" * 60)
print("TASK 1 — Conv2D + MaxPooling2D shape trace")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = keras.Sequential([
#       keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
#       keras.layers.MaxPooling2D((2,2))
#   ])
#   model.summary()
#   print("\nShape trace:")
#   print(f"  Input:         (None, 28, 28, 1)")
#   print(f"  After Conv2D:  (None, 26, 26, 32)  <- (28-3+1)=26 per filter, 32 filters")
#   print(f"  After MaxPool: (None, 13, 13, 32)  <- 26/2=13 after 2×2 pooling")

# EXPECTED OUTPUT (model.summary):
# conv2d (Conv2D)       (None, 26, 26, 32)    320
# max_pooling2d         (None, 13, 13, 32)      0

# =============================================================================
# TASK 2 — Compare Parameter Count: Conv2D vs Dense Equivalent
# =============================================================================
# If we had used a Dense(32) layer on the flattened 28×28 image:
#   Dense(32): 784 × 32 + 32 = 25,120 parameters
# Our Conv2D(32,(3,3)) uses:
#   3 × 3 × 1 × 32 + 32 = 320 parameters
# Print both counts and the ratio.

print("\n" + "=" * 60)
print("TASK 2 — Conv2D vs Dense parameter count")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   conv_params  = 3 * 3 * 1 * 32 + 32   # kernel_h × kernel_w × in_channels × filters + biases
#   dense_params = 784 * 32 + 32           # flat_input × units + biases
#   print(f"Conv2D(32,(3,3)) parameters: {conv_params}")
#   print(f"Dense(32) parameters:        {dense_params}")
#   print(f"Dense uses {dense_params/conv_params:.0f}× more parameters!")
#   print(f"Conv2D model count_params(): {model.count_params()}")

# EXPECTED OUTPUT:
# Conv2D(32,(3,3)) parameters: 320
# Dense(32) parameters:        25,120
# Dense uses 79× more parameters!

# =============================================================================
# TASK 3 — Visualise One Input Image and Describe What a Filter Looks For
# =============================================================================
# Display the first MNIST test image.
# Print its pixel values for rows 10-12, columns 10-15 to show a region.
# Explain conceptually what a 3×3 filter "looks for" when it slides over this region.

print("\n" + "=" * 60)
print("TASK 3 — Visualise image and describe filter purpose")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   sample = X_test[0].squeeze()
#   plt.figure(figsize=(6, 6))
#   plt.imshow(sample, cmap='gray')
#   plt.title(f'MNIST Digit: {y_test[0]}')
#   plt.colorbar()
#   plt.tight_layout()
#   plt.show()
#   print(f"Digit label: {y_test[0]}")
#   print(f"Pixel values at rows 10-12, cols 10-15:")
#   print(sample[10:13, 10:16].round(2))
#   print()
#   print("A 3×3 filter slides over this image looking for local patterns.")
#   print("One filter might detect vertical edges: [dark | bright]")
#   print("Another might detect corners: [dark dark | dark bright]")
#   print("These filters are LEARNED from the training data — not hand-coded.")

# =============================================================================
# TASK 4 (BONUS) — Change Kernel Size from (3,3) to (5,5)
# =============================================================================
# Build a new model with Conv2D(32, (5,5)) instead of (3,3).
# Call model.summary() and compare:
#   - Parameter count (should increase)
#   - Output shape after Conv2D (should be smaller: (24,24,32) not (26,26,32))
# Formula: output = 28 - kernel_size + 1

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare kernel size (3,3) vs (5,5)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_5x5 = keras.Sequential([
#       keras.layers.Conv2D(32, (5,5), activation='relu', input_shape=(28,28,1)),
#       keras.layers.MaxPooling2D((2,2))
#   ])
#   model_5x5.summary()
#   params_3x3 = 3*3*1*32 + 32
#   params_5x5 = 5*5*1*32 + 32
#   out_3x3 = 28 - 3 + 1
#   out_5x5 = 28 - 5 + 1
#   print(f"\n3×3 kernel: output={out_3x3}×{out_3x3}, params={params_3x3}")
#   print(f"5×5 kernel: output={out_5x5}×{out_5x5}, params={params_5x5}")
#   print(f"Larger kernel → fewer output positions, more parameters per filter")

# EXPECTED OUTPUT:
# 3×3 kernel: output=26×26, params=320
# 5×5 kernel: output=24×24, params=832

print("\n--- Exercise 2 complete. Move to exercise3_build_and_train_cnn.py ---")
