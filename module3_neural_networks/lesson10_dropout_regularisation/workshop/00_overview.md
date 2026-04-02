# Lesson 3.10 — Workshop Guide
## Dropout and Regularisation

> **Read first:** [../notes.md](../notes.md)
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_demonstrate_overfitting.py`) — open only after finishing the exercise

## What This Workshop Covers

You will deliberately overfit a large neural network to see the problem clearly, then apply three regularisation techniques one by one: Dropout, Batch Normalisation, and Early Stopping. Each exercise isolates one technique so you can measure its effect directly. By the end you will have a regularised model that generalises well and stops training automatically at the right moment.

This workshop reuses the same synthetic binary classification dataset from Lesson 3.9 (10 features, 90/10 class imbalance). Import and setup code is provided in each exercise — do not modify it.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_demonstrate_overfitting.md](01_guide_demonstrate_overfitting.md) | [01_lab_demonstrate_overfitting.md](01_lab_demonstrate_overfitting.md) | Build large unregularised network, plot diverging loss |
| 2 | [02_guide_add_dropout.md](02_guide_add_dropout.md) | [02_lab_add_dropout.md](02_lab_add_dropout.md) | Add Dropout(0.3), compare val loss to exercise 1 |
| 3 | [03_guide_batch_normalisation.md](03_guide_batch_normalisation.md) | [03_lab_batch_normalisation.md](03_lab_batch_normalisation.md) | BatchNormalization, smoother curves, combine with Dropout |
| 4 | [04_guide_early_stopping.md](04_guide_early_stopping.md) | [04_lab_early_stopping.md](04_lab_early_stopping.md) | EarlyStopping callback, patience, restore_best_weights |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson10_dropout_regularisation/workshop/01_solution_demonstrate_overfitting.py
```

## Tips

- Training 50 epochs on a large network takes 5-15 seconds — be patient
- Overfitting may not always be dramatic on this synthetic dataset — look for any increasing val_loss trend
- Random seed is set for reproducibility but some variance in results is expected

## After This Workshop

Move to [Lesson 3.11 — Convolutional Networks](../../lesson11_convolutional_networks/workshop/00_overview.md)
