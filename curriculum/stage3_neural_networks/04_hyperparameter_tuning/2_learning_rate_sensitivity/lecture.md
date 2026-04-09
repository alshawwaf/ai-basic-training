# Learning Rate Sensitivity

> Read this guide fully before opening the lab.

---

## What You Will Learn

- Why learning rate is the single most important hyperparameter
- How too-small and too-large learning rates affect training differently
- How to read a loss curve to diagnose learning rate problems
- The practical range to start from in real projects

---

## Concept: What Learning Rate Does

In gradient descent, after computing the gradient of the loss, the model updates each weight:

```
new_weight = old_weight − learning_rate × gradient
```

The learning rate controls **how far to step** in the direction the gradient points.

```
lr=0.0001  →  tiny steps  →  slow convergence, may never reach minimum in budget
lr=0.001   →  normal steps →  usually converges well (safe default for Adam)
lr=0.01    →  bigger steps →  faster early, may oscillate near minimum
lr=0.1     →  huge steps   →  often diverges (loss explodes or oscillates wildly)
```

**Learning rate effect on the loss landscape:**

| Learning rate | Behaviour | Loss pattern |
|--------------|-----------|-------------|
| `lr=0.0001` | Too slow | Loss crawls down gradually — still decreasing after many epochs, may never reach minimum |
| `lr=0.001` | Just right | Loss decreases smoothly and reaches the minimum efficiently |
| `lr=0.1` | Too large | Loss overshoots and oscillates (bounces) — may never converge |

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_lr_step_size.png" alt="Three side-by-side panels, each plotting the same parabolic loss curve in grey. Left panel 'lr = 0.0001 (too small)': red dots trace eight tiny steps that barely move from the starting point on the left side of the bowl. Middle panel 'lr = 0.001 (just right)': green dots trace eight smooth steps that descend cleanly to the bottom of the bowl. Right panel 'lr = 0.1 (too large)': orange dots zigzag wildly across the bowl, overshooting the minimum on every step.">
  <div class="vis-caption">The learning rate is literally the step size on the loss landscape. Too small and the model crawls; too large and the model overshoots the minimum every step. The middle picture is the only one that converges.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_lr_loss_curves.png" alt="A line chart titled 'Real training loss — three Adam learning rates on the same data' with three curves over 30 epochs. Green 'lr = 0.001 (just right)' falls smoothly from ~0.65 toward ~0.15 and levels off. Orange 'lr = 0.1 (too large)' is erratic — bounces between 0.6 and 0.8 with no clear downward trend. Red 'lr = 0.00001 (too small)' is nearly flat at ~0.69, barely moving over the entire 30 epochs.">
  <div class="vis-caption">Real numbers from this stage's lab. Same dataset, same architecture, same number of epochs — only the learning rate differs. The green curve reaches val_acc ≈ 0.94; the orange and red curves get stuck around 0.67-0.69 because their step size is wrong for the loss landscape.</div>
</div>

> **Want to go deeper?** [Learning rate (Wikipedia)](https://en.wikipedia.org/wiki/Learning_rate)

---

## Concept: The Three Training Failure Modes

| Symptom in loss curve | Diagnosis | Fix |
|----------------------|-----------|-----|
| Loss barely moves after many epochs | lr too small | Increase by 10× |
| Loss improves slowly then plateaus | lr slightly small | Increase by 2-3× |
| Loss decreases then spikes upward | lr too large | Decrease by 10× |
| Loss immediately goes to NaN | lr way too large | Decrease by 100× |
| Loss decreases smoothly and levels off | Goldilocks zone | Keep it |

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_lr_diagnosis.png" alt="A diagnostic table with three columns: Symptom in loss curve, Diagnosis, and Fix. Five rows: 'Loss barely moves' / lr too small / red ↑10× pill; 'Slow then plateaus' / lr slightly small / orange ↑2-3× pill; 'Falls then spikes upward' / lr too large / orange ↓10× pill; 'Immediately NaN' / lr way too large / red ↓100× pill; 'Smooth, levels off' / Goldilocks zone / green 'keep it' pill.">
  <div class="vis-caption">A field guide for diagnosing learning rate problems by glancing at the loss curve. The shape of the curve almost always tells you which direction to move the learning rate.</div>
</div>

---

## Concept: Adam vs SGD and Learning Rate Sensitivity

Adam (Adaptive Moment Estimation) automatically adjusts per-parameter learning rates, so it is less sensitive than vanilla SGD. That is why:
- Adam default lr=0.001 works for most problems
- SGD default lr=0.01 is more finicky

This exercise uses Adam. Even so, the difference between 0.0001 and 0.1 is visible and instructive.

---

## Concept: Reading a Loss Curve

```
Good (lr=0.001):
  Epoch 1:  loss=0.65
  Epoch 5:  loss=0.42
  Epoch 10: loss=0.28   <- steady decline
  Epoch 20: loss=0.18
  Epoch 30: loss=0.16   <- approaching plateau (converged)

Bad — too slow (lr=0.00001):
  Epoch 1:  loss=0.69
  Epoch 30: loss=0.65   <- barely moved

Bad — unstable (lr=0.5):
  Epoch 1:  loss=0.68
  Epoch 5:  loss=0.43
  Epoch 8:  loss=0.71   <- spiked back up
  Epoch 12: loss=0.38
  Epoch 15: loss=0.82   <- oscillating
```

---

## What Each Task Asks You to Do

### Task 1 — Baseline: lr=0.001
Train the network with Adam at lr=0.001. Record final val accuracy.

```python
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), ...)
```

### Task 2 — Too large: lr=0.1
Repeat with lr=0.1. Compare the loss trajectory — look for spikes or divergence.

### Task 3 — Too small: lr=0.00001
Repeat with lr=0.00001. Observe how little progress is made in 30 epochs.

### Task 4 — Plot all three (Bonus)
Plot the training loss curves for all three runs on one figure. Title the lines by learning rate.

---

## Common Mistakes

**`NaN` in loss from epoch 1**
Your lr is so large the weights overflow. Drop lr by 100× immediately.

**All three look the same**
Make sure you are creating a fresh model for each experiment — reusing a trained model means you are continuing from where the previous training left off.

**Results wildly different from expected**
Neural network training has randomness. Set `tf.random.set_seed(42)` and `np.random.seed(42)` before each model build.
