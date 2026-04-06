# Exercise 3 — Compile and Train

> Read this guide fully before opening the lab.

## What You Will Learn

- How `model.fit()` controls the training loop (epochs, batch_size, validation_split)
- What the `history` object stores and how to extract values from it
- How to interpret training vs validation accuracy curves
- When to stop training (before overfitting begins)

---

## Concept: The Training Loop

When you call `model.fit()`, Keras runs the following loop for each epoch:

```
For each epoch:
    Shuffle training data (optional)
    For each mini-batch of batch_size samples:
        1. Forward pass — compute predictions
        2. Compute loss between predictions and true labels
        3. Backward pass — compute gradients via backpropagation
        4. Update all weights: w = w - learning_rate × gradient
    Compute validation metrics (no weight updates during validation)
    Print epoch summary
```

**One mini-batch iteration (forward + backward):**

**Forward pass** (left to right):

| Step | Component | Shape / Detail |
|------|-----------|---------------|
| 1 | Batch input | 32 x 10 |
| 2 | Dense(64), relu | Hidden layer activation |
| 3 | Dense(1), sigmoid | Output probability |
| 4 | Loss function | Compare prediction vs label |

**Backward pass** (right to left):

| Step | Component | What happens |
|------|-----------|-------------|
| 4 → 3 | Gradients layer 2 | Compute error signal |
| 3 → 2 | Gradients layer 1 | Propagate gradients back |
| 2 → 1 | Weights updated | `w = w - learning_rate x gradient` |

One **epoch** = one complete pass through all training data.
One **batch** = `batch_size` samples processed before updating weights.

With 1,600 training samples and `batch_size=32`:
- 1600 / 32 = **50 gradient updates per epoch**

With `batch_size=1600` (one big batch):
- **1 gradient update per epoch** — slow learning

> **Want to go deeper?** [Backpropagation (Wikipedia)](https://en.wikipedia.org/wiki/Backpropagation)

---

## Concept: The History Object

`model.fit()` returns a `History` object. Access metrics as a dictionary:

```python
history = model.fit(...)

history.history.keys()
# ['loss', 'accuracy', 'val_loss', 'val_accuracy']

history.history['accuracy']   # list of 20 values (one per epoch)
history.history['val_accuracy'][-1]  # final validation accuracy
```

The length of each list equals the number of epochs trained.

---

## Concept: Reading Training Curves

A healthy run shows two curves climbing together — `accuracy` (on training data) and `val_accuracy` (on the validation portion) — both rising sharply at first and then flattening as the model runs out of new things to learn:

| Epoch range | What `accuracy` does | What `val_accuracy` does | What it means |
|---|---|---|---|
| 1 – 5   | jumps from ~0.6 to ~0.85 | tracks training closely | **rapid learning** — picking up obvious patterns |
| 5 – 15  | rises slowly to ~0.95   | rises slowly, then plateaus | **fine-tuning** — learning subtler patterns |
| 15 +    | keeps creeping up to ~1.0 | flat or starts dropping | **overfitting risk** — training on noise specific to the train set |

The single most important signal: when `val_loss` starts **rising** while `loss` keeps **falling**, stop. The model has begun memorising the training data.

---

## Concept: validation_split vs Test Set

`validation_split=0.2` reserves the **last 20% of your training data** for validation.

```
X_train (1600 samples after split)
  |__ Training portion (1280):  used for gradient updates
  |__ Validation portion (320): used to measure performance each epoch

X_test (400 samples — never seen during training or validation)
  |__ Used ONLY for final evaluation in Exercise 4
```

**Data layout when you call `fit(..., validation_split=0.2)`**

| Subset | Size | Source | What it is used for |
|---|---:|---|---|
| Training portion | 1280 (80% of `X_train`) | `X_train`, first 80% | gradient updates — weights actually change here |
| Validation portion | 320 (20% of `X_train`) | `X_train`, last 20% | per-epoch monitoring — no weight updates |
| Test set | 400 | `X_test`, never touched by `fit()` | held back until **after** all training, used for the final report |

Never use `X_test` inside the training loop. The test set evaluates how well the trained model generalises to truly unseen data.

---

## What Each Task Asks You to Do

### Task 1 — Train for 20 Epochs
Call `model.fit()` with `validation_split=0.2`, `epochs=20`, `batch_size=32`. Store the returned object in `history`. Watch the per-epoch output to see loss decreasing.

### Task 2 — Extract Final Accuracy
Access `history.history['accuracy'][-1]` and `history.history['val_accuracy'][-1]`. Print both and compute the gap. A gap below 0.02 usually indicates the model is not significantly overfitting.

### Task 3 — Plot Training Curves
Create side-by-side plots for loss and accuracy, both showing train vs validation. The curves should converge and track each other closely for a healthy model.

### Task 4 (BONUS) — Train Longer and Find the Peak
Train the same architecture for 100 epochs. Use `np.argmax()` on `val_accuracy` to find which epoch had the best validation accuracy. Compare that to the final epoch accuracy — the difference shows the cost of overtraining.

---

## Common Mistakes

- **Not storing the return value of model.fit()**: `model.fit(...)` without assignment — you lose the history and can't plot curves.
- **Printing from `history.history` before training**: `history` doesn't exist until after `model.fit()` completes.
- **Confusing validation_split with the test set**: The validation portion of X_train and X_test are different things. Never evaluate on X_test until the very end.
- **Plotting loss on wrong axis**: Loss and accuracy have different scales. Always put them on separate subplots.

---

## Now Open the Lab

[handson.md](handson.md)

## Next

[../4_evaluate_and_improve/lecture.md](../4_evaluate_and_improve/lecture.md)
