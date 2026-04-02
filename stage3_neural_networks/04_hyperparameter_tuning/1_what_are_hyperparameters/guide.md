# Exercise 1 — What Are Hyperparameters?

> Read this guide fully before opening the lab.

## What You Will Learn

- The distinction between model parameters (weights that change during training) and hyperparameters (settings that you control)
- How to inspect actual weight values before and after training
- What a complete hyperparameter inventory looks like for a Keras model
- Why setting random seeds is important for reproducible experiments

---

## Concept: Parameters vs Hyperparameters

**Parameters** (also called weights or model weights):
- Stored inside the model in `layer.weights`
- Start as small random numbers
- Updated every batch by the optimizer (gradient descent)
- You do NOT set these — training adjusts them automatically

**Hyperparameters**:
- Set by YOU before any training happens
- Cannot be learned by gradient descent — they define the training process
- Wrong choices → slow convergence, failure to train, or overfitting

```
You set (hyperparameters):
  Dense(64)          ← 64 units
  activation='relu'  ← relu activation
  lr = 0.001         ← learning rate
  epochs = 20        ← how long to train
  batch_size = 32    ← how many samples per gradient update

Training learns (parameters):
  Layer 1 weights: shape (10, 64) = 640 values
  Layer 1 biases:  shape (64,)    =  64 values
  Layer 2 weights: ...
```

```
┌──────────────────────────────────────────────────────────┐
│                   YOU DECIDE                             │
│  (hyperparameters — fixed before training)               │
│                                                          │
│  units=64, lr=0.001, batch_size=32, epochs=20            │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  model.fit()   │  ← training loop
              └───────┬────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│                TRAINING LEARNS                           │
│  (parameters — updated every batch by gradient descent)  │
│                                                          │
│  W1: 640 values, b1: 64 values, W2: 65 values, ...       │
└──────────────────────────────────────────────────────────┘
```

---

## Concept: Complete Hyperparameter Inventory

| Category | Hyperparameter | Typical range |
|----------|---------------|---------------|
| Architecture | n_hidden_layers | 1-5 |
| Architecture | units per layer | 8-512 |
| Architecture | activation (hidden) | relu, elu, tanh |
| Architecture | activation (output) | sigmoid, softmax |
| Regularisation | dropout_rate | 0.1-0.5 |
| Regularisation | L2 weight decay | 0-0.01 |
| Optimizer | learning_rate | 0.0001-0.1 |
| Training | batch_size | 16-2048 |
| Training | epochs | 10-500 |

Hyperparameter tuning = choosing the best combination from this space.

> **Want to go deeper?** [Hyperparameter optimisation (Wikipedia)](https://en.wikipedia.org/wiki/Hyperparameter_optimization)

---

## What Each Task Asks You to Do

### Task 1 — Weights Before and After Training
Build a tiny model. Print `model.layers[0].get_weights()[0]` — the first layer's weight matrix — before and after training. Confirm the values changed. The amount of change reflects how much was learned.

### Task 2 — Hyperparameter Inventory
Print a formatted table categorising all hyperparameters for your model. This gives you a complete mental map of what you're in control of.

### Task 3 — Two Different Hyperparameter Choices
Train Model A (tiny, low lr) and Model B (larger, higher lr). Compare final test accuracy. Same data, different hyperparameters → different results.

### Task 4 (BONUS) — Reproducibility
Train the same model twice without a seed — results differ slightly. Then train twice with a seed — identical. Random seeds are essential for honest hyperparameter comparison experiments.

---

## Common Mistakes

- **Confusing "parameters" with "hyperparameters" in documentation**: Keras docs often use "params" to mean the learned weights. Hyperparameters are always specified by the user in the function call.
- **Using `.weights` without calling `.get_weights()`**: `layer.weights` returns TensorFlow Variable objects, not numpy arrays. Use `layer.get_weights()[0]` to get a numpy array you can print and manipulate.

---

## Now Open the Lab

[lab.md](lab.md)

## Next

[../2_learning_rate_sensitivity/guide.md](../2_learning_rate_sensitivity/guide.md)
