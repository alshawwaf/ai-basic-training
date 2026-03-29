# =============================================================================
# LESSON 1.1 | WORKSHOP | Exercise 5 of 5
# What the Model Actually Sees
# =============================================================================
#
# WHAT YOU WILL LEARN
# -------------------
# - How to print an image as a grid of raw numbers
# - Why the model sees numbers, not pictures (and why that matters)
# - How to identify which features carry the most information
# - How this structure maps directly to real security data (logs, packets)
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/exercise5_what_model_sees.py
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
# An ML model never "sees" an image, a log line, or a packet.
# It receives a flat row of numbers — always.
#
# Digits dataset:
#   One sample = [0, 0, 5, 13, 9, 1, 0, 0, 0, 0, 13, ...]   (64 numbers)
#   Label       = 0
#
# Network intrusion dataset:
#   One sample = [0.24, 1, 443, 1048576, 0, 2.1, ...]        (N numbers)
#   Label       = malicious
#
# The model sees the same structure. The domain changes; the math does not.
# Understanding this is the foundation for understanding every ML algorithm.


# =============================================================================
# TASK 1 — Print one image as its raw 8x8 number grid
# =============================================================================
#
# Pick the first image (index 0) and print it as an 8x8 grid of integers.
# Use digits.images[0] — this gives the 8x8 array form.
# Cast to int with .astype(int) for cleaner printing.
# Format each number as 2 characters wide so columns align.
#
# Hint: f"{v:2d}" formats an integer as exactly 2 characters wide.

# >>> YOUR CODE HERE
# print the label first, then loop over rows of the 8x8 image


# EXPECTED OUTPUT:
# Image index 0 — label: 0
#  0  0  5 13  9  1  0  0
#  0  0 13 15 10 15  5  0
#  0  3 15  2  0 11  8  0
#  0  4 12  0  0  8  8  0
#  0  5  8  0  0  9  8  0
#  0  4 11  0  1 12  7  0
#  0  2 14  5 10 12  0  0
#  0  0  6 13 10  0  0  0
#
# This is the entire input the model receives for this sample.
# 64 numbers. Nothing else.


# =============================================================================
# TASK 2 — Print examples of each digit as number grids
# =============================================================================
#
# Print the raw 8x8 grid for one example of digit 1 and one example of digit 7.
# Use: digits.images[digits.target == digit][0]
#
# After printing both, answer for yourself:
#   Which pixels are clearly different between 1 and 7?
#   Could you write a rule to separate them? (e.g. "if pixel_X > 8 ...")

# >>> YOUR CODE HERE


# EXPECTED OUTPUT (approximate):
# --- Digit 1 ---
#  0  0  0  3 15 12  2  0
#  0  0  0 14 15  2  0  0
#  ...
#
# --- Digit 7 ---
#  0  0  6 16  9  0  0  0
#  0  0 15 16  6  0  0  0
#  ...


# =============================================================================
# TASK 3 — Find the most informative pixels (correlation with target)
# =============================================================================
#
# Which pixels carry the most information about what digit is in the image?
# A pixel that is always 0 for digit 1 but always 16 for digit 7 is highly
# informative for separating those two classes.
#
# We can measure this roughly by computing the absolute correlation of each
# pixel column with the target label.
#
# Use: df.corr()["target"].abs().sort_values(ascending=False)
# Print the top 10 results (excluding "target" itself which will be 1.0).

# >>> YOUR CODE HERE


# EXPECTED OUTPUT (approximate):
# Top 10 pixels most correlated with digit label:
# pixel_43    0.55
# pixel_34    0.53
# pixel_26    0.52
# pixel_27    0.50
# ...
#
# WHAT THIS MEANS:
# pixel_43 is near the centre-right of the 8x8 grid (row 5, col 3).
# Pixels in the centre carry more information than corners (which are almost
# always blank). In Lesson 2.1 you will learn to engineer features like this
# deliberately instead of relying on raw pixels.


# =============================================================================
# TASK 4 — Visualise the most informative pixels (BONUS)
# =============================================================================
#
# Reshape the correlation values back into an 8x8 grid and plot them as a
# heatmap. Bright pixels = most informative for the model.
#
# Steps:
#   1. Get correlations for all pixel columns (not "target")
#   2. .values gives the raw array, .reshape(8, 8) makes it a grid
#   3. plt.imshow with cmap="hot" makes a heatmap

# >>> YOUR CODE HERE (optional)


# =============================================================================
# SECURITY ANALOGY
# =============================================================================
#
# In a network intrusion dataset the features might be:
#
#   bytes_sent, bytes_received, duration_sec, unique_dst_ports,
#   syn_flag_count, rst_flag_count, src_ip_entropy, packet_size_mean, ...
#
# The model receives exactly the same structure as above:
#   one flat row of numbers per connection, one label per connection.
#
# What changes between datasets:
#   - The number of features (64 pixels vs hundreds of network metrics)
#   - What the features represent (pixel brightness vs bytes sent)
#   - The number of classes (10 digits vs 2: malicious/benign)
#
# What stays exactly the same:
#   - The row-of-numbers structure
#   - The train/test split
#   - The loss-minimisation learning process
#   - All the algorithms you will use

print("\n=== Security Feature Analogy ===")
print("Digits:   [0, 0, 5, 13, 9, ...]  <- pixel brightnesses")
print("Network:  [1048576, 443, 0.24, 2, 14, ...]  <- bytes, port, duration, flags ...")
print("Same structure. Same algorithms. Different domain.")


# =============================================================================
# DONE — Workshop Complete
# =============================================================================
print("\n--- Exercise 5 complete ---")
print("You have completed all 5 exercises for Lesson 1.1.")
print("")
print("Next steps:")
print("  1. Open reference_solution.py to compare your code")
print("  2. Read the theory notes: ../1_what_is_ml.md")
print("  3. Move to Lesson 1.2: ../../../lesson2_linear_regression/")
