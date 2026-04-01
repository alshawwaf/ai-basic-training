# Exercise 4 — Early Stopping

> Read this guide fully before opening the exercise file.

## What You Will Learn

- How `EarlyStopping` monitors validation loss and stops training automatically
- How `restore_best_weights=True` ensures the model ends with its best state
- How `patience` controls the balance between stopping too early vs too late
- How to read the training history to report on what actually happened

---

## Concept: Why Early Stopping?

Setting `epochs=200` without early stopping means the model trains for the full 200 epochs — even when val_loss stopped improving at epoch 25. The extra 175 epochs:
- Waste computation time
- Allow the model to slowly overfit (val_loss gradually worsens)

Early Stopping solves both problems automatically.

---

## Concept: How EarlyStopping Works

```python
keras.callbacks.EarlyStopping(
    monitor='val_loss',          # metric to watch
    patience=5,                  # wait this many non-improving epochs
    restore_best_weights=True,   # rewind to the best epoch
    min_delta=0.001              # minimum change to count as improvement
)
```

Timeline example with `patience=5`:

```
Epoch 15: val_loss = 0.168  ← new best, reset counter
Epoch 16: val_loss = 0.171  (counter = 1)
Epoch 17: val_loss = 0.173  (counter = 2)
Epoch 18: val_loss = 0.169  ← improvement! reset counter
Epoch 19: val_loss = 0.174  (counter = 1)
Epoch 20: val_loss = 0.177  (counter = 2)
Epoch 21: val_loss = 0.179  (counter = 3)
Epoch 22: val_loss = 0.181  (counter = 4)
Epoch 23: val_loss = 0.184  (counter = 5) ← STOP, restore epoch 18 weights
```

The model that gets restored is from epoch 18 (val_loss = 0.169) — the best it ever achieved.

---

## Concept: restore_best_weights

Without `restore_best_weights=True`:
- Model stops at epoch 23 but keeps epoch-23 weights
- Epoch 23 weights may be slightly overfit compared to epoch 18

With `restore_best_weights=True`:
- Model stops at epoch 23 but restores epoch-18 weights
- You get the best model for free, automatically

Always use `restore_best_weights=True` unless you have a specific reason not to.

---

## Concept: Choosing patience

| patience | Effect | Risk |
|----------|--------|------|
| 1–2 | Stops very aggressively | May stop before model converges |
| 5–10 | Standard balanced choice | None significant |
| 15–20 | Lenient, allows small plateaus | May allow gradual overfitting |
| 50+ | Essentially no early stopping | Defeats the purpose |

Rule of thumb: use `patience = max(5, 10% of expected_epochs)`.

> **Want to go deeper?** [Overfitting (Wikipedia)](https://en.wikipedia.org/wiki/Overfitting)

---

## What Each Task Asks You to Do

### Task 1 — Train with EarlyStopping
Create the callback with `patience=5, restore_best_weights=True`. Pass it in `callbacks=[early_stop]`. Set `epochs=200`. Print how many epochs actually ran — should be well under 200.

### Task 2 — Plot with Stop Marker
Add a vertical dashed line at the actual stop epoch and a gold dot at the minimum val_loss point. This visually demonstrates that training was halted at the right time.

### Task 3 — Training Efficiency Report
Calculate how many epochs were "saved" and estimate the time saved. On real datasets with millions of samples, early stopping can save hours of GPU time.

### Task 4 (BONUS) — Compare Patience Values
Train with patience=1, 5, and 20. Print a table of epochs run and final val_accuracy. patience=1 typically stops too early (lower accuracy); patience=20 allows more training but may overfit slightly.

---

## Expected Outputs at a Glance

```
TASK 1:
Restoring model weights from the end of the best epoch.
Stopped at epoch: ~25-35  (out of 200)
Final val_loss: ~0.160
Final val_acc:  ~0.945

TASK 3:
Scheduled epochs: 200
Epochs ran:       ~30
Epochs saved:     ~170
Estimated time saved: ~51 seconds

TASK 4 (BONUS):
  Patience | Epochs ran | Val accuracy
         1 |          8 |       ~0.930
         5 |         30 |       ~0.945
        20 |         55 |       ~0.943
```

---

## Common Mistakes

- **Monitoring train loss instead of val_loss**: If you monitor `loss` instead of `val_loss`, early stopping triggers when train loss stops improving — which may never happen (train loss keeps falling with overfitting). Always monitor `val_loss`.
- **Forgetting `restore_best_weights=True`**: Without it, you get the weights from the final epoch, not the best epoch. Always set it to True.
- **Setting patience=0 or patience=1**: With noisy val_loss curves, setting patience too low causes premature stopping. Use at least 3-5.
- **Not passing callbacks as a list**: `callbacks=early_stop` silently fails in some TF versions. Always use `callbacks=[early_stop]` (a list).

---

## Now Open the Exercise File

[exercise4_early_stopping_lab.md](exercise4_early_stopping_lab.md)

## Next

[Lesson 3.11 Workshop — Convolutional Networks](../../lesson11_convolutional_networks/workshop/1_lab_guide.md)
