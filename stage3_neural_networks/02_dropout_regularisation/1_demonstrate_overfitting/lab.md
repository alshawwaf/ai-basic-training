# Lab -- Exercise 1: Demonstrate Overfitting — Large Unregularised Network

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_demonstrate_overfitting.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)
print(f"Training samples: {X_train.shape[0]}")
```

---

## Step 4: Build and Train a Large Unregularised Network

Build this architecture (no Dropout, no BatchNorm, no regularisation): Dense(256, relu) → Dense(256, relu) → Dense(256, relu) → Dense(1, sigmoid) Compile with adam + binary_crossentropy.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Large network, 50 epochs, no regularisation")
print("=" * 60)
model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
print(f"Total parameters: {model.count_params():,}")
history = model.fit(X_train, y_train, validation_split=0.2,
                    epochs=50, batch_size=32, verbose=0)
print(f"Final train accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final val accuracy:   {history.history['val_accuracy'][-1]:.4f}")
```

Run your file. You should see:
```
Total parameters: ~133,633
Final train accuracy: ~0.985+
Final val accuracy:   ~0.940
```

---

## Step 5: Plot Diverging Train vs Val Loss

Plot training loss and validation loss on the same graph. The divergence (val loss rising while train loss keeps falling) is the visual signature of overfitting. Add a title, axis labels, legend, and grid.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Plot diverging loss curves")
print("=" * 60)
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'],     label='Train loss',      color='blue')
plt.plot(history.history['val_loss'], label='Validation loss', color='red')
plt.xlabel('Epoch')
plt.ylabel('Loss (binary crossentropy)')
plt.title('Overfitting: Train vs Validation Loss (No Regularisation)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Step 6: Measure the Overfitting Gap at Epoch 50

Compute and print: - Final train loss and train accuracy - Final val loss and val accuracy

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Measure overfitting gap")
print("=" * 60)
train_acc = history.history['accuracy'][-1]
val_acc   = history.history['val_accuracy'][-1]
train_loss = history.history['loss'][-1]
val_loss   = history.history['val_loss'][-1]
print(f"Train accuracy:  {train_acc:.4f}  | Val accuracy:  {val_acc:.4f}")
print(f"Train loss:      {train_loss:.4f}  | Val loss:      {val_loss:.4f}")
print(f"Accuracy gap (train - val): {train_acc - val_acc:.4f}")
print(f"Loss gap (val - train):     {val_loss - train_loss:.4f}")
```

Run your file. You should see:
```
Train accuracy:  ~0.990+  | Val accuracy:  ~0.938
Accuracy gap (train - val): ~0.050+
Loss gap (val - train):     ~0.100+
```

---

## Step 7: TASK 4 (BONUS) — Add Even More Layers and Watch It Get Worse

Build a deeper network: 5 Dense(256) layers instead of 3. Train for 50 epochs. Compare the final overfitting gap to Task 3. The deeper model should show an even larger gap.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Even deeper network, bigger overfit")
print("=" * 60)
print("\n--- Exercise 1 complete. Move to 02_add_dropout.py ---")
model_deep = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
])
model_deep.compile(optimizer='adam', loss='binary_crossentropy',
                   metrics=['accuracy'])
hist_deep = model_deep.fit(X_train, y_train, validation_split=0.2,
                            epochs=50, batch_size=32, verbose=0)
gap_original = (history.history['accuracy'][-1] -
                history.history['val_accuracy'][-1])
gap_deep     = (hist_deep.history['accuracy'][-1] -
                hist_deep.history['val_accuracy'][-1])
print(f"3-layer gap: {gap_original:.4f}")
print(f"5-layer gap: {gap_deep:.4f}  (deeper → more overfit)")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
