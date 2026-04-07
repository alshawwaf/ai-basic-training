# Lesson 2.4 — Cross-Validation & Overfitting

---

## Concept: Does Your Model Actually Generalise?

A model that scores 99% on training data but 70% on new data is useless. It has **overfit** — memorised the training examples rather than learning general patterns.

This is the single most important concept to master before moving to neural networks.

---

## What is Overfitting?

```
Training accuracy: 99.8%
Test accuracy:     71.2%

-> The model memorised the training data. It has not learned.
```

As model complexity increases, training and validation accuracy diverge:

| Model complexity | Training accuracy | Validation accuracy | Diagnosis |
|-----------------|-------------------|---------------------|-----------|
| Low (simple) | Low | Low | Underfitting — model too simple |
| Medium | High | **Peaks here** | Sweet spot — best generalisation |
| High (complex) | Very high | Falls | Overfitting — model memorises noise |

> The gap between training and validation accuracy is the overfitting signal. When the gap opens up, the model has learned noise specific to the training set.

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

```
5-Fold Cross-Validation (k=5):

Fold 1: [EVAL][train][train][train][train]  -> score: 0.91
Fold 2: [train][EVAL][train][train][train]  -> score: 0.89
Fold 3: [train][train][EVAL][train][train]  -> score: 0.93
Fold 4: [train][train][train][EVAL][train]  -> score: 0.90
Fold 5: [train][train][train][train][EVAL]  -> score: 0.92

Final: 0.91 +/- 0.01  (stable = trustworthy)
```

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

## Next: Stage Project

**[intrusion_detector.py](../project/intrusion_detector.py):** Full network intrusion detection pipeline with proper cross-validation and evaluation.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

# Lesson 2.4 — Workshop Guide
## Overfitting and Cross-Validation

> Read first: [README.md](README.md)
> Reference: Each exercise has a matching solution file (e.g. `1_overfitting_demo/solution_overfitting_crossval.py`)

## What This Workshop Covers

You will deeply understand overfitting by watching a decision tree's train-vs-test accuracy diverge as depth increases, visualise the bias-variance tradeoff with three concrete models, then use k-fold cross-validation to get more reliable performance estimates than a single train/test split.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_overfitting_demo/lecture.md) | [handson.md](1_overfitting_demo/handson.md) | Sweep tree depth, watch train vs val accuracy diverge |
| 2 | [lecture.md](2_bias_variance/lecture.md) | [handson.md](2_bias_variance/handson.md) | Underfit vs good fit vs overfit — visualise all three |
| 3 | [lecture.md](3_kfold_crossval/lecture.md) | [handson.md](3_kfold_crossval/handson.md) | cross_val_score, 5-fold vs 10-fold, variance reduction |
| 4 | [lecture.md](4_validation_curve/lecture.md) | [handson.md](4_validation_curve/handson.md) | validation_curve(), automatic parameter sweep, plot |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage2_intermediate/04_overfitting_crossval/1_overfitting_demo/solution_overfitting_crossval.py
```
