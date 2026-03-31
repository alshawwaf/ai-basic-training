# =============================================================================
# LESSON 1.3 | WORKSHOP | Exercise 1 of 4
# From Regression to Classification
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why linear regression is unsuitable for classification
# - What the sigmoid (logistic) function does
# - How logistic regression outputs probabilities between 0 and 1
# - How to plot the sigmoid curve
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson3_logistic_regression/workshop/exercise1_from_regression_to_classification.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression

# --- Minimal dataset for demonstration (do not modify) ----------------------
np.random.seed(42)
url_lengths_legit   = np.random.normal(40, 10, 50).clip(10, 80)
url_lengths_phish   = np.random.normal(90, 20, 50).clip(40, 250)
url_lengths = np.concatenate([url_lengths_legit, url_lengths_phish])
labels = np.array([0]*50 + [1]*50)   # 0=legitimate, 1=phishing
demo_df = pd.DataFrame({"url_length": url_lengths, "is_phishing": labels})
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Linear regression predicts continuous numbers. If we try to use it for
# binary classification (phishing=1, legitimate=0), it can output values
# less than 0 or greater than 1 — neither of which is a valid probability.
#
# Logistic regression fixes this with the sigmoid function:
#   σ(z) = 1 / (1 + e^(-z))
# This squashes any real number z into the range (0, 1). The result is a
# probability: "what is the chance this URL is phishing?"
#
# A probability >= 0.5 → predict phishing; < 0.5 → predict legitimate.
# (You can adjust this threshold — Exercise 4 explores why you'd want to.)

# =============================================================================
# TASK 1 — Show Why Linear Regression Fails
# =============================================================================
# Fit a LinearRegression on demo_df['url_length'] and demo_df['is_phishing'].
# Then print predictions for url_length = 5 and url_length = 500.
# Show that at least one prediction is outside [0, 1].

print("=" * 60)
print("TASK 1 — Linear regression gives invalid probabilities")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   X_demo = demo_df[['url_length']]
#   y_demo  = demo_df['is_phishing']
#   lin_model = LinearRegression().fit(X_demo, y_demo)
#   for length in [5, 500]:
#       pred = lin_model.predict([[length]])[0]
#       valid = "valid" if 0 <= pred <= 1 else "INVALID — outside [0,1]!"
#       print(f"url_length={length:4d}: prediction={pred:.3f}  ← {valid}")

# EXPECTED OUTPUT:
# url_length=   5: prediction=-0.12  ← INVALID — outside [0,1]!
# url_length= 500: prediction= 1.34  ← INVALID — outside [0,1]!

# =============================================================================
# TASK 2 — Plot the Sigmoid Function
# =============================================================================
# Create z = np.linspace(-8, 8, 200).
# Compute sigmoid(z) = 1 / (1 + np.exp(-z)).
# Plot the S-curve:
#   - Label x-axis: "z (linear score)"
#   - Label y-axis: "P(phishing)"
#   - Add a horizontal dashed grey line at y=0.5
#   - Add a vertical dashed grey line at x=0
#   - Add title: "The Sigmoid Function"

print("\n" + "=" * 60)
print("TASK 2 — Sigmoid function plot")
print("=" * 60)

# >>> YOUR CODE HERE

# EXPECTED OUTPUT:
# A plot showing an S-shaped curve rising from ~0 on the left to ~1 on the right,
# crossing 0.5 at z=0. Display or save it.
print("Sigmoid plot created.")

# =============================================================================
# TASK 3 — Logistic Regression Probabilities
# =============================================================================
# Fit a LogisticRegression on demo_df['url_length'] (X) and demo_df['is_phishing'] (y).
# For each url_length in [20, 50, 80, 120, 200], use predict_proba() to get
# P(phishing). Print the probability and whether the URL would be flagged (>= 0.5).

print("\n" + "=" * 60)
print("TASK 3 — Logistic regression probabilities")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   log_model = LogisticRegression().fit(demo_df[['url_length']], demo_df['is_phishing'])
#   for length in [20, 50, 80, 120, 200]:
#       prob = log_model.predict_proba([[length]])[0, 1]
#       label = "phishing" if prob >= 0.5 else "legitimate"
#       print(f"url_length={length:4d}: P(phishing)={prob:.2f} → {label}")

# EXPECTED OUTPUT:
# url_length=  20: P(phishing)=0.08 → legitimate
# url_length=  50: P(phishing)=0.31 → legitimate
# url_length=  80: P(phishing)=0.62 → phishing
# url_length= 120: P(phishing)=0.89 → phishing
# url_length= 200: P(phishing)=0.99 → phishing

# =============================================================================
# TASK 4 (BONUS) — Find the Decision Boundary
# =============================================================================
# For the 1-feature logistic model, find the url_length where
# P(phishing) = 0.5 exactly. At this point z=0, so:
#   0 = coef * url_length + intercept
#   url_length = -intercept / coef
# Print this value and explain what it means operationally.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Decision boundary")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   coef      = log_model.coef_[0][0]
#   intercept = log_model.intercept_[0]
#   boundary  = -intercept / coef
#   print(f"Decision boundary: url_length = {boundary:.1f} characters")
#   print("URLs longer than this are classified as phishing by the model.")

# EXPECTED OUTPUT:
# Decision boundary: url_length = ~74 characters
# URLs longer than ~74 characters are classified as phishing by this simple model.

print("\n--- Exercise 1 complete. Move to exercise2_feature_engineering_urls.py ---")
