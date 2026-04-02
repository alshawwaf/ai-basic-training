# Lab -- Exercise 2: Add Dropout — Regularise by Random Neuron Silencing

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_add_dropout.py` in this folder.

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
_m_base = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
_m_base.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
_base_history = _m_base.fit(X_train, y_train, validation_split=0.2,
                             epochs=50, batch_size=32, verbose=0)
BASE_VAL_LOSS = _base_history.history['val_loss'][-1]
BASE_VAL_ACC  = _base_history.history['val_accuracy'][-1]
print(f"Baseline (no dropout) — val_loss: {BASE_VAL_LOSS:.4f}, "
      f"val_acc: {BASE_VAL_ACC:.4f}")
```

---

## Step 4: Add Dropout(0.3) After Each Dense Layer

Rebuild the same architecture as Exercise 1 but add Dropout(0.3) after EACH Dense layer (except the output layer): Dense(256, relu) → Dropout(0.3) → Dense(256, relu) → Dropout(0.3)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 1 — Train with Dropout(0.3)")
print("=" * 60)
model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(10,)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
history = model.fit(X_train, y_train, validation_split=0.2,
                    epochs=50, batch_size=32, verbose=0)
val_loss_dropout = history.history['val_loss'][-1]
val_acc_dropout  = history.history['val_accuracy'][-1]
print(f"With Dropout(0.3): val_loss={val_loss_dropout:.4f}, "
      f"val_acc={val_acc_dropout:.4f}")
```

Run your file. You should see:
```
With Dropout(0.3): val_loss=~0.16, val_acc=~0.945
(val_loss lower than baseline ~0.22, val_acc higher than baseline ~0.938)
```

---

## Step 5: Compare Val Loss: Baseline vs Dropout

Plot the val_loss curves for both models on the same graph. The Dropout model's val_loss should be lower and less variable. Also print the improvement numerically.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Compare val loss baseline vs dropout")
print("=" * 60)
plt.figure(figsize=(10, 5))
plt.plot(_base_history.history['val_loss'], label='No dropout', color='red',
         alpha=0.7)
plt.plot(history.history['val_loss'], label='Dropout(0.3)', color='green',
         alpha=0.7)
plt.xlabel('Epoch')
plt.ylabel('Validation Loss')
plt.title('Val Loss: No Dropout vs Dropout(0.3)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
print(f"Baseline val_loss:   {BASE_VAL_LOSS:.4f}")
print(f"Dropout val_loss:    {val_loss_dropout:.4f}")
print(f"Improvement:         {BASE_VAL_LOSS - val_loss_dropout:.4f}")
```

---

## Step 6: Try dropout_rate=0.1 vs dropout_rate=0.5

Train two more models with different dropout rates. Record the final val_accuracy for each rate. Print a summary table: rate → val_accuracy.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Compare dropout rates 0.1 vs 0.3 vs 0.5")
print("=" * 60)
results = {}
for rate in [0.1, 0.3, 0.5]:
    m = keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(10,)),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
    h = m.fit(X_train, y_train, validation_split=0.2,
              epochs=50, batch_size=32, verbose=0)
    results[rate] = h.history['val_accuracy'][-1]
print(f"{'Rate':>6} | {'Val Accuracy':>12}")
print("-" * 22)
for rate, acc in results.items():
    print(f"{rate:>6.1f} | {acc:>12.4f}")
```

Run your file. You should see:
```
Rate | Val Accuracy
----------------------
0.1 |       ~0.942
0.3 |       ~0.945
0.5 |       ~0.940
```

---

## Step 7: TASK 4 (BONUS) — Verify Dropout Is Off During Prediction

Make 10 repeated calls to model.predict() on the same input. If Dropout were active during prediction, each call would give different output (because different neurons would be zeroed). Show they are all identical.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Dropout is OFF during prediction")
print("=" * 60)
print("\n--- Exercise 2 complete. Move to exercise3_batch_normalisation.py ---")
sample = X_test[:3]
preds = [model.predict(sample, verbose=0).flatten().round(4) for _ in range(5)]
print("5 repeated predictions on same input (Dropout should be OFF):")
for i, p in enumerate(preds, 1):
    print(f"  Call {i}: {p}")
all_same = all(np.array_equal(preds[0], p) for p in preds)
print(f"All identical: {all_same}")  # should print True
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_add_dropout.py`) if anything looks different.
