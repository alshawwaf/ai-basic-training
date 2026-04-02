# Exercise 2 — Conv2D and MaxPooling2D

> Read this guide fully before opening the lab.

## What You Will Learn

- How `Conv2D(filters, kernel_size)` slides a filter window over an image
- How `MaxPooling2D(pool_size)` downsamples feature maps
- How to trace spatial dimensions through conv + pooling layers
- Why Conv2D uses dramatically fewer parameters than Dense for the same task

---

## Concept: How a Convolutional Filter Works

A `Conv2D(32, (3,3))` layer creates 32 filters, each of shape 3×3 pixels.

Each filter slides across the image one position at a time:

```
Input image (6×6):          Filter (3×3):       At position (0,0):
+--+--+--+--+--+--+         +--+--+--+          sum([0.1×0.2, 0.5×0.4, ...])
|0 |0 |0 |0 |0 |0 |         |0.1|0.4|0.3|       + bias = output value
|0 |0 |0 |0 |0 |0 |    ×    |0.2|0.5|0.1|
|0 |0 |.7|.9|.8|0 |         |0.0|0.3|0.8|
|0 |0 |.8|1 |.9|0 |
|0 |0 |.6|.8|.7|0 |
|0 |0 |0 |0 |0 |0 |

Filter slides to (0,1), (0,2), ..., (3,3) → 4×4 output positions
```

Key insight: **the same filter weights are applied at every position**. This is weight sharing — a "horizontal edge detector" learned once detects horizontal edges everywhere.

---

## Concept: Shape Arithmetic

For `Conv2D` with `valid` padding (default) and stride=1:

```
output_size = input_size - kernel_size + 1
```

| Input | Kernel | Output per filter |
|-------|--------|------------------|
| 28×28 | 3×3 | 26×26 |
| 28×28 | 5×5 | 24×24 |
| 26×26 | 3×3 | 24×24 |

For `MaxPooling2D((2,2))`:

```
output_size = input_size / pool_size
```

| Input | Pool | Output |
|-------|------|--------|
| 26×26 | 2×2 | 13×13 |
| 13×13 | 2×2 | 6×6 |

---

## Concept: MaxPooling2D

```
2×2 MaxPool example:
+---+---+---+---+         +---+---+
| 1 | 3 | 2 | 4 |         | 3 | 4 |
| 2 | 0 | 1 | 3 |    →    | 2 | 3 |
| 0 | 2 | 3 | 1 |         (max of each 2×2 block)
| 1 | 0 | 0 | 3 |
```

Benefits:
- Reduces spatial dimensions (less computation for later layers)
- Provides small-translation invariance (a feature slightly shifted still activates)
- No learnable parameters (just a max operation)

> **Want to go deeper?** [Pooling layer (Wikipedia)](https://en.wikipedia.org/wiki/Convolutional_neural_network#Pooling_layer)

---

## Concept: Parameter Count

```
Conv2D(32, (3,3)) on 1-channel (greyscale) input:
  weight params: 3 × 3 × 1_channel × 32_filters = 288
  bias params:   32_filters = 32
  TOTAL: 320 parameters

Dense(32) on flat 784-pixel input:
  weight params: 784 × 32 = 25,088
  bias params:   32
  TOTAL: 25,120 parameters

Ratio: Dense uses 79× more parameters for the same 32 output features!
```

---

## What Each Task Asks You to Do

### Task 1 — Build Conv + Pool and Trace Shapes
Build `Conv2D(32,(3,3),relu) → MaxPooling2D((2,2))` and call `model.summary()`. Trace: input (28,28,1) → after conv (26,26,32) → after pool (13,13,32). Print the arithmetic manually.

### Task 2 — Count Parameters
Manually compute Conv2D parameter count: `3×3×1×32 + 32 = 320`. Compare to Dense equivalent: `784×32 + 32 = 25,120`. Print the ratio — Conv2D is 79x more efficient.

### Task 3 — Visualise Image and Explain Filters
Display the first MNIST test image. Print pixel values in a small region. Explain conceptually what filters look for (edges, corners, curves).

### Task 4 (BONUS) — Compare Kernel Sizes (3,3) vs (5,5)
Rebuild with a 5×5 kernel. Compare output shapes and parameter counts. Larger kernels see bigger context but have more parameters and produce smaller output maps.

---

## Common Mistakes

- **Confusing filter count with parameter count**: 32 filters does NOT mean 32 parameters. Each filter has `kernel_h × kernel_w × channels` parameters, giving `320` total for Conv2D(32,(3,3)) on greyscale.
- **Adding MaxPooling before Conv2D**: MaxPooling goes AFTER Conv2D. The Conv2D creates the feature maps; MaxPooling downsamples them.

---

## Now Open the Lab

[02_lab_conv_and_pooling.md](02_lab_conv_and_pooling.md)

## Next

[03_guide_build_and_train_cnn.md](03_guide_build_and_train_cnn.md)
