# Compile and Train

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_training_loop.png" alt="Two-row diagram of a single training step. Top row labelled 'FORWARD PASS — predict → compute loss': four cyan and red boxes connected by left-to-right arrows: Batch input (32 × 10), Dense(64) relu, Dense(1) sigmoid, Loss (BCE). A vertical arrow drops from the loss box down to the bottom row. Bottom row labelled 'BACKWARD PASS — propagate gradients → update weights': four orange and violet boxes connected by right-to-left arrows: ∂L/∂output, Grad W2, Grad W1, Update W1. A green box on the right reads 'one batch × one epoch'.">
  <div class="vis-caption">One mini-batch step inside <code>model.fit()</code>. The forward pass computes a prediction and a loss; the backward pass propagates gradients back through every layer and updates the weights. Repeat for every batch in every epoch.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_training_curves.png" alt="Two side-by-side line charts showing 100 epochs of training history. Left panel: 'Loss curves — both fall together' with cyan train loss and red val loss both decreasing rapidly in the first 10 epochs and then flattening. Right panel: 'Accuracy curves — train climbs slightly above val' with cyan train accuracy reaching about 0.99 and red val accuracy reaching about 0.94, with a green dashed vertical line marking 'Peak val @ epoch 18'.">
  <div class="vis-caption">Real <code>model.fit()</code> output for the lab dataset. Both losses fall together, both accuracies climb together, and the validation accuracy peaks around epoch 18 then plateaus — the train curve continues climbing slightly, opening a small generalisation gap.</div>
</div>

The single most important signal: when `val_loss` starts **rising** while `loss` keeps **falling**, stop. The model has begun memorising the training data.

---

## Concept: validation_split vs Test Set

`validation_split=0.2` reserves the **last 20% of your training data** for validation.

<div class="lecture-visual">
  <img src="/static/lecture_assets/nn_validation_split.png" alt="Horizontal stacked bar chart of 2000 samples split into three coloured segments. Cyan 'Training portion (1280)' on the left labelled 'weights actually update here'. Orange 'Validation (320)' in the middle labelled 'per-epoch monitoring (no updates)'. Red 'Test (400)' on the right labelled 'sealed until the very end'. A grey bracket above the first two segments marks 'X_train (1600 — fed to model.fit)' and a separate bracket above the third segment marks 'X_test (untouched)'.">
  <div class="vis-caption">Where <code>validation_split=0.2</code> carves the data inside <code>model.fit()</code>. The training portion is the only part where weights change; the validation portion is monitored each epoch; the test set is sealed until Exercise 4.</div>
</div>

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
