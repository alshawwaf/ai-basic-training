# Exercise 1 — Demonstrate Overfitting

> Read this guide fully before opening the lab.

## What You Will Learn

- How too much model capacity relative to training data causes overfitting
- How to read the diverging loss curves that signal overfitting
- How to measure the overfitting gap numerically
- How going deeper amplifies the problem

---

## Concept: Model Capacity and Overfitting

**Model capacity** = how many distinct functions the model can represent. A network with more parameters has higher capacity — it can fit more complex patterns.

With 3 × Dense(256) layers and 15 input features, this model has ~138,000 trainable parameters but only ~5,440 training samples to learn from. That's roughly 25 parameters per training sample — enough capacity to memorise every training example, including its random noise.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_capacity_vs_data.png" alt="Side-by-side blocks. Left: a large red block containing the number 137,729 labelled 'trainable parameters (3 × Dense(256))'. Right: a smaller cyan block containing the number 5,440 labelled 'training samples'. Below both: a banner reading 'approximately 25 parameters per training sample — far too much capacity'.">
  <div class="vis-caption">The 3 × Dense(256) network has roughly 25 trainable parameters for every training sample. With that much capacity it can simply memorise the noise in the training set instead of learning the real attack pattern.</div>
</div>

**The overfit architecture:**

| Layer | Size | Activation | Parameters |
|-------|------|-----------|------------|
| Input | 15 | — | — |
| Dense | 256 | relu | 15 × 256 + 256 = 4,096 |
| Dense | 256 | relu | 256 × 256 + 256 = 65,792 |
| Dense | 256 | relu | 256 × 256 + 256 = 65,792 |
| Output | 1 | sigmoid | 256 × 1 + 1 = 257 |
| **Total** | | | **~135,937 params** |

```
Too much capacity:
  model learns: "training sample #47 had these exact values → label=1"
  Real pattern:  "high connection_rate AND many failed_connections → attack"

Result:
  Training accuracy: 99.5%   (memorised examples)
  Validation accuracy: 92%   (noise patterns don't generalise)
```

---

## Concept: The Diverging Loss Signature

In a healthy training run, train loss and val loss both decrease and track each other. With too much capacity, they pull apart:

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_overfit_curves.png" alt="Two side-by-side line charts of 50 training epochs for the 3 × Dense(256) baseline. Left panel 'Loss — train falls forever, val turns upward': cyan train loss decreases monotonically toward zero, red val loss falls to a minimum around epoch 5 then rises steadily for the rest of training; a green dashed vertical line marks 'val min @ ep 5'. Right panel 'Accuracy — gap = 0.035 at epoch 50': cyan train accuracy reaches 1.0 by epoch 10 while red val accuracy plateaus around 0.965, leaving a clear gap.">
  <div class="vis-caption">Real lab numbers from <code>solution_demonstrate_overfitting.py</code>. Train loss falls forever; val loss reaches its minimum within the first few epochs and then drifts upward — the textbook overfitting signature.</div>
</div>

| Epoch range | Train loss | Val loss | What's happening |
|-------------|-----------|----------|-----------------|
| 1–10 | Falling fast | Falling fast | Both learning — healthy |
| 10–30 | Still falling | Flattens | Val gains slow — approaching capacity |
| 30–50 | Still falling | **Rising** | Overfitting — model memorising noise |

The point where val loss hits its minimum is the ideal stopping point. Training beyond that point makes the model worse on unseen data.

> **Want to go deeper?** [Overfitting (Wikipedia)](https://en.wikipedia.org/wiki/Overfitting)

---

## What Each Task Asks You to Do

### Task 1 — Build and Train the Large Network
Build 3 × Dense(256) with sigmoid output, train for 50 epochs with no regularisation. Print the total parameter count (should be >130,000) and final train vs val accuracy.

### Task 2 — Plot the Diverging Curves
Plot train loss vs val loss on a single graph. You should see val loss start rising after ~10-20 epochs while train loss continues falling. This is the core overfitting signal.

### Task 3 — Measure the Gap
Print the numerical overfitting gap. An accuracy gap above 0.03 is significant. A loss gap above 0.05 is clearly overfitting. These numbers give you a baseline to compare against in exercises 2-4.

### Task 4 (BONUS) — More Depth = More Overfit
Add 2 more Dense(256) layers (5 total) and compare the final gap. Deeper without regularisation is worse. Record both gaps — you'll apply fixes in the next exercises.

---

## Common Mistakes

- **Training for too few epochs**: With only 10 epochs you may not see divergence. Use 50.
- **Using small Dense layers**: Dense(16)×3 won't overfit much. You need Dense(256) to see the effect clearly.
- **Forgetting to set random seed**: Without `tf.random.set_seed(42)` and `np.random.seed(42)`, results vary significantly between runs.
