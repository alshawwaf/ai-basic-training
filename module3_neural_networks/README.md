# Module 3 — Neural Networks

## Goal
Build neural networks step by step — understanding exactly what each layer, activation, and loss function does — then apply that knowledge using Keras to build practical security classifiers.

---

## Key Concepts

### What is a neuron?
A neuron takes inputs, multiplies each by a weight, sums them up, adds a bias, and passes the result through an activation function:

```
output = activation( sum(inputs × weights) + bias )
```

Stack thousands of these together and you get a neural network.

### What are weights and biases?
- **Weights** — how much each input matters (the model learns these during training)
- **Bias** — a constant offset so the neuron can fire even when all inputs are zero
- Training = adjusting weights and biases until the network makes accurate predictions

### What is an activation function?
Without activation functions, a deep network collapses into a single linear equation — no matter how many layers you stack. Activation functions introduce non-linearity, allowing the network to learn complex patterns.

| Function | Formula | Used for |
|----------|---------|----------|
| **ReLU** | max(0, x) | Hidden layers (most common) |
| **Softmax** | exp(x) / sum(exp(x)) | Output layer for multi-class classification |
| **Sigmoid** | 1 / (1 + exp(-x)) | Output layer for binary classification |

### What is loss?
Loss measures how wrong the model is. Training = minimising loss via backpropagation and gradient descent.

---

## Lessons

| Lesson | File | Topic |
|--------|------|-------|
| 3.1 | [p001-Basic-Neuron-3-inputs.py](foundations/p001-Basic-Neuron-3-inputs.py) | Building your first neuron |
| 3.2 | [p002-Basic-Neuron-Layer.py](foundations/p002-Basic-Neuron-Layer.py) | A layer of neurons |
| 3.3 | [p003-Dot-Product.py](foundations/p003-Dot-Product.py) | Vectorising with NumPy |
| 3.4 | [p004-Layers-and-Object.py](foundations/p004-Layers-and-Object.py) | Layers as Python classes |
| 3.5 | [p005-ReLU-Activation.py](foundations/p005-ReLU-Activation.py) | ReLU activation function |
| 3.6 | [p006-Softmax-Activation.py](foundations/p006-Softmax-Activation.py) | Softmax activation |
| 3.7 | [p007-Categorical-Cross-Entropy-Loss.py](foundations/p007-Categorical-Cross-Entropy-Loss.py) | Cross-entropy loss |
| 3.8 | [p008-Categorical-Cross-Entropy-Loss-applied.py](foundations/p008-Categorical-Cross-Entropy-Loss-applied.py) | Full network + loss |
| 3.9 | [1_first_neural_net.py](1_first_neural_net.py) | Building with Keras |
| 3.10 | [2_deeper_network.py](2_deeper_network.py) | Deeper networks + regularisation |
| 3.11 | [3_cnn.py](3_cnn.py) | Convolutional networks |
| 3.12 | [4_hyperparameters.py](4_hyperparameters.py) | Tuning your network |
| Milestone | [milestone_packets.py](milestone_packets.py) | Neural network packet classifier |

---

## The Mental Model

```
Input features
      ↓
[Layer 1: Dense + ReLU]    ← learns low-level patterns
      ↓
[Layer 2: Dense + ReLU]    ← learns combinations of patterns
      ↓
[Output Layer: Sigmoid]    ← outputs probability of attack
      ↓
Loss (how wrong are we?)
      ↓
Backpropagation (adjust weights to reduce loss)
      ↓
Repeat for N epochs
```

---

## Dependencies

```bash
pip install tensorflow nnfs numpy
```
