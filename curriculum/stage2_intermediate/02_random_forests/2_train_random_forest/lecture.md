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

```
All 7 features: [entropy, packer, vsize, imports, imp_ent, code_sz, sections]

At each split, each tree picks a RANDOM subset of sqrt(7) ~ 3 features:

Tree 1, node A:  picks [entropy, packer, code_sz]  ───► splits on entropy
Tree 2, node A:  picks [vsize, imports, sections]   ───► splits on vsize
Tree 3, node A:  picks [entropy, imp_ent, imports]  ───► splits on entropy

Result: trees make DIFFERENT splits ───► diverse, uncorrelated predictions
```

For 7 features: √7 ≈ 2.6 → 2 or 3 features considered at each node. This is small enough to create diversity but large enough to use the good features most of the time.

---

## Concept: Single Tree vs Forest

| Property | Single Tree | Random Forest |
|---------|------------|---------------|
| Training accuracy | ~100% (overfits) | ~99% (also overfits, but ensemble averages it out) |
| Test accuracy | ~89% | ~94% |
| Interpretability | High — readable rules | Low — cannot read 100 trees |
| Stability | Low — different seeds → very different trees | High — ensemble is stable |
| Feature importance | Unstable (single tree dependent) | Stable (averaged over 100 trees) |

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
Training accuracy: 0.999
Test accuracy:     0.943
OOB score:         0.941

TASK 2 — Comparison:
Model               Train Acc  Test Acc   OOB
Single Tree (none)    1.000     0.891     N/A
Random Forest (100)   0.999     0.943     0.941

TASK 3 — Classification report:
              precision  recall  f1-score  support
benign          0.948     0.941     0.944      200
malware         0.939     0.945     0.942      200
accuracy                            0.943      400

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

---

> Next: [../3_feature_importance/lecture.md](../3_feature_importance/lecture.md)
