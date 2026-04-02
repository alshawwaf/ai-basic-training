# Lab -- Exercise 3: Batch Size Effects

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_batch_size_effects.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

---

## Step 3: Small batch: batch_size=32

Build a fresh model with build_model(). Record the start time with time.time(). Train for EPOCHS epochs with batch_size=32, validation_data=(X_val, y_val), verbose=0.

Add this to your file:

```python
```

Run your file. You should see:
```
batch_size=  32 | val_accuracy: 0.9150 | time: 4.1s
```

---

## Step 4: Large batch: batch_size=512

Repeat with batch_size=512. Print the same formatted line.

Add this to your file:

```python
```

Run your file. You should see:
```
batch_size= 512 | val_accuracy: 0.9000 | time: 1.7s
```

---

## Step 5: Full batch: batch_size=len(X_train)

Use the entire training set as a single batch. Print the same formatted line. Does accuracy drop? Is it noticeably faster?

Add this to your file:

```python
```

Run your file. You should see:
```
batch_size=1600 | val_accuracy: 0.8850 | time: 0.9s
```

---

## Step 6: Summary comparison (BONUS)

Print a table showing all three results side by side, including: - batch_size - val_accuracy

Add this to your file:

```python
print("\n--- Exercise 3 complete. Move to 04_architecture_search.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
