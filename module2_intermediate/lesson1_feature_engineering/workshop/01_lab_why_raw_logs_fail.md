# Lab — Exercise 1: Why Raw Logs Fail

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_why_raw_logs_fail.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
```

---

## Step 3: Generate the raw log DataFrame

Add this block. It builds a synthetic firewall log with string columns, mixed types, and a duration suffix — exactly the kind of data that breaks sklearn.

```python
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
```

---

## Step 4: Task 1 — Display the raw log

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Raw log inspection")
print("=" * 60)

print("First 5 rows:")
print(raw_df.head().to_string())
print("\nColumn dtypes:")
print(raw_df.dtypes)

# Usable directly: src_port, dst_port, bytes_sent, packets
# Need transformation: timestamp, src_ip, dst_ip, protocol, duration_str, action
```

Run your file. You should see:

```
TASK 1 — Raw log inspection
============================================================
First 5 rows:
             timestamp        src_ip  ...
Column dtypes:
timestamp     object
src_ip        object
dst_ip        object
src_port       int64
dst_port       int64
protocol      object
bytes_sent     int64
packets        int64
duration_str  object
action        object
```

---

## Step 5: Task 2 — Try to fit a model on raw data

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Attempting to fit on raw data (expect an error)")
print("=" * 60)

X_raw = raw_df[['bytes_sent', 'packets', 'protocol', 'src_port']]
y_raw = (raw_df['action'] == 'BLOCK').astype(int)
try:
    model = LogisticRegression()
    model.fit(X_raw, y_raw)
    print("Model fitted successfully (unexpected!)")
except Exception as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nConclusion: 'protocol' column contains strings — cannot fit model.")
```

Run your file. You should see:

```
TASK 2 — Attempting to fit on raw data (expect an error)
============================================================
Error type: ValueError
Error message: could not convert string to float: 'TCP'

Conclusion: 'protocol' column contains strings — cannot fit model.
```

---

## Step 6: Task 3 — Build a transformation plan

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Feature transformation plan")
print("=" * 60)

transformation_plan = {
    'timestamp':    'extract hour_of_day and day_of_week',
    'src_ip':       'extract: is_private_ip (boolean), /24 subnet',
    'dst_ip':       'extract: is_private_ip (boolean)',
    'src_port':     'use directly (numeric)',
    'dst_port':     'use directly OR create port_risk_score',
    'protocol':     'one-hot encode (TCP/UDP/ICMP → 3 binary columns)',
    'bytes_sent':   'use directly (numeric)',
    'packets':      'use directly (numeric)',
    'duration_str': 'strip "s" suffix and parse as float',
    'action':       'convert to target label (BLOCK=1, ALLOW=0) — not a feature',
}
print(f"{'Column':15s}: {'Transformation'}")
print("-" * 60)
for col, plan in transformation_plan.items():
    print(f"{col:15s}: {plan}")
```

Run your file. You should see:

```
TASK 3 — Feature transformation plan
============================================================
Column         : Transformation
------------------------------------------------------------
timestamp      : extract hour_of_day and day_of_week
src_ip         : extract: is_private_ip (boolean), /24 subnet
...
action         : convert to target label (BLOCK=1, ALLOW=0) — not a feature
```

---

## Step 7: Task 4 (BONUS) — Private IP detection

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Private IP detection")
print("=" * 60)

def is_private_ip(ip_str):
    parts = ip_str.split('.')
    if parts[0] == '10':
        return True
    if parts[0] == '192' and parts[1] == '168':
        return True
    if parts[0] == '172' and 16 <= int(parts[1]) <= 31:
        return True
    return False

raw_df['src_is_private'] = raw_df['src_ip'].apply(is_private_ip)
counts = raw_df['src_is_private'].value_counts()
print(f"Private source IPs:  {counts.get(True, 0):3d} ({counts.get(True,0)/n*100:.0f}%)")
print(f"Public source IPs:   {counts.get(False, 0):3d} ({counts.get(False,0)/n*100:.0f}%)")

print("\n--- Exercise 1 complete. Move to 02_numeric_feature_extraction.py ---")
```

Run your file. You should see:

```
TASK 4 (BONUS) — Private IP detection
============================================================
Private source IPs:  ~140 (70%)
Public source IPs:    ~60 (30%)
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`01_solution_why_raw_logs_fail.py`) if anything looks different.
