# Lab -- Exercise 4: Threshold Tuning

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_threshold_tuning.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: array math
import pandas as pd                         # pandas: tabular data
import matplotlib.pyplot as plt             # matplotlib: plotting
from sklearn.linear_model import LogisticRegression       # the classifier
from sklearn.preprocessing import StandardScaler          # zero-mean, unit-variance scaling
from sklearn.model_selection import train_test_split      # holdout-set helper
# precision/recall/F1 = the three core classifier metrics; PR curve sweeps thresholds
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve
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
X = df[FEATURES]                              # 2D feature matrix
y = df['is_phishing']                          # 1D label vector
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y     # stratified 80/20 split
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)            # fit + transform on training set
X_test_scaled  = scaler.transform(X_test)                 # transform only on test set
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)            # exact same model as the previous lab
```

---

## Step 4: Get Probability Scores

Call model.predict_proba(X_test_scaled)[:, 1] to get P(phishing) for each URL. Build a DataFrame with columns: P(phishing), predicted_label (at 0.5), actual. Print the first 10 rows. Highlight any rows where prediction != actual.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Probability scores vs hard labels")
print("=" * 60)
# predict_proba returns 2 columns [P(legit), P(phishing)] — [:, 1] grabs the phishing probability
probs = model.predict_proba(X_test_scaled)[:, 1]
results = pd.DataFrame({
    'P(phishing)':      probs,
    'predicted_label':  (probs >= 0.5).astype(int),       # default 0.5 threshold → 0/1 label
    'actual':           y_test.values
})
print(results.head(10).to_string(index=False))
# Close calls = the model wasn't confident — these are where threshold tuning matters most
close_calls = results[(results['P(phishing)'] > 0.4) & (results['P(phishing)'] < 0.6)]
print(f"\nClose calls (P between 0.4 and 0.6): {len(close_calls)}")
```

Run your file. You should see:
```
P(phishing)  predicted_label  actual
0.04              0           0
0.87              1           1
...
Close calls (P between 0.4 and 0.6): ~8
```

---

## Step 5: Threshold Comparison Table

For thresholds [0.2, 0.3, 0.5, 0.7, 0.8], compute: - precision (for phishing class) - recall    (for phishing class)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Threshold comparison table")
print("=" * 60)
# Sweep five thresholds — low = aggressive (catches more, more false alarms); high = strict (the opposite)
thresholds = [0.2, 0.3, 0.5, 0.7, 0.8]
print(f"{'Threshold':>10} | {'Precision':>9} | {'Recall':>7} | {'F1':>6} | {'Flagged':>8}")
print("-" * 55)
for thresh in thresholds:
    y_pred = (probs >= thresh).astype(int)             # convert probabilities to 0/1 at this cutoff
    p = precision_score(y_test, y_pred, zero_division=0)   # of flagged URLs, how many were actually phishing?
    r = recall_score(y_test, y_pred)                       # of all phishing URLs, how many did we catch?
    f = f1_score(y_test, y_pred)                           # harmonic mean of precision + recall
    flagged = y_pred.sum()                                  # total URLs predicted as phishing
    print(f"{thresh:>10.2f} | {p:>9.3f} | {r:>7.3f} | {f:>6.3f} | {flagged:>8}")
```

Run your file. You should see:
```
Threshold | Precision |  Recall |    F1 |  Flagged
-------------------------------------------------------
0.20 |     0.785 |   0.980 | 0.872 |      124
0.30 |     0.838 |   0.960 | 0.895 |      114
0.50 |     0.930 |   0.910 | 0.920 |       98
0.70 |     0.970 |   0.820 | 0.889 |       85
0.80 |     0.988 |   0.790 | 0.878 |       80
```

---

## Step 6: Choose Threshold for 95% Recall

Find the LOWEST threshold (sweeping from 0.0 to 0.9 in steps of 0.01) that still achieves recall >= 0.95. Print the threshold, the actual recall achieved, and the precision at that point.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Find threshold for recall >= 0.95")
print("=" * 60)
# Walk DOWN from 0.9 to 0.0 — first hit at recall>=0.95 is the LOWEST threshold meeting the goal
for thresh in np.arange(0.9, 0.0, -0.01):
    y_pred = (probs >= thresh).astype(int)
    r = recall_score(y_test, y_pred)
    if r >= 0.95:
        p = precision_score(y_test, y_pred, zero_division=0)
        flagged = y_pred.sum()
        print(f"Lowest threshold for recall>=0.95: {thresh:.2f}")
        print(f"  Actual recall:    {r:.3f}")
        print(f"  Precision:        {p:.3f}")
        print(f"  URLs flagged:     {flagged} / {len(y_test)}")
        break                                           # stop at first match — this is the lowest
```

Run your file. You should see:
```
Lowest threshold for recall>=0.95: ~0.22
Actual recall:    0.950
Precision:        ~0.79
URLs flagged:     ~120 / 200
```

---

## Step 7: TASK 4 (BONUS) — Plot the Precision-Recall Curve

Use precision_recall_curve(y_test, probs) to get precision, recall, and thresholds. Plot the curve (recall on x-axis, precision on y-axis). Mark the default 0.5 threshold point with a red dot.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Precision-recall curve")
print("=" * 60)
print("\n--- Exercise 4 complete. Lesson 1.3 workshop done! ---")
print("--- Next: stage1_classic_ml/04_decision_trees/ ---")
# precision_recall_curve returns the (precision, recall) tradeoff for every possible threshold
precision_vals, recall_vals, thresholds_pr = precision_recall_curve(y_test, probs)
plt.figure(figsize=(8, 6))
plt.plot(recall_vals, precision_vals, label='PR Curve')
# Find which point on the curve corresponds to threshold = 0.5 (the default)
idx_05 = np.argmin(np.abs(thresholds_pr - 0.5))
plt.scatter(recall_vals[idx_05], precision_vals[idx_05],
            color='red', zorder=5, label='Threshold=0.5')      # zorder=5 keeps it on top
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve — Phishing Classifier')
plt.legend()
plt.grid(True)
plt.show()
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_threshold_tuning.py`) if anything looks different.
