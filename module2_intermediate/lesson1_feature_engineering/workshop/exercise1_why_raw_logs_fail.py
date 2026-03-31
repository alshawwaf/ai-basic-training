# =============================================================================
# LESSON 2.1 | WORKSHOP | Exercise 1 of 4
# Why Raw Logs Fail
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - What raw firewall/NetFlow logs look like as a DataFrame
# - Why string and mixed-type columns break sklearn
# - How to identify which columns need transformation
# - The feature engineering mindset: translate raw data into ML-usable numbers
#
# RUN THIS FILE
# -------------
#   python module2_intermediate/lesson1_feature_engineering/workshop/exercise1_why_raw_logs_fail.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# =============================================================================
# BACKGROUND
# =============================================================================
# sklearn estimators require a 2D array of numbers. Raw network logs contain
# IP addresses (strings), protocols (categorical), timestamps (strings),
# and durations with unit suffixes ("2.3s"). Trying to feed these directly
# to a model raises ValueError. Feature engineering is the process of
# translating these raw fields into numbers that capture security-relevant signals.

# --- Raw log generation (do not modify) -------------------------------------
np.random.seed(42)
n = 200
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
    'timestamp':    pd.date_range('2024-01-15 08:00', periods=n, freq='1min').astype(str),
    'src_ip':       src_ips,
    'dst_ip':       dst_ips,
    'src_port':     np.random.randint(1024, 65535, n),
    'dst_port':     np.random.choice([80, 443, 22, 3389, 8080, 53], n),
    'protocol':     protocols,
    'bytes_sent':   np.random.exponential(5000, n).astype(int),
    'packets':      np.random.poisson(15, n),
    'duration_str': durations,
    'action':       actions
})
# ----------------------------------------------------------------------------

# =============================================================================
# TASK 1 — Display the Raw Log
# =============================================================================
# Print the first 5 rows and the dtypes of the raw_df DataFrame.
# After reviewing dtypes, add a comment listing which columns are directly
# usable as numbers and which need transformation.

print("=" * 60)
print("TASK 1 — Raw log inspection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   print("First 5 rows:")
#   print(raw_df.head().to_string())
#   print("\nColumn dtypes:")
#   print(raw_df.dtypes)

# EXPECTED OUTPUT:
# First 5 rows:
#              timestamp        src_ip  dst_ip  ...
#
# Column dtypes:
# timestamp     object
# src_ip        object
# dst_ip        object
# src_port       int64
# dst_port       int64
# protocol      object
# bytes_sent     int64
# packets        int64
# duration_str  object
# action        object

# Usable directly: src_port, dst_port, bytes_sent, packets
# Need transformation: timestamp, src_ip, dst_ip, protocol, duration_str, action

# =============================================================================
# TASK 2 — Try to Fit a Model on Raw Data (Intentional Failure)
# =============================================================================
# Select columns: ['bytes_sent', 'packets', 'protocol', 'src_port']
# Create a target: label = (raw_df['action'] == 'BLOCK').astype(int)
# Attempt to fit a LogisticRegression.
# Catch the error with try/except, print the error message.

print("\n" + "=" * 60)
print("TASK 2 — Attempting to fit on raw data (expect an error)")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   X_raw = raw_df[['bytes_sent', 'packets', 'protocol', 'src_port']]
#   y_raw = (raw_df['action'] == 'BLOCK').astype(int)
#   try:
#       model = LogisticRegression()
#       model.fit(X_raw, y_raw)
#       print("Model fitted successfully (unexpected!)")
#   except Exception as e:
#       print(f"Error type: {type(e).__name__}")
#       print(f"Error message: {e}")
#       print("\nConclusion: 'protocol' column contains strings — cannot fit model.")

# EXPECTED OUTPUT:
# Error type: ValueError
# Error message: could not convert string to float: 'TCP'
# Conclusion: 'protocol' column contains strings — cannot fit model.

# =============================================================================
# TASK 3 — Build a Transformation Plan
# =============================================================================
# For each column in raw_df, decide what transformation is needed.
# Create a Python dict: {column_name: 'transformation description'}.
# Print it in a readable format.

print("\n" + "=" * 60)
print("TASK 3 — Feature transformation plan")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   transformation_plan = {
#       'timestamp':    'extract hour_of_day and day_of_week',
#       'src_ip':       'extract: is_private_ip (boolean), /24 subnet',
#       'dst_ip':       'extract: is_private_ip (boolean)',
#       'src_port':     'use directly (numeric)',
#       'dst_port':     'use directly OR create port_risk_score',
#       'protocol':     'one-hot encode (TCP/UDP/ICMP → 3 binary columns)',
#       'bytes_sent':   'use directly (numeric)',
#       'packets':      'use directly (numeric)',
#       'duration_str': 'strip "s" suffix and parse as float',
#       'action':       'convert to target label (BLOCK=1, ALLOW=0) — not a feature',
#   }
#   print(f"{'Column':15s}: {'Transformation'}")
#   print("-" * 60)
#   for col, plan in transformation_plan.items():
#       print(f"{col:15s}: {plan}")

# EXPECTED OUTPUT:
# Column          : Transformation
# timestamp       : extract hour_of_day and day_of_week
# src_ip          : extract: is_private_ip, /24 subnet
# ...

# =============================================================================
# TASK 4 (BONUS) — IP Private Address Detection
# =============================================================================
# Write a function is_private_ip(ip_str) that returns True if the IP is in
# RFC1918 private ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x.
# Apply it to raw_df['src_ip'] to create a new column 'src_is_private'.
# Print the proportion of private vs public source IPs.

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Private IP detection")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   def is_private_ip(ip_str):
#       parts = ip_str.split('.')
#       if parts[0] == '10':
#           return True
#       if parts[0] == '192' and parts[1] == '168':
#           return True
#       if parts[0] == '172' and 16 <= int(parts[1]) <= 31:
#           return True
#       return False
#
#   raw_df['src_is_private'] = raw_df['src_ip'].apply(is_private_ip)
#   counts = raw_df['src_is_private'].value_counts()
#   print(f"Private source IPs:  {counts.get(True, 0):3d} ({counts.get(True,0)/n*100:.0f}%)")
#   print(f"Public source IPs:   {counts.get(False, 0):3d} ({counts.get(False,0)/n*100:.0f}%)")

# EXPECTED OUTPUT:
# Private source IPs:  ~140 (70%)
# Public source IPs:    ~60 (30%)

print("\n--- Exercise 1 complete. Move to exercise2_numeric_feature_extraction.py ---")
