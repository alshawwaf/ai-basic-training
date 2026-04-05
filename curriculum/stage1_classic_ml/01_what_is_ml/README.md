# What is Machine Learning?

Machine learning is a branch of computer science where systems **learn patterns from data** instead of being explicitly programmed with rules.

## Traditional Programming vs ML

| Traditional | Machine Learning |
|-------------|-----------------|
| You write rules | The algorithm finds rules |
| Input + Rules → Output | Input + Output → Rules |
| Breaks when rules change | Adapts when data changes |

A spam filter built with traditional programming needs a human to maintain a list of spam keywords. An ML spam filter learns from thousands of labelled emails and discovers its own patterns — including ones no human would think to check.

## The Three Ingredients

Every ML problem has the same three components:

1. **Data** — rows of observations, each described by numbers (features)
2. **Labels** — the answer you want the model to predict (supervised learning)
3. **Algorithm** — the method that finds patterns connecting features to labels

In this lesson you'll work with the **digits dataset**: 1,797 handwritten digit images, each stored as an 8x8 grid of pixel intensities (64 features), labelled 0–9.

## Why This Matters for Security

Security data follows the same structure:

| ML Concept | Security Equivalent |
|-----------|-------------------|
| Sample | A network flow, log entry, or executable |
| Feature | Packet size, entropy, byte frequency, timing |
| Label | Benign vs malicious |
| Model | Classifier that flags threats automatically |

The techniques you learn on digits — loading data, checking class balance, finding important features — transfer directly to security datasets.

## What You'll Learn

- What ML data looks like (features, labels, samples)
- Why some features are useless and how to find them
- The class imbalance problem and the accuracy trap
- How models see data — flat arrays of numbers, not images
- Why every concept maps to a real security scenario

## Next Lesson

[Lesson 1.2 — Linear Regression](../02_linear_regression/README.md) — build your first trained model.
