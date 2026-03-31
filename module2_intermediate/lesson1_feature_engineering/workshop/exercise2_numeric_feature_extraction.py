# =============================================================================
# LESSON 2.1 | WORKSHOP | Exercise 2 of 4
# Numeric Feature Extraction
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to parse string fields (duration "2.3s") into usable numbers
# - How to derive bytes_per_second, packet_rate, bytes_ratio from raw fields
# - How to create a port_risk_score using domain knowledge
# - How to validate derived features make intuitive sense
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson1_feature_engineering/workshop/exercise2_numeric_feature_extraction.py
# =============================================================================

import numpy as np
import pandas as pd

# =============================================================================
# BACKGROUND
# =============================================================================
# Raw numeric fields like bytes_sent and duration have value, but their
# *combinations* often carry more signal. bytes_per_second normalises volume
# by time — a 10MB transfer over 1 second is very different from the same
# volume over 10 hours. Similarly, port risk scores embed security expertise
# directly into the feature space, freeing the model from having to learn
# port semantics from scratch.

# --- Raw log (do not modify) ------------------------------------------------
np.random.seed(42)
n = 200
np.random.seed(42)
protocols  = np.random.choice(['TCP', 'UDP', 'ICMP'], n, p=[0.6, 0.3, 0.1])
actions    = np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.8, 0.2])
src_ips    = [f"192.168.{np.random.randint(0,5)}.{np.random.randint(1,254)}"
              if np.random.rand() < 0.7 else
              f"{np.random.randint(1,223)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,254)}"
              for _ in range(n)]
dst_ips    = [f"{np.random.randint(1,223)}.{np.random.randint(0,255)}.0.{np.random.randint(1,254)}"
              for _ in range(n)]
durations  = [f"{round(np.random.exponential(2), 2)}s" for _ in range(n)]

raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='45min').astype(str),
    'src_ip':       src_ips,
    'dst_ip':       dst_ips,
    'src_port':     np.random.randint(1024, 65535, n),
    'dst_port':     np.random.choice([80, 443, 22, 3389, 8080, 53], n,
                                      p=[0.3, 0.3, 0.1, 0.08, 0.12, 0.1]),
    'protocol':     protocols,
    'bytes_sent':   np.random.exponential(5000, n).astype(int),
    'bytes_received': np.random.exponential(8000, n).astype(int),
    'packets':      np.random.poisson(15, n),
    'duration_str': durations,
    'action':       actions
})
# We'll build a features DataFrame as we go
feat_df = pd.DataFrame()
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Parse Duration and Compute bytes_per_second
# =============================================================================
# 1. Strip the "s" suffix from raw_df['duration_str'] and convert to float.
#    Store as feat_df['duration'].
# 2. Compute feat_df['bytes_per_second'] = bytes_sent / duration.
#    Handle zero durations by setting the result to 0.
# 3. Print 5 sample rows (raw duration_str, parsed duration, bytes_per_second).
# 4. Print .describe() of bytes_per_second.

print("=" * 60)
print("TASK 1 — Parse duration, compute bytes_per_second")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   feat_df['duration'] = raw_df['duration_str'].str.replace('s', '').astype(float)
#   feat_df['bytes_per_second'] = np.where(
#       feat_df['duration'] > 0,
#       raw_df['bytes_sent'] / feat_df['duration'],
#       0
#   )
#   sample = raw_df[['duration_str', 'bytes_sent']].copy()
#   sample['duration_parsed'] = feat_df['duration']
#   sample['bytes_per_second'] = feat_df['bytes_per_second']
#   print(sample.head().to_string(index=False))
#   print("\nbytes_per_second stats:")
#   print(feat_df['bytes_per_second'].describe().round(1))

# EXPECTED OUTPUT:
# duration_str  bytes_sent  duration_parsed  bytes_per_second
#     2.34s        8700         2.34            3718.0
# ...
# mean: ~3500

# =============================================================================
# TASK 2 — Derive packet_rate and bytes_ratio
# =============================================================================
# Compute:
#   feat_df['packet_rate']  = packets / duration  (handle zero duration → 0)
#   feat_df['bytes_ratio']  = bytes_sent / (bytes_received + 1)
# Print .describe() for both.
# Comment on what unusually high packet_rate or bytes_ratio might indicate.

print("\n" + "=" * 60)
print("TASK 2 — packet_rate and bytes_ratio")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   feat_df['packet_rate'] = np.where(
#       feat_df['duration'] > 0,
#       raw_df['packets'] / feat_df['duration'],
#       0
#   )
#   feat_df['bytes_ratio'] = raw_df['bytes_sent'] / (raw_df['bytes_received'] + 1)
#   print("packet_rate stats:")
#   print(feat_df['packet_rate'].describe().round(2))
#   print("\nbytes_ratio stats (sent/received):")
#   print(feat_df['bytes_ratio'].describe().round(2))

# EXPECTED OUTPUT:
# packet_rate — high values (>50) may indicate SYN flood
# bytes_ratio — high values (>10) may indicate data exfiltration

# =============================================================================
# TASK 3 — Create port_risk_score
# =============================================================================
# Map raw_df['dst_port'] to a risk score using this table:
#   {80: 1, 443: 1, 53: 2, 22: 3, 8080: 2, 3389: 5, default: 2}
# Store as feat_df['port_risk_score'].
# Print the value_counts() of port_risk_score.

print("\n" + "=" * 60)
print("TASK 3 — Port risk score")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   port_risk_map = {80: 1, 443: 1, 53: 2, 22: 3, 8080: 2, 3389: 5}
#   feat_df['port_risk_score'] = raw_df['dst_port'].map(port_risk_map).fillna(2).astype(int)
#   print("port_risk_score distribution:")
#   for score, count in feat_df['port_risk_score'].value_counts().sort_index().items():
#       print(f"  Risk={score}: {count:3d} connections")

# EXPECTED OUTPUT:
# Risk=1: ~120 connections  (HTTP/HTTPS — normal)
# Risk=2: ~50 connections   (DNS/8080/unknown)
# Risk=3: ~20 connections   (SSH)
# Risk=5: ~16 connections   (RDP — risky!)

# =============================================================================
# TASK 4 (BONUS) — Extract Timestamp Features
# =============================================================================
# Parse raw_df['timestamp'] to datetime. Extract:
#   feat_df['hour_of_day']   = hour (0-23)
#   feat_df['day_of_week']   = day (0=Mon, 6=Sun)
#   feat_df['is_biz_hours']  = 1 if hour in 9-17 and day in 0-4, else 0
# Print the mean bytes_per_second for business hours vs off-hours.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Timestamp features")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   dt = pd.to_datetime(raw_df['timestamp'])
#   feat_df['hour_of_day']  = dt.dt.hour
#   feat_df['day_of_week']  = dt.dt.dayofweek
#   feat_df['is_biz_hours'] = ((feat_df['hour_of_day'].between(9, 17)) &
#                               (feat_df['day_of_week'] <= 4)).astype(int)
#   biz     = feat_df[feat_df['is_biz_hours']==1]['bytes_per_second'].mean()
#   off_hrs = feat_df[feat_df['is_biz_hours']==0]['bytes_per_second'].mean()
#   print(f"Mean bytes/sec during business hours: {biz:.0f}")
#   print(f"Mean bytes/sec off hours:             {off_hrs:.0f}")
#   print(f"(Higher off-hours activity may indicate malicious behaviour)")

print("\n--- Exercise 2 complete. Move to exercise3_categorical_encoding.py ---")
