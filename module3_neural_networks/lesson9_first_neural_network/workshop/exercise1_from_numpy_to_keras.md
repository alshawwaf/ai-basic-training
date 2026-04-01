# Exercise 1 — From NumPy to Keras

> Read this guide fully before opening the exercise file.

## What You Will Learn

- How a Keras `Dense` layer directly mirrors the NumPy matrix multiply you did in the foundations
- How to build a `Sequential` model and call `model.summary()`
- How to count parameters manually and verify against Keras
- How to run a forward pass with `model.predict()`

---

## Concept: Dense = Matrix Multiply + Bias + Activation

In `module3_neural_networks/foundations/4_layers_as_classes.py` you wrote:

```python
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases  = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
```

Keras `Dense(8, activation='relu')` does exactly this — plus the activation function in one step. The API looks different but the maths is identical.

---

## Concept: Sequential Model

`keras.Sequential` chains layers: the output of layer N becomes the input of layer N+1.

```python
model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(4,)),
    keras.layers.Dense(1, activation='sigmoid')
])
```

Data flow:
```
Input (shape: 4)  →  Dense(8, relu)  →  Dense(1, sigmoid)  →  Output (shape: 1)
```

You only need to specify `input_shape` on the first layer. Keras infers the rest.

---

## Concept: Counting Parameters

Every `Dense` layer has two sets of parameters:
- **Weight matrix** W of shape `(n_inputs, n_units)`
- **Bias vector** b of shape `(n_units,)`

Total parameters in one Dense layer:

```
params = (n_inputs × n_units) + n_units
```

Example for `Dense(8)` receiving 4 inputs:
```
W: 4 × 8 = 32  entries
b:     8 =  8  entries
Total = 40 parameters
```

This is exactly what `model.summary()` shows in the "Param #" column.

---

## Concept: model.predict() — The Forward Pass

Once a model is built (even before training), you can run a forward pass:

```python
output = model.predict(input_array, verbose=0)
```

This applies each layer's matrix multiply and activation in sequence. Before training, the weights are random, so the output is meaningless — but the shape is always correct and shows the architecture is wired up properly.

---

## What Each Task Asks You to Do

### Task 1 — Build the Model
Build a 2-layer Sequential model and call `model.summary()`. Read the output: what are the layer names, output shapes, and parameter counts?

### Task 2 — Manual Parameter Count
Calculate the parameter count for each layer by hand using `(inputs × units) + units`. Verify your answer matches `model.count_params()`.

### Task 3 — Run a Prediction
Create 3 random input samples of 4 features each. Run `model.predict()`. Confirm the output shape is `(3, 1)` and all values are between 0 and 1 (because the last layer uses sigmoid).

### Task 4 (BONUS) — Architecture Comparison
Build three models with very different sizes and compare parameter counts. Notice how the count grows rapidly — a 256-unit first layer with input_shape=(10,) already creates 2,816 parameters in that layer alone.

---

## Expected Outputs at a Glance

```
TASK 1:
Total params: 49  (40 in layer 1, 9 in layer 2)

TASK 2:
Layer 1 (Dense 8):  (4 × 8) + 8 = 40
Layer 2 (Dense 1):  (8 × 1) + 1 = 9
Total: 49  Match: True

TASK 3:
Input shape:   (3, 4)
Output shape:  (3, 1)
All values between 0 and 1: True

TASK 4 (BONUS):
Architecture [4, 1]:          ~51 params
Architecture [64, 32, 1]:   ~2,625 params
Architecture [256, 128, 64, 1]: ~67,393 params
```

---

## Common Mistakes

- **Forgetting `input_shape` on the first layer**: Keras needs to know the input dimensions to build the weight matrix. Without it, `model.summary()` shows "?" for output shapes.
- **Confusing units with parameters**: Dense(8) has 8 *neurons* but the *parameter count* also depends on how many inputs it receives.
- **Using `model.predict()` with wrong input shape**: input must be 2D — `(n_samples, n_features)`. A 1D array of shape `(4,)` needs to be reshaped to `(1, 4)`.

---

## Now Open the Exercise File

[exercise1_from_numpy_to_keras.py](exercise1_from_numpy_to_keras.py)

## Next

[exercise2_build_the_network.md](exercise2_build_the_network.md)
