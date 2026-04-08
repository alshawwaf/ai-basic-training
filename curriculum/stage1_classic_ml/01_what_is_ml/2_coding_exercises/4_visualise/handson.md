# Lab — Visualising Your Data

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_visualise.py` in this folder.

---

## Step 2: Add the imports and setup

Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: fast numeric arrays
import pandas as pd                         # pandas: tabular data with labels
import matplotlib.pyplot as plt             # matplotlib: the standard Python plotting library
from sklearn.datasets import load_digits    # built-in 8x8 handwritten digits dataset

digits = load_digits()                       # Bunch with .data, .target, .images, ...
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
```

---

## Step 3: Plot one sample image per class

`plt.subplots(rows, cols)` creates a grid of panels. `ax.imshow()` renders a 2D array as an image. Add this to your file:

```python
fig, axes = plt.subplots(1, 10, figsize=(18, 2))   # 1 row x 10 cols of panels, 18x2 inches
fig.suptitle("One example of each digit class (0-9)", fontsize=12)
for digit in range(10):
    ax = axes[digit]
    # Boolean indexing: keep only images whose target == this digit, take the first
    sample = digits.images[digits.target == digit][0]
    ax.imshow(sample, cmap="gray_r")               # gray_r = inverted greyscale (dark = ink)
    ax.set_title(str(digit))
    ax.axis("off")                                  # hide tick marks for a clean image grid
plt.tight_layout()                                  # auto-adjust spacing to avoid overlap
plt.show()
```

Run your file. You should see a row of 10 digit images, one per class. All should be clearly recognisable.

---

## Step 4: Plot two examples per class

Two examples side by side shows how much variation exists within one class. Add this to your file:

```python
fig, axes = plt.subplots(2, 10, figsize=(18, 4))   # 2 rows x 10 cols = 20 panels
fig.suptitle("Two examples of each digit class (0-9)", fontsize=12)
for digit in range(10):
    samples = digits.images[digits.target == digit]   # all images of this digit
    for row_idx, sample in zip(axes, samples[:2]):    # take the first 2, place one per row
        row_idx[digit].imshow(sample, cmap="gray_r")
        row_idx[digit].set_title(str(digit))
        row_idx[digit].axis("off")

plt.tight_layout()
plt.savefig("sample_digits.png")                     # write the figure to disk as a PNG
plt.show()
```

---

## Step 5: Compute and plot average images

Averaging all images of a class produces a prototype. Similar prototypes predict which digits the model will confuse. Add this to your file:

```python
fig, axes = plt.subplots(1, 10, figsize=(18, 2))   # one panel per digit class
fig.suptitle("Average image per digit class", fontsize=12)
for digit, ax in enumerate(axes):
    # .mean(axis=0) averages across the SAMPLE dimension, leaving an 8x8 "prototype"
    mean_image = digits.images[digits.target == digit].mean(axis=0)
    ax.imshow(mean_image, cmap="gray_r")           # smooth, blurry shape = average of ~180 examples
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("average_digits.png")                  # save prototype grid for later comparison
plt.show()
```

Run your file and look at which digit pairs have the most similar prototypes. Common problem pairs: 1 vs 7, 3 vs 8, 4 vs 9.

---

## Step 6: Add the completion message

```python
print("\n--- Visualising Your Data — complete ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_visualise.py`) if anything looks different.
