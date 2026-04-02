# Lesson 2.1 — Workshop Guide
## Feature Engineering: From Raw Logs to ML Features

> Read first: [../notes.md](../notes.md)
> Reference: Each exercise has a matching `_solution_` file (e.g. `01_solution_why_raw_logs_fail.py`)

## What This Workshop Covers

Raw firewall and NetFlow logs contain strings, IP addresses, timestamps, and protocol codes that sklearn cannot accept. In this workshop you will transform those raw logs into a numerical feature matrix suitable for ML: extracting behavioural metrics, encoding categorical columns, scaling, and validating the result.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_why_raw_logs_fail.md](01_guide_why_raw_logs_fail.md) | [01_lab_why_raw_logs_fail.md](01_lab_why_raw_logs_fail.md) | What raw logs look like and why sklearn can't use them |
| 2 | [02_guide_numeric_feature_extraction.md](02_guide_numeric_feature_extraction.md) | [02_lab_numeric_feature_extraction.md](02_lab_numeric_feature_extraction.md) | Derive bytes_per_second, packet_rate, duration, port risk scores |
| 3 | [03_guide_categorical_encoding.md](03_guide_categorical_encoding.md) | [03_lab_categorical_encoding.md](03_lab_categorical_encoding.md) | One-hot encode protocol, LabelEncoder vs OneHotEncoder, dummy trap |
| 4 | [04_guide_scaling_and_validation.md](04_guide_scaling_and_validation.md) | [04_lab_scaling_and_validation.md](04_lab_scaling_and_validation.md) | StandardScaler, MinMaxScaler, fit on train only, validate intuition |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module2_intermediate/lesson1_feature_engineering/workshop/01_solution_why_raw_logs_fail.py
```

## Next Lesson

[Lesson 2.2 — Random Forests](../../lesson2_random_forests/workshop/00_overview.md)
