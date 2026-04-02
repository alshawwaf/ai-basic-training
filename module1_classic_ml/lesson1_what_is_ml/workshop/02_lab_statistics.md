# Lab — Exercise 2: Shape, Statistics, and Missing Values

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_statistics.py` in this folder.

---

## Step 2: Add the imports and setup

The dataset is loaded for you so you can focus on the statistics tasks. Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
```

---

## Step 3: Print shape and class information

Add this to your file:

```python
print(f"Samples  : {digits.data.shape[0]}")
print(f"Features : {digits.data.shape[1]}")
print(f"Classes  : {digits.target_names}")
```

Run your file. You should see:
```
Samples  : 1797
Features : 64
Classes  : [0 1 2 3 4 5 6 7 8 9]
```

---

## Step 4: Print value range

`digits.data.min()` and `.max()` operate on the entire array and return a single number. Add this:

```python
print(f"\nPixel value range: min={int(digits.data.min())}, max={int(digits.data.max())}")
print("(0 = white background, 16 = maximum ink density)")
```

Run your file. You should see:
```
Pixel value range: min=0, max=16
(0 = white background, 16 = maximum ink density)
```

---

## Step 5: Summary statistics with `.describe()`

Select a few columns to keep the output readable. Add this:

```python
subset = df[["pixel_0", "pixel_10", "pixel_32", "pixel_63", "target"]]
print("\nSummary statistics:")
print(subset.describe().round(2))
```

Run your file. You should see a table where `pixel_0` and `pixel_63` have `std=0.00` — they never change. `pixel_10` and `pixel_32` have higher standard deviations, meaning they carry information.

---

## Step 6: Check for missing values

Add this to your file:

```python
missing = df.isnull().sum()
print("\nMissing values per column (showing first 5):")
print(missing.head())
print(f"\nTotal missing values: {df.isnull().sum().sum()}")
```

Run your file. You should see:
```
Missing values per column (showing first 5):
pixel_0    0
pixel_1    0
pixel_2    0
pixel_3    0
pixel_4    0

Total missing values: 0
```

---

## Step 7: Add the completion message

```python
print("\n--- Exercise 2 complete. Move to 03_class_balance.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_statistics.py`) if anything looks different.
