# Exercise 4 — Evaluate and Improve

> Read this guide fully before opening the lab.

## What You Will Learn

- How `model.evaluate()` measures performance on unseen test data
- How to convert raw sigmoid probabilities to class predictions
- How to read a `classification_report` on an imbalanced dataset
- How to compare a neural network's AUC against a logistic regression baseline

---

## Concept: model.evaluate() vs model.predict()

Both methods run a forward pass — no weight updates happen.

| Method | Returns | When to use |
|--------|---------|-------------|
| `model.evaluate(X, y)` | (loss, metric1, metric2, ...) | Get numeric performance on a labelled dataset |
| `model.predict(X)` | raw probabilities/scores | Get predictions for new inputs |

```python
# model.evaluate — for measuring performance
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

# model.predict — for generating predictions
probabilities = model.predict(X_test, verbose=0).flatten()
```

Note the `.flatten()` call: for a binary model, `predict()` returns shape `(n_samples, 1)`. Calling `.flatten()` converts it to shape `(n_samples,)` so it works with sklearn's metrics functions.

---

## Concept: Probabilities → Class Labels

The sigmoid output is a probability, not a class label. You apply a threshold to decide:

```python
# Standard threshold: 0.5
y_pred = (model.predict(X_test).flatten() > 0.5).astype(int)
```

```
Prediction pipeline:  raw output → threshold → class label

model.predict(X_test)     threshold=0.5       y_pred
┌────────────────┐        ┌───────────┐       ┌───┐
│ sample 0: 0.92 │ ─────► │ 0.92>0.5? │ YES ► │ 1 │  attack
│ sample 1: 0.14 │ ─────► │ 0.14>0.5? │ NO  ► │ 0 │  benign
│ sample 2: 0.67 │ ─────► │ 0.67>0.5? │ YES ► │ 1 │  attack
│ sample 3: 0.03 │ ─────► │ 0.03>0.5? │ NO  ► │ 0 │  benign
└────────────────┘        └───────────┘       └───┘
  shape: (n, 1)                                shape: (n,)
  call .flatten() first
```

This is identical to the threshold tuning concept from Lesson 1.3. A lower threshold (e.g., 0.3) increases recall but decreases precision for the positive class. In security work, you often lower the threshold to catch more attacks, accepting more false positives.

---

## Concept: AUC Is Better Than Accuracy on Imbalanced Data

With 90% benign, 10% attack:
- A model that predicts "benign" for everything gets **90% accuracy** — useless!
- AUC measures whether the model's **probability scores rank positives above negatives** — it's threshold-independent

```
AUC = 0.5  → Random classifier (no skill)
AUC = 0.7  → Reasonable baseline
AUC = 0.9  → Good model
AUC = 1.0  → Perfect ranking
```

Always report AUC (or average precision) alongside accuracy on imbalanced datasets.

> **Want to go deeper?** [Artificial neural network (Wikipedia)](https://en.wikipedia.org/wiki/Artificial_neural_network)

---

## Concept: Is Neural Network Better Than Logistic Regression?

On this dataset, results will be very close. Neural networks excel when:
- Data has complex non-linear relationships
- Dataset is large (100k+ samples)
- Input is high-dimensional (images, text, sequences)

On small structured datasets with good features, logistic regression often matches or beats neural networks. The lesson here: **always benchmark against a simple baseline**.

---

## What Each Task Asks You to Do

### Task 1 — model.evaluate() on the Test Set
Call `model.evaluate(X_test, y_test, verbose=0)` and print test loss and test accuracy. This is the only honest performance estimate — training and validation data were used to train or select the model.

### Task 2 — Classification Report
Get probabilities with `model.predict()`, convert to labels with threshold 0.5, then print `classification_report`. Focus on the minority class (attack/label=1) — is the F1 score acceptable for a security use case?

### Task 3 — AUC Comparison with Logistic Regression
Train a `LogisticRegression` baseline and compare test AUC to the neural network. Print which model achieves higher AUC and by how much. If the difference is under 0.01, the simpler model is probably the right choice.

### Task 4 (BONUS) — Deeper Network
Add a third hidden layer and compare AUC. On simple tabular datasets, deeper doesn't always win. Verify this experimentally.

---

## Common Mistakes

- **Evaluating on training data**: Always call `model.evaluate(X_test, y_test)` — not `X_train`.
- **Forgetting `.flatten()`**: `model.predict()` returns 2D shape `(n, 1)`. Pass `.flatten()` before comparing with y_test (1D).
- **Using `.predict_classes()`**: This method was removed in TF 2.6+. Use `(model.predict(X) > 0.5).astype(int)` instead.
- **Reporting only accuracy on imbalanced data**: With 90/10 split, a dummy classifier gets 90% accuracy. AUC and F1 on the minority class are the informative metrics.

---

## Now Open the Lab

[handson.md](handson.md)

## Next

[Lesson 3.10 Workshop — Dropout and Regularisation](../../02_dropout_regularisation/README.md)
