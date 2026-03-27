# Lesson 3.4 — Hyperparameters & Tuning

**Script:** [4_hyperparameters.py](4_hyperparameters.py)

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

## Next: Milestone Project

**[milestone_packets.py](milestone_packets.py):** Full neural network pipeline on network packet data with proper tuning.
