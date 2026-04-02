# Lab -- Exercise 1: Why Dense Fails on Images — Spatial Blindness

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_why_dense_fails_on_images.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
```

---

## Step 3: Flatten MNIST and Build Dense Baseline

Build a Dense-only model that takes flat 784-pixel input: Flatten (or use pre-flattened X_train_flat) Dense(128, relu)

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Dense baseline on flattened MNIST")
print("=" * 60)
model_dense = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10,  activation='softmax')
])
model_dense.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
model_dense.fit(X_train_flat, y_train, epochs=3, batch_size=128, verbose=1,
                validation_split=0.1)
_, dense_acc = model_dense.evaluate(X_test_flat, y_test, verbose=0)
print(f"\nDense baseline test accuracy (3 epochs): {dense_acc:.4f}")
```

Run your file. You should see:
```
Dense baseline test accuracy (3 epochs): ~0.970
```

---

## Step 4: Count Parameters in Dense Baseline

Print the parameter count for the Dense model using model.summary(). Manually calculate: (784 × 128) + 128 + (128 × 10) + 10 = ? This is the "cost" of not sharing weights spatially.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Dense model parameter count")
print("=" * 60)
model_dense.summary()
l1 = 784 * 128 + 128
l2 = 128 * 10  + 10
print(f"\nManual calculation: {l1} + {l2} = {l1+l2} parameters")
print(f"model.count_params(): {model_dense.count_params()}")
```

Run your file. You should see:
```
Layer 1: 100,480 params
Layer 2:   1,290 params
Total:   101,770 params
```

---

## Step 5: Visualise a Flattened Image

Take the first training image (X_train[0], shape 28×28×1). Display it as a 28×28 grid (its natural form). Also display its flattened version as a 1D bar chart.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Original 28×28 vs flattened 1D view")
print("=" * 60)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
#
ax1.imshow(X_train[0].squeeze(), cmap='gray')
ax1.set_title('Image as 28×28 grid\n(CNN sees this — spatial structure intact)')
ax1.axis('off')
#
ax2.bar(range(784), X_train_flat[0], width=1, color='steelblue', alpha=0.7)
ax2.set_title('Image as 784 flat pixels\n(Dense sees this — no spatial structure)')
ax2.set_xlabel('Pixel index (0-783)')
ax2.set_ylabel('Pixel value (0-1)')
ax2.set_xlim(0, 784)
#
plt.tight_layout()
plt.show()
print(f"Flattened shape: {X_train_flat[0].shape}")
print("Dense learns: 'pixel 401 correlates with label 3'")
print("CNN learns:   'a horizontal edge at row 14 correlates with label 3'")
```

---

## Step 6: TASK 4 (BONUS) — Shuffle Pixels and Test Dense Accuracy

Create a fixed pixel permutation and apply it to all images. (This completely destroys spatial structure — edges are shattered.) Retrain the Dense model on shuffled images.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Dense model survives pixel shuffle")
print("=" * 60)
print("\n--- Exercise 1 complete. Move to 02_conv_and_pooling.py ---")
perm = np.random.permutation(784)
X_train_shuffled = X_train_flat[:, perm]
X_test_shuffled  = X_test_flat[:, perm]
model_shuffled = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10,  activation='softmax')
])
model_shuffled.compile(optimizer='adam',
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])
model_shuffled.fit(X_train_shuffled, y_train, epochs=3, batch_size=128,
                   verbose=0, validation_split=0.1)
_, shuffled_acc = model_shuffled.evaluate(X_test_shuffled, y_test, verbose=0)
print(f"Dense on normal pixels:   {dense_acc:.4f}")
print(f"Dense on shuffled pixels: {shuffled_acc:.4f}")
print("The accuracy is similar — Dense does NOT use spatial structure!")
print("A CNN trained on shuffled pixels would fail completely.")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
