# Lesson 2.4 — Workshop Guide
## Overfitting and Cross-Validation

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_overfitting_demo.py`)

## What This Workshop Covers

You will deeply understand overfitting by watching a decision tree's train-vs-test accuracy diverge as depth increases, visualise the bias-variance tradeoff with three concrete models, then use k-fold cross-validation to get more reliable performance estimates than a single train/test split.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_overfitting_demo.md](01_guide_overfitting_demo.md) | [01_lab_overfitting_demo.md](01_lab_overfitting_demo.md) | Sweep tree depth, watch train vs val accuracy diverge |
| 2 | [02_guide_bias_variance.md](02_guide_bias_variance.md) | [02_lab_bias_variance.md](02_lab_bias_variance.md) | Underfit vs good fit vs overfit — visualise all three |
| 3 | [03_guide_kfold_crossval.md](03_guide_kfold_crossval.md) | [03_lab_kfold_crossval.md](03_lab_kfold_crossval.md) | cross_val_score, 5-fold vs 10-fold, variance reduction |
| 4 | [04_guide_validation_curve.md](04_guide_validation_curve.md) | [04_lab_validation_curve.md](04_lab_validation_curve.md) | validation_curve(), automatic parameter sweep, plot |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson4_overfitting_crossval/workshop/01_solution_overfitting_demo.py
```

## Next Lesson

[Module 3 — Neural Networks](../../../module3_neural_networks/lesson9_first_neural_network/workshop/00_overview.md)
