# Gate 1 Assessment — Stages 0 and 1

> **Week:** 4  |  **Duration:** 60 min  |  **Format:** Quiz (30 min) + Code Challenge (30 min)  |  **Passing:** 7/10 quiz + working code

---

## Part A — Knowledge Quiz (10 questions, 30 minutes)

*Answer each question. For multiple-choice, select the single best answer.*

---

### Q1. AI Positioning

A customer says: "We already have SIEM correlation rules. Why do we need AI?"

Which response best demonstrates technical depth?

- A) "AI is more advanced than rules and will replace your SIEM."
- B) "SIEM rules catch known patterns precisely. ML models generalise to variations and scale to high-dimensional signals. The best deployments layer both — ML scores and prioritises SIEM alerts."
- C) "Our AI uses deep learning which is much more powerful than rules."
- D) "You don't need AI if your rules are working."

---

### Q2. ML Fundamentals

In supervised machine learning, what is the relationship between features (X) and labels (y)?

- A) Features are the outputs the model predicts; labels are the inputs
- B) Features are the measurable inputs; labels are the answers the model learns to predict
- C) Features and labels are the same thing — they describe the dataset
- D) Features are only used during testing; labels are only used during training

---

### Q3. Train/Test Split

Why must you evaluate a model on data it has never seen during training?

- A) Training data is usually corrupted and unreliable
- B) Evaluating on training data measures memorisation, not the model's ability to generalise to new data
- C) The test set is always larger and more representative
- D) It is a convention with no practical impact on results

---

### Q4. Class Imbalance

You are building a malware classifier. Your dataset has 9,500 benign samples and 500 malicious samples. A model that predicts "benign" for every input achieves 95% accuracy.

Why is this model useless despite its high accuracy?

- A) 95% accuracy is too low for production use
- B) The model has never learned to detect malware — it misses 100% of malicious samples. Accuracy is misleading when classes are imbalanced.
- C) The model is overfitting to the training data
- D) The test set is too small to draw conclusions

---

### Q5. Model Evaluation

A phishing detection system has the following confusion matrix:

|  | Predicted: Legit | Predicted: Phish |
|--|-----------------|-----------------|
| **Actual: Legit** | 8,900 | 100 |
| **Actual: Phish** | 200 | 800 |

Calculate the **precision** for the phishing class (Predicted: Phish).

- A) 80%
- B) 89%
- C) 88.9%
- D) 90%

*Show your work:*

---

### Q6. Linear vs Logistic Regression

What is the key difference between linear regression and logistic regression?

- A) Linear regression is for small datasets; logistic regression is for large datasets
- B) Linear regression predicts a continuous value; logistic regression predicts a probability for classification
- C) Linear regression uses features; logistic regression does not
- D) They are the same algorithm with different names

---

### Q7. Decision Trees

What makes decision trees particularly useful in security applications compared to other ML models?

- A) They are always more accurate than other models
- B) They are inherently explainable — you can read the exact rules the model learned, which supports audit and compliance requirements
- C) They require no training data
- D) They cannot overfit

---

### Q8. Overfitting

A model achieves 99% accuracy on the training set but only 65% on the test set. What is this a sign of?

- A) Underfitting — the model is too simple
- B) Overfitting — the model has memorised the training data instead of learning generalisable patterns
- C) Class imbalance in the test set
- D) A bug in the evaluation code

---

### Q9. AI Claim Evaluation

A vendor claims their product uses "proprietary AI trained on trillions of events" for threat detection. Using the 5-question evaluation framework, which question would MOST effectively reveal whether this claim has substance?

- A) "How many customers do you have?"
- B) "What is the false positive rate on a standardised benchmark, and how does it compare to a rule-only baseline?"
- C) "Is your AI better than ChatGPT?"
- D) "How much does it cost?"

---

### Q10. Competitor Analysis

A customer is evaluating Darktrace for network anomaly detection. Based on your understanding of Darktrace's AI approach, what is the most important limitation to raise?

- A) Darktrace doesn't use any real AI
- B) Darktrace uses unsupervised anomaly detection, which flags anything unusual — including legitimate business changes. This leads to high false positive rates, especially in the first months. Additionally, slow persistent attackers can poison the baseline.
- C) Darktrace is too expensive
- D) Darktrace only works on Windows

---

## Part A — Answer Key

*For facilitator use. Remove this section before distributing to participants.*

