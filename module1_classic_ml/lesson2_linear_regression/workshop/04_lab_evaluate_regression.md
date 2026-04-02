# Lab -- Exercise 4: Evaluate Regression and Build a Security Baseline

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_evaluate_regression.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
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
```

---

## Step 4: Calculate All Four Metrics

Compute MSE, RMSE, MAE, and R² for the TEST set. First compute manually using numpy, then verify with sklearn functions. Print all values clearly with units.

Add this to your file:

```python
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
```

Run your file. You should see:
```
MSE:   ~228 ms²
RMSE:  ~15.1 ms
MAE:   ~12.0 ms
R²:    ~0.973
sklearn values match manual values: True
```

---

## Step 5: Residual Analysis

Compute residuals for the test set (`residual = actual - predicted`). Print the mean residual (should be near 0), the standard deviation, and the 5 largest positive residuals (actual >> predicted).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Residual analysis")
print("=" * 60)
test_df = X_test.copy()
test_df['actual']    = y_test.values
test_df['predicted'] = y_pred_test
test_df['residual']  = y_test.values - y_pred_test
top5 = test_df.nlargest(5, 'residual')
print(top5.to_string(index=False))
```

Run your file. You should see:
```
Mean residual: ~0.0 ms
Std residual:  ~15.1 ms
Top 5 largest positive residuals:
rps     actual  predicted  residual
...      ...      ...        ...
```

---

## Step 6: Build the Security Baseline (3σ Alert Threshold)

1. Compute training residuals: y_train - y_pred_train 2. Compute the standard deviation of training residuals (sigma) 3. Set alert_threshold = 3 * sigma

Add this to your file:

```python
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
```

Run your file. You should see:
```
Training σ:             ~15.2 ms
Alert threshold (3σ):   ~45.6 ms
Anomalies flagged:      ~2 / 100
```

---

## Step 7: TASK 4 (BONUS) — Threshold Sensitivity Table

Vary k from 1.5 to 4.0 in steps of 0.5. For each k, compute threshold = k * sigma and count how many test observations are flagged (residual > threshold).

Add this to your file:

```python
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
```

Run your file. You should see:
```
k      threshold    flagged  flag_rate
-----------------------------------------------
1.5          22.8 ms       14     14.0%
2.0          30.4 ms        7      7.0%
2.5          38.0 ms        4      4.0%
3.0          45.6 ms        2      2.0%
3.5          53.2 ms        1      1.0%
4.0          60.8 ms        0      0.0%
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `04_solution_evaluate_regression.py` file if anything looks different.
