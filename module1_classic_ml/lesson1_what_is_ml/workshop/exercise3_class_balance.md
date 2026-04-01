# Exercise 3 — Class Balance: The Silent Model Killer

> Read this guide fully before opening the exercise file.

---

## What You Will Learn

- What class imbalance is and why it matters more in security than anywhere else
- How to measure it and calculate the imbalance ratio
- Why a model with 95% accuracy can catch zero attacks
- How to calculate the **naive baseline** — the score you must beat just to prove the model is useful

---

## Concept: What Class Imbalance Is

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

In a classification dataset, **class imbalance** means one class has far more examples than another.

This is the rule in security ML, not the exception:

| Security dataset | Typical split |
|-----------------|---------------|
| Network intrusion | 99% normal, 1% attack |
| Phishing URLs | 85% legitimate, 15% phishing |
| Malware samples | 95% benign, 5% malicious |
| Fraud transactions | 99.8% legitimate, 0.2% fraud |

You will almost never encounter a naturally balanced security dataset in the real world. You must always check.

---

## Concept: The Naive Accuracy Trap

Here is a model that achieves 95% accuracy on a network intrusion dataset:

```python
def predict(connection):
    return "normal"   # always. no matter what.
```

It has learned nothing. It does not look at a single feature. It simply predicts the majority class every time.

If 95% of your data is labelled "normal," this strategy scores 95% — and catches **zero attacks**.

This is called the **naive baseline** — the score an unintelligent model achieves by always predicting the majority class. Any model you train must score meaningfully higher than this to be worth using.

The trap is easy to fall into:
- You train a model
- You see 95% accuracy
- You conclude the model is excellent
- You deploy it
- Every single attack goes undetected

This scenario has happened in real production systems. Understanding class imbalance before you train is not optional.

---

## Concept: The Metrics That Expose the Trap

Accuracy is:
```
(correct predictions) / (total predictions)
```

It does not distinguish between types of correct and types of wrong. You need metrics that do:

| Metric | What it measures |
|--------|-----------------|
| **Precision** | Of all the times the model said "attack" — how often was it right? |
| **Recall** (Sensitivity) | Of all the actual attacks — how many did the model catch? |
| **F1-score** | Harmonic mean of precision and recall — a single balanced number |

The naive model has:
- Accuracy: 95% ← looks good
- Recall (attack class): 0% ← catches nothing
- F1-score (attack class): 0% ← useless

You will calculate all of these properly in **Lesson 1.5 — Model Evaluation**. For now, learn to spot the problem before it happens.

---

## Concept: How to Measure Imbalance

```python
counts = df["target"].value_counts()

majority = counts.max()    # most frequent class
minority = counts.min()    # least frequent class
ratio    = majority / minority
```

Rule of thumb for how serious the imbalance is:

| Ratio | Severity | Action |
|-------|----------|--------|
| 1:1 – 2:1 | Balanced | None needed |
| 2:1 – 10:1 | Mild imbalance | Use `class_weight="balanced"` |
| 10:1 – 100:1 | Severe | Oversample minority (SMOTE) or undersample majority |
| > 100:1 | Extreme | Anomaly detection approaches; standard classifiers struggle |

---

## Concept: What You Can Do About It

You will apply these techniques in Module 2, but it helps to know they exist:

**`class_weight="balanced"` (easiest)**
Most scikit-learn classifiers accept this parameter. It automatically penalises errors on the minority class more heavily during training. Zero extra code.

```python
model = LogisticRegression(class_weight="balanced")
```

**Oversampling the minority class (SMOTE)**
Generates synthetic samples of the minority class to even out the distribution. The `imbalanced-learn` library provides this.

**Undersampling the majority class**
Randomly remove majority class samples. Simple but discards real data. Only use when data is plentiful.

**Anomaly detection framing**
Instead of classifying normal vs attack, model "what does normal look like?" and flag anything that deviates significantly. This sidesteps the label problem entirely — useful when you have very few attack examples.

---

## What Each Task Asks You to Do

### Task 1 — Count samples per class
`df["target"].value_counts().sort_index()` counts each class and sorts by label.

`.sort_index()` forces 0, 1, 2... order (rather than sorted by count). Always use this when you want to see the natural label ordering.

### Task 2 — Calculate the imbalance ratio
Get `.max()` and `.min()` from the counts Series. Divide. Print with context.

Then print what the naive accuracy would be for a hypothetical security dataset with a 19:1 ratio (95% vs 5%) — just arithmetic, no model needed.

### Task 3 — Simulate the security scenario
Create two variables: `normal_count = 950`, `attack_count = 50`.

Calculate:
- What percentage is normal? (950/1000 × 100)
- What accuracy does a model that always predicts "normal" achieve?
- What percentage of attacks does it catch?

Print these formatted clearly.

### Task 4 — ASCII bar chart
Loop over the class counts. For each class, print a bar of `#` characters proportional to its count. This builds the habit of visual sanity-checking.

---

## Expected Outputs at a Glance

**Task 1**
```
Samples per class:
0    178
1    182
2    177
3    183
4    181
5    182
6    181
7    179
8    174
9    180
```

**Task 2**
```
Majority class: 183 samples
Minority class: 174 samples
Imbalance ratio: 1.05 : 1
This dataset is well balanced.
```

**Task 3**
```
--- Simulated Security Dataset ---
Normal connections :  950  (95.0%)
Attack connections :   50   (5.0%)

A naive model (always predicts 'normal'):
  Accuracy       : 95.0%   <- looks great!
  Attacks caught :  0.0%   <- completely useless

This is why accuracy alone is a dangerous metric in security.
```

**Task 4** (approximate)
```
Class distribution:
0 | ########################################################## (178)
1 | ############################################################  (182)
...
8 | ####################################################### (174)
9 | ########################################################## (180)
```

---

## The Bigger Picture

This lesson uses a balanced dataset intentionally — it lets you learn the workflow without fighting imbalance at the same time. Starting in **Module 2** you will work with real imbalanced datasets.

In every lesson from this point on, the first check after loading data is: what is the class distribution? Before checking accuracy. Before looking at any other metric. Always.

---

## Now Open the Exercise File

[exercise3_class_balance_lab.md](exercise3_class_balance_lab.md)

---

## Next

[exercise4_visualise.md](exercise4_visualise.md) — plotting sample images, average class prototypes, and predicting where your model will struggle before it is even trained.
