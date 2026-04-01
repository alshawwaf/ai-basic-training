# Exercise 3 — Batch Size Effects

> Read this guide fully before opening the exercise file.

---

## What You Will Learn

- How batch size affects gradient quality and training noise
- The tradeoff between computational speed and generalisation
- Why the deep learning community settled on 32–256 as the standard range
- How to measure wall-clock training time in Python

---

## Concept: What a Batch Is

During training, instead of computing the gradient over the entire dataset at once (too slow) or one sample at a time (too noisy), we use a **mini-batch** — a random subset of samples.

```
Full dataset: 1600 training samples

batch_size=32  →  50 batches per epoch  →  50 gradient updates per epoch
batch_size=256 →  6.25 batches per epoch → ~6 gradient updates per epoch
batch_size=1600 → 1 batch per epoch    →  1 gradient update per epoch (= "full batch")
```

Each gradient update uses only the samples in that batch to compute the gradient. Smaller batches = noisier gradient estimates.

---

## Concept: The Noise-Stability Tradeoff

| Batch size | Gradient quality | Updates per epoch | Generalisation | GPU memory |
|------------|-----------------|-------------------|----------------|------------|
| Small (8–32) | Noisy (high variance) | Many | Often better | Low |
| Medium (64–256) | Balanced | Moderate | Good | Moderate |
| Large (512–2048) | Stable (low variance) | Few | Sometimes worse | High |
| Full batch | Very stable | 1 | Can overfit sharper minima | Very high |

The noise from small batches acts as implicit **regularisation** — it prevents the model from settling into sharp, narrow minima that don't generalise. This is counter-intuitive but well-established empirically.

> **Want to go deeper?** [Gradient descent (Wikipedia)](https://en.wikipedia.org/wiki/Gradient_descent)

---

## Concept: The Sharp vs Flat Minima Insight

Research (Keskar et al., 2017) found that large-batch training tends to converge to **sharp minima** — points where the loss is low but the surrounding loss landscape is steep. Small perturbations (new test data) push the model off the cliff.

Small-batch training converges to **flat minima** — the model stays near a low-loss region even under perturbation, which is exactly what generalisation requires.

```
Sharp minimum (large batch):      Flat minimum (small batch):
      |    |                              ___________
      |  * |     ← deep but narrow       |         |
______|    |______                  _____|    *    |_____
                                              ↑ stays low even with perturbation
```

---

## Concept: Timing Training in Python

```python
import time
start = time.time()
model.fit(...)
elapsed = time.time() - start
print(f"Training time: {elapsed:.1f}s")
```

Use this to compare wall-clock time across batch sizes. Larger batches are often faster per epoch because modern hardware (GPUs especially) are optimised for large matrix operations.

---

## What Each Task Asks You to Do

### Task 1 — Small batch: batch_size=32
Train for 30 epochs with batch_size=32. Record val_accuracy and wall-clock time.

### Task 2 — Large batch: batch_size=512
Train for 30 epochs with batch_size=512. Compare accuracy and time.

### Task 3 — Full batch: batch_size=1600
Use the full training set as one batch. Observe: does it generalise as well? Is it faster or slower?

### Task 4 — Summary table (Bonus)
Print a formatted comparison table:
```
batch_size | val_accuracy | train_time(s) | updates/epoch
```

---

## Expected Outputs at a Glance

```
batch_size=  32 | val_accuracy: ~0.91 | time: ~4.0s | updates/epoch: 50
batch_size= 512 | val_accuracy: ~0.90 | time: ~1.5s | updates/epoch: 3
batch_size=1600 | val_accuracy: ~0.88 | time: ~0.8s | updates/epoch: 1
```

Actual times depend on your hardware. The relative ranking (32 slowest, full-batch fastest) should hold.

---

## Common Mistakes

**All three give the same accuracy**
This can happen with simple problems — the dataset is easy enough that any batch size works. Try increasing epochs to 100 to see divergence in final accuracy.

**batch_size=1600 gives an error**
Your training set may not be exactly 1600. Use `len(X_train)` instead of a hardcoded number.

**Training time looks backwards (small batch faster)**
On CPU, very small batches have overhead per update. On GPU the relationship is more pronounced. Your machine may show different ratios — focus on the accuracy comparison, not the timing.

---

## Now Open the Exercise File

[exercise3_batch_size_effects_lab.md](exercise3_batch_size_effects_lab.md)

---

## Next

[exercise4_architecture_search.md](exercise4_architecture_search.md) — manual grid search over network depth and width.
