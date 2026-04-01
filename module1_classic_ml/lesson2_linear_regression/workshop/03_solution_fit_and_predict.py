import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

print("=" * 60)
print("TASK 1 — Fit the model, inspect slope and intercept")
print("=" * 60)

model = LinearRegression()
model.fit(X_train, y_train)
slope     = model.coef_[0]
intercept = model.intercept_
print(f"Slope (coef):  {slope:.2f} ms per request/second")
print(f"Intercept:     {intercept:.2f} ms (baseline overhead)")

print("\n" + "=" * 60)
print("TASK 2 — Predictions vs actuals (first 5 rows)")
print("=" * 60)

y_pred = model.predict(X_test)
results = pd.DataFrame({
    'actual':    y_test.values,
    'predicted': y_pred,
    'residual':  y_test.values - y_pred
})
print(results.head().round(1).to_string(index=False))

print("\n" + "=" * 60)
print("TASK 3 — Predictions at specific load values")
print("=" * 60)

load_values = np.array([[50], [100], [150]])
predictions = model.predict(load_values)
for rps, ms in zip([50, 100, 150], predictions):
    print(f"At {rps:3d} rps: predicted response time = {ms:.1f} ms")

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Regression line visualisation")
print("=" * 60)

x_line = np.linspace(X.min().values[0], X.max().values[0], 200).reshape(-1, 1)
y_line = model.predict(x_line)

plt.figure(figsize=(8, 5))
plt.scatter(X_test, y_test, alpha=0.4, label="Actual (test set)")
plt.plot(x_line, y_line, color="red", linewidth=2, label="Model prediction")
plt.xlabel("Requests per Second")
plt.ylabel("Response Time (ms)")
plt.title("Server Load vs Response Time — Regression Line")
plt.legend()
plt.tight_layout()
plt.show()

print("\n--- Exercise 3 complete. Move to exercise4_evaluate_regression.py ---")
