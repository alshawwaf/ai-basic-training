# Lesson 1.4 — Workshop Guide
## Network Traffic Classifier with Decision Trees

> Read first: [../4_decision_trees.md](../4_decision_trees.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

In this workshop you will build a decision tree classifier that identifies four types of network traffic: benign, port_scan, exfiltration, and DoS. You will learn how decision trees split data, how to read the rules the model learned, how to identify the most informative network features, and how to tune tree depth to avoid overfitting.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_how_trees_make_decisions.md](exercise1_how_trees_make_decisions.md) | [exercise1_how_trees_make_decisions.py](exercise1_how_trees_make_decisions.py) | The if/else concept, Gini impurity, information gain |
| 2 | [exercise2_train_and_read_the_tree.md](exercise2_train_and_read_the_tree.md) | [exercise2_train_and_read_the_tree.py](exercise2_train_and_read_the_tree.py) | DecisionTreeClassifier, plot_tree(), interpret rules |
| 3 | [exercise3_feature_importance.md](exercise3_feature_importance.md) | [exercise3_feature_importance.py](exercise3_feature_importance.py) | .feature_importances_, which network features matter most |
| 4 | [exercise4_depth_and_overfitting.md](exercise4_depth_and_overfitting.md) | [exercise4_depth_and_overfitting.py](exercise4_depth_and_overfitting.py) | max_depth sweep, train vs test accuracy, sweet spot |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson4_decision_trees/workshop/exercise1_how_trees_make_decisions.py
```

## Next Lesson

[Lesson 1.5 — Model Evaluation](../../lesson5_model_evaluation/workshop/1_lab_guide.md)
