# Lab -- Exercise 4: Early Stopping — Automatic Training Termination at the Best Point

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise4_early_stopping.py` in this folder.

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
def build_model():
    """Returns a fresh compiled model (call this before each experiment)."""
    m = keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(10,)),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return m
```

---

## Step 4: Add EarlyStopping Callback

Create an EarlyStopping callback with: monitor='val_loss', patience=5, restore_best_weights=True Pass it to model.fit() via the callbacks argument.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Train with EarlyStopping(patience=5)")
print("=" * 60)
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)
model = build_model()
history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=200,
    batch_size=32,
    callbacks=[early_stop],
    verbose=0
)
actual_epochs = len(history.history['loss'])
print(f"Stopped at epoch: {actual_epochs} out of 200")
print(f"Final val_loss: {history.history['val_loss'][-1]:.4f}")
print(f"Final val_acc:  {history.history['val_accuracy'][-1]:.4f}")
```

Run your file. You should see:
```
Restoring model weights from the end of the best epoch.
Stopped at epoch: ~20-35 (much less than 200)
Final val_loss: ~0.160
Final val_acc:  ~0.945
```

---

## Step 5: Plot Loss Curves Showing Early Stop Point

Plot train_loss and val_loss. Add a vertical dashed line at the epoch where training stopped. Add a marker at the minimum val_loss point.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Plot with early stop marker")
print("=" * 60)
best_epoch = int(np.argmin(history.history['val_loss']))
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'],     label='Train loss', color='blue')
plt.plot(history.history['val_loss'], label='Val loss',   color='red')
plt.axvline(actual_epochs - 1, color='green', linestyle='--',
            label=f'Early stop (epoch {actual_epochs})')
plt.scatter([best_epoch], [history.history['val_loss'][best_epoch]],
            color='gold', s=100, zorder=5, label=f'Best val_loss (epoch {best_epoch+1})')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Early Stopping — Training Halted Automatically')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Step 6: Print How Many Epochs Actually Ran

Without EarlyStopping this would have run 200 epochs. Print: epochs_scheduled, epochs_ran, epochs_saved, and time_saved_estimate. Assume each epoch takes ~0.3 seconds.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Training efficiency report")
print("=" * 60)
epochs_ran   = len(history.history['loss'])
epochs_saved = 200 - epochs_ran
time_saved   = epochs_saved * 0.3
print(f"Scheduled epochs: 200")
print(f"Epochs ran:       {epochs_ran}")
print(f"Epochs saved:     {epochs_saved}")
print(f"Estimated time saved: {time_saved:.1f} seconds")
print(f"(On a large dataset this could save hours of training)")
```

---

## Step 7: TASK 4 (BONUS) — Compare patience=1, patience=5, patience=20

Train three models with different patience values. Record: actual epochs run, final val_accuracy for each. patience=1 stops very aggressively (may stop too early).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare patience values")
print("=" * 60)
print(f"{'Patience':>10} | {'Epochs ran':>10} | {'Val accuracy':>12}")
print("-" * 38)
for p in [1, 5, 20]:
    m = build_model()
    es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=p,
                                       restore_best_weights=True)
    h = m.fit(X_train, y_train, validation_split=0.2, epochs=200,
              batch_size=32, callbacks=[es], verbose=0)
    ep = len(h.history['loss'])
    acc = h.history['val_accuracy'][-1]
    print(f"{p:>10} | {ep:>10} | {acc:>12.4f}")
```

Run your file. You should see:
```
Patience | Epochs ran | Val accuracy
1 |         ~8 |      ~0.930   (stops too early)
5 |        ~25 |      ~0.945   (good balance)
20 |        ~50 |      ~0.943   (allows slight overfit)
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`04_solution_early_stopping.py`) if anything looks different.
