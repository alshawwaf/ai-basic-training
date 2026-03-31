# =============================================================================
# LESSON 2.2 | WORKSHOP | Exercise 3 of 4
# Feature Importance
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How random forest feature importances are stable across runs
# - Which PE file features are most predictive of malware
# - How to compare importance stability: single tree vs forest
# - How to create a bar chart with error bars
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson2_random_forests/workshop/exercise3_feature_importance.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- PE file dataset (do not modify) ----------------------------------------
np.random.seed(42)
n = 2000
benign = pd.DataFrame({
    'file_entropy':       np.random.normal(5.5, 0.8, n//2).clip(3, 7.9),
    'num_sections':       np.random.poisson(4, n//2).clip(2, 10),
    'num_imports':        np.random.normal(80, 25, n//2).clip(5, 200).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.05).astype(int),
    'virtual_size_ratio': np.random.normal(1.2, 0.3, n//2).clip(0.8, 3),
    'code_section_size':  np.random.normal(50000, 20000, n//2).clip(1000, 200000).astype(int),
    'import_entropy':     np.random.normal(4.2, 0.6, n//2).clip(1, 6),
    'label': 0
})
malware = pd.DataFrame({
    'file_entropy':       np.random.normal(7.2, 0.4, n//2).clip(5, 8),
    'num_sections':       np.random.poisson(6, n//2).clip(2, 15),
    'num_imports':        np.random.normal(35, 20, n//2).clip(0, 150).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.68).astype(int),
    'virtual_size_ratio': np.random.normal(2.8, 0.8, n//2).clip(0.5, 8),
    'code_section_size':  np.random.normal(15000, 10000, n//2).clip(500, 100000).astype(int),
    'import_entropy':     np.random.normal(3.1, 0.9, n//2).clip(0.5, 5.5),
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
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Print Sorted Feature Importances
# =============================================================================
# Extract rf.feature_importances_, create a sorted DataFrame, print it.
# Verify importances sum to 1.0.

print("=" * 60)
print("TASK 1 — Random forest feature importances")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   imp_df = pd.DataFrame({'feature': FEATURES, 'importance': rf.feature_importances_})
#   imp_df = imp_df.sort_values('importance', ascending=False)
#   print(imp_df.to_string(index=False))
#   print(f"\nSum: {rf.feature_importances_.sum():.3f} {'✓' if abs(rf.feature_importances_.sum()-1)<0.001 else '✗'}")

# EXPECTED OUTPUT:
# file_entropy        ~0.382
# has_packer_sig      ~0.241
# virtual_size_ratio  ~0.178
# ...
# Sum: 1.000 ✓

# =============================================================================
# TASK 2 — Stability Comparison (Single Tree vs Forest)
# =============================================================================
# Train 20 single trees and 20 random forests (different random_state each time).
# For each run, record the feature importances array.
# Compute std of importance across 20 runs for each feature.
# Print a comparison table: feature | tree_std | forest_std.

print("\n" + "=" * 60)
print("TASK 2 — Importance stability (20 runs each)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   tree_imps, forest_imps = [], []
#   for seed in range(20):
#       t = DecisionTreeClassifier(max_depth=None, random_state=seed)
#       t.fit(X_train, y_train)
#       tree_imps.append(t.feature_importances_)
#       rf_i = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1)
#       rf_i.fit(X_train, y_train)
#       forest_imps.append(rf_i.feature_importances_)
#   tree_stds   = np.std(tree_imps, axis=0)
#   forest_stds = np.std(forest_imps, axis=0)
#   print(f"{'Feature':22s} {'Tree Std':>10} {'Forest Std':>12}")
#   print("-" * 48)
#   for feat, ts, fs in zip(FEATURES, tree_stds, forest_stds):
#       print(f"{feat:22s} {ts:>10.4f} {fs:>12.4f}")

# EXPECTED OUTPUT:
# Feature                Tree Std  Forest Std
# file_entropy             ~0.042      ~0.004
# has_packer_sig           ~0.038      ~0.003
# ... (forest stds are 5-10x smaller)

# =============================================================================
# TASK 3 — Bar Chart with Error Bars
# =============================================================================
# Using the forest importances from 20 runs, compute mean importance per feature.
# Create a horizontal bar chart sorted by mean importance.
# Add error bars showing std.

print("\n" + "=" * 60)
print("TASK 3 — Feature importance bar chart with error bars")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   mean_imps = np.mean(forest_imps, axis=0)
#   std_imps  = np.std(forest_imps, axis=0)
#   order = np.argsort(mean_imps)
#   fig, ax = plt.subplots(figsize=(8, 5))
#   ax.barh([FEATURES[i] for i in order], mean_imps[order],
#           xerr=std_imps[order], capsize=4, color='steelblue', alpha=0.8)
#   ax.set_xlabel('Feature Importance (mean ± std over 20 runs)')
#   ax.set_title('Random Forest Feature Importance — PE Malware Classifier')
#   plt.tight_layout()
#   plt.show()

print("Bar chart created.")

# =============================================================================
# TASK 4 (BONUS) — Feature Selection with Top-4 Features
# =============================================================================
# Identify the top 4 features. Retrain the forest with only those features.
# Compare accuracy to the full-feature model.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Top-4 feature selection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   top4 = imp_df.nlargest(4, 'importance')['feature'].tolist()
#   print(f"Top-4 features: {top4}")
#   rf_top4 = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
#   rf_top4.fit(X_train[top4], y_train)
#   acc_full = rf.score(X_test, y_test)
#   acc_top4 = rf_top4.score(X_test[top4], y_test)
#   print(f"Full model (7 features):  {acc_full:.3f}")
#   print(f"Top-4 model (4 features): {acc_top4:.3f}")
#   print(f"Accuracy drop:            {acc_full - acc_top4:.3f}")

# EXPECTED OUTPUT:
# Top-4 features: ['file_entropy', 'has_packer_sig', 'virtual_size_ratio', 'import_entropy']
# Full model:  ~0.943
# Top-4 model: ~0.940
# Accuracy drop: ~0.003  (very small — 4 features are nearly as good as 7)

print("\n--- Exercise 3 complete. Move to exercise4_tune_the_forest.py ---")
