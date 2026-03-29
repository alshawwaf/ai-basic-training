# Lesson 1.1 — ML Concepts and Exploring Data
#
# GOAL: Before training any model, understand your data.
# A model is only as good as the data you feed it.
#
# We'll use scikit-learn's built-in digits dataset:
# 1,797 handwritten digit images (0-9), each stored as an 8x8 grid of
# pixel brightness values. No download needed — it ships with scikit-learn.
#
# Why this example?
#   - It's visual — you can literally see what the model will learn
#   - Same structure as any security classification problem:
#     raw measurements (pixels / log fields) -> label (digit / attack type)
#   - We'll revisit digits with a neural network in Module 3

# ── Imports ────────────────────────────────────────────────────────────────────

import numpy as np
# NumPy: the foundational library for working with arrays of numbers in Python.
# "np" is the universal shorthand alias — you'll see it in every ML codebase.
# We use it here for array operations (filtering, averaging pixel values).

import pandas as pd
# Pandas: gives us the DataFrame — a table of data (like a spreadsheet in Python).
# Each row = one image.  Each column = one feature (one pixel value).
# "pd" is the universal alias.
# Key methods we use: .shape, .head(), .value_counts(), .describe()

import matplotlib.pyplot as plt
# Matplotlib: Python's core plotting library.
# We import the "pyplot" sub-module and alias it as "plt".
# plt.imshow()   — display a 2D array as an image
# plt.subplots() — create a grid of plot panels
# plt.show()     — open the plot window
# plt.savefig()  — save the plot to a file

from sklearn.datasets import load_digits
# scikit-learn: the standard ML library in Python.
# load_digits() loads a famous dataset that ships bundled inside scikit-learn.
# No internet needed — the data is a file inside the installed package.


# ── 1. Load the dataset ────────────────────────────────────────────────────────

digits = load_digits()
# load_digits() returns a "Bunch" object — like a dictionary with named fields.
# Think of it as a container holding several related arrays:
#
#   digits.data    — shape (1797, 64)    — 1797 images, 64 pixel features each
#   digits.target  — shape (1797,)       — correct label for each image (0-9)
#   digits.images  — shape (1797, 8, 8)  — same pixels, kept as 8x8 grids
#   digits.target_names — [0, 1, 2, ..., 9]  — the list of class labels

# Wrap the raw data in a DataFrame so we can inspect and manipulate it easily.
df = pd.DataFrame(
    digits.data,                              # the 1797 x 64 array of pixel values
    columns=[f"pixel_{i}" for i in range(64)] # name each column pixel_0, pixel_1, ...
)
df["target"] = digits.target
# Add a column called "target" with the correct digit label (0-9) for each row.
# Now each row has 64 pixel features + 1 label.


# ── 2. First look at the data ──────────────────────────────────────────────────

print("=== Dataset shape ===")
# .shape returns a tuple: (number of rows, number of columns)
# shape[0] = rows = number of images
# shape[1] = columns = number of features per image
print(f"Images : {digits.data.shape[0]}")
print(f"Features per image : {digits.data.shape[1]}  (8x8 pixels, flattened into one row)")
print(f"Classes : {len(digits.target_names)}  -> {list(digits.target_names)}")

print("\n=== Class balance (how many examples of each digit) ===")
# value_counts() counts how many rows have each unique value in the "target" column.
# sort_index() sorts by the label value (0,1,2...) rather than by count.
# to_string() prints the full result (prevents pandas from truncating long output).
print(df["target"].value_counts().sort_index().to_string())
# If one class had far fewer examples than the others, the model would struggle to
# learn it. In security: 99% normal traffic + 1% attacks = class imbalance problem.

print("\n=== Pixel value range ===")
# .min() and .max() return the smallest and largest values across the entire array.
print(f"Min: {digits.data.min():.0f}  |  Max: {digits.data.max():.0f}  (0 = white, 16 = black)")


# ── 3. Visualise sample images ─────────────────────────────────────────────────
# Reminder: digits.images[i] is an 8x8 grid of numbers — not a real image file.
# plt.imshow() can display any 2D array of numbers as a heatmap or greyscale image.

