# Exercise 2 — Add Dropout

> Read this guide fully before opening the lab.

## What You Will Learn

- How `Dropout(rate)` randomly silences neurons during training
- Why Dropout acts as an implicit ensemble of smaller networks
- How to measure the reduction in overfitting (comparing val_loss curves)
- How different dropout rates trade off regularisation strength vs capacity

---

## Concept: What Dropout Does

```python
keras.layers.Dropout(0.3)
```

For each sample in a training batch, this layer:
1. Generates a random binary mask (1 = keep, 0 = zero)
2. Multiplies each neuron output by its mask value
3. Scales remaining outputs by `1/(1 - rate)` to preserve expected magnitude

With `rate=0.3`: 30% of neurons are zeroed each batch. Different neurons are zeroed each batch.

```
Dropout(0.3) in action — training vs prediction:

TRAINING (batch 1):             TRAINING (batch 2):
 o  active                       o  active
 X  DROPPED (zeroed)             o  active
 o  active                       X  DROPPED
 o  active                       o  active
 X  DROPPED                      o  active
 o  active                       X  DROPPED
 o  active                       o  active
 X  DROPPED                      o  active

 30% off (random)                30% off (different random set)

PREDICTION (always):
 o  active
 o  active       ← ALL neurons active
 o  active          no dropout applied
 o  active          outputs unchanged
 o  active
 o  active
 o  active
 o  active
```

**Training vs Prediction behaviour:**

| Phase | Dropout active? | Effect |
|-------|----------------|--------|
| Training (`model.fit`) | YES | 30% of neurons zeroed randomly |
| Prediction (`model.predict`) | NO | All neurons active, outputs unchanged |

This asymmetry is important: the model trains in a noisy, regularised way, but predicts with its full capacity.

---

## Concept: Why Dropout Prevents Overfitting

Without Dropout, neurons can develop **co-adaptation** — neuron A learns to correct for neuron B's mistakes. If B is always present, A never learns an independent feature.

With Dropout:
- A cannot rely on B being there
- Each neuron must learn a robust, independent feature
- The trained network acts like an average of ~2^n sub-networks (where n = number of dropout neurons)

This ensemble effect is what makes Dropout so effective. A model with Dropout(0.3) effectively averages thousands of slightly different network configurations.

---

## Concept: Choosing the Dropout Rate

| Rate | Effect | When to use |
|------|--------|-------------|
| 0.1 | Very mild | Small models, slightly over-parameterised |
| 0.2–0.3 | Standard | Default starting point for most networks |
| 0.4–0.5 | Strong | Large networks with significant overfitting |
| >0.5 | Aggressive | Rarely useful — often causes underfitting |

The original Dropout paper (Srivastava et al.) recommended 0.5 for fully connected layers. In practice, 0.2–0.3 is the most common starting point.

> **Want to go deeper?** [Dropout regularisation (Wikipedia)](https://en.wikipedia.org/wiki/Dilution_(neural_networks))

---

## What Each Task Asks You to Do

### Task 1 — Add Dropout(0.3) After Each Dense Layer
Rebuild the 3×256 architecture and add a `Dropout(0.3)` layer after each Dense layer (not after the output). Train for 50 epochs. Compare final val_loss to the baseline printed at startup.

### Task 2 — Plot Val Loss Comparison
Plot both val_loss curves on the same graph. The Dropout curve should be lower and less spiky. Print the numerical improvement in val_loss.

### Task 3 — Compare Rates 0.1, 0.3, 0.5
Train three models with different rates. Print a table. Rate 0.3 typically gives the best result. Rate 0.5 may start showing underfitting (model loses too much capacity).

### Task 4 (BONUS) — Verify Dropout Is Off During Prediction
Make 5 identical `model.predict()` calls on the same input. All outputs should be identical — confirming Dropout is disabled in inference mode.

---

## Common Mistakes

- **Adding Dropout AFTER the output layer**: The output layer should not have Dropout — it changes the predicted probabilities at inference time.
- **Using Dropout during evaluation manually**: Keras handles train/eval mode automatically. You do not need to do anything special; calling `model.predict()` always uses inference mode.
- **Setting rate too high and underfitting**: If train accuracy is also poor (around the same as val), the dropout rate is too high and the model cannot learn at all.

---

## Now Open the Lab

[lab.md](lab.md)

## Next

[../3_batch_normalisation/guide.md](../3_batch_normalisation/guide.md)
