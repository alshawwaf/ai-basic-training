# Exercise 2 — Build the Network

> Read this guide fully before opening the lab.

## What You Will Learn

- How to choose activation functions for hidden layers vs output layers
- How to set the output layer shape for binary vs multi-class problems
- How to compile a model with the right optimizer, loss function, and metrics
- How switching problem type changes the output layer and loss

---

## Concept: Activation Functions

Activation functions determine what kind of signal flows through the network.

### ReLU (Rectified Linear Unit) — for hidden layers

`relu(x) = max(0, x)`

| Input `x` | Output `relu(x)` | Behaviour |
|---:|---:|---|
| −5 | 0 | clamped — neuron is "off" |
| −1 | 0 | clamped |
|  0 | 0 | exactly zero |
|  1 | 1 | passes through unchanged |
|  5 | 5 | passes through unchanged |

The shape is a flat floor at zero for any negative input, then a straight 45° ramp upward for positive input — no saturation at the top, no expensive `exp()`.

Why ReLU for hidden layers?
- Computationally cheap
- Does not suffer from the vanishing gradient problem (unlike sigmoid in hidden layers)
- Sparse activation — many neurons output 0, which acts as implicit regularisation

### Sigmoid — for binary output

```
sigmoid(x) = 1 / (1 + e^-x)
```

| x value | sigmoid(x) | Behaviour |
|---------|-----------|-----------|
| Very negative | Near 0.0 | Suppressed |
| 0 | 0.5 | Midpoint |
| Very positive | Near 1.0 | Saturated |

Maps any real number to [0, 1]. Interpret as probability of the positive class.

### Softmax — for multi-class output

Softmax takes a vector of raw scores and converts them to probabilities that sum to 1.0.

```python
softmax([2.0, 1.0, 0.1]) → [0.66, 0.24, 0.10]  # sums to 1.0
```

Use when your problem has 3+ mutually exclusive classes.

> **Want to go deeper?** [Activation function (Wikipedia)](https://en.wikipedia.org/wiki/Activation_function)

---

## Concept: Output Layer Design

| Problem type | Output units | Activation | Loss function |
|-------------|--------------|------------|---------------|
| Binary classification | 1 | sigmoid | binary_crossentropy |
| Multi-class (N classes) | N | softmax | sparse_categorical_crossentropy |
| Regression | 1 | none (linear) | mse or mae |

The number of output units must match the number of classes in your problem.

**Same hidden layer, two different output layers**

|  | Binary classification | Multi-class (3 classes) |
|---|---|---|
| Hidden layer | `Dense(64, relu)` | `Dense(64, relu)` |
| Output layer | `Dense(1, sigmoid)` | `Dense(3, softmax)` |
| Output shape | `(batch, 1)` | `(batch, 3)` |
| Example output for one sample | `0.82` (probability of attack) | `[0.66, 0.24, 0.10]` (sums to 1.0) |
| Loss function | `binary_crossentropy` | `sparse_categorical_crossentropy` |

Same hidden network, different head: choose the head and loss to match the *number of mutually exclusive classes* in your problem.

---

## Concept: Compiling a Model

`model.compile()` sets up the training configuration before any data is seen:

```python
model.compile(
    optimizer='adam',           # how to update weights
    loss='binary_crossentropy', # what to minimise
    metrics=['accuracy']        # what to display during training
)
```

**Adam** (Adaptive Moment Estimation) is the default optimizer for almost all neural networks. It adjusts the learning rate for each weight individually, converging faster than plain gradient descent.

**binary_crossentropy** measures how far a probability prediction is from the true label (0 or 1). It penalises confident wrong predictions heavily.

> **Want to go deeper?** [Cross-entropy (Wikipedia)](https://en.wikipedia.org/wiki/Cross-entropy)

---

## What Each Task Asks You to Do

### Task 1 — Build the Binary Classifier
Build a 3-layer network for the binary classification dataset. Input has 10 features. Hidden layers use relu; output uses sigmoid. Call `model.summary()` and understand each row.

### Task 2 — Parameter Count Breakdown
Calculate the parameter count for all three layers manually. The formula is `(inputs × units) + units` per layer. Verify your total matches `model.count_params()`.

### Task 3 — Compile the Model
Call `model.compile()` with adam, binary_crossentropy, and accuracy. The model is now ready to train. Print confirmation.

### Task 4 (BONUS) — 3-Class Architecture
Create a 3-class dataset and rebuild the model with `Dense(3, softmax)` as the output. Switch the loss to `sparse_categorical_crossentropy`. Observe how the output layer changes from 1 unit to 3 units.

---

## Common Mistakes

- **Using sigmoid on hidden layers**: Sigmoid in hidden layers causes vanishing gradients during training. Use relu for hidden layers, sigmoid only on binary output.
- **Wrong loss for the problem**: `binary_crossentropy` only works for 2-class output. Use `sparse_categorical_crossentropy` for 3+ classes with integer labels.
- **Output units don't match classes**: Dense(1) with softmax makes no mathematical sense. Binary = Dense(1, sigmoid). N-class = Dense(N, softmax).
- **Not scaling input features**: Neural networks train much better on standardised input. The dataset setup already calls `StandardScaler` — don't skip this step.
