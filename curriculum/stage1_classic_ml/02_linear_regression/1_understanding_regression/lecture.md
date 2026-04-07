# Exercise 1 — Understanding Regression

> Back to [README.md](README.md)

## What You Will Learn

- The difference between regression and classification problems
- When to choose regression over classification
- How to inspect a dataset before modelling
- How to create a scatter plot and visually judge whether a linear relationship exists

---

## Concept: Regression vs Classification

> **Want to go deeper?** [Linear regression — Wikipedia](https://en.wikipedia.org/wiki/Linear_regression)

Machine learning problems divide into two broad types depending on what you are trying to predict.

| Property | Regression | Classification |
|----------|-----------|----------------|
| Output | A continuous number | A category / label |
| Example output | 145 ms response time | "attack" or "benign" |
| Error metric | MSE, RMSE, MAE, R² | Accuracy, F1, AUC |
| Sklearn class | `LinearRegression` | `LogisticRegression`, `DecisionTreeClassifier` |

**Security examples:**

| Task | Type | Why |
|------|------|-----|
| Predict server response time | Regression | Output is a millisecond value |
| Classify a URL as phishing or not | Classification | Output is one of two labels |
| Estimate bytes exfiltrated | Regression | Output is a byte count |
| Flag a login as fraudulent | Classification | Output is a yes/no decision |

The rule of thumb: if you can put your output on a number line and care about *how far off* you are, use regression. If you only care about *which bucket* the output falls into, use classification.

|  | **Regression** | **Classification** |
|---|---|---|
| Output type   | continuous number on a line (e.g. *0 ms → 300 ms*) | one of a fixed set of buckets (e.g. *"attack"* or *"benign"*) |
| Example prediction | predicted: **145.2 ms**, actual: **148.0 ms** | predicted: **"attack"** |
| Error means | distance from the truth (here: 2.8 ms) | right bucket or wrong bucket — no notion of "how far off" |

---

## Concept: The Server Response Time Dataset

This workshop uses a synthetic dataset representing a web server under varying load:

| Column | Type | Meaning |
|--------|------|---------|
| `requests_per_second` | Float | Number of HTTP requests arriving each second (the input feature) |
| `response_time_ms` | Float | Average response time in milliseconds (what we predict) |

The relationship is approximately linear: as load increases, response time rises proportionally — until the server saturates. In this dataset we keep load in the linear range (0–200 rps) so that linear regression is appropriate.

**Why this matters for security:** A trained baseline says "at X rps, the server should respond in Y ms ± Z ms". Any observation that deviates far beyond that band is suspicious — it could indicate a DoS flood, resource exhaustion, or a background process consuming CPU.

---

## Concept: Exploratory Data Analysis (EDA)

Before fitting any model you should understand your data:

1. **Shape** — how many rows and columns?
2. **Types** — are columns numeric or categorical?
3. **Summary statistics** — mean, min, max, standard deviation
4. **Missing values** — any NaN entries?
5. **Distribution** — does a scatter plot suggest linearity?

These steps catch problems early (e.g., outliers, wrong data types, missing values) and tell you whether your modelling assumption (linear relationship) is reasonable.

---

## Concept: Reading a Scatter Plot

A scatter plot of `requests_per_second` (x-axis) vs `response_time_ms` (y-axis) shows:

- **Positive linear trend** — points slope upward left to right → linear regression is appropriate
- **Curve** — suggests a polynomial or non-linear model
- **No pattern** — suggests the features are not predictive
- **Outliers** — individual points far from the main cloud; investigate before trusting them

For our server data you should see a clear positive trend with some Gaussian noise around a straight line — points start near `(0 rps, ~50 ms)` and rise steadily toward `(150 rps, ~280 ms)`, scattered loosely around an imaginary diagonal. The cloud is tight enough that you can mentally draw the best-fit line with a ruler, which is exactly what `LinearRegression` will do for you in the next exercise.

---

## What Each Task Asks You to Do

### Task 1 — Load and Inspect the Dataset
Generate the synthetic server dataset using the provided seed so your results match the expected output. Print the shape, data types, and first five rows. Count any missing values.

### Task 2 — Summary Statistics
Call `.describe()` on the DataFrame and print it. Then answer in a comment: what is the approximate average response time? What is the maximum requests per second in the dataset?

### Task 3 — Scatter Plot
Create a matplotlib scatter plot of `requests_per_second` vs `response_time_ms`. Add axis labels and a title. Save or show the figure. Visually judge whether a straight line would fit well — write your answer as a comment.

### Task 4 (BONUS) — Regression or Classification?
For each of three new security scenarios listed in the file, write a comment stating whether you would use regression or classification and why.

---

## Expected Outputs

```
Dataset shape: (500, 2)
Columns: ['requests_per_second', 'response_time_ms']
Dtypes:
 requests_per_second    float64
 response_time_ms       float64

First 5 rows:
   requests_per_second  response_time_ms
0                 ...              ...

Missing values: 0

Summary statistics:
       requests_per_second  response_time_ms
count           500.000000        500.000000
mean             ~100.0             ~210.0
...

Scatter plot saved/shown — upward trend visible.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Forgetting to set `np.random.seed()` | Different numbers each run; results don't match | Always set seed before generating data |
| Calling `.info()` instead of `.describe()` for stats | No numeric summaries | Use `.describe()` for statistics, `.info()` for dtypes |
| Plotting y on x-axis and x on y-axis | Misleading chart | Feature (input) → x-axis; target (output) → y-axis |
| Skipping EDA and jumping straight to modelling | Undetected issues corrupt the model | Always inspect data first |
