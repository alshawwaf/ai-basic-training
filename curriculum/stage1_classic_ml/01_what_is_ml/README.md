# What is Machine Learning?

Machine learning is a branch of computer science where systems **learn patterns from data** instead of being explicitly programmed with rules.

## Traditional Programming vs ML

| Traditional | Machine Learning |
|-------------|-----------------|
| You write rules | The algorithm finds rules |
| Input + Rules → Output | Input + Output → Rules |
| Breaks when rules change | Adapts when data changes |

A spam filter built with traditional programming needs a human to maintain a list of spam keywords. An ML spam filter learns from thousands of labelled emails and discovers its own patterns — including ones no human would think to check.

## The Four Ingredients

Every ML problem has the same four components:

1. **Data** — rows of observations, each described by numbers (features)
2. **Labels** — the answer you want the model to predict (supervised learning)
3. **Algorithm** — the method that finds patterns connecting features to labels
4. **Model** — the bag of tuned numbers the algorithm produces, which you save and use to make predictions

Think of the **algorithm as the recipe and the model as the cake.** The algorithm runs once (during `.fit()`), looks at all the data, and tunes a set of numeric parameters until they describe the patterns it found. Those tuned numbers ARE the model — for linear regression they are literally two numbers (`weight` and `bias`); for the digits classifier you'll build below, they are around 640 numbers (one weight per pixel, per digit class). After training, the algorithm is done. The numbers are what you save to disk and ship to production.

> Want to physically *be* the algorithm? In Lesson 1.2 you can drag two sliders to set `weight` and `bias` by hand and watch the error grow and shrink — see [`02_linear_regression/0_interactive_intro/explore_model_knobs.py`](../02_linear_regression/0_interactive_intro/explore_model_knobs.py).

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
