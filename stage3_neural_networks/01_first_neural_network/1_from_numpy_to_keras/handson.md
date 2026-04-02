# Lab — Exercise 1: From NumPy to Keras

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 0: Install the required packages

If you haven't already, activate your virtual environment and install the libraries used throughout Stage 3:

```bash
pip install tensorflow nnfs
```

> You only need to do this once. If you have already installed these packages, skip to Step 1.

---

## Step 1: Create your script file

Create a new file called `01_from_numpy_to_keras.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
```

---

## Step 3: Build a tiny Sequential model (Task 1)

A `Dense(8, activation='relu', input_shape=(4,))` layer takes 4 inputs and produces 8 outputs. A final `Dense(1, activation='sigmoid')` squashes the output to a probability. Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Build a tiny Sequential model")
print("=" * 60)

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(4,)),
    keras.layers.Dense(1, activation='sigmoid')
])
model.summary()
```

Run your file. You should see:
```
TASK 1 — Build a tiny Sequential model
============================================================
Model: "sequential"
_________________________________________________________________
 Layer (type)         Output Shape         Param #
=================================================================
 dense (Dense)        (None, 8)            40
 dense_1 (Dense)      (None, 1)            9
=================================================================
Total params: 49  Trainable params: 49
```

---

## Step 4: Verify the parameter count manually (Task 2)

Each Dense layer's parameters follow the formula `(n_inputs × n_units) + n_units`. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Verify parameter count manually")
print("=" * 60)

layer1_params = (4 * 8) + 8
layer2_params = (8 * 1) + 1
total         = layer1_params + layer2_params
print(f"Layer 1 (Dense 8):  ({4} × {8}) + {8} = {layer1_params}")
print(f"Layer 2 (Dense 1):  ({8} × {1}) + {1} = {layer2_params}")
print(f"Total parameters:   {total}")
print(f"model.count_params(): {model.count_params()}")
print(f"Match: {total == model.count_params()}")
```

Run your file. You should see:
```
Layer 1 (Dense 8):  (4 × 8) + 8 = 40
Layer 2 (Dense 1):  (8 × 1) + 1 = 9
Total parameters:   49
model.count_params(): 49
Match: True
```

---

## Step 5: Run a forward-pass prediction (Task 3)

Even before training the model has random weights, so we can run `model.predict()` to verify the output shape and that sigmoid keeps values in [0, 1]. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Single forward-pass prediction")
print("=" * 60)

np.random.seed(0)
sample_input = np.random.randn(3, 4).astype('float32')
predictions  = model.predict(sample_input, verbose=0)
print(f"Input shape:   {sample_input.shape}")
print(f"Output shape:  {predictions.shape}")
print(f"Output values: {predictions.flatten().round(4)}")
print(f"All between 0-1: {(predictions >= 0).all() and (predictions <= 1).all()}")
```

Run your file. You should see:
```
Input shape:   (3, 4)
Output shape:  (3, 1)
Output values: [some values between 0 and 1]
All between 0-1: True
```

---

## Step 6: Compare parameter counts across architectures (Task 4 — Bonus)

Building three models of different sizes shows how parameter count grows with layer width and depth. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Parameter count across architectures")
print("=" * 60)

configs = [
    [(4,'relu'), (1,'sigmoid')],
    [(64,'relu'), (32,'relu'), (1,'sigmoid')],
    [(256,'relu'), (128,'relu'), (64,'relu'), (1,'sigmoid')],
]
for config in configs:
    layers = []
    for i, (units, act) in enumerate(config):
        if i == 0:
            layers.append(keras.layers.Dense(units, activation=act,
                                             input_shape=(10,)))
        else:
            layers.append(keras.layers.Dense(units, activation=act))
    m = keras.Sequential(layers)
    print(f"Architecture {[u for u,a in config]}: {m.count_params():,} params")

print("\n--- Exercise 1 complete. Move to 02_build_the_network.py ---")
```

Run your file. You should see:
```
Architecture [4, 1]: 51 params
Architecture [64, 32, 1]: 2,625 params
Architecture [256, 128, 64, 1]: 67,393 params
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `solution_from_numpy_to_keras.py` if anything looks different.
