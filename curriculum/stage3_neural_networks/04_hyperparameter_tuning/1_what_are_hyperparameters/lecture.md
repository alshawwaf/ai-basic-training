# What Are Hyperparameters?

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

**Two clearly separated buckets**

| Owned by | Examples | When set | How they change |
|---|---|---|---|
| **You** (hyperparameters) | `units=64`, `lr=0.001`, `batch_size=32`, `epochs=20` | **before** `model.fit()` | only when you re-run training with new values |
| **Training loop** (parameters) | `W1`: 640 values, `b1`: 64 values, `W2`: 65 values, … | **inside** `model.fit()` | updated by gradient descent on every batch |

You wire up the training process; the training process fills in the weights. Hyperparameter tuning means *systematically* trying different "you decide" combinations and measuring which one produces the best learned weights.

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_params_vs_hyperparams.png" alt="Two side-by-side rounded boxes. Left orange-bordered box titled 'YOU set (hyperparameters)' with subtitle 'before model.fit() — define the training' lists six monospace lines: units=64, learning_rate=0.001, batch_size=32, epochs=20, activation='relu', dropout_rate=0.3. Right cyan-bordered box titled 'TRAINING learns (parameters)' with subtitle 'inside model.fit() — gradient descent' lists six monospace lines describing W1, b1, W2, b2, W3, b3 weight and bias shapes. A small italic caption between them reads 'you wire it up → training fills it in'.">
  <div class="vis-caption">The two buckets in one picture. Everything on the left side is a knob you set. Everything on the right side is filled in automatically by gradient descent. Hyperparameter tuning is the practice of systematically searching the left side to find the combination that produces the best right side.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_weights_before_after.png" alt="Three heatmaps side by side, each showing the (20, 64) weight matrix of the first Dense layer using a red-blue diverging colormap. Left titled 'Layer 1 weights — BEFORE training' shows mostly small noisy values centred around zero. Middle titled 'AFTER 20 epochs' shows a clearly different pattern with stronger reds and blues in specific cells. Right titled 'Δ = AFTER − BEFORE (what was learned)' shows the difference — a structured pattern of changes concentrated on specific input features.">
  <div class="vis-caption">Real weight snapshots from a 20-epoch training run. The left grid is what the layer started with (small random numbers). The middle grid is what training discovered. The right grid shows the difference — that pattern <em>is</em> what "learning" looks like at the parameter level.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_inventory.png" alt="Three coloured columns side by side, each a category of hyperparameters. Cyan column 'Architecture' lists n_hidden_layers 1-5, units_per_layer 8-512, activation hidden relu/elu/tanh, activation out sigmoid/softmax. Violet column 'Regularisation' lists dropout_rate 0.1-0.5, L2 weight decay 0-0.01, early stopping patience 3-10, data augmentation yes/no. Orange column 'Optimiser & Training' lists optimizer Adam/SGD/RMSProp, learning_rate 1e-4 to 1e-1, batch_size 16-2048, epochs 10-500.">
  <div class="vis-caption">The full hyperparameter inventory grouped into three categories. Architecture decides what the model looks like; Regularisation decides how it resists overfitting; Optimiser & Training decide how it learns. Tuning means walking through this space and measuring which combinations work best on validation data.</div>
</div>

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
