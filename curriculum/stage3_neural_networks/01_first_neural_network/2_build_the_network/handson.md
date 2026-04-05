# Lab — Exercise 2: Build the Network

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_build_the_network.py` in this folder.

---

## Step 2: Add the imports and dataset setup

The dataset is an imbalanced binary classification problem (90% benign, 10% attack). Add these imports to the top of your file:

```python
import numpy as np
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
print(f"Dataset: {X_train.shape[0]} train / {X_test.shape[0]} test samples")
print(f"Class distribution (train): {np.bincount(y_train)}")
```

Run your file. You should see:
```
Dataset: 1600 train / 400 test samples
Class distribution (train): [1436  164]
```

---

## Step 3: Build the binary classifier (Task 1)

The input has 10 features. Hidden layers use relu; the single output unit uses sigmoid to produce a probability. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 1 — Build the binary classifier")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model.summary()
```

Run your file. You should see:
```
 dense (Dense)          (None, 64)    704
 dense_1 (Dense)        (None, 32)    2080
 dense_2 (Dense)        (None, 1)     33
 Total params: 2,817
```

---

## Step 4: Verify the parameter count manually (Task 2)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Parameter count breakdown")
print("=" * 60)

l1 = (10 * 64) + 64
l2 = (64 * 32) + 32
l3 = (32 *  1) +  1
print(f"Dense(64): (10×64)+64   = {l1}")
print(f"Dense(32): (64×32)+32   = {l2}")
print(f"Dense(1):  (32×1) +1    = {l3}")
print(f"Total:                    {l1+l2+l3}")
print(f"model.count_params():     {model.count_params()}")
```

Run your file. You should see:
```
Dense(64): (10×64)+64   = 704
Dense(32): (64×32)+32   = 2080
Dense(1):  (32×1) +1    = 33
Total:                    2817
```

---

## Step 5: Compile the model (Task 3)

Compiling sets the optimizer, loss function, and metrics. The model is now ready to train. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Compile the model")
print("=" * 60)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
print("Model compiled successfully.")
print(f"Optimizer: {model.optimizer.__class__.__name__}")
print(f"Loss:      {model.loss}")
```

Run your file. You should see:
```
Model compiled successfully.
Optimizer: Adam
Loss: binary_crossentropy
```

---

## Step 6: Build a 3-class classifier (Task 4 — Bonus)

For multi-class output, switch to `Dense(N, softmax)` and `sparse_categorical_crossentropy`. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — 3-class classifier")
print("=" * 60)

X3, y3 = make_classification(n_samples=2000, n_features=10, n_classes=3,
                              n_informative=6, n_clusters_per_class=1,
                              random_state=42)
model3 = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(3,  activation='softmax')
])
model3.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])
model3.summary()
print(f"Output layer for 3-class: {model3.layers[-1].units} units (softmax)")

print("\n--- Exercise 2 complete. Move to 03_compile_and_train.py ---")
```

Run your file. You should see:
```
Output layer for 3-class: 3 units (softmax)
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `solution_build_the_network.py` if anything looks different.
