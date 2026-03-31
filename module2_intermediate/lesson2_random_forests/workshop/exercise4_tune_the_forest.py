# =============================================================================
# LESSON 2.2 | WORKSHOP | Exercise 4 of 4
# Tune the Forest
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How n_estimators affects accuracy and diminishing returns
# - How to find the elbow of the learning curve
# - How max_features controls tree diversity
# - How to balance training time vs accuracy
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson2_random_forests/workshop/exercise4_tune_the_forest.py
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
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
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# Adding more trees always helps, but returns diminish. The learning curve
# shows accuracy rising steeply at first (1→50 trees) then flattening (50→500).
# The "elbow" is where adding more trees costs significant compute for
# minimal accuracy gain — usually around 100-200 trees.

# =============================================================================
# TASK 1 — n_estimators Learning Curve
# =============================================================================
# For n_estimators in [1, 5, 10, 25, 50, 100, 200, 500]:
#   - Train a RandomForestClassifier (random_state=42, n_jobs=-1)
#   - Record test accuracy and training time
# Print a table.

print("=" * 60)
print("TASK 1 — n_estimators learning curve")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   n_list = [1, 5, 10, 25, 50, 100, 200, 500]
#   accs, times = [], []
#   print(f"{'n_estimators':>13} | {'Test Acc':>9} | {'Time (s)':>9}")
#   print("-" * 38)
#   for n_est in n_list:
#       t0 = time.time()
#       rf = RandomForestClassifier(n_estimators=n_est, random_state=42, n_jobs=-1)
#       rf.fit(X_train, y_train)
#       elapsed = time.time() - t0
#       acc = rf.score(X_test, y_test)
#       accs.append(acc)
#       times.append(elapsed)
#       print(f"{n_est:>13} | {acc:>9.3f} | {elapsed:>9.2f}")

# EXPECTED OUTPUT:
#  n_estimators | Test Acc | Time (s)
#             1 |    0.891 |     0.01
#             5 |    0.921 |     0.04
#           100 |    0.943 |     0.65
#           500 |    0.944 |     3.15

# =============================================================================
# TASK 2 — Find the Elbow
# =============================================================================
# From the results in Task 1, identify the smallest n_estimators where
# the accuracy improvement over the next step is < 0.001 (0.1%).
# Print this as the "recommended minimum".
# Also plot the learning curve.

print("\n" + "=" * 60)
print("TASK 2 — Find the elbow of the learning curve")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   for i in range(1, len(accs)):
#       gain = accs[i] - accs[i-1]
#       if gain < 0.001:
#           print(f"Elbow at n_estimators={n_list[i]}: improvement dropped below 0.1%")
#           print(f"Recommended minimum n_estimators: {n_list[i-1]}")
#           break
#
#   plt.figure(figsize=(9, 5))
#   plt.plot(n_list, accs, 'b-o', markersize=5)
#   plt.xlabel('n_estimators')
#   plt.ylabel('Test Accuracy')
#   plt.title('Random Forest Learning Curve (n_estimators)')
#   plt.grid(True, alpha=0.3)
#   plt.xscale('log')
#   plt.show()

# EXPECTED OUTPUT:
# Elbow at n_estimators=100: improvement dropped below 0.1%
# Recommended minimum n_estimators: 100

# =============================================================================
# TASK 3 — max_features Comparison
# =============================================================================
# For n_estimators=100, train forests with max_features in:
#   [1, 2, 3, 4, 5, 'sqrt', 'log2']
# Print test accuracy for each. Identify which is best.

print("\n" + "=" * 60)
print("TASK 3 — max_features comparison")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   mf_options = [1, 2, 3, 4, 5, 'sqrt', 'log2']
#   results = []
#   for mf in mf_options:
#       rf = RandomForestClassifier(n_estimators=100, max_features=mf,
#                                    random_state=42, n_jobs=-1)
#       rf.fit(X_train, y_train)
#       acc = rf.score(X_test, y_test)
#       results.append((str(mf), acc))
#   results.sort(key=lambda x: x[1], reverse=True)
#   print(f"{'max_features':>12} | {'Accuracy':>9}")
#   print("-" * 26)
#   for mf_str, acc in results:
#       marker = " ← best" if acc == results[0][1] else ""
#       print(f"{mf_str:>12} | {acc:>9.3f}{marker}")

# EXPECTED OUTPUT:
# max_features | Accuracy
#         sqrt |   0.943  ← best
#         log2 |   0.941
#            3 |   0.941
#            4 |   0.939
#            ...

# =============================================================================
# TASK 4 (BONUS) — Accuracy vs Training Time Scatter
# =============================================================================
# Using the Task 1 results, create a scatter plot:
#   x-axis: training time (seconds)
#   y-axis: test accuracy
# Label each point with n_estimators.
# Mark the "sweet spot" (best accuracy/time ratio).

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Accuracy vs time tradeoff")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   fig, ax = plt.subplots(figsize=(8, 5))
#   ax.scatter(times, accs, s=80, color='steelblue', zorder=5)
#   for i, n_est in enumerate(n_list):
#       ax.annotate(str(n_est), (times[i], accs[i]),
#                   textcoords='offset points', xytext=(5, 5), fontsize=9)
#   ax.set_xlabel('Training Time (seconds)')
#   ax.set_ylabel('Test Accuracy')
#   ax.set_title('Accuracy vs Training Time — Random Forest')
#   ax.grid(True, alpha=0.3)
#   plt.tight_layout()
#   plt.show()

print("\n--- Exercise 4 complete. Lesson 2.2 workshop done! ---")
print("--- Next: module2_intermediate/lesson3_clustering_anomaly/ ---")
