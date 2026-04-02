# Exercise 2 — Numeric Feature Extraction
#
# Goal: Derive meaningful numeric features from raw log fields.
#       bytes_per_second, packet_rate, bytes_ratio, port_risk_score,
#       and timestamp-based features.

import numpy as np
import pandas as pd

np.random.seed(42)

# ── Rebuild the raw log (self-contained) ──────────────────────────────────────
n = 200

raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='2min'),
    'src_ip':       [f"192.168.{np.random.randint(0,10)}.{np.random.randint(1,255)}"
                     for _ in range(n)],
    'dst_ip':       [f"{np.random.randint(1,223)}.{np.random.randint(0,255)}."
                     f"{np.random.randint(0,255)}.{np.random.randint(1,255)}"
                     for _ in range(n)],
    'src_port':     np.random.randint(49152, 65535, n),
    'dst_port':     np.random.choice([80, 443, 22, 53, 3389, 21, 8080], n,
                                     p=[0.30, 0.30, 0.10, 0.10, 0.05, 0.05, 0.10]),
    'protocol':     np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.7, 0.25, 0.05]),
    'bytes_sent':   np.random.lognormal(7, 1.2, n).astype(int).clip(100, 100000),
    'bytes_recv':   np.random.lognormal(8, 1.5, n).astype(int).clip(100, 500000),
    'packets':      np.random.poisson(40, n).clip(1, 200),
    'duration_str': [f"{d:.2f}s" for d in np.random.exponential(15, n).clip(0.05, 300)],
    'action':       np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.85, 0.15]),
})

# ============================================================
# TASK 1 — Parse duration and compute bytes_per_second
# ============================================================
# duration_str has a "s" suffix (e.g. "2.34s") that must be stripped
# before converting to float. Then derive bytes_per_second.
print("=" * 60)
print("TASK 1 — Parse duration and compute bytes_per_second")
print("=" * 60)

# Strip the "s" suffix and convert to float
raw_df['duration'] = raw_df['duration_str'].str.rstrip('s').astype(float)

# Derive bytes_per_second; use np.where to avoid division-by-zero
raw_df['bytes_per_second'] = np.where(
    raw_df['duration'] > 0,
    raw_df['bytes_sent'] / raw_df['duration'],
    0
)

print("Sample of duration (raw -> parsed):")
for _, row in raw_df[['duration_str', 'duration']].head(3).iterrows():
    print(f"  raw: '{row['duration_str']}'  ->  float: {row['duration']}")

print(f"\nbytes_per_second stats:")
bps = raw_df['bytes_per_second']
print(f"  mean:  {bps.mean():.1f}")
print(f"  max:   {bps.max():.1f}")
print(f"  min:   {bps.min():.1f}")

# ============================================================
# TASK 2 — Derive packet_rate and bytes_ratio
# ============================================================
# packet_rate = packets / duration  (packets per second)
# bytes_ratio = bytes_sent / (bytes_recv + 1)  (upload-to-download ratio)
# Add 1 to denominator to avoid division by zero.
print("\n" + "=" * 60)
print("TASK 2 — Derive packet_rate and bytes_ratio")
print("=" * 60)

raw_df['packet_rate'] = np.where(
    raw_df['duration'] > 0,
    raw_df['packets'] / raw_df['duration'],
    0
)
raw_df['bytes_ratio'] = raw_df['bytes_sent'] / (raw_df['bytes_recv'] + 1)

print("packet_rate stats:")
pr = raw_df['packet_rate']
print(f"  mean: {pr.mean():.2f} packets/sec")
print(f"  max:  {pr.max():.2f}  <- suspicious if very high (SYN flood indicator)")
print(f"  min:  {pr.min():.2f}")

print("\nbytes_ratio stats (sent / received):")
br = raw_df['bytes_ratio']
print(f"  mean: {br.mean():.2f}")
print(f"  max:  {br.max():.2f}  <- sent much more than received (potential upload/exfil)")
print(f"  min:  {br.min():.4f}")

# ============================================================
# TASK 3 — Create port_risk_score
# ============================================================
# Map each destination port to a risk score based on security knowledge.
# This embeds domain expertise: the model doesn't need to learn from
# scratch that port 3389 (RDP) is riskier than port 443 (HTTPS).
print("\n" + "=" * 60)
print("TASK 3 — Create port_risk_score")
print("=" * 60)

port_risk_map = {
    80: 1,      # HTTP — standard
    443: 1,     # HTTPS — standard
    53: 2,      # DNS — watch for DNS tunnelling
    22: 3,      # SSH — legitimate but targeted
    21: 4,      # FTP — credentials sent in clear text
    3389: 5,    # RDP — frequently exploited
}

def port_to_risk(port):
    """Map a port number to a security risk score."""
    if port in port_risk_map:
        return port_risk_map[port]
    elif port < 1024:
        return 3   # other well-known ports — potentially dangerous
    else:
        return 1   # ephemeral ports — typically benign

raw_df['port_risk_score'] = raw_df['dst_port'].apply(port_to_risk)

print("Port risk score distribution:")
risk_counts = raw_df['port_risk_score'].value_counts().sort_index()
risk_labels = {1: 'standard HTTP/HTTPS/ephemeral', 2: 'DNS', 3: 'SSH/well-known',
               4: 'FTP', 5: 'RDP'}
for score, count in risk_counts.items():
    label = risk_labels.get(score, 'other')
    print(f"  port_risk_score={score} ({label}): {count} connections")

# ============================================================
# TASK 4 (BONUS) — Extract timestamp features
# ============================================================
# Timestamps carry time-of-day and day-of-week patterns.
# Attacks often happen at night or on weekends when fewer analysts watch.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Extract timestamp features")
print("=" * 60)

raw_df['hour_of_day']       = raw_df['timestamp'].dt.hour
raw_df['day_of_week']       = raw_df['timestamp'].dt.dayofweek   # 0=Mon, 6=Sun
raw_df['is_business_hours'] = (
    (raw_df['hour_of_day'] >= 9) &
    (raw_df['hour_of_day'] <= 17) &
    (raw_df['day_of_week'] < 5)    # Monday-Friday
).astype(int)

# Compare bytes_per_second during business hours vs off-hours
biz = raw_df[raw_df['is_business_hours'] == 1]['bytes_per_second']
off = raw_df[raw_df['is_business_hours'] == 0]['bytes_per_second']

print(f"Business hours connections: {len(biz)}")
print(f"Off-hours connections:      {len(off)}")
print(f"\nMean bytes_per_second:")
print(f"  Business hours: {biz.mean():.1f}")
print(f"  Off-hours:      {off.mean():.1f}")
print(f"\nSample of timestamp features:")
print(raw_df[['timestamp', 'hour_of_day', 'day_of_week', 'is_business_hours']].head(5).to_string())

print("\n--- Exercise 2 complete. Move to ../3_categorical_encoding/solve.py ---")
