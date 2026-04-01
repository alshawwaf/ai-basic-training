import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (roc_curve, roc_auc_score,
                             precision_score, recall_score, f1_score,
                             accuracy_score)

# Same imbalanced dataset (95% benign, 5% attack)
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
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)

# Train 3 models: dummy baseline, logistic regression, and decision tree
dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
lr    = LogisticRegression(max_iter=1000, random_state=42).fit(X_tr_sc, y_train)
dt    = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train)

print("=" * 60)
print("TASK 1 — ROC curve for LogisticRegression")
print("=" * 60)
# predict_proba[:, 1] gives the model's confidence that each sample is an attack
lr_scores = lr.predict_proba(X_te_sc)[:, 1]

# roc_curve sweeps across all thresholds and returns FPR/TPR at each one
# AUC summarises this into a single number: 1.0 = perfect, 0.5 = random
fpr, tpr, thresholds = roc_curve(y_test, lr_scores)
auc_lr = roc_auc_score(y_test, lr_scores)
print(f"LogisticRegression AUC: {auc_lr:.3f}")

plt.figure(figsize=(7, 6))
plt.plot(fpr, tpr, label=f'LR (AUC={auc_lr:.3f})')
plt.plot([0,1], [0,1], 'k--', label='Random (AUC=0.50)')
# Mark the default threshold=0.5 operating point on the curve
idx_05 = np.argmin(np.abs(thresholds - 0.5))
plt.scatter(fpr[idx_05], tpr[idx_05], color='red', zorder=5, label='threshold=0.5')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate (Recall)')
plt.title('ROC Curve — Intrusion Detector')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n" + "=" * 60)
print("TASK 2 — ROC curves for three models")
print("=" * 60)
# Dummy always predicts benign, so its "probability" is always 0 (no attack)
dummy_scores = np.zeros(len(y_test))
dt_scores = dt.predict_proba(X_test)[:, 1]

# Plot all 3 models on the same ROC chart to compare discrimination ability
models_info = [
    ("DummyClassifier",    dummy_scores),
    ("LogisticRegression", lr_scores),
    ("DecisionTree",       dt_scores),
]
plt.figure(figsize=(8, 6))
for name, scores in models_info:
    fpr_m, tpr_m, _ = roc_curve(y_test, scores)
    auc_m = roc_auc_score(y_test, scores)
    plt.plot(fpr_m, tpr_m, label=f'{name} (AUC={auc_m:.3f})')
    print(f"{name:25s} AUC: {auc_m:.3f}")
plt.plot([0,1],[0,1],'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n" + "=" * 60)
print("TASK 3 — Optimal threshold from ROC curve")
print("=" * 60)
lr_scores = lr.predict_proba(X_te_sc)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, lr_scores)

# The "best" threshold is the point on the ROC curve closest to the top-left corner
# Top-left = perfect classifier (TPR=1, FPR=0), so minimise distance to it
distances = np.sqrt((1 - tpr)**2 + fpr**2)
best_idx  = np.argmin(distances)
opt_thresh = thresholds[best_idx]
opt_tpr    = tpr[best_idx]
opt_fpr    = fpr[best_idx]
print(f"Optimal threshold (min distance to top-left): {opt_thresh:.3f}")
print(f"At this threshold: TPR={opt_tpr:.3f}, FPR={opt_fpr:.3f}")

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Full evaluation scorecard")
print("=" * 60)
# Build a full scorecard: hard predictions for metrics, probabilities for AUC
dummy_preds = dummy.predict(X_test)
lr_preds    = lr.predict(X_te_sc)
dt_preds    = dt.predict(X_test)
dummy_scores_auc = np.zeros(len(y_test))
lr_scores_auc    = lr.predict_proba(X_te_sc)[:, 1]
dt_scores_auc    = dt.predict_proba(X_test)[:, 1]
all_models = [
    ("DummyClassifier",    dummy_preds, dummy_scores_auc),
    ("LogisticRegression", lr_preds,    lr_scores_auc),
    ("DecisionTree",       dt_preds,    dt_scores_auc),
]
print(f"{'Model':25s} {'Accuracy':>8} {'Precision':>9} {'Recall':>7} {'F1':>7} {'AUC':>7}")
print("-" * 70)
for name, y_pred, scores in all_models:
    acc = accuracy_score(y_test, y_pred)
    p   = precision_score(y_test, y_pred, zero_division=0)
    r   = recall_score(y_test, y_pred)
    f   = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, scores)
    print(f"{name:25s} {acc:>8.3f} {p:>9.3f} {r:>7.3f} {f:>7.3f} {auc:>7.3f}")
