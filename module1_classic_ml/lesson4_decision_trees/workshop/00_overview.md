# Lesson 1.4 — Workshop Guide
## Network Traffic Classifier with Decision Trees

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_how_trees_make_decisions.py`)

## What This Workshop Covers

In this workshop you will build a decision tree classifier that identifies four types of network traffic: benign, port_scan, exfiltration, and DoS. You will learn how decision trees split data, how to read the rules the model learned, how to identify the most informative network features, and how to tune tree depth to avoid overfitting.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_how_trees_make_decisions.md](01_guide_how_trees_make_decisions.md) | [01_lab_how_trees_make_decisions.md](01_lab_how_trees_make_decisions.md) | The if/else concept, Gini impurity, information gain |
| 2 | [02_guide_train_and_read_the_tree.md](02_guide_train_and_read_the_tree.md) | [02_lab_train_and_read_the_tree.md](02_lab_train_and_read_the_tree.md) | DecisionTreeClassifier, plot_tree(), interpret rules |
| 3 | [03_guide_feature_importance.md](03_guide_feature_importance.md) | [03_lab_feature_importance.md](03_lab_feature_importance.md) | .feature_importances_, which network features matter most |
| 4 | [04_guide_depth_and_overfitting.md](04_guide_depth_and_overfitting.md) | [04_lab_depth_and_overfitting.md](04_lab_depth_and_overfitting.md) | max_depth sweep, train vs test accuracy, sweet spot |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson4_decision_trees/workshop/exercise1_how_trees_make_decisions.py
```

## Next Lesson

[Lesson 1.5 — Model Evaluation](../../lesson5_model_evaluation/workshop/00_overview.md)
