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

# Legitimate URLs (label = 0)
legit = pd.DataFrame({
    'url_length':       np.random.normal(40, 10, n // 2).clip(10, 100),
    'num_dots':         np.random.poisson(2, n // 2).clip(1, 5),
    'has_at_symbol':    np.random.binomial(1, 0.01, n // 2),
    'uses_https':       np.random.binomial(1, 0.90, n // 2),
    'num_subdomains':   np.random.poisson(1, n // 2).clip(0, 3),
    'has_ip_address':   np.random.binomial(1, 0.01, n // 2),
    'num_hyphens':      np.random.poisson(0.5, n // 2).clip(0, 3),
    'path_length':      np.random.normal(20, 10, n // 2).clip(0, 60),
    'label': 0
})

# Phishing URLs (label = 1)
phish = pd.DataFrame({
    'url_length':       np.random.normal(75, 20, n // 2).clip(20, 200),
    'num_dots':         np.random.poisson(5, n // 2).clip(2, 12),
    'has_at_symbol':    np.random.binomial(1, 0.30, n // 2),
    'uses_https':       np.random.binomial(1, 0.40, n // 2),
    'num_subdomains':   np.random.poisson(4, n // 2).clip(1, 10),
    'has_ip_address':   np.random.binomial(1, 0.25, n // 2),
    'num_hyphens':      np.random.poisson(3, n // 2).clip(0, 10),
    'path_length':      np.random.normal(50, 20, n // 2).clip(0, 150),
    'label': 1
})

df = pd.concat([legit, phish], ignore_index=True).sample(frac=1, random_state=42)

print("=== Dataset ===")
print(df['label'].value_counts().rename({0: 'Legitimate', 1: 'Phishing'}))
print("\nFeature preview:")
print(df.drop('label', axis=1).describe().round(2))

# ── 2. Prepare and split ───────────────────────────────────────────────────────
feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols]
y = df['label']

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
plt.savefig('stage1_ml/lesson3_logistic_regression.png')
plt.show()
print("\nPlot saved to stage1_ml/lesson3_logistic_regression.png")
