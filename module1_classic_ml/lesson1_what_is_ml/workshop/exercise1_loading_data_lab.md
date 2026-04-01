# Lab — Exercise 1: Loading a Dataset

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_loading_data.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
```

---

## Step 3: Load the dataset

`load_digits()` returns a `Bunch` object — a container with named fields. Add this to your file:

```python
digits = load_digits()

print("Dataset loaded.")
print(f"Type: {type(digits)}")
print(f"Fields available: {list(digits.keys())}")
```

Run your file. You should see:
```
Dataset loaded.
Type: <class 'sklearn.utils._bunch.Bunch'>
Fields available: ['data', 'target', 'target_names', 'images', 'DESCR']
```

---

## Step 4: Access the raw arrays

`.shape` returns a tuple: `(rows, columns)`. Add this to your file:

```python
print(f"Features (X) shape: {digits.data.shape}")
print(f"Labels   (y) shape: {digits.target.shape}")
```

Run your file. You should see:
```
Features (X) shape: (1797, 64)
Labels   (y) shape: (1797,)
```

---

## Step 5: Wrap the data in a DataFrame

A DataFrame gives you named columns and easy inspection. Add this to your file:

```python
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

print("\nFirst 3 rows of the DataFrame:")
print(df.head(3).to_string())
print(f"\nDataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")
```

Run your file. You should see:
```
First 3 rows of the DataFrame:
   pixel_0  pixel_1  pixel_2  ...  pixel_63  target
0      0.0      0.0      5.0  ...       0.0       0
1      0.0      0.0      0.0  ...       0.0       1
2      0.0      0.0      0.0  ...       0.0       2

DataFrame shape: (1797, 65)
Columns: pixel_0 ... pixel_63, target  (65 total)
```

---

## Step 6: Inspect one sample

Print the label and first 10 pixel values of the very first row. Add this to your file:

```python
print(f"\nFirst sample — label: {digits.target[0]}")
print(f"First 10 pixel values: {digits.data[0, :10]}")
```

Run your file. You should see:
```
First sample — label: 0
First 10 pixel values: [ 0.  0.  5. 13.  9.  1.  0.  0.]
```

---

## Step 7: Add the completion message

```python
print("\n--- Exercise 1 complete. Move to exercise2_statistics.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
