# =============================================================================
# LESSON 1.2 | WORKSHOP | Exercise 2 of 4
# Train/Test Split
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why evaluating on training data gives falsely optimistic results
# - How to use train_test_split() correctly
# - How to verify your split has the right proportions
# - The concept of data leakage
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson2_linear_regression/workshop/exercise2_train_test_split.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Dataset (same as Exercise 1 — do not modify) ---------------------------
np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
X = df[["requests_per_second"]]   # 2D array (required by sklearn)
y = df["response_time_ms"]
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Before we can train a model we must split the data into a training set (what
# the model learns from) and a test set (what we use to evaluate how well it
# generalises to new, unseen data).
#
# The key rule: the model must NEVER see the test data during training.
# Violating this rule is called data leakage and produces metrics that look
# impressive on paper but fail in production.
#
# sklearn's train_test_split() shuffles the rows randomly (reproducibly when
# you set random_state) then splits them into the requested proportions.
# A typical split is 80% training, 20% testing.

# =============================================================================
# TASK 1 — Evaluate on Training Data (the Wrong Way)
# =============================================================================
# Fit a LinearRegression model on ALL 500 rows, then score it on the same 500.
# This is intentionally wrong — we want to see how misleadingly high the R²
# appears. Print: "R² on full dataset (train=test): X.XXX"

print("=" * 60)
print("TASK 1 — Evaluating on training data (WRONG)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = LinearRegression()
#   model.fit(X, y)
#   r2 = model.score(X, y)
#   print(f"R² on full dataset (train=test): {r2:.3f}")

# EXPECTED OUTPUT:
# R² on full dataset (train=test): 0.978

# =============================================================================
# TASK 2 — Perform the Train/Test Split
# =============================================================================
# Split X and y into X_train, X_test, y_train, y_test.
# Use test_size=0.2 and random_state=42.
# Print the shape of all four arrays and confirm that train + test = 500 rows.

print("\n" + "=" * 60)
print("TASK 2 — Train/test split shapes")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#   print(f"X_train: {X_train.shape}   y_train: {y_train.shape}")
#   print(f"X_test:  {X_test.shape}    y_test:  {y_test.shape}")
#   total = len(X_train) + len(X_test)
#   print(f"Total rows: {total} {'✓' if total == 500 else '✗'}")

# EXPECTED OUTPUT:
# X_train: (400, 1)   y_train: (400,)
# X_test:  (100, 1)   y_test:  (100,)
# Total rows: 500 ✓

# =============================================================================
# TASK 3 — Compare Train vs Test R²
# =============================================================================
# Fit a NEW LinearRegression model on X_train / y_train only.
# Compute R² on X_train (training score) and on X_test (test score).
# Print both values and the gap between them.
# A small gap means the model generalises well. A large gap means overfitting.

print("\n" + "=" * 60)
print("TASK 3 — Train vs Test R²")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model2 = LinearRegression()
#   model2.fit(X_train, y_train)
#   train_r2 = model2.score(X_train, y_train)
#   test_r2  = model2.score(X_test,  y_test)
#   print(f"Training R²: {train_r2:.3f}")
#   print(f"Test R²:     {test_r2:.3f}")
#   print(f"Gap (overfit indicator): {abs(train_r2 - test_r2):.3f}")

# EXPECTED OUTPUT:
# Training R²: 0.977
# Test R²:     0.973
# Gap (overfit indicator): 0.004

# =============================================================================
# TASK 4 (BONUS) — Stratified Split Exploration
# =============================================================================
# Create a boolean column 'high_load' (True if requests_per_second > 100).
# Compute the proportion of high_load rows in the full set.
# Then do a stratified split (stratify=df['high_load']) and verify that both
# train and test have approximately the same proportion of high_load rows.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Stratified split")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   df['high_load'] = df['requests_per_second'] > 100
#   print(f"High-load proportion in full set:  {df['high_load'].mean():.2%}")
#   X2 = df[['requests_per_second']]
#   y2 = df['response_time_ms']
#   X2_tr, X2_te, _, _ = train_test_split(X2, y2, test_size=0.2,
#                                          random_state=42, stratify=df['high_load'])
#   print(f"High-load proportion in train set: ...")
#   print(f"High-load proportion in test set:  ...")

# EXPECTED OUTPUT:
# High-load proportion in full set:  ~50%
# High-load proportion in train set: ~50%
# High-load proportion in test set:  ~50%

print("\n--- Exercise 2 complete. Move to exercise3_fit_and_predict.py ---")
