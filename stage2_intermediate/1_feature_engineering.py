# Lesson 2.1 — Feature Engineering
#
# Goal: Transform raw network log data into ML-ready features.
# We simulate raw firewall/NetFlow-style log entries and extract
# meaningful numerical features from them.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

np.random.seed(42)

# ── 1. Simulate raw log data ───────────────────────────────────────────────────
n_benign = 3000
n_attack = 300   # ~9% attack — imbalanced, realistic

def random_ip(private=True):
    if private:
        return f"192.168.{np.random.randint(0,255)}.{np.random.randint(1,255)}"
    return f"{np.random.randint(1,223)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,255)}"

protocols = ['TCP', 'UDP', 'ICMP']

timestamps_benign = pd.date_range('2024-01-01 08:00', periods=n_benign, freq='5min') \
    + pd.to_timedelta(np.random.randint(-120, 120, n_benign), unit='m')
timestamps_attack = pd.date_range('2024-01-01', periods=n_attack, freq='2h') \
    + pd.to_timedelta(np.random.choice([2, 3, 4], n_attack), unit='h')  # early morning

raw_logs = pd.concat([
    pd.DataFrame({
        'timestamp':       timestamps_benign,
        'src_ip':          [random_ip(True)  for _ in range(n_benign)],
        'dest_ip':         [random_ip(False) for _ in range(n_benign)],
        'dest_port':       np.random.choice([80, 443, 22, 53, 8080], n_benign,
                                             p=[0.4, 0.4, 0.05, 0.1, 0.05]),
        'protocol':        np.random.choice(protocols, n_benign, p=[0.7, 0.25, 0.05]),
        'bytes_sent':      np.random.lognormal(7, 1.2, n_benign).astype(int).clip(100, 100000),
        'bytes_received':  np.random.lognormal(8, 1.5, n_benign).astype(int).clip(100, 500000),
        'duration_s':      np.random.exponential(15, n_benign).clip(0.1, 300),
        'label': 0
    }),
    pd.DataFrame({
        'timestamp':       timestamps_attack,
        'src_ip':          [random_ip(True)  for _ in range(n_attack)],
        'dest_ip':         [random_ip(False) for _ in range(n_attack)],
        'dest_port':       np.random.randint(1, 65535, n_attack),
        'protocol':        np.random.choice(protocols, n_attack, p=[0.5, 0.3, 0.2]),
        'bytes_sent':      np.random.lognormal(11, 1.5, n_attack).astype(int).clip(1000, 10000000),
        'bytes_received':  np.random.lognormal(5, 1, n_attack).astype(int).clip(50, 5000),
        'duration_s':      np.random.exponential(2, n_attack).clip(0.01, 30),
        'label': 1
    })
], ignore_index=True).sort_values('timestamp').reset_index(drop=True)

print("=== Raw Log Sample ===")
print(raw_logs.drop('label', axis=1).head(3).to_string())
print(f"\nTotal logs: {len(raw_logs)} | Attacks: {raw_logs['label'].sum()}")

# ── 2. Feature engineering ─────────────────────────────────────────────────────
print("\n=== Engineering Features ===")

df = raw_logs.copy()

# Time-based features
df['hour_of_day']    = df['timestamp'].dt.hour
df['day_of_week']    = df['timestamp'].dt.dayofweek
df['is_after_hours'] = ((df['hour_of_day'] < 7) | (df['hour_of_day'] > 21)).astype(int)
df['is_weekend']     = (df['day_of_week'] >= 5).astype(int)

# Ratio features
df['bytes_per_second']   = df['bytes_sent'] / (df['duration_s'] + 0.001)
df['upload_to_download'] = df['bytes_sent'] / (df['bytes_received'] + 1)
df['total_bytes']        = df['bytes_sent'] + df['bytes_received']

# Port category
df['is_well_known_port'] = (df['dest_port'] < 1024).astype(int)
df['is_ephemeral_port']  = (df['dest_port'] > 49151).astype(int)

# Protocol encoding
df['protocol_tcp']  = (df['protocol'] == 'TCP').astype(int)
df['protocol_udp']  = (df['protocol'] == 'UDP').astype(int)
df['protocol_icmp'] = (df['protocol'] == 'ICMP').astype(int)

feature_cols = [
    'hour_of_day', 'is_after_hours', 'is_weekend',
    'bytes_sent', 'bytes_received', 'total_bytes',
    'bytes_per_second', 'upload_to_download',
    'duration_s', 'is_well_known_port', 'is_ephemeral_port',
    'protocol_tcp', 'protocol_udp', 'protocol_icmp'
]

print(f"Engineered {len(feature_cols)} features from {len(raw_logs.columns)-1} raw columns")
print("\nFeature matrix sample:")
print(df[feature_cols].head(3).round(2).to_string())

# ── 3. Which features correlate with the label? ────────────────────────────────
corr = df[feature_cols + ['label']].corr()['label'].drop('label').sort_values(key=abs, ascending=False)
print("\n=== Feature Correlation with Attack Label ===")
print(corr.round(3).to_string())

# ── 4. Measure impact of feature engineering ──────────────────────────────────
X = df[feature_cols]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

raw_features = ['bytes_sent', 'bytes_received', 'duration_s']  # raw only
eng_features = feature_cols                                      # all engineered

results = {}
for name, feats in [('Raw features only', raw_features), ('All engineered features', eng_features)]:
    m = RandomForestClassifier(n_estimators=50, random_state=42)
    m.fit(X_train[feats], y_train)
    auc = roc_auc_score(y_test, m.predict_proba(X_test[feats])[:, 1])
    results[name] = auc
    print(f"\n{name}: ROC AUC = {auc:.4f}")

print(f"\nFeature engineering improvement: +{results['All engineered features'] - results['Raw features only']:.4f} AUC")

# ── 5. Plot ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Feature correlation bar chart
corr.head(10).plot(kind='barh', ax=axes[0], color=['crimson' if v > 0 else 'steelblue' for v in corr.head(10)])
axes[0].set_title('Top Feature Correlations with Attack Label')
axes[0].axvline(0, color='black', linewidth=0.8)
axes[0].set_xlabel('Correlation coefficient')

# Bytes per second distribution
for label, grp in df.groupby('label'):
    name = 'Attack' if label else 'Benign'
    axes[1].hist(np.log1p(grp['bytes_per_second']), bins=40, alpha=0.6, label=name)
axes[1].set_xlabel('log(bytes_per_second + 1)')
axes[1].set_title('Engineered Feature: bytes_per_second by Class')
axes[1].legend()

plt.tight_layout()
plt.savefig('stage2_intermediate/lesson1_feature_engineering.png')
plt.show()
print("\nPlot saved to stage2_intermediate/lesson1_feature_engineering.png")
