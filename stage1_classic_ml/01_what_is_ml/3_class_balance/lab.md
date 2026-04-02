# Lab — Exercise 3: Class Balance — The Silent Model Killer

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_class_balance.py` in this folder.

---

## Step 2: Add the imports and setup

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
```

---

## Step 3: Count samples per class

`value_counts().sort_index()` counts each class and sorts by label number. Add this to your file:

```python
counts = df["target"].value_counts().sort_index()
print("Samples per class:")
print(counts)
```

Run your file. You should see:
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
Name: target, dtype: int64
```

---

## Step 4: Calculate the imbalance ratio

Add this to your file:

```python
majority = counts.max()
minority = counts.min()
ratio = majority / minority

print(f"\nMajority class: {majority} samples")
print(f"Minority class: {minority} samples")
print(f"Imbalance ratio: {ratio:.2f} : 1")
print("This dataset is well balanced.")
```

Run your file. You should see:
```
Majority class: 183 samples
Minority class: 174 samples
Imbalance ratio: 1.05 : 1
This dataset is well balanced.
```

---

## Step 5: Simulate the imbalanced security scenario

This makes the accuracy trap concrete. Add this to your file:

```python
normal_count = 950
attack_count = 50
total = normal_count + attack_count

naive_accuracy = normal_count / total
attack_recall = 0.0

print("\n--- Simulated Security Dataset ---")
print(f"Normal connections : {normal_count:4d}  ({normal_count/total*100:.1f}%)")
print(f"Attack connections : {attack_count:4d}   ({attack_count/total*100:.1f}%)")
print()
print("A naive model (always predicts 'normal'):")
print(f"  Accuracy       : {naive_accuracy*100:.1f}%   <- looks great!")
print(f"  Attacks caught :  {attack_recall*100:.1f}%   <- completely useless")
print()
print("This is why accuracy alone is a dangerous metric in security.")
```

Run your file. You should see:
```
--- Simulated Security Dataset ---
Normal connections :  950  (95.0%)
Attack connections :   50   (5.0%)

A naive model (always predicts 'normal'):
  Accuracy       : 95.0%   <- looks great!
  Attacks caught :  0.0%   <- completely useless

This is why accuracy alone is a dangerous metric in security.
```

---

## Step 6: ASCII bar chart of class distribution

A quick visual sanity check. Add this to your file:

```python
print("\nClass distribution:")
for label, count in counts.items():
    bar = "#" * count
    print(f"{label} | {bar} ({count})")
```

Run your file. You should see a horizontal bar for each digit class, all approximately the same length — confirming the dataset is balanced.

---

## Step 7: Add the completion message

```python
print("\n--- Exercise 3 complete. Move to 04_visualise.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
