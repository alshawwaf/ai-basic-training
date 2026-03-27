# Stage 1 Milestone — Phishing URL Classifier
#
# End-to-end pipeline:
#   1. Generate a realistic phishing URL feature dataset
#   2. Exploratory data analysis
#   3. Feature engineering
#   4. Train and compare multiple models
#   5. Full evaluation with security-relevant metrics
#   6. Simulate a live detection scenario

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (classification_report, roc_auc_score,
                              RocCurveDisplay, confusion_matrix, ConfusionMatrixDisplay)
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("  STAGE 1 MILESTONE: PHISHING URL CLASSIFIER")
print("=" * 60)

# ── 1. Dataset ─────────────────────────────────────────────────────────────────
np.random.seed(2024)
n = 2000

def make_urls(n, phishing=False):
    if phishing:
        return pd.DataFrame({
            'url_length':           np.random.normal(85, 25, n).clip(20, 250),
            'domain_length':        np.random.normal(30, 10, n).clip(8, 80),
            'num_dots':             np.random.poisson(6, n).clip(2, 15),
            'num_hyphens':          np.random.poisson(4, n).clip(0, 12),
            'has_at_symbol':        np.random.binomial(1, 0.28, n),
            'has_ip_address':       np.random.binomial(1, 0.22, n),
            'uses_https':           np.random.binomial(1, 0.38, n),
            'num_subdomains':       np.random.poisson(5, n).clip(1, 12),
            'path_length':          np.random.normal(55, 20, n).clip(0, 200),
            'num_query_params':     np.random.poisson(4, n).clip(0, 15),
            'has_suspicious_words': np.random.binomial(1, 0.60, n),  # login/verify/update
            'entropy':              np.random.normal(4.2, 0.4, n).clip(2, 5),
            'label': 1
        })
    else:
        return pd.DataFrame({
            'url_length':           np.random.normal(42, 12, n).clip(10, 100),
            'domain_length':        np.random.normal(12, 5, n).clip(4, 30),
            'num_dots':             np.random.poisson(2, n).clip(1, 5),
            'num_hyphens':          np.random.poisson(0.3, n).clip(0, 3),
            'has_at_symbol':        np.random.binomial(1, 0.01, n),
            'has_ip_address':       np.random.binomial(1, 0.005, n),
            'uses_https':           np.random.binomial(1, 0.88, n),
            'num_subdomains':       np.random.poisson(1, n).clip(0, 3),
            'path_length':          np.random.normal(18, 10, n).clip(0, 60),
            'num_query_params':     np.random.poisson(1, n).clip(0, 6),
            'has_suspicious_words': np.random.binomial(1, 0.04, n),
            'entropy':              np.random.normal(3.5, 0.3, n).clip(2, 5),
            'label': 0
        })

df = pd.concat([
    make_urls(n, phishing=False),
    make_urls(n, phishing=True)
], ignore_index=True).sample(frac=1, random_state=42)

feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols]
y = df['label']

# ── 2. EDA ─────────────────────────────────────────────────────────────────────
print("\n── 1. Dataset ──")
print(f"Total samples: {len(df)}")
print(df['label'].value_counts().rename({0: 'Legitimate', 1: 'Phishing'}))

print("\n── 2. Feature means by class ──")
means = df.groupby('label')[feature_cols].mean().round(2)
means.index = ['Legitimate', 'Phishing']
print(means.T)

# ── 3. Feature engineering ────────────────────────────────────────────────────
# Derived features that may capture additional signal
X = X.copy()
X['dots_per_length']    = X['num_dots'] / (X['url_length'] + 1)
X['subdomain_density']  = X['num_subdomains'] / (X['num_dots'] + 1)
X['suspicious_score']   = (X['has_at_symbol'] * 3 +
                           X['has_ip_address'] * 3 +
                           X['has_suspicious_words'] * 2)
feature_cols_eng = list(X.columns)

# ── 4. Train / test split ──────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 5. Train and compare models ───────────────────────────────────────────────
print("\n── 3. Model Comparison ──")
candidates = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree (d=5)': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Decision Tree (d=8)': DecisionTreeClassifier(max_depth=8, random_state=42),
}

