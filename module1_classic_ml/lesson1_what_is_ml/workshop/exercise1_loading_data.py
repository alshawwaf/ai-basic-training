# =============================================================================
# LESSON 1.1 | WORKSHOP | Exercise 1 of 5
# Loading a Dataset
# =============================================================================
#
# WHAT YOU WILL LEARN
# -------------------
# - How to load a built-in dataset from scikit-learn
# - What a "Bunch" object is and how to access its fields
# - How to wrap raw data in a pandas DataFrame
# - The difference between features (X) and labels (y)
#
# HOW TO WORK THROUGH THIS
# ------------------------
# 1. Read the explanation in each section
# 2. Fill in the blocks marked with  # >>> YOUR CODE HERE
# 3. Run the file and check your output matches the EXPECTED OUTPUT shown
# 4. Move to exercise2_statistics.py when this runs cleanly
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/exercise1_loading_data.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.datasets import load_digits


# =============================================================================
# BACKGROUND
# =============================================================================
#
# The digits dataset contains 1,797 images of handwritten digits (0-9).
# Each image is 8 pixels wide and 8 pixels tall = 64 pixel values per image.
#
# This is the dataset structure every ML problem shares:
#
#   Features (X)  --  the measurements / inputs  (64 pixel values per image)
#   Labels   (y)  --  the correct answer          (which digit 0-9)
#
# In a security context:
#   Features = bytes_per_sec, unique_ports, entropy, protocol flags ...
#   Labels   = malicious / benign


# =============================================================================
# TASK 1 — Load the dataset
# =============================================================================
#
# load_digits() returns a "Bunch" object — a container with named fields.
# The fields you will use most are:
#
#   .data         -- shape (1797, 64)  the raw pixel values
#   .target       -- shape (1797,)     the correct label for each image
#   .images       -- shape (1797,8,8)  same pixels as 8x8 grids (for plotting)
#   .target_names -- array([0,1,...,9]) all possible class labels
#   .DESCR        -- a long text description of the dataset

# >>> YOUR CODE HERE
# Load the dataset and store it in a variable called `digits`


print("Dataset loaded.")
print(f"Type: {type(digits)}")
print(f"Fields available: {list(digits.keys())}")

# EXPECTED OUTPUT:
# Dataset loaded.
# Type: <class 'sklearn.utils._bunch.Bunch'>
# Fields available: ['data', 'target', 'target_names', 'images', 'DESCR']


# =============================================================================
# TASK 2 — Access the raw arrays
# =============================================================================
#
# Access the .data and .target fields and print their shapes.
# .shape returns a tuple: (rows, columns)

# >>> YOUR CODE HERE
# Print the shape of digits.data and digits.target


# EXPECTED OUTPUT:
# Features (X) shape: (1797, 64)
# Labels   (y) shape: (1797,)
#
# This means: 1797 samples, each with 64 features, and 1797 labels.


# =============================================================================
# TASK 3 — Wrap the data in a DataFrame
# =============================================================================
#
# A pandas DataFrame is like a spreadsheet — rows are samples, columns are features.
# It makes it much easier to inspect, slice, and describe your data.
#
# The column names should be: pixel_0, pixel_1, ..., pixel_63
# Hint: use an f-string inside a list comprehension:
#   [f"pixel_{i}" for i in range(64)]

# >>> YOUR CODE HERE
# Create a DataFrame called `df` from digits.data with the column names above
# Then add a column called "target" containing digits.target


print("\nFirst 3 rows of the DataFrame:")
print(df.head(3).to_string())
print(f"\nDataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")

# EXPECTED OUTPUT:
# First 3 rows of the DataFrame:
#    pixel_0  pixel_1  pixel_2  ...  pixel_63  target
# 0      0.0      0.0      5.0  ...       0.0       0
# 1      0.0      0.0      0.0  ...       0.0       1
# 2      0.0      0.0      0.0  ...       0.0       2
#
# DataFrame shape: (1797, 65)
# Columns: pixel_0 ... pixel_63, target  (65 total)


# =============================================================================
# TASK 4 — Inspect one sample
# =============================================================================
#
# Print the target label and first 10 pixel values of the very first row.

# >>> YOUR CODE HERE
# Print the label of the first sample (digits.target[0])
# Print the first 10 pixel values of the first sample (digits.data[0, :10])


# EXPECTED OUTPUT:
# First sample — label: 0
# First 10 pixel values: [ 0.  0.  5. 13.  9.  1.  0.  0.]
#
# The label tells us the correct answer. The pixel values are what the model sees.


# =============================================================================
# DONE
# =============================================================================
print("\n--- Exercise 1 complete. Move to exercise2_statistics.py ---")
