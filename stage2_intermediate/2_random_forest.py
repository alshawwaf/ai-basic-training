# Lesson 2.2 — Random Forests
#
# Goal: Classify files as malware (1) or benign (0) using PE file features.
# Demonstrates: ensemble learning, OOB scoring, feature importance,
#               comparison with a single decision tree.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import classification_report, roc_auc_score, RocCurveDisplay
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# ── 1. Generate synthetic PE file features ─────────────────────────────────────
# Features inspired by common static malware analysis attributes
n = 3000

def make_pe_features(n, malware=False):
    if malware:
        return {
            'file_entropy':         np.random.normal(7.2, 0.5, n).clip(4, 8),  # high = packed
            'num_sections':         np.random.poisson(6, n).clip(2, 20),
            'num_imports':          np.random.poisson(15, n).clip(0, 60),
            'num_exports':          np.random.poisson(2, n).clip(0, 20),
            'has_debug_info':       np.random.binomial(1, 0.05, n),
            'virtual_size_ratio':   np.random.normal(3.5, 1, n).clip(1, 10),
            'uses_network_dlls':    np.random.binomial(1, 0.75, n),  # WinSock, etc.
            'uses_crypto_dlls':     np.random.binomial(1, 0.60, n),
            'file_size_kb':         np.random.lognormal(7, 1.5, n).clip(10, 20000),
            'code_section_size':    np.random.lognormal(9, 1, n).clip(100, 500000),
            'suspicious_strings':   np.random.poisson(8, n).clip(0, 40),
            'has_valid_signature':  np.random.binomial(1, 0.08, n),
            'packer_detected':      np.random.binomial(1, 0.65, n),
        }
    else:
        return {
            'file_entropy':         np.random.normal(5.5, 0.8, n).clip(2, 7.5),
            'num_sections':         np.random.poisson(4, n).clip(1, 8),
            'num_imports':          np.random.poisson(80, n).clip(10, 250),
            'num_exports':          np.random.poisson(30, n).clip(0, 150),
            'has_debug_info':       np.random.binomial(1, 0.60, n),
            'virtual_size_ratio':   np.random.normal(1.2, 0.3, n).clip(0.8, 3),
            'uses_network_dlls':    np.random.binomial(1, 0.30, n),
            'uses_crypto_dlls':     np.random.binomial(1, 0.20, n),
            'file_size_kb':         np.random.lognormal(9, 1.2, n).clip(50, 200000),
            'code_section_size':    np.random.lognormal(11, 1, n).clip(1000, 10000000),
            'suspicious_strings':   np.random.poisson(1, n).clip(0, 5),
            'has_valid_signature':  np.random.binomial(1, 0.80, n),
            'packer_detected':      np.random.binomial(1, 0.05, n),
        }

malware_df = pd.DataFrame(make_pe_features(n // 2, malware=True))
malware_df['label'] = 1
benign_df  = pd.DataFrame(make_pe_features(n // 2, malware=False))
benign_df['label']  = 0

df = pd.concat([malware_df, benign_df], ignore_index=True).sample(frac=1, random_state=42)

feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols]
y = df['label']

print("=== Dataset ===")
print(df['label'].value_counts().rename({0: 'Benign', 1: 'Malware'}))

# ── 2. Split ───────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Compare: single tree vs random forest ──────────────────────────────────
single_tree = DecisionTreeClassifier(max_depth=8, random_state=42)
single_tree.fit(X_train, y_train)

forest = RandomForestClassifier(
    n_estimators=200, oob_score=True, n_jobs=-1, random_state=42
)
forest.fit(X_train, y_train)

print("\n=== Model Comparison ===")
for name, model in [('Decision Tree (d=8)', single_tree), ('Random Forest (200 trees)', forest)]:
    proba = model.predict_proba(X_test)[:, 1]
    auc   = roc_auc_score(y_test, proba)
    pred  = model.predict(X_test)
    from sklearn.metrics import f1_score
    f1 = f1_score(y_test, pred)
    print(f"  {name:<30}  AUC: {auc:.4f}  F1: {f1:.4f}")

print(f"\nRandom Forest OOB score (free estimate): {forest.oob_score_:.4f}")

# ── 4. Full classification report for forest ──────────────────────────────────
y_pred = forest.predict(X_test)
print("\n=== Random Forest — Full Report ===")
print(classification_report(y_test, y_pred, target_names=['Benign', 'Malware']))

# ── 5. Feature importances ─────────────────────────────────────────────────────
imp = pd.Series(forest.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("=== Top Feature Importances ===")
print(imp.round(4).to_string())

# ── 6. Effect of number of trees (learning curve) ─────────────────────────────
print("\n=== AUC vs Number of Trees ===")
tree_counts = [1, 5, 10, 25, 50, 100, 200]
aucs = []
for n_trees in tree_counts:
    m = RandomForestClassifier(n_estimators=n_trees, random_state=42, n_jobs=-1)
    m.fit(X_train, y_train)
    auc = roc_auc_score(y_test, m.predict_proba(X_test)[:, 1])
    aucs.append(auc)
    print(f"  {n_trees:>4} trees → AUC: {auc:.4f}")

# ── 7. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# ROC curves
for name, model in [('Decision Tree', single_tree), ('Random Forest', forest)]:
    RocCurveDisplay.from_predictions(y_test, model.predict_proba(X_test)[:, 1],
                                     name=name, ax=axes[0])
axes[0].set_title('ROC: Decision Tree vs Random Forest')

# Feature importances
imp.head(8).sort_values().plot(kind='barh', ax=axes[1], color='steelblue')
axes[1].set_title('Top 8 Feature Importances (Random Forest)')

# AUC vs n_estimators
axes[2].plot(tree_counts, aucs, marker='o', color='crimson')
axes[2].set_xlabel('Number of Trees')
axes[2].set_ylabel('ROC AUC')
axes[2].set_title('Performance vs Number of Trees')
axes[2].axhline(aucs[-1], color='grey', linestyle='--', label='200-tree AUC')
axes[2].legend()

plt.tight_layout()
plt.savefig('stage2_intermediate/lesson2_random_forest.png')
plt.show()
print("\nPlot saved to stage2_intermediate/lesson2_random_forest.png")
