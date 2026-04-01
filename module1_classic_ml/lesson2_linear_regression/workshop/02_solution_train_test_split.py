import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Generate the same synthetic server-load dataset (seed ensures reproducibility)
np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
# X must be a 2D DataFrame (double brackets) — sklearn expects a matrix, not a 1D series
X = df[["requests_per_second"]]
y = df["response_time_ms"]

print("=" * 60)
print("TASK 1 — Evaluating on training data (WRONG)")
print("=" * 60)

# BAD PRACTICE: training and evaluating on the same data inflates accuracy
# The model memorises the data, so R² looks great but tells us nothing about new data
model = LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)
print(f"R² on full dataset (train=test): {r2:.3f}")

print("\n" + "=" * 60)
print("TASK 2 — Train/test split shapes")
print("=" * 60)

# Hold out 20% of the data as a test set the model never sees during training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"X_train: {X_train.shape}   y_train: {y_train.shape}")
print(f"X_test:  {X_test.shape}    y_test:  {y_test.shape}")
# Sanity check: train + test should equal the original dataset size
total = len(X_train) + len(X_test)
print(f"Total rows: {total} {'✓' if total == 500 else '✗'}")

print("\n" + "=" * 60)
print("TASK 3 — Train vs Test R²")
print("=" * 60)

# CORRECT: train on train set, then score on both to compare
model2 = LinearRegression()
model2.fit(X_train, y_train)
train_r2 = model2.score(X_train, y_train)
test_r2  = model2.score(X_test,  y_test)
print(f"Training R²: {train_r2:.3f}")
print(f"Test R²:     {test_r2:.3f}")
# A large gap between train and test R² signals overfitting
print(f"Gap (overfit indicator): {abs(train_r2 - test_r2):.3f}")

print("\n--- Exercise 2 complete. Move to exercise3_fit_and_predict.py ---")
