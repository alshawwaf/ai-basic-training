# Exercise 4 — Evaluate Regression and Build a Security Baseline

> Back to [00_overview.md](00_overview.md)

## What You Will Learn

- What MSE, RMSE, MAE, and R² measure and how to interpret each
- Why you need multiple metrics, not just one
- How to turn a regression model into a security anomaly detector
- How to set an alert threshold based on prediction residuals

---

## Concept: Error Metrics for Regression

> **Want to go deeper?** [Linear regression — Wikipedia](https://en.wikipedia.org/wiki/Linear_regression)

After fitting a model, you need to quantify how wrong it is. Four metrics are standard:

| Metric | Formula | Units | Interpretation |
|--------|---------|-------|----------------|
| **MSE** (Mean Squared Error) | mean((y - ŷ)²) | ms² | Penalises large errors heavily; hard to interpret |
| **RMSE** (Root MSE) | √MSE | ms | Same units as target; "average error magnitude" |
| **MAE** (Mean Absolute Error) | mean(\|y - ŷ\|) | ms | Robust to outliers; typical error size |
| **R²** (Coefficient of determination) | 1 - SS_res/SS_tot | unitless (0–1) | Fraction of variance explained; 1.0 = perfect |

**Which to use?**

- **RMSE** is the most common; directly comparable to your target's scale
- **MAE** if your data has outliers you don't want to over-penalise
- **R²** for a quick headline number (but can be misleading with few features)
- Always report at least two metrics

**For our server model:**
- RMSE ≈ 15 ms means predictions are off by ~15 ms on average
- R² ≈ 0.97 means the model explains 97% of response time variance

---

## Concept: Residual Analysis

A **residual** is `actual - predicted`. Examining residuals reveals:

| Residual pattern | Meaning | Action |
|-----------------|---------|--------|
| Randomly distributed around 0 | Good fit | None |
| Systematic curve (not random) | Non-linear relationship | Try polynomial features |
| Fan shape (variance grows with x) | Heteroscedasticity | Transform target (log) |
| Large individual residuals | Outliers | Investigate those observations |

In the security context, **large positive residuals** (actual >> predicted) are the most interesting: they mean the server is slower than expected, which could indicate an attack.

---

## Concept: Building a Security Baseline

Once the model is trained on normal traffic, it defines a **behavioural baseline**. The steps to turn it into an anomaly detector:

1. **Fit** the model on historical normal traffic
2. **Compute residuals** on new observations: `residual = actual - predicted`
3. **Calculate the standard deviation** of training residuals (σ)
4. **Set a threshold**: flag any observation where `residual > k * σ` (commonly k = 2 or 3)
5. **Alert** when a new observation exceeds the threshold

This is a statistical process control approach — the same idea as control charts used in manufacturing, now applied to network security.

```
Normal zone:     predicted ± 2σ
Warning zone:    predicted ± 3σ
Alert threshold: residual > 3σ  →  possible DoS / resource exhaustion
```

---

## Concept: Why 3σ?

Under a normal distribution, only 0.3% of observations naturally fall beyond 3 standard deviations. That means for every 1000 legitimate observations, you would expect ~3 false alarms. Lowering the threshold (e.g., 2σ) catches anomalies earlier but produces more false positives. Raising it (4σ) reduces false alarms but may miss subtle attacks. Tuning this threshold is the core of anomaly-based detection.

---

## What Each Task Asks You to Do

### Task 1 — Calculate All Four Metrics
Using `y_test` and `y_pred`, compute MSE, RMSE, MAE, and R² manually (using numpy) and then verify with sklearn's `mean_squared_error` and `r2_score`. Print all values with units.

### Task 2 — Residual Analysis
Compute residuals for the test set. Plot a histogram of residuals. Check whether they are approximately normally distributed (a good sign). Identify the 5 largest positive residuals.

### Task 3 — Build the Security Baseline
Using training residuals, compute σ (standard deviation). Set a 3σ threshold. Apply the threshold to test residuals and print how many observations are flagged as anomalies.

### Task 4 (BONUS) — Threshold Sensitivity
Vary k from 1.5 to 4.0 in steps of 0.5. For each k, print the threshold value (ms) and the number of test observations flagged. Build a small table to see the tradeoff.

---

## Expected Outputs

```
TASK 1 — Regression metrics:
MSE:   227.8 ms²
RMSE:  15.1 ms
MAE:   12.0 ms
R²:    0.973

TASK 2 — Residual analysis:
Mean residual: ~0.0 ms  (centred — good sign)
Std residual:  ~15.1 ms
Largest positive residuals (actual >> predicted):
  row 42: residual = +48.2 ms  (rps=143.1, actual=327.5, predicted=279.3)
  ...

TASK 3 — Security baseline (3σ threshold):
Training σ:  15.2 ms
Alert threshold (3σ):  45.6 ms
Anomalies flagged in test set: 2 / 100 (2.0%)

TASK 4 (BONUS) — Threshold sensitivity:
  k=1.5  threshold= 22.8 ms   flagged=14/100
  k=2.0  threshold= 30.4 ms   flagged= 7/100
  k=2.5  threshold= 38.0 ms   flagged= 4/100
  k=3.0  threshold= 45.6 ms   flagged= 2/100
  k=3.5  threshold= 53.2 ms   flagged= 1/100
  k=4.0  threshold= 60.8 ms   flagged= 0/100
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `mean_squared_error` for RMSE directly | Returns MSE, not RMSE | Take `np.sqrt(mse)` |
| Computing σ on test residuals | σ is contaminated by test set; leakage | Always compute σ on training residuals only |
| Reporting only R² | R² alone is misleading | Always report RMSE or MAE alongside R² |
| Setting k too low (k=1) | 32% false alarm rate | Use k=2 or k=3 in production |

---

> Back to [00_overview.md](00_overview.md) | Next lesson: [Lesson 1.3 Logistic Regression](../../lesson3_logistic_regression/workshop/00_overview.md)
