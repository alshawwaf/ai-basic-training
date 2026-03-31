# =============================================================================
# LESSON 1.2 | WORKSHOP | Exercise 3 of 4
# Fit and Predict
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How model.fit() finds the best slope and intercept
# - How model.predict() applies the learned equation to new inputs
# - What the slope and intercept mean for server response time
# - How to visualise the fitted regression line
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson2_linear_regression/workshop/exercise3_fit_and_predict.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Dataset + split (do not modify) ----------------------------------------
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
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# LinearRegression.fit() uses the Ordinary Least Squares method to find the
# slope and intercept that minimise the total squared error between predictions
# and actual values. For our server data:
#
#   response_time_ms = slope * requests_per_second + intercept
#
# After fitting you can access:
#   model.coef_[0]       — the slope (change in ms per 1 rps increase)
#   model.intercept_     — the intercept (ms when rps = 0)
#
# model.predict(X_new) applies the equation to any new array of X values.
# The input must be 2D: shape (n_samples, n_features).

# =============================================================================
# TASK 1 — Fit the Model and Inspect Parameters
# =============================================================================
# Create a LinearRegression model, fit it on X_train and y_train.
# Then print the slope and intercept with units.
# Add a comment interpreting what each parameter means physically.

print("=" * 60)
print("TASK 1 — Fit the model, inspect slope and intercept")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model = LinearRegression()
#   model.fit(X_train, y_train)
#   slope = model.coef_[0]
#   intercept = model.intercept_
#   print(f"Slope (coef):  {slope:.2f} ms per request/second")
#   print(f"Intercept:     {intercept:.2f} ms (baseline overhead)")

# EXPECTED OUTPUT:
# Slope (coef):  1.82 ms per request/second
# Intercept:     29.47 ms (baseline overhead)
# (Interpretation: each extra req/s adds ~1.82 ms; server needs ~29 ms even at idle)

# =============================================================================
# TASK 2 — Predict on the Test Set
# =============================================================================
# Use model.predict(X_test) to generate predictions.
# Build a small DataFrame with columns: 'actual', 'predicted', 'residual'
# where residual = actual - predicted.
# Print the first 5 rows.

print("\n" + "=" * 60)
print("TASK 2 — Predictions vs actuals (first 5 rows)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   y_pred = model.predict(X_test)
#   results = pd.DataFrame({
#       'actual':    y_test.values,
#       'predicted': y_pred,
#       'residual':  y_test.values - y_pred
#   })
#   print(results.head().to_string(index=False))

# EXPECTED OUTPUT:
#    actual  predicted  residual
#    ...       ...        ...
# (residuals should be small — mostly ±20 ms)

# =============================================================================
# TASK 3 — Predict at Specific Load Values
# =============================================================================
# Predict the response time at exactly 50, 100, and 150 requests/second.
# Print each prediction in a sentence: "At X rps: predicted Y ms"

print("\n" + "=" * 60)
print("TASK 3 — Predictions at specific load values")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   load_values = np.array([[50], [100], [150]])
#   predictions = model.predict(load_values)
#   for rps, ms in zip([50, 100, 150], predictions):
#       print(f"At {rps:3d} rps: predicted response time = {ms:.1f} ms")

# EXPECTED OUTPUT:
# At  50 rps: predicted response time = 120.5 ms
# At 100 rps: predicted response time = 211.5 ms
# At 150 rps: predicted response time = 302.5 ms

# =============================================================================
# TASK 4 (BONUS) — Visualise the Regression Line
# =============================================================================
# Create a scatter plot of the test set (X_test vs y_test) with alpha=0.4.
# Overlay the regression line in red:
#   - Create x_line = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
#   - Predict y_line = model.predict(x_line)
#   - Plot as a red line
# Add labels, a legend, and a title.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Regression line visualisation")
print("=" * 60)

# >>> YOUR CODE HERE

# EXPECTED OUTPUT:
# Scatter plot with a red regression line through the data cloud.

print("\n--- Exercise 3 complete. Move to exercise4_evaluate_regression.py ---")
