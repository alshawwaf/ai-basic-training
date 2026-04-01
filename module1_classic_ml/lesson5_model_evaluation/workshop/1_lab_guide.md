# Lesson 1.5 — Workshop Guide
## Model Evaluation on Imbalanced Security Data

> Read first: [../5_model_evaluation.md](../5_model_evaluation.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

In this workshop you will discover why accuracy is a dangerous metric for imbalanced security datasets, build a complete evaluation toolkit (confusion matrix, precision, recall, F1, ROC/AUC), and learn how to tune decision thresholds based on operational priorities. The dataset has a 5% attack rate — a realistic proportion for many security monitoring scenarios.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_the_accuracy_trap.md](exercise1_the_accuracy_trap.md) | [exercise1_the_accuracy_trap_lab.md](exercise1_the_accuracy_trap_lab.md) | DummyClassifier, 95% accuracy that catches 0 attacks |
| 2 | [exercise2_confusion_matrix.md](exercise2_confusion_matrix.md) | [exercise2_confusion_matrix_lab.md](exercise2_confusion_matrix_lab.md) | TP/TN/FP/FN for security, compute manually and with sklearn |
| 3 | [exercise3_precision_recall_f1.md](exercise3_precision_recall_f1.md) | [exercise3_precision_recall_f1_lab.md](exercise3_precision_recall_f1_lab.md) | Precision, recall, F1, security tradeoffs |
| 4 | [exercise4_roc_and_auc.md](exercise4_roc_and_auc.md) | [exercise4_roc_and_auc_lab.md](exercise4_roc_and_auc_lab.md) | ROC curve, AUC, compare three models |
| 5 | [exercise5_threshold_tuning.md](exercise5_threshold_tuning.md) | [exercise5_threshold_tuning_lab.md](exercise5_threshold_tuning_lab.md) | Threshold sensitivity, pick for use case |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson5_model_evaluation/workshop/exercise1_the_accuracy_trap.py
```

## Next Lesson

[Lesson 2.1 — Feature Engineering](../../module2_intermediate/lesson1_feature_engineering/workshop/1_lab_guide.md)
