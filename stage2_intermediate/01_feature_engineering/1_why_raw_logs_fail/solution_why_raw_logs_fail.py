# Exercise 1 — Why Raw Logs Fail
#
# Goal: See why raw firewall/NetFlow logs cannot be fed directly to sklearn,
#       what errors you get, and why feature engineering is necessary.

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

np.random.seed(42)

# ============================================================
# TASK 1 — Generate and display the raw log
# ============================================================
# Simulate a small raw log with all the problem columns:
# strings (IPs, protocol), timestamps, and a duration with a unit suffix.
print("=" * 60)
print("TASK 1 — Generate and display the raw log")
print("=" * 60)

n = 200

# Build a raw log DataFrame that mimics a real firewall export
raw_df = pd.DataFrame({
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='2min').astype(str),
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
    # Duration stored as a string with "s" suffix — common in log exports
    'duration_str': [f"{d:.2f}s" for d in np.random.exponential(15, n).clip(0.05, 300)],
    'action':       np.random.choice(['ALLOW', 'BLOCK'], n, p=[0.85, 0.15]),
})

print("First 5 rows of the raw log:")
print(raw_df.head().to_string())
print(f"\nDtypes:\n{raw_df.dtypes}")
print("\nUsable as-is (numeric): src_port, dst_port, bytes_sent, bytes_recv, packets")
print("NOT usable (strings):  timestamp, src_ip, dst_ip, protocol, duration_str, action")

# ============================================================
# TASK 2 — Try to fit a model on raw data
# ============================================================
# sklearn requires all-numeric input. Passing string columns triggers an error.
print("\n" + "=" * 60)
print("TASK 2 — Try to fit a model on raw data")
print("=" * 60)

# Create a dummy binary label for demonstration
y = np.random.binomial(1, 0.1, n)

# Select columns including a string column (protocol) to trigger the error
raw_features = raw_df[['bytes_sent', 'bytes_recv', 'protocol', 'packets']]

try:
    model = LogisticRegression(max_iter=200)
    model.fit(raw_features, y)
    print("Model fit succeeded (unexpected!)")
except ValueError as e:
    print(f"ValueError: {e}")
    print("Column that caused failure: protocol (a string column)")

# ============================================================
# TASK 3 — Identify all non-numeric columns
# ============================================================
# Build a transformation plan: what needs to happen to each column
# before it can be used as an ML feature.
print("\n" + "=" * 60)
print("TASK 3 — Identify all non-numeric columns")
print("=" * 60)

# Classify each column by whether it is numeric or needs transformation
numeric_cols = raw_df.select_dtypes(include=[np.number]).columns.tolist()
non_numeric_cols = raw_df.select_dtypes(exclude=[np.number]).columns.tolist()

print(f"Numeric columns ({len(numeric_cols)}):     {numeric_cols}")
print(f"Non-numeric columns ({len(non_numeric_cols)}): {non_numeric_cols}")

# A transformation plan encodes domain knowledge about how to handle each column
transformation_plan = {
    'bytes_sent':    'use directly',
    'bytes_recv':    'use directly',
    'packets':       'use directly',
    'src_port':      'use directly (or drop — ephemeral ports have little signal)',
    'dst_port':      'map to port_risk_score (encode security knowledge)',
    'protocol':      'one-hot encode (TCP/UDP/ICMP)',
    'src_ip':        'extract: is_private, /24 subnet',
    'dst_ip':        'extract: is_private, known-bad list lookup',
    'timestamp':     'extract: hour_of_day, day_of_week, is_business_hours',
    'duration_str':  'parse float from string (strip "s" suffix)',
    'action':        'drop — this is the target variable, not a feature',
}

print("\nTransformation plan:")
for col, plan in transformation_plan.items():
    print(f"  {col:<15} → {plan}")

# ============================================================
# TASK 4 (BONUS) — IP address analysis
# ============================================================
# Write a function to classify IPs as private (RFC 1918) or public.
# Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — IP address analysis")
print("=" * 60)

def is_private_ip(ip_str):
    """Return True if IP is in an RFC 1918 private range."""
    if ip_str.startswith("10."):
        return True
    if ip_str.startswith("192.168."):
        return True
    if ip_str.startswith("172."):
        # Check 172.16.0.0 – 172.31.255.255
        second_octet = int(ip_str.split('.')[1])
        if 16 <= second_octet <= 31:
            return True
    return False

# Apply to src_ip to create a boolean feature
raw_df['src_is_private'] = raw_df['src_ip'].apply(is_private_ip)

print(f"Private source IPs: {raw_df['src_is_private'].sum()} / {len(raw_df)}")
print(f"Public source IPs:  {(~raw_df['src_is_private']).sum()} / {len(raw_df)}")
print("\nSample with new column:")
print(raw_df[['src_ip', 'src_is_private']].head(10).to_string())

print("\n--- Exercise 1 complete. Move to ../2_numeric_feature_extraction/solution.py ---")
