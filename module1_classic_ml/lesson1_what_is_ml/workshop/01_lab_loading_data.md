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

Every supervised ML dataset has two parts:

- **Features (X)** — the measurements the model uses to make predictions. Here, the pixel intensities of each image.
- **Labels (y)** — the correct answer for each sample. Here, which digit (0–9) the image actually shows.

They are stored as two separate arrays that line up by row — row 0 of X pairs with row 0 of y, row 1 with row 1, and so on:

```
Features (X)                          Labels (y)
┌──────────────────────────────┐      ┌───┐
│ sample 0:  0  0  5 13 ...    │ ───► │ 0 │   ← this image is a "0"
│ sample 1:  0  0  0 12 ...    │ ───► │ 1 │   ← this image is a "1"
│ sample 2:  0  0  0 12 ...    │ ───► │ 2 │   ← this image is a "2"
│ ...        (1797 rows)       │      │...│
│ sample 1796: 0  0 10 14 ...  │ ───► │ 8 │
└──────────────────────────────┘      └───┘
  1797 rows × 64 columns               1797 values
```

`.shape` tells you the dimensions. Add this to your file:

```python
print(f"Features (X) shape: {digits.data.shape}")
print(f"Labels   (y) shape: {digits.target.shape}")
```

Run your file. You should see:
```
Features (X) shape: (1797, 64)
Labels   (y) shape: (1797,)
```

`(1797, 64)` means 1,797 samples, each described by 64 features (one per pixel). `(1797,)` means a flat array of 1,797 labels — one per sample.

---

## Step 5: Wrap the data in a DataFrame

So far the data lives in a NumPy array — just rows of numbers with no column names. A **DataFrame** (from the `pandas` library) adds column names and gives you powerful inspection methods like `.head()`, `.describe()`, and `.shape`.

Add this to your file:

```python
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
```

This creates a table with 64 columns named `pixel_0` through `pixel_63` (one per pixel in the 8x8 image) plus a `target` column holding the digit label (0–9).

Printing all 65 columns would flood the terminal, so we pick a few to preview. Add this to your file:

```python
preview_cols = ["pixel_21", "pixel_28", "pixel_36", "pixel_43", "target"]
print("\nFirst 5 rows (selected columns):")
print(df[preview_cols].head().to_string())
print(f"\nFull DataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")
```

**Why these columns?** Each image is an 8x8 grid — 64 pixels numbered left-to-right, top-to-bottom. Pixels at the edges (0, 7, 56, 63) are almost always zero because handwriting sits in the centre. Pixels 21, 28, 36, and 43 are in the middle rows where the ink actually is, so they show meaningful variation across different digits.

```
 0   1   2   3   4   5   6   7      ← top row (mostly blank)
 8   9  10  11  12  13  14  15
16  17  18  19  20 [21] 22  23      ← pixel 21
24  25  26  27 [28] 29  30  31      ← pixel 28
32  33  34  35 [36] 37  38  39      ← pixel 36
40  41  42 [43] 44  45  46  47      ← pixel 43
48  49  50  51  52  53  54  55
56  57  58  59  60  61  62  63      ← bottom row (mostly blank)
```

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

Notice how each digit has a different pattern of pixel intensities — that is exactly what the model will learn from.

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
