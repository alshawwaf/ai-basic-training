# How Trees Make Decisions

> Back to [README.md](README.md)

## What You Will Learn

- How a decision tree builds if/else rules from data
- What Gini impurity measures and how it drives splits
- What information gain is and how the tree uses it to choose the best feature to split on
- How to manually apply tree rules to classify a network connection

---

## Concept: The If/Else Tree

> **Want to go deeper?** [Decision tree learning — Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)

A decision tree is a flowchart of yes/no questions. Each internal node asks a question about one feature; each branch is an answer; each leaf is a prediction.

Example for network traffic — read each row as a path of yes/no answers from the root question down to a final prediction:

| `connection_rate > 50`? | `unique_dest_ports > 20`? | `bytes_sent > 100000`? | Prediction |
|:---:|:---:|:---:|---|
| no  | — | — | **benign** |
| yes | yes | — | **port_scan** |
| yes | no  | yes | **exfil** |
| yes | no  | no  | **benign** |

Each row corresponds to one root-to-leaf path in the tree. A real tree may have many more questions, but the structure is the same: each internal node splits the data on one feature, each leaf is a final prediction.

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_gini_intuition.png" alt="Three side-by-side bar charts showing class composition for different node states. Left: 100 benign only, Gini = 0.000. Middle: 60 benign and 40 DoS, Gini = 0.480. Right: 25 of each of four classes, Gini = 0.750">
  <div class="vis-caption">Three nodes side by side. Each chart shows the class composition; the title prints the Gini value. A pure node has impurity 0; a perfectly mixed 4-class node hits the maximum at 0.75.</div>
</div>

---

## Concept: Information Gain

Information gain measures the improvement in purity from a split:

```
Gain = Gini(parent) - [weighted average of Gini(left child), Gini(right child)]
```

A high information gain means the split dramatically reduces uncertainty. The tree evaluates every possible feature and every possible threshold, then picks the (feature, threshold) pair with the highest gain.

**Information gain from splitting on `connection_rate <= 55`**

| Node | Samples | Composition | Gini | Notes |
|---|---:|---|---:|---|
| **Parent** | 100 | 60 benign, 40 DoS | **0.480** | mixed — high impurity |
| Left child (`rate ≤ 55`) | 60 (60%) | 58 benign, 2 DoS | 0.065 | almost pure benign |
| Right child (`rate > 55`) | 40 (40%) | 2 benign, 38 DoS | 0.095 | almost pure DoS |

The weighted child impurity is `0.6 × 0.065 + 0.4 × 0.095 = 0.077`, so the **information gain** is `0.480 − 0.077 = 0.403`. A near-half drop in impurity is a great split — the tree's split-search routine would happily pick this one over any competing feature.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_information_gain.png" alt="Three bar charts showing the information gain split. Parent: 60 benign and 40 DoS, Gini=0.480. Left child (rate ≤ 55): 58 benign and 2 DoS, Gini=0.064. Right child (rate > 55): 2 benign and 38 DoS, Gini=0.095. Title: gain = 0.480 - 0.077 = 0.403">
  <div class="vis-caption">Real worked example. Splitting the parent on <code>connection_rate ≤ 55</code> drops the weighted child Gini from 0.480 to 0.077 — an information gain of 0.403.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_class_scatter.png" alt="Scatter plot of all 2000 connections on log-log axes. connection_rate on x-axis, bytes_sent on y-axis. Four coloured clusters: cyan benign in the middle-left, violet port_scan slightly higher-left, green exfil in the top-left, red DoS in the far right">
  <div class="vis-caption">Real <code>plt.scatter</code> on the lab dataset, coloured by class. Each cluster sits in its own corner — that is exactly the kind of structure a decision tree exploits with simple axis-aligned splits.</div>
</div>

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
