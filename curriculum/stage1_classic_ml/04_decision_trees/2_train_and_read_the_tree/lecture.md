# Exercise 2 — Train and Read the Tree

> Back to [README.md](README.md)

## What You Will Learn

- How to train a `DecisionTreeClassifier`
- How to visualise the tree with `plot_tree()` or export it as text
- How to read and interpret individual tree nodes
- How to extract and understand the rules the model learned

---

## Concept: DecisionTreeClassifier Parameters

> **Want to go deeper?** [Decision tree learning — Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=4,          # limits tree depth to prevent overfitting
    criterion='gini',     # use Gini impurity (alternative: 'entropy')
    random_state=42       # reproducible splits when there are ties
)
```

| Parameter | What it controls |
|-----------|-----------------|
| `max_depth` | Maximum number of levels in the tree; None = grow until all leaves are pure |
| `criterion` | Splitting criterion: 'gini' (default) or 'entropy' (information gain) |
| `min_samples_split` | Minimum samples a node must have to attempt a split |
| `min_samples_leaf` | Minimum samples required in each leaf |

---

## Concept: Visualising the Tree

`sklearn.tree.plot_tree()` renders the tree as a matplotlib figure:

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plot_tree(model,
          feature_names=FEATURES,
          class_names=CLASS_NAMES,
          filled=True,           # colour nodes by majority class
          rounded=True,          # rounded boxes
          fontsize=10)
plt.show()
```

For text output (easier to read programmatically):

```python
from sklearn.tree import export_text
rules = export_text(model, feature_names=FEATURES)
print(rules)
```

---

## Concept: Reading a Tree Node

Each node in `plot_tree()` output shows:

```
connection_rate <= 55.3     ← the split question
gini = 0.423                ← impurity before the split
samples = 800               ← how many training samples reached this node
value = [310, 290, 90, 110] ← count of each class [benign, port_scan, exfil, DoS]
class = benign              ← majority class at this node
```

The **root node** is the first split — the single most informative feature/threshold. Nodes near the root are always more important than nodes near the leaves.

**Reading the tree — node anatomy**

A single internal node displayed by `plot_tree()` carries five pieces of information:

| Line in the node | Example | Meaning |
|---|---|---|
| Split question | `connection_rate <= 55.3` | the test the node applies to incoming samples |
| `gini` | `0.423` | impurity at this node *before* the split |
| `samples` | `800` | how many training samples landed here |
| `value` | `[310, 290, 90, 110]` | class counts in the order `[benign, port_scan, exfil, DoS]` |
| `class` | `benign` | majority class — what this node would predict if it were a leaf |

The split question routes samples to one of two children:

| Branch | Condition | Where the sample goes |
|---|---|---|
| **Yes** | `feature ≤ threshold` | left child |
| **No**  | `feature > threshold`  | right child |

The **root node** is the first split — the single most informative feature/threshold the tree could find. Nodes near the root are always more important than nodes near the leaves.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_tree_depth4.png" alt="Decision tree visualisation produced by sklearn plot_tree at max_depth=4. The root node splits on duration_seconds <= 59.34 with 1600 samples. Internal nodes branch on connection_rate, unique_dest_ports, bytes_sent, bytes_received and failed_connections; leaf nodes are coloured by majority class (orange benign, green port_scan, blue exfil, magenta DoS)">
  <div class="vis-caption">Real <code>plot_tree(model, max_depth=4)</code> on the lab dataset. The root split is <code>duration_seconds ≤ 59.34</code> — exfil has long sessions and ends up on the right, everything else on the left.</div>
</div>

---

## Concept: Interpreting Rules in a Security Context

When `export_text()` shows:

```
|--- duration_seconds <= 59.34
|   |--- connection_rate <= 64.98
|   |   |--- unique_dest_ports <= 14.00
|   |   |   |--- class: benign
|   |   |--- unique_dest_ports >  14.00
|   |   |   |--- class: port_scan
|   |--- connection_rate >  64.98
|   |   |--- class: DoS
|--- duration_seconds >  59.34
|   |--- class: exfil
```

This tells you: "Short sessions with normal connection rate and few ports → benign. Short sessions with normal rate but many ports → port scan. Short sessions with very high rate → DoS. Long sessions → exfil." These rules are directly actionable in a firewall or IDS.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dt_decision_regions.png" alt="2D decision regions plot. Background is divided into four colour bands by the trained tree on connection_rate and bytes_sent (log axes). Cyan benign region top-left, violet port_scan band, green exfil top, red DoS far right. Training points overlaid as small coloured dots">
  <div class="vis-caption">A 2-feature tree's decision regions visualised. The boundaries are always axis-aligned rectangles — that is the only kind of region a decision tree can carve out.</div>
</div>

---

## What Each Task Asks You to Do

### Task 1 — Train the Classifier
Train a `DecisionTreeClassifier` with `max_depth=4` and `random_state=42` on the training data. Print the training and test accuracy.

### Task 2 — Export the Tree as Text
Use `export_text()` to print the first 30 lines of the tree rules. Identify: what is the root node's split? What does it mean for network traffic?

### Task 3 — Visualise the Tree
Use `plot_tree()` to generate a figure. Read and manually describe what happens at the root and at least one second-level node. Write your interpretation as a comment.

### Task 4 (BONUS) — Extract a Specific Decision Path
Pick one test sample and trace it through the tree manually using the exported text rules. Print the sample's features and which leaf node it ends up at.

---

## Expected Outputs

```
TASK 1 — Training:
Training accuracy: 0.940
Test accuracy:     0.910

TASK 2 — Tree rules (first 30 lines):
|--- duration_seconds <= 59.34
|   |--- connection_rate <= 64.98
|   |   |--- unique_dest_ports <= 14.00
|   |   |   |--- class: 0 (benign)
|   |   |--- unique_dest_ports >  14.00
|   |   |   |--- class: 1 (port_scan)
|   |--- connection_rate >  64.98
|   |   |--- class: 3 (DoS)
|--- duration_seconds >  59.34
|   |--- class: 2 (exfil)

Root split: duration_seconds <= 59.34
Meaning: Long-lived sessions (>59 s) are almost always exfil

TASK 3 — Tree visualisation created.
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Not setting `max_depth` | Tree becomes enormous and unreadable | Use `max_depth=4` for visualisation |
| Using `plot_tree` without a figure size | Tiny, unreadable figure | Set `figsize=(20, 10)` |
| Reading feature importance from node appearance alone | Misleading | Use `.feature_importances_` (Exercise 3) |
| Confusing "class" in a node with "prediction" | Node class is the majority class, not always correct | Only leaf nodes give final predictions |
