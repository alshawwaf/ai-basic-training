# Lesson 1.5 — Workshop Guide
## Model Evaluation on Imbalanced Security Data

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_the_accuracy_trap.py`)

## What This Workshop Covers

In this workshop you will discover why accuracy is a dangerous metric for imbalanced security datasets, build a complete evaluation toolkit (confusion matrix, precision, recall, F1, ROC/AUC), and learn how to tune decision thresholds based on operational priorities. The dataset has a 5% attack rate — a realistic proportion for many security monitoring scenarios.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_the_accuracy_trap.md](01_guide_the_accuracy_trap.md) | [01_lab_the_accuracy_trap.md](01_lab_the_accuracy_trap.md) | DummyClassifier, 95% accuracy that catches 0 attacks |
| 2 | [02_guide_confusion_matrix.md](02_guide_confusion_matrix.md) | [02_lab_confusion_matrix.md](02_lab_confusion_matrix.md) | TP/TN/FP/FN for security, compute manually and with sklearn |
| 3 | [03_guide_precision_recall_f1.md](03_guide_precision_recall_f1.md) | [03_lab_precision_recall_f1.md](03_lab_precision_recall_f1.md) | Precision, recall, F1, security tradeoffs |
| 4 | [04_guide_roc_and_auc.md](04_guide_roc_and_auc.md) | [04_lab_roc_and_auc.md](04_lab_roc_and_auc.md) | ROC curve, AUC, compare three models |
| 5 | [05_guide_threshold_tuning.md](05_guide_threshold_tuning.md) | [05_lab_threshold_tuning.md](05_lab_threshold_tuning.md) | Threshold sensitivity, pick for use case |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson5_model_evaluation/workshop/exercise1_the_accuracy_trap.py
```

## Next Lesson

[Lesson 2.1 — Feature Engineering](../../module2_intermediate/lesson1_feature_engineering/workshop/00_overview.md)
