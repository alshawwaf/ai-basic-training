# Exercise 3 — Build and Train a CNN

> Read this guide fully before opening the lab.

## What You Will Learn

- How to assemble a full CNN from the building blocks covered in Exercise 2
- How to train and evaluate the CNN on MNIST digit classification
- How CNN accuracy compares to the Dense baseline (same training time, higher accuracy)
- How to read CNN training curves

---

## Concept: Complete CNN Architecture

The standard pattern for image classification:

```
Input (28, 28, 1)
      |
  Conv2D(32,(3,3),relu)   ← detects low-level features: edges, corners
      |       [26,26,32]
  MaxPool(2,2)
      |       [13,13,32]
  Conv2D(64,(3,3),relu)   ← combines features: curves, digit parts
      |       [11,11,64]
  MaxPool(2,2)
      |       [5,5,64]
  Flatten()
      |       [1600]
  Dense(128, relu)         ← classification reasoning
      |       [128]
  Dense(10, softmax)       ← one score per digit class (0-9)
      |       [10]
Output: probabilities for 10 classes
```

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

## Expected Outputs at a Glance

```
TASK 1 (model.summary totals):
Total params: ~225,034

TASK 2:
CNN test accuracy (5 epochs):   ~0.990
Dense baseline (3 epochs):      0.970
CNN improvement:                +0.020

(CNN uses fewer well-organised parameters and achieves higher accuracy)
```

---

## Common Mistakes

- **Forgetting Flatten() before Dense**: Keras will raise a shape error — Dense expects 1D input, Conv2D output is 3D.
- **Wrong loss function**: With 10 integer class labels (0-9), use `sparse_categorical_crossentropy`. Use `categorical_crossentropy` only if labels are one-hot encoded.
- **Using `input_shape` on the wrong layer**: Only the first layer needs `input_shape`. All subsequent layers infer their input shape from the previous layer's output.

---

## Now Open the Exercise File

[03_lab_build_and_train_cnn.md](03_lab_build_and_train_cnn.md)

## Next

[04_guide_malware_visualisation_context.md](04_guide_malware_visualisation_context.md)
