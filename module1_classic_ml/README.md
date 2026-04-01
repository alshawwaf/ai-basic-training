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

**Machine learning:** you show labelled examples, and the computer figures out the rules.

Imagine you have 10,000 emails that your security team has already reviewed. Each email is described by measurable properties — word count, number of links, whether there's an attachment, how old the sender's domain is. Each one has also been tagged: spam or legitimate. You hand all of that to a model and ask it to find the pattern.

```python
# emails: 10,000 rows, one per email
#         each row is a list of measurable properties
#         e.g. [word_count=42, num_links=8, has_attachment=1, domain_age_days=3]
#
# labels: the correct answer for each email, in the same order
#         e.g. [1, 0, 1, 1, 0, ...]  where 1 = spam, 0 = legitimate
#
# The connection between them is position:
#   emails[0] is the first email  →  labels[0] = 1 means that email is spam
#   emails[1] is the second email →  labels[1] = 0 means that email is legitimate
#   emails[2] is the third email  →  labels[2] = 1 means that email is spam
#   ...and so on for all 10,000
#
# There is no ID column linking them — the lists must stay in the same order.
# If you shuffle one without shuffling the other, the model learns nonsense.

# Once both lists are ready, you hand them to the model together.
# .fit() is the training step — the model reads through all 10,000 pairs
# and adjusts its internal numbers until its predictions match the labels.
model.fit(emails, labels)
# The model has now found the pattern:
# "emails with many links + a very young sender domain tend to be spam"
# It encodes that pattern as numbers (weights) — not as rules you wrote.

# .predict() is the deployment step — you give it one new email it has never seen.
# It applies the pattern it learned during .fit() and returns a label.
model.predict(new_email)
# → 1  (spam)
# You never told it what spam looks like — it worked it out from the examples.
```

ML is pattern recognition at scale. Instead of hand-crafting rules, you hand the model data and let it extract patterns automatically. This is why it works well in cybersecurity — attackers constantly change their tactics, but their *statistical patterns* often persist across campaigns.

> **Want to go deeper?** [Machine Learning — Wikipedia](https://en.wikipedia.org/wiki/Machine_learning) — a thorough overview of what ML is, how it works, and where it is applied.

---

## Three Types of ML

| Type | How it learns | Cyber example |
|------|--------------|---------------|
| **Supervised** | Labeled examples: "this is malware / this is not" | Malware classifier, phishing detector |
| **Unsupervised** | No labels — finds structure on its own | Anomaly detection in network traffic |
| **Reinforcement** | Learns by trial and error with rewards | Automated pentesting agents |

**Module 1 focuses on supervised learning** — the most practical and widely used type.

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning) — covers the full concept, with links to unsupervised and reinforcement learning for comparison.

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

> **Want to go deeper?** [Training, Validation, and Test Sets — Wikipedia](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets) — explains the purpose of each split and why evaluating on training data gives falsely optimistic results.

---

## Key Vocabulary

| Term | Plain English | Learn more |
|------|--------------|------------|
| **Feature** | An input variable (e.g. URL length, number of dots in domain) | [Feature Engineering — Wikipedia](https://en.wikipedia.org/wiki/Feature_engineering) |
| **Label / Target** | The answer the model predicts (e.g. phishing = 1, legit = 0) | |
| **Training set** | Data used to teach the model | |
| **Test set** | Held-out data used to evaluate the model honestly | |
| **Accuracy** | % of predictions that were correct — often misleading in security | [Precision and Recall — Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall) |
| **Overfitting** | Model memorised training data but fails on new data | [Overfitting — Wikipedia](https://en.wikipedia.org/wiki/Overfitting) |
| **Underfitting** | Model is too simple to capture the real pattern | ↑ same article |
| **Class imbalance** | One label appears far more often — normal traffic vastly outnumbers attacks | [Imbalanced Data — Wikipedia](https://en.wikipedia.org/wiki/Oversampling_and_undersampling_in_data_analysis) |

---

## Lessons

### Lesson 1.1 — [What is ML?](1_what_is_ml.md)
**Script:** [1_concepts_and_data.py](1_concepts_and_data.py)
Learn to load, inspect, and visualise a dataset before training anything.

### Lesson 1.2 — [Linear Regression](2_linear_regression.md)
**Script:** [2_linear_regression.py](2_linear_regression.py)
Predict a continuous value: server response time from traffic load.

### Lesson 1.3 — [Logistic Regression](3_logistic_regression.md)
**Script:** [3_logistic_regression.py](3_logistic_regression.py)
Make binary decisions: phishing URL (yes/no).

### Lesson 1.4 — [Decision Trees](4_decision_trees.md)
**Script:** [4_decision_tree.py](4_decision_tree.py)
Classify network traffic as threat or benign using rule-based splits.

### Lesson 1.5 — [Model Evaluation](5_model_evaluation.md)
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
