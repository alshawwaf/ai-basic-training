# Exercise 1 — Why Raw Logs Fail

> Back to [README.md](README.md)

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_raw_log_dtypes.png" alt="Sample of the raw firewall log with column headers colour-coded by dtype. Cyan headers (dst_port, bytes_sent) are numeric and accepted by sklearn directly. Orange header (duration_str) is a string that can be parsed with str.rstrip('s'). Red headers (timestamp, src_ip, protocol) are strings that sklearn rejects without one-hot or feature extraction. Four data rows shown beneath, all in monospace.">
  <div class="vis-caption">A real lab raw_df row. Cyan columns flow straight into <code>fit()</code>; orange parses with one strip; red columns must be engineered before sklearn will accept the matrix.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_sklearn_rejects.png" alt="Flow diagram. A grey box on the left labelled raw_df with columns bytes_sent, bytes_recv, protocol, packets connects via an arrow labelled .fit(X, y) to a cyan LogisticRegression box. From the LogisticRegression box a red arrow points to a red ValueError box reading 'could not convert string to float: TCP'. Caption beneath: sklearn fit() requires every column to be numeric — one string column is enough to halt the entire pipeline.">
  <div class="vis-caption">What actually happens when you forget to encode <code>protocol</code>. One non-numeric column stops the whole training run.</div>
</div>

---

## Concept: Feature Engineering as Translation

Feature engineering is the process of translating raw data into a numerical representation that:
1. Contains the signal the model needs to distinguish classes
2. Is in a format sklearn can process
3. Is robust to variations (different port numbers, new IPs, etc.)

**Raw log line → numeric feature vector**

Raw log line (strings + mixed types — sklearn rejects this):

```
"2024-01-15 08:23:11  192.168.1.42  TCP  443  14580  2.3s"
```

After feature engineering, the same row becomes a numeric vector that sklearn can consume:

| Position | Engineered feature | Value | Derived from |
|---:|---|---:|---|
| 0 | `hour_of_day`        | 8     | `timestamp` → `.hour` |
| 1 | `is_business_hours`  | 1     | `8 ≤ hour < 18` |
| 2 | `proto_TCP`          | 1     | one-hot of `protocol` |
| 3 | `port_risk_score`    | 3     | lookup table on `dst_port` (443 = web) |
| 4 | `bytes_per_second`   | 6339  | `bytes / duration` |
| 5 | `packet_rate`        | 5.2   | `packets / duration` |
| 6 | `is_private`         | 1     | `src_ip` is in RFC1918 range |

Output vector: `[8, 1, 1, 3, 6339, 5.2, 1]` — every column is numeric, fixed-width, and ready for `model.fit(X, y)`.

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_transformation_plan.png" alt="Two-column diagram listing each raw column on the left and the transformation it needs on the right. timestamp arrow extract hour/day/business_hours, src_ip arrow is_private flag, dst_ip arrow is_private and reputation lookup, dst_port arrow port_risk_score lookup table, protocol arrow one-hot encode, bytes_sent/bytes_recv/packets arrow use directly, duration_str arrow strip s and cast to float, action arrow drop because it is the LABEL.">
  <div class="vis-caption">The full transformation plan for the lab raw_df. Cyan = use directly, violet = encode, orange = parse, red = drop.</div>
</div>

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
