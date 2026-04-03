# Gate 3 Assessment — Stage 3 Architecture Review

> **Week:** 10  |  **Duration:** 45 min  |  **Format:** Written analysis  |  **Passing:** 70% of issues correctly identified with valid reasoning

---

## Overview

You are presented with a neural network architecture and its training results. The network has **7 intentional design and training issues**. Your task is to identify as many as you can, explain why each is a problem, and propose a fix.

This tests whether you can evaluate an AI solution's architecture — a critical skill for security architects assessing vendor claims or designing their own systems.

---

## The Scenario

A junior engineer on your team has built a neural network to classify network packets as `malicious` or `benign`. They've shared their code and training results with you for review. They're confused about why the model performs well on training data but fails in production testing.

---

## The Architecture

```python
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import numpy as np

# Dataset: 1,200 network packet samples, 30 features each
X, y = make_classification(
    n_samples=1200, n_features=30, n_informative=15,
    n_classes=2, weights=[0.5, 0.5], random_state=42
)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42               # <-- Issue area
)

# Model
model = keras.Sequential([
    keras.layers.Dense(512, activation='relu', input_shape=(30,)),   # <-- Issue area
    keras.layers.Dense(512, activation='relu'),                      # <-- Issue area
    keras.layers.Dense(512, activation='relu'),                      # <-- Issue area
    keras.layers.Dense(512, activation='relu'),                      # <-- Issue area
    keras.layers.Dense(1, activation='relu'),                        # <-- Issue area
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.1),              # <-- Issue area
    loss='mean_squared_error',                                       # <-- Issue area
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    epochs=500,
    batch_size=8,
    validation_split=0.0,                                            # <-- Issue area
)
```

## The Training Results

The engineer reports:

| Metric | Training Set | Production Test (100 new samples) |
|--------|-------------|----------------------------------|
| Accuracy | 99.8% | 61.2% |
| Loss (final epoch) | 0.001 | 2.34 |

> "The model gets 99.8% on training data but only 61.2% on new production data. I've tried training for more epochs but it doesn't help. What's wrong?"

---

## Your Task

Identify the issues in the architecture, training configuration, and evaluation setup. For each issue:

1. **State the issue** — what specifically is wrong
2. **Explain why it's a problem** — what effect does it have on the model
3. **Propose a fix** — what should be changed

**There are 7 intentional issues.** You need to find at least 5 (70%) to pass.

---

## Answer Template

Use this format for each issue you identify:

### Issue [N]: [Brief title]

**What's wrong:** [Describe the specific problem in the code or configuration]

**Why it's a problem:** [Explain the effect on model performance]

**Fix:** [What should be changed, with specific values or code]

---

## Answer Key

*For facilitator use. Remove this section before distributing to participants.*

### Issue 1: Wrong activation on output layer

**What's wrong:** The output layer uses `activation='relu'` for a binary classification task.

**Why it's a problem:** ReLU outputs values from 0 to infinity. For binary classification, the output should be a probability between 0 and 1. With ReLU, the model cannot produce proper probabilities and the loss function behaves incorrectly.

**Fix:** Change to `activation='sigmoid'` for binary classification.

---

### Issue 2: Wrong loss function

**What's wrong:** The loss function is `mean_squared_error`, which is for regression tasks.

**Why it's a problem:** MSE is designed for continuous outputs, not binary classification. It doesn't properly penalise confident wrong predictions. The gradients are weak for probabilities near 0.5, making training slow and unstable.

**Fix:** Change to `loss='binary_crossentropy'`, which is the correct loss for binary classification with a sigmoid output.

---

### Issue 3: Learning rate too high

**What's wrong:** `learning_rate=0.1` is extremely high for Adam optimizer.

**Why it's a problem:** A learning rate of 0.1 causes the optimizer to overshoot the loss minimum. Weights oscillate wildly instead of converging smoothly. This is a primary cause of unstable training and poor generalisation.

**Fix:** Use `learning_rate=0.001` (Adam's default) or `learning_rate=0.0001` for more stable training.

---

### Issue 4: Network is massively overparameterised

**What's wrong:** Four hidden layers of 512 neurons each for a dataset of only 1,200 samples with 30 features. The model has approximately 800,000+ parameters for 1,200 training samples.

**Why it's a problem:** The model has far more capacity than needed, making it trivially easy to memorise the training data (hence 99.8% training accuracy). It cannot generalise because it learned noise and sample-specific patterns, not real signal.

**Fix:** Reduce to 2 hidden layers with 64-128 neurons each. A network like `Dense(64) → Dense(32) → Dense(1)` is appropriate for 1,200 samples with 30 features.

---

### Issue 5: No regularisation (dropout, batch normalisation, or early stopping)

**What's wrong:** No dropout layers, no batch normalisation, and no early stopping callback. The model trains for a fixed 500 epochs without any mechanism to prevent overfitting.

**Why it's a problem:** Without regularisation, the overparameterised model is free to memorise the training data completely. Dropout randomly disables neurons during training, forcing the network to learn redundant representations. Early stopping halts training when validation performance stops improving.

**Fix:** Add `keras.layers.Dropout(0.3)` after each hidden layer. Add `keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)` to the fit call.

---

### Issue 6: No validation split during training

**What's wrong:** `validation_split=0.0` means the model has no way to monitor overfitting during training.

**Why it's a problem:** Without a validation set, you cannot detect when the model starts overfitting. Training loss will keep decreasing even as the model's ability to generalise degrades. Early stopping and model checkpointing both require validation data.

**Fix:** Set `validation_split=0.2` or use a separate validation set. This provides a signal for early stopping and helps diagnose overfitting by comparing training vs validation loss curves.

---

### Issue 7: Test set too small (10%)

**What's wrong:** `test_size=0.1` with only 1,200 samples means the test set has approximately 120 samples.

**Why it's a problem:** 120 samples is too few for a reliable performance estimate. With binary classification, random chance variation on 120 samples can swing accuracy by 5-10%. The 61.2% production accuracy may not even be statistically meaningful. Additionally, using only 10% for testing means the model is evaluated on a narrow slice of the data distribution.

**Fix:** Use `test_size=0.2` (standard 80/20 split). For a 1,200-sample dataset, 240 test samples provides a more reliable estimate. Consider k-fold cross-validation for even more robust evaluation.

---

## Scoring

| Issues Found | Score | Result |
|-------------|-------|--------|
| 7/7 | 100% | Exceptional |
| 6/7 | 86% | Strong pass |
| 5/7 | 71% | Pass |
| 4/7 | 57% | Fail — review Stage 3 material |
| 3 or fewer | <50% | Fail — retake after additional study |

**Partial credit:** An issue is counted as "found" if the participant correctly identifies the problem AND provides a valid explanation of why it matters. The proposed fix does not need to be perfect.

**Pass → Tier 2: AI Practitioner Certified**
