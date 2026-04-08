# Lab — Shape, Statistics, and Missing Values

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_statistics.py` in this folder.

---

## Step 2: Add the imports and setup

The dataset is loaded for you so you can focus on the statistics tasks. Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: fast numeric arrays
import pandas as pd                         # pandas: tabular data with labels
from sklearn.datasets import load_digits    # built-in 8x8 handwritten digits dataset

digits = load_digits()                       # Bunch object with .data, .target, .images, ...
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])  # 1797 rows x 64 cols
df["target"] = digits.target                 # add the label column (0..9)
```

---

## Step 3: Print shape and class information

Add this to your file:

```python
print(f"Samples  : {digits.data.shape[0]}")    # shape[0] = number of rows = number of images
print(f"Features : {digits.data.shape[1]}")    # shape[1] = number of columns = pixels per image
print(f"Classes  : {digits.target_names}")     # the unique labels the model can predict
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
# .min() / .max() collapse the entire 1797x64 array into a single number
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
# Pick 4 pixels + label so .describe() output stays readable
subset = df[["pixel_0", "pixel_10", "pixel_32", "pixel_63", "target"]]
print("\nSummary statistics:")
print(subset.describe().round(2))            # count, mean, std, min/max, quartiles per column
```

Run your file. You should see a table where `pixel_0` and `pixel_63` have `std=0.00` — they never change. `pixel_10` and `pixel_32` have higher standard deviations, meaning they carry information.

---

## Step 6: Check for missing values

Add this to your file:

```python
missing = df.isnull().sum()                  # .isnull() = True/False mask, .sum() counts True per col
print("\nMissing values per column (showing first 5):")
print(missing.head())                         # first 5 columns only — full output would be 65 rows
print(f"\nTotal missing values: {df.isnull().sum().sum()}")  # double-sum collapses to one number
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
print("\n--- Shape, Statistics, and Missing Values — complete ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_statistics.py`) if anything looks different.
