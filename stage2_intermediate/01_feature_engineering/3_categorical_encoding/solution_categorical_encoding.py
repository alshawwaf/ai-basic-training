# Exercise 3 — Categorical Encoding
#
# Goal: Understand LabelEncoder vs OneHotEncoder, see why one-hot encoding
#       is preferred for nominal categories, and learn the dummy variable trap.

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)

# ── Rebuild the raw log with a binary label (self-contained) ─────────────────
n = 200
n_attack = 30  # 15% attack rate

raw_df = pd.DataFrame({
    'dst_port':     np.random.choice([80, 443, 22, 53, 3389], n,
                                     p=[0.30, 0.30, 0.15, 0.15, 0.10]),
    'protocol':     np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.7, 0.25, 0.05]),
    'bytes_sent':   np.random.lognormal(7, 1.2, n).astype(int).clip(100, 100000),
    'bytes_recv':   np.random.lognormal(8, 1.5, n).astype(int).clip(100, 500000),
    'packets':      np.random.poisson(40, n).clip(1, 200),
    'duration':     np.random.exponential(15, n).clip(0.05, 300),
})

# Simple binary label: connections with high bytes_sent and low duration are "attacks"
raw_df['label'] = ((raw_df['bytes_sent'] > raw_df['bytes_sent'].quantile(0.85)) &
                   (raw_df['duration'] < raw_df['duration'].quantile(0.30))).astype(int)

# ============================================================
# TASK 1 — LabelEncoder on protocol
# ============================================================
# LabelEncoder maps each category to an integer: ICMP=0, TCP=1, UDP=2.
# Problem: this implies an ordering (ICMP < TCP < UDP) that does not exist.
# A linear model treats the integers as a numeric scale — meaningless here.
print("=" * 60)
print("TASK 1 — LabelEncoder on protocol")
print("=" * 60)

le = LabelEncoder()
raw_df['protocol_label'] = le.fit_transform(raw_df['protocol'])

# Show the mapping
print("LabelEncoder mapping:")
for cls, idx in zip(le.classes_, range(len(le.classes_))):
    print(f"  {cls} -> {idx}")

print(f"\nProblem: treats TCP ({le.transform(['TCP'])[0]}) as halfway between "
      f"ICMP ({le.transform(['ICMP'])[0]}) and "
      f"UDP ({le.transform(['UDP'])[0]}) — meaningless!")
print("A logistic regression would learn a coefficient for this number,")
print("implying 'distance' between protocols that does not exist.")

# ============================================================
# TASK 2 — OneHotEncoder on protocol
# ============================================================
# OneHotEncoder creates one binary column per category.
# drop='first' avoids the dummy variable trap (multicollinearity).
print("\n" + "=" * 60)
print("TASK 2 — OneHotEncoder on protocol (drop first)")
print("=" * 60)

ohe = OneHotEncoder(sparse_output=False, drop='first')
protocol_encoded = ohe.fit_transform(raw_df[['protocol']])

# Get the feature names that remain after dropping the first category
ohe_feature_names = ohe.get_feature_names_out(['protocol'])

print(f"Feature names: {list(ohe_feature_names)}")
print(f"Dropped reference category: {ohe.categories_[0][0]}")
print(f"\nFirst 5 encoded rows:")
ohe_df = pd.DataFrame(protocol_encoded, columns=ohe_feature_names)
print(ohe_df.head().to_string())

# ============================================================
# TASK 3 — pd.get_dummies comparison
# ============================================================
# pd.get_dummies is a convenient pandas alternative to OneHotEncoder.
# Verify it produces the same result (column order may differ).
print("\n" + "=" * 60)
print("TASK 3 — pd.get_dummies comparison")
print("=" * 60)

dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)
print("pd.get_dummies result (first 5 rows):")
print(dummies.head().to_string())

# Compare: get_dummies should produce the same binary matrix as OHE
# (column names differ in prefix, but values should match)
ohe_values = ohe_df.values
dum_values = dummies.values
match = np.allclose(ohe_values, dum_values)
print(f"\nValues match OneHotEncoder: {match}")

# ============================================================
# TASK 4 (BONUS) — Encoding comparison demo
# ============================================================
# Fit a LogisticRegression with LabelEncoded protocol vs OneHotEncoded.
# Show that encoding choice affects model quality.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Encoding comparison demo")
print("=" * 60)

y = raw_df['label']
base_features = ['bytes_sent', 'bytes_recv', 'packets', 'duration']

# LabelEncoded features — protocol as a single integer column
X_label = raw_df[base_features + ['protocol_label']].copy()

# OneHotEncoded features — protocol as binary columns
X_onehot = pd.concat([raw_df[base_features], ohe_df], axis=1)

results = {}
for name, X in [('LabelEncoded', X_label), ('OneHotEncoded', X_onehot)]:
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                               random_state=42, stratify=y)
    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    results[name] = acc
    print(f"  {name:<20} accuracy: {acc:.3f}")

diff = results['OneHotEncoded'] - results['LabelEncoded']
print(f"\n  Difference: {diff:+.3f}  ({'OHE is better' if diff > 0 else 'LabelEncoded is better' if diff < 0 else 'Same'})")
print("\nNote: For tree-based models (Random Forest, Decision Tree) label encoding")
print("works fine because trees split on thresholds, not distances. But for linear")
print("models and neural networks, always use one-hot encoding for nominal features.")

print("\n--- Exercise 3 complete. Move to ../4_scaling_and_validation/solution.py ---")
