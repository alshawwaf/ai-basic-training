import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

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
X = df[FEATURES]
y = df['is_phishing']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("=" * 60)
print("TASK 1 — Feature scaling")
print("=" * 60)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)          # NOTE: transform only, no fit!
#
# Compare raw vs scaled url_length
raw_col   = X_train['url_length']
scaled_col = X_train_scaled[:, 0]   # url_length is first column
print(f"Raw url_length:    mean={raw_col.mean():.1f}, std={raw_col.std():.1f}")
print(f"Scaled url_length: mean={scaled_col.mean():.2f}, std={scaled_col.std():.2f}")

print("\n" + "=" * 60)
print("TASK 2 — Model coefficients")
print("=" * 60)
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)
coef_df = pd.DataFrame({
    'feature': FEATURES,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', key=abs, ascending=False)
print(coef_df.to_string(index=False))

print("\n" + "=" * 60)
print("TASK 3 — Evaluation: classification report + confusion matrix")
print("=" * 60)
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred,
                             target_names=['legitimate', 'phishing']))
#
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion matrix:")
print("                Predicted Legit  Predicted Phishing")
print(f"Actual Legit       {cm[0,0]:3d} (TN)         {cm[0,1]:3d} (FP)")
print(f"Actual Phish       {cm[1,0]:3d} (FN)         {cm[1,1]:3d} (TP)")
#
# Optional: seaborn heatmap
# sns.heatmap(cm, annot=True, fmt='d', xticklabels=['Legit','Phish'],
#             yticklabels=['Legit','Phish'])
# plt.show()

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Scaled vs unscaled comparison")
print("=" * 60)
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    model_unscaled = LogisticRegression(max_iter=100, random_state=42)
    model_unscaled.fit(X_train, y_train)
    if w:
        print(f"Warning: {w[-1].message}")
acc_scaled   = model.score(X_test_scaled, y_test)
acc_unscaled = model_unscaled.score(X_test, y_test)
print(f"Scaled model accuracy:   {acc_scaled:.3f}")
print(f"Unscaled model accuracy: {acc_unscaled:.3f}")
