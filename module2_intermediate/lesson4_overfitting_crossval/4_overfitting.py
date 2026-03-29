# Lesson 2.4 — Cross-Validation & Overfitting
#
# Demonstrates:
#   - How a decision tree overfits as depth increases
#   - How cross-validation gives a more reliable performance estimate
#   - Validation curves to find the right model complexity
#   - The bias-variance tradeoff visually

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split, cross_val_score,
    validation_curve, learning_curve
)
from sklearn.metrics import roc_auc_score

np.random.seed(42)

# ── 1. Generate dataset ────────────────────────────────────────────────────────
# Simulates a modestly complex intrusion detection problem
X, y = make_classification(
    n_samples=2000, n_features=15, n_informative=8,
    n_redundant=3, flip_y=0.05,   # 5% label noise (realistic)
    weights=[0.9, 0.1],           # 10% attacks
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("=== Dataset ===")
print(f"Training: {len(X_train)} | Test: {len(X_test)}")
print(f"Attack rate: {y.mean()*100:.1f}%")

# ── 2. Overfitting demo: tree depth vs train/test accuracy ────────────────────
print("\n=== Overfitting Demo: Decision Tree Depth ===")
print(f"{'Depth':<8} {'Train AUC':<12} {'Test AUC':<12} {'Gap':<8}")

depths = list(range(1, 25))
train_aucs, test_aucs = [], []

for depth in depths:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42)
    tree.fit(X_train, y_train)

    tr_auc = roc_auc_score(y_train, tree.predict_proba(X_train)[:, 1])
    te_auc = roc_auc_score(y_test,  tree.predict_proba(X_test)[:, 1])
    train_aucs.append(tr_auc)
    test_aucs.append(te_auc)

    if depth in [1, 3, 5, 8, 12, 20]:
        gap = tr_auc - te_auc
        flag = " ← OVERFITTING" if gap > 0.1 else ""
        print(f"{depth:<8} {tr_auc:<12.4f} {te_auc:<12.4f} {gap:.4f}{flag}")

best_depth = depths[np.argmax(test_aucs)]
print(f"\nBest depth for test AUC: {best_depth} (AUC = {max(test_aucs):.4f})")

# ── 3. Cross-validation: more reliable than a single split ────────────────────
print("\n=== Cross-Validation (5-fold) ===")

models = {
    'Tree depth=3 (underfit)':    DecisionTreeClassifier(max_depth=3, random_state=42),
    f'Tree depth={best_depth} (good)': DecisionTreeClassifier(max_depth=best_depth, random_state=42),
    'Tree depth=20 (overfit)':    DecisionTreeClassifier(max_depth=20, random_state=42),
    'Random Forest':               RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
}

for name, model in models.items():
    # Single split estimate
    model.fit(X_train, y_train)
    single = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

    # Cross-validation estimate (more reliable)
    cv = cross_val_score(model, X, y, cv=5, scoring='roc_auc', n_jobs=-1)
    print(f"\n  {name}")
    print(f"    Single split AUC : {single:.4f}")
    print(f"    5-fold CV AUC    : {cv.mean():.4f} ± {cv.std():.4f}")

# ── 4. Validation curve ───────────────────────────────────────────────────────
param_range = np.arange(1, 20)
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=42), X, y,
    param_name='max_depth', param_range=param_range,
    cv=5, scoring='roc_auc', n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std  = train_scores.std(axis=1)
val_mean   = val_scores.mean(axis=1)
val_std    = val_scores.std(axis=1)

# ── 5. Learning curve (how much data do we need?) ────────────────────────────
train_sizes, lc_train, lc_val = learning_curve(
    DecisionTreeClassifier(max_depth=best_depth, random_state=42),
    X, y, cv=5, scoring='roc_auc',
    train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
)

# ── 6. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Overfitting curve
axes[0].plot(depths, train_aucs, label='Train AUC', color='steelblue')
axes[0].plot(depths, test_aucs,  label='Test AUC',  color='crimson')
axes[0].axvline(best_depth, color='green', linestyle='--', label=f'Best depth={best_depth}')
axes[0].set_xlabel('Tree Max Depth')
axes[0].set_ylabel('ROC AUC')
axes[0].set_title('Overfitting: Train vs Test AUC')
axes[0].legend()

# Validation curve with confidence bands
axes[1].plot(param_range, train_mean, label='Train CV AUC', color='steelblue')
axes[1].fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.2, color='steelblue')
axes[1].plot(param_range, val_mean, label='Val CV AUC', color='crimson')
axes[1].fill_between(param_range, val_mean - val_std, val_mean + val_std, alpha=0.2, color='crimson')
axes[1].set_xlabel('max_depth')
axes[1].set_ylabel('ROC AUC')
axes[1].set_title('Validation Curve (5-fold CV)')
axes[1].legend()

# Learning curve
lc_train_mean = lc_train.mean(axis=1)
lc_val_mean   = lc_val.mean(axis=1)
axes[2].plot(train_sizes, lc_train_mean, label='Train AUC', color='steelblue')
axes[2].plot(train_sizes, lc_val_mean,   label='Val AUC',   color='crimson')
axes[2].set_xlabel('Training Set Size')
axes[2].set_ylabel('ROC AUC')
axes[2].set_title('Learning Curve (how much data do we need?)')
axes[2].legend()

plt.tight_layout()
plt.savefig('module2_intermediate/lesson4_overfitting.png')
plt.show()
print("\nPlot saved to module2_intermediate/lesson4_overfitting.png")
