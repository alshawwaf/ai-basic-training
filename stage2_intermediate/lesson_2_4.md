# Lesson 2.4 — Cross-Validation & Overfitting

**Script:** [4_overfitting.py](4_overfitting.py)

---

## Concept: Does Your Model Actually Generalise?

A model that scores 99% on training data but 70% on new data is useless. It has **overfit** — memorised the training examples rather than learning general patterns.

This is the single most important concept to master before moving to neural networks.

---

## What is Overfitting?

```
Training accuracy: 99.8%
Test accuracy:     71.2%

→ The model memorised the training data. It has not learned.
```

The model has learned noise specific to the training set — patterns that don't exist in the real world. It's like a student who memorises exam answers without understanding the material.

### Signs of overfitting
- Large gap between training and test performance
- Model performance degrades significantly on new data
- Very complex model (deep tree, many parameters) on small dataset

---

## What is Underfitting?

The opposite problem: model is too simple to capture the real pattern.

```
Training accuracy: 65%
Test accuracy:     64%

→ Small gap — but both are poor. The model hasn't learned enough.
```

---

## The Bias-Variance Tradeoff

| | High Bias (underfit) | High Variance (overfit) |
|--|----------------------|------------------------|
| **Training error** | High | Low |
| **Test error** | High | High |
| **Gap** | Small | Large |
| **Fix** | More complex model | Regularisation, more data |

---

## Cross-Validation

Instead of a single train/test split, cross-validation gives you a more reliable estimate:

1. Split data into `k` folds (usually 5 or 10)
2. Train on k-1 folds, evaluate on the remaining fold
3. Repeat k times, rotating the evaluation fold
4. Final score = mean ± std across all folds

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"AUC: {scores.mean():.4f} ± {scores.std():.4f}")
```

A low standard deviation means your model is stable across different data splits.

---

## Regularisation (Reducing Overfitting)

### For Decision Trees / Random Forests
- `max_depth` — limit tree depth
- `min_samples_split` — require minimum samples per split
- `min_samples_leaf` — minimum samples per leaf

### For Logistic Regression
- `C` parameter — smaller C = stronger regularisation (penalises large coefficients)
- `penalty='l1'` or `penalty='l2'`

---

## What to Notice When You Run It

1. The overfitting demo — train vs test curve as tree depth increases
2. Cross-validation scores — compare to a single train/test split
3. The validation curve — find the sweet spot for `max_depth`

---

## Next: Milestone Project

**[milestone_intrusion.py](milestone_intrusion.py):** Full network intrusion detection pipeline with proper cross-validation and evaluation.
