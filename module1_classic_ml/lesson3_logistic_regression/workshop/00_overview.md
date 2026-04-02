# Lesson 1.3 — Workshop Guide
## Phishing URL Classifier

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_...py`)

## What This Workshop Covers

In this workshop you will build a logistic regression classifier that distinguishes phishing URLs from legitimate ones. You will move from linear regression's continuous outputs to classification's probability outputs, engineer security-relevant features from URL metadata, evaluate your model with a proper classification report and confusion matrix, and then tune the decision threshold to match operational priorities (catching every phish vs minimising analyst alert fatigue).

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_from_regression_to_classification.md](01_guide_from_regression_to_classification.md) | [01_lab_from_regression_to_classification.md](01_lab_from_regression_to_classification.md) | What makes it classification, the sigmoid function, probability outputs |
| 2 | [02_guide_feature_engineering_urls.md](02_guide_feature_engineering_urls.md) | [02_lab_feature_engineering_urls.md](02_lab_feature_engineering_urls.md) | Why URL features matter for phishing detection, dataset creation and inspection |
| 3 | [03_guide_train_and_evaluate.md](03_guide_train_and_evaluate.md) | [03_lab_train_and_evaluate.md](03_lab_train_and_evaluate.md) | LogisticRegression, StandardScaler, classification_report, confusion matrix |
| 4 | [04_guide_threshold_tuning.md](04_guide_threshold_tuning.md) | [04_lab_threshold_tuning.md](04_lab_threshold_tuning.md) | predict_proba(), why 0.5 is not always right, precision-recall tradeoff |

## Running a Solution

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson3_logistic_regression/workshop/01_solution_from_regression_to_classification.py
```

## Next Lesson

[Lesson 1.4 — Decision Trees](../../lesson4_decision_trees/workshop/00_overview.md)
