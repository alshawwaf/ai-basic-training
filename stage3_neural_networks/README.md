# Stage 3 — Neural Networks

## Goal
Understand how neural networks work *from the ground up*, then apply that knowledge using Keras to build practical classifiers.

---

## Two-Part Structure

This stage is split into two parts deliberately:

| Part | Approach | Why |
|------|----------|-----|
| **Part A — From Scratch** | Build a neural net using only numpy | Understand *what* is actually happening mathematically |
| **Part B — With Keras** | Build the same thing in 10 lines | Understand *how* to use the industry-standard tools |

If you skip Part A and go straight to Keras, you end up with a black box you can't debug. Part A makes you dangerous.

---

## Key Concepts

### What is a neuron?
A neuron takes inputs, multiplies each by a weight, sums them up, adds a bias, and passes the result through an activation function:

```
output = activation( sum(inputs * weights) + bias )
```

That's it. Stack thousands of these together and you get a neural network.

### What are weights and biases?
- **Weights** — how much each input matters (the model learns these)
- **Bias** — a constant offset so the neuron can fire even when all inputs are zero
- Training = adjusting weights and biases until the network makes good predictions

### What is an activation function?
Without activation functions, a deep network collapses into a single linear equation — no matter how many layers you stack.
Activation functions introduce non-linearity, allowing the network to learn complex patterns.

| Function | Formula | Used for |
|----------|---------|----------|
| **ReLU** | max(0, x) | Hidden layers (most common) |
| **Softmax** | exp(x) / sum(exp(x)) | Output layer for multi-class classification |
| **Sigmoid** | 1 / (1 + exp(-x)) | Output layer for binary classification |

### What is loss?
Loss measures how wrong the model is. Training = minimising loss.
- **Categorical Cross-Entropy** — standard loss for classification problems
- The model adjusts weights to reduce loss via **backpropagation** + **gradient descent**

---

## Part A — From Scratch (Sentdex NNFS series)

Source: [github.com/Sentdex/NNfSiX](https://github.com/Sentdex/NNfSiX/tree/master/Python)
YouTube playlist: [Neural Networks from Scratch](https://www.youtube.com/playlist?list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3)

Work through these files in order. Each builds on the last.

| File | What it introduces | Cyber analogy |
|------|--------------------|---------------|
| [p001](from_scratch/p001-Basic-Neuron-3-inputs.py) | A single neuron with 3 inputs | One rule in a detection engine |
| [p002](from_scratch/p002-Basic-Neuron-Layer.py) | A full layer of neurons (manual) | Multiple rules firing in parallel |
| [p003](from_scratch/p003-Dot-Product.py) | Numpy dot product (same thing, cleaner) | Vectorising your detection rules |
| [p004](from_scratch/p004-Layers-and-Object.py) | Layers as Python classes, multiple layers | Stacking detection stages |
| [p005](from_scratch/p005-ReLU-Activation.py) | ReLU activation function | Thresholding — only fire if signal is strong enough |
| [p006](from_scratch/p006-Softmax-Activation.py) | Softmax activation (probabilities) | Output a confidence score per class |
| [p007](from_scratch/p007-Categorical-Cross-Entropy-Loss.py) | Cross-entropy loss (manual) | Measuring how wrong your classifier is |
| [p008](from_scratch/p008-Categorical-Cross-Entropy-Loss-applied.py) | Full network + loss calculation | End-to-end forward pass |

**Install the extra dependency for p005–p008:**
```bash
pip install nnfs
```

---

## Part B — With Keras

Once you've worked through Part A, these files build the same concepts using Keras — which handles the heavy lifting for you.

| Lesson | File | Topic |
|--------|------|-------|
| 3.1 | [1_first_neural_net.py](1_first_neural_net.py) | Recreate Part A in Keras (10 lines) |
| 3.2 | [2_deeper_network.py](2_deeper_network.py) | Add depth, dropout, batch normalisation |
| 3.3 | [3_cnn.py](3_cnn.py) | Convolutional networks for image data |
| 3.4 | [4_hyperparameters.py](4_hyperparameters.py) | Tuning learning rate, epochs, layer size |
| Milestone | [milestone_packets.py](milestone_packets.py) | Neural network to classify malicious network packets |

---

## Dependencies

```bash
pip install tensorflow nnfs
```

---

## The Mental Model

```
Input features
      ↓
[Layer 1: Dense + ReLU]    ← learns low-level patterns
      ↓
[Layer 2: Dense + ReLU]    ← learns higher-level combinations
      ↓
[Output Layer: Softmax]    ← outputs probabilities per class
      ↓
Loss (how wrong are we?)
      ↓
Backpropagation (adjust weights to reduce loss)
      ↓
Repeat for N epochs
```
