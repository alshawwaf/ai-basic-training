# =============================================================================
# LESSON 1.3 | WORKSHOP | Exercise 2 of 4
# Feature Engineering for URL Phishing Detection
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why specific URL features predict phishing
# - How to generate and inspect a realistic synthetic dataset
# - How to analyse feature distributions by class
# - How to check for class imbalance before modelling
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson3_logistic_regression/workshop/exercise2_feature_engineering_urls.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# BACKGROUND
# =============================================================================
# Features used for phishing URL detection:
#   url_length       — phishing URLs are often longer (obscure the real domain)
#   num_dots         — deep subdomains inflate dot count  (a.b.c.evil.com)
#   has_at_symbol    — browser ignores everything before @ in a URL
#   uses_https       — HTTPS presence is not a safety guarantee
#   num_subdomains   — many subdomains suggest domain spoofing
#   has_ip_address   — IP-based URLs instead of domains are suspicious
#   num_hyphens      — hyphens used to mimic brands (secure-paypal-login.com)
#   path_length      — long paths often encode redirects or malicious params

# --- Dataset generation (do not modify) -------------------------------------
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
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Inspect the Dataset
# =============================================================================
# Print: shape, class balance (value_counts with %), first 5 rows, missing values.

print("=" * 60)
print("TASK 1 — Dataset inspection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print(f"Shape: {df.shape}")
#   print("\nClass balance:")
#   print(df['is_phishing'].value_counts())
#   print(f"\nFirst 5 rows:\n{df.head()}")
#   print(f"\nMissing values: {df.isnull().sum().sum()}")

# EXPECTED OUTPUT:
# Shape: (1000, 9)
# Class balance:
#   0    500
#   1    500
# Missing values: 0

# =============================================================================
# TASK 2 — Compare Feature Means by Class
# =============================================================================
# Group by 'is_phishing' and compute the mean of each feature.
# Print the result transposed (features as rows, classes as columns).
# Identify the top 3 features with the largest absolute difference between classes.

print("\n" + "=" * 60)
print("TASK 2 — Feature means by class")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   means = df.groupby('is_phishing')[FEATURES].mean()
#   print(means.T.to_string())
#   diff = (means.loc[1] - means.loc[0]).abs().sort_values(ascending=False)
#   print(f"\nTop 3 most discriminative features:")
#   print(diff.head(3))

# EXPECTED OUTPUT:
#                 is_phishing=0   is_phishing=1
# url_length           ~45           ~98
# num_dots             ~2.1          ~4.8
# path_length          ~15           ~48
# ...

# =============================================================================
# TASK 3 — Plot Feature Distributions
# =============================================================================
# Create a 2x2 grid of histograms for:
#   url_length, num_dots, num_subdomains, path_length
# For each, plot overlapping histograms for phishing (red) and legitimate (blue)
# with alpha=0.5 and a legend.

print("\n" + "=" * 60)
print("TASK 3 — Feature distribution plots")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, axes = plt.subplots(2, 2, figsize=(10, 8))
#   plot_features = ['url_length', 'num_dots', 'num_subdomains', 'path_length']
#   for ax, feat in zip(axes.flat, plot_features):
#       df[df['is_phishing']==0][feat].hist(ax=ax, bins=20, alpha=0.5,
#                                           color='steelblue', label='Legitimate')
#       df[df['is_phishing']==1][feat].hist(ax=ax, bins=20, alpha=0.5,
#                                           color='red', label='Phishing')
#       ax.set_title(feat)
#       ax.legend()
#   plt.tight_layout()
#   plt.show()

print("Distribution plots created.")

# =============================================================================
# TASK 4 (BONUS) — Correlation with Phishing Label
# =============================================================================
# Compute the Pearson correlation of each feature with 'is_phishing'.
# Print the correlations sorted descending.
# Identify which 2 features are most positively and which (if any) are
# negatively correlated with phishing.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Feature-label correlations")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   correlations = df[FEATURES + ['is_phishing']].corr()['is_phishing'].drop('is_phishing')
#   print(correlations.sort_values(ascending=False))

# EXPECTED OUTPUT:
# url_length       ~0.61
# num_dots         ~0.47
# has_at_symbol    ~0.39
# num_subdomains   ~0.35
# path_length      ~0.33
# num_hyphens      ~0.27
# has_ip_address   ~0.22
# uses_https       ~-0.20  ← negative: HTTPS is less common among phishing sites

print("\n--- Exercise 2 complete. Move to exercise3_train_and_evaluate.py ---")
