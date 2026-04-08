# Exercise 3 — Feature Importance
#
# Goal: Extract and interpret feature importances from a random forest,
#       measure stability vs a single tree, and try feature selection.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)

# ── Generate synthetic PE file features (self-contained) ─────────────────────
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
X = df[feature_cols].astype(float)
y = df['label']

# Add per-feature Gaussian noise so classes overlap (otherwise everything scores 1.000).
rng = np.random.default_rng(13)
X = X + rng.normal(0, X.std(axis=0).values * 1.4, X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# TASK 1 — Print forest feature importances
# ============================================================
# feature_importances_ = total Gini reduction each feature contributed
# across all splits in all trees, normalised so they sum to 1.0.
print("=" * 60)
print("TASK 1 — Forest feature importances")
print("=" * 60)

forest = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
forest.fit(X_train, y_train)

imp = pd.Series(forest.feature_importances_, index=feature_cols).sort_values(ascending=False)

print("Feature importances (sorted):")
for feat, val in imp.items():
    print(f"  {feat:<22} {val:.4f}")
print(f"\nSum: {imp.sum():.3f}  (should be 1.000)")

# ============================================================
# TASK 2 — Stability: single tree vs forest
# ============================================================
# Train 20 models with different seeds. For each feature, compute the
# std of its importance across runs. Forest std should be much smaller.
print("\n" + "=" * 60)
print("TASK 2 — Stability: single tree vs forest (20 runs)")
print("=" * 60)

n_runs = 20

# Collect importances across runs
tree_importances   = np.zeros((n_runs, len(feature_cols)))
forest_importances = np.zeros((n_runs, len(feature_cols)))

for i in range(n_runs):
    # Single tree with different seed
    t = DecisionTreeClassifier(max_depth=None, random_state=i)
    t.fit(X_train, y_train)
    tree_importances[i] = t.feature_importances_

    # Random forest with different seed
    rf = RandomForestClassifier(n_estimators=100, random_state=i, n_jobs=-1)
    rf.fit(X_train, y_train)
    forest_importances[i] = rf.feature_importances_

tree_std   = tree_importances.std(axis=0)
forest_std = forest_importances.std(axis=0)

print(f"{'Feature':<22} {'Tree Std':>10} {'Forest Std':>12}")
print("-" * 46)
for j, feat in enumerate(feature_cols):
    print(f"  {feat:<22} {tree_std[j]:>8.4f}   {forest_std[j]:>10.4f}")

print(f"\nMean std across features:")
print(f"  Single trees: {tree_std.mean():.4f}")
print(f"  Forests:      {forest_std.mean():.4f}")
print(f"  Forest importances are {tree_std.mean()/forest_std.mean():.1f}x more stable")

# ============================================================
# TASK 3 — Top features bar chart with error bars
# ============================================================
# Horizontal bar chart showing mean importance +/- std across 20 forest runs.
print("\n" + "=" * 60)
print("TASK 3 — Top features bar chart (saved to file)")
print("=" * 60)

forest_mean = forest_importances.mean(axis=0)
forest_se   = forest_importances.std(axis=0)

# Sort by mean importance
order = np.argsort(forest_mean)[::-1]

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = range(len(feature_cols))
ax.barh(y_pos, forest_mean[order], xerr=forest_se[order],
        color='steelblue', capsize=3)
ax.set_yticks(y_pos)
ax.set_yticklabels([feature_cols[i] for i in order])
ax.set_xlabel('Mean Gini Importance')
ax.set_title('Feature Importances (20 forest runs, error bars = std)')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('stage2_intermediate/lesson2_feature_importance.png')
plt.close()
print("Plot saved to stage2_intermediate/lesson2_feature_importance.png")

# ============================================================
# TASK 4 (BONUS) — Feature selection
# ============================================================
# Keep only the top 4 features. Retrain the forest. Compare accuracy
# to the full-feature model. A small accuracy drop means the remaining
# features contributed little — simpler model, nearly same performance.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Feature selection (top 4 features)")
print("=" * 60)

top4 = imp.head(4).index.tolist()
print(f"Top 4 features: {top4}")

# Full model accuracy
full_acc = accuracy_score(y_test, forest.predict(X_test))

# Top-4 model
rf_top4 = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf_top4.fit(X_train[top4], y_train)
top4_acc = accuracy_score(y_test, rf_top4.predict(X_test[top4]))

print(f"\nFull model accuracy ({len(feature_cols)} features): {full_acc:.3f}")
print(f"Top-4 model accuracy:                     {top4_acc:.3f}")
print(f"Drop: {full_acc - top4_acc:+.3f}")
print("\nA small drop means the top 4 features carry most of the signal.")
print("Simpler models are faster, easier to explain, and less prone to noise.")

print("\n--- Exercise 3 complete. Move to ../4_tune_the_forest/solution.py ---")
