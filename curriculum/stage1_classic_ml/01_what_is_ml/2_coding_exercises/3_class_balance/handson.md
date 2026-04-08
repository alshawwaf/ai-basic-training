# Lab — Class Balance & the Accuracy Trap

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_class_balance.py` in this folder.

---

## Step 2: Add the imports and setup

Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: fast numeric arrays
import pandas as pd                         # pandas: tabular data with labels
from sklearn.datasets import load_digits    # built-in 8x8 handwritten digits dataset

digits = load_digits()                       # Bunch with .data, .target, .images, ...
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])  # 1797 x 64 table
df["target"] = digits.target                 # add the label column (digit 0..9)
```

---

## Step 3: Count samples per class

`value_counts().sort_index()` counts each class and sorts by label number. Add this to your file:

```python
# value_counts() = "how many of each value"; sort_index() puts the labels in 0..9 order
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
majority = counts.max()                       # the largest class size
minority = counts.min()                       # the smallest class size
ratio = majority / minority                   # >1 means imbalanced; closer to 1 = balanced

print(f"\nMajority class: {majority} samples")
print(f"Minority class: {minority} samples")
print(f"Imbalance ratio: {ratio:.2f} : 1")    # the key number — anything >2:1 starts to bias models
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
# Real-world security data is almost always heavily imbalanced — 95% normal, 5% attack is generous
normal_count = 950
attack_count = 50
total = normal_count + attack_count

naive_accuracy = normal_count / total         # if you predict "normal" for every row, you get this
attack_recall = 0.0                           # ...but you catch zero attacks. The "accuracy trap".

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
for label, count in counts.items():           # iterate through (label, count) pairs
    bar = "#" * count                          # one '#' per sample → length encodes the count
    print(f"{label} | {bar} ({count})")
```

Run your file. You should see a horizontal bar for each digit class, all approximately the same length — confirming the dataset is balanced.

---

## Step 7: Add the completion message

```python
print("\n--- Class Balance & the Accuracy Trap — complete ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_class_balance.py`) if anything looks different.
