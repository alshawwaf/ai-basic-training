# Exercise 2 — Numeric Feature Extraction

> Back to [README.md](README.md)

## What You Will Learn

- How to derive `bytes_per_second` and `packet_rate` from raw bytes and duration
- How to create a `port_risk_score` based on security knowledge
- Why derived features often outperform raw fields
- How to validate that derived features make intuitive sense

---

## Concept: Derived Features

Raw numeric fields like `bytes_sent` and `duration` are useful, but their *combination* is often more informative:

| Raw fields | Derived feature | Why it's better |
|-----------|----------------|-----------------|
| `bytes_sent`, `duration` | `bytes_per_second` | Normalises volume by time; exfil at 1KB/s for 10 hours looks very different from 10KB in 1 second |
| `packets`, `duration` | `packet_rate` | Identifies SYN floods (very high packet rate, short duration) |
| `bytes_sent`, `bytes_received` | `bytes_ratio` | Asymmetric connections (much more sent than received) suggest upload/exfil |
| `bytes_sent`, `packets` | `bytes_per_packet` | Large bytes/packet = file transfer; small = control traffic |

**From raw fields to derived features**

| Derived feature | Formula | Worked example | Result |
|---|---|---|---:|
| `bytes_per_second` | `bytes_sent / duration` | `14580 / 2.3` | **6339** |
| `packet_rate`      | `packets / duration`    | `12 / 2.3` | **5.2** |
| `bytes_ratio`      | `bytes_sent / (bytes_received + 1)` | `14580 / (820 + 1)` | **17.8** |

The `+1` in `bytes_ratio` is a guard against division by zero when a connection received nothing back.

> **Want to go deeper?** [Feature engineering (Wikipedia)](https://en.wikipedia.org/wiki/Feature_engineering)

---

## Concept: Port Risk Scores

Instead of using raw port numbers as features (which have no natural numerical ordering — port 443 is not "more" than port 80 in any meaningful ML sense), we encode security knowledge as a risk score:

| Port(s) | Risk | Rationale |
|---------|------|-----------|
| 80, 443 | 1 | Standard HTTP/HTTPS — normal |
| 53 | 2 | DNS — watch for DNS tunnelling |
| 22 | 3 | SSH — legitimate but targeted |
| 3389 | 5 | RDP — frequently exploited |
| 21 | 4 | FTP — sends credentials in clear |
| Ports < 1024 (other) | 3 | Well-known, potentially dangerous |
| Ports >= 1024 | 1 | Ephemeral, typically benign |

**Mapping raw port numbers to a risk score**

| Raw `dst_port` | Mapped risk | Interpretation |
|---:|---:|---|
| 443   | 1 | standard HTTPS — normal |
| 22    | 3 | SSH — legitimate but targeted |
| 3389  | 5 | RDP — high-risk, frequently exploited |
| 51234 | 1 | ephemeral source-side port — typically benign |

Port numbers themselves have no meaningful ordering — `3389` is not "more" than `443` in any sense the model can use. The lookup table is how we *inject security knowledge* into the feature space, so the model doesn't have to learn that RDP is risky from scratch.

This embeds domain knowledge into the feature space — the model does not need to learn port semantics from scratch.

---

## Concept: Time-Based Features

Timestamps can be decomposed into:
- `hour_of_day` — attacks often happen at night (off-hours) or during business hours (blend in)
- `day_of_week` — weekend activity from usually-offline machines is suspicious
- `is_business_hours` — binary flag for 09:00–17:00 Monday–Friday

```python
df['hour']     = pd.to_datetime(df['timestamp']).dt.hour
df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
```

---

## What Each Task Asks You to Do

### Task 1 — Parse Duration and Compute bytes_per_second
Strip the "s" suffix from `duration_str` and convert to float. Derive `bytes_per_second = bytes_sent / duration`. Handle division by zero (set to 0 if duration=0).

### Task 2 — Derive packet_rate and bytes_ratio
Compute `packet_rate = packets / duration` and `bytes_ratio = bytes_sent / (bytes_received + 1)` (add 1 to avoid division by zero). Print summary statistics for both.

### Task 3 — Create port_risk_score
Map each `dst_port` value to a risk score using the table above. Print the distribution of risk scores.

### Task 4 (BONUS) — Extract Timestamp Features
Parse the `timestamp` column into `hour_of_day`, `day_of_week`, and `is_business_hours`. Print the mean bytes_per_second during business hours vs off-hours.

---

## Expected Outputs

```
TASK 1 — Duration parsed and bytes_per_second computed:
Sample of duration (raw → parsed):
  raw: '2.34s'  →  float: 2.34
  raw: '0.05s'  →  float: 0.05

bytes_per_second stats:
  mean:  ~3500  (legitimate transfers)
  max:   ~45000  (potential exfil spike)
  min:    0.0

TASK 2 — Derived features:
packet_rate stats:
  mean: ~8.2 packets/sec
  max:  ~180  ← suspicious high rate

bytes_ratio stats (sent/received):
  mean: ~0.85
  max:  ~32.1  ← sent much more than received — potential upload/exfil

TASK 3 — Port risk scores:
port_risk_score=1 (standard HTTP/HTTPS): ~140 connections
port_risk_score=2 (DNS):                  ~25 connections
port_risk_score=3 (SSH):                  ~20 connections
port_risk_score=5 (RDP):                  ~15 connections
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Forgetting to handle zero duration | ZeroDivisionError | Use `np.where(duration > 0, bytes/duration, 0)` |
| Using raw port numbers as features | Model treats 443 as "bigger" than 80 | Use port risk scores or one-hot encode top-N ports |
| Including the target (`action`) as a feature | Label leakage | Drop target from feature matrix |
| Not validating derived features | Silent bugs | Print `.describe()` and check ranges make sense |
