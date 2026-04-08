# Exercise 3 — Fit and Predict

> Back to [README.md](README.md)

## What You Will Learn

- How `model.fit()` works mathematically
- How `model.predict()` generates predictions
- What the slope and intercept mean in physical terms for server performance
- How to overlay the regression line on a scatter plot

---

## Concept: What model.fit() Does

> **Want to go deeper?** [Gradient descent — Wikipedia](https://en.wikipedia.org/wiki/Gradient_descent)

When you call `LinearRegression().fit(X_train, y_train)`, sklearn finds the slope and intercept that minimise the **sum of squared residuals** — the total squared distance between each actual value and the model's prediction.

For simple linear regression (one feature):

```
y_predicted = slope * x + intercept
```

**What `.fit()` is doing.** Imagine the scatter plot from the previous exercise. `.fit()` slides a straight line around the cloud, looking for the unique line where the **vertical gaps** between each point and the line — the **residuals** — are as small as possible overall. Concretely it minimises the sum of those gaps *squared*, so a few large misses are penalised much more than many small ones.

<div class="lecture-visual">
  <img src="/static/lecture_assets/lr_fit_residuals.png" alt="Scatter plot of 30 actual server data points with a red regression line; thin grey vertical lines connect each point to the line showing the residuals">
  <div class="vis-caption">Real fitted line on a 30-row sample. Each grey line is a residual — <code>.fit()</code> finds the slope and intercept that minimise the sum of all those (squared) lengths.</div>
</div>

Mathematically, sklearn solves:

```
minimise Σ (y_actual - (slope * x + intercept))²
```

This has a closed-form solution (the "normal equation") so no iteration is needed. After `.fit()`, the model stores:
- `model.coef_[0]` — the slope
- `model.intercept_` — the intercept (y-value when x = 0)

---

## Concept: Physical Meaning of Slope and Intercept

For our server model:

```
response_time_ms = slope * requests_per_second + intercept
```

| Parameter | Symbol | Physical meaning |
|-----------|--------|-----------------|
| `intercept` | b | Baseline response time when the server handles 0 requests/second (overhead, processing time) |
| `slope` | m | Additional milliseconds added per extra request per second |

**Example interpretation:** On the lab dataset the fit produces slope ≈ 1.82 and intercept ≈ 28.1, so the model says:
- At 0 rps the server needs ~28 ms of overhead (network stack, etc.)
- Each additional request per second adds ~1.82 ms
- At 100 rps: 1.82 × 100 + 28.1 ≈ 210 ms predicted

<div class="lecture-visual">
  <img src="/static/lecture_assets/lr_slope_intercept.png" alt="Fitted regression line in red with a violet dot at x=0 marking the intercept (28.1 ms) and a cyan rise/run triangle from 100 to 150 rps showing the slope of 1.82 ms per rps">
  <div class="vis-caption">Real fitted line. Violet = where the line crosses x=0 (intercept). Cyan triangle = rise/run, showing every +50 rps adds ≈ +91 ms.</div>
</div>

**Reading the equation `response_time ≈ 1.82 * requests_per_second + 28.1` as points on a line:**

| Requests/sec | Predicted response (ms) | What it represents |
|---:|---:|---|
| **0** | **28.1** | the **intercept** — baseline overhead with no traffic |
| 25 | 73.6 | |
| 50 | 119.0 | |
| 100 | 209.9 | |
| 150 | 300.8 | |

The gap between consecutive rows is exactly `25 × 1.82 ≈ 45.5 ms` — that constant gap *is* the **slope**. Every extra request per second adds `1.82 ms` to the predicted response time, no matter where on the line you stand.

This is far more interpretable than a black-box model — and that interpretability is why linear regression remains a valuable baseline.

---

## Concept: model.predict()

After fitting, `model.predict(X_new)` applies the learned equation to new data:

```python
# Predict for a new value
new_load = np.array([[150]])       # 150 requests/second
predicted_ms = model.predict(new_load)
```

You can also predict for the entire test set:
```python
y_pred = model.predict(X_test)    # returns an array of predictions
```

**`model.predict()` pipeline**

| Stage | Input | Learned equation | Output |
|---|---|---|---|
| Single value | `[[150]]` | `1.82 * 150 + 28.1` | `≈ 300.8 ms` |

The model carries the learned `slope` and `intercept` inside `.coef_` / `.intercept_`, and `predict()` is just plugging the new `X` into that equation row by row. Visually, calling `predict()` for `50`, `100`, and `150` rps just means dropping a finger onto the line at each x-value:

<div class="lecture-visual">
  <img src="/static/lecture_assets/lr_predict_points.png" alt="Fitted regression line with three cyan dots at x=50 119 ms, x=100 209.9 ms, and x=150 300.8 ms; dashed lines drop down to the x-axis and across to the y-axis">
  <div class="vis-caption">Three real <code>model.predict([[x]])</code> calls. Each dashed line shows how the prediction is read off the fitted line.</div>
</div>

The predictions are point estimates — no uncertainty bounds. Later you will learn about prediction intervals.

---

## Concept: Visualising the Regression Line

A regression line plot overlays the model's predictions on the scatter plot. The standard approach:

1. Create a range of x-values spanning the data range
2. Predict y for each x-value
3. Plot as a line over the scatter of actual data points

```python
x_line = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
y_line = model.predict(x_line)
plt.scatter(X_test, y_test, alpha=0.4, label="Actual")
plt.plot(x_line, y_line, color="red", label="Predicted")
```

Points **above** the line have longer-than-predicted response times — worth investigating for performance issues.

---

## What Each Task Asks You to Do

### Task 1 — Fit the Model
Create a `LinearRegression` instance, fit it on `X_train` and `y_train`. Print the slope and intercept. Write a comment interpreting both values in terms of server performance.

### Task 2 — Make Predictions
Call `model.predict(X_test)` to generate predictions for the test set. Print the first 5 actual values and their corresponding predictions side by side.

### Task 3 — Predict Specific Load Values
Use `model.predict()` to answer: what response time does the model predict at 50, 100, and 150 requests/second? Print each prediction.

### Task 4 (BONUS) — Visualise the Regression Line
Plot the test set as a scatter and overlay the fitted regression line. Add axis labels, a legend, and a title. Save or display the figure.

---

## Expected Outputs

```
TASK 1 — Model parameters:
Slope (coef):     1.82 ms per request/second
Intercept:        29.47 ms (baseline overhead)
Interpretation:   Each extra request/second adds ~1.82 ms response time

TASK 2 — First 5 predictions vs actuals:
   Actual   Predicted   Residual
0   210.3     207.1       3.2
1   ...

TASK 3 — Predictions at specific loads:
At  50 rps: predicted response time = 120.5 ms
At 100 rps: predicted response time = 211.5 ms
At 150 rps: predicted response time = 302.5 ms
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Passing a 1D array to `predict()` | `ValueError: Expected 2D array` | Use `.reshape(-1, 1)` or double brackets `[[value]]` |
| Forgetting to fit before predict | `NotFittedError` | Always call `.fit()` before `.predict()` |
| Fitting on test data | Data leakage — optimistic results | Fit on `X_train` only |
| Interpreting slope without units | Meaningless number | Always include units in interpretation |
