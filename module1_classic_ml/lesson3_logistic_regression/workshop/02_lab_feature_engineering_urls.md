# Lab -- Exercise 2: Feature Engineering for URL Phishing Detection

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_feature_engineering_urls.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n = 1000
half = n // 2
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
```

---

## Step 4: Inspect the Dataset

Print: shape, class balance (value_counts with %), first 5 rows, missing values.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Dataset inspection")
print("=" * 60)
print(f"Shape: {df.shape}")
print("\nClass balance:")
print(df['is_phishing'].value_counts())
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values: {df.isnull().sum().sum()}")
```

Run your file. You should see:
```
Shape: (1000, 9)
Class balance:
0    500
1    500
Missing values: 0
```

---

## Step 5: Compare Feature Means by Class

Group by 'is_phishing' and compute the mean of each feature. Print the result transposed (features as rows, classes as columns). Identify the top 3 features with the largest absolute difference between classes.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Feature means by class")
print("=" * 60)
means = df.groupby('is_phishing')[FEATURES].mean()
print(means.T.to_string())
diff = (means.loc[1] - means.loc[0]).abs().sort_values(ascending=False)
print(f"\nTop 3 most discriminative features:")
print(diff.head(3))
```

Run your file. You should see:
```
is_phishing=0   is_phishing=1
url_length           ~45           ~98
num_dots             ~2.1          ~4.8
path_length          ~15           ~48
...
```

---

## Step 6: Plot Feature Distributions

Create a 2x2 grid of histograms for: url_length, num_dots, num_subdomains, path_length For each, plot overlapping histograms for phishing (red) and legitimate (blue)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Feature distribution plots")
print("=" * 60)
print("Distribution plots created.")
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
plot_features = ['url_length', 'num_dots', 'num_subdomains', 'path_length']
for ax, feat in zip(axes.flat, plot_features):
    df[df['is_phishing']==0][feat].hist(ax=ax, bins=20, alpha=0.5,
                                        color='steelblue', label='Legitimate')
    df[df['is_phishing']==1][feat].hist(ax=ax, bins=20, alpha=0.5,
                                        color='red', label='Phishing')
    ax.set_title(feat)
    ax.legend()
plt.tight_layout()
plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Correlation with Phishing Label

Compute the Pearson correlation of each feature with 'is_phishing'. Print the correlations sorted descending. Identify which features are most positively correlated and which (if any) are negatively correlated.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Feature-label correlations")
print("=" * 60)
correlations = df[FEATURES + ['is_phishing']].corr()['is_phishing'].drop('is_phishing')
print(correlations.sort_values(ascending=False))
```

Run your file. You should see:
```
url_length       ~0.61
num_dots         ~0.47
has_at_symbol    ~0.39
num_subdomains   ~0.35
path_length      ~0.33
num_hyphens      ~0.27
has_ip_address   ~0.22
uses_https       ~-0.20  ← negative: HTTPS is less common among phishing sites
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
