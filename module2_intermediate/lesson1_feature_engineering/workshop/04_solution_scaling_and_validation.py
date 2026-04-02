# Exercise 4 — Scaling and Validation
#
# Goal: Assemble a complete feature matrix, scale it properly
#       (fit on train, transform both), compare StandardScaler vs MinMaxScaler,
#       and build a full sklearn Pipeline.

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

np.random.seed(42)

# ── Rebuild features from scratch (self-contained) ──────────────────────────
n = 200

raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='2min'),
    'dst_port':     np.random.choice([80, 443, 22, 53, 3389, 21, 8080], n,
                                     p=[0.30, 0.30, 0.10, 0.10, 0.05, 0.05, 0.10]),
    'protocol':     np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.7, 0.25, 0.05]),
    'bytes_sent':   np.random.lognormal(7, 1.2, n).astype(int).clip(100, 100000),
    'bytes_recv':   np.random.lognormal(8, 1.5, n).astype(int).clip(100, 500000),
    'packets':      np.random.poisson(40, n).clip(1, 200),
    'duration':     np.random.exponential(15, n).clip(0.05, 300),
})

# Derive the features built in exercises 2 and 3
raw_df['bytes_per_second'] = np.where(raw_df['duration'] > 0,
                                       raw_df['bytes_sent'] / raw_df['duration'], 0)
raw_df['packet_rate']      = np.where(raw_df['duration'] > 0,
                                       raw_df['packets'] / raw_df['duration'], 0)
raw_df['bytes_ratio']      = raw_df['bytes_sent'] / (raw_df['bytes_recv'] + 1)

# Port risk score
port_risk_map = {80: 1, 443: 1, 53: 2, 22: 3, 21: 4, 3389: 5}
raw_df['port_risk_score'] = raw_df['dst_port'].apply(
    lambda p: port_risk_map.get(p, 3 if p < 1024 else 1)
)

# One-hot encode protocol (drop first to avoid dummy variable trap)
proto_dummies = pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)

# Simple binary label
raw_df['label'] = ((raw_df['bytes_sent'] > raw_df['bytes_sent'].quantile(0.85)) &
                   (raw_df['duration'] < raw_df['duration'].quantile(0.30))).astype(int)

# ============================================================
# TASK 1 — Assemble the full feature matrix
# ============================================================
# Combine all derived features into one DataFrame X.
# Validate: correct shape, all numeric, no NaN.
print("=" * 60)
print("TASK 1 — Assemble the full feature matrix")
print("=" * 60)

feature_cols = ['bytes_sent', 'bytes_recv', 'packets', 'duration',
                'bytes_per_second', 'packet_rate', 'bytes_ratio',
                'port_risk_score']

X = pd.concat([raw_df[feature_cols], proto_dummies], axis=1)
y = raw_df['label']

print(f"Shape: {X.shape}")
print(f"All dtypes:\n{X.dtypes}")
print(f"\nMissing values: {X.isnull().sum().sum()}")
print(f"\nDescriptive statistics:")
print(X.describe().round(2).to_string())

# ============================================================
# TASK 2 — Scale with StandardScaler
# ============================================================
# Critical rule: fit the scaler on training data ONLY, then transform both.
# If you fit on test data too, the test set's distribution leaks into the
# scaling parameters, giving optimistic performance estimates.
print("\n" + "=" * 60)
print("TASK 2 — Scale with StandardScaler (fit on train only)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # learns mean and std from TRAIN
X_test_scaled  = scaler.transform(X_test)          # applies SAME mean/std to TEST

# Verify: training set should have mean~0 and std~1 after scaling
train_means = X_train_scaled.mean(axis=0)
train_stds  = X_train_scaled.std(axis=0)

print("Column means after scaling (should all be ~0.00):")
for col, m in zip(X.columns, train_means):
    print(f"  {col:<20} {m:+.4f}")

print("\nColumn stds after scaling (should all be ~1.00):")
for col, s in zip(X.columns, train_stds):
    print(f"  {col:<20} {s:.4f}")

# ============================================================
# TASK 3 — Compare StandardScaler vs MinMaxScaler
# ============================================================
# StandardScaler uses (x - mean) / std — robust to outliers.
# MinMaxScaler uses (x - min) / (max - min) — one extreme value
# compresses all others toward 0.
print("\n" + "=" * 60)
print("TASK 3 — StandardScaler vs MinMaxScaler on bytes_per_second")
print("=" * 60)

bps_col = X_train[['bytes_per_second']].values

# StandardScaler
ss = StandardScaler()
bps_standard = ss.fit_transform(bps_col)
print(f"StandardScaler: mean={bps_standard.mean():.3f}, std={bps_standard.std():.3f}, "
      f"range=[{bps_standard.min():.2f}, {bps_standard.max():.2f}]")
print("  -> Outliers extend the range but most data stays near 0")

# MinMaxScaler
mm = MinMaxScaler()
bps_minmax = mm.fit_transform(bps_col)
print(f"\nMinMaxScaler:   mean={bps_minmax.mean():.3f}, "
      f"range=[{bps_minmax.min():.2f}, {bps_minmax.max():.2f}]")
print("  -> One extreme value at max=1.0 compresses all normal values toward 0")

print(f"\nMedian with StandardScaler: {np.median(bps_standard):.3f}")
print(f"Median with MinMaxScaler:   {np.median(bps_minmax):.3f}")
print("\nFor network data with extreme outliers (exfil spikes), StandardScaler")
print("is the safer choice — MinMaxScaler squashes most data to near zero.")

# ============================================================
# TASK 4 (BONUS) — Full Pipeline
# ============================================================
# sklearn Pipeline chains scaler + model so fit/transform rules
# are enforced automatically. The scaler fits ONLY on training data
# inside the pipeline — no risk of accidental leakage.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Full Pipeline")
print("=" * 60)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LogisticRegression(max_iter=500, random_state=42)),
])

# fit calls scaler.fit_transform on X_train, then model.fit
pipeline.fit(X_train, y_train)

# score calls scaler.transform on X_test (NOT fit_transform), then model.predict
train_acc = pipeline.score(X_train, y_train)
test_acc  = pipeline.score(X_test, y_test)

print(f"Pipeline training accuracy: {train_acc:.3f}")
print(f"Pipeline test accuracy:     {test_acc:.3f}")
print(f"\nThe pipeline automatically applies fit_transform to train and")
print(f"transform-only to test — no manual scaler management needed.")

print("\n--- Exercise 4 complete. Lesson 1 done! ---")
