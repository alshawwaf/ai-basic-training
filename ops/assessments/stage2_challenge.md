# Gate 2 Assessment — Stage 2 Mini-Project

> **Week:** 7  |  **Duration:** 60 min  |  **Format:** Timed hands-on project  |  **Passing:** Working pipeline with correct metric interpretation

---

## Overview

You are given a **previously unseen** security dataset. In 60 minutes, build a complete ML pipeline from scratch — data exploration through model evaluation. This tests whether you can apply the Stage 1-2 workflow independently, without step-by-step guidance.

---

## The Scenario

Your SOC team has collected 6 months of DNS query logs. A threat analyst has manually labelled 3,000 queries as either `benign` or `dga` (domain generation algorithm — used by malware for command-and-control). Your task: build a classifier that detects DGA domains from their features.

---

## The Dataset

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Simulate DGA detection dataset
X, y = make_classification(
    n_samples=3000,
    n_features=12,
    n_informative=7,
    n_redundant=3,
    n_classes=2,
    weights=[0.70, 0.30],   # 70% benign, 30% DGA
    random_state=99,
    flip_y=0.05,            # 5% label noise (realistic)
)

feature_names = [
    "domain_length", "num_digits", "num_hyphens", "entropy",
    "vowel_ratio", "consonant_ratio", "max_consecutive_consonants",
    "num_subdomains", "tld_frequency_rank", "domain_age_days",
    "alexa_rank_log", "whois_registered"
]

df = pd.DataFrame(X, columns=feature_names)
df["label"] = y   # 0 = benign, 1 = dga
```

---

## Requirements

Complete all 6 steps. Print output for each step so the evaluator can verify your work.

### Step 1 — Exploratory Data Analysis (10 min)

Explore the dataset and print:
- Shape of the dataset
- Class distribution (counts and percentages)
- Summary statistics (`describe()`)
- Check for missing values
- Identify the 3 most correlated features with the label

**Print a brief interpretation:** Is the dataset balanced or imbalanced? Will accuracy be a reliable metric?

### Step 2 — Feature Engineering (10 min)

Create **at least 2 new features** derived from existing ones. Examples (you may choose your own):
- `digit_ratio` = `num_digits` / `domain_length`
- `length_entropy_interaction` = `domain_length` * `entropy`
- A binary feature: `is_long_domain` = 1 if `domain_length` > median, else 0

Print the updated feature list and shape after engineering.

### Step 3 — Preprocessing and Split (5 min)

- Apply `StandardScaler` to all numeric features
- Split into 80% train / 20% test using `train_test_split` with `stratify=y` and `random_state=42`
- Print the class distribution in both train and test sets to confirm stratification

### Step 4 — Train Two Models (10 min)

Train both of the following on the training set:
1. `RandomForestClassifier(n_estimators=100, random_state=42)`
2. `DecisionTreeClassifier(random_state=42)`

### Step 5 — Evaluate and Compare (15 min)

For **each model**, print:
- Confusion matrix
- Precision, recall, and F1 for the `dga` class
- Overall accuracy

Then print:
- **Feature importance** from the Random Forest (top 5 features)
- Which model performed better and why (2-3 sentences)

### Step 6 — Analysis Questions (10 min)

Print your answers to these questions:

1. **Why did you use `stratify=y` in the train/test split?**
2. **The Random Forest likely outperformed the Decision Tree. Why does ensembling help?**
3. **If this model were deployed in production, which metric matters most — precision or recall? Why?**
4. **One of the features you engineered: did it appear in the top-5 feature importances? What does that tell you?**
5. **A colleague suggests using accuracy as the primary metric. What do you tell them?**

---

## Evaluation Rubric

| Criterion | Pass | Fail |
|-----------|------|------|
| **EDA** | Shape, class distribution, statistics, missing values, and correlations printed with interpretation | Missing steps or no interpretation |
| **Feature Engineering** | At least 2 new features created with clear rationale | No new features, or features that don't make sense |
| **Preprocessing** | StandardScaler applied, stratified split, class distributions verified | No scaling, no stratification, or data leakage (scaling before split) |
| **Model Training** | Both RandomForest and DecisionTree trained on training set only | Models trained on full dataset, or only one model trained |
| **Evaluation** | Confusion matrix + precision/recall/F1 for both models, feature importances printed, comparison written | Only accuracy reported, or metrics for wrong class |
| **Analysis** | All 5 questions answered with correct, thoughtful reasoning | Missing answers or incorrect reasoning |

**All 6 criteria must be met to pass.**

---

## Common Mistakes That Cause Failure

| Mistake | Why It Fails |
|---------|-------------|
| Scaling the full dataset before splitting | Data leakage — test set statistics leak into training |
| Reporting only accuracy | Misses the class imbalance problem — the core lesson of Stages 1-2 |
| No feature engineering | Step 2 is required — tests whether you can create meaningful features |
| Training on the full dataset | No train/test split means no valid evaluation |
| Copying the Gate 1 code exactly | The dataset and features are different — you need to adapt |

---

## Grading Summary

| Component | Passing |
|-----------|---------|
| All 6 steps completed with correct output | Required |
| Analysis questions demonstrate understanding, not just code execution | Required |
| Code runs without errors | Required |

**Pass → Tier 1: AI Foundations Certified (both Gates 1 and 2 required)**
