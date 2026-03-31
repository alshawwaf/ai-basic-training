# =============================================================================
# LESSON 2.1 | WORKSHOP | Exercise 3 of 4
# Categorical Encoding
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - The difference between LabelEncoder and OneHotEncoder
# - Why one-hot encoding is preferred for nominal categories in linear models
# - The dummy variable trap and how to avoid it with drop='first'
# - How pd.get_dummies compares to sklearn's OneHotEncoder
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson1_feature_engineering/workshop/exercise3_categorical_encoding.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# --- Raw log (do not modify) ------------------------------------------------
np.random.seed(42)
n = 200
protocols  = np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.6, 0.3, 0.1])
actions    = np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.8, 0.2])
raw_df = pd.DataFrame({
    'bytes_sent':   np.random.exponential(5000, n).astype(int),
    'bytes_received': np.random.exponential(8000, n).astype(int),
    'packets':      np.random.poisson(15, n),
    'duration':     np.random.exponential(2, n).clip(0.01),
    'protocol':     protocols,
    'dst_port':     np.random.choice([80, 443, 22, 3389, 8080, 53], n),
    'action':       actions
})
y = (raw_df['action'] == 'BLOCK').astype(int)
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# sklearn requires all features to be numeric. The 'protocol' column contains
# strings: 'TCP', 'UDP', 'ICMP'. We have two main encoding options:
#
#   LabelEncoder:    TCP→1, UDP→2, ICMP→0  — assigns integers
#     PROBLEM: implies TCP > ICMP, UDP > TCP, which is meaningless
#
#   OneHotEncoder:   [1,0] for TCP, [0,1] for UDP, [0,0] for ICMP
#     BETTER: each category is independent; no false ordering
#     (drop='first' removes one column to avoid multicollinearity)

# =============================================================================
# TASK 1 — LabelEncoder
# =============================================================================
# Apply LabelEncoder to raw_df['protocol'].
# Print the mapping: for each class, show which integer it was assigned.
# Add a comment explaining why this would mislead a logistic regression.

print("=" * 60)
print("TASK 1 — LabelEncoder on protocol")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   le = LabelEncoder()
#   labels_encoded = le.fit_transform(raw_df['protocol'])
#   print("LabelEncoder mapping:")
#   for cls, code in zip(le.classes_, range(len(le.classes_))):
#       print(f"  {cls} → {code}")
#   print(f"\nFirst 10 encoded values: {labels_encoded[:10]}")
#   # Comment: logistic regression will treat code 2 (UDP) as "2x" more than
#   # code 1 (TCP), which has no semantic meaning for protocols.

# EXPECTED OUTPUT:
# LabelEncoder mapping:
#   ICMP → 0
#   TCP  → 1
#   UDP  → 2

# =============================================================================
# TASK 2 — OneHotEncoder
# =============================================================================
# Apply OneHotEncoder(drop='first', sparse_output=False) to raw_df[['protocol']].
# Print:
#   - The feature names after encoding
#   - The first 5 encoded rows with the corresponding raw protocol value

print("\n" + "=" * 60)
print("TASK 2 — OneHotEncoder (drop first category)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   ohe = OneHotEncoder(drop='first', sparse_output=False)
#   proto_encoded = ohe.fit_transform(raw_df[['protocol']])
#   feature_names = ohe.get_feature_names_out(['protocol'])
#   print(f"Feature names: {list(feature_names)}")
#   print("(First category dropped is the reference = ICMP)")
#   encoded_df = pd.DataFrame(proto_encoded, columns=feature_names)
#   encoded_df['original'] = raw_df['protocol'].values
#   print("\nFirst 5 rows:")
#   print(encoded_df.head().to_string(index=False))

# EXPECTED OUTPUT:
# Feature names: ['protocol_TCP', 'protocol_UDP']
# (ICMP = reference category, encoded as [0, 0])
# First 5 rows:
#   protocol_TCP  protocol_UDP  original
#      1.0           0.0          TCP
#      0.0           1.0          UDP
#      ...

# =============================================================================
# TASK 3 — pd.get_dummies Comparison
# =============================================================================
# Use pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True).
# Compare the resulting columns to those from Task 2 (should match).
# Print first 5 rows.

print("\n" + "=" * 60)
print("TASK 3 — pd.get_dummies comparison")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)
#   print("get_dummies result (first 5 rows):")
#   print(dummies.head().to_string(index=False))
#
#   # Check if they match OHE (values should be the same)
#   ohe_df = pd.DataFrame(proto_encoded.astype(int), columns=['TCP', 'UDP'])
#   dum_df = dummies.astype(int)
#   dum_df.columns = ['TCP', 'UDP']
#   match = ohe_df.equals(dum_df)
#   print(f"\nget_dummies matches OneHotEncoder: {match}")

# EXPECTED OUTPUT:
# proto_TCP  proto_UDP
#     1          0
#     0          1
#     ...
# Matches OneHotEncoder: True

# =============================================================================
# TASK 4 (BONUS) — Compare LabelEncoded vs OneHotEncoded Model Accuracy
# =============================================================================
# Build two feature sets:
#   feat_label: [bytes_sent, packets, duration, label_encoded_protocol]
#   feat_ohe:   [bytes_sent, packets, duration, proto_TCP, proto_UDP]
# Split, fit LogisticRegression on each, compare test accuracy.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — LabelEncoded vs OneHotEncoded model accuracy")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   base_features = raw_df[['bytes_sent', 'packets', 'duration']].copy()
#
#   # Label encoded version
#   X_label = base_features.copy()
#   X_label['protocol'] = labels_encoded
#
#   # OHE version
#   X_ohe = pd.concat([base_features, dummies.astype(int)], axis=1)
#
#   for name, X in [("LabelEncoded", X_label), ("OneHotEncoded", X_ohe)]:
#       X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
#       m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
#       acc = m.score(X_te, y_te)
#       print(f"{name:18s} accuracy: {acc:.3f}")

# EXPECTED OUTPUT:
# LabelEncoded       accuracy: ~0.847
# OneHotEncoded      accuracy: ~0.863

print("\n--- Exercise 3 complete. Move to exercise4_scaling_and_validation.py ---")
