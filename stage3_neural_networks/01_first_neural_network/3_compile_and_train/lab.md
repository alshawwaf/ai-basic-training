# Lab — Exercise 3: Compile and Train

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_compile_and_train.py` in this folder.

---

## Step 2: Add the imports, dataset, and model setup

This exercise starts from a pre-built model so you can focus on the training loop. Add these imports to the top of your file:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras

X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("Model built and compiled.")
```

Run your file. You should see:
```
Model built and compiled.
```

---

## Step 3: Train for 20 epochs (Task 1)

`model.fit()` runs the training loop. `validation_split=0.2` reserves 20% of the training data to measure performance each epoch without updating weights. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 1 — Train the model for 20 epochs")
print("=" * 60)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=20,
    batch_size=32,
    verbose=1
)
```

Run your file. You should see per-epoch output ending with approximately:
```
Epoch 20/20
... loss: ~0.15 — accuracy: ~0.95 — val_loss: ~0.17 — val_accuracy: ~0.94
```

---

## Step 4: Print final accuracy from history (Task 2)

The `history` object stores metrics for every epoch as Python lists. The last item `[-1]` is the final epoch value. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Final accuracy from history")
print("=" * 60)

final_train_acc = history.history['accuracy'][-1]
final_val_acc   = history.history['val_accuracy'][-1]
print(f"Final train accuracy: {final_train_acc:.4f}")
print(f"Final val accuracy:   {final_val_acc:.4f}")
print(f"Overfit gap: {final_train_acc - final_val_acc:.4f}")
```

Run your file. You should see:
```
Final train accuracy: ~0.953
Final val accuracy:   ~0.941
Overfit gap: ~0.012
```

---

## Step 5: Plot training curves (Task 3)

Side-by-side plots show whether loss and accuracy are moving in the right direction and whether the model is overfitting. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Plot loss and accuracy training curves")
print("=" * 60)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(history.history['loss'],     label='Train loss')
ax1.plot(history.history['val_loss'], label='Val loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Training vs Validation Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(history.history['accuracy'],     label='Train accuracy')
ax2.plot(history.history['val_accuracy'], label='Val accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.set_title('Training vs Validation Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Step 6: Train longer to find the peak (Task 4 — Bonus)

Training for 100 epochs and finding when val_accuracy peaked shows the cost of overtraining. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Train for 100 epochs, find when val peaks")
print("=" * 60)

model2 = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model2.compile(optimizer='adam', loss='binary_crossentropy',
               metrics=['accuracy'])
history2 = model2.fit(X_train, y_train, validation_split=0.2,
                      epochs=100, batch_size=32, verbose=0)
val_accs = history2.history['val_accuracy']
best_epoch = int(np.argmax(val_accs)) + 1
print(f"Best val accuracy: {max(val_accs):.4f} at epoch {best_epoch}")
print(f"Final val accuracy: {val_accs[-1]:.4f}")
print(f"Difference (overtraining effect): {max(val_accs) - val_accs[-1]:.4f}")

print("\n--- Exercise 3 complete. Move to 04_evaluate_and_improve.py ---")
```

Run your file. You should see approximately:
```
Best val accuracy: ~0.945 at epoch ~18
Final val accuracy: ~0.938
Difference (overtraining effect): ~0.007
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `solve.py` if anything looks different.
