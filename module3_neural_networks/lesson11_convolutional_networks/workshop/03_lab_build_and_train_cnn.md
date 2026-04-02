# Lab -- Exercise 3: Build and Train a Full CNN on MNIST

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_build_and_train_cnn.py` in this folder.

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

## Step 3: Build and Compile the Full CNN

Build the architecture described above. Compile with: optimizer='adam'

Add this to your file:

```python
print("=" * 60)
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
EXPECTED (model.summary key lines):
conv2d     (None, 26, 26, 32)    320
max_pool   (None, 13, 13, 32)      0
conv2d_1   (None, 11, 11, 64)  18,496
max_pool_1 (None,  5,  5, 64)      0
flatten    (None, 1600)             0
dense      (None, 128)        204,928
dense_1    (None, 10)           1,290
Total params: ~225,034
```

---

## Step 4: Train for 5 Epochs and Compare to Dense Baseline

Train with: epochs=5, batch_size=128, validation_split=0.1 After training, evaluate on X_test and print:

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Train and compare to Dense baseline")
print("=" * 60)
history = model.fit(X_train, y_train, epochs=5, batch_size=128,
                    validation_split=0.1, verbose=1)
_, cnn_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nCNN test accuracy (5 epochs):   {cnn_acc:.4f}")
print(f"Dense baseline (3 epochs):      {DENSE_BASELINE_ACC:.4f}")
print(f"CNN improvement:                {cnn_acc - DENSE_BASELINE_ACC:+.4f}")
```

Run your file. You should see:
```
CNN test accuracy (5 epochs):   ~0.990
Dense baseline (3 epochs):      0.970
CNN improvement:                +0.020
```

---

## Step 5: Plot Training Curves

Create a 2-panel plot: loss (left) and accuracy (right). Each panel shows both train and validation curves.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Plot training curves")
print("=" * 60)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(history.history['loss'],     label='Train')
ax1.plot(history.history['val_loss'], label='Val')
ax1.set_title('CNN Training Loss'), ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss'), ax1.legend(), ax1.grid(True, alpha=0.3)
#
ax2.plot(history.history['accuracy'],     label='Train')
ax2.plot(history.history['val_accuracy'], label='Val')
ax2.set_title('CNN Training Accuracy'), ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy'), ax2.legend(), ax2.grid(True, alpha=0.3)
plt.suptitle('CNN on MNIST — Training Curves')
plt.tight_layout()
plt.show()
```

---

## Step 6: TASK 4 (BONUS) — Add a Third Conv Layer and Compare

Build: Conv(32) → Pool → Conv(64) → Pool → Conv(64) → Flatten → Dense(128) → Dense(10) Train for 5 epochs. Compare test accuracy to the 2-conv model. Note: the third conv layer may have a very small spatial output (or may not fit

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — 3-conv-layer CNN")
print("=" * 60)
print("\n--- Exercise 3 complete. Move to 04_malware_visualisation_context.py ---")
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
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_build_and_train_cnn.py`) if anything looks different.
