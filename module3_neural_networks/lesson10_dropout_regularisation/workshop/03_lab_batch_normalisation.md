# Lab -- Exercise 3: Batch Normalisation — Stabilise Training, Allow Higher Learning Rates

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise3_batch_normalisation.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

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
print("Dataset ready.")
```

---

## Step 4: Add BatchNormalization After Each Dense Layer

Architecture: Dense(256, relu) → BatchNormalization Dense(256, relu) → BatchNormalization

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Train with BatchNormalization")
print("=" * 60)
model_bn = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1, activation='sigmoid')
])
model_bn.compile(optimizer='adam', loss='binary_crossentropy',
                 metrics=['accuracy'])
history_bn = model_bn.fit(X_train, y_train, validation_split=0.2,
                           epochs=50, batch_size=32, verbose=0)
print(f"Final val_loss: {history_bn.history['val_loss'][-1]:.4f}")
print(f"Final val_acc:  {history_bn.history['val_accuracy'][-1]:.4f}")
```

---

## Step 5: Compare Training Stability (Smoother Loss Curve)

Build a baseline WITHOUT BatchNorm (same architecture, just no BN layers). Plot both training loss curves side by side. The BN version should converge faster and have a smoother curve.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Compare training stability")
print("=" * 60)
model_no_bn = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
model_no_bn.compile(optimizer='adam', loss='binary_crossentropy',
                    metrics=['accuracy'])
history_no_bn = model_no_bn.fit(X_train, y_train, validation_split=0.2,
                                 epochs=50, batch_size=32, verbose=0)
#
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(history_no_bn.history['loss'], label='Train', color='blue')
ax1.plot(history_no_bn.history['val_loss'], label='Val', color='red')
ax1.set_title('No BatchNorm')
ax1.set_xlabel('Epoch'), ax1.set_ylabel('Loss')
ax1.legend(), ax1.grid(True, alpha=0.3)
#
ax2.plot(history_bn.history['loss'], label='Train', color='blue')
ax2.plot(history_bn.history['val_loss'], label='Val', color='red')
ax2.set_title('With BatchNorm')
ax2.set_xlabel('Epoch'), ax2.set_ylabel('Loss')
ax2.legend(), ax2.grid(True, alpha=0.3)
#
plt.suptitle('Training Stability: No BatchNorm vs BatchNorm')
plt.tight_layout()
plt.show()
```

---

## Step 6: Combine BatchNorm + Dropout in One Model

Build the combined architecture: Dense(256, relu) → BatchNorm → Dropout(0.3) Dense(256, relu) → BatchNorm → Dropout(0.3)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Combined BatchNorm + Dropout")
print("=" * 60)
model_combined = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation='sigmoid')
])
model_combined.compile(optimizer='adam', loss='binary_crossentropy',
                        metrics=['accuracy'])
history_combined = model_combined.fit(X_train, y_train, validation_split=0.2,
                                       epochs=50, batch_size=32, verbose=0)
print(f"BatchNorm only  val_acc: {history_bn.history['val_accuracy'][-1]:.4f}")
print(f"Combined BN+DO  val_acc: {history_combined.history['val_accuracy'][-1]:.4f}")
```

---

## Step 7: TASK 4 (BONUS) — Remove BatchNorm from the Middle Layer

Build an asymmetric model: BN on layers 1 and 3 but NOT on layer 2. Train and observe whether the loss at epoch 5-10 shows more noise compared to the fully normalised model. Print the std of the training loss over

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Asymmetric BatchNorm placement")
print("=" * 60)
print("\n--- Exercise 3 complete. Move to exercise4_early_stopping.py ---")
model_asym = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(256, activation='relu'),  # no BN here
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1, activation='sigmoid')
])
model_asym.compile(optimizer='adam', loss='binary_crossentropy',
                   metrics=['accuracy'])
history_asym = model_asym.fit(X_train, y_train, validation_split=0.2,
                               epochs=50, batch_size=32, verbose=0)
loss_full = np.array(history_bn.history['loss'][:20])
loss_asym = np.array(history_asym.history['loss'][:20])
print(f"Full BN train loss std (first 20 epochs): {loss_full.std():.4f}")
print(f"Asymm train loss std (first 20 epochs):   {loss_asym.std():.4f}")
print("(Higher std = noisier training = less stable)")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_batch_normalisation.py`) if anything looks different.
