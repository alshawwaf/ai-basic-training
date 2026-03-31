# Exercise 3 — Feature Importance

> Back to [1_lab_guide.md](1_lab_guide.md)
> Exercise file: [exercise3_feature_importance.py](exercise3_feature_importance.py)

## What You Will Learn

- How random forest feature importances are more stable than single-tree importances
- Which PE file features are most predictive of malware
- How to measure importance stability across multiple training runs
- How to use importances for feature selection

---

## Concept: Stability of Feature Importances

A single decision tree's feature importance depends heavily on which training sample it saw. Two trees trained with different random seeds can produce very different importance rankings.

A random forest averages importances over 100 trees, each trained on a different bootstrap sample. This produces a stable ranking — retrain with a different seed and the top features remain roughly the same.

**Measuring stability:**
Train the model 20 times with different seeds. For each feature, compute the std of its importance across runs. A small std means the feature's importance is consistent and trustworthy.

---

## Concept: PE File Feature Interpretation

| Feature | High value in malware | Security reason |
|---------|----------------------|-----------------|
| `file_entropy` | ~7.2 (near maximum) | Packed/encrypted malware has high entropy |
| `has_packer_sig` | 68% vs 5% for benign | Packers are used to evade AV detection |
| `virtual_size_ratio` | ~2.8 (large unpacked sections) | Malware unpacks itself in memory |
| `import_entropy` | Lower — fewer, specific imports | Malware uses targeted API calls (e.g., CreateRemoteThread) |
| `num_imports` | Lower — fewer imports | Malware minimises its import table to evade static analysis |

---

## What Each Task Asks You to Do

### Task 1 — Print Forest Feature Importances
Extract and print sorted feature importances from a trained random forest. Verify they sum to 1.0.

### Task 2 — Stability: Single Tree vs Forest
Train 20 single trees and 20 random forests. For each, compute feature importance for every feature. Report std of importance across 20 runs for both. Show forest is more stable.

### Task 3 — Top Features Bar Chart
Create a horizontal bar chart of sorted feature importances with error bars showing std across 20 forest runs.

### Task 4 (BONUS) — Feature Selection
Keep only the top 4 features. Retrain the forest. Compare accuracy to the full-feature model.

---

## Expected Outputs

```
TASK 1 — Feature importances:
file_entropy        0.382
has_packer_sig      0.241
virtual_size_ratio  0.178
import_entropy      0.089
num_imports         0.058
code_section_size   0.031
num_sections        0.021
Sum: 1.000 ✓

TASK 2 — Stability comparison:
Feature              Tree Std   Forest Std
file_entropy         0.042       0.004
has_packer_sig       0.038       0.003
...

TASK 4 (BONUS):
Top-4 model accuracy: 0.940  (vs full model 0.943 — drop of 0.003)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using single-tree importances for feature selection | Unstable; may discard important features | Use random forest importances |
| Forgetting to re-fit with new seed in stability test | All 20 runs produce the same result | Use `random_state=i` in the loop |
| Reporting importances without error bars | False confidence | Always show std or confidence interval |

---

> Next: [exercise4_tune_the_forest.md](exercise4_tune_the_forest.md)
