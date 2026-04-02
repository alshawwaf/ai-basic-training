# Exercise 2 — Conv2D and MaxPooling2D: Filters, Sliding Windows, Downsampling
#
# Conv2D slides small filters (e.g. 3x3) across the image detecting local
# patterns like edges and corners. MaxPooling2D then halves the spatial
# dimensions, keeping the strongest activations. Together they extract
# spatial features with far fewer parameters than Dense.
#
# Prerequisite: pip install tensorflow matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("EXERCISE 2 — Conv2D and MaxPooling2D")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Load MNIST for the visualisation in Task 3 ────────────────────────────────
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0

# ── TASK 1 — Conv2D + MaxPooling2D shape trace ────────────────────────────────
# Build a minimal model: one Conv2D and one MaxPooling2D.
# Conv2D(32,(3,3)): 32 filters, each 3x3, sliding across a 28x28 image.
# Output: (28-3+1)=26 per side, 32 feature maps → (None, 26, 26, 32).
# MaxPooling2D(2,2): takes 2x2 blocks, keeps the max → halves each side.
print("\n" + "=" * 60)
print("TASK 1 — Conv2D + MaxPooling2D shape trace")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2))
])
model.summary()

print("\nShape trace:")
print(f"  Input:         (None, 28, 28, 1)")
print(f"  After Conv2D:  (None, 26, 26, 32)  <- (28-3+1)=26 per filter, 32 filters")
print(f"  After MaxPool: (None, 13, 13, 32)  <- 26/2=13 after 2x2 pooling")

# ── TASK 2 — Conv2D vs Dense parameter count ──────────────────────────────────
# Conv2D reuses the same small filter across all positions (weight sharing).
# Dense connects every input to every output — no sharing at all.
print("\n" + "=" * 60)
print("TASK 2 — Conv2D vs Dense parameter count")
print("=" * 60)

conv_params  = 3 * 3 * 1 * 32 + 32   # kernel_h x kernel_w x in_channels x filters + biases
dense_params = 784 * 32 + 32           # flat_input x units + biases

print(f"Conv2D(32,(3,3)) parameters: {conv_params}")
print(f"Dense(32) parameters:        {dense_params}")
print(f"Dense uses {dense_params/conv_params:.0f}x more parameters!")
print(f"Conv2D model count_params(): {model.count_params()}")

# ── TASK 3 — Visualise image and describe filter purpose ──────────────────────
# Show what a 3x3 region looks like in an actual MNIST digit.
# The filter slides over every such 3x3 patch computing a dot product,
# responding strongly when it finds a matching pattern (edge, corner, etc.).
print("\n" + "=" * 60)
print("TASK 3 — Visualise image and describe filter purpose")
print("=" * 60)

sample = X_test[0].squeeze()
plt.figure(figsize=(6, 6))
plt.imshow(sample, cmap='gray')
plt.title(f'MNIST Digit: {y_test[0]}')
plt.colorbar()
plt.tight_layout()
plt.show()

print(f"Digit label: {y_test[0]}")
print(f"Pixel values at rows 10-12, cols 10-15:")
print(sample[10:13, 10:16].round(2))
print()
print("A 3x3 filter slides over this image looking for local patterns.")
print("One filter might detect vertical edges: [dark | bright]")
print("Another might detect corners: [dark dark | dark bright]")
print("These filters are LEARNED from the training data — not hand-coded.")

# ── TASK 4 (BONUS) — Compare kernel size (3,3) vs (5,5) ──────────────────────
# Larger kernels see more context per position but use more parameters.
# They also produce smaller output maps (fewer valid sliding positions).
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare kernel size (3,3) vs (5,5)")
print("=" * 60)

model_5x5 = keras.Sequential([
    keras.layers.Conv2D(32, (5,5), activation='relu', input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2))
])
model_5x5.summary()

params_3x3 = 3*3*1*32 + 32
params_5x5 = 5*5*1*32 + 32
out_3x3 = 28 - 3 + 1
out_5x5 = 28 - 5 + 1

print(f"\n3x3 kernel: output={out_3x3}x{out_3x3}, params={params_3x3}")
print(f"5x5 kernel: output={out_5x5}x{out_5x5}, params={params_5x5}")
print(f"Larger kernel -> fewer output positions, more parameters per filter")

print("\n--- Exercise 2 complete. Move to ../3_build_and_train_cnn/solve.py ---")
