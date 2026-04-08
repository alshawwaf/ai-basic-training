# Exercise 4 — Evaluate Regression and Build a Security Baseline

> Back to [README.md](README.md)

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

A healthy model produces residuals that are tightly centred on zero and randomly scattered (no curves, no fans):

<div class="lecture-visual">
  <img src="/static/lecture_assets/lr_residuals.png" alt="Left panel: histogram of training residuals shaped like a bell curve centred at zero. Right panel: scatter of residuals against predicted values showing a random cloud around the y=0 line">
  <div class="vis-caption">Real training residuals from the lab's fitted model. Left = roughly normal, centred on zero. Right = random scatter — no leftover pattern for the model to capture.</div>
</div>

**Reading residuals — `residual = actual - predicted`**

| Sign of residual | Position vs the regression line | What it means | Why you care |
|---|---|---|---|
| **Large positive** | well **above** the line | server is **slower** than the model expected | possible DoS, resource exhaustion, noisy neighbour — **investigate** |
| Near zero | sitting **on** the line | matches the baseline | normal traffic |
| **Large negative** | well **below** the line | server is **faster** than expected | usually benign — caching, low load, lucky retry |

---

## Concept: Building a Security Baseline

Once the model is trained on normal traffic, it defines a **behavioural baseline**. The steps to turn it into an anomaly detector:

1. **Fit** the model on historical normal traffic
2. **Compute residuals** on new observations: `residual = actual - predicted`
3. **Calculate the standard deviation** of training residuals (σ)
4. **Set a threshold**: flag any observation where `residual > k * σ` (commonly k = 2 or 3)
5. **Alert** when a new observation exceeds the threshold

This is a statistical process control approach — the same idea as control charts used in manufacturing, now applied to network security. Drawn on the scatter plot, the baseline is a band around the regression line: any point that pokes above the +3σ line is an anomaly worth investigating.

<div class="lecture-visual">
  <img src="/static/lecture_assets/lr_security_baseline.png" alt="Scatter plot of training data with the fitted regression line and a green ±3σ normal zone, an orange +2σ to +3σ warning band, and a dashed red +3σ alert threshold line; three red X marks above the threshold are labelled as anomalies">
  <div class="vis-caption">Real fitted line + ±3σ bands. Green = normal. Orange = warning. Above the dashed red line = alert. Three synthetic anomalies plotted as red X.</div>
</div>

**The bands around the regression line — measured in σ (standard deviations of the training residuals)**

| Distance from prediction | Zone | Meaning | Action |
|---|---|---|---|
| within ±2σ | **Normal** | typical variation around the baseline | ignore |
| ±2σ to ±3σ | **Warning** | unusual but not extreme | log, watch |
| beyond +3σ (above the line) | **Alert** | server far slower than predicted | possible DoS / resource exhaustion — page on-call |
| beyond −3σ (below the line) | rare | server far faster than predicted | almost always benign (cache hit, low load) |

The asymmetry matters — in security baselines, only the *upper* tail is interesting. A detector that fires on `residual > 3σ` follows exactly the same logic as a control chart in manufacturing quality control.

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
