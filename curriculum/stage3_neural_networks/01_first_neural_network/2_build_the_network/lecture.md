# Build the Network

## What You Will Learn

- How to choose activation functions for hidden layers vs output layers
- How to set the output layer shape for binary vs multi-class problems
- How to compile a model with the right optimizer, loss function, and metrics
- How switching problem type changes the output layer and loss

---

## Concept: Activation Functions

Activation functions determine what kind of signal flows through the network.

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_activation_functions.png" alt="Three side-by-side panels. Left: ReLU plotted in cyan from x=-6 to 6, flat at zero for negative input then a straight 45-degree ramp upward; annotations 'off for negative input' and 'linear ramp for positive'. Middle: Sigmoid plotted in red, an S-curve from 0 at left to 1 at right with the 0.5 midpoint at x=0; annotation 'P(positive class) ∈ [0, 1]'. Right: Softmax shown as three coloured bars (violet 0.66, orange 0.24, cyan 0.10) labelled class A, B, C; caption 'sums to 1.00'.">
  <div class="vis-caption">ReLU is the default for hidden layers (cheap and gradient-friendly). Sigmoid squashes one number to a [0,1] probability — use it for binary output. Softmax turns a vector of N scores into N probabilities that sum to 1.0 — use it for N-class output.</div>
</div>

### ReLU (Rectified Linear Unit) — for hidden layers

`relu(x) = max(0, x)` — flat at zero for any negative input, then a straight 45° ramp upward for positive input. No saturation at the top, no expensive `exp()`.

Why ReLU for hidden layers?
- Computationally cheap
- Does not suffer from the vanishing gradient problem (unlike sigmoid in hidden layers)
- Sparse activation — many neurons output 0, which acts as implicit regularisation

### Sigmoid — for binary output

`sigmoid(x) = 1 / (1 + e^-x)` — maps any real number to [0, 1]. Interpret as probability of the positive class.

### Softmax — for multi-class output

Softmax takes a vector of raw scores and converts them to probabilities that sum to 1.0:

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_output_heads.png" alt="Two side-by-side network diagrams sharing the same cyan hidden layer of three neurons labelled Dense(64, relu). Left panel labelled 'Binary classification': hidden layer connects to a single red sigmoid neuron labelled Dense(1, sigmoid), with output box showing '0.82' and caption 'P(attack)'; below it 'loss: binary_crossentropy'. Right panel labelled 'Multi-class (3 classes)': hidden layer connects to three coloured neurons (violet, orange, cyan) labelled Dense(3, softmax), with output box showing 0.66, 0.24, 0.10 and caption 'sums to 1.00'; below it 'loss: sparse_categorical_crossentropy'.">
  <div class="vis-caption">Same hidden network, two different output heads. Pick the head and loss to match the number of mutually exclusive classes in your problem — one sigmoid neuron for binary, N softmax neurons for N-class.</div>
</div>

| | Binary classification | Multi-class (3 classes) |
|---|---|---|
| Hidden layer | `Dense(64, relu)` | `Dense(64, relu)` |
| Output layer | `Dense(1, sigmoid)` | `Dense(3, softmax)` |
| Output shape | `(batch, 1)` | `(batch, 3)` |
| Example output for one sample | `0.82` (probability of attack) | `[0.66, 0.24, 0.10]` (sums to 1.0) |
| Loss function | `binary_crossentropy` | `sparse_categorical_crossentropy` |

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
