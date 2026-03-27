# Lesson 1.2 — Linear Regression
#
# Goal: Predict server response time (ms) from requests per second.
# Security use case: model baseline server behaviour so deviations
# (e.g. sudden latency spikes) can be flagged as potential DoS attacks.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ── 1. Generate synthetic server load data ─────────────────────────────────────
np.random.seed(42)
n_samples = 300

requests_per_second = np.random.uniform(10, 500, n_samples)

# Response time increases linearly with load + realistic noise
# True relationship: ~2.5 ms per req/s, 50 ms baseline
response_time_ms = (2.5 * requests_per_second
                    + np.random.normal(0, 25, n_samples)
                    + 50)

df = pd.DataFrame({
    'requests_per_second': requests_per_second,
    'response_time_ms': response_time_ms
})

print("=== Dataset preview ===")
print(df.describe().round(1))

# ── 2. Prepare and split ───────────────────────────────────────────────────────
X = df[['requests_per_second']]   # 2D array — sklearn expects this shape
y = df['response_time_ms']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)} | Test samples: {len(X_test)}")

# ── 3. Train ───────────────────────────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)

r2   = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n=== Model Parameters ===")
print(f"Coefficient : {model.coef_[0]:.3f} ms per req/s")
print(f"Intercept   : {model.intercept_:.1f} ms (baseline at zero load)")

print("\n=== Performance ===")
print(f"R² Score : {r2:.4f}  (1.0 = perfect fit)")
print(f"RMSE     : {rmse:.1f} ms  (average prediction error)")

# ── 5. Security application: baseline & anomaly threshold ─────────────────────
print("\n=== Security Baseline ===")
for load in [50, 100, 200, 400]:
    predicted = model.predict([[load]])[0]
    threshold = predicted * 3   # flag anything 3x above predicted as anomalous
    print(f"  {load:>4} req/s → expected {predicted:.0f} ms | "
          f"anomaly threshold: {threshold:.0f} ms")

print("\nIf actual response time exceeds the threshold, investigate for DoS / resource exhaustion.")

# ── 6. Plot ────────────────────────────────────────────────────────────────────
x_line = np.linspace(X_test['requests_per_second'].min(),
                     X_test['requests_per_second'].max(), 200).reshape(-1, 1)
y_line = model.predict(x_line)

plt.figure(figsize=(10, 5))
plt.scatter(X_test, y_test, alpha=0.4, color='steelblue', label='Actual (test set)')
plt.plot(x_line, y_line, color='crimson', linewidth=2, label='Linear regression fit')
plt.xlabel('Requests per Second')
plt.ylabel('Response Time (ms)')
plt.title('Server Response Time vs Traffic Load')
plt.legend()
plt.tight_layout()
plt.savefig('stage1_ml/lesson2_linear_regression.png')
plt.show()
print("\nPlot saved to stage1_ml/lesson2_linear_regression.png")
