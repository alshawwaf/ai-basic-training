# Hyperparameters & Tuning

---

## Concept: The Knobs You Turn

Model parameters (weights and biases) are *learned* during training. **Hyperparameters** are the settings you choose *before* training. They control *how* the model learns.

Getting hyperparameters right is what separates a 75% model from a 95% model.

---

## Key Hyperparameters

### Learning Rate (most important)
Controls how big each weight update step is.

| Learning rate | Effect |
|--------------|--------|
| Too high | Loss oscillates, may diverge |
| Too low | Trains very slowly, may get stuck |
| Just right | Steady decrease in loss |

Common starting point: `0.001` (Adam default). Try: `[0.01, 0.001, 0.0001]`

### Number of Layers & Neurons
More layers = more capacity to learn complex patterns, but more risk of overfitting.

Rule of thumb: start small, add complexity only if the model is underfitting.

```
Start:    Dense(32) → Dense(16) → output
Add if needed: Dense(64) → Dense(32) → Dense(16) → output
```

### Batch Size
- Small batches (8–32): noisier updates, can escape local minima, slower per epoch
- Large batches (256–1024): stable updates, faster per epoch, may overfit

### Dropout Rate
- 0.1–0.2: light regularisation
- 0.3–0.5: strong regularisation (useful with limited data)

### Epochs + Early Stopping
Don't tune epochs manually. Use early stopping with `patience=10–20`.

---

## Systematic Tuning Approaches

### Manual tuning
Intuition-based: start with defaults, change one thing at a time.

### Grid search
Try all combinations of a pre-defined set. Expensive but thorough.

### Random search
Sample randomly from a hyperparameter space. Often better than grid search at the same budget.

### Keras Tuner (automated)
```bash
pip install keras-tuner
```
```python
import keras_tuner as kt

def build_model(hp):
    units = hp.Int('units', min_value=16, max_value=256, step=16)
    lr    = hp.Float('lr', min_value=1e-4, max_value=1e-2, sampling='log')
    ...
```

---

## What to Notice When You Run It

1. Learning rate sensitivity — compare loss curves for 0.01, 0.001, 0.0001
2. How batch size affects training stability (variance of the loss curve)
3. Which hyperparameter combination achieves the best validation AUC

---

## Next: Stage Project

**[packet_classifier.py](../project/packet_classifier.py):** Full neural network pipeline on network packet data with proper tuning.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

# Lesson 3.12 — Workshop Guide
## Hyperparameter Tuning

> **Read first:** [README.md](README.md)
> **Reference solutions:** Each exercise has a matching solution file (e.g. `1_what_are_hyperparameters/solution_hyperparameter_tuning.py`) — open only after finishing the exercise

## What This Workshop Covers

You will develop an empirical intuition for the most important neural network hyperparameters. Starting from the distinction between learned weights and user-specified hyperparameters, you will experiment with learning rate, batch size, and architecture search — observing how each affects training speed, stability, and final accuracy. Each exercise is self-contained so you can run them in any order after Exercise 1.

This workshop reuses the same synthetic binary classification dataset from Lessons 3.9-3.10.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_what_are_hyperparameters/lecture.md) | [handson.md](1_what_are_hyperparameters/handson.md) | Parameters vs hyperparameters; before/after weight inspection |
| 2 | [lecture.md](2_learning_rate_sensitivity/lecture.md) | [handson.md](2_learning_rate_sensitivity/handson.md) | lr=0.001 vs 0.01 vs 0.1 — convergence, divergence, slow learning |
| 3 | [lecture.md](3_batch_size_effects/lecture.md) | [handson.md](3_batch_size_effects/handson.md) | batch_size=32 vs 256 vs 1024 — gradient noise vs stability |
| 4 | [lecture.md](4_architecture_search/lecture.md) | [handson.md](4_architecture_search/handson.md) | Manual grid search over units×layers, store results in DataFrame |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage3_neural_networks/04_hyperparameter_tuning/1_what_are_hyperparameters/solution_hyperparameter_tuning.py
```

## Tips

- Exercise 4 trains multiple models (up to 9) — it may take 2-5 minutes total
- Use `verbose=0` in model.fit() inside loops to avoid cluttering the terminal
- Results will vary slightly between runs due to random weight initialisation — this is expected
