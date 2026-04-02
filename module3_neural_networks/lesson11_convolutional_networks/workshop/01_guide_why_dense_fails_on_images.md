# Exercise 1 — Why Dense Fails on Images

> Read this guide fully before opening the lab.

## What You Will Learn

- Why flattening an image to a 1D vector destroys spatial structure
- How Dense layers still get decent accuracy on MNIST despite spatial blindness
- How to count the massive parameter cost of treating images as flat vectors
- The definitive experiment: shuffled pixels don't hurt Dense accuracy (but would destroy a CNN)

---

## Concept: What Dense "Sees"

A 28×28 greyscale image has 784 pixels. When flattened:

```
Original 28×28:        Flattened to 784:
+-+-+-+-+--+           [0.0, 0.0, 0.12, 0.85, 0.95, 0.71, 0.0, ...]
|  |  |  |  |               pixel 0  1    2     3     4    5   6
|  |  | #|# |
|  | #|# |# |    →    Dense doesn't know pixel 3 is next to pixel 4.
|  | #|# |  |         It doesn't know they form an edge.
+-+-+-+-+--+          It just knows "when index 3 is high, index 4 is
                       usually also high" — a correlation without geometry.
```

A Dense layer with `input_shape=(784,)` and 128 units learns:
- "When pixel 401 is bright AND pixel 402 is bright AND pixel 415 is bright → probably digit 3"

It can learn this pattern but must learn it separately for every position in the image. No generalisation across positions.

---

## Concept: Spatial Invariance — What Dense Misses

If the digit "3" slides one pixel to the right, a Dense layer must re-learn all the pixel correlations from scratch. It has no concept of translation invariance.

A Conv2D filter learns **one detector** (e.g., "curved line") and applies it at **every position**. If the "3" shifts right, the same filter still detects it.

```
Dense: must learn separate weights for each position

 "3" centred:               "3" shifted right:
 ┌─────────────┐            ┌─────────────┐
 │    ###      │            │       ###   │
 │       #     │            │          #  │
 │    ###      │            │       ###   │
 │       #     │            │          #  │
 │    ###      │            │       ###   │
 └─────────────┘            └─────────────┘
 Dense: learned!             Dense: never seen this!

Conv2D: same 3x3 filter detects curves at EVERY position
 → works for both, no relearning needed
```

This is why CNNs use dramatically fewer parameters:

| Architecture | Parameters (for MNIST) |
|-------------|----------------------|
| Dense(128) on 784 pixels | ~101,770 |
| Conv2D(32,(3,3)) on 28×28×1 | 288 (just the filter weights!) |

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

---

## Now Open the Lab

[01_lab_why_dense_fails_on_images.md](01_lab_why_dense_fails_on_images.md)

## Next

[02_guide_conv_and_pooling.md](02_guide_conv_and_pooling.md)
