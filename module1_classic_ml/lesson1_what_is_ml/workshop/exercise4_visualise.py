# =============================================================================
# LESSON 1.1 | WORKSHOP | Exercise 4 of 5
# Visualising Your Data
# =============================================================================
#
# WHAT YOU WILL LEARN
# -------------------
# - How to use matplotlib to plot image grids
# - Why you must visually inspect data before training
# - How to compute and plot average images per class
# - What "prototype" images reveal about model difficulty
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/exercise4_visualise.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

# Setup
digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target


# =============================================================================
# BACKGROUND
# =============================================================================
#
# Always look at your data before training. This applies equally to:
#   - Images       (are the labels correct? are there corrupted samples?)
#   - Network logs (do connection records look like real traffic?)
#   - Malware features (do feature values make physical sense?)
#
# Matplotlib is the standard plotting library. Key functions:
#
#   plt.subplots(rows, cols)     creates a grid of panels
#   ax.imshow(array, cmap=...)   renders a 2D array as an image
#   ax.set_title(text)           label above a panel
#   ax.axis("off")               hide tick marks and axis lines
#   plt.tight_layout()           auto-fix spacing between panels
#   plt.savefig("path.png")      save to disk
#   plt.show()                   display the window


# =============================================================================
# TASK 1 — Plot one sample image per class
# =============================================================================
#
# Create a 1-row, 10-column grid of panels.
# In each panel, show one example image of the corresponding digit.
# Title each panel with the digit number.
#
# Hint:
#   digits.images[digits.target == digit][0]  <- first image of this digit

# >>> YOUR CODE HERE
# fig, axes = plt.subplots(...)
# for digit in range(10):
#     ...


# WHAT TO LOOK FOR:
# - Are all digits clearly recognisable?
# - Any panel that looks ambiguous or unusual is a likely source of model errors.


# =============================================================================
# TASK 2 — Plot two examples per class
# =============================================================================
#
# Create a 2-row, 10-column grid.
# Row 0: first example of each digit
# Row 1: second example of each digit
#
# Notice how different two examples of the same digit can look.
# That variation is exactly what the model must learn to handle.

# >>> YOUR CODE HERE
# fig, axes = plt.subplots(2, 10, figsize=(18, 4))
# fig.suptitle("Two examples of each digit class (0-9)", fontsize=12)
# for digit in range(10):
#     samples = digits.images[digits.target == digit]
#     for row_idx, sample in zip(axes, samples[:2]):
#         ...

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/sample_digits.png")
plt.show()


# =============================================================================
# TASK 3 — Compute and plot average images
# =============================================================================
#
# Average all images of each digit class to produce one "prototype" per class.
# Two prototypes that look nearly identical = those digits will be confused most.
#
# Steps:
#   1. For each digit 0-9, filter all its images with: digits.images[digits.target == digit]
#   2. Call .mean(axis=0) to average across all images of that digit (axis=0 = across samples)
#   3. Plot the result in a 1x10 grid

# >>> YOUR CODE HERE
# fig, axes = plt.subplots(1, 10, figsize=(18, 2))
# for digit, ax in enumerate(axes):
#     mean_image = ...
#     ax.imshow(...)
#     ax.set_title(str(digit))
#     ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/average_digits.png")
plt.show()

# WHAT TO LOOK FOR:
# Which digit pairs have the most similar average shapes?
# Those pairs will produce the most confusion errors when the model is trained.
# Common problem pairs: 1 vs 7,  3 vs 8,  4 vs 9


# =============================================================================
# TASK 4 — Find the most visually similar class pair (BONUS)
# =============================================================================
#
# Quantify the similarity between average images using the mean absolute difference.
# Lower difference = more similar = harder to classify.
#
# Steps:
#   1. Compute average images for all 10 classes (store in a list or dict)
#   2. For every pair (i, j) where i < j, compute mean(abs(avg_i - avg_j))
#   3. Print the 3 most similar pairs

# >>> YOUR CODE HERE (optional)


# EXPECTED OUTPUT (approximate):
# 3 most similar digit pairs (by average image distance):
#   Digits 3 vs 8 : distance = 1.23
#   Digits 1 vs 7 : distance = 1.41
#   Digits 0 vs 6 : distance = 1.58
#
# These pairs will have the highest confusion rate when the model is trained.
# You can verify this in Lesson 1.5 when you inspect the confusion matrix.


# =============================================================================
# DONE
# =============================================================================
print("\n--- Exercise 4 complete. Move to exercise5_what_model_sees.py ---")
