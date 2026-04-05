# Lesson 1.3 — Logistic Regression

---

## Concept: Yes or No Decisions

Linear regression predicts a number. Logistic regression predicts a **probability** and then converts it into a binary decision: 0 or 1, yes or no, malicious or benign.

```
P(phishing) = sigmoid( w₁×url_length + w₂×num_dots + ... + bias )
```

The sigmoid function squashes any number into the range [0, 1], making it interpretable as a probability:

The sigmoid curve maps any linear score to a probability between 0 and 1:

| Linear score | Sigmoid output | Interpretation |
|-------------|---------------|----------------|
| Very negative | Near 0.0 | Very likely legitimate |
| Near 0 | 0.5 | Decision boundary — uncertain |
| Very positive | Near 1.0 | Very likely phishing |

```
sigmoid(x) = 1 / (1 + e^(-x))
```

If P(phishing) > 0.5 → classify as phishing.

---

## Real-Life Example: Phishing URL Detector

A phishing URL often has telltale signs:
- Very long URL (to hide the real domain)
- Many dots (e.g. paypal.verify.account.evil.com)
- Contains `@` symbol (browser ignores everything before `@`)
- Uses an IP address instead of a domain name
- Has many hyphens in the domain

We extract these as features and train a model to classify URLs as phishing (1) or legitimate (0).

---

## Key Concepts

### Decision Boundary
The model learns a line (in 2D) or hyperplane (in many dimensions) that separates the two classes. Everything on one side = phishing, the other = legit.

### Probability vs Hard Label
```python
model.predict_proba(X)   # returns [P(legit), P(phishing)] for each sample
model.predict(X)         # returns 0 or 1 (uses 0.5 threshold by default)
```

You can lower the threshold (e.g. 0.3) to catch more phishing — at the cost of more false positives. This tradeoff will be discussed in Lesson 1.5.

### Feature Coefficients
```python
model.coef_   # positive = increases P(phishing), negative = decreases it
```

This tells you which features matter most — great for explaining your detector to non-technical stakeholders.

---

## Key sklearn API

Say you have extracted features from 5,000 URLs — each row has `url_length`, `num_dots`, `has_at_symbol`, and similar columns. Half are phishing (label=1), half are legitimate (label=0). Here's how you train and apply the classifier:

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]   # probability of being phishing
```

---

## What to Notice When You Run It

1. The classification report — precision, recall, F1 (explained fully in Lesson 1.5)
2. Feature coefficients — which URL features are most suspicious?
3. The confusion matrix — how many phishing URLs slipped through?

---

## Next Lesson

**[Lesson 1.4 — Decision Trees](../04_decision_trees/README.md):** A different kind of classifier that works more like an explicit set of rules — great for interpretability.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

# Lesson 1.3 — Workshop Guide
## Phishing URL Classifier

> Read first: [README.md](README.md)
> Reference: Each exercise has a matching solution file (e.g. `solve_...py`)

## What This Workshop Covers

In this workshop you will build a logistic regression classifier that distinguishes phishing URLs from legitimate ones. You will move from linear regression's continuous outputs to classification's probability outputs, engineer security-relevant features from URL metadata, evaluate your model with a proper classification report and confusion matrix, and then tune the decision threshold to match operational priorities (catching every phish vs minimising analyst alert fatigue).

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_from_regression_to_classification/lecture.md) | [handson.md](1_from_regression_to_classification/handson.md) | What makes it classification, the sigmoid function, probability outputs |
| 2 | [lecture.md](2_feature_engineering_urls/lecture.md) | [handson.md](2_feature_engineering_urls/handson.md) | Why URL features matter for phishing detection, dataset creation and inspection |
| 3 | [lecture.md](3_train_and_evaluate/lecture.md) | [handson.md](3_train_and_evaluate/handson.md) | LogisticRegression, StandardScaler, classification_report, confusion matrix |
| 4 | [lecture.md](4_threshold_tuning/lecture.md) | [handson.md](4_threshold_tuning/handson.md) | predict_proba(), why 0.5 is not always right, precision-recall tradeoff |

## Running a Solution

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage1_classic_ml/03_logistic_regression/1_from_regression_to_classification/solution_logistic_regression.py
```

## Next Lesson

[Lesson 1.4 — Decision Trees](../../04_decision_trees/README.md)
