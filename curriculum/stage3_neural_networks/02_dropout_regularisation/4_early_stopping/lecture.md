# Early Stopping

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_patience_timeline.png" alt="Six rounded boxes in a horizontal row, each representing one epoch. Box 1 (green) labelled 'Epoch 15, val_loss = 0.170, ↓ best'. Boxes 2-5 (orange) labelled 'Epoch 16-19, val_loss = 0.172-0.180, count = 1-4'. Box 6 (red) labelled 'Epoch 20, val_loss = 0.182, STOP — restore epoch 15'. A gold curved arrow loops from the last box back to the first, with a label below 'restore_best_weights=True → rewind to epoch 15'.">
  <div class="vis-caption">Patience walkthrough. Each non-improving epoch increments a counter; when it reaches <code>patience=5</code>, training halts and <code>restore_best_weights=True</code> rewinds the model back to the epoch with the lowest val_loss.</div>
</div>

The model that gets restored is from epoch 15 (val_loss = 0.170) — the best it ever achieved.

---

## Concept: restore_best_weights

Without `restore_best_weights=True`:
- Model stops at epoch 23 but keeps epoch-23 weights
- Epoch 23 weights may be slightly overfit compared to epoch 18

With `restore_best_weights=True`:
- Model stops at epoch 23 but restores epoch-18 weights
- You get the best model for free, automatically

**Same training run, two final-state policies**

|  | `restore_best_weights=False` | `restore_best_weights=True` |
|---|---|---|
| Epoch where training stops | 23 | 23 |
| Weights kept at the end | epoch 23 (slightly overfit) | **epoch 18** (the best the model ever was) |
| Final `val_loss` | 0.184 | **0.169** |

The "stop epoch" and the "best epoch" are different things. `restore_best_weights=True` gives you the best model for free — there's almost no reason to leave it off.

<div class="lecture-visual">
  <img src="/static/lecture_assets/dr_early_stopping_curves.png" alt="Line chart of train and val loss over the epochs of a real EarlyStopping run. Cyan train loss falls smoothly. Red val loss falls then begins to climb. A large gold dot marks the best val_loss point. A grey dashed vertical line marks where training was actually halted, with an orange shaded region between the best epoch and the stop epoch labelled '5 non-improving epochs'.">
  <div class="vis-caption">Real lab run from <code>solution_early_stopping.py</code>. The gold dot is where the model is rewound to; the dashed line is where training actually halts after 5 consecutive non-improving epochs. Without early stopping the run would have wasted ~190 more epochs.</div>
</div>

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

## Common Mistakes

- **Monitoring train loss instead of val_loss**: If you monitor `loss` instead of `val_loss`, early stopping triggers when train loss stops improving — which may never happen (train loss keeps falling with overfitting). Always monitor `val_loss`.
- **Forgetting `restore_best_weights=True`**: Without it, you get the weights from the final epoch, not the best epoch. Always set it to True.
- **Setting patience=0 or patience=1**: With noisy val_loss curves, setting patience too low causes premature stopping. Use at least 3-5.
- **Not passing callbacks as a list**: `callbacks=early_stop` silently fails in some TF versions. Always use `callbacks=[early_stop]` (a list).
