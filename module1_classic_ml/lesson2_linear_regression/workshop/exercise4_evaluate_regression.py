# =============================================================================
# LESSON 1.2 | WORKSHOP | Exercise 4 of 4
# Evaluate Regression and Build a Security Baseline
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to compute MSE, RMSE, MAE, and R² and interpret them
# - How to analyse residuals to check model health
# - How to convert a regression model into an anomaly detector
# - How changing the alert threshold affects false-positive rate
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson2_linear_regression/workshop/exercise4_evaluate_regression.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# --- Dataset + split + fit (do not modify) ----------------------------------
np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
X = df[["requests_per_second"]]
y = df["response_time_ms"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred_train = model.predict(X_train)
y_pred_test  = model.predict(X_test)
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# After fitting a model we need to know HOW GOOD it is. Four metrics matter:
#
#   MSE   = mean of (actual - predicted)^2    [units: ms^2]
#   RMSE  = sqrt(MSE)                          [units: ms]  ← most interpretable
#   MAE   = mean of |actual - predicted|       [units: ms]  ← robust to outliers
#   R²    = 1 - SS_residual / SS_total         [0 to 1]    ← fraction explained
#
# A residual is (actual - predicted). Large positive residuals mean the server
# was MUCH SLOWER than expected — a potential DoS indicator.
# We use the standard deviation of TRAINING residuals to set an alert threshold.

# =============================================================================
# TASK 1 — Calculate All Four Metrics
# =============================================================================
# Compute MSE, RMSE, MAE, and R² for the TEST set.
# First compute manually using numpy, then verify with sklearn functions.
# Print all values clearly with units.

print("=" * 60)
print("TASK 1 — Regression metrics on test set")
print("=" * 60)

# >>> YOUR CODE HERE
# Manual calculation:
#   mse_manual  = np.mean((y_test.values - y_pred_test) ** 2)
#   rmse_manual = np.sqrt(mse_manual)
#   mae_manual  = np.mean(np.abs(y_test.values - y_pred_test))
#   r2_manual   = 1 - np.sum((y_test.values - y_pred_test)**2) / \
#                     np.sum((y_test.values - y_test.mean())**2)
#
# sklearn verification:
#   mse_sk  = mean_squared_error(y_test, y_pred_test)
#   mae_sk  = mean_absolute_error(y_test, y_pred_test)
#   r2_sk   = r2_score(y_test, y_pred_test)
#
# Print all values with a label and units.

# EXPECTED OUTPUT:
# MSE:   ~228 ms²
# RMSE:  ~15.1 ms
# MAE:   ~12.0 ms
# R²:    ~0.973
# sklearn values match manual values: True

# =============================================================================
# TASK 2 — Residual Analysis
# =============================================================================
# Compute residuals for the test set: residuals = y_test - y_pred_test
# Print:
#   - mean residual (should be near 0)
#   - std of residuals
# Plot a histogram of residuals with 30 bins.
# Print the 5 observations with the LARGEST POSITIVE residuals (most anomalous).

print("\n" + "=" * 60)
print("TASK 2 — Residual analysis")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint for top anomalies:
#   test_df = X_test.copy()
#   test_df['actual']    = y_test.values
#   test_df['predicted'] = y_pred_test
#   test_df['residual']  = y_test.values - y_pred_test
#   top5 = test_df.nlargest(5, 'residual')
#   print(top5.to_string(index=False))

# EXPECTED OUTPUT:
# Mean residual: ~0.0 ms
# Std residual:  ~15.1 ms
# Top 5 largest positive residuals:
#  rps     actual  predicted  residual
#  ...      ...      ...        ...

# =============================================================================
# TASK 3 — Build the Security Baseline (3σ Alert Threshold)
# =============================================================================
# 1. Compute training residuals: y_train - y_pred_train
# 2. Compute the standard deviation of training residuals (sigma)
# 3. Set alert_threshold = 3 * sigma
# 4. Flag test observations where residual > alert_threshold
# 5. Print: sigma, alert_threshold, number of flagged observations

print("\n" + "=" * 60)
print("TASK 3 — Security baseline anomaly detection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   train_residuals = y_train.values - y_pred_train
#   sigma = np.std(train_residuals)
#   alert_threshold = 3 * sigma
#   test_residuals  = y_test.values - y_pred_test
#   flagged = np.sum(test_residuals > alert_threshold)
#   print(f"Training σ:             {sigma:.1f} ms")
#   print(f"Alert threshold (3σ):   {alert_threshold:.1f} ms")
#   print(f"Anomalies flagged:      {flagged} / {len(y_test)}")

# EXPECTED OUTPUT:
# Training σ:             ~15.2 ms
# Alert threshold (3σ):   ~45.6 ms
# Anomalies flagged:      ~2 / 100

# =============================================================================
# TASK 4 (BONUS) — Threshold Sensitivity Table
# =============================================================================
# Vary k from 1.5 to 4.0 in steps of 0.5.
# For each k, compute threshold = k * sigma and count how many test observations
# are flagged (residual > threshold).
# Print a formatted table: k | threshold (ms) | flagged | flag_rate

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Threshold sensitivity analysis")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print(f"{'k':>5} {'threshold':>14} {'flagged':>10} {'flag_rate':>10}")
#   print("-" * 45)
#   for k in np.arange(1.5, 4.1, 0.5):
#       thresh  = k * sigma
#       flagged = np.sum(test_residuals > thresh)
#       rate    = flagged / len(test_residuals)
#       print(f"{k:>5.1f} {thresh:>12.1f} ms {flagged:>8} {rate:>9.1%}")

# EXPECTED OUTPUT:
#     k      threshold    flagged  flag_rate
# -----------------------------------------------
#   1.5          22.8 ms       14     14.0%
#   2.0          30.4 ms        7      7.0%
#   2.5          38.0 ms        4      4.0%
#   3.0          45.6 ms        2      2.0%
#   3.5          53.2 ms        1      1.0%
#   4.0          60.8 ms        0      0.0%

print("\n--- Exercise 4 complete. Lesson 1.2 workshop done! ---")
print("--- Next: module1_classic_ml/lesson3_logistic_regression/ ---")
