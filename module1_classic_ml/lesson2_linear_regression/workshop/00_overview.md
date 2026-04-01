# Lesson 1.2 — Workshop Guide
## Predicting Server Response Time and Detecting DoS Anomalies

> Read first: [../notes.md](../notes.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

In this workshop you will build a linear regression model that predicts a server's response time from its requests-per-second load. Along the way you will learn how to split data properly, fit a model, interpret the slope and intercept in physical terms, and evaluate your model with standard error metrics. The final exercise turns that model into a security tool: a baseline that flags anomalous response times that could indicate a Denial-of-Service attack.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_understanding_regression.md](01_guide_understanding_regression.md) | [01_lab_understanding_regression.md](01_lab_understanding_regression.md) | Regression vs classification, the dataset, visualising the relationship |
| 2 | [02_guide_train_test_split.md](02_guide_train_test_split.md) | [02_lab_train_test_split.md](02_lab_train_test_split.md) | Why we split data, train_test_split(), the danger of evaluating on training data |
| 3 | [03_guide_fit_and_predict.md](03_guide_fit_and_predict.md) | [03_lab_fit_and_predict.md](03_lab_fit_and_predict.md) | model.fit(), model.predict(), slope and intercept, visualise the line |
| 4 | [04_guide_evaluate_regression.md](04_guide_evaluate_regression.md) | [04_lab_evaluate_regression.md](04_lab_evaluate_regression.md) | MSE, RMSE, MAE, R², interpret results, build a security baseline |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module1_classic_ml/lesson2_linear_regression/workshop/exercise1_understanding_regression.py
```

## Next Lesson

[Lesson 1.3 — Logistic Regression](../../lesson3_logistic_regression/workshop/00_overview.md)
