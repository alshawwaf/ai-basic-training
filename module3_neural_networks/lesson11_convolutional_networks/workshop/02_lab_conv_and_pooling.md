# Lab -- Exercise 2: Conv2D and MaxPooling2D — Filters, Sliding Windows, Downsampling

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_conv_and_pooling.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
```

---

## Step 3: Build Conv2D + MaxPooling2D and Trace Shape Changes

Build a model with just: Input shape: (28, 28, 1) Conv2D(32, (3,3), relu)

Add this to your file:

```python
print("=" * 60)
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
print(f"  After MaxPool: (None, 13, 13, 32)  <- 26/2=13 after 2×2 pooling")
```

Run your file. You should see:
```
conv2d (Conv2D)       (None, 26, 26, 32)    320
max_pooling2d         (None, 13, 13, 32)      0
```

---

## Step 4: Compare Parameter Count: Conv2D vs Dense Equivalent

If we had used a Dense(32) layer on the flattened 28×28 image: Dense(32): 784 × 32 + 32 = 25,120 parameters Our Conv2D(32,(3,3)) uses:

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Conv2D vs Dense parameter count")
print("=" * 60)
conv_params  = 3 * 3 * 1 * 32 + 32   # kernel_h × kernel_w × in_channels × filters + biases
dense_params = 784 * 32 + 32           # flat_input × units + biases
print(f"Conv2D(32,(3,3)) parameters: {conv_params}")
print(f"Dense(32) parameters:        {dense_params}")
print(f"Dense uses {dense_params/conv_params:.0f}× more parameters!")
print(f"Conv2D model count_params(): {model.count_params()}")
```

Run your file. You should see:
```
Conv2D(32,(3,3)) parameters: 320
Dense(32) parameters:        25,120
Dense uses 79× more parameters!
```

---

## Step 5: Visualise One Input Image and Describe What a Filter Looks For

Display the first MNIST test image. Print its pixel values for rows 10-12, columns 10-15 to show a region. Explain conceptually what a 3×3 filter "looks for" when it slides over this region.

Add this to your file:

```python
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
print("A 3×3 filter slides over this image looking for local patterns.")
print("One filter might detect vertical edges: [dark | bright]")
print("Another might detect corners: [dark dark | dark bright]")
print("These filters are LEARNED from the training data — not hand-coded.")
```

---

## Step 6: TASK 4 (BONUS) — Change Kernel Size from (3,3) to (5,5)

Build a new model with Conv2D(32, (5,5)) instead of (3,3). Call model.summary() and compare: - Parameter count (should increase)

Add this to your file:

```python
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
print(f"\n3×3 kernel: output={out_3x3}×{out_3x3}, params={params_3x3}")
print(f"5×5 kernel: output={out_5x5}×{out_5x5}, params={params_5x5}")
print(f"Larger kernel → fewer output positions, more parameters per filter")
```

Run your file. You should see:
```
3×3 kernel: output=26×26, params=320
5×5 kernel: output=24×24, params=832
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_conv_and_pooling.py`) if anything looks different.
