# Exercise 1 — Why Raw Logs Fail

> Back to [00_overview.md](00_overview.md)

## What You Will Learn

- What a raw firewall/NetFlow log looks like as a pandas DataFrame
- Why string columns (IP addresses, protocols, timestamps) cannot be fed to sklearn
- What error messages you get when you try
- Why feature engineering is the bridge between raw data and ML

---

## Concept: What Raw Logs Contain

A typical NetFlow or firewall log row looks like:

```
timestamp           src_ip          dst_ip          src_port  dst_port  protocol  bytes   packets  duration  action
2024-01-15 08:23:11 192.168.1.42    8.8.8.8         52341     443       TCP       14580   12       2.3s      ALLOW
2024-01-15 08:23:15 10.0.0.5        185.234.219.42  58921     80        HTTP      420     5        0.1s      BLOCK
```

| Problem | Why it breaks sklearn |
|---------|----------------------|
| `timestamp` is a string | No mathematical meaning; must be converted or dropped |
| `src_ip`, `dst_ip` are strings | High-cardinality text; models can't learn from "192.168.1.42" directly |
| `protocol` is categorical | "TCP", "UDP" are labels, not numbers |
| `duration` has unit suffix ("2.3s") | Can't parse "2.3s" as a float |
| IPs can have security meaning | RFC1918 vs public IP distinction must be engineered |

---

## Concept: The sklearn Contract

sklearn's estimators require the input `X` to be a 2D array-like of numbers with shape `(n_samples, n_features)`. Any column containing:
- strings
- mixed types
- NaN values (for some estimators)
- Python objects

will cause a `ValueError` like `could not convert string to float: 'TCP'`.

---

## Concept: Feature Engineering as Translation

Feature engineering is the process of translating raw data into a numerical representation that:
1. Contains the signal the model needs to distinguish classes
2. Is in a format sklearn can process
3. Is robust to variations (different port numbers, new IPs, etc.)

```
Raw log line (strings, mixed types — sklearn rejects this)
┌──────────────────────────────────────────────────────────────┐
│ "2024-01-15 08:23:11  192.168.1.42  TCP  443  14580  2.3s"   │
└──────────────────────────┬───────────────────────────────────┘
                           │  feature engineering
                           ▼
Numeric feature vector (sklearn accepts this)
┌──────────────────────────────────────────────────────────┐
│  [ 8,  1,  1,  3,  6339,  5.2,  1 ]                      │
│    │  │  │  │    │     │    └─ is_private (bool)         │
│    │  │  │  │    │     └─ packet_rate                    │
│    │  │  │  │    └─ bytes_per_second                     │
│    │  │  │  └─ port_risk_score                           │
│    │  │  └─ proto_TCP (one-hot)                          │
│    │  └─ is_business_hours (bool)                        │
│    └─ hour_of_day                                        │
└──────────────────────────────────────────────────────────┘
```

For network logs, this means computing *behavioural* features that capture what the connection is *doing*, not just its identifiers.

> **Want to go deeper?** [Feature engineering (Wikipedia)](https://en.wikipedia.org/wiki/Feature_engineering)

---

## What Each Task Asks You to Do

### Task 1 — Generate and Display the Raw Log
Create a synthetic raw log DataFrame with all the problem columns (strings, mixed types). Print its first 5 rows and `.dtypes`. Identify which columns are usable as-is.

### Task 2 — Try to Fit a Model on Raw Data
Attempt to fit a `LogisticRegression` on the raw DataFrame (select a few columns). Catch and print the error. Record which column caused it.

### Task 3 — Identify All Non-Numeric Columns
Print a summary of which columns are numeric, which are categorical, and which need transformation. Build a small "transformation plan" as a Python dict.

### Task 4 (BONUS) — IP Address Analysis
Write a function `is_private_ip(ip_str)` that returns True if the IP starts with 192.168, 10., or 172.16-31. Apply it to `src_ip` to create a `src_is_private` boolean column.

---

## Expected Outputs

```
TASK 1 — Raw log sample:
             timestamp        src_ip          dst_ip  src_port  ...
0  2024-01-15 08:23:11  192.168.1.42         8.8.8.8     52341  ...

Dtypes:
timestamp     object
src_ip        object
dst_ip        object
protocol      object
duration_str  object
bytes_sent     int64   ← usable as-is
action        object

TASK 2 — Attempted fit error:
ValueError: could not convert string to float: 'TCP'
(Column that caused failure: protocol)

TASK 3 — Transformation plan:
{
  'bytes_sent': 'use directly',
  'packets': 'use directly',
  'protocol': 'one-hot encode',
  'src_ip': 'extract: is_private, /24 subnet',
  'timestamp': 'extract: hour_of_day, day_of_week',
  'duration_str': 'parse float from string',
  'action': 'drop (target variable, not a feature)'
}
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Dropping IP columns entirely | Loses valuable signal (private vs public, known-bad IPs) | Extract meaningful features from IPs |
| Converting IP to integer directly | "192.168.1.1" becomes a large number with misleading math | Extract subnet, public/private, etc. |
| Including `action` as a feature | Label leakage — the model sees the answer | Drop the target variable from features |
| Ignoring timestamp structure | Misses time-of-day patterns (attacks often happen at night) | Extract hour, day-of-week, etc. |

---

> Next: [02_guide_numeric_feature_extraction.md](02_guide_numeric_feature_extraction.md)
