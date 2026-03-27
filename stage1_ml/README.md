# Module 1 — Classic Machine Learning

## Goal
Understand what ML is, how models learn from data, and build your first classifiers using scikit-learn.

---

## The Core Idea

**Traditional programming:** you write the rules.
```python
if "free money" in email:
    mark_as_spam()
```

**Machine learning:** you show examples, and the computer figures out the rules.
```python
model.fit(emails, labels)    # show it 10,000 examples
model.predict(new_email)     # it now knows the rule itself
```

ML is pattern recognition at scale. Instead of hand-crafting rules, you hand the model data and let it extract patterns automatically. This is why it's so powerful in cybersecurity — attackers constantly change tactics, but their *statistical patterns* often persist.

---

## Three Types of ML

| Type | How it learns | Cyber example |
|------|--------------|---------------|
| **Supervised** | Labeled examples: "this is malware / this is not" | Malware classifier, phishing detector |
| **Unsupervised** | No labels — finds structure on its own | Anomaly detection in network traffic |
| **Reinforcement** | Learns by trial and error with rewards | Automated pentesting agents |

**Stage 1 focuses on supervised learning** — the most practical and widely used type.

---

## The ML Workflow

This loop applies to every single ML project you'll ever build:

```
1. Get data
2. Clean & prepare it
3. Split: training set + test set
4. Train a model on the training set
5. Evaluate on the test set
6. Tune → repeat from step 4
7. Deploy / use
```

The split in step 3 is critical: you never evaluate on data the model was trained on, because it would look artificially good. You need to test on data it has never seen — just like in real life.

---

## Key Vocabulary

| Term | Plain English |
|------|--------------|
| **Feature** | An input variable (e.g. URL length, number of dots in domain) |
| **Label / Target** | What you're predicting (e.g. phishing = 1, legit = 0) |
| **Training set** | Data used to teach the model |
| **Test set** | Held-out data used to evaluate the model |
| **Accuracy** | % of predictions that were correct |
| **Overfitting** | Model memorised training data but fails on new data |

---

## Lessons

### Lesson 1.1 — [What is ML?](what_is_ml.md)
**Script:** [1_concepts_and_data.py](1_concepts_and_data.py)
Learn to load, inspect, and visualise a dataset before training anything.

### Lesson 1.2 — [Linear Regression](linear_regression.md)
**Script:** [2_linear_regression.py](2_linear_regression.py)
Predict a continuous value: server response time from traffic load.

### Lesson 1.3 — [Logistic Regression](logistic_regression.md)
**Script:** [3_logistic_regression.py](3_logistic_regression.py)
Make binary decisions: phishing URL (yes/no).

### Lesson 1.4 — [Decision Trees](decision_trees.md)
**Script:** [4_decision_tree.py](4_decision_tree.py)
Classify network traffic as threat or benign using rule-based splits.

### Lesson 1.5 — [Model Evaluation](model_evaluation.md)
**Script:** [5_model_evaluation.py](5_model_evaluation.py)
Accuracy, precision, recall, F1, confusion matrix — what they mean and when to use each.

### Milestone — [Phishing URL Classifier](milestone_phishing.py)
**Script:** [milestone_phishing.py](milestone_phishing.py)
End-to-end project using a real phishing dataset.

---

## Dependencies

```bash
pip install pandas scikit-learn matplotlib seaborn
```
