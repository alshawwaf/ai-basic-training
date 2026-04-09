# Why Dense Fails on Images

> Read this guide fully before opening the lab.

## What You Will Learn

- Why flattening an image to a 1D vector destroys spatial structure
- How Dense layers still get decent accuracy on MNIST despite spatial blindness
- How to count the massive parameter cost of treating images as flat vectors
- The definitive experiment: shuffled pixels don't hurt Dense accuracy (but would destroy a CNN)

---

## Concept: What Dense "Sees"

A 28×28 greyscale image has 784 pixels. When flattened:

A 28x28 image is flattened to a 784-element array: `[0.0, 0.0, 0.12, 0.85, 0.95, 0.71, 0.0, ...]`

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_image_vs_flat.png" alt="Two side-by-side panels of the same MNIST digit. Left panel: a 28×28 greyscale image of the digit '7' rendered as a real picture with a cyan border, titled 'What humans see — 28×28 pixel grid'. Right panel: a bar chart of 784 grey bars (one per pixel index 0 to 783) showing pixel values from 0.0 to 1.0, titled 'What Dense sees — 784 numbers, no spatial relationship'.">
  <div class="vis-caption">The exact same MNIST digit shown two ways. Humans see a 7. A Dense layer sees an unordered list of 784 brightness numbers — pixel 0 and pixel 1 are no more "neighbours" to it than pixel 0 and pixel 783.</div>
</div>

Dense doesn't know pixel 3 is next to pixel 4. It doesn't know they form an edge. It just knows "when index 3 is high, index 4 is usually also high" — a correlation without geometry.

A Dense layer with `input_shape=(784,)` and 128 units learns:
- "When pixel 401 is bright AND pixel 402 is bright AND pixel 415 is bright → probably digit 3"

It can learn this pattern but must learn it separately for every position in the image. No generalisation across positions.

---

## Concept: Spatial Invariance — What Dense Misses

If the digit "3" slides one pixel to the right, a Dense layer must re-learn all the pixel correlations from scratch. It has no concept of translation invariance.

A Conv2D filter learns **one detector** (e.g., "curved line") and applies it at **every position**. If the "3" shifts right, the same filter still detects it.

| Scenario | Dense layer | Conv2D layer |
|----------|------------|-------------|
| "3" centred in image | Learned — recognises it | Learned — recognises it |
| "3" shifted 5px right | **Never seen this** — must relearn all weights | **Still works** — same 3x3 filter detects curves at every position |

> Conv2D achieves **translation invariance** through weight sharing — one detector applied everywhere. Dense must learn separate weights for every position.

This is why CNNs use dramatically fewer parameters:

| Architecture | Parameters (for MNIST) |
|-------------|----------------------|
| Dense(128) on 784 pixels | ~101,770 |
| Conv2D(32,(3,3)) on 28×28×1 | 288 (just the filter weights!) |

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_dense_vs_cnn_params.png" alt="Bar chart titled 'Parameter cost — Dense vs Conv2D for the same MNIST input'. Left red bar labelled 'Dense(128) on flat 784' towering with the value 100,480. Right cyan bar labelled 'Conv2D(32, 3×3) on 28×28×1' tiny by comparison with the value 320. Orange bold text near the top reads 'Dense uses 314× more parameters'.">
  <div class="vis-caption">Same MNIST input, two layer choices. The Dense layer has to learn a separate weight for every (pixel, neuron) pair — over 100,000 parameters. A Conv2D layer with thirty-two 3×3 filters reuses the same handful of weights at every position and only needs ~320 parameters total.</div>
</div>

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_shuffled_pixels.png" alt="Two MNIST images side by side. Left panel titled 'Original — humans see 7' with a cyan title shows a clean greyscale digit 7. Right panel titled 'Same pixels, shuffled positions' with a red title shows what looks like random scattered noise — the exact same pixel values rearranged with a fixed permutation. A subtitle below reads 'Dense scores ≈ identically on both — it has no spatial awareness'.">
  <div class="vis-caption">The shuffle test from Task 4. The right image contains the exact same 784 pixel values as the left — just in different positions. A Dense network trained on either version reaches almost identical accuracy, because it never knew where the pixels were in the first place. A CNN, by contrast, would collapse on the right image.</div>
</div>

> **Want to go deeper?** [Convolutional neural network (Wikipedia)](https://en.wikipedia.org/wiki/Convolutional_neural_network)

---

## What Each Task Asks You to Do

### Task 1 — Build and Train Dense Baseline
Build `Dense(128, relu) → Dense(10, softmax)` with flattened 784-pixel input. Train 3 epochs. Record test accuracy (~97%) — Dense does quite well on MNIST! But we'll beat it with far fewer parameters in Exercise 3.

### Task 2 — Count Dense Parameters
Print `model.summary()` and manually verify: `(784 × 128) + 128 = 100,480` for the first layer alone. This massive parameter count is the cost of not using spatial structure.

### Task 3 — Visualise the Two Representations
Plot the same image as a 28×28 grid and as a flat bar chart. This makes visually concrete what Dense vs CNN "sees".

### Task 4 (BONUS) — Shuffle Pixels
Apply a random permutation to all pixels in all images (same permutation for train and test). Retrain Dense — accuracy is nearly identical! Dense truly has no spatial awareness; pixel positions are arbitrary to it.

---

## Common Mistakes

- **Not reshaping the output correctly**: `model.evaluate()` returns a tuple `(loss, metric)` — unpack both or use `_` for the loss.
- **Mixing X_train and X_train_flat**: Make sure the Dense model uses the flat version `(n, 784)` and the CNN uses the 4D version `(n, 28, 28, 1)`.
