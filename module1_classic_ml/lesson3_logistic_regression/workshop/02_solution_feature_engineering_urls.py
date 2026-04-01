import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

print("=" * 60)
print("TASK 1 — Dataset inspection")
print("=" * 60)
print(f"Shape: {df.shape}")
print("\nClass balance:")
print(df['is_phishing'].value_counts())
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values: {df.isnull().sum().sum()}")

print("\n" + "=" * 60)
print("TASK 2 — Feature means by class")
print("=" * 60)
means = df.groupby('is_phishing')[FEATURES].mean()
print(means.T.to_string())
diff = (means.loc[1] - means.loc[0]).abs().sort_values(ascending=False)
print(f"\nTop 3 most discriminative features:")
print(diff.head(3))

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

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Feature-label correlations")
print("=" * 60)
correlations = df[FEATURES + ['is_phishing']].corr()['is_phishing'].drop('is_phishing')
print(correlations.sort_values(ascending=False))
