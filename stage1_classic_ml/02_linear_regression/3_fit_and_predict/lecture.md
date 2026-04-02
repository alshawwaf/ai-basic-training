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

```
  What .fit() finds — the best line through the data

  response_time
  300 │             ·  ·       · ·
      │          ·  · ·  ·  ·
  200 │       · ·─────────────────── ← best-fit line
      │    · ·───·  ·
  100 │  ·───· ·          residual = actual - predicted
      │──·                    │
      └───────────────────────┼──── requests_per_second
                              ▼
              .fit() minimises the sum of all
              squared residuals (vertical gaps)
```

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

**Example interpretation:** If slope = 1.82 and intercept = 29.5, the model says:
- At 0 rps the server needs ~30 ms of overhead (network stack, etc.)
- Each additional request per second adds ~1.82 ms
- At 100 rps: 1.82 × 100 + 29.5 = 211.5 ms predicted

```
  response_time = 1.82 * requests_per_second + 29.5

  ms
  350 │                              /
      │                            /
  300 │                          /  ← slope = 1.82 ms per extra rps
      │                        /
  250 │                      /
      │                    /
  200 │                  /
      │                /
  150 │              /
      │            /
  100 │          /
      │        /
   50 │      /
  29.5│..../ ← intercept (baseline overhead at 0 rps)
      └──────────────────────────────────
       0    25   50   75  100  125  150  rps
```

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

```
  model.predict() pipeline

  ┌────────────────┐     ┌─────────────────────────┐     ┌──────────────┐
  │   New X value  │────►│ slope * X + intercept    │────►│  Prediction │
  │   [[150]]      │     │ 1.82 * 150 + 29.5       │     │   302.5 ms   │
  └────────────────┘     └─────────────────────────┘     └──────────────┘
       input                  learned equation               output
```

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

---

> Next: [../4_evaluate_regression/lecture.md](../4_evaluate_regression/lecture.md)
