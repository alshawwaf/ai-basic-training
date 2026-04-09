# Feature Importance

> Back to [README.md](README.md)

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_importance_stability.png" alt="Grouped horizontal bar chart. Each row is one PE feature; the red bar (single tree) is the std of that feature's importance across 20 seeds and the cyan bar (random forest) is the same std for the forest. Every feature shows a much shorter cyan bar than red bar. Bottom-right annotation: mean σ ratio approximately 7x more stable in the forest.">
  <div class="vis-caption">Per-feature standard deviation across 20 seeds. The cyan forest bars are dramatically shorter — that is what "stable importance" looks like in numbers.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_feature_importance_bars.png" alt="Horizontal bar chart of mean Gini importance across 20 random-forest runs on the lab PE dataset. Cyan bars sorted from largest to smallest with orange error bars showing the std across runs. Top features: num_imports about 0.19, num_exports 0.18, virtual_size_ratio 0.12, suspicious_strings 0.11, file_entropy 0.09, has_valid_signature 0.08, packer_detected 0.05, with the remaining six features below 0.04.">
  <div class="vis-caption">Real lab feature importances. Error bars are tiny because every one of the 20 forests rank-orders the features almost identically — that is the stability the ensemble buys you.</div>
</div>

> **Want to go deeper?** [Random forest (Wikipedia)](https://en.wikipedia.org/wiki/Random_forest)

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
TASK 1 — Feature importances (sorted, sum = 1.000):
num_imports          0.1887
num_exports          0.1788
virtual_size_ratio   0.1204
suspicious_strings   0.1144
file_entropy         0.0862
has_valid_signature  0.0805
packer_detected      0.0532
file_size_kb         0.0381
code_section_size    0.0353
num_sections         0.0282
uses_network_dlls    0.0247
uses_crypto_dlls     0.0258
has_debug_info       0.0257
Sum: 1.000

TASK 2 — Stability comparison (mean std across 20 seeds):
Single trees: ~0.014
Forests:      ~0.002
Forest importances are roughly 7x more stable

TASK 4 (BONUS):
Full model accuracy (13 features): 0.938
Top-4 model accuracy:              0.877
Drop: -0.061  (top-4 is leaner but loses 6 pts because the signal is spread across many weak features)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using single-tree importances for feature selection | Unstable; may discard important features | Use random forest importances |
| Forgetting to re-fit with new seed in stability test | All 20 runs produce the same result | Use `random_state=i` in the loop |
| Reporting importances without error bars | False confidence | Always show std or confidence interval |
