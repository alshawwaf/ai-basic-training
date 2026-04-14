# Build and Train a CNN

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_full_architecture.png" alt="A horizontal flow diagram of eight rounded rectangles connected by arrows, each labelled with a layer in the standard MNIST CNN. From left: grey 'Input (28,28,1)', cyan 'Conv2D(32, 3×3) → (26,26,32)', orange 'MaxPool(2,2) → (13,13,32)', cyan 'Conv2D(64, 3×3) → (11,11,64)', orange 'MaxPool(2,2) → (5,5,64)', violet 'Flatten() → (1600,)', violet 'Dense(128, relu) → (128,)', green 'Dense(10, softmax) → (10,)'.">
  <div class="vis-caption">The full 2-conv CNN, layer by layer. Cyan = convolutions (feature detectors), orange = pooling (downsampling), violet = the dense head, green = the softmax output. Each box shows the tensor shape after that layer so you can sanity-check the shape arithmetic by eye.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_vs_dense_accuracy.png" alt="A bar chart titled 'MNIST test accuracy — Dense baseline vs 2-conv CNN'. Two bars: red bar labelled 'Dense(128)' at 0.9642, cyan bar labelled '2-conv CNN' at 0.9894. The CNN bar has a thicker gold border highlighting it as the winner. Text above the bars reads 'CNN beats Dense by 0.025 with 2.2× more parameters but vastly better accuracy'.">
  <div class="vis-caption">Real numbers from this stage's lab. The Dense baseline trained for 3 epochs reaches ~96.4% test accuracy; the 2-conv CNN trained for 5 epochs reaches ~98.9%. That gap looks small but it represents a ~70% reduction in error rate.</div>
</div>

### Task 3 — Plot Training Curves
Side-by-side: training loss (left) and training accuracy (right), both showing train and validation. The CNN curves typically converge faster and reach lower loss than Dense.

<div class="lecture-visual">
  <img src="/static/lecture_assets/cnn_training_curves.png" alt="Two side-by-side line charts of the 5-epoch CNN training run. Left panel 'Loss': cyan train loss falls from ~0.3 to near 0, red val loss tracks closely. Right panel 'Accuracy': cyan train accuracy climbs from ~0.92 to ~0.99, red val accuracy tracks closely just below.">
  <div class="vis-caption">Real lab run. Train and val curves stay close together for all 5 epochs — the model is learning steadily without overfitting. Compare this to the Dense baseline curves from Exercise 1, where the model converged but plateaued at lower accuracy.</div>
</div>

### Task 4 (BONUS) — 3 Conv Layers
Add a third `Conv2D(64,(3,3))` before the Flatten. Check `model.summary()` to verify spatial dimensions don't go negative. Compare accuracy to 2-layer CNN.

---

## Common Mistakes

- **Forgetting Flatten() before Dense**: Keras will raise a shape error — Dense expects 1D input, Conv2D output is 3D.
- **Wrong loss function**: With 10 integer class labels (0-9), use `sparse_categorical_crossentropy`. Use `categorical_crossentropy` only if labels are one-hot encoded.
- **Using `input_shape` on the wrong layer**: Only the first layer needs `input_shape`. All subsequent layers infer their input shape from the previous layer's output.
