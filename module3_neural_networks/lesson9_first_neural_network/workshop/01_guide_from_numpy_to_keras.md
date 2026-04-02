# Exercise 1 — From NumPy to Keras

> Read this guide fully before opening the lab.

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

```
Single Dense Neuron (what happens inside ONE unit):

  x1 ──w1──┐
  x2 ──w2──┤
  x3 ──w3──┼──► [ sum + bias ] ──► [ relu ] ──► output
  x4 ──w4──┘
            weighted sum = x1*w1 + x2*w2 + x3*w3 + x4*w4 + b
```

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

How Dense layers connect — every input feeds every neuron:

```
 Input          Dense(8, relu)       Dense(1, sigmoid)
  (4)              (8)                   (1)

  o ─────┬──────► o
  o ─────┼──────► o ─────┬──────────► o  → output
  o ─────┼──────► o ─────┘               (probability)
  o ─────┼──────► o
         ├──────► o        All 8 neurons
         ├──────► o        connect to the
         ├──────► o        1 output neuron
         └──────► o

  4 inputs       8 neurons             1 neuron
  each connects  each connects
  to ALL 8       to the 1 output
```

You only need to specify `input_shape` on the first layer. Keras infers the rest.

> **Want to go deeper?** [Keras Sequential Model (keras.io)](https://keras.io/guides/sequential_model/)

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

```
Weight matrix W          Bias vector b
(4 inputs × 8 units)    (8 units)
┌─────────────────────┐  ┌───┐
│ w11 w12 w13 ... w18 │  │b1 │
│ w21 w22 w23 ... w28 │  │b2 │
│ w31 w32 w33 ... w38 │  │...│
│ w41 w42 w43 ... w48 │  │b8 │
└─────────────────────┘  └───┘
     32 values            8 values   = 40 params total
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

## Common Mistakes

- **Forgetting `input_shape` on the first layer**: Keras needs to know the input dimensions to build the weight matrix. Without it, `model.summary()` shows "?" for output shapes.
- **Confusing units with parameters**: Dense(8) has 8 *neurons* but the *parameter count* also depends on how many inputs it receives.
- **Using `model.predict()` with wrong input shape**: input must be 2D — `(n_samples, n_features)`. A 1D array of shape `(4,)` needs to be reshaped to `(1, 4)`.

---

## Now Open the Lab

[01_lab_from_numpy_to_keras.md](01_lab_from_numpy_to_keras.md)

## Next

[02_guide_build_the_network.md](02_guide_build_the_network.md)
