# Exercise 3 — Build and Train a CNN

> Read this guide fully before opening the lab.

## What You Will Learn

- How to assemble a full CNN from the building blocks covered in Exercise 2
- How to train and evaluate the CNN on MNIST digit classification
- How CNN accuracy compares to the Dense baseline (same training time, higher accuracy)
- How to read CNN training curves

---

## Concept: Complete CNN Architecture

The standard pattern for image classification, layer by layer:

| Layer | Output shape | What it does |
|---|---|---|
| Input | `(28, 28, 1)` | one greyscale image |
| `Conv2D(32, (3,3), relu)` | `(26, 26, 32)` | detects low-level features: edges, corners |
| `MaxPool2D((2,2))`        | `(13, 13, 32)` | halves the spatial size, keeps the strongest signal |
| `Conv2D(64, (3,3), relu)` | `(11, 11, 64)` | combines edges into curves and digit parts |
| `MaxPool2D((2,2))`        | `(5, 5, 64)`   | halves spatial size again |
| `Flatten()`               | `(1600,)`      | unrolls the 2D feature maps into one long vector |
| `Dense(128, relu)`        | `(128,)`       | classification reasoning over the detected features |
| `Dense(10, softmax)`      | `(10,)`        | one probability per digit class (0–9) |

Convolutions shrink each spatial dimension by `kernel - 1` (here `3 - 1 = 2`), and pooling halves it. Trace those rules once and the shape column above is fully predictable.

---

## Concept: How Conv Layers Stack

Early convolutional layers learn simple features (edges, gradients).
Later layers combine those simple features into complex ones (loops, straight lines, curves of specific angles).

```
Conv layer 1: detects pixel-level gradients (edges)
Conv layer 2: detects combinations of edges (curves, corners, angles)
Dense head:   maps detected shapes to digit identity
```

This hierarchical feature learning is why CNNs generalise well from far fewer parameters than Dense networks.

> **Want to go deeper?** [Convolutional neural network (Wikipedia)](https://en.wikipedia.org/wiki/Convolutional_neural_network)

---

## Concept: Flatten Layer

Before a Dense layer can process the 2D feature maps, they must be flattened to 1D:

```
Feature maps: (5, 5, 64)  →  Flatten  →  (1600,)
```

`Flatten()` just reshapes the tensor. It has no learnable parameters.

**Flatten — 3D feature maps to a 1D vector**

| Stage | Tensor shape | Total values |
|---|---|---:|
| After last conv block | `(5, 5, 64)` — 64 maps, each 5 × 5 | `5 × 5 × 64 = 1600` |
| After `Flatten()` | `(1600,)` — single long vector | `1600` |

`Flatten` doesn't *change* any values — it just unrolls the cube into a row, so the next `Dense(128)` layer can see the 1600 numbers as a flat feature vector.

---

## What Each Task Asks You to Do

### Task 1 — Build and Compile
Build the 2-conv CNN described above. Call `model.summary()`. Note the total parameter count (~225,034) and verify the shape trace manually.

### Task 2 — Train 5 Epochs and Compare
Train with `batch_size=128, validation_split=0.1`. After training, call `model.evaluate(X_test, y_test)`. Compare CNN test accuracy to the Dense baseline of ~0.970. With 5 epochs the CNN should reach ~0.990.

### Task 3 — Plot Training Curves
Side-by-side: training loss (left) and training accuracy (right), both showing train and validation. The CNN curves typically converge faster and reach lower loss than Dense.

### Task 4 (BONUS) — 3 Conv Layers
Add a third `Conv2D(64,(3,3))` before the Flatten. Check `model.summary()` to verify spatial dimensions don't go negative. Compare accuracy to 2-layer CNN.

---

## Common Mistakes

- **Forgetting Flatten() before Dense**: Keras will raise a shape error — Dense expects 1D input, Conv2D output is 3D.
- **Wrong loss function**: With 10 integer class labels (0-9), use `sparse_categorical_crossentropy`. Use `categorical_crossentropy` only if labels are one-hot encoded.
- **Using `input_shape` on the wrong layer**: Only the first layer needs `input_shape`. All subsequent layers infer their input shape from the previous layer's output.

---

## Now Open the Lab

[handson.md](handson.md)

## Next

[../4_malware_visualisation_context/lecture.md](../4_malware_visualisation_context/lecture.md)
