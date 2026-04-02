# Exercise 3 — Batch Normalisation

> Read this guide fully before opening the lab.

## What You Will Learn

- How `BatchNormalization` normalises layer activations within each mini-batch
- Why BatchNorm stabilises training and produces smoother loss curves
- How to combine BatchNorm and Dropout in a single architecture
- How the placement of BatchNorm layers affects training behaviour

---

## Concept: Internal Covariate Shift

As training progresses, the weights in early layers change. This shifts the distribution of inputs to later layers, forcing them to constantly re-adapt. This is called **internal covariate shift**.

Example without BatchNorm:
```
Epoch 1:  layer 2 receives inputs with mean=0.5, std=1.2
Epoch 10: layer 2 now receives inputs with mean=2.1, std=3.8
Epoch 20: layer 2 now receives inputs with mean=-0.3, std=0.4
```

Layer 2 must continuously adjust to a moving target — slowing learning and causing instability.

---

## Concept: What BatchNorm Does

```python
keras.layers.BatchNormalization()
```

For each mini-batch, this layer:
1. Computes mean μ and variance σ² of each feature across the batch
2. Normalises: `z = (x - μ) / sqrt(σ² + ε)`
3. Applies learned scale γ and shift β: `output = γ·z + β`

The result: each layer always receives inputs with approximately mean=0 and std=1, regardless of what happened in earlier layers.

```
BatchNorm transformation (per feature, within one mini-batch):

 Before BN                  After BN
 (shifting distribution)    (stable, centred)

      __                         __
    /    \   mean=2.1          /    \   mean~0
   /      \  std=3.8          /      \  std~1
  /        \                 /        \
 /          \               /          \
─┼──────────┼──►         ──┼──────────┼──►
 -2    0  2  4             -2    0    2
```

---

## Concept: Effect on Training

| Without BatchNorm | With BatchNorm |
|-------------------|----------------|
| Spiky, noisy loss curves | Smooth, steady loss decrease |
| Slow convergence | Faster convergence |
| Must use small learning rate | Can use larger learning rate |
| Sensitive to weight initialisation | More robust |

The smoothing effect makes it much easier to spot overfitting — the val_loss trend is cleaner.

> **Want to go deeper?** [Batch normalisation (Wikipedia)](https://en.wikipedia.org/wiki/Batch_normalization)

---

## Concept: Where to Place BatchNorm

Two common conventions:

**After activation (simpler, more common):**
```python
Dense(256, activation='relu') → BatchNormalization()
```

**Before activation (original paper):**
```python
Dense(256) → BatchNormalization() → Activation('relu')
```

In practice the difference is small for most problems. Use the first (simpler) placement unless you have a specific reason not to.

**Combined with Dropout:**
The standard order is: `Dense → BatchNorm → Dropout → next Dense`
BatchNorm comes before Dropout because Dropout changes the scale of inputs.

```
Recommended layer stack (one "block"):

┌──────────────────────┐
│  Dense(256, relu)    │  ← compute activations
├──────────────────────┤
│  BatchNormalization  │  ← normalise to mean~0, std~1
├──────────────────────┤
│  Dropout(0.3)        │  ← randomly zero 30% of neurons
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Dense(256, relu)    │  ← next block receives clean,
├──────────────────────┤     normalised, regularised input
│  BatchNormalization  │
├──────────────────────┤
│  Dropout(0.3)        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Dense(1, sigmoid)   │  ← output layer (no BN, no Dropout)
└──────────────────────┘
```

---

## What Each Task Asks You to Do

### Task 1 — Add BatchNorm After Each Dense Layer
Insert `BatchNormalization()` after each of the three Dense(256) layers. Train for 50 epochs. Notice that the initial loss drops more quickly than in Exercise 1.

### Task 2 — Compare Training Stability
Build a matching model without BatchNorm and plot both training loss curves side by side. The BatchNorm version should show a visibly smoother, less spiky curve.

### Task 3 — Combine BatchNorm + Dropout
Add both BatchNorm and Dropout(0.3) after each Dense layer. Compare the final val_accuracy to the BatchNorm-only model from Task 1. The combination often gives the best results.

### Task 4 (BONUS) — Asymmetric Placement
Remove BatchNorm from the middle layer only. Measure the standard deviation of training loss over the first 20 epochs. A higher std indicates noisier, less stable training.

---

## Common Mistakes

- **Placing BatchNorm after the output layer**: The sigmoid output needs to remain in [0,1]. BatchNorm would distort this distribution. Only use BatchNorm in hidden layers.
- **Using Dropout before BatchNorm**: Dropout changes the scale of outputs. If applied before BatchNorm, the normalisation statistics are distorted. Always apply BatchNorm first, then Dropout.
- **Expecting BatchNorm to cure overfitting by itself**: BatchNorm provides very mild regularisation as a side effect. It is primarily a training stability technique, not a regulariser. Use it alongside Dropout.

---

## Now Open the Lab

[03_lab_batch_normalisation.md](03_lab_batch_normalisation.md)

## Next

[04_guide_early_stopping.md](04_guide_early_stopping.md)
