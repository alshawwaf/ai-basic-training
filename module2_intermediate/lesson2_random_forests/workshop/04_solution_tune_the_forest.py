# Exercise 4 — Tune the Forest
#
# Goal: Understand how n_estimators and max_features affect accuracy
#       and training time, find the elbow where more trees stop helping,
#       and identify the cost-effective sweet spot.

import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
X = df[feature_cols]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# TASK 1 — n_estimators learning curve
# ============================================================
# Train forests with increasing tree counts. Record test accuracy and
# wall-clock training time for each. Diminishing returns appear quickly.
print("=" * 60)
print("TASK 1 — n_estimators learning curve")
print("=" * 60)

tree_counts = [1, 5, 10, 25, 50, 100, 200, 500]
accs   = []
times  = []

print(f"{'n_estimators':>12} | {'Test Acc':>8} | {'Train Time (s)':>14}")
print("-" * 42)

for n_trees in tree_counts:
    t0 = time.time()
    rf = RandomForestClassifier(n_estimators=n_trees, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    elapsed = time.time() - t0

    acc = accuracy_score(y_test, rf.predict(X_test))
    accs.append(acc)
    times.append(elapsed)
    print(f"{n_trees:>12} | {acc:>8.3f} | {elapsed:>14.3f}")

# ============================================================
# TASK 2 — Find the elbow
# ============================================================
# The elbow is where adding more trees gives < 0.1% improvement.
# Beyond this point, extra trees cost CPU time for negligible gains.
print("\n" + "=" * 60)
print("TASK 2 — Find the elbow")
print("=" * 60)

elbow_idx = None
for i in range(1, len(accs)):
    improvement = accs[i] - accs[i-1]
    if improvement < 0.001:    # less than 0.1% improvement
        elbow_idx = i - 1      # the previous value was the last meaningful step
        break

if elbow_idx is not None:
    print(f"Recommended minimum n_estimators: {tree_counts[elbow_idx]}")
    print(f"  Accuracy at {tree_counts[elbow_idx]} trees: {accs[elbow_idx]:.3f}")
    print(f"  Accuracy at {tree_counts[-1]} trees:  {accs[-1]:.3f}")
    print(f"  Beyond {tree_counts[elbow_idx]}, accuracy improvement < 0.1%")
else:
    print("No clear elbow found — all steps showed > 0.1% improvement")
    print(f"Using largest tested: {tree_counts[-1]} trees with acc {accs[-1]:.3f}")

# ============================================================
# TASK 3 — max_features comparison
# ============================================================
# max_features controls how many features each tree considers per split.
# Fewer features = more diverse trees = better ensemble, but each
# individual tree is weaker. 'sqrt' is the standard default.
print("\n" + "=" * 60)
print("TASK 3 — max_features comparison (n_estimators=100)")
print("=" * 60)

max_features_options = [1, 2, 3, 4, 5, 'sqrt', 'log2']
mf_results = []

for mf in max_features_options:
    rf = RandomForestClassifier(n_estimators=100, max_features=mf,
                                 random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    acc = accuracy_score(y_test, rf.predict(X_test))
    mf_results.append((mf, acc))

# Sort by accuracy descending
mf_results.sort(key=lambda x: x[1], reverse=True)

print(f"{'max_features':>12} | {'Accuracy':>8}")
print("-" * 25)
for mf, acc in mf_results:
    marker = " <- default" if mf == 'sqrt' else ""
    print(f"{str(mf):>12} | {acc:>8.3f}{marker}")

# ============================================================
# TASK 4 (BONUS) — Training time vs accuracy tradeoff
# ============================================================
# Scatter plot: x=training time, y=accuracy, each point labelled with n_estimators.
# The sweet spot is high accuracy with low training time.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Training time vs accuracy tradeoff plot")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: accuracy vs n_estimators
axes[0].plot(tree_counts, accs, marker='o', color='steelblue')
axes[0].set_xlabel('Number of Trees (n_estimators)')
axes[0].set_ylabel('Test Accuracy')
axes[0].set_title('Accuracy vs Number of Trees')
if elbow_idx is not None:
    axes[0].axvline(tree_counts[elbow_idx], color='red', linestyle='--',
                    label=f'Elbow at {tree_counts[elbow_idx]}')
    axes[0].legend()

# Right: accuracy vs training time with labels
axes[1].scatter(times, accs, color='crimson', s=60, zorder=5)
for i, n_t in enumerate(tree_counts):
    axes[1].annotate(f"n={n_t}", (times[i], accs[i]),
                     textcoords="offset points", xytext=(8, 5), fontsize=8)
axes[1].set_xlabel('Training Time (seconds)')
axes[1].set_ylabel('Test Accuracy')
axes[1].set_title('Accuracy vs Training Time (sweet spot = top-left)')

plt.tight_layout()
plt.savefig('module2_intermediate/lesson2_tune_forest.png')
plt.close()
print("Plot saved to module2_intermediate/lesson2_tune_forest.png")

print(f"\nSweet spot: n_estimators={tree_counts[elbow_idx] if elbow_idx else tree_counts[-1]} "
      f"gives {accs[elbow_idx] if elbow_idx else accs[-1]:.3f} accuracy "
      f"in {times[elbow_idx] if elbow_idx else times[-1]:.2f}s")

print("\n--- Exercise 4 complete. Lesson 2 done! ---")
