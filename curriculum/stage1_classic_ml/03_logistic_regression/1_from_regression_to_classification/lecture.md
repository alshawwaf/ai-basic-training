# Exercise 1 — From Regression to Classification

> Back to [README.md](README.md)

## What You Will Learn

- Why linear regression fails for classification tasks
- What the sigmoid (logistic) function does and why it solves the problem
- How logistic regression outputs probabilities between 0 and 1
- How to plot the sigmoid curve and interpret it

---

## Concept: Why Linear Regression Fails for Classification

> **Want to go deeper?** [Logistic regression — Wikipedia](https://en.wikipedia.org/wiki/Logistic_regression)

Suppose you try to predict whether a URL is phishing (1) or legitimate (0) using linear regression. The model would predict numbers like 0.3, 0.7, 1.2, -0.1 — numbers outside the valid 0–1 probability range, and there is no natural way to convert 1.2 into "definitely phishing."

The problems with using linear regression for binary outcomes:

| Problem | Explanation |
|---------|-------------|
| Unbounded output | Predictions can be < 0 or > 1, which are not valid probabilities |
| Sensitive to outliers | A single extreme x-value can pull the line and reverse predictions |
| Poor fit | The true relationship between features and class probability is usually an S-curve, not a line |
| No built-in threshold | You have to arbitrarily pick a cutoff (e.g., ŷ > 0.5 = phishing) |

<div class="lecture-visual">
  <img src="/static/lecture_assets/logreg_linear_fails.png" alt="Scatter plot of legitimate URLs at y=0 and phishing URLs at y=1, with a violet LinearRegression line that crosses below 0 on the left and above 1 on the right; red shaded regions mark the invalid zones with arrow annotations">
  <div class="vis-caption">Real <code>LinearRegression</code> fit on a binary target. The line escapes the [0, 1] band on both ends — you cannot read those values as probabilities. This is exactly the failure mode the sigmoid fixes.</div>
</div>

---

## Concept: The Sigmoid Function

Logistic regression squashes any real number into the range (0, 1) using the **sigmoid function**:

```
σ(z) = 1 / (1 + e^(-z))
```

Where `z = w₀ + w₁x₁ + w₂x₂ + ...` is the linear combination of features (exactly what linear regression computes).

| Input z | Output σ(z) | Interpretation |
|---------|-------------|----------------|
| -5 | 0.007 | Very likely legitimate |
| -2 | 0.119 | Probably legitimate |
|  0 | 0.500 | Completely uncertain |
| +2 | 0.881 | Probably phishing |
| +5 | 0.993 | Almost certainly phishing |

The sigmoid produces an **S-curve**: near 0 for very negative `z`, near 1 for very positive `z`, passing through `0.5` at `z = 0`. Pictured another way, it's a flat floor on the left, a steep climb in the middle, and a flat ceiling on the right — every linear score gets mapped into the `(0, 1)` band.

<div class="lecture-visual">
  <img src="/static/lecture_assets/logreg_sigmoid.png" alt="The sigmoid S-curve drawn in cyan from z=-8 to z=+8 with five violet marker dots at z=-5, -2, 0, 2, 5 labelled with their probabilities 0.01, 0.12, 0.50, 0.88, 0.99; the left half is shaded cyan (predict legitimate) and the right half red (predict phishing)">
  <div class="vis-caption">The sigmoid plotted from <code>z = np.linspace(-8, 8, 400)</code>. Five sample points show how every <code>z</code> maps to a probability between 0 and 1. <code>z = 0</code> is the decision boundary.</div>
</div>

| `z` (linear score) | `σ(z)` (probability) | Side of the decision boundary | Predicted class |
|---:|---:|---|---|
| −5 | 0.007 | well left of 0 | **legitimate** |
| −1 | 0.269 | left of 0 | legitimate |
| **0** | **0.500** | **decision boundary** | tie — model is maximally unsure |
| +1 | 0.731 | right of 0 | phishing |
| +5 | 0.993 | well right of 0 | **phishing** |

Reading the table left-to-right walks you up the S-curve: floor → ramp → ceiling. The default rule "predict phishing when `p ≥ 0.5`" is equivalent to "predict phishing when `z ≥ 0`".

---

## Concept: From Probability to Class Label

Once we have a probability `p = σ(z)`, we need a rule to make a binary decision:

```
if p >= threshold:
    predict "phishing" (1)
else:
    predict "legitimate" (0)
```

The default threshold is **0.5**. But in security you often want to be more aggressive:
- A lower threshold (e.g., 0.3) catches more phishing but produces more false positives
- A higher threshold (e.g., 0.7) is more conservative: fewer false positives, but misses more phishing

Threshold tuning is explored in Exercise 4.

---

## Concept: What Logistic Regression Is Really Doing

Despite the name, logistic regression is a **classification** algorithm. It:

1. Computes a linear score: `z = w₀ + w₁·url_length + w₂·num_dots + ...`
2. Passes `z` through the sigmoid: `p = σ(z)` → probability of phishing
3. Classifies based on threshold: `1 if p >= 0.5 else 0`

The model learns the weights `w` during training by maximising the likelihood of the observed labels — a process called **maximum likelihood estimation** (equivalent to minimising log-loss).

**Logistic regression pipeline — one URL flowing through the model**

| Stage | What it holds | Worked example |
|---|---|---|
| 1. **Features** (raw inputs) | the numbers you measured | `url_length=120`, `num_dots=5`, `has_at=1` |
| 2. **Linear score `z`** (weighted sum) | `w₀ + w₁·url_length + w₂·num_dots + …` | `z = 2.1` |
| 3. **Sigmoid `σ(z)`** (probability) | squashes `z` into `(0, 1)` | `p = 0.89` |
| 4. **Decision** (class label) | `1` if `p ≥ 0.5` else `0` | `1` → **phishing** |

Steps 1–2 are exactly what linear regression does. Step 3 is the only thing logistic regression adds, and step 4 is a thresholding rule the user controls.

---

## What Each Task Asks You to Do

### Task 1 — Show Why Linear Regression Fails
Generate 20 artificial data points (url_length and label). Fit a LinearRegression. Print predictions for extreme inputs (url_length = 5 and url_length = 500). Show that some predictions are < 0 or > 1.

### Task 2 — Plot the Sigmoid Function
Create an array `z = np.linspace(-8, 8, 200)`. Compute `sigmoid(z) = 1 / (1 + np.exp(-z))`. Plot the S-curve with axis labels and a horizontal dashed line at 0.5.

### Task 3 — Demonstrate Logistic Regression Output
Create a simple 1-feature logistic regression (feature: url_length). Fit it, then call `predict_proba()` on 5 example URLs. Print the probability of phishing for each.

### Task 4 (BONUS) — Decision Boundary
For the 1-feature model, find and print the url_length at which the model is exactly 50% uncertain (the decision boundary). This is where `z = 0`, so `url_length = -intercept / coef`.

---

## Expected Outputs

```
TASK 1 — Linear regression failures:
Prediction for url_length=5:   -0.12  ← below 0, invalid probability!
Prediction for url_length=500:  1.34  ← above 1, invalid probability!

TASK 2 — Sigmoid plot:
(S-curve plot displayed)

TASK 3 — Logistic regression probabilities:
url_length=20:  P(phishing)=0.08  → legitimate
url_length=50:  P(phishing)=0.31  → legitimate
url_length=80:  P(phishing)=0.62  → phishing
url_length=120: P(phishing)=0.89  → phishing
url_length=200: P(phishing)=0.99  → phishing

TASK 4 (BONUS):
Decision boundary: url_length = 74.3
(URLs longer than 74 characters are flagged as phishing by this simple model)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `predict()` instead of `predict_proba()` | Gets 0/1 labels, not probabilities | Use `predict_proba()[:, 1]` for positive class probability |
| Forgetting `[:, 1]` on `predict_proba()` | Returns both columns (P(0) and P(1)) | Index `[:, 1]` to get P(phishing) |
| Confusing sigmoid input (z) with probability (p) | Misinterpretation | z is the linear score; p = σ(z) is the probability |
| Applying `np.exp` to very large z | Overflow warning | `scipy.special.expit` handles this safely |
