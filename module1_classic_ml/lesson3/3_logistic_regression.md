# Lesson 1.3 — Logistic Regression

**Script:** [3_logistic_regression.py](3_logistic_regression.py)

---

## Concept: Yes or No Decisions

Linear regression predicts a number. Logistic regression predicts a **probability** and then converts it into a binary decision: 0 or 1, yes or no, malicious or benign.

```
P(phishing) = sigmoid( w₁×url_length + w₂×num_dots + ... + bias )
```

The sigmoid function squashes any number into the range [0, 1], making it interpretable as a probability:

```
P(phishing)
  1.0 |                       ___________
      |                    ../
  0.8 |                  ./
      |                ./
  0.5 |_______________X_________________ <-- decision boundary
      |            ./
  0.2 |          ./
      |       ../
  0.0 |______/
      +-------+-------+-------+-------+-> linear score (features x weights)
           very          0          very
          legit                   suspicious
```

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

**[Lesson 1.4 — Decision Trees](4_decision_trees.md):** A different kind of classifier that works more like an explicit set of rules — great for interpretability.
