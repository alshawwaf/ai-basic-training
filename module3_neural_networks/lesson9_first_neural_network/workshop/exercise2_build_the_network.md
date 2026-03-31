# Exercise 2 — Build the Network

> **Exercise file:** [exercise2_build_the_network.py](exercise2_build_the_network.py)
> Read this guide fully before opening the exercise file.

## What You Will Learn

- How to choose activation functions for hidden layers vs output layers
- How to set the output layer shape for binary vs multi-class problems
- How to compile a model with the right optimizer, loss function, and metrics
- How switching problem type changes the output layer and loss

---

## Concept: Activation Functions

Activation functions determine what kind of signal flows through the network.

### ReLU (Rectified Linear Unit) — for hidden layers

```
relu(x) = max(0, x)

Output:
   |        /
   |       /
   |      /
   |_____/
   +---------> x
    negative = 0
```

Why ReLU for hidden layers?
- Computationally cheap
- Does not suffer from the vanishing gradient problem (unlike sigmoid in hidden layers)
- Sparse activation — many neurons output 0, which acts as implicit regularisation

### Sigmoid — for binary output

```
sigmoid(x) = 1 / (1 + e^-x)

Output:
  1.0 |          _______
  0.5 |        ./
  0.0 |_______/
      +---------> x
```

Maps any real number to [0, 1]. Interpret as probability of the positive class.

### Softmax — for multi-class output

Softmax takes a vector of raw scores and converts them to probabilities that sum to 1.0.

```python
softmax([2.0, 1.0, 0.1]) → [0.66, 0.24, 0.10]  # sums to 1.0
```

Use when your problem has 3+ mutually exclusive classes.

---

## Concept: Output Layer Design

| Problem type | Output units | Activation | Loss function |
|-------------|--------------|------------|---------------|
| Binary classification | 1 | sigmoid | binary_crossentropy |
| Multi-class (N classes) | N | softmax | sparse_categorical_crossentropy |
| Regression | 1 | none (linear) | mse or mae |

The number of output units must match the number of classes in your problem.

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

## Expected Outputs at a Glance

```
TASK 1 (model.summary() key lines):
 dense (Dense)          (None, 64)    704
 dense_1 (Dense)        (None, 32)    2080
 dense_2 (Dense)        (None, 1)     33
 Total params: 2,817

TASK 2:
Dense(64): (10×64)+64   = 704
Dense(32): (64×32)+32   = 2080
Dense(1):  (32×1)+1     = 33
Total:                    2817

TASK 3:
Model compiled successfully.
Optimizer: Adam
Loss: binary_crossentropy
```

---

## Common Mistakes

- **Using sigmoid on hidden layers**: Sigmoid in hidden layers causes vanishing gradients during training. Use relu for hidden layers, sigmoid only on binary output.
- **Wrong loss for the problem**: `binary_crossentropy` only works for 2-class output. Use `sparse_categorical_crossentropy` for 3+ classes with integer labels.
- **Output units don't match classes**: Dense(1) with softmax makes no mathematical sense. Binary = Dense(1, sigmoid). N-class = Dense(N, softmax).
- **Not scaling input features**: Neural networks train much better on standardised input. The dataset setup already calls `StandardScaler` — don't skip this step.

---

## Now Open the Exercise File

[exercise2_build_the_network.py](exercise2_build_the_network.py)

## Next

[exercise3_compile_and_train.md](exercise3_compile_and_train.md)
