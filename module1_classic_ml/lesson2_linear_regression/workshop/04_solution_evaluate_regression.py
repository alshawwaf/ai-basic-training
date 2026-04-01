import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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

print("=" * 60)
print("TASK 1 — Regression metrics on test set")
print("=" * 60)
# Manual calculation:
mse_manual  = np.mean((y_test.values - y_pred_test) ** 2)
rmse_manual = np.sqrt(mse_manual)
mae_manual  = np.mean(np.abs(y_test.values - y_pred_test))
r2_manual   = 1 - np.sum((y_test.values - y_pred_test)**2) / \
                  np.sum((y_test.values - y_test.mean())**2)
# sklearn verification:
mse_sk  = mean_squared_error(y_test, y_pred_test)
mae_sk  = mean_absolute_error(y_test, y_pred_test)
r2_sk   = r2_score(y_test, y_pred_test)
# Print all values with units
print(f"MSE:   {mse_manual:.1f} ms²")
print(f"RMSE:  {rmse_manual:.1f} ms")
print(f"MAE:   {mae_manual:.1f} ms")
print(f"R²:    {r2_manual:.3f}")
print(f"sklearn values match manual values: "
      f"{np.isclose(mse_manual, mse_sk) and np.isclose(r2_manual, r2_sk)}")

print("\n" + "=" * 60)
print("TASK 2 — Residual analysis")
print("=" * 60)
test_df = X_test.copy()
test_df['actual']    = y_test.values
test_df['predicted'] = y_pred_test
test_df['residual']  = y_test.values - y_pred_test
top5 = test_df.nlargest(5, 'residual')
print(top5.to_string(index=False))

print("\n" + "=" * 60)
print("TASK 3 — Security baseline anomaly detection")
print("=" * 60)
train_residuals = y_train.values - y_pred_train
sigma = np.std(train_residuals)
alert_threshold = 3 * sigma
test_residuals  = y_test.values - y_pred_test
flagged = np.sum(test_residuals > alert_threshold)
print(f"Training σ:             {sigma:.1f} ms")
print(f"Alert threshold (3σ):   {alert_threshold:.1f} ms")
print(f"Anomalies flagged:      {flagged} / {len(y_test)}")

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Threshold sensitivity analysis")
print("=" * 60)
print(f"{'k':>5} {'threshold':>14} {'flagged':>10} {'flag_rate':>10}")
print("-" * 45)
for k in np.arange(1.5, 4.1, 0.5):
    thresh  = k * sigma
    flagged = np.sum(test_residuals > thresh)
    rate    = flagged / len(test_residuals)
    print(f"{k:>5.1f} {thresh:>12.1f} ms {flagged:>8} {rate:>9.1%}")
