# Lesson 2.1 — Workshop Guide
## Feature Engineering: From Raw Logs to ML Features

> Read first: [../1_feature_engineering.md](../1_feature_engineering.md)
> Reference: [reference_solution.py](reference_solution.py)

## What This Workshop Covers

Raw firewall and NetFlow logs contain strings, IP addresses, timestamps, and protocol codes that sklearn cannot accept. In this workshop you will transform those raw logs into a numerical feature matrix suitable for ML: extracting behavioural metrics, encoding categorical columns, scaling, and validating the result.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_why_raw_logs_fail.md](exercise1_why_raw_logs_fail.md) | [exercise1_why_raw_logs_fail.py](exercise1_why_raw_logs_fail.py) | What raw logs look like and why sklearn can't use them |
| 2 | [exercise2_numeric_feature_extraction.md](exercise2_numeric_feature_extraction.md) | [exercise2_numeric_feature_extraction.py](exercise2_numeric_feature_extraction.py) | Derive bytes_per_second, packet_rate, duration, port risk scores |
| 3 | [exercise3_categorical_encoding.md](exercise3_categorical_encoding.md) | [exercise3_categorical_encoding.py](exercise3_categorical_encoding.py) | One-hot encode protocol, LabelEncoder vs OneHotEncoder, dummy trap |
| 4 | [exercise4_scaling_and_validation.md](exercise4_scaling_and_validation.md) | [exercise4_scaling_and_validation.py](exercise4_scaling_and_validation.py) | StandardScaler, MinMaxScaler, fit on train only, validate intuition |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson1_feature_engineering/workshop/exercise1_why_raw_logs_fail.py
```

## Next Lesson

[Lesson 2.2 — Random Forests](../../lesson2_random_forests/workshop/1_lab_guide.md)
