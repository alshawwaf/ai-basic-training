# Exercise 2 — Train a Random Forest
#
# Goal: Train a RandomForestClassifier on PE file features, compare it
#       to a single tree, read the classification report, and explore
#       predict_proba for false-positive / hard-to-detect analysis.

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

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
X = df[feature_cols]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# TASK 1 — Train the random forest
# ============================================================
# n_estimators=100 trees, oob_score=True for a free validation estimate,
# n_jobs=-1 uses all CPU cores for parallel training.
print("=" * 60)
print("TASK 1 — Train the random forest")
print("=" * 60)

forest = RandomForestClassifier(
    n_estimators=100, oob_score=True, random_state=42, n_jobs=-1
)
forest.fit(X_train, y_train)

train_acc = accuracy_score(y_train, forest.predict(X_train))
test_acc  = accuracy_score(y_test, forest.predict(X_test))

print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")
print(f"OOB score:         {forest.oob_score_:.3f}")

# ============================================================
# TASK 2 — Compare single tree vs forest
# ============================================================
# Single unlimited tree overfits (train=1.000); the forest generalises better.
print("\n" + "=" * 60)
print("TASK 2 — Single tree vs forest comparison")
print("=" * 60)

single_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
single_tree.fit(X_train, y_train)

tree_train = accuracy_score(y_train, single_tree.predict(X_train))
tree_test  = accuracy_score(y_test, single_tree.predict(X_test))

print(f"{'Model':<30} {'Train Acc':>10} {'Test Acc':>10} {'OOB':>10}")
print("-" * 62)
print(f"{'Single Tree (no limit)':<30} {tree_train:>10.3f} {tree_test:>10.3f} {'N/A':>10}")
print(f"{'Random Forest (100 trees)':<30} {train_acc:>10.3f} {test_acc:>10.3f} {forest.oob_score_:>10.3f}")

# ============================================================
# TASK 3 — Classification report
# ============================================================
# Focus on recall for the malware class — missing malware is costly.
# precision = "of files flagged as malware, how many really are?"
# recall    = "of actual malware files, how many did we catch?"
print("\n" + "=" * 60)
print("TASK 3 — Classification report (Random Forest)")
print("=" * 60)

y_pred = forest.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Benign', 'Malware']))

# ============================================================
# TASK 4 (BONUS) — Predict probabilities
# ============================================================
# predict_proba gives P(malware) for each sample. This lets us find:
# - False positives: benign files the model is most confident are malware
# - Hard-to-detect malware: actual malware with lowest P(malware)
print("=" * 60)
print("TASK 4 (BONUS) — Predict probabilities analysis")
print("=" * 60)

proba = forest.predict_proba(X_test)[:, 1]   # P(malware)

# Build a results DataFrame for analysis
results_df = X_test.copy()
results_df['true_label'] = y_test.values
results_df['p_malware']  = proba

# Top 5 false positives: benign files with highest P(malware)
benign_results = results_df[results_df['true_label'] == 0].sort_values('p_malware', ascending=False)
print("Top 5 false positives (benign files the model thinks are malware):")
for i, (_, row) in enumerate(benign_results.head(5).iterrows()):
    print(f"  {i+1}. entropy={row['file_entropy']:.1f}, packer={int(row['packer_detected'])}, "
          f"signature={int(row['has_valid_signature'])}, P(malware)={row['p_malware']:.3f}")

# Top 5 hard-to-detect malware: actual malware with lowest P(malware)
malware_results = results_df[results_df['true_label'] == 1].sort_values('p_malware', ascending=True)
print("\nTop 5 hardest-to-detect malware (lowest P(malware) among actual malware):")
for i, (_, row) in enumerate(malware_results.head(5).iterrows()):
    print(f"  {i+1}. entropy={row['file_entropy']:.1f}, packer={int(row['packer_detected'])}, "
          f"signature={int(row['has_valid_signature'])}, P(malware)={row['p_malware']:.3f}")

print("\n--- Exercise 2 complete. Move to 03_solution_feature_importance.py ---")
