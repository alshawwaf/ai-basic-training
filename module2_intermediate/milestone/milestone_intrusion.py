# Stage 2 Milestone — Network Intrusion Detector
#
# KDD Cup-style network intrusion detection pipeline.
# Demonstrates the full Stage 2 skillset:
#   - Feature engineering on connection-level data
#   - Random Forest classifier
#   - Cross-validation
#   - Multi-class classification (normal vs attack types)
#   - Threshold tuning for operational use

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix,
                              ConfusionMatrixDisplay, roc_auc_score)

print("=" * 60)
print("  STAGE 2 MILESTONE: NETWORK INTRUSION DETECTOR")
print("=" * 60)

np.random.seed(2024)

# ── 1. Generate KDD Cup-inspired dataset ──────────────────────────────────────
# Attack types: DoS, Probe (scan), R2L (remote-to-local), Normal

def make_connections(n, attack_type='normal'):
    base = {
        'normal': dict(
            duration=np.random.exponential(15, n).clip(0, 500),
            src_bytes=np.random.lognormal(8, 1.5, n).clip(0, 1e6),
            dst_bytes=np.random.lognormal(9, 1.5, n).clip(0, 5e6),
            wrong_fragment=np.random.poisson(0.01, n).clip(0, 3),
            urgent=np.zeros(n),
            hot=np.random.poisson(1, n).clip(0, 20),
            num_failed_logins=np.zeros(n).astype(int),
            logged_in=np.random.binomial(1, 0.8, n),
            num_compromised=np.zeros(n),
            srv_count=np.random.poisson(20, n).clip(1, 100),
            serror_rate=np.random.beta(0.5, 10, n),
            same_srv_rate=np.random.beta(8, 2, n),
        ),
        'dos': dict(
            duration=np.random.exponential(0.5, n).clip(0, 5),
            src_bytes=np.random.lognormal(5, 0.5, n).clip(0, 5000),
            dst_bytes=np.zeros(n),
            wrong_fragment=np.random.poisson(0.5, n).clip(0, 5),
            urgent=np.zeros(n),
            hot=np.zeros(n),
            num_failed_logins=np.zeros(n).astype(int),
            logged_in=np.zeros(n),
            num_compromised=np.zeros(n),
            srv_count=np.random.poisson(500, n).clip(100, 1000),
            serror_rate=np.random.beta(8, 2, n),
            same_srv_rate=np.random.beta(10, 1, n),
        ),
        'probe': dict(
            duration=np.random.exponential(0.2, n).clip(0, 2),
            src_bytes=np.random.lognormal(4, 0.5, n).clip(0, 1000),
            dst_bytes=np.zeros(n),
            wrong_fragment=np.zeros(n),
            urgent=np.zeros(n),
            hot=np.zeros(n),
            num_failed_logins=np.zeros(n).astype(int),
            logged_in=np.zeros(n),
            num_compromised=np.zeros(n),
            srv_count=np.random.poisson(3, n).clip(1, 20),
            serror_rate=np.random.beta(2, 5, n),
            same_srv_rate=np.random.beta(1, 5, n),
        ),
        'r2l': dict(
            duration=np.random.normal(300, 100, n).clip(10, 1200),
            src_bytes=np.random.lognormal(7, 1, n).clip(100, 50000),
            dst_bytes=np.random.lognormal(7, 1, n).clip(100, 50000),
            wrong_fragment=np.zeros(n),
            urgent=np.zeros(n),
            hot=np.random.poisson(5, n).clip(0, 30),
            num_failed_logins=np.random.poisson(3, n).clip(0, 20).astype(int),
            logged_in=np.random.binomial(1, 0.3, n),
            num_compromised=np.random.poisson(2, n).clip(0, 10),
            srv_count=np.random.poisson(5, n).clip(1, 30),
            serror_rate=np.random.beta(1, 5, n),
            same_srv_rate=np.random.beta(3, 3, n),
        ),
    }
    df = pd.DataFrame(base[attack_type])
    df['attack_type'] = attack_type
    return df