| Question | Correct Answer | Explanation |
|----------|---------------|-------------|
| Q1 | **B** | Acknowledges SIEM value, explains ML's complementary strength, recommends layering. Demonstrates ACE-style response. |
| Q2 | **B** | Features are inputs (pixel values, URL length, etc.); labels are the target variable the model predicts. |
| Q3 | **B** | Evaluating on training data measures memorisation. The test set measures generalisation — the model's performance on unseen data. |
| Q4 | **B** | With 95% class imbalance, a naive model predicting the majority class achieves high accuracy but zero recall on the minority class. Precision, recall, and F1 are the appropriate metrics. |
| Q5 | **C** | Precision = TP / (TP + FP) = 800 / (800 + 100) = 88.9%. The 100 false positives (legit emails flagged as phish) reduce precision. |
| Q6 | **B** | Linear regression outputs a continuous number (e.g., predicted response time). Logistic regression applies a sigmoid function to output a probability between 0 and 1 for binary classification. |
| Q7 | **B** | Decision trees produce human-readable rules. In security, this explainability is critical for compliance, audit trails, and analyst trust. |
| Q8 | **B** | Large gap between training and test performance is the classic sign of overfitting. The model learned noise and specifics of the training data rather than generalisable patterns. |
| Q9 | **B** | "What metric, on what benchmark, compared to what baseline?" directly applies questions 3 and 4 of the evaluation framework and forces a concrete, verifiable answer. |
| Q10 | **B** | Darktrace's unsupervised approach is genuinely different but comes with high FP rates and baseline poisoning risk. This is technically accurate and actionable for the customer. |

**Scoring:** 7/10 correct = pass.

---

## Part B — Code Challenge (30 minutes)

### Scenario

You are given a dataset of network connection logs. Each row is a connection with features describing it, and a label indicating whether the connection is `normal` or `attack`.

Your task: build a complete ML pipeline and answer the analysis questions.

### The Dataset

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Generate a synthetic network intrusion dataset
X, y = make_classification(
    n_samples=2000,
    n_features=10,
    n_informative=6,
    n_redundant=2,
    n_classes=2,
    weights=[0.85, 0.15],   # 85% normal, 15% attack — imbalanced
    random_state=42,
)

feature_names = [
    "duration", "bytes_sent", "bytes_received", "packets",
    "src_port_entropy", "dst_port_entropy", "flag_count",
    "protocol_type", "failed_logins", "connection_rate"
]

df = pd.DataFrame(X, columns=feature_names)
df["label"] = y   # 0 = normal, 1 = attack
```

### Instructions

Write a Python script that:

1. **Loads the dataset** using the code above
2. **Performs EDA** — print the shape, class distribution, and basic statistics
3. **Splits** the data into 80% training / 20% test
4. **Trains** a `DecisionTreeClassifier` on the training set
5. **Evaluates** on the test set — print the confusion matrix, precision, recall, and F1 score for the `attack` class
6. **Answers these questions** (print your answers in the script):
   - Is the dataset balanced or imbalanced?
   - Why would accuracy alone be a poor metric for this dataset?
   - What is the recall for the `attack` class, and why does it matter in security?

### Evaluation Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| Data loaded and EDA printed | Shape, class counts, and describe() visible | Missing or incomplete |
| Train/test split correct | 80/20 split with no data leakage | Evaluated on training data, or no split |
| Model trained and predictions generated | DecisionTreeClassifier fit on train, predict on test | Wrong model, or fit on full dataset |
| Metrics computed correctly | Confusion matrix + precision + recall + F1 for attack class | Only accuracy reported, or metrics for wrong class |
| Analysis questions answered | All 3 questions answered with correct reasoning | Missing or incorrect reasoning |

### Sample Output (approximate)

```
Dataset shape: (2000, 11)
Class distribution:
  0 (normal): 1700
  1 (attack):  300

Confusion matrix:
[[330  10]
 [ 12  48]]

Attack class metrics:
  Precision: 0.83
  Recall:    0.80
  F1 Score:  0.81

Analysis:
- The dataset is imbalanced (85% normal, 15% attack)
- Accuracy would be misleading because a model predicting all-normal gets 85%
- Recall for attack = 0.80 means 20% of attacks are missed (false negatives),
  which in security could mean undetected breaches
```

*Exact numbers will vary based on random_state and model. The reasoning matters more than the precise values.*

---

## Grading Summary

| Component | Weight | Passing |
|-----------|--------|---------|
| Part A — Quiz | 50% | 7/10 correct |
| Part B — Code Challenge | 50% | All 5 criteria met |

**Pass → Tier 1: AI Foundations Certified (pending Gate 2)**
