# Exercise 1 — From Tree to Forest

> Back to [00_overview.md](00_overview.md)

## What You Will Learn

- Why a single decision tree with no depth limit overfits dramatically
- What bagging (Bootstrap Aggregation) does and why it helps
- How averaging predictions from many trees reduces variance
- Why random forests outperform single trees on noisy data

---

## Concept: The Single Tree Overfit Problem

A single `DecisionTreeClassifier` with `max_depth=None` will grow until every training sample is perfectly classified — memorising noise, outliers, and peculiarities of the training set. On new data, those memorised patterns don't generalise.

**Visualising the problem:**
```
Single tree (no limit):
  Training accuracy: 1.000   (perfect — but suspicious!)
  Test accuracy:     0.891   (gap of 0.109 = overfitting)
```

> **Want to go deeper?** [Decision tree learning (Wikipedia)](https://en.wikipedia.org/wiki/Decision_tree_learning)

---

## Concept: Bootstrap Aggregation (Bagging)

Bagging creates diversity among trees:
1. Draw a **bootstrap sample** — randomly sample N rows from the training set *with replacement*
2. Train one tree on that sample
3. Repeat K times → K different trees, each slightly different
4. **Aggregate** predictions: majority vote (classification) or average (regression)

Because each tree sees a different random subset, no single noisy point can dominate all trees. The ensemble averages out errors.

**Out-of-Bag (OOB) samples:** In each bootstrap sample, ~37% of training rows are *not* sampled. These "out-of-bag" samples can be used as a free validation set, giving an unbiased estimate of test performance without a separate hold-out set.

> **Want to go deeper?** [Random forest (Wikipedia)](https://en.wikipedia.org/wiki/Random_forest)

---

## Concept: Why Averaging Reduces Variance

If each tree makes an error with variance σ², but errors are independent:
- Averaging N trees → variance σ²/N
- Standard deviation √(σ²/N) = σ/√N

With 100 trees, the standard deviation of predictions is 10× smaller than a single tree. Random forests get the benefit of reduced variance while keeping the bias of individual trees similar.

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
Test accuracy:     0.891
Overfit gap:       0.109

TASK 2 — Manual bagging (10 trees):
Test accuracy: 0.931  ← better than single tree!

TASK 3 — Variance comparison:
20 single trees:  mean=0.888, std=0.031  ← high variance!
20 random forests: mean=0.943, std=0.005 ← much more stable

TASK 4 (BONUS) — OOB score:
OOB score:   0.941
Test score:  0.943
Difference:  0.002  ← OOB is a reliable proxy for test performance
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `max_depth=None` in production | Overfitting, poor generalisation | Always set a depth limit or use random forest |
| Forgetting `replace=True` in bootstrap | Sampling without replacement = different dataset, not bootstrap | Use `np.random.choice(..., replace=True)` |
| Comparing OOB to training accuracy | OOB should compare to TEST accuracy | OOB approximates test set performance |
| Using too few trees (n_estimators=5) | High variance remains | Use at least 100; check learning curve in Exercise 4 |

---

> Next: [02_guide_train_random_forest.md](02_guide_train_random_forest.md)
