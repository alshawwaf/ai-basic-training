# Lab — What the Model Actually Sees

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `05_what_model_sees.py` in this folder.

---

## Step 2: Add the imports and setup

Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: fast numeric arrays
import pandas as pd                         # pandas: tabular data with labels
import matplotlib.pyplot as plt             # matplotlib: standard Python plotting library
from sklearn.datasets import load_digits    # built-in 8x8 handwritten digits dataset

digits = load_digits()                       # Bunch with .data, .target, .images, ...
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])  # 1797 x 64 table
df["target"] = digits.target                 # add the label column (digit 0..9)
```

---

## Step 3: Print one image as its raw 8x8 number grid

The model never sees a picture — it sees a flat row of numbers. `f"{v:2d}"` formats an integer as exactly 2 characters wide so columns align. Add this to your file:

```python
image = digits.images[0].astype(int)         # cast 0..16 floats to ints for clean printing
print(f"Image index 0 — label: {digits.target[0]}")
for row in image:                             # each row is one of the 8 horizontal scanlines
    # f"{v:2d}" pads each integer to 2 chars wide so columns line up vertically
    print("  ".join(f"{v:2d}" for v in row))
```

Run your file. You should see:
```
Image index 0 — label: 0
 0   0   5  13   9   1   0   0
 0   0  13  15  10  15   5   0
 0   3  15   2   0  11   8   0
 0   4  12   0   0   8   8   0
 0   5   8   0   0   9   8   0
 0   4  11   0   1  12   7   0
 0   2  14   5  10  12   0   0
 0   0   6  13  10   0   0   0
```

---

## Step 4: Print examples of digit 1 and digit 7 as number grids

These two digits are often confused. Printing them side by side reveals where they differ. Add this to your file:

```python
for digit in [1, 7]:
    # Boolean mask: keep only images of this class, then take the first one
    example = digits.images[digits.target == digit][0].astype(int)
    print(f"\n--- Digit {digit} ---")
    for row in example:
        print("  ".join(f"{v:2d}" for v in row))    # same 2-char-wide formatting as before
```

Run your file and look for which rows differ between 1 and 7.

---

## Step 5: Find the most informative pixels

Features with higher absolute correlation to the target carry more predictive information. Add this to your file:

```python
# .corr() = pairwise correlations between every column; ["target"] = just the label column;
# .abs() flips negatives so strong positive AND negative correlations both rank high
correlations = df.corr()["target"].abs().drop("target").sort_values(ascending=False)
print("\nTop 10 pixels most correlated with digit label:")
print(correlations.head(10).round(2))         # the 10 most predictive pixels in the image
```

Run your file. You should see something like:
```
Top 10 pixels most correlated with digit label:
pixel_43    0.55
pixel_34    0.53
pixel_26    0.52
...
```

---

## Step 6: Print the security analogy

Add this to your file:

```python
print("\n=== Security Feature Analogy ===")
print("Digits:   [0, 0, 5, 13, 9, ...]  <- pixel brightnesses")
print("Network:  [1048576, 443, 0.24, 2, 14, ...]  <- bytes, port, duration, flags ...")
print("Same structure. Same algorithms. Different domain.")
```

---

## Step 7: Add the completion message

```python
print("\n--- What the Model Actually Sees — complete ---")
print("You have completed all 5 hands-on labs for Lesson 1.1.")
print("")
print("Next steps:")
print("  1. Open the matching solution file to compare your code")
print("  2. Read the theory notes: README.md")
print("  3. Move to Lesson 1.2: ../../../02_linear_regression/")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_what_model_sees.py`) if anything looks different.
