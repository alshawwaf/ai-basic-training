# Lesson 2.2 — Workshop Guide
## Malware vs Benign PE File Classifier with Random Forests

> Read first: [../2_random_forests.md](../2_random_forests.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will build a random forest classifier that distinguishes malware from benign PE (Portable Executable) files using static analysis features — file entropy, section count, imported functions, etc. You will see why a single decision tree overfits, how bagging solves this, and how to tune the forest size and feature selection.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_from_tree_to_forest.md](exercise1_from_tree_to_forest.md) | [exercise1_from_tree_to_forest.py](exercise1_from_tree_to_forest.py) | Single tree overfitting demo, bagging concept |
| 2 | [exercise2_train_random_forest.md](exercise2_train_random_forest.md) | [exercise2_train_random_forest.py](exercise2_train_random_forest.py) | RandomForestClassifier, oob_score, tree vs forest accuracy |
| 3 | [exercise3_feature_importance.md](exercise3_feature_importance.md) | [exercise3_feature_importance.py](exercise3_feature_importance.py) | Stable importances, single tree vs forest stability |
| 4 | [exercise4_tune_the_forest.md](exercise4_tune_the_forest.md) | [exercise4_tune_the_forest.py](exercise4_tune_the_forest.py) | n_estimators sweep, max_features, learning curve |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson2_random_forests/workshop/exercise1_from_tree_to_forest.py
```

## Next Lesson

[Lesson 2.3 — Clustering and Anomaly Detection](../../lesson3_clustering_anomaly/workshop/1_lab_guide.md)
