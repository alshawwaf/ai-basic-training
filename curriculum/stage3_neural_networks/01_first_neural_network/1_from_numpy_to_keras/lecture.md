# From NumPy to Keras

> Read this guide fully before opening the lab.

## What You Will Learn

- How a Keras `Dense` layer directly mirrors the NumPy matrix multiply you did in the foundations
- How to build a `Sequential` model and call `model.summary()`
- How to count parameters manually and verify against Keras
- How to run a forward pass with `model.predict()`

---

## Concept: Dense = Matrix Multiply + Bias + Activation

In `stage3_neural_networks/foundations/4_layers_as_classes.py` you wrote:

```python
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases  = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
```

Keras `Dense(8, activation='relu')` does exactly this — plus the activation function in one step. The API looks different but the maths is identical.

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_dense_neuron.png" alt="Diagram of a single Dense neuron with four input circles labelled x1 to x4 on the left, each connected by lines labelled w1 to w4 to a central cyan sigma node, an orange bias circle feeding the same node from below, an arrow leaving the sigma node to a violet 'relu' box, and a final arrow to an output label. Below the diagram a formula reads output = relu(x1·w1 + x2·w2 + x3·w3 + x4·w4 + b).">
  <div class="vis-caption">Inside one Dense neuron: each input is multiplied by its own weight, the weighted values are summed with one bias, and the sum passes through an activation function. A <code>Dense(N)</code> layer is just N copies of this circuit, each with its own private weights and bias.</div>
</div>

| Stage | What it does | Formula |
|---|---|---|
| 1. Multiply | each input is multiplied by its own weight | `x1·w1, x2·w2, x3·w3, x4·w4` |
| 2. Sum + bias | the weighted contributions are added together with one bias term | `z = x1·w1 + x2·w2 + x3·w3 + x4·w4 + b` |
| 3. Activation | the sum passes through a non-linear function | `output = relu(z)` |

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_sequential_wiring.png" alt="Network wiring diagram. Left column: 4 grey input circles. Middle column: 8 cyan hidden neurons labelled Dense(8, relu). Right: a single red sigmoid output neuron labelled Dense(1, sigmoid). Every input is connected to every hidden neuron with thin grey lines, and every hidden neuron is connected to the output. Below: '(4 × 8) + 8 = 40 params' in cyan and '(8 × 1) + 1 = 9 params' in red, with 'Total: 49 trainable parameters' below.">
  <div class="vis-caption">Every input is connected to every hidden neuron, and every hidden neuron is connected to the output. That "all-to-all" wiring with one private weight per edge is what makes a layer "Dense".</div>
</div>

| Layer | Neurons | Each neuron receives | Each neuron's output goes to |
|---|---:|---|---|
| Input | 4 | the raw feature value | every neuron in the next Dense |
| `Dense(8, relu)` | 8 | all 4 inputs (its own weights + bias) | every neuron in the next Dense |
| `Dense(1, sigmoid)` | 1 | all 8 outputs from the previous layer | the model's final probability |

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_param_count.png" alt="Parameter count breakdown. Left: a cyan grid of 4 rows by 8 columns labelled 'Weight matrix W: shape (4, 8)' with caption '4 × 8 = 32 weights'. Middle: a thin orange column of 8 cells labelled 'Bias b: shape (8,)' with caption '8 biases'. A plus sign between them and an equals sign on the right lead to a green box containing '40' with the label 'total params'.">
  <div class="vis-caption">A <code>Dense(8)</code> layer over a 4-feature input holds 32 weights in its W matrix plus 8 biases — exactly 40 trainable parameters, which is what <code>model.summary()</code> prints in the "Param #" column.</div>
</div>

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
