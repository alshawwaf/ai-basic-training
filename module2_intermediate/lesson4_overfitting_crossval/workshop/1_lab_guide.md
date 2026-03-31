# Lesson 2.4 — Workshop Guide
## Overfitting and Cross-Validation

> Read first: [../4_overfitting_cross_validation.md](../4_overfitting_cross_validation.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will deeply understand overfitting by watching a decision tree's train-vs-test accuracy diverge as depth increases, visualise the bias-variance tradeoff with three concrete models, then use k-fold cross-validation to get more reliable performance estimates than a single train/test split.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_overfitting_demo.md](exercise1_overfitting_demo.md) | [exercise1_overfitting_demo.py](exercise1_overfitting_demo.py) | Sweep tree depth, watch train vs val accuracy diverge |
| 2 | [exercise2_bias_variance.md](exercise2_bias_variance.md) | [exercise2_bias_variance.py](exercise2_bias_variance.py) | Underfit vs good fit vs overfit — visualise all three |
| 3 | [exercise3_kfold_crossval.md](exercise3_kfold_crossval.md) | [exercise3_kfold_crossval.py](exercise3_kfold_crossval.py) | cross_val_score, 5-fold vs 10-fold, variance reduction |
| 4 | [exercise4_validation_curve.md](exercise4_validation_curve.md) | [exercise4_validation_curve.py](exercise4_validation_curve.py) | validation_curve(), automatic parameter sweep, plot |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson4_overfitting_crossval/workshop/exercise1_overfitting_demo.py
```

## Next Lesson

[Module 3 — Neural Networks](../../../module3_neural_networks/lesson9_first_neural_network/workshop/1_lab_guide.md)
