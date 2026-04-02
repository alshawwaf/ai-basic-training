# Lab — Exercise 2: Numeric Feature Extraction

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_numeric_feature_extraction.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
```

---

## Step 3: Generate the raw log and create feat_df

Add this data-generation block. Do not modify it — all tasks build on top of it.

```python
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
    'timestamp':      pd.date_range('2024-01-15 08:00', periods=n, freq='45min').astype(str),
    'src_ip':         src_ips,
    'dst_ip':         dst_ips,
    'src_port':       np.random.randint(1024, 65535, n),
    'dst_port':       np.random.choice([80, 443, 22, 3389, 8080, 53], n,
                                        p=[0.3, 0.3, 0.1, 0.08, 0.12, 0.1]),
    'protocol':       protocols,
    'bytes_sent':     np.random.exponential(5000, n).astype(int),
    'bytes_received': np.random.exponential(8000, n).astype(int),
    'packets':        np.random.poisson(15, n),
    'duration_str':   durations,
    'action':         actions
})
feat_df = pd.DataFrame()
```

---

## Step 4: Task 1 — Parse duration and compute bytes_per_second

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Parse duration, compute bytes_per_second")
print("=" * 60)

feat_df['duration'] = raw_df['duration_str'].str.replace('s', '').astype(float)
feat_df['bytes_per_second'] = np.where(
    feat_df['duration'] > 0,
    raw_df['bytes_sent'] / feat_df['duration'],
    0
)
sample = raw_df[['duration_str', 'bytes_sent']].copy()
sample['duration_parsed'] = feat_df['duration']
sample['bytes_per_second'] = feat_df['bytes_per_second']
print(sample.head().to_string(index=False))
print("\nbytes_per_second stats:")
print(feat_df['bytes_per_second'].describe().round(1))
```

Run your file. You should see:

```
TASK 1 — Parse duration, compute bytes_per_second
============================================================
duration_str  bytes_sent  duration_parsed  bytes_per_second
       2.34s        8700             2.34            3718.0
...
bytes_per_second stats:
mean: ~3500
```

---

## Step 5: Task 2 — Derive packet_rate and bytes_ratio

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — packet_rate and bytes_ratio")
print("=" * 60)

feat_df['packet_rate'] = np.where(
    feat_df['duration'] > 0,
    raw_df['packets'] / feat_df['duration'],
    0
)
feat_df['bytes_ratio'] = raw_df['bytes_sent'] / (raw_df['bytes_received'] + 1)
print("packet_rate stats:")
print(feat_df['packet_rate'].describe().round(2))
print("\nbytes_ratio stats (sent/received):")
print(feat_df['bytes_ratio'].describe().round(2))
# packet_rate — high values (>50) may indicate SYN flood
# bytes_ratio — high values (>10) may indicate data exfiltration
```

Run your file. You should see:

```
TASK 2 — packet_rate and bytes_ratio
============================================================
packet_rate stats:
mean    ~8.2
max    ~180.0
...
bytes_ratio stats (sent/received):
mean    ~0.85
max     ~32.1
```

---

## Step 6: Task 3 — Create port_risk_score

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Port risk score")
print("=" * 60)

port_risk_map = {80: 1, 443: 1, 53: 2, 22: 3, 8080: 2, 3389: 5}
feat_df['port_risk_score'] = raw_df['dst_port'].map(port_risk_map).fillna(2).astype(int)
print("port_risk_score distribution:")
for score, count in feat_df['port_risk_score'].value_counts().sort_index().items():
    print(f"  Risk={score}: {count:3d} connections")
```

Run your file. You should see:

```
TASK 3 — Port risk score
============================================================
port_risk_score distribution:
  Risk=1: ~120 connections  (HTTP/HTTPS — normal)
  Risk=2:  ~50 connections  (DNS/8080/unknown)
  Risk=3:  ~20 connections  (SSH)
  Risk=5:  ~16 connections  (RDP — risky!)
```

---

## Step 7: Task 4 (BONUS) — Extract timestamp features

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Timestamp features")
print("=" * 60)

dt = pd.to_datetime(raw_df['timestamp'])
feat_df['hour_of_day']  = dt.dt.hour
feat_df['day_of_week']  = dt.dt.dayofweek
feat_df['is_biz_hours'] = ((feat_df['hour_of_day'].between(9, 17)) &
                            (feat_df['day_of_week'] <= 4)).astype(int)
biz     = feat_df[feat_df['is_biz_hours']==1]['bytes_per_second'].mean()
off_hrs = feat_df[feat_df['is_biz_hours']==0]['bytes_per_second'].mean()
print(f"Mean bytes/sec during business hours: {biz:.0f}")
print(f"Mean bytes/sec off hours:             {off_hrs:.0f}")
print(f"(Higher off-hours activity may indicate malicious behaviour)")

print("\n--- Exercise 2 complete. Move to 03_categorical_encoding.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_numeric_feature_extraction.py`) if anything looks different.
