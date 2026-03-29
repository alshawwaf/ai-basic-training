# Lesson 1.1 — Lab Guide: Build the Exploration Script

> **Read first:** [1_what_is_ml.md](1_what_is_ml.md) — concepts and theory
> **Reference solution:** [1_concepts_and_data.py](1_concepts_and_data.py) — open only after finishing this guide

---

## What You Will Build

By the end of this lab you will have your own working script that loads a real dataset and explores it thoroughly. This EDA (Exploratory Data Analysis) workflow is the same one you will repeat at the start of every ML project.

---

## Before You Start

**Create a new file** in this folder called `my_lab_1_1.py` and open it in VS Code.

This is your working file. Write all the code from the steps below into it. Run it after each step to see the output — do not write the whole thing first and run it at the end.

---

## Step 1 — Import Your Tools

Type this at the top of `my_lab_1_1.py`:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
```

What each one is:

- `numpy` — fast numerical arrays. Everything in ML is arrays of numbers. Alias `np` is universal.
- `pandas` — DataFrames, like a spreadsheet you can query in code. Alias `pd` is universal.
- `matplotlib.pyplot` — plots and charts. Alias `plt` is universal.
- `load_digits` — a function inside scikit-learn that loads a ready-made dataset. No download needed.

**Run it:**
```
python module1_classic_ml/lesson1/my_lab_1_1.py
```

**Expected output:** nothing. No errors means Python found all the libraries.

---

## Step 2 — Load the Dataset

Add this below your imports:

```python
digits = load_digits()

df = pd.DataFrame(
    digits.data,
    columns=[f"pixel_{i}" for i in range(64)]
)
df["target"] = digits.target
```

`load_digits()` returns an object with these fields:

| Field | Shape | Contents |
|-------|-------|----------|
| `digits.data` | (1797, 64) | 1797 images, each flattened to 64 pixel values |
| `digits.target` | (1797,) | Correct label (0–9) for each image |
| `digits.images` | (1797, 8, 8) | Same pixels but as 8×8 grids — for plotting |

`f"pixel_{i}"` is an f-string — Python fills in the variable, giving column names `pixel_0`, `pixel_1`, ..., `pixel_63`. The last line adds a `target` column so each row has 64 features plus its correct label.

**Run it.** No output yet — we loaded into memory but haven't printed anything.

---

## Step 3 — Check Shape and Basic Statistics

Add this:

```python
print("=" * 60)
print("STEP 2 - Shape and Basic Statistics")
print("=" * 60)

print(f"\nRows    : {digits.data.shape[0]}  (each row = one image)")
print(f"Columns : {digits.data.shape[1]}  (each column = one pixel feature)")
print(f"Classes : {list(digits.target_names)}")
print(f"\nPixel value range: min={digits.data.min():.0f}, max={digits.data.max():.0f}")
print("(0 = white background, 16 = black ink)")
```

**Run it.**

**Expected output:**
```
============================================================
STEP 2 - Shape and Basic Statistics
============================================================

Rows    : 1797  (each row = one image)
Columns : 64  (each column = one pixel feature)
Classes : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Pixel value range: min=0, max=16
(0 = white background, 16 = black ink)
```

Always do this first on any new dataset — it confirms the data loaded correctly and tells you immediately what you are working with.

---

## Step 4 — Check Class Balance

Add this:

```python
print("\n" + "=" * 60)
print("STEP 3 - Class Balance")
print("=" * 60)

print("\nSamples per digit:")
print(df["target"].value_counts().sort_index().to_string())
print("\nThis dataset is well-balanced (~178 per class).")
print("Compare: a real network dataset might have 950,000 normal vs 50,000 attacks.")
print("A model that always predicts 'normal' gets 95% accuracy but catches ZERO attacks.")
```

**Run it.**

**Expected output:**
```
============================================================
STEP 3 - Class Balance
============================================================

Samples per digit:
0    178
1    182
2    177
3    183
4    181
5    182
6    181
7    179
8    174
9    180

This dataset is well-balanced (~178 per class).
Compare: a real network dataset might have 950,000 normal vs 50,000 attacks.
A model that always predicts 'normal' gets 95% accuracy but catches ZERO attacks.
```

In real security work, balanced data is rare. Checking balance before training is non-negotiable.

---

## Step 5 — Visualise Sample Images

Add this:

```python
print("\n" + "=" * 60)
print("STEP 4 - Sample Images (see plot window)")
print("=" * 60)

