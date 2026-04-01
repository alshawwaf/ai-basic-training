# Lesson 1.3 — Logistic Regression
#
# Goal: Classify URLs as phishing (1) or legitimate (0).
# Features are extracted from the URL itself — no need to visit the site.
# This is how many browser-based phishing filters work at a basic level.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler

# ── 1. Generate synthetic phishing URL feature dataset ────────────────────────
np.random.seed(42)
n = 1000
half = n // 2

# Legitimate URLs (is_phishing = 0)
legit = pd.DataFrame({
    'url_length':       np.random.normal(45, 12, half).clip(10, 100).astype(int),
    'num_dots':         np.random.poisson(2.1, half),
    'has_at_symbol':    (np.random.rand(half) < 0.05).astype(int),
    'uses_https':       (np.random.rand(half) < 0.82).astype(int),
    'num_subdomains':   np.random.poisson(0.8, half),
    'has_ip_address':   (np.random.rand(half) < 0.02).astype(int),
    'num_hyphens':      np.random.poisson(0.3, half),
    'path_length':      np.random.normal(15, 8, half).clip(0, 60).astype(int),
    'is_phishing': 0
})

# Phishing URLs (is_phishing = 1)
phish = pd.DataFrame({
    'url_length':       np.random.normal(98, 25, half).clip(30, 250).astype(int),
    'num_dots':         np.random.poisson(4.8, half),
    'has_at_symbol':    (np.random.rand(half) < 0.31).astype(int),
    'uses_https':       (np.random.rand(half) < 0.61).astype(int),
    'num_subdomains':   np.random.poisson(2.5, half),
    'has_ip_address':   (np.random.rand(half) < 0.21).astype(int),
    'num_hyphens':      np.random.poisson(2.1, half),
    'path_length':      np.random.normal(48, 18, half).clip(0, 150).astype(int),
    'is_phishing': 1
})

df = pd.concat([legit, phish], ignore_index=True).sample(frac=1, random_state=42)

print("=== Dataset ===")
print(df['is_phishing'].value_counts().rename({0: 'Legitimate', 1: 'Phishing'}))
print("\nFeature preview:")
print(df.drop('is_phishing', axis=1).describe().round(2))

# ── 2. Prepare and split ───────────────────────────────────────────────────────
feature_cols = [c for c in df.columns if c != 'is_phishing']
X = df[feature_cols]
y = df['is_phishing']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features — logistic regression is sensitive to feature scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 3. Train ───────────────────────────────────────────────────────────────────
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
y_pred  = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]   # P(phishing)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))

# ── 5. Feature importance (via coefficients) ──────────────────────────────────
coef_df = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', ascending=False)

print("=== Feature Coefficients (positive = increases P(phishing)) ===")
print(coef_df.to_string(index=False))

# ── 6. Adjustable threshold ───────────────────────────────────────────────────
# In security, you often prefer to catch more phishing (higher recall)
# even at the cost of more false positives. Lower the threshold to do this.
for threshold in [0.5, 0.4, 0.3]:
    y_thresh = (y_proba >= threshold).astype(int)
    report = classification_report(y_test, y_thresh,
                                   target_names=['Legitimate', 'Phishing'],
                                   output_dict=True)
    p = report['Phishing']['precision']
    r = report['Phishing']['recall']
    print(f"Threshold {threshold}: Phishing precision={p:.2f}, recall={r:.2f}")

# ── 7. Confusion matrix plot ──────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=['Legitimate', 'Phishing'])
disp.plot(cmap='Blues')
plt.title('Logistic Regression — Phishing URL Classifier')
plt.tight_layout()
plt.savefig('module1_classic_ml/lesson3_logistic_regression.png')
plt.show()
print("\nPlot saved to module1_classic_ml/lesson3_logistic_regression.png")
