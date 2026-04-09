# Categorical Encoding

> Back to [README.md](README.md)

## What You Will Learn

- The difference between `LabelEncoder` and `OneHotEncoder`
- Why one-hot encoding is usually preferred for nominal categories
- What the "dummy variable trap" is and how to avoid it
- How to use `pd.get_dummies()` as a quick alternative

---

## Concept: LabelEncoder vs OneHotEncoder

**LabelEncoder** assigns an integer to each category:
```
TCP → 0, UDP → 1, ICMP → 2
```

**Problem:** This implies an ordering (ICMP > UDP > TCP) and a distance (TCP to ICMP is "2 apart") that doesn't exist. A linear model will try to learn coefficients that treat 0, 1, 2 as a scale — leading to incorrect behaviour.

**OneHotEncoder** creates one binary column per category. The single `protocol` column expands into one column per category:

| Original `protocol` | `proto_TCP` | `proto_UDP` | `proto_ICMP` |
|---|:---:|:---:|:---:|
| TCP  | **1** | 0 | 0 |
| UDP  | 0 | **1** | 0 |
| ICMP | 0 | 0 | **1** |
| TCP  | **1** | 0 | 0 |

One column becomes three. Each protocol now lives in its own dimension, with no implied ordering or distance between them.

Now there is no implied ordering. Each protocol is independent.

| Encoding | Use when |
|---------|---------|
| LabelEncoder | Target variable (y), not features; or tree-based models (which don't use distances) |
| OneHotEncoder | Linear models, neural networks, any model that uses distances |
| Ordinal encoding | Categories have a natural order (low/medium/high) |

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_label_vs_onehot.png" alt="Side-by-side panels. Left panel 'LabelEncoder' in red shows a two-column table — protocol on the left, protocol_label on the right — with TCP encoded as 1, UDP as 2, ICMP as 0. Italic caption beneath: model thinks TCP is halfway between ICMP and UDP. Right panel 'OneHotEncoder' in green shows a four-column table — protocol, proto_ICMP, proto_TCP, proto_UDP — where every row has exactly one cell highlighted in green. Italic caption beneath: each protocol gets its own flag column, no implied distance.">
  <div class="vis-caption">Same five protocol values, two encodings. LabelEncoder forces a fake order; OneHotEncoder gives each category its own dimension.</div>
</div>

> **Want to go deeper?** [One-hot encoding (Wikipedia)](https://en.wikipedia.org/wiki/One-hot)

---

## Concept: The Dummy Variable Trap

With one-hot encoding, the three protocol columns sum to exactly 1 for every row (`TCP + UDP + ICMP = 1`). This causes **perfect multicollinearity** in linear models — the model cannot distinguish the individual effect of each protocol.

The fix: drop one column (`drop='first'`). With two columns (UDP, ICMP), the third (TCP) is implied when both are 0.

**With `drop='first'` (ICMP dropped as the reference category)**

| Original `protocol` | `proto_TCP` | `proto_UDP` | What both 0s mean |
|---|:---:|:---:|---|
| TCP  | **1** | 0 | — |
| UDP  | 0 | **1** | — |
| ICMP | 0 | 0 | row falls back to the dropped reference → ICMP is implied |

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_dummy_trap.png" alt="Two side-by-side encoding tables. Left table 'Naive one-hot (3 columns)' shows proto_ICMP, proto_TCP, proto_UDP for three rows TCP/UDP/ICMP — the ICMP row's proto_ICMP cell is highlighted in red to show the redundancy. A green arrow labelled 'drop reference' points to the right table 'drop=first (2 columns)' which now has only proto_TCP and proto_UDP — the ICMP row has 0 in both columns. Caption: if proto_TCP=0 and proto_UDP=0 the row must be ICMP.">
  <div class="vis-caption">The third column carries no new information. Dropping it removes perfect collinearity without losing any signal — ICMP becomes the implicit reference category.</div>
</div>

```python
# sklearn
ohe = OneHotEncoder(drop='first', sparse_output=False)

# pandas
pd.get_dummies(df['protocol'], drop_first=True)
```

**When does it matter?** For tree-based models (decision trees, random forests) it does not matter — they split on individual features and are not affected by multicollinearity. For linear models and neural networks, always drop one column.

---

## Concept: Handling High-Cardinality Categoricals

`src_ip` might have thousands of unique values. One-hot encoding 1000 IPs creates 1000 columns, most of which have very few 1s. This is impractical. Instead:
- Keep only the top-N most frequent values as separate columns
- Group rare values into an "other" category
- Extract meaningful sub-features (subnet, is_private, etc.)

---

## What Each Task Asks You to Do

### Task 1 — LabelEncoder on Protocol
Apply `LabelEncoder` to `raw_df['protocol']`. Print the mapping (class_ → integer). Explain in a comment why this would be problematic for a logistic regression.

### Task 2 — OneHotEncoder on Protocol
Apply `OneHotEncoder(sparse_output=False, drop='first')` to `raw_df[['protocol']]`. Print the resulting column names and the first 5 encoded rows.

### Task 3 — pd.get_dummies Comparison
Use `pd.get_dummies(raw_df['protocol'], prefix='proto', drop_first=True)`. Verify it produces the same result as OneHotEncoder. Print the first 5 rows.

### Task 4 (BONUS) — Encoding Comparison Demo
Fit a LogisticRegression with LabelEncoded protocol vs OneHotEncoded protocol. Compare test accuracy. Show that the encoding choice affects model quality.

<div class="lecture-visual">
  <img src="/static/lecture_assets/fe_encoding_accuracy.png" alt="Bar chart with two bars, both reaching 0.975 on the y-axis. Left bar in red labelled LabelEncoded, right bar in green labelled OneHotEncoded. Title 'Same model, same features, only the encoding differs'. Caption beneath: delta accuracy = +0.000 — they tie because the toy 200-row dataset's label is dominated by bytes_sent and duration, so the protocol column carries little signal either way.">
  <div class="vis-caption">On this tiny lab dataset the two encodings tie — the protocol column is almost noise relative to the engineered features. On real datasets with stronger categorical signal the OHE bar typically pulls ahead for linear models.</div>
</div>

---

## Expected Outputs

```
TASK 1 — LabelEncoder:
ICMP → 0
TCP  → 1
UDP  → 2
Problem: treats TCP (1) as halfway between ICMP (0) and UDP (2) — meaningless!

TASK 2 — OneHotEncoder (drop first):
Feature names: ['protocol_TCP', 'protocol_UDP']
(ICMP is the dropped reference category)
First 5 rows:
protocol_TCP  protocol_UDP
    1.0           0.0
    0.0           1.0
    ...

TASK 3 — pd.get_dummies:
proto_TCP  proto_UDP
    1          0
    0          1
    ...
Matches OneHotEncoder: True

TASK 4 (BONUS):
LabelEncoded  accuracy: 0.975
OneHotEncoded accuracy: 0.975
Difference: +0.000  (Same — protocol carries little signal in this lab set)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using LabelEncoder on features for linear models | Implied numerical ordering corrupts training | Use OneHotEncoder for nominal features |
| Forgetting `drop='first'` | Dummy variable trap — multicollinearity | Always drop one column |
| Fitting the encoder on test data | Data leakage | Fit encoder on train set, transform both |
| Applying get_dummies to full dataset before splitting | Leakage — test distribution affects encoder | Split first, encode separately |
