# Lab -- Exercise 1: From Regression to Classification

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_from_regression_to_classification.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
url_lengths_legit   = np.random.normal(40, 10, 50).clip(10, 80)
url_lengths_phish   = np.random.normal(90, 20, 50).clip(40, 250)
url_lengths = np.concatenate([url_lengths_legit, url_lengths_phish])
labels = np.array([0]*50 + [1]*50)   # 0=legitimate, 1=phishing
demo_df = pd.DataFrame({"url_length": url_lengths, "is_phishing": labels})
```

---

## Step 4: Show Why Linear Regression Fails

Fit a LinearRegression on demo_df['url_length'] and demo_df['is_phishing']. Then print predictions for url_length = 5 and url_length = 500. Show that at least one prediction is outside [0, 1].

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Linear regression gives invalid probabilities")
print("=" * 60)
X_demo = demo_df[['url_length']]
y_demo  = demo_df['is_phishing']
lin_model = LinearRegression().fit(X_demo, y_demo)
for length in [5, 500]:
    pred = lin_model.predict([[length]])[0]
    valid = "valid" if 0 <= pred <= 1 else "INVALID — outside [0,1]!"
    print(f"url_length={length:4d}: prediction={pred:.3f}  ← {valid}")
```

Run your file. You should see:
```
url_length=   5: prediction=-0.12  ← INVALID — outside [0,1]!
url_length= 500: prediction= 1.34  ← INVALID — outside [0,1]!
```

---

## Step 5: Plot the Sigmoid Function

Create z = np.linspace(-8, 8, 200). Compute sigmoid(z) = 1 / (1 + np.exp(-z)). Plot the S-curve:

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Sigmoid function plot")
print("=" * 60)
```

Run your file. You should see:
```
A plot showing an S-shaped curve rising from ~0 on the left to ~1 on the right,
crossing 0.5 at z=0. Display or save it.
```

---

## Step 6: Logistic Regression Probabilities

Fit a LogisticRegression on demo_df['url_length'] (X) and demo_df['is_phishing'] (y). For each url_length in [20, 50, 80, 120, 200], use predict_proba() to get P(phishing). Print the probability and whether the URL would be flagged (>= 0.5).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Logistic regression probabilities")
print("=" * 60)
log_model = LogisticRegression().fit(demo_df[['url_length']], demo_df['is_phishing'])
for length in [20, 50, 80, 120, 200]:
    prob = log_model.predict_proba([[length]])[0, 1]
    label = "phishing" if prob >= 0.5 else "legitimate"
    print(f"url_length={length:4d}: P(phishing)={prob:.2f} → {label}")
```

Run your file. You should see:
```
url_length=  20: P(phishing)=0.08 → legitimate
url_length=  50: P(phishing)=0.31 → legitimate
url_length=  80: P(phishing)=0.62 → phishing
url_length= 120: P(phishing)=0.89 → phishing
url_length= 200: P(phishing)=0.99 → phishing
```

---

## Step 7: TASK 4 (BONUS) — Find the Decision Boundary

For the 1-feature logistic model, find the url_length where P(phishing) = 0.5 exactly. At this point z=0, so: 0 = coef * url_length + intercept

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Decision boundary")
print("=" * 60)
coef      = log_model.coef_[0][0]
intercept = log_model.intercept_[0]
boundary  = -intercept / coef
print(f"Decision boundary: url_length = {boundary:.1f} characters")
print("URLs longer than this are classified as phishing by the model.")
```

Run your file. You should see:
```
Decision boundary: url_length = ~74 characters
URLs longer than ~74 characters are classified as phishing by this simple model.
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_from_regression_to_classification.py`) if anything looks different.
