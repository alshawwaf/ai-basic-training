# =============================================================================
# LESSON 1.2 | WORKSHOP | Exercise 1 of 4
# Understanding Regression
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - The difference between regression and classification
# - When to use linear regression vs other model types
# - How to inspect a new dataset (shape, dtypes, missing values, stats)
# - How to create a scatter plot to judge whether a linear model is appropriate
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson2_linear_regression/workshop/exercise1_understanding_regression.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Dataset generation (do not modify) -------------------------------------
np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
# True relationship: response_time = 1.8 * rps + 30 + noise
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Linear regression predicts a continuous number (e.g., milliseconds) from one
# or more input features. It is the right choice when:
#   1. Your output is a real-valued number, not a category.
#   2. You expect a roughly linear relationship between inputs and output.
#   3. You want an interpretable model (slope + intercept have physical meaning).
#
# This dataset represents a web server under varying HTTP load. Each row is a
# one-second window. 'requests_per_second' is the feature; 'response_time_ms'
# is what we want to predict.
#
# A trained linear regression model will let us say: "given X requests/second,
# the server should respond in approximately Y ms". Observations far outside
# that prediction become anomaly candidates — possible DoS indicators.

# =============================================================================
# TASK 1 — Load and Inspect the Dataset
# =============================================================================
# Print the shape, column names, dtypes, first 5 rows, and count of missing values.
# The DataFrame 'df' is already created above — no loading from disk needed.

print("=" * 60)
print("TASK 1 — Dataset Inspection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint: use df.shape, df.columns, df.dtypes, df.head(), df.isnull().sum()

# EXPECTED OUTPUT:
# Dataset shape: (500, 2)
# Columns: Index(['requests_per_second', 'response_time_ms'], dtype='object')
# Dtypes:
#  requests_per_second    float64
#  response_time_ms       float64
# dtype: object
# First 5 rows:
#    requests_per_second  response_time_ms
# 0         ...                  ...
# Missing values:
# requests_per_second    0
# response_time_ms       0
# dtype: int64

# =============================================================================
# TASK 2 — Summary Statistics
# =============================================================================
# Call df.describe() and print the result.
# Then add a comment answering:
#   a) What is the approximate mean response time?
#   b) What is the maximum requests_per_second value?

print("\n" + "=" * 60)
print("TASK 2 — Summary Statistics")
print("=" * 60)

# >>> YOUR CODE HERE

# EXPECTED OUTPUT:
#        requests_per_second  response_time_ms
# count          500.000000        500.000000
# mean           ~103.0             ~215.0
# std             ~56.0              ~101.0
# min              ~5.0               ~35.0
# 25%             ~54.0              ~126.0
# 50%            ~103.0              ~218.0
# 75%            ~153.0              ~306.0
# max            ~200.0              ~397.0

# =============================================================================
# TASK 3 — Scatter Plot
# =============================================================================
# Create a scatter plot: x = requests_per_second, y = response_time_ms.
# - Use alpha=0.4 so overlapping points are visible
# - Add x-label: "Requests per Second"
# - Add y-label: "Response Time (ms)"
# - Add title: "Server Load vs Response Time"
# Then add a comment below: does the relationship look linear? Why or why not?

print("\n" + "=" * 60)
print("TASK 3 — Scatter Plot")
print("=" * 60)

# >>> YOUR CODE HERE

# EXPECTED OUTPUT:
# A scatter plot window opens showing a clear upward linear trend with noise.
# (If running headless, the figure will save instead of display.)

# =============================================================================
# TASK 4 (BONUS) — Regression or Classification?
# =============================================================================
# For each scenario below, decide: regression or classification? Write your
# reasoning as a comment next to each one.
#
# Scenario A: Predict the number of failed login attempts in the next hour.
# Scenario B: Decide whether a file is malware or benign.
# Scenario C: Estimate the dollar value of data stolen in a breach.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Regression or Classification?")
print("=" * 60)

# >>> YOUR CODE HERE
# Example format:
# scenario_a = "regression"  # because ...
# scenario_b = "classification"  # because ...
# scenario_c = "regression"  # because ...
# print(f"Scenario A: {scenario_a}")
# print(f"Scenario B: {scenario_b}")
# print(f"Scenario C: {scenario_c}")

print("\n--- Exercise 1 complete. Move to exercise2_train_test_split.py ---")
