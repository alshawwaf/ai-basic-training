# Batch Normalisation

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_batchnorm_distribution.png" alt="Three side-by-side histograms of the same 4000 activations. Left 'Before BN — drifted' (grey): a wide bell shape stretching from -10 to 14, mean ≈ 2.1, std ≈ 3.8 with a red dashed line at the mean. Middle 'Centred + scaled' (cyan): a tighter bell from -4 to 4, mean ≈ 0, std ≈ 1, red dashed line at zero. Right 'After learned γ·z + β' (green): a similar tight bell shifted slightly so mean ≈ 0.3, std ≈ 0.8.">
  <div class="vis-caption">What BatchNorm does to one feature inside a mini-batch. Step 1 centres and scales the activations to mean ≈ 0, std ≈ 1. Step 2 reshapes them with the learned <code>γ</code> and <code>β</code>, which gives the layer the freedom to undo BN if it's unhelpful.</div>
</div>

The key effect: every later layer receives inputs whose statistics are pinned to a stable target instead of drifting around as training progresses, which is exactly what cures internal covariate shift.

---

## Concept: Effect on Training

| Without BatchNorm | With BatchNorm |
|-------------------|----------------|
| Spiky, noisy loss curves | Smooth, steady loss decrease |
| Slow convergence | Faster convergence |
| Must use small learning rate | Can use larger learning rate |
| Sensitive to weight initialisation | More robust |

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_batchnorm_smoothing.png" alt="Two side-by-side line charts. Left 'Training loss — BN smooths the curve': grey baseline curve falls fast then wobbles, cyan With-BatchNorm curve falls smoothly to the same low value with much less noise. Right 'Validation loss — same trend, less wobble': grey baseline rises and oscillates after the initial drop, cyan With-BatchNorm curve stays much flatter and tighter.">
  <div class="vis-caption">Real lab numbers. Both networks reach the same final accuracy, but the BatchNorm version's loss curves are visibly smoother — easier to read and easier to spot overfitting against.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_combined_block.png" alt="Horizontal flow diagram of four boxes connected by left-to-right arrows. Cyan box 'Dense(256, relu)' with caption 'compute activations'. Orange box 'BatchNormalization()' with caption 'stabilise mean ≈ 0, std ≈ 1'. Violet box 'Dropout(0.3)' with caption 'zero 30% of neurons'. Grey box '→ next block' with caption 'or final Dense head'.">
  <div class="vis-caption">The recommended block: <code>Dense → BatchNorm → Dropout</code>. Stack two or three of these back-to-back and finish with the output layer. BatchNorm goes before Dropout because Dropout would otherwise distort the statistics BN measures.</div>
</div>

Stack two or three of these blocks back-to-back, then finish with `Dense(1, sigmoid)` (or `Dense(N, softmax)`). The final output layer gets neither BatchNorm nor Dropout — its job is to produce the actual prediction distribution, and both regularisers would distort it.

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
