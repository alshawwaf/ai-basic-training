# Lesson 1.5 — Model Evaluation
#
# Accuracy alone is dangerous in security. This lesson demonstrates:
#   - Confusion matrix
#   - Precision, Recall, F1
#   - ROC curve and AUC
#   - Decision threshold tuning
#
# We use three classifiers side-by-side so you can compare their tradeoffs.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
    precision_score, recall_score, f1_score,
    roc_auc_score, RocCurveDisplay, precision_recall_curve
)
from sklearn.preprocessing import StandardScaler

# ── 1. Create an imbalanced dataset (mimics real security data) ────────────────
# 5% attack, 95% benign — realistic for most enterprise environments
np.random.seed(42)
n_benign, n_attack = 9_500, 500
benign_data = np.column_stack([
    np.random.normal(10, 3, n_benign),
    np.random.normal(5000, 1500, n_benign),
    np.random.poisson(3, n_benign)
])
attack_data = np.column_stack([
    np.random.normal(80, 30, n_attack),
    np.random.normal(500, 300, n_attack),
    np.random.poisson(30, n_attack)
])
X = np.vstack([benign_data, attack_data])
y = np.array([0]*n_benign + [1]*n_attack)
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]

print("=== Class Distribution ===")
unique, counts = np.unique(y, return_counts=True)
for label, count in zip(unique, counts):
    name = 'Benign' if label == 0 else 'Attack'
    print(f"  {name}: {count} ({count/len(y)*100:.1f}%)")

# ── 2. Split and scale ─────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 3. Train three models ──────────────────────────────────────────────────────
models = {
    'Always Benign (baseline)': DummyClassifier(strategy='most_frequent'),
    'Logistic Regression':      LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree (depth=5)':  DecisionTreeClassifier(max_depth=5, random_state=42),
}

# DummyClassifier and DecisionTree use unscaled data;
# LogisticRegression uses scaled data.
models['Always Benign (baseline)'].fit(X_train, y_train)
models['Logistic Regression'].fit(X_train_s, y_train)
models['Decision Tree (depth=5)'].fit(X_train, y_train)

# ── 4. Compare accuracy — show why it's misleading ────────────────────────────
print("\n=== Accuracy Comparison (why accuracy is misleading) ===")
for name, m in models.items():
    X_eval = X_test_s if 'Logistic' in name else X_test
    acc = m.score(X_eval, y_test)
    print(f"  {name:<35} accuracy: {acc:.3f}")
print("→ The 'Always Benign' model has high accuracy but catches ZERO attacks!")

# ── 5. Proper evaluation of the best model ────────────────────────────────────
best = models['Logistic Regression']
y_pred  = best.predict(X_test_s)
y_proba = best.predict_proba(X_test_s)[:, 1]

print("\n=== Classification Report — Logistic Regression ===")
print(classification_report(y_test, y_pred, target_names=['Benign', 'Attack']))
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# ── 6. Threshold sensitivity ───────────────────────────────────────────────────
print("\n=== Threshold Sensitivity (Attack class) ===")
print(f"{'Threshold':<12} {'Precision':<12} {'Recall':<12} {'F1':<8}")
for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    y_t = (y_proba >= threshold).astype(int)
    p = precision_score(y_test, y_t, zero_division=0)
    r = recall_score(y_test, y_t, zero_division=0)
    f = f1_score(y_test, y_t, zero_division=0)
    print(f"{threshold:<12.1f} {p:<12.3f} {r:<12.3f} {f:<8.3f}")

# ── 7. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm, display_labels=['Benign', 'Attack']).plot(
    ax=axes[0], cmap='Blues', colorbar=False
)
axes[0].set_title('Confusion Matrix')

# ROC curves
for name in ['Logistic Regression', 'Decision Tree (depth=5)']:
    m = models[name]
    X_eval = X_test_s if 'Logistic' in name else X_test
    proba = m.predict_proba(X_eval)[:, 1]
    RocCurveDisplay.from_predictions(y_test, proba, name=name, ax=axes[1])
axes[1].plot([0, 1], [0, 1], 'k--', label='Random')
axes[1].set_title('ROC Curves')
axes[1].legend(fontsize=8)

# Precision-Recall curve (better for imbalanced data)
precision, recall, _ = precision_recall_curve(y_test, y_proba)
axes[2].plot(recall, precision, color='steelblue', lw=2)
axes[2].set_xlabel('Recall (attacks caught)')
axes[2].set_ylabel('Precision (alert accuracy)')
axes[2].set_title('Precision-Recall Curve')
axes[2].axhline(y=0.05, color='grey', linestyle='--', label='Random baseline (5%)')
axes[2].legend()

plt.tight_layout()
plt.savefig('module1_classic_ml/lesson5_evaluation.png')
plt.show()
print("\nPlot saved to module1_classic_ml/lesson5_evaluation.png")
