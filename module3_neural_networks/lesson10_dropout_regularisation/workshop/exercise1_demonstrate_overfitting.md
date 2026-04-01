# Exercise 1 — Demonstrate Overfitting

> Read this guide fully before opening the exercise file.

## What You Will Learn

- How too much model capacity relative to training data causes overfitting
- How to read the diverging loss curves that signal overfitting
- How to measure the overfitting gap numerically
- How going deeper amplifies the problem

---

## Concept: Model Capacity and Overfitting

**Model capacity** = how many distinct functions the model can represent. A network with more parameters has higher capacity — it can fit more complex patterns.

With 3 × Dense(256) layers and 10 input features, this model has ~133,000 parameters being trained on 1,600 samples. That's 83 parameters per training sample. The model has enough capacity to memorise every training example, including the random noise in the data.

```
Too much capacity:
  model learns: "training sample #47 had these exact values → label=1"
  Real pattern:  "high connection_rate AND many failed_connections → attack"

Result:
  Training accuracy: 99.5%   (memorised examples)
  Validation accuracy: 92%   (noise patterns don't generalise)
```

---

## Concept: The Diverging Loss Signature

In a healthy training run, train loss and val loss both decrease and track each other:

```
Loss
  0.6 | \  val
      |  \.____
  0.3 |   \____   train and val converge
      |        \__________
  0.1 |                    \_____
      +---+---+---+---+---+---> Epoch
```

Overfitting signature — val loss stops falling, then rises:

```
Loss
  0.6 | \  train          val
      |  \               /____  <- divergence here
  0.3 |   \_______      /
      |           \____/
  0.1 |                train continues falling
      +---+---+---+---+---+---> Epoch
         10  20  30  40  50
```

The point where val loss hits its minimum is the ideal stopping point. Training beyond that point makes the model worse on unseen data.

---

## What Each Task Asks You to Do

### Task 1 — Build and Train the Large Network
Build 3 × Dense(256) with sigmoid output, train for 50 epochs with no regularisation. Print the total parameter count (should be >130,000) and final train vs val accuracy.

### Task 2 — Plot the Diverging Curves
Plot train loss vs val loss on a single graph. You should see val loss start rising after ~10-20 epochs while train loss continues falling. This is the core overfitting signal.

### Task 3 — Measure the Gap
Print the numerical overfitting gap. An accuracy gap above 0.03 is significant. A loss gap above 0.05 is clearly overfitting. These numbers give you a baseline to compare against in exercises 2-4.

### Task 4 (BONUS) — More Depth = More Overfit
Add 2 more Dense(256) layers (5 total) and compare the final gap. Deeper without regularisation is worse. Record both gaps — you'll apply fixes in the next exercises.

---

## Expected Outputs at a Glance

```
TASK 1:
Total parameters: 133,633
Final train accuracy: ~0.990
Final val accuracy:   ~0.938

TASK 3:
Train accuracy:  ~0.990  | Val accuracy:  ~0.938
Accuracy gap (train - val): ~0.052
Loss gap (val - train):     ~0.110
```

---

## Common Mistakes

- **Training for too few epochs**: With only 10 epochs you may not see divergence. Use 50.
- **Using small Dense layers**: Dense(16)×3 won't overfit much. You need Dense(256) to see the effect clearly.
- **Forgetting to set random seed**: Without `tf.random.set_seed(42)` and `np.random.seed(42)`, results vary significantly between runs.

---

## Now Open the Exercise File

[exercise1_demonstrate_overfitting.py](exercise1_demonstrate_overfitting.py)

## Next

[exercise2_add_dropout.md](exercise2_add_dropout.md)
