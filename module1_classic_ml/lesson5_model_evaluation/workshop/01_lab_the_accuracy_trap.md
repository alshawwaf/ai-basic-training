# Lab -- Exercise 1: The Accuracy Trap

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_the_accuracy_trap.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, recall_score
from sklearn.preprocessing import StandardScaler
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_total  = 10_000
n_attack = 500      # 5% attack rate
n_benign = n_total - n_attack
benign_data = np.column_stack([
    np.random.normal(10, 3, n_benign),
    np.random.normal(5000, 1500, n_benign),
    np.random.poisson(3, n_benign)
])
attack_data = np.column_stack([
    np.random.normal(80, 30, n_attack),
    np.random.normal(500, 300, n_attack),
    np.random.poisson(30, n_attack)
])
X = np.vstack([benign_data, attack_data])
y = np.array([0]*n_benign + [1]*n_attack)
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Step 4: Inspect the Class Imbalance

Count the number of benign and attack samples in the full dataset. Print each with the percentage. Confirm: attack rate is 5%.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Class imbalance in the dataset")
print("=" * 60)
unique, counts = np.unique(y, return_counts=True)
total = len(y)
for cls, count in zip(unique, counts):
    name = "benign" if cls == 0 else "attack"
    print(f"{name}: {count:5d} ({count/total*100:.1f}%)")
```

Run your file. You should see:
```
benign:  9500 (95.0%)
attack:   500  (5.0%)
```

---

## Step 5: Train DummyClassifier and Show the Trap

Fit DummyClassifier(strategy='most_frequent') on X_train / y_train. Print its accuracy on X_test / y_test. Print the full classification_report.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — DummyClassifier: the accuracy trap")
print("=" * 60)
dummy = DummyClassifier(strategy='most_frequent', random_state=42)
dummy.fit(X_train, y_train)
dummy_acc = dummy.score(X_test, y_test)
print(f"DummyClassifier accuracy: {dummy_acc:.3f}  ← looks good!")
y_pred_dummy = dummy.predict(X_test)
print("\nClassification report:")
print(classification_report(y_test, y_pred_dummy,
                             target_names=['benign', 'attack'],
                             zero_division=0))
# Comment: recall for 'attack' = 0.00 — the model detected ZERO attacks!
```

Run your file. You should see:
```
DummyClassifier accuracy: 0.950
precision  recall  f1-score  support
benign          0.95      1.00      0.97     1900
attack          0.00      0.00      0.00      100
accuracy                            0.95     2000
```

---

## Step 6: Compare with LogisticRegression

Scale features, train LogisticRegression. Build a comparison table showing accuracy AND attack recall for both models.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — DummyClassifier vs LogisticRegression")
print("=" * 60)
scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc  = scaler.transform(X_test)
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_tr_sc, y_train)
lr_acc    = lr.score(X_te_sc, y_test)
lr_recall = recall_score(y_test, lr.predict(X_te_sc))
print(f"{'Model':25s} {'Accuracy':>10} {'Attack Recall':>14}")
print("-" * 52)
print(f"{'DummyClassifier':25s} {dummy_acc:>10.3f} {0.0:>14.3f}")
print(f"{'LogisticRegression':25s} {lr_acc:>10.3f} {lr_recall:>14.3f}")
caught_dummy = 0
caught_lr    = int(lr_recall * 100)
print(f"\nOf 100 test attacks: Dummy caught {caught_dummy}, LR caught ~{caught_lr}")
```

Run your file. You should see:
```
Model                   Accuracy  Attack Recall
---------------------------------------------------
DummyClassifier            0.950         0.000
LogisticRegression         ~0.962        ~0.720
Of 100 test attacks: Dummy caught 0, LR caught ~72
```

---

## Step 7: TASK 4 (BONUS) — Daily Cost of the Accuracy Trap

Assume 10,000 network events per day, 5% attack rate = 500 attacks/day. For each model, compute: how many attacks are missed per day? Print a clear summary.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Daily missed attacks")
print("=" * 60)
daily_events  = 10_000
attack_rate   = 0.05
daily_attacks = int(daily_events * attack_rate)
print(f"Daily attacks (5% of {daily_events:,}): {daily_attacks}")
for name, recall in [("DummyClassifier", 0.0), ("LogisticRegression", lr_recall)]:
    missed = int(daily_attacks * (1 - recall))
    print(f"  {name:25s}: {missed:3d} / {daily_attacks} missed ({(1-recall)*100:.0f}%)")
```

Run your file. You should see:
```
Daily attacks (5% of 10,000): 500
DummyClassifier          : 500 / 500 missed (100%)
LogisticRegression       : ~140 / 500 missed (~28%)
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file `01_solution_the_accuracy_trap.py` if anything looks different.
