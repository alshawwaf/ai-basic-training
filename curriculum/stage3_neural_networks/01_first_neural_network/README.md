# Lesson 3.1 — Your First Neural Network in Keras

**Pre-reading:** Work through the [foundations scripts](../foundations/1_basic_neuron.py) first.

---

## Concept: From Scratch to Keras

In the `from_scratch` folder you built a neural network using only numpy — every weight multiplication, every dot product, every layer by hand. You now know what's happening under the hood.

Keras does all of that for you in a few lines. The concepts are identical.

---

## The Keras Equivalent

What you wrote in `p004-Layers-and-Object.py` (from scratch):
```python
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases  = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
```

In Keras:
```python
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(5, activation='relu', input_shape=(4,)),
    keras.layers.Dense(2, activation='softmax')
])
```

Same thing. Keras handles initialisation, the forward pass, and (crucially) the backward pass — backpropagation — automatically.

---

## What the Network Looks Like

```
Input Layer         Hidden Layer        Output Layer
(64 pixel values)   (learned features)  (10 digit classes)

  x1  ---+
  x2  ---+---> [ neuron ] ---+
  x3  ---+     [ neuron ] ---+---> [ 0 ] = P(digit=0)
  ...      +-> [ neuron ] ---+     [ 1 ] = P(digit=1)
  x64 ---+     [ neuron ]         ...
               [ neuron ]         [ 9 ] = P(digit=9)

  Each connection has a weight.       Softmax converts to
  Training adjusts all weights.       probabilities (sum=1.0)
```

## The Three Steps to Train Any Keras Model

```python
# 1. Define architecture
model = keras.Sequential([...])

# 2. Compile (choose loss function and optimiser)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. Train
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)
```

### Epochs
One full pass through the training data. You usually need many passes (epochs) before the model converges.

### Batch size
Training on all data at once is slow. Instead, process `batch_size` samples, compute the gradient, update weights, and repeat. Common values: 32, 64, 128.

### Optimiser: Adam
Gradient descent with adaptive learning rate — the default choice for most problems. It figures out how big each weight update should be.

### Loss function
- `binary_crossentropy` — binary classification (attack / benign)
- `categorical_crossentropy` — multi-class classification
- `mse` — regression

---

## Watching Training: Loss Curves

```python
history = model.fit(...)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
```

**Good training:** Both train_loss and val_loss decrease together and converge.

**Overfitting:** val_loss stops falling and starts rising while train_loss keeps decreasing.

| Pattern | Train loss | Val loss | Diagnosis |
|---------|-----------|----------|-----------|
| Both falling together | Decreasing | Decreasing | Healthy — model is learning |
| Diverging | Still decreasing | Rising | Overfitting — stop training earlier |

- **loss decreasing** — model is learning
- **val_loss increasing while loss decreases** — overfitting, stop training earlier

---

## What to Notice When You Run It

1. The `model.summary()` output — count the total parameters
2. The training progress — watch loss decrease each epoch
3. The loss curves — does val_loss track train_loss or diverge?
4. Final accuracy vs the Random Forest from Stage 2 — is deeper always better?

---

## Next Lesson

**[Lesson 3.2 — Deeper Networks](../02_dropout_regularisation/README.md):** Add more layers, dropout, and batch normalisation to build a more powerful and stable model.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

# Lesson 3.9 — Workshop Guide
## Your First Neural Network in Keras

> **Read first:** [README.md](README.md)
> **Reference solutions:** Each exercise has a matching solution file (e.g. `1_from_numpy_to_keras/solution_first_neural_network.py`) — open only after finishing the exercise

## What This Workshop Covers

You will bridge the gap between the NumPy foundations you built by hand and a full Keras neural network. Starting from how a `Dense` layer maps directly to matrix multiplication, you will build, compile, and train a neural network on a binary classification problem, evaluate it properly, and compare it to a logistic regression baseline. By the end you will know exactly what each Keras API call is doing and why.

This workshop uses a synthetic binary classification dataset with class imbalance (90/10 split) — deliberately chosen to mirror the conditions you encounter in real network security data.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_from_numpy_to_keras/lecture.md) | [handson.md](1_from_numpy_to_keras/handson.md) | Dense layer = matrix multiply + bias + activation |
| 2 | [lecture.md](2_build_the_network/lecture.md) | [handson.md](2_build_the_network/handson.md) | Choose layers, activations, output shape |
| 3 | [lecture.md](3_compile_and_train/lecture.md) | [handson.md](3_compile_and_train/handson.md) | model.fit(), history object, training curves |
| 4 | [lecture.md](4_evaluate_and_improve/lecture.md) | [handson.md](4_evaluate_and_improve/handson.md) | model.evaluate(), classification report, LR baseline |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage3_neural_networks/01_first_neural_network/1_from_numpy_to_keras/solution_first_neural_network.py
```

## Tips

- If TensorFlow is not installed: `pip install tensorflow`
- The first import of TensorFlow/Keras takes 5-10 seconds — this is normal
- Keras prints verbose GPU/CPU info at startup — you can safely ignore it
- Random weight initialisation means your exact accuracy numbers may differ by ±2%
