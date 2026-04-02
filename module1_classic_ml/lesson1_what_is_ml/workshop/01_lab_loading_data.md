# Lab — Exercise 1: Loading a Dataset

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 0: Install the required packages

If you haven't already, activate your virtual environment and install the libraries used throughout Modules 1 and 2:

```bash
pip install pandas scikit-learn matplotlib seaborn
```

> You only need to do this once. If you have already installed these packages, skip to Step 1.

---

## Step 1: Create your script file

Create a new file called `01_loading_data.py` in this folder.

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
Fields available: ['data', 'target', 'frame', 'feature_names', 'target_names', 'images', 'DESCR']
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

preview_cols = ["pixel_21", "pixel_28", "pixel_36", "pixel_43", "target"]
print("\nFirst 5 rows (selected columns):")
print(df[preview_cols].head().to_string())
print(f"\nFull DataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")
```

We pick centre pixels (21, 28, 36, 43) because edge pixels are mostly zero — the handwriting sits in the middle of the 8x8 grid.

Run your file. You should see:
```
First 5 rows (selected columns):
   pixel_21  pixel_28  pixel_36  pixel_43  target
0      11.0       0.0       0.0       0.0       0
1       6.0      16.0      16.0      16.0       1
2      16.0      15.0      15.0      16.0       2
3       0.0      11.0      12.0       0.0       3
4       2.0       0.0       0.0      16.0       4

Full DataFrame shape: (1797, 65)
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
First 10 pixel values: [ 0.  0.  5. 13.  9.  1.  0.  0.  0.  0.]
```

---

## Step 7: Add the completion message

```python
print("\n--- Exercise 1 complete. Move to 02_statistics.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`01_solution_loading_data.py`) if anything looks different.
