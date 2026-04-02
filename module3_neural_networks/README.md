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
| 3.1 | [1_basic_neuron.py](foundations/1_basic_neuron.py) | Building your first neuron |
| 3.2 | [2_neuron_layer.py](foundations/2_neuron_layer.py) | A layer of neurons |
| 3.3 | [3_dot_product.py](foundations/3_dot_product.py) | Vectorising with NumPy |
| 3.4 | [4_layers_as_classes.py](foundations/4_layers_as_classes.py) | Layers as Python classes |
| 3.5 | [5_relu_activation.py](foundations/5_relu_activation.py) | ReLU activation function |
| 3.6 | [6_softmax_activation.py](foundations/6_softmax_activation.py) | Softmax activation |
| 3.7 | [7_cross_entropy_loss.py](foundations/7_cross_entropy_loss.py) | Cross-entropy loss |
| 3.8 | [8_full_forward_pass.py](foundations/8_full_forward_pass.py) | Full network + loss |
| 3.9 | [First Neural Network](lesson9_first_neural_network/notes.md) | Building with Keras — [workshop](lesson9_first_neural_network/workshop/00_overview.md) |
| 3.10 | [Dropout & Regularisation](lesson10_dropout_regularisation/notes.md) | Dropout + regularisation — [workshop](lesson10_dropout_regularisation/workshop/00_overview.md) |
| 3.11 | [Convolutional Networks](lesson11_convolutional_networks/notes.md) | Convolutional networks — [workshop](lesson11_convolutional_networks/workshop/00_overview.md) |
| 3.12 | [Hyperparameter Tuning](lesson12_hyperparameter_tuning/notes.md) | Tuning your network — [workshop](lesson12_hyperparameter_tuning/workshop/00_overview.md) |
| Milestone | [milestone_packets.py](milestone/milestone_packets.py) | Neural network packet classifier |

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
