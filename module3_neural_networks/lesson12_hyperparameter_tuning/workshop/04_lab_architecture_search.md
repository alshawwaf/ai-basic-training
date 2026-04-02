# Lab -- Exercise 4: Architecture Search

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_architecture_search.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

---

## Step 3: Define the search space

Create: units_options = [32, 64, 128] depth_options = [1, 2, 3]

Add this to your file:

```python
```

---

## Step 4: Run the grid search

Nested loop over depth_options and units_options. For each combination: 1. Build the model with build_model(units, depth)

Add this to your file:

```python
```

---

## Step 5: Print results table

Convert `results` to a DataFrame. Sort by "val_acc" descending. Print with: print(df.to_string(index=False))

Add this to your file:

```python
```

Run your file. You should see:
```
units  depth  val_acc  params
128      2   0.9200   10625
64      2   0.9150    4929
128      1   0.9100    5505
...
```

---

## Step 6: Identify the winner (BONUS)

Print: "Best architecture: units=X, depth=Y, val_accuracy=Z.ZZZZ" Use df.iloc[0] after sorting.

Add this to your file:

```python
print("\n--- Exercise 4 complete. Workshop finished! Open 04_solution_architecture_search.py to compare. ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`04_solution_architecture_search.py`) if anything looks different.
