# Lab -- Exercise 2: Learning Rate Sensitivity

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_learning_rate_sensitivity.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
X, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                            n_redundant=5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)
def build_model(learning_rate):
    """Build and compile the same architecture with a given learning rate."""
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ])
    m.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return m
print("\n--- Exercise 2 complete. Move to 03_batch_size_effects.py ---")
```

---

## Step 4: Baseline: lr = 0.001

Build a model using build_model(0.001). Train it for 30 epochs with validation_data=(X_val, y_val) and verbose=0. Store the History object in a variable called history1.

Add this to your file:

```python
```

Run your file. You should see:
```
lr=0.001000 | final val_accuracy: 0.9150
Loss trajectory: smooth decline from ~0.65 to ~0.20
```

---

## Step 5: Too large: lr = 0.1

Repeat with build_model(0.1). Store history in history2. Print the final val_accuracy. Observe: does the loss curve oscillate or spike?

Add this to your file:

```python
```

Run your file. You should see:
```
lr=0.100000 | final val_accuracy: ~0.75-0.88 (varies more between runs)
Loss trajectory: erratic, may spike upward mid-training
```

---

## Step 6: Too small: lr = 0.00001

Repeat with build_model(0.00001). Store history in history3. Print the final val_accuracy. Observe: has the loss actually moved much?

Add this to your file:

```python
```

Run your file. You should see:
```
lr=0.000010 | final val_accuracy: ~0.55-0.65 (barely above random)
Loss trajectory: almost flat — very slow descent
```

---

## Step 7: Compare loss trajectories (BONUS)

Print the loss at epochs 1, 5, 10, 20, 30 for all three runs side by side. Format: "Epoch 10 | lr=0.001: 0.2834  lr=0.1: 0.3912  lr=0.00001: 0.6891" The histories store per-epoch loss in history.history['loss'] as a Python list.

Add this to your file:

```python
print("\n--- Exercise 2 complete. Move to 03_batch_size_effects.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_learning_rate_sensitivity.py`) if anything looks different.
