# Exercise 1 — The Accuracy Trap

> Back to [00_overview.md](00_overview.md)

## What You Will Learn

- Why accuracy is misleading when classes are imbalanced
- What `DummyClassifier` is and why it exposes accuracy's weakness
- How to immediately spot the accuracy trap by checking recall for the minority class
- Why security datasets are almost always imbalanced

---

## Concept: Class Imbalance in Security

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

In most real-world security monitoring, attacks are rare:

| Dataset | Typical attack rate |
|---------|-------------------|
| Intrusion detection (CICIDS) | 1–20% |
| Fraud detection | 0.1–1% |
| Phishing detection | 5–30% |
| Malware in enterprise telemetry | 0.01–5% |

If 95% of events are benign and 5% are attacks, a model that simply predicts "benign" for every single event achieves **95% accuracy** — without ever detecting a single attack. This is the accuracy trap.

---

## Concept: DummyClassifier

sklearn's `DummyClassifier` makes predictions using simple rules, ignoring the input features entirely:

| Strategy | Behaviour |
|----------|----------|
| `most_frequent` | Always predicts the most common class |
| `stratified` | Predicts randomly in proportion to class frequencies |
| `uniform` | Predicts each class with equal probability |
| `constant` | Always predicts a specified constant |

`most_frequent` on a 95/5 dataset always predicts "benign" → 95% accuracy. This is the baseline that any real model must beat — and it must beat it on metrics that matter (recall on attacks), not just accuracy.

---

## Concept: The Real Question

When you report model performance for a security tool, the question is not:
> "What percentage of all events did we classify correctly?"

The question is:
> "Of all the actual attacks, how many did we catch?"
> "Of all the alerts we raised, how many were real attacks?"

These are **recall** and **precision** for the attack class — covered in Exercise 3.

---

## Concept: Spotting the Trap Immediately

When you see a classification report with high accuracy but near-zero recall for the minority (attack) class:

```
              precision  recall  f1-score  support
benign          0.95      1.00      0.97      950
attack          0.00      0.00      0.00       50
accuracy                            0.95     1000
```

This tells you immediately: the model is useless for its security purpose. `accuracy = 0.95` is a lie.

---

## What Each Task Asks You to Do

### Task 1 — Create the Imbalanced Dataset
Generate 10,000 network events: 9,500 benign and 500 attacks (5% attack rate). Print the class distribution to confirm the imbalance.

### Task 2 — Train a DummyClassifier
Fit a `DummyClassifier(strategy='most_frequent')` on the training data. Print its accuracy on the test set. Then print the classification report. Show that recall for attacks is 0.

### Task 3 — Compare to a Real Classifier
Train a LogisticRegression on the same data. Compare accuracy AND recall-on-attacks between DummyClassifier and LogisticRegression.

### Task 4 (BONUS) — Why 95% is Not Impressive
Calculate: if there are 10,000 real network events per day and the DummyClassifier is deployed, how many attacks (at 5% rate) go undetected? Print the number. Then calculate the same for LogisticRegression with recall=0.75.

---

## Expected Outputs

```
TASK 1 — Dataset:
benign: 9500 (95.0%)
attack:  500  (5.0%)

TASK 2 — DummyClassifier:
Accuracy: 0.950  ← looks impressive!

Classification Report:
              precision  recall  f1-score  support
benign          0.95      1.00      0.97     1900
attack          0.00      0.00      0.00      100
accuracy                            0.95     2000

TASK 3 — DummyClassifier vs LogisticRegression:
              DummyClassifier  LogisticRegression
Accuracy           0.950            0.962
Attack Recall      0.000            0.720
The LR model catches 72 attacks; Dummy catches 0.

TASK 4 (BONUS):
Daily attacks (5% of 10,000): 500
DummyClassifier  missed: 500 / 500 (100%)
LogisticRegression missed: 140 / 500 (28%)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Reporting only accuracy for a security model | Hides complete failure to detect attacks | Always report recall for attack class |
| Not checking class balance before modelling | Accuracy trap | Always call `value_counts()` first |
| Using DummyClassifier as the final model | 0% attack detection rate | DummyClassifier is only a baseline, not a solution |
| Forgetting `zero_division=0` in precision_score | ZeroDivisionWarning when precision=0 | Pass `zero_division=0` |

---

> Next: [02_guide_confusion_matrix.md](02_guide_confusion_matrix.md)
