# =============================================================================
# LESSON 2.2 | WORKSHOP | Exercise 1 of 4
# From Tree to Forest
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why a single unlimited decision tree overfits dramatically
# - What bagging (bootstrap aggregation) does
# - Why averaging predictions from many trees reduces variance
# - How OOB (Out-of-Bag) score works as a free validation estimate
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson2_random_forests/workshop/exercise1_from_tree_to_forest.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# =============================================================================
# BACKGROUND
# =============================================================================
# A single decision tree with max_depth=None memorises training data → 100% train
# accuracy but poor test accuracy. Random forests fix this with bagging:
# train many trees on random bootstrap samples, then vote. Each tree has high
# variance (different bootstrap = different tree), but the average is stable.
# OOB samples: ~37% of rows are not selected in each bootstrap; they serve
# as a free validation set for that tree.

# --- PE file malware dataset (do not modify) --------------------------------
np.random.seed(42)
n = 2000
benign = pd.DataFrame({
    'file_entropy':      np.random.normal(5.5, 0.8, n//2).clip(3, 7.9),
    'num_sections':      np.random.poisson(4, n//2).clip(2, 10),
    'num_imports':       np.random.normal(80, 25, n//2).clip(5, 200).astype(int),
    'has_packer_sig':    (np.random.rand(n//2) < 0.05).astype(int),
    'virtual_size_ratio':np.random.normal(1.2, 0.3, n//2).clip(0.8, 3),
    'code_section_size': np.random.normal(50000, 20000, n//2).clip(1000, 200000).astype(int),
    'import_entropy':    np.random.normal(4.2, 0.6, n//2).clip(1, 6),
    'label': 0
})
malware = pd.DataFrame({
    'file_entropy':      np.random.normal(7.2, 0.4, n//2).clip(5, 8),
    'num_sections':      np.random.poisson(6, n//2).clip(2, 15),
    'num_imports':       np.random.normal(35, 20, n//2).clip(0, 150).astype(int),
    'has_packer_sig':    (np.random.rand(n//2) < 0.68).astype(int),
    'virtual_size_ratio':np.random.normal(2.8, 0.8, n//2).clip(0.5, 8),
    'code_section_size': np.random.normal(15000, 10000, n//2).clip(500, 100000).astype(int),
    'import_entropy':    np.random.normal(3.1, 0.9, n//2).clip(0.5, 5.5),
    'label': 1
})
df = pd.concat([benign, malware], ignore_index=True).sample(frac=1, random_state=42)
FEATURES = ['file_entropy', 'num_sections', 'num_imports', 'has_packer_sig',
            'virtual_size_ratio', 'code_section_size', 'import_entropy']
X = df[FEATURES]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Single Unlimited Decision Tree
# =============================================================================
# Train DecisionTreeClassifier(max_depth=None, random_state=42).
# Print training accuracy, test accuracy, and the overfit gap.

print("=" * 60)
print("TASK 1 — Single unlimited decision tree")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   single_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
#   single_tree.fit(X_train, y_train)
#   train_acc = single_tree.score(X_train, y_train)
#   test_acc  = single_tree.score(X_test,  y_test)
#   print(f"Training accuracy: {train_acc:.3f}")
#   print(f"Test accuracy:     {test_acc:.3f}")
#   print(f"Overfit gap:       {train_acc - test_acc:.3f}")

# EXPECTED OUTPUT:
# Training accuracy: 1.000
# Test accuracy:     ~0.891
# Overfit gap:       ~0.109

# =============================================================================
# TASK 2 — Manual Bagging Demo (10 Trees)
# =============================================================================
# Without using RandomForestClassifier, manually:
#   1. For each of 10 iterations, draw a bootstrap sample (sampling with replacement)
#   2. Train a DecisionTreeClassifier(max_depth=None) on that sample
#   3. Get predictions on X_test
#   4. Aggregate by majority vote (np.bincount on stacked predictions)
# Print the test accuracy of the ensemble vs the single tree.

print("\n" + "=" * 60)
print("TASK 2 — Manual bagging (10 trees, bootstrap sampling)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   n_trees = 10
#   all_preds = []
#   n_train   = len(X_train)
#   for i in range(n_trees):
#       idx = np.random.choice(n_train, n_train, replace=True)   # bootstrap
#       X_boot = X_train.iloc[idx]
#       y_boot = y_train.iloc[idx]
#       t = DecisionTreeClassifier(max_depth=None, random_state=i)
#       t.fit(X_boot, y_boot)
#       all_preds.append(t.predict(X_test))
#   # Majority vote
#   stacked = np.array(all_preds)   # shape (10, n_test)
#   y_pred_ensemble = np.array([np.bincount(stacked[:, j]).argmax()
#                                for j in range(stacked.shape[1])])
#   ensemble_acc = np.mean(y_pred_ensemble == y_test.values)
#   print(f"Single tree test accuracy:  {test_acc:.3f}")
#   print(f"Manual ensemble (10 trees): {ensemble_acc:.3f}")

# EXPECTED OUTPUT:
# Single tree test accuracy:  ~0.891
# Manual ensemble (10 trees): ~0.931 ← better!

# =============================================================================
# TASK 3 — Variance Comparison
# =============================================================================
# Train 20 individual unlimited trees (different random_state each time).
# Record their test accuracies. Compute mean and std.
# Then train 20 random forests (n_estimators=100, different random_state each).
# Show that the forests have much lower variance.

print("\n" + "=" * 60)
print("TASK 3 — Single tree vs forest: variance comparison")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   tree_accs, forest_accs = [], []
#   for seed in range(20):
#       t = DecisionTreeClassifier(max_depth=None, random_state=seed)
#       t.fit(X_train, y_train)
#       tree_accs.append(t.score(X_test, y_test))
#       rf = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
#       rf.fit(X_train, y_train)
#       forest_accs.append(rf.score(X_test, y_test))
#   print(f"20 single trees:   mean={np.mean(tree_accs):.3f}, std={np.std(tree_accs):.3f}")
#   print(f"20 random forests: mean={np.mean(forest_accs):.3f}, std={np.std(forest_accs):.3f}")

# EXPECTED OUTPUT:
# 20 single trees:   mean=~0.888, std=~0.031  (high variance)
# 20 random forests: mean=~0.943, std=~0.005  (much more stable)

# =============================================================================
# TASK 4 (BONUS) — OOB Score
# =============================================================================
# Train RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42).
# Print oob_score_ and actual test accuracy. Verify they are close.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — OOB score as free validation estimate")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   rf_oob = RandomForestClassifier(n_estimators=200, oob_score=True,
#                                    random_state=42, n_jobs=-1)
#   rf_oob.fit(X_train, y_train)
#   oob = rf_oob.oob_score_
#   test = rf_oob.score(X_test, y_test)
#   print(f"OOB score:   {oob:.3f}")
#   print(f"Test score:  {test:.3f}")
#   print(f"Difference:  {abs(oob - test):.3f}  ← small = OOB is reliable")

# EXPECTED OUTPUT:
# OOB score:   ~0.941
# Test score:  ~0.943
# Difference:  ~0.002

print("\n--- Exercise 1 complete. Move to exercise2_train_random_forest.py ---")
