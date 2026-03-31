# Lesson 3.12 — Workshop Guide
## Hyperparameter Tuning

> **Read first:** [../12_hyperparameter_tuning.md](../12_hyperparameter_tuning.md)
> **Reference solution:** [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will develop an empirical intuition for the most important neural network hyperparameters. Starting from the distinction between learned weights and user-specified hyperparameters, you will experiment with learning rate, batch size, and architecture search — observing how each affects training speed, stability, and final accuracy. Each exercise is self-contained so you can run them in any order after Exercise 1.

This workshop reuses the same synthetic binary classification dataset from Lessons 3.9-3.10.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_what_are_hyperparameters.md](exercise1_what_are_hyperparameters.md) | [exercise1_what_are_hyperparameters.py](exercise1_what_are_hyperparameters.py) | Parameters vs hyperparameters; before/after weight inspection |
| 2 | [exercise2_learning_rate_sensitivity.md](exercise2_learning_rate_sensitivity.md) | [exercise2_learning_rate_sensitivity.py](exercise2_learning_rate_sensitivity.py) | lr=0.001 vs 0.01 vs 0.1 — convergence, divergence, slow learning |
| 3 | [exercise3_batch_size_effects.md](exercise3_batch_size_effects.md) | [exercise3_batch_size_effects.py](exercise3_batch_size_effects.py) | batch_size=32 vs 256 vs 1024 — gradient noise vs stability |
| 4 | [exercise4_architecture_search.md](exercise4_architecture_search.md) | [exercise4_architecture_search.py](exercise4_architecture_search.py) | Manual grid search over units×layers, store results in DataFrame |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson12_hyperparameter_tuning/workshop/exercise1_what_are_hyperparameters.py
```

## Tips

- Exercise 4 trains multiple models (up to 9) — it may take 2-5 minutes total
- Use `verbose=0` in model.fit() inside loops to avoid cluttering the terminal
- Results will vary slightly between runs due to random weight initialisation — this is expected

## After This Workshop

Move to [Module 4 — Generative AI](../../../module4_genai/lesson1_how_llms_work/workshop/1_lab_guide.md)
