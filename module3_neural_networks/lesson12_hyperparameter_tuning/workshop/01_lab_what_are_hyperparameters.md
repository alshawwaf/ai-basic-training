# Lab -- Exercise 1: What Are Hyperparameters? — Parameters vs Hyperparameters

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_what_are_hyperparameters.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
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

## Step 4: Inspect Weights Before and After Training

Build a simple model: Dense(8, relu, input_shape=(10,)) → Dense(1, sigmoid) Print the first layer's weight matrix BEFORE training (random initialisation). Train for 10 epochs.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Weights before and after training")
print("=" * 60)
model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(10,)),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
# Weights BEFORE training
weights_before = model.layers[0].get_weights()[0].copy()  # shape (10, 8)
print("Layer 1 weights BEFORE training (first row):")
print(weights_before[0].round(4))
# Train
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
# Weights AFTER training
weights_after = model.layers[0].get_weights()[0]
print("\nLayer 1 weights AFTER training (first row):")
print(weights_after[0].round(4))
print(f"\nWeights changed: {not np.allclose(weights_before, weights_after)}")
print(f"Mean absolute change: {np.abs(weights_after - weights_before).mean():.4f}")
```

Run your file. You should see:
```
Layer 1 weights BEFORE: [some random small values near 0]
Layer 1 weights AFTER:  [different values, some larger, some smaller]
Weights changed: True
```

---

## Step 5: List All Hyperparameters in a Keras Model

Print a formatted table of all hyperparameters with their categories and values. Use the model from Task 1 (or rebuild it) with its specific settings.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Complete hyperparameter inventory")
print("=" * 60)
hyperparams = {
    'Architecture': {
        'n_hidden_layers': 1,
        'units_layer_1': 8,
        'activation_hidden': 'relu',
        'output_units': 1,
        'activation_output': 'sigmoid',
    },
    'Regularisation': {
        'dropout_rate': 0.0,
        'l1_penalty': 0.0,
        'l2_penalty': 0.0,
    },
    'Optimiser': {
        'optimizer': 'adam',
        'learning_rate': 0.001,
        'beta_1': 0.9,
        'beta_2': 0.999,
    },
    'Training': {
        'epochs': 10,
        'batch_size': 32,
        'validation_split': 0.0,
    }
}
print(f"{'Category':>16} | {'Hyperparameter':>20} | {'Value'}")
print("-" * 52)
for category, params in hyperparams.items():
    for name, val in params.items():
        print(f"{category:>16} | {name:>20} | {val}")
    print("-" * 52)
```

---

## Step 6: Two Models, Different Hyperparameters, Different Results

Build Model A: Dense(8, relu) → Dense(1, sigmoid), lr=0.001, epochs=20 Build Model B: Dense(64, relu) → Dense(32, relu) → Dense(1, sigmoid), lr=0.01, epochs=20 Train both. Print test accuracy for each.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Different hyperparameters, different results")
print("=" * 60)
model_a = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(10,)),
    keras.layers.Dense(1, activation='sigmoid')
])
model_a.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='binary_crossentropy', metrics=['accuracy'])
model_a.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
_, acc_a = model_a.evaluate(X_test, y_test, verbose=0)
#
model_b = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model_b.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
                loss='binary_crossentropy', metrics=['accuracy'])
model_b.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
_, acc_b = model_b.evaluate(X_test, y_test, verbose=0)
#
print(f"Model A (Dense(8),  lr=0.001): test accuracy = {acc_a:.4f}")
print(f"Model B (Dense(64,32), lr=0.01): test accuracy = {acc_b:.4f}")
print(f"Difference:                       {abs(acc_b - acc_a):.4f}")
```

Run your file. You should see:
```
Model A: test accuracy = ~0.910
Model B: test accuracy = ~0.940
Different hyperparameters → different results!
```

---

## Step 7: TASK 4 (BONUS) — Set Random Seed for Reproducibility

Train the same model TWICE without a seed. Print both test accuracies. Then train twice WITH tf.random.set_seed() and np.random.seed(). Show that setting the seed makes results identical.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Reproducibility with random seeds")
print("=" * 60)
print("\n--- Exercise 1 complete. Move to 02_learning_rate_sensitivity.py ---")
def make_model_and_train():
    m = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(10,)),
        keras.layers.Dense(1,  activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    m.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    _, acc = m.evaluate(X_test, y_test, verbose=0)
    return acc
#
# Without seed — results differ
acc1 = make_model_and_train()
acc2 = make_model_and_train()
print(f"Without seed: {acc1:.4f}, {acc2:.4f} — same? {abs(acc1-acc2) < 0.001}")
#
# With seed — results identical
tf.random.set_seed(99); np.random.seed(99)
acc3 = make_model_and_train()
tf.random.set_seed(99); np.random.seed(99)
acc4 = make_model_and_train()
print(f"With seed:    {acc3:.4f}, {acc4:.4f} — same? {abs(acc3-acc4) < 0.001}")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`01_solution_what_are_hyperparameters.py`) if anything looks different.
