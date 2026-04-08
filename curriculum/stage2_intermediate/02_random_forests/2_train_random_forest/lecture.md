# Exercise 2 — Train a Random Forest

> Back to [README.md](README.md)

## What You Will Learn

- The key parameters of `RandomForestClassifier`
- How `oob_score=True` gives a free estimate of generalisation
- How to compare a single tree to a forest on the same data
- How to read the classification report for a binary security classifier

---

## Concept: RandomForestClassifier Key Parameters

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,      # number of trees
    max_depth=None,        # individual tree depth (None = grow fully, then bag)
    max_features='sqrt',   # features considered at each split (sqrt(n_features) typical)
    oob_score=True,        # use out-of-bag samples for free validation
    n_jobs=-1,             # use all CPU cores
    random_state=42
)
```

| Parameter | Effect |
|-----------|--------|
| `n_estimators` | More trees → more stable predictions; diminishing returns after ~200 |
| `max_features` | Fewer features per split → more diverse trees → less correlation between trees |
| `max_depth` | Limits individual tree depth; but random forests are usually grown fully |
| `oob_score` | If True, computes OOB accuracy automatically (free; no extra data needed) |

> **Want to go deeper?** [Random forest (Wikipedia)](https://en.wikipedia.org/wiki/Random_forest)

---

## Concept: Feature Subsampling

At each split, the random forest considers only a **random subset** of features (not all features). This is the key difference from plain bagging. It ensures that even when one feature is very strong, different trees will use different primary splits, producing diverse and uncorrelated trees.

Default: `max_features='sqrt'` → √(n_features) features considered per split.

**Feature subsampling at one node, three different trees**

The full feature pool: `[entropy, packer, vsize, imports, imp_ent, code_sz, sections]`. At each split, every tree is shown only a random subset of `√7 ≈ 3` of those features.

| Tree | Random feature subset offered at this node | Best split chosen |
|---|---|---|
| 1 | `[entropy, packer, code_sz]` | splits on `entropy` |
| 2 | `[vsize, imports, sections]` | splits on `vsize` |
| 3 | `[entropy, imp_ent, imports]` | splits on `entropy` |

The trees end up splitting on **different** features even when one feature (here, `entropy`) is genuinely strong — that diversity is what stops the trees from agreeing too closely with each other and is the real source of the forest's lower variance.

For 7 features: √7 ≈ 2.6 → 2 or 3 features considered at each node. This is small enough to create diversity but large enough to use the good features most of the time.

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_feature_subsampling.png" alt="Diagram showing the full pool of 7 PE features in a row of grey cards across the top. Beneath, three rows labelled Tree 1, Tree 2, Tree 3 each show the same seven cards but only three are highlighted (cyan/violet/orange respectively), the rest greyed out. Tree 1 highlights file_entropy, packer_detected, code_section_size; Tree 2 highlights virtual_size_ratio, num_imports, num_sections; Tree 3 highlights file_entropy, suspicious_strings, num_imports. To the right of each row a coloured arrow points to the chosen split feature.">
  <div class="vis-caption">Three trees, three random feature subsets at the same node. Even when one feature is genuinely strong, different trees pick different splits — that diversity is the forest's variance reducer.</div>
</div>

---

## Concept: Single Tree vs Forest

| Property | Single Tree | Random Forest |
|---------|------------|---------------|
| Training accuracy | ~100% (overfits) | ~100% (also overfits, but ensemble averages it out) |
| Test accuracy | ~87% | ~94% |
| Interpretability | High — readable rules | Low — cannot read 100 trees |
| Stability | Low — different seeds → very different trees | High — ensemble is stable |
| Feature importance | Unstable (single tree dependent) | Stable (averaged over 100 trees) |

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_tree_vs_forest.png" alt="Grouped bar chart comparing Single Tree (red) and Random Forest (cyan) on two metrics: Train accuracy and Test accuracy. Both Single Tree and Random Forest reach 1.000 on Train. On Test the Single Tree drops to 0.867 while the Random Forest holds 0.940. A dotted line marks the OOB score of 0.930. Title: Both fit the train set — only the forest holds up on test.">
  <div class="vis-caption">Same data, same hyperparameters apart from <code>n_estimators</code>. Both fit the train set perfectly, but only the forest survives the jump to test.</div>
</div>

---

## What Each Task Asks You to Do

### Task 1 — Train the Random Forest
Train `RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)`. Print training accuracy, test accuracy, and OOB score.

### Task 2 — Compare Single Tree vs Forest
Print a side-by-side table comparing a single unlimited tree vs the random forest on: training accuracy, test accuracy, OOB score (if available).

### Task 3 — Classification Report
Print `classification_report` for the forest predictions on the test set. Focus on recall for the malware class.

### Task 4 (BONUS) — Predict Probabilities
Use `predict_proba()` to get P(malware) for each test sample. Print the 5 samples with the highest malware probability that were actually benign (i.e., potential false positives) and the 5 actual malware with the lowest P(malware) (hardest-to-detect malware).

---

## Expected Outputs

```
TASK 1 — Random forest:
Training accuracy: 1.000
Test accuracy:     0.940
OOB score:         0.930

TASK 2 — Comparison:
Model               Train Acc  Test Acc   OOB
Single Tree (none)    1.000     0.867     N/A
Random Forest (100)   1.000     0.940     0.930

TASK 3 — Classification report:
              precision  recall  f1-score  support
benign           0.94      0.94     0.94      300
malware          0.94      0.94     0.94      300
accuracy                            0.94      600

TASK 4 (BONUS):
Top 5 false positives (benign files most like malware):
  file_entropy=7.1, has_packer_sig=1, P(malware)=0.91
  ...
Top 5 hard-to-detect malware (lowest P(malware)):
  file_entropy=5.6, has_packer_sig=0, P(malware)=0.34
  ...
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| `n_jobs=1` (default) | Training 100 trees is slow | Use `n_jobs=-1` to use all cores |
| Forgetting `random_state` | Non-reproducible results | Always set `random_state=42` |
| Confusing OOB score with training score | OOB is an out-of-sample estimate | OOB ≈ test score; training score ≈ 1.0 |
| Using `max_features=None` (all features) | Trees become identical (no diversity) | Use 'sqrt' or 'log2' |
