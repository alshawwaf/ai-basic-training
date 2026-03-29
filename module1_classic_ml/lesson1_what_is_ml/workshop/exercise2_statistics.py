# =============================================================================
# LESSON 1.1 | WORKSHOP | Exercise 2 of 5
# Inspecting Your Data — Shape and Statistics
# =============================================================================
#
# WHAT YOU WILL LEARN
# -------------------
# - How to check shape, data types, and value ranges
# - How to use .describe() to get summary statistics in one call
# - How to check for missing values (critical in real-world security data)
# - Why you should always do this before writing a single line of model code
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/exercise2_statistics.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

# Setup — dataset already loaded for you so you can focus on the tasks
digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target


# =============================================================================
# BACKGROUND
# =============================================================================
#
# Checking statistics is not optional — it is the first thing every experienced
# data scientist does. Common problems caught here:
#
#   - Wrong number of rows (data loaded incorrectly)
#   - Wildly different scales across features (breaks many algorithms)
#   - NaN values that will cause silent failures
#   - Values that make no physical sense (negative bytes, port 99999)
#
# In security data these problems are extremely common because logs come from
# multiple sensors with inconsistent formats, dropped fields, and sensor gaps.


# =============================================================================
# TASK 1 — Print shape and class information
# =============================================================================
#
# Print:
#   - Number of samples (rows)
#   - Number of features (columns, excluding target)
#   - The list of unique class labels

# >>> YOUR CODE HERE


# EXPECTED OUTPUT:
# Samples  : 1797
# Features : 64
# Classes  : [0 1 2 3 4 5 6 7 8 9]


# =============================================================================
# TASK 2 — Print value range
# =============================================================================
#
# Pixel values in this dataset range from 0 (white) to 16 (black ink).
# Print the min and max across the entire features array.
# Use digits.data.min() and digits.data.max()

# >>> YOUR CODE HERE


# EXPECTED OUTPUT:
# Pixel value range: min=0, max=16
# (0 = white background, 16 = maximum ink density)


# =============================================================================
# TASK 3 — Summary statistics with .describe()
# =============================================================================
#
# pandas .describe() returns count, mean, std, min, 25%, 50%, 75%, max
# for every numeric column in one call.
#
# To keep the output readable, only describe a few columns.
# Select columns: pixel_0, pixel_10, pixel_32, pixel_63, target

# >>> YOUR CODE HERE
# Create a subset DataFrame with those 5 columns and call .describe() on it
# Round the result to 2 decimal places with .round(2)


# EXPECTED OUTPUT (approximate):
#        pixel_0  pixel_10  pixel_32  pixel_63  target
# count  1797.00   1797.00   1797.00   1797.00 1797.00
# mean      0.00      5.77      5.19      0.00    4.49
# std       0.00      4.35      4.54      0.00    2.87
# min       0.00      0.00      0.00      0.00    0.00
# ...
#
# WHAT TO NOTICE:
# pixel_0 has mean=0 and std=0 — it never varies! Corner pixels are always
# white background. A feature that never changes carries zero information.
# You could safely drop it without affecting the model.


# =============================================================================
# TASK 4 — Check for missing values
# =============================================================================
#
# This dataset has no missing values — but checking is a habit you must build.
# In real security logs you will almost always find NaNs.
#
# Use df.isnull().sum() to count missing values per column,
# then .sum() again to get the total across all columns.

# >>> YOUR CODE HERE


# EXPECTED OUTPUT:
# Missing values per column (showing first 5):
# pixel_0    0
# pixel_1    0
# pixel_2    0
# pixel_3    0
# pixel_4    0
# dtype: int64
#
# Total missing values: 0
#
# WHAT WOULD YOU DO IF YOU FOUND MISSING VALUES?
# Options depend on how many and which features:
#   - Drop rows with missing values (if few)
#   - Fill with median or mean (simple)
#   - Fill with a model prediction (advanced)
#   - Keep as a separate category (sometimes "missing" is informative itself)


# =============================================================================
# BONUS — Find the least and most informative pixels
# =============================================================================
#
# Standard deviation of 0 means a feature never changes — it's useless.
# Print the 5 pixels with the LOWEST std and the 5 with the HIGHEST std.
# Use df.drop(columns=["target"]).std().sort_values()

# >>> YOUR CODE HERE (optional — try this after completing tasks 1-4)


# EXPECTED OUTPUT (approximate):
# 5 least variable pixels (std near 0 = useless features):
# pixel_0     0.00
# pixel_8     0.00
# pixel_63    0.00
# ...
#
# 5 most variable pixels (std highest = most informative features):
# pixel_43    5.80
# pixel_34    5.72
# ...


# =============================================================================
# DONE
# =============================================================================
print("\n--- Exercise 2 complete. Move to exercise3_class_balance.py ---")
