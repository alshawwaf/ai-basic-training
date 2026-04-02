# Exercise 1 — How Trees Make Decisions

> Back to [00_overview.md](00_overview.md)

## What You Will Learn

- How a decision tree builds if/else rules from data
- What Gini impurity measures and how it drives splits
- What information gain is and how the tree uses it to choose the best feature to split on
- How to manually apply tree rules to classify a network connection

---

## Concept: The If/Else Tree

> **Want to go deeper?** [Decision tree learning — Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)

A decision tree is a flowchart of yes/no questions. Each internal node asks a question about one feature; each branch is an answer; each leaf is a prediction.

Example for network traffic:

```
Is connection_rate > 50?
├── YES → Is unique_dest_ports > 20?
│          ├── YES → port_scan
│          └── NO  → Is bytes_sent > 100000?
│                     ├── YES → exfil
│                     └── NO  → benign
└── NO  → benign
```

The model learns *which* questions to ask and *which* threshold to use by finding splits that best separate the classes.

---

## Concept: Gini Impurity

Gini impurity measures how "mixed" a node's class distribution is:

```
Gini = 1 - Σ p²_i
```

Where `p_i` is the proportion of samples belonging to class i.

| Scenario | Gini | Interpretation |
|----------|------|----------------|
| All samples are benign | 0.0 | Pure node — perfect |
| 50% benign, 50% attack | 0.5 | Maximum uncertainty |
| 25% each of 4 classes | 0.75 | Very impure |

The tree always chooses the split that **minimises the weighted average Gini** of the resulting child nodes.

---

## Concept: Information Gain

Information gain measures the improvement in purity from a split:

```
Gain = Gini(parent) - [weighted average of Gini(left child), Gini(right child)]
```

A high information gain means the split dramatically reduces uncertainty. The tree evaluates every possible feature and every possible threshold, then picks the (feature, threshold) pair with the highest gain.

```
  Information gain from splitting on connection_rate <= 55

  PARENT (100 samples)                Gini = 0.480
  ┌──────────────────────────────┐
  │  60 benign     40 DoS       │
  └──────────────┬───────────────┘
                 │
      connection_rate <= 55?
        ┌────────┴────────┐
        ▼                 ▼
  LEFT (60 samples)    RIGHT (40 samples)
  ┌──────────────┐    ┌──────────────┐
  │ 58 benign    │    │  2 benign    │
  │  2 DoS       │    │ 38 DoS       │
  │ Gini = 0.065 │    │ Gini = 0.095 │
  └──────────────┘    └──────────────┘
       almost pure         almost pure

  Gain = 0.480 - (0.6*0.065 + 0.4*0.095) = 0.403  ← great split!
```

**Security intuition:** The feature `connection_rate` splits benign (low rate) from DoS (very high rate) cleanly → high Gini gain. The feature `src_port` is more uniformly distributed → low gain.

---

## Concept: The Network Traffic Dataset

The dataset simulates 4 traffic classes with 6 features:

| Feature | Description |
|---------|-------------|
| `connection_rate` | Connections per second from this source |
| `bytes_sent` | Total bytes sent per connection |
| `bytes_received` | Total bytes received |
| `unique_dest_ports` | Number of distinct destination ports contacted |
| `duration_seconds` | How long the connection lasted |
| `failed_connections` | Number of failed (SYN without SYN-ACK) connections |

| Label | Traffic type | Signature |
|-------|-------------|-----------|
| 0 | benign | Low rate, normal ports, balanced bytes |
| 1 | port_scan | High unique_dest_ports, low bytes, many failures |
| 2 | exfil | High bytes_sent, low ports, long duration |
| 3 | DoS | Very high connection_rate, low bytes, short duration |

---

## What Each Task Asks You to Do

### Task 1 — Compute Gini Impurity Manually
Given a node with 40 benign, 30 port_scan, 20 exfil, 10 DoS samples, compute the Gini impurity by hand (using numpy). Then compute it for a "pure" node with 100% benign. Print both.

### Task 2 — Compute Information Gain for a Split
A parent node has 60 benign and 40 DoS. A split on `connection_rate > 50` produces:
- Left child (rate ≤ 50): 58 benign, 2 DoS
- Right child (rate > 50): 2 benign, 38 DoS

Compute the information gain of this split manually.

### Task 3 — Generate the Dataset and Inspect It
Create the 4-class network traffic dataset. Print shape, class distribution, and mean feature values by class. Identify which features show the biggest difference between classes.

### Task 4 (BONUS) — Classify Manually
Using the example tree rules from the Background section above, classify these three connections manually (write your answer as a comment):
- A: connection_rate=80, unique_dest_ports=25, bytes_sent=1000
- B: connection_rate=20, unique_dest_ports=3, bytes_sent=200
- C: connection_rate=60, unique_dest_ports=5, bytes_sent=150000

---

## Expected Outputs

```
TASK 1 — Gini impurity:
Mixed node (40 benign, 30 port_scan, 20 exfil, 10 DoS):
  Gini = 1 - (0.4² + 0.3² + 0.2² + 0.1²) = 0.700

Pure node (100% benign):
  Gini = 1 - (1.0²) = 0.000

TASK 2 — Information gain:
Parent Gini: 0.480
Left child Gini:  0.065  (weight=0.60)
Right child Gini: 0.095  (weight=0.40)
Weighted child Gini: 0.077
Information Gain = 0.480 - 0.077 = 0.403  ← very good split!

TASK 3 — Dataset:
Shape: (2000, 7)
Classes: {0: 500, 1: 500, 2: 500, 3: 500}

Feature means by class:
                   connection_rate  bytes_sent  unique_dest_ports  ...
0 (benign)               ~10           ~5000            ~3
1 (port_scan)            ~25           ~500             ~45
2 (exfil)                ~8            ~80000           ~2
3 (DoS)                  ~200          ~200             ~2
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Computing Gini as Σ p² instead of 1 - Σ p² | Wrong value | Remember Gini = 1 - Σ p² |
| Forgetting to weight child Ginis by sample count | Wrong information gain | Weight by n_child / n_parent |
| Using information gain = parent - children (not weighted) | Incorrect | Use weighted average of child impurities |
| Labelling target as string instead of int | Some sklearn functions require int labels | Use integer class codes |

---

> Next: [02_guide_train_and_read_the_tree.md](02_guide_train_and_read_the_tree.md)
