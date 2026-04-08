# Lab -- Exercise 3: Train and Evaluate the Phishing Classifier

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_train_and_evaluate.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: array math
import pandas as pd                         # pandas: tabular data
import matplotlib.pyplot as plt             # matplotlib: plotting
import seaborn as sns                       # seaborn: prettier statistical plots (heatmaps)
from sklearn.linear_model import LogisticRegression       # the classifier
from sklearn.preprocessing import StandardScaler          # zero-mean, unit-variance scaling
from sklearn.model_selection import train_test_split      # holdout-set helper
# classification_report = precision/recall/F1 table; confusion_matrix = TN/FP/FN/TP grid
from sklearn.metrics import classification_report, confusion_matrix
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n, half = 1000, 500
def make_urls(n_legit, n_phish):
    legit = pd.DataFrame({
        'url_length':     np.random.normal(45, 12, n_legit).clip(10, 100).astype(int),
        'num_dots':       np.random.poisson(2.1, n_legit),
        'has_at_symbol':  (np.random.rand(n_legit) < 0.05).astype(int),
        'uses_https':     (np.random.rand(n_legit) < 0.82).astype(int),
        'num_subdomains': np.random.poisson(0.8, n_legit),
        'has_ip_address': (np.random.rand(n_legit) < 0.02).astype(int),
        'num_hyphens':    np.random.poisson(0.3, n_legit),
        'path_length':    np.random.normal(15, 8, n_legit).clip(0, 60).astype(int),
        'is_phishing':    0
    })
    phish = pd.DataFrame({
        'url_length':     np.random.normal(98, 25, n_phish).clip(30, 250).astype(int),
        'num_dots':       np.random.poisson(4.8, n_phish),
        'has_at_symbol':  (np.random.rand(n_phish) < 0.31).astype(int),
        'uses_https':     (np.random.rand(n_phish) < 0.61).astype(int),
        'num_subdomains': np.random.poisson(2.5, n_phish),
        'has_ip_address': (np.random.rand(n_phish) < 0.21).astype(int),
        'num_hyphens':    np.random.poisson(2.1, n_phish),
        'path_length':    np.random.normal(48, 18, n_phish).clip(0, 150).astype(int),
        'is_phishing':    1
    })
    return pd.concat([legit, phish], ignore_index=True).sample(frac=1, random_state=42)
df = make_urls(half, half)
FEATURES = ['url_length', 'num_dots', 'has_at_symbol', 'uses_https',
            'num_subdomains', 'has_ip_address', 'num_hyphens', 'path_length']
X = df[FEATURES]                              # 2D feature matrix (8 columns)
y = df['is_phishing']                          # 1D label vector (0/1)
# stratify=y keeps the same class proportions in train and test (50/50 here)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Step 4: Scale the Features

Fit a StandardScaler on X_train, transform both X_train and X_test. Print the mean and std of the raw 'url_length' column vs the scaled version to confirm the transformation worked.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Feature scaling")
print("=" * 60)
scaler = StandardScaler()                          # learns mean + std from training data
X_train_scaled = scaler.fit_transform(X_train)     # fit AND transform on training set
X_test_scaled  = scaler.transform(X_test)          # NOTE: transform only — never fit on test!
#
# Compare raw vs scaled url_length to confirm the transformation worked
raw_col   = X_train['url_length']
scaled_col = X_train_scaled[:, 0]                  # url_length is first column in FEATURES
print(f"Raw url_length:    mean={raw_col.mean():.1f}, std={raw_col.std():.1f}")
# After scaling: mean ≈ 0, std ≈ 1 (the whole point of StandardScaler)
print(f"Scaled url_length: mean={scaled_col.mean():.2f}, std={scaled_col.std():.2f}")
```

Run your file. You should see:
```
Raw url_length:    mean=71.6, std=32.1
Scaled url_length: mean=0.00, std=1.00
```

---

## Step 5: Fit the Model and Print Coefficients

Fit LogisticRegression(max_iter=1000) on scaled training data. Print each feature's coefficient sorted by absolute magnitude (largest first). Add a comment identifying the most and least important features.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Model coefficients")
print("=" * 60)
# max_iter=1000 → give the optimiser enough steps to converge; random_state pins the result
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)             # learns one coefficient per feature
coef_df = pd.DataFrame({
    'feature': FEATURES,
    'coefficient': model.coef_[0]               # .coef_ has shape (1, n_features) for binary classification
}).sort_values('coefficient', key=abs, ascending=False)   # rank by magnitude, sign-agnostic
print(coef_df.to_string(index=False))
```

Run your file. You should see:
```
feature         coefficient
url_length          ~1.52   (positive → longer URLs → more phishing)
path_length         ~1.31
num_dots            ~0.98
...
uses_https          ~-0.61  (negative → HTTPS less common in phishing)
```

---

## Step 6: Classification Report and Confusion Matrix

Predict on X_test_scaled. Print: 1. classification_report with target_names=['legitimate', 'phishing'] 2. The confusion matrix as a heatmap (using seaborn or printing as a table)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Evaluation: classification report + confusion matrix")
print("=" * 60)
y_pred = model.predict(X_test_scaled)              # 0/1 predictions on the held-out 200 rows
# precision, recall, F1, support per class — all in one formatted table
print(classification_report(y_test, y_pred,
                             target_names=['legitimate', 'phishing']))
#
cm = confusion_matrix(y_test, y_pred)              # 2x2: rows=actual, cols=predicted
print("\nConfusion matrix:")
print("                Predicted Legit  Predicted Phishing")
# TN=true negative, FP=false positive (false alarm), FN=false negative (missed attack), TP=true positive
print(f"Actual Legit       {cm[0,0]:3d} (TN)         {cm[0,1]:3d} (FP)")
print(f"Actual Phish       {cm[1,0]:3d} (FN)         {cm[1,1]:3d} (TP)")
#
# Optional: seaborn heatmap (uncomment to visualise the confusion matrix as colour)
# sns.heatmap(cm, annot=True, fmt='d', xticklabels=['Legit','Phish'],
#             yticklabels=['Legit','Phish'])
# plt.show()
```

Run your file. You should see:
```
precision  recall  f1-score  support
legitimate       ~0.91    ~0.93     ~0.92     100
phishing         ~0.93    ~0.91     ~0.92     100
accuracy                            ~0.92     200
```

---

## Step 7: TASK 4 (BONUS) — Scaled vs Unscaled

Train a second LogisticRegression without scaling (use X_train directly). Compare accuracy on the test set. Note any ConvergenceWarning (set max_iter=100 for the unscaled model to see the warning).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Scaled vs unscaled comparison")
print("=" * 60)
import warnings
# Capture any ConvergenceWarning so we can show it instead of letting it spam stderr
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    # max_iter=100 deliberately too low → unscaled features will fail to converge
    model_unscaled = LogisticRegression(max_iter=100, random_state=42)
    model_unscaled.fit(X_train, y_train)        # raw features — no scaling
    if w:
        print(f"Warning: {w[-1].message}")
acc_scaled   = model.score(X_test_scaled, y_test)
acc_unscaled = model_unscaled.score(X_test, y_test)
print(f"Scaled model accuracy:   {acc_scaled:.3f}")
print(f"Unscaled model accuracy: {acc_unscaled:.3f}")
```

Run your file. You should see:
```
Warning: Solver lbfgs failed to converge (status=1)...
Scaled model accuracy:   ~0.920
Unscaled model accuracy: ~0.905
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_train_and_evaluate.py`) if anything looks different.
