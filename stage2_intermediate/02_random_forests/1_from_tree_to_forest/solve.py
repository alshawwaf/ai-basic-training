# Exercise 1 — From Tree to Forest
#
# Goal: See why a single unlimited decision tree overfits, how manual
#       bagging (bootstrap aggregation) improves things, and how
#       averaging many trees reduces variance.

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)

# ── Generate synthetic PE file features (self-contained) ─────────────────────
# Features inspired by static malware analysis: entropy, imports, packer, etc.
n = 3000

def make_pe_features(n_samples, malware=False):
    if malware:
        return {
            'file_entropy':       np.random.normal(7.2, 0.5, n_samples).clip(4, 8),
            'num_sections':       np.random.poisson(6, n_samples).clip(2, 20),
            'num_imports':        np.random.poisson(15, n_samples).clip(0, 60),
            'num_exports':        np.random.poisson(2, n_samples).clip(0, 20),
            'has_debug_info':     np.random.binomial(1, 0.05, n_samples),
            'virtual_size_ratio': np.random.normal(3.5, 1, n_samples).clip(1, 10),
            'uses_network_dlls':  np.random.binomial(1, 0.75, n_samples),
            'uses_crypto_dlls':   np.random.binomial(1, 0.60, n_samples),
            'file_size_kb':       np.random.lognormal(7, 1.5, n_samples).clip(10, 20000),
            'code_section_size':  np.random.lognormal(9, 1, n_samples).clip(100, 500000),
            'suspicious_strings': np.random.poisson(8, n_samples).clip(0, 40),
            'has_valid_signature':np.random.binomial(1, 0.08, n_samples),
            'packer_detected':    np.random.binomial(1, 0.65, n_samples),
        }
    else:
        return {
            'file_entropy':       np.random.normal(5.5, 0.8, n_samples).clip(2, 7.5),
            'num_sections':       np.random.poisson(4, n_samples).clip(1, 8),
            'num_imports':        np.random.poisson(80, n_samples).clip(10, 250),
            'num_exports':        np.random.poisson(30, n_samples).clip(0, 150),
            'has_debug_info':     np.random.binomial(1, 0.60, n_samples),
            'virtual_size_ratio': np.random.normal(1.2, 0.3, n_samples).clip(0.8, 3),
            'uses_network_dlls':  np.random.binomial(1, 0.30, n_samples),
            'uses_crypto_dlls':   np.random.binomial(1, 0.20, n_samples),
            'file_size_kb':       np.random.lognormal(9, 1.2, n_samples).clip(50, 200000),
            'code_section_size':  np.random.lognormal(11, 1, n_samples).clip(1000, 10000000),
            'suspicious_strings': np.random.poisson(1, n_samples).clip(0, 5),
            'has_valid_signature':np.random.binomial(1, 0.80, n_samples),
            'packer_detected':    np.random.binomial(1, 0.05, n_samples),
        }

malware_df = pd.DataFrame(make_pe_features(n // 2, malware=True))
malware_df['label'] = 1
benign_df  = pd.DataFrame(make_pe_features(n // 2, malware=False))
benign_df['label']  = 0

df = pd.concat([malware_df, benign_df], ignore_index=True).sample(frac=1, random_state=42)

feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# TASK 1 — Single tree with no depth limit
# ============================================================
# An unlimited tree grows until every training sample is perfectly classified.
# This memorises noise — great on train, poor on test.
print("=" * 60)
print("TASK 1 — Single tree with no depth limit")
print("=" * 60)

tree_unlimited = DecisionTreeClassifier(max_depth=None, random_state=42)
tree_unlimited.fit(X_train, y_train)

train_acc = accuracy_score(y_train, tree_unlimited.predict(X_train))
test_acc  = accuracy_score(y_test, tree_unlimited.predict(X_test))
gap       = train_acc - test_acc

print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")
print(f"Overfit gap:       {gap:.3f}")
print(f"\nTraining accuracy of 1.000 is suspicious — the tree memorised the training set.")

# ============================================================
# TASK 2 — Manual bagging demo
# ============================================================
# Create 10 bootstrap samples (sampling with replacement), train one
# tree on each, and average their predictions. This is bagging by hand.
print("\n" + "=" * 60)
print("TASK 2 — Manual bagging (10 trees)")
print("=" * 60)

n_trees_manual = 10
predictions = np.zeros((len(X_test), n_trees_manual))

for i in range(n_trees_manual):
    # Bootstrap sample: sample N rows WITH replacement
    boot_idx = np.random.choice(len(X_train), size=len(X_train), replace=True)
    X_boot = X_train.iloc[boot_idx]
    y_boot = y_train.iloc[boot_idx]

    tree = DecisionTreeClassifier(max_depth=None, random_state=i)
    tree.fit(X_boot, y_boot)
    predictions[:, i] = tree.predict(X_test)

# Majority vote across the 10 trees
ensemble_pred = (predictions.mean(axis=1) >= 0.5).astype(int)
bagging_acc   = accuracy_score(y_test, ensemble_pred)

print(f"Manual bagging test accuracy: {bagging_acc:.3f}")
print(f"Single tree test accuracy:    {test_acc:.3f}")
print(f"Improvement from bagging:     {bagging_acc - test_acc:+.3f}")

# ============================================================
# TASK 3 — Show the variance reduction
# ============================================================
# Single trees are unstable: different random seeds -> very different accuracies.
# Random forests are stable: averaging many trees cancels out individual noise.
print("\n" + "=" * 60)
print("TASK 3 — Variance reduction: single trees vs forests")
print("=" * 60)

n_runs = 20

# 20 single trees with different seeds
tree_accs = []
for i in range(n_runs):
    t = DecisionTreeClassifier(max_depth=None, random_state=i)
    t.fit(X_train, y_train)
    tree_accs.append(accuracy_score(y_test, t.predict(X_test)))

# 20 random forests with different seeds
forest_accs = []
for i in range(n_runs):
    rf = RandomForestClassifier(n_estimators=100, random_state=i, n_jobs=-1)
    rf.fit(X_train, y_train)
    forest_accs.append(accuracy_score(y_test, rf.predict(X_test)))

tree_accs   = np.array(tree_accs)
forest_accs = np.array(forest_accs)

print(f"20 single trees:   mean={tree_accs.mean():.3f}, std={tree_accs.std():.3f}  <- high variance!")
print(f"20 random forests: mean={forest_accs.mean():.3f}, std={forest_accs.std():.3f}  <- much more stable")
print(f"\nVariance ratio: {tree_accs.std() / forest_accs.std():.1f}x higher for single trees")

# ============================================================
# TASK 4 (BONUS) — OOB score
# ============================================================
# Out-of-bag: each bootstrap sample leaves ~37% of training rows unused.
# Those unused rows serve as a free validation set. oob_score_ approximates
# test accuracy without needing a separate hold-out set.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — OOB score")
print("=" * 60)

rf_oob = RandomForestClassifier(n_estimators=200, oob_score=True,
                                 random_state=42, n_jobs=-1)
rf_oob.fit(X_train, y_train)

oob_score  = rf_oob.oob_score_
test_score = accuracy_score(y_test, rf_oob.predict(X_test))

print(f"OOB score:    {oob_score:.4f}")
print(f"Test score:   {test_score:.4f}")
print(f"Difference:   {abs(oob_score - test_score):.4f}")
print(f"\nOOB is a reliable proxy for test performance — no extra data needed.")

print("\n--- Exercise 1 complete. Move to ../2_train_random_forest/solve.py ---")
