# Exercise 2 — Train and Read the Tree

> Back to [1_lab_guide.md](1_lab_guide.md)

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

---

## Concept: Interpreting Rules in a Security Context

When `export_text()` shows:

```
|--- connection_rate <= 55.30
|   |--- unique_dest_ports <= 14.50
|   |   |--- class: benign
|   |--- unique_dest_ports >  14.50
|   |   |--- class: port_scan
|--- connection_rate >  55.30
|   |--- class: DoS
```

This tells you: "If connection rate is normal (≤55 rps) and the source contacts many ports (>14), it is a port scan. If connection rate is very high (>55), it is DoS." These rules are directly actionable in a firewall or IDS.

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
Training accuracy: 0.978
Test accuracy:     0.962

TASK 2 — Tree rules (first 30 lines):
|--- connection_rate <= 55.32
|   |--- bytes_sent <= 27500.00
|   |   |--- unique_dest_ports <= 14.50
|   |   |   |--- class: 0 (benign)
|   |   |--- unique_dest_ports >  14.50
|   |   |   |--- class: 1 (port_scan)
|   |--- bytes_sent >  27500.00
|   |   |--- class: 2 (exfil)
|--- connection_rate >  55.32
|   |--- class: 3 (DoS)

Root split: connection_rate <= 55.32
Meaning: High connection rate (>55 rps) immediately → DoS classification

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

---

> Next: [exercise3_feature_importance.md](exercise3_feature_importance.md)