fig, axes = plt.subplots(2, 10, figsize=(18, 4))
# subplots() creates a grid of blank plot panels.
# (2, 10) = 2 rows, 10 columns = 20 panels (2 examples per digit, 10 digits).
# figsize=(18, 4) = the whole figure is 18 inches wide, 4 inches tall.
# Returns: fig (the whole figure), axes (a 2x10 array of individual panels).

fig.suptitle("Sample images — two examples per digit", fontsize=12)
# suptitle() adds a title to the top of the whole figure (not a single panel).

for digit in range(10):
    # range(10) gives 0, 1, 2, ..., 9
    samples = digits.images[digits.target == digit]
    # digits.target == digit creates a True/False mask — True where label matches.
    # Applying it to digits.images filters to only images of this digit.
    # "samples" is now an array of all 8x8 images labelled as this digit.

    for row, sample in zip(axes, samples[:2]):
        # zip() pairs up two lists: axes[0] with sample[0], axes[1] with sample[1].
        # samples[:2] = first 2 examples of this digit.
        row[digit].imshow(sample, cmap="gray_r")
        # imshow() renders the 8x8 number grid as a greyscale picture.
        # cmap="gray_r" = reversed greyscale: high numbers (bright pixels) appear dark.
        row[digit].set_title(str(digit))  # label the panel with the digit
        row[digit].axis("off")            # hide the axis ticks and labels

plt.tight_layout()
# tight_layout() automatically adjusts spacing so panels don't overlap.

plt.savefig("module1_classic_ml/lesson1_sample_digits.png")
# Save the figure to disk so you can refer back to it later.
plt.show()
# Open the interactive plot window. Script pauses here until you close it.
print("\nPlot saved -> module1_classic_ml/lesson1_sample_digits.png")


# ── 4. Print one image as raw numbers ─────────────────────────────────────────
# This is the most important step for understanding what the model actually sees.
# A model never sees a picture — it sees a flat list of numbers.

print("\n=== One image as an 8x8 grid of pixel values ===")
print("(Each number is a pixel brightness: 0 = white, 16 = black)")
print()

sample_image = digits.images[0]
# digits.images[0] = the first image in the dataset, as an 8x8 NumPy array.

for row in sample_image.astype(int):
    # .astype(int) converts float values to integers (cleaner to print).
    # We loop over each row of the 8x8 grid and print it as a line of numbers.
    print("  " + "  ".join(f"{v:2d}" for v in row))
    # f"{v:2d}" formats each number as 2 characters wide, so columns line up neatly.

print(f"\n  ^ This is the digit '{digits.target[0]}'")
# digits.target[0] = the label for the first image — should be 0.


# ── 5. Visualise average images per class ─────────────────────────────────────
# Instead of one example, we average ALL images of each digit together.
# This gives us the "ideal" or "prototype" for each class.
# If two prototypes look very similar, the model will struggle to tell them apart.

fig, axes = plt.subplots(1, 10, figsize=(18, 2))
# 1 row, 10 columns — one panel per digit.

fig.suptitle("Average pixel pattern for each digit class", fontsize=12)

for digit, ax in enumerate(axes):
    # enumerate(axes) gives both the index (digit = 0,1,2...) and the panel (ax).

    mean_image = digits.images[digits.target == digit].mean(axis=0)
    # digits.target == digit  — filter to only images of this digit
    # .mean(axis=0)            — average across all those images, pixel by pixel
    # Result: one 8x8 array showing the average brightness at each pixel position.

    ax.imshow(mean_image, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_average_digits.png")
plt.show()
print("Plot saved -> module1_classic_ml/lesson1_average_digits.png")


# ── Key takeaways ──────────────────────────────────────────────────────────────
#
# 1. The model NEVER sees images — it sees rows of 64 numbers.
#    In security: bytes_per_second, unique_ports, entropy, protocol_flags — same idea.
#
# 2. Always check shape, class balance, and feature ranges before training.
#    Problems you miss here will silently break your model later.
#
# 3. Visualise your data. The average digit images show which classes are easy
#    (0 vs 1 look very different) and which are hard (3 vs 8 overlap more).
#
# Next lesson: we feed these features into our first ML model.
