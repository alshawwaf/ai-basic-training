# Lesson 3.10 — Workshop Guide
## Dropout and Regularisation

> **Read first:** [../10_dropout_and_regularisation.md](../10_dropout_and_regularisation.md)
> **Reference solution:** [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will deliberately overfit a large neural network to see the problem clearly, then apply three regularisation techniques one by one: Dropout, Batch Normalisation, and Early Stopping. Each exercise isolates one technique so you can measure its effect directly. By the end you will have a regularised model that generalises well and stops training automatically at the right moment.

This workshop reuses the same synthetic binary classification dataset from Lesson 3.9 (10 features, 90/10 class imbalance). Import and setup code is provided in each exercise file — do not modify it.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_demonstrate_overfitting.md](exercise1_demonstrate_overfitting.md) | [exercise1_demonstrate_overfitting.py](exercise1_demonstrate_overfitting.py) | Build large unregularised network, plot diverging loss |
| 2 | [exercise2_add_dropout.md](exercise2_add_dropout.md) | [exercise2_add_dropout.py](exercise2_add_dropout.py) | Add Dropout(0.3), compare val loss to exercise 1 |
| 3 | [exercise3_batch_normalisation.md](exercise3_batch_normalisation.md) | [exercise3_batch_normalisation.py](exercise3_batch_normalisation.py) | BatchNormalization, smoother curves, combine with Dropout |
| 4 | [exercise4_early_stopping.md](exercise4_early_stopping.md) | [exercise4_early_stopping.py](exercise4_early_stopping.py) | EarlyStopping callback, patience, restore_best_weights |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson10_dropout_regularisation/workshop/exercise1_demonstrate_overfitting.py
```

## Tips

- Training 50 epochs on a large network takes 5-15 seconds — be patient
- Overfitting may not always be dramatic on this synthetic dataset — look for any increasing val_loss trend
- Random seed is set for reproducibility but some variance in results is expected

## After This Workshop

Move to [Lesson 3.11 — Convolutional Networks](../../lesson11_convolutional_networks/workshop/1_lab_guide.md)
