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

With 3 x Dense(256) layers and 10 input features, this model has ~133,000 parameters being trained on 1,600 samples. That's 83 parameters per training sample. The model has enough capacity to memorise every training example, including the random noise in the data.

**The overfit architecture:**

| Layer | Size | Activation | Parameters |
|-------|------|-----------|------------|
| Input | 10 | — | — |
| Dense | 256 | relu | 10 x 256 + 256 = 2,816 |
| Dense | 256 | relu | 256 x 256 + 256 = 65,792 |
| Dense | 256 | relu | 256 x 256 + 256 = 65,792 |
| Output | 1 | sigmoid | 256 x 1 + 1 = 257 |
| **Total** | | | **~134,657 params** |

> With only 1,600 training samples, that is **84 parameters per sample** — far too much capacity.

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

In a healthy training run, train loss and val loss both decrease and track each other:

**Healthy training:** Both train and val loss decrease together and converge toward the same low value.

**Overfitting signature:** Val loss stops falling (around epoch 20-30), then starts rising, while train loss continues decreasing.

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

---

## Now Open the Lab

[handson.md](handson.md)

## Next

[../2_add_dropout/lecture.md](../2_add_dropout/lecture.md)
