# Lesson 2.2 — Workshop Guide
## Malware vs Benign PE File Classifier with Random Forests

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_from_tree_to_forest.py`)

## What This Workshop Covers

You will build a random forest classifier that distinguishes malware from benign PE (Portable Executable) files using static analysis features — file entropy, section count, imported functions, etc. You will see why a single decision tree overfits, how bagging solves this, and how to tune the forest size and feature selection.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_from_tree_to_forest.md](01_guide_from_tree_to_forest.md) | [01_lab_from_tree_to_forest.md](01_lab_from_tree_to_forest.md) | Single tree overfitting demo, bagging concept |
| 2 | [02_guide_train_random_forest.md](02_guide_train_random_forest.md) | [02_lab_train_random_forest.md](02_lab_train_random_forest.md) | RandomForestClassifier, oob_score, tree vs forest accuracy |
| 3 | [03_guide_feature_importance.md](03_guide_feature_importance.md) | [03_lab_feature_importance.md](03_lab_feature_importance.md) | Stable importances, single tree vs forest stability |
| 4 | [04_guide_tune_the_forest.md](04_guide_tune_the_forest.md) | [04_lab_tune_the_forest.md](04_lab_tune_the_forest.md) | n_estimators sweep, max_features, learning curve |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson2_random_forests/workshop/01_solution_from_tree_to_forest.py
```

## Next Lesson

[Lesson 2.3 — Clustering and Anomaly Detection](../../lesson3_clustering_anomaly/workshop/00_overview.md)
