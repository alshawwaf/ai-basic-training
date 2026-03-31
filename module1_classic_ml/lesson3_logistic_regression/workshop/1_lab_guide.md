# Lesson 1.3 — Workshop Guide
## Phishing URL Classifier

> Read first: [../3_logistic_regression.md](../3_logistic_regression.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

In this workshop you will build a logistic regression classifier that distinguishes phishing URLs from legitimate ones. You will move from linear regression's continuous outputs to classification's probability outputs, engineer security-relevant features from URL metadata, evaluate your model with a proper classification report and confusion matrix, and then tune the decision threshold to match operational priorities (catching every phish vs minimising analyst alert fatigue).

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_from_regression_to_classification.md](exercise1_from_regression_to_classification.md) | [exercise1_from_regression_to_classification.py](exercise1_from_regression_to_classification.py) | What makes it classification, the sigmoid function, probability outputs |
| 2 | [exercise2_feature_engineering_urls.md](exercise2_feature_engineering_urls.md) | [exercise2_feature_engineering_urls.py](exercise2_feature_engineering_urls.py) | Why URL features matter for phishing detection, dataset creation and inspection |
| 3 | [exercise3_train_and_evaluate.md](exercise3_train_and_evaluate.md) | [exercise3_train_and_evaluate.py](exercise3_train_and_evaluate.py) | LogisticRegression, StandardScaler, classification_report, confusion matrix |
| 4 | [exercise4_threshold_tuning.md](exercise4_threshold_tuning.md) | [exercise4_threshold_tuning.py](exercise4_threshold_tuning.py) | predict_proba(), why 0.5 is not always right, precision-recall tradeoff |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson3_logistic_regression/workshop/exercise1_from_regression_to_classification.py
```

## Next Lesson

[Lesson 1.4 — Decision Trees](../../lesson4_decision_trees/workshop/1_lab_guide.md)
