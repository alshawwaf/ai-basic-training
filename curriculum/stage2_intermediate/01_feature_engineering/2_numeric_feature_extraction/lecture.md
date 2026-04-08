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

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_derived_features.png" alt="Three coloured cards side by side. Cyan card 'bytes_per_second = bytes_sent / duration' with worked example using row 0 of the lab raw_df. Violet card 'packet_rate = packets / duration' with the same row's numbers. Orange card 'bytes_ratio = bytes_sent / (bytes_recv + 1)' showing the +1 guard. Each card has an italic intuition line beneath: huge spikes flag exfil bursts, very high rate means SYN flood/scan, ratio greater than 1 means more upload than download.">
  <div class="vis-caption">The three derived features computed on the very first row of the lab raw_df. Each formula is one line of pandas — the value comes from combining two raw columns the model could not exploit on its own.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_port_risk_table.png" alt="Lookup table mapping six common destination ports to a risk score. Header row dst_port, service, risk score, why. Rows: 80 HTTP score 1 cyan badge, 443 HTTPS score 1 cyan, 53 DNS score 2 light cyan, 22 SSH score 3 orange, 21 FTP score 4 deep orange, 3389 RDP score 5 red. Each row also includes a one-line rationale.">
  <div class="vis-caption">The exact lookup table the lab uses. Cyan-to-red colour ramp on the score badge mirrors the risk: standard web traffic on the safe end, RDP on the dangerous end.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_business_hours.png" alt="Two-panel bar chart from the lab raw_df. Left panel: number of connections in business hours (cyan, large bar) versus off hours (orange, smaller bar). Right panel: mean bytes_per_second for the two windows, both bars labelled with the actual mean. The off-hours mean is noticeably higher than the business-hours mean.">
  <div class="vis-caption">Splitting the same 200 events by <code>is_business_hours</code> immediately surfaces a behavioural gap that no single raw column reveals.</div>
</div>

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
Sample of duration (raw -> parsed):
  raw: '2.34s'  ->  float: 2.34
  raw: '0.05s'  ->  float: 0.05

bytes_per_second stats:
  mean:    2236.4  (legitimate transfers)
  max:   138800.0  (potential exfil spike)
  min:        2.8

TASK 2 — Derived features:
packet_rate stats:
  mean:  21.85 packets/sec
  max:  860.00  <- suspicious high rate (SYN flood indicator)

bytes_ratio stats (sent/received):
  mean:   4.77
  max:  256.74  <- sent much more than received — potential upload/exfil

TASK 3 — Port risk scores:
port_risk_score=1 (standard HTTP/HTTPS/ephemeral): 138 connections
port_risk_score=2 (DNS):                            22 connections
port_risk_score=3 (SSH/well-known):                 16 connections
port_risk_score=4 (FTP):                             7 connections
port_risk_score=5 (RDP):                            17 connections
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Forgetting to handle zero duration | ZeroDivisionError | Use `np.where(duration > 0, bytes/duration, 0)` |
| Using raw port numbers as features | Model treats 443 as "bigger" than 80 | Use port risk scores or one-hot encode top-N ports |
| Including the target (`action`) as a feature | Label leakage | Drop target from feature matrix |
| Not validating derived features | Silent bugs | Print `.describe()` and check ranges make sense |