sizes = {'normal': 4000, 'dos': 1500, 'probe': 800, 'r2l': 400}
df = pd.concat([make_connections(n, t) for t, n in sizes.items()], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\n── 1. Dataset ──")
print(df['attack_type'].value_counts())

# ── 2. Feature engineering ────────────────────────────────────────────────────
df['bytes_ratio']        = df['src_bytes'] / (df['dst_bytes'] + 1)
df['bytes_per_second']   = (df['src_bytes'] + df['dst_bytes']) / (df['duration'] + 0.001)
df['is_short_conn']      = (df['duration'] < 1).astype(int)
df['high_srv_count']     = (df['srv_count'] > 100).astype(int)
df['is_binary']          = (df['attack_type'] != 'normal').astype(int)

feature_cols = [
    'duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised',
    'srv_count', 'serror_rate', 'same_srv_rate',
    'bytes_ratio', 'bytes_per_second', 'is_short_conn', 'high_srv_count'
]

# Multi-class labels
le = LabelEncoder()
y_multi = le.fit_transform(df['attack_type'])
y_binary = df['is_binary'].values
X = df[feature_cols].values

# ── 3. Train / test split ──────────────────────────────────────────────────────
X_train, X_test, y_train_m, y_test_m, y_train_b, y_test_b = train_test_split(
    X, y_multi, y_binary, test_size=0.2, random_state=42, stratify=y_binary
)

# ── 4. Train models ────────────────────────────────────────────────────────────
print("\n── 2. Training ──")
rf_binary = RandomForestClassifier(n_estimators=200, oob_score=True, n_jobs=-1, random_state=42)
rf_multi  = RandomForestClassifier(n_estimators=200, oob_score=True, n_jobs=-1, random_state=42)

rf_binary.fit(X_train, y_train_b)
rf_multi.fit(X_train, y_train_m)

print(f"Binary classifier OOB score : {rf_binary.oob_score_:.4f}")
print(f"Multi-class classifier OOB  : {rf_multi.oob_score_:.4f}")

# ── 5. Cross-validation ───────────────────────────────────────────────────────
cv = cross_val_score(rf_binary, X, y_binary, cv=5, scoring='roc_auc', n_jobs=-1)
print(f"\n5-fold CV AUC (binary): {cv.mean():.4f} ± {cv.std():.4f}")

# ── 6. Evaluation ─────────────────────────────────────────────────────────────
print("\n── 3. Binary (Normal vs Attack) ──")
y_pred_b = rf_binary.predict(X_test)
print(classification_report(y_test_b, y_pred_b, target_names=['Normal', 'Attack']))
auc = roc_auc_score(y_test_b, rf_binary.predict_proba(X_test)[:, 1])
print(f"ROC AUC: {auc:.4f}")

print("\n── 4. Multi-class (Attack Type) ──")
y_pred_m = rf_multi.predict(X_test)
print(classification_report(y_test_m, y_pred_m, target_names=le.classes_))

# ── 7. Feature importances ─────────────────────────────────────────────────────
imp = pd.Series(rf_binary.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\n── 5. Top Features ──")
print(imp.head(8).round(4).to_string())

# ── 8. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Binary confusion matrix
cm_b = confusion_matrix(y_test_b, y_pred_b)
ConfusionMatrixDisplay(cm_b, display_labels=['Normal', 'Attack']).plot(ax=axes[0], cmap='Blues', colorbar=False)
axes[0].set_title(f'Binary Classifier\nAUC={auc:.3f}')

# Multi-class confusion matrix
cm_m = confusion_matrix(y_test_m, y_pred_m)
sns.heatmap(cm_m, annot=True, fmt='d', xticklabels=le.classes_, yticklabels=le.classes_,
            cmap='Blues', ax=axes[1])
axes[1].set_title('Multi-class Confusion Matrix')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

# Feature importance
imp.head(10).sort_values().plot(kind='barh', ax=axes[2], color='steelblue')
axes[2].set_title('Top 10 Feature Importances')

plt.tight_layout()
plt.savefig('module2_intermediate/milestone_intrusion.png')
plt.show()
print("\nPlot saved to module2_intermediate/milestone_intrusion.png")
print("\n" + "=" * 60)
print("  MILESTONE COMPLETE")
print("=" * 60)