fig, axes = plt.subplots(2, 10, figsize=(18, 4))
fig.suptitle("Two examples of each digit class (0-9)", fontsize=12)

for digit in range(10):
    samples = digits.images[digits.target == digit]
    for row, sample in zip(axes, samples[:2]):
        row[digit].imshow(sample, cmap="gray_r")
        row[digit].set_title(str(digit))
        row[digit].axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1/sample_digits.png")
plt.show()
print("What to look for: are the digits recognisable? Any that look ambiguous?")
```

**Run it.** A window opens showing 20 digit images (2 per class).

**What to look for:** Some digits will look messy — handwriting varies. The more ambiguous a digit looks to you, the harder it is for the model too.

- `plt.subplots(2, 10)` — creates a 2-row, 10-column grid of panels
- `digits.target == digit` — a True/False mask that filters only images with that label
- `cmap="gray_r"` — reversed greyscale: high values (ink) appear dark

---

## Step 6 — See What the Model Actually Sees

The model never sees a picture. It sees a flat row of 64 numbers. Add this:

```python
print("\n" + "=" * 60)
print("STEP 5 - One Image as Raw Numbers")
print("=" * 60)

print("\nThe first image in the dataset, printed as its 8x8 pixel grid:")
print("(0 = white background, 16 = black ink)\n")

sample_image = digits.images[0]
for row in sample_image.astype(int):
    print("  " + "  ".join(f"{v:2d}" for v in row))

print(f"\n  ^ This is the digit '{digits.target[0]}'")
print("\nThis row of 64 numbers is exactly what the model will receive as input.")
```

**Run it.**

**Expected output:**
```
============================================================
STEP 5 - One Image as Raw Numbers
============================================================

The first image in the dataset, printed as its 8x8 pixel grid:
(0 = white background, 16 = black ink)

   0   0   5  13   9   1   0   0
   0   0  13  15  10  15   5   0
   0   3  15   2   0  11   8   0
   0   4  12   0   0   8   8   0
   0   5   8   0   0   9   8   0
   0   4  11   0   1  12   7   0
   0   2  14   5  10  12   0   0
   0   0   6  13  10   0   0   0

  ^ This is the digit '0'

This row of 64 numbers is exactly what the model will receive as input.
```

In security, instead of pixel values you would see `bytes_per_second`, `unique_ports`, `entropy`, `protocol_flags` — same flat-row structure, different domain.

---

## Step 7 — Average Image per Class

Averaging all images of one digit gives its "prototype." Similar prototypes = harder classification problem. Add this:

```python
print("\n" + "=" * 60)
print("STEP 6 - Average Images per Class (see plot window)")
print("=" * 60)

fig, axes = plt.subplots(1, 10, figsize=(18, 2))
fig.suptitle("Average pixel pattern per digit class", fontsize=12)

for digit, ax in enumerate(axes):
    mean_image = digits.images[digits.target == digit].mean(axis=0)
    ax.imshow(mean_image, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1/average_digits.png")
plt.show()
print("What to look for: which digits have the most similar average shapes?")
print("Hint: look at 1 vs 7, and 3 vs 8 - those pairs will confuse the model most.")
```

**Run it.**

**What to look for:** Which digit pairs look most alike in the average image? In Lesson 1.5 you will look at the confusion matrix and see whether those same pairs produce the most errors.

---

## Your Script Is Complete

Your `my_lab_1_1.py` should now:

1. Load 1,797 digit images (64 features each, 10 classes)
2. Print shape and pixel range
3. Print class balance and flag the imbalance risk
4. Display 2 sample images per class
5. Print one raw image as a number grid
6. Display the average pixel pattern per class

**Now open [1_concepts_and_data.py](1_concepts_and_data.py)** and compare it to yours.

Things to notice in the reference:
- The structure matches what you built
- Every line has a comment explaining why, not just what
- The `EXERCISES` section at the bottom has 4 extensions — try them one at a time

---

## Exercises

Uncomment one block at a time in [1_concepts_and_data.py](1_concepts_and_data.py), run it, observe, then move to the next.

| Exercise | What it shows |
|----------|--------------|
| 1 | Which pixels differ most between digit 0 and digit 1? |
| 2 | Are there any missing values? (In real security data, almost always yes) |
| 3 | Distribution of one pixel's brightness across all 1,797 images |
| 4 | Which pixels correlate most strongly with the target label? |

---

## Next Lesson

**[Lesson 1.2 — Linear Regression](../lesson2/2_linear_regression.md):** Your first trained model — predicts server response time from network traffic load.
