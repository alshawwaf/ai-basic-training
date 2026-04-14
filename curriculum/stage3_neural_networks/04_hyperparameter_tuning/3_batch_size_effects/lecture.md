# Batch Size Effects

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

**One epoch, two extremes (1600 samples)**

| `batch_size` | Batches per epoch | Samples per batch | Weight updates per epoch | Character |
|---|---:|---:|---:|---|
| 32 | 50 | 32 | 50 | many small noisy steps |
| 1600 (full batch) | 1 | 1600 | 1 | one big stable step |

With `batch_size=32` the model takes 50 small, slightly-wrong steps per epoch — the noise averages out across batches. With full-batch the model takes a single very accurate step that uses every sample at once.

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_batch_updates.png" alt="Two side-by-side panels of the same parabolic loss bowl. Left panel 'batch_size = 32 → 50 small noisy steps per epoch': cyan dots trace a wandering noisy path with 50 steps from an orange start dot at top-left down to a green end dot near the bottom. Right panel 'batch_size = 1600 (full batch) → 1 big stable step': a single violet arrow goes straight from the orange start dot down to the green end dot at the bottom of the bowl.">
  <div class="vis-caption">The same parabolic loss bowl, the same number of training samples seen — but two completely different update strategies. Small batches take many noisy steps; full batch takes one big accurate step. The noise on the left is what gives small-batch training its implicit regularisation effect.</div>
</div>

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

**Sharp vs flat minima — what each batch regime converges to**

| Minimum type | Trained by | Loss landscape near the minimum | Behaviour on unseen data |
|---|---|---|---|
| **Sharp** | large batches | deep but very narrow — loss climbs steeply on either side | a small input shift pushes the model off the cliff → poor generalisation |
| **Flat** | small batches | low and wide — loss stays low across a broad region | small perturbations keep loss low → much better generalisation |

The noise injected by small batches makes it hard for SGD to *settle* into a sharp valley — it keeps getting bumped out, and only the wide flat regions are stable enough for it to stick.

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_sharp_vs_flat.png" alt="A grey curve representing a 1D loss landscape across 'weight space'. The curve has two minima: a narrow deep spike on the right marked with a red dot labelled 'Sharp minimum (large-batch training) — poor generalisation', and a wide gentle bowl on the left marked with a green dot labelled 'Flat minimum (small-batch training) — robust to perturbation'. Both minima reach roughly the same loss value but the sharp one rises steeply on either side.">
  <div class="vis-caption">Same loss value, two different shapes. The red sharp minimum is a knife-edge — a tiny shift in input distribution sends the loss soaring. The green flat minimum stays low across a wide region, so unseen test samples land in roughly the same area and the model still works. Small-batch training systematically prefers the flat one.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/hp_batch_results.png" alt="Two side-by-side bar charts. Left 'Final validation accuracy' shows three bars: cyan bs=32 at 0.935, violet bs=512 at 0.935, orange bs=1600 (full batch) at 0.888. Right 'Wall-clock training time (30 epochs)' shows three bars: cyan bs=32 at 9.0s, violet bs=512 at 5.4s, orange bs=1600 at 5.0s.">
  <div class="vis-caption">Real numbers from this stage's lab on CPU. bs=32 and bs=512 reach the same final accuracy but bs=32 takes ~70% longer wall-clock. Full-batch training is the fastest per epoch but generalises noticeably worse — the textbook small-vs-large batch trade-off in three bars.</div>
</div>

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

## Common Mistakes

**All three give the same accuracy**
This can happen with simple problems — the dataset is easy enough that any batch size works. Try increasing epochs to 100 to see divergence in final accuracy.

**batch_size=1600 gives an error**
Your training set may not be exactly 1600. Use `len(X_train)` instead of a hardcoded number.

**Training time looks backwards (small batch faster)**
On CPU, very small batches have overhead per update. On GPU the relationship is more pronounced. Your machine may show different ratios — focus on the accuracy comparison, not the timing.
