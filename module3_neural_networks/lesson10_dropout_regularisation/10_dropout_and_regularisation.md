# Lesson 3.2 — Deeper Networks, Dropout & Batch Normalisation

---

## Concept: Going Deeper

Adding more layers lets the network learn more complex, hierarchical patterns:

- **Layer 1** might learn low-level features (e.g. high packet rate)
- **Layer 2** might learn combinations (high rate + specific port = scan)
- **Layer 3** might learn context (that combination with long duration = APT)

But deeper networks have two new problems: **overfitting** and **unstable training**.

---

## Dropout

During training, randomly "drop" (zero out) a fraction of neurons in a layer. This forces the network to not rely on any single neuron — similar to ensemble learning.

```python
keras.layers.Dropout(0.3)   # randomly zero 30% of neurons each training step
```

```
Without Dropout:             With Dropout (rate=0.3):
                             X = dropped this step

  [N1]--[N2]--[N3]            [N1]-- X --[N3]
   |  \  | \  /  |             |  \       /  |
  [N4]--[N5]--[N6]            [N4]--[N5]-- X
   |  \  | \  /  |             |  \  |       |
  [N7]--[N8]--[N9]             X --[N8]--[N9]

  All neurons active.         Different neurons dropped
  Model can become lazy.      each step -> redundancy learned.
```

- Applied **only during training** — not during inference
- Typical values: 0.2–0.5
- Reduces overfitting significantly

**Analogy:** Like training a sports team where random players sit out each practice — everyone has to learn every position.

---

## Batch Normalisation

Normalises the activations within each mini-batch during training. This:
- Speeds up training (can use higher learning rates)
- Reduces sensitivity to weight initialisation
- Acts as a mild regulariser

```python
keras.layers.BatchNormalization()
```

Place it **between** a Dense layer and its activation:
```python
keras.layers.Dense(64),
keras.layers.BatchNormalization(),
keras.layers.Activation('relu'),
```

---

## Early Stopping

Instead of choosing the number of epochs manually, let Keras stop training when validation loss stops improving:

```python
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,        # stop if no improvement for 10 epochs
    restore_best_weights=True
)
model.fit(..., callbacks=[early_stop])
```

This is the most practical way to prevent overfitting without manual tuning.

---

## Class Imbalance in Neural Networks

Security data is heavily imbalanced (1% attacks). Fix with:
```python
from sklearn.utils import class_weight
weights = class_weight.compute_class_weight('balanced', classes=[0,1], y=y_train)
model.fit(..., class_weight={0: weights[0], 1: weights[1]})
```

This tells the model to penalise missing an attack much more than a false alarm.

---

## What to Notice When You Run It

1. Compare the loss curves to Lesson 3.1 — does dropout help?
2. The early stopping callback — how many epochs did it actually train?
3. Final AUC vs the shallow model from 3.1

---

## Next Lesson

**[Lesson 3.3 — CNNs](11_convolutional_networks.md):** A different network architecture designed for spatial/grid data like images.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/1_lab_guide.md](workshop/1_lab_guide.md)**