results = {}
for name, m in candidates.items():
    m.fit(X_train_s, y_train)
    cv = cross_val_score(m, X_train_s, y_train, cv=5, scoring='roc_auc')
    proba = m.predict_proba(X_test_s)[:, 1]
    auc = roc_auc_score(y_test, proba)
    results[name] = {'model': m, 'auc': auc, 'cv_auc': cv.mean(), 'proba': proba}
    print(f"  {name:<30} CV AUC: {cv.mean():.4f} ± {cv.std():.4f}  |  Test AUC: {auc:.4f}")

# Pick best by test AUC
best_name = max(results, key=lambda k: results[k]['auc'])
best = results[best_name]
print(f"\n  Best model: {best_name}")

# ── 6. Final evaluation ───────────────────────────────────────────────────────
y_pred  = best['model'].predict(X_test_s)
y_proba = best['proba']

print(f"\n── 4. Final Evaluation ({best_name}) ──")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# ── 7. Simulate live detection ────────────────────────────────────────────────
print("\n── 5. Live Detection Simulation ──")
test_urls = pd.DataFrame([
    # Likely phishing
    {'url_length': 120, 'domain_length': 45, 'num_dots': 8, 'num_hyphens': 5,
     'has_at_symbol': 1, 'has_ip_address': 0, 'uses_https': 0, 'num_subdomains': 6,
     'path_length': 80, 'num_query_params': 7, 'has_suspicious_words': 1, 'entropy': 4.3},
    # Likely legitimate
    {'url_length': 35, 'domain_length': 10, 'num_dots': 2, 'num_hyphens': 0,
     'has_at_symbol': 0, 'has_ip_address': 0, 'uses_https': 1, 'num_subdomains': 1,
     'path_length': 12, 'num_query_params': 1, 'has_suspicious_words': 0, 'entropy': 3.4},
    # Ambiguous
    {'url_length': 65, 'domain_length': 20, 'num_dots': 4, 'num_hyphens': 2,
     'has_at_symbol': 0, 'has_ip_address': 0, 'uses_https': 1, 'num_subdomains': 3,
     'path_length': 35, 'num_query_params': 3, 'has_suspicious_words': 1, 'entropy': 3.8},
])
test_urls['dots_per_length']   = test_urls['num_dots'] / (test_urls['url_length'] + 1)
test_urls['subdomain_density'] = test_urls['num_subdomains'] / (test_urls['num_dots'] + 1)
test_urls['suspicious_score']  = (test_urls['has_at_symbol'] * 3 +
                                   test_urls['has_ip_address'] * 3 +
                                   test_urls['has_suspicious_words'] * 2)

test_scaled = scaler.transform(test_urls[feature_cols_eng])
probas = best['model'].predict_proba(test_scaled)[:, 1]

labels = ['Likely phishing', 'Likely legitimate', 'Ambiguous']
for label, p in zip(labels, probas):
    verdict = "BLOCK" if p > 0.5 else "allow"
    print(f"  {label:<22} P(phishing)={p:.3f}  →  {verdict}")

# ── 8. Plot ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm, display_labels=['Legit', 'Phish']).plot(
    ax=axes[0], cmap='Blues', colorbar=False
)
axes[0].set_title(f'Confusion Matrix\n{best_name}')

# ROC curves
for name, res in results.items():
    RocCurveDisplay.from_predictions(y_test, res['proba'], name=name, ax=axes[1])
axes[1].set_title('ROC Curves — All Models')
axes[1].legend(fontsize=8)

# Feature importance (if decision tree)
if 'Decision Tree' in best_name:
    imp = pd.Series(best['model'].feature_importances_, index=feature_cols_eng).sort_values()
    imp.plot(kind='barh', ax=axes[2], color='steelblue')
    axes[2].set_title('Feature Importances')
else:
    coef = pd.Series(best['model'].coef_[0], index=feature_cols_eng).sort_values()
    coef.plot(kind='barh', ax=axes[2], color='steelblue')
    axes[2].set_title('Feature Coefficients')

plt.tight_layout()
plt.savefig('module1_classic_ml/milestone_phishing.png')
plt.show()
print("\nPlot saved to module1_classic_ml/milestone_phishing.png")
print("\n" + "=" * 60)
print("  MILESTONE COMPLETE")
print("=" * 60)
