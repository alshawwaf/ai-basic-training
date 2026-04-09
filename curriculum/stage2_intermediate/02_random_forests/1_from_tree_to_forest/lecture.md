# From Tree to Forest

> Back to [README.md](README.md)

## What You Will Learn

- Why a single decision tree with no depth limit overfits dramatically
- What bagging (Bootstrap Aggregation) does and why it helps
- How averaging predictions from many trees reduces variance
- Why random forests outperform single trees on noisy data

---

## Concept: The Single Tree Overfit Problem

A single `DecisionTreeClassifier` with `max_depth=None` will grow until every training sample is perfectly classified — memorising noise, outliers, and peculiarities of the training set. On new data, those memorised patterns don't generalise.

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_overfit_gap.png" alt="Bar chart with two bars. Left green bar 'Training accuracy' reaches 1.000 with the value labelled. Right red bar 'Test accuracy' reaches 0.867 with the value labelled. An orange double-headed arrow between the two bar tops marks the overfit gap = 0.133. Title: Single DecisionTree with no depth limit memorises the training set.">
  <div class="vis-caption">Real lab numbers from <code>DecisionTreeClassifier(max_depth=None)</code> on the PE feature dataset. Training accuracy of 1.000 is the smoking gun — the tree has memorised noise, not learned a rule.</div>
</div>

> **Want to go deeper?** [Decision tree learning (Wikipedia)](https://en.wikipedia.org/wiki/Decision_tree_learning)

---

## Concept: Bootstrap Aggregation (Bagging)

Bagging creates diversity among trees:
1. Draw a **bootstrap sample** — randomly sample N rows from the training set *with replacement*
2. Train one tree on that sample
3. Repeat K times → K different trees, each slightly different
4. **Aggregate** predictions: majority vote (classification) or average (regression)

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_bagging_flow.png" alt="Top-down bagging flow diagram. A grey 'Training data (N rows)' box at the top. Four arrows point down to four cyan bootstrap sample boxes labelled Sample 1 to Sample K. Each bootstrap sample feeds a violet tree box (Tree 1 to Tree K). Each tree outputs a circle showing its individual prediction (1, 0, 1, 1) coloured green or red. Arrows from all four predictions converge on a black box at the bottom labelled 'Majority vote → final prediction = 1'.">
  <div class="vis-caption">The full bagging pipeline. K different bootstrap samples create K different trees; their majority vote becomes the ensemble's answer.</div>
</div>

Because each tree sees a different random subset, no single noisy point can dominate all trees. The ensemble averages out errors.

**Out-of-Bag (OOB) samples:** In each bootstrap sample, ~37% of training rows are *not* sampled. These "out-of-bag" samples can be used as a free validation set, giving an unbiased estimate of test performance without a separate hold-out set.

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_oob_concept.png" alt="Strip of 30 cells representing training rows. About two-thirds of the cells are coloured cyan (rows that landed in this tree's bootstrap sample) and one-third are orange (out-of-bag rows). A two-row legend explains the colours. A bottom caption reads: oob_score on the lab forest = 0.930, test = 0.940 — OOB tracks the held-out test score for free.">
  <div class="vis-caption">Each bootstrap leaves ≈ 37 % of rows untouched. Sklearn re-uses those orange rows as a free validation set — no separate hold-out needed.</div>
</div>

> **Want to go deeper?** [Random forest (Wikipedia)](https://en.wikipedia.org/wiki/Random_forest)

---

## Concept: Why Averaging Reduces Variance

If each tree makes an error with variance σ², but errors are independent:
- Averaging N trees → variance σ²/N
- Standard deviation √(σ²/N) = σ/√N

With 100 trees, the standard deviation of predictions is 10× smaller than a single tree. Random forests get the benefit of reduced variance while keeping the bias of individual trees similar.

<div class="lecture-visual">
  <img src="/static/lecture_assets/rf_variance_reduction.png" alt="Scatter plot with 20 points per series across the x-axis (run index 0 to 19). Red dots show single-tree test accuracy bouncing around 0.86 with visible spread. Cyan dots show random-forest test accuracy clustered tightly at 0.94. Two horizontal dashed lines mark the means. Top-left annotation: σ ratio — single tree is roughly 2x more variable.">
  <div class="vis-caption">Re-train 20 times with different seeds. Single trees scatter; the forests cluster near the same accuracy. That tight cluster <em>is</em> the variance reduction the math predicted.</div>
</div>

---

## What Each Task Asks You to Do

### Task 1 — Single Tree with No Limit
Train `DecisionTreeClassifier(max_depth=None)` on the PE file dataset. Print training and test accuracy. Calculate the overfit gap.

### Task 2 — Manual Bagging Demo
Without using RandomForest, manually create 10 bootstrap samples from the training data, train a tree on each, and average their predictions. Compare accuracy to the single unlimited tree.

### Task 3 — Show the Variance Reduction
Train 20 individual unlimited trees, each on a different random seed. Record their test accuracies. Compute mean and std. Then do the same with 20 different random forests (n_estimators=100). Show that the std of forest accuracies is much smaller.

### Task 4 (BONUS) — OOB Score
Train a `RandomForestClassifier(oob_score=True)`. Print `model.oob_score_` and compare it to the actual test accuracy. Verify that OOB is a reliable estimate.

---

## Expected Outputs

```
TASK 1 — Single unlimited tree:
Training accuracy: 1.000
Test accuracy:     0.867
Overfit gap:       0.133

TASK 2 — Manual bagging (10 trees):
Manual bagging test accuracy: 0.917  <- better than single tree!
Single tree test accuracy:    0.867
Improvement from bagging:    +0.050

TASK 3 — Variance comparison:
20 single trees:   mean=0.865, std=0.007  <- baseline
20 random forests: mean=0.940, std=0.003  <- much more stable
Variance ratio: 2.3x higher for single trees

TASK 4 (BONUS) — OOB score:
OOB score:    0.930
Test score:   0.940
Difference:   0.010  <- OOB is a reliable proxy for test performance
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `max_depth=None` in production | Overfitting, poor generalisation | Always set a depth limit or use random forest |
| Forgetting `replace=True` in bootstrap | Sampling without replacement = different dataset, not bootstrap | Use `np.random.choice(..., replace=True)` |
| Comparing OOB to training accuracy | OOB should compare to TEST accuracy | OOB approximates test set performance |
| Using too few trees (n_estimators=5) | High variance remains | Use at least 100; check learning curve in Exercise 4 |
