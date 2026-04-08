# Exercise 3 — Feature Importance

> Back to [README.md](README.md)

## What You Will Learn

- How `feature_importances_` is calculated
- Why `connection_rate` and `unique_dest_ports` dominate for network classification
- How to create a feature importance bar chart
- How to use importance scores to guide feature selection

---

## Concept: What feature_importances_ Measures

> **Want to go deeper?** [Decision tree learning — Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)

After training, `model.feature_importances_` is an array with one value per feature. Each value represents the total **information gain** contributed by that feature across all splits in the tree, normalised so all values sum to 1.0.

```python
feature_importances_ = [0.52, 0.28, 0.09, 0.07, 0.03, 0.01]
#                        ^                                ^
#                  most important                  least important
```

**Feature importance — which features drive predictions**

| Feature | Importance | Share of total |
|---|---:|---|
| `duration_seconds`  | **0.338** | dominant — splits exfil (long-lived) from everything else |
| `connection_rate`   | 0.337 | almost tied — splits DoS (very high) from everything else |
| `unique_dest_ports` | 0.317 | almost tied — splits port_scan from benign |
| `failed_connections`| 0.004 | barely used |
| `bytes_sent`        | 0.002 | barely used |
| `bytes_received`    | 0.002 | barely used |
| **Sum**             | **1.000** | importances are normalised |

Notice the structure: three features carry **99% of the tree's predictive power** and the remaining three are essentially decoration. That is a real and useful discovery — feature engineering often produces a dataset where a small subset of features does almost all the work.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_feature_importance.png" alt="Horizontal bar chart of decision tree feature_importances_. Three large red bars at the top: duration_seconds 0.338, connection_rate 0.337, unique_dest_ports 0.317. Three tiny cyan bars at the bottom: failed_connections 0.004, bytes_sent 0.002, bytes_received 0.002">
  <div class="vis-caption">Real <code>model.feature_importances_</code> from the trained lab tree. Three features account for ~99% of the tree's gain — the other three barely register.</div>
</div>

This is also called the **Mean Decrease in Impurity (MDI)**. A feature that appears near the root (where it improves the split most) accumulates more importance.

**What it does NOT tell you:**
- Whether the relationship is positive or negative
- Whether a feature's effect is linear or non-linear
- Whether the feature would be important in a different model

---

## Concept: Why These Features Matter for Network Security

| Feature | Expected importance | Reason |
|:---|:---|:---|
| `duration_seconds` | Very high | Exfil sessions last minutes; DoS connections are extremely brief |
| `connection_rate` | Very high | DoS is characterised by extreme rate; benign and scans are much lower |
| `unique_dest_ports` | High | Port scanning contacts many ports; benign and exfil use very few |
| `bytes_sent` | Low | Highly correlated with the three features above; tree never needs it |
| `failed_connections` | Low | Mostly redundant with `unique_dest_ports` for port-scan detection |
| `bytes_received` | Low | Less discriminative; most classes receive some data |

This ranking is consistent with real-world network intrusion detection research. Features that model *behavioural patterns* (rate, direction asymmetry) tend to outperform raw packet fields.

---

## Concept: Using Importance for Feature Selection

If you are building a production sensor that needs to run on limited hardware, you might keep only the top-3 features and retrain:

```python
top3 = importance_df.nlargest(3, 'importance')['feature'].tolist()
X_train_small = X_train[top3]
X_test_small  = X_test[top3]
model_small = DecisionTreeClassifier(max_depth=4).fit(X_train_small, y_train)
```

If the accuracy drop is small (< 2%), the simpler model is often preferred in production.

**Feature selection — keep top-3, retrain**

| Model | Features kept | Accuracy | Notes |
|---|---|---:|---|
| Full | all 6 | **91.0%** | baseline |
| Top-3 | `duration_seconds`, `connection_rate`, `unique_dest_ports` | 90.5% | only 0.5 pp lower |

For a production sensor running on limited hardware, the simpler model is almost always preferred — losing half a percentage point of accuracy is a fair trade for halving the feature pipeline.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_top3_comparison.png" alt="Two-bar comparison of test accuracy. Cyan bar 'Full (6 features)' at 0.910 and red bar 'Top-3 (duration_seconds, connection_rate, unique_dest_ports)' at 0.905. Title: dropping 3 features costs only 0.5 pp">
  <div class="vis-caption">Same train/test split, two models. Dropping the three barely-used features costs 0.5 pp of test accuracy — a clear win for production.</div>
</div>

---

## What Each Task Asks You to Do

### Task 1 — Print Feature Importances
Extract `model.feature_importances_` and create a DataFrame of (feature, importance) pairs, sorted descending. Print it. Verify that importances sum to 1.0.

### Task 2 — Plot the Importance Bar Chart
Create a horizontal bar chart of feature importances (most important at top). Colour bars by rank (use a gradient). Add value labels on each bar.

### Task 3 — Retrain with Top-3 Features Only
Keep only the 3 most important features. Retrain the tree. Compare accuracy to the full-feature model. Is the accuracy drop acceptable?

### Task 4 (BONUS) — Importance vs Security Knowledge
Look at the importances and the feature descriptions. Write a comment for each feature explaining whether the importance ranking makes intuitive sense from a network security standpoint.

---

## Expected Outputs

```
TASK 1 — Feature importances:
           feature  importance
  duration_seconds    0.338
   connection_rate    0.337
 unique_dest_ports    0.317
failed_connections    0.004
        bytes_sent    0.002
    bytes_received    0.002

Sum of importances: 1.000 ✓

TASK 2 — Bar chart created (horizontal, sorted).

TASK 3 — Top-3 features: ['duration_seconds', 'connection_rate', 'unique_dest_ports']
Full model accuracy:   0.910
Top-3 model accuracy:  0.905  (drop of 0.5%)
The 3 most important features retain 99.5% of the model's predictive power.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Confusing importance with correlation | High importance ≠ linear correlation | They measure different things |
| Fitting on test data when retraining | Data leakage | Always fit on X_train only |
| Assuming importance = causation | Can lead to misleading conclusions | Feature importance shows what the model uses, not real-world cause |
| Ignoring features with low importance | Some low-importance features interact with others | Check accuracy with/without them before discarding |
