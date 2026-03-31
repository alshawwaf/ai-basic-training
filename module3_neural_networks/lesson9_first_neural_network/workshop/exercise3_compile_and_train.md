# Exercise 3 — Compile and Train

> **Exercise file:** [exercise3_compile_and_train.py](exercise3_compile_and_train.py)
> Read this guide fully before opening the exercise file.

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

One **epoch** = one complete pass through all training data.
One **batch** = `batch_size` samples processed before updating weights.

With 1,600 training samples and `batch_size=32`:
- 1600 / 32 = **50 gradient updates per epoch**

With `batch_size=1600` (one big batch):
- **1 gradient update per epoch** — slow learning

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

```
Accuracy
  1.0 |                    train ________
      |                  ./
  0.9 |            ______/  <- val plateaus
      |          ./
  0.8 |        ./
      |      ./
  0.7 |    ./
      |  ./
  0.6 |./
      +--+--+--+--+--+--+--+--+--+---> Epoch
         5  10  15  20

Three phases:
  1-5:   Rapid improvement — model learns obvious patterns
  5-15:  Slowing improvement — learning fine details
  15+:   Plateau or divergence — risk of overfitting
```

When `val_loss` starts rising while `loss` keeps falling — stop training. This is the overfitting signal.

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

## Expected Outputs at a Glance

```
TASK 1 (last few epochs):
Epoch 18/20: loss: 0.152 — accuracy: 0.952 — val_loss: 0.172 — val_accuracy: 0.941
Epoch 19/20: loss: 0.149 — accuracy: 0.952 — val_loss: 0.171 — val_accuracy: 0.941
Epoch 20/20: loss: 0.147 — accuracy: 0.953 — val_loss: 0.170 — val_accuracy: 0.941

TASK 2:
Final train accuracy: ~0.953
Final val accuracy:   ~0.941
Overfit gap: ~0.012

TASK 4 (BONUS):
Best val accuracy: ~0.946 at epoch ~18
Final val accuracy: ~0.939
Difference (overtraining effect): ~0.007
```

---

## Common Mistakes

- **Not storing the return value of model.fit()**: `model.fit(...)` without assignment — you lose the history and can't plot curves.
- **Printing from `history.history` before training**: `history` doesn't exist until after `model.fit()` completes.
- **Confusing validation_split with the test set**: The validation portion of X_train and X_test are different things. Never evaluate on X_test until the very end.
- **Plotting loss on wrong axis**: Loss and accuracy have different scales. Always put them on separate subplots.

---

## Now Open the Exercise File

[exercise3_compile_and_train.py](exercise3_compile_and_train.py)

## Next

[exercise4_evaluate_and_improve.md](exercise4_evaluate_and_improve.md)
