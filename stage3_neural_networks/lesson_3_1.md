# Lesson 3.1 — Your First Neural Network in Keras

**Script:** [1_first_neural_net.py](1_first_neural_net.py)
**Pre-reading:** Work through [from_scratch/p001–p004](from_scratch/) first.

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

- **loss decreasing** → model is learning
- **val_loss increasing while loss decreases** → overfitting — stop training earlier

---

## What to Notice When You Run It

1. The `model.summary()` output — count the total parameters
2. The training progress — watch loss decrease each epoch
3. The loss curves — does val_loss track train_loss or diverge?
4. Final accuracy vs the Random Forest from Stage 2 — is deeper always better?

---

## Next Lesson

**[Lesson 3.2 — Deeper Networks](lesson_3_2.md):** Add more layers, dropout, and batch normalisation to build a more powerful and stable model.
