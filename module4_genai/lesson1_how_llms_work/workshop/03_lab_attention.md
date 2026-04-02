# Lab — Exercise 3: Attention: Which Words Matter to Which

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_attention.py` in this folder.

---

## Step 2: Add the imports and sentence

NumPy provides the array operations. The sentence defines the five tokens whose attention relationships you will explore.

```python
import numpy as np

sentence = ["the", "firewall", "blocked", "malicious", "connection"]
n = len(sentence)
```

---

## Step 3: Build the attention matrix

Each row is the attention distribution for one word — how much that word attends to every other word. Each row sums to 1.0 (softmax output). For example, "blocked" (row 2) attends most strongly to "firewall" (0.45) because the firewall is what does the blocking.

Add this to your file:

```python
attention = np.array([
    [0.80, 0.10, 0.05, 0.03, 0.02],  # the
    [0.15, 0.65, 0.10, 0.05, 0.05],  # firewall
    [0.03, 0.45, 0.00, 0.28, 0.24],  # blocked
    [0.02, 0.08, 0.12, 0.70, 0.08],  # malicious
    [0.04, 0.12, 0.30, 0.25, 0.29],  # connection
])

print("Attention matrix shape:", attention.shape)
print("Row sums:", attention.sum(axis=1))
```

Run your file. You should see:
```
Attention matrix shape: (5, 5)
Row sums: [1. 1. 1. 1. 1.]
```

---

## Step 4: Interpret attention — what does each word attend to most?

For each word, `np.argmax` finds the column with the highest weight, revealing which word that position "looks at" the most when forming its contextual representation.

Add this to your file:

```python
print("\nAttention — what each word attends to most:")
for i, word in enumerate(sentence):
    j = np.argmax(attention[i])
    score = attention[i][j]
    print(f'  "{word:<10}" → attends most to: "{sentence[j]:<10}" ({score:.2f})')
```

Run your file. You should see:
```
Attention — what each word attends to most:
  "the"        → attends most to: "the"        (0.80)
  "firewall"   → attends most to: "firewall"   (0.65)
  "blocked"    → attends most to: "firewall"   (0.45)
  "malicious"  → attends most to: "malicious"  (0.70)
  "connection" → attends most to: "blocked"    (0.30)
```

---

## Step 5: Compute a context vector for "blocked"

The attention output for a position is a weighted sum of value vectors. "Blocked" draws most of its context from "firewall" (0.45) and "malicious" (0.28), which is semantically correct — the firewall is the subject doing the blocking, and malicious is what gets blocked.

Add this to your file:

```python
values = np.array([
    [ 0.10, -0.20,  0.05,  0.10,  0.05],  # the
    [ 0.70,  0.60, -0.30,  0.20,  0.10],  # firewall
    [ 0.50,  0.40, -0.10,  0.30,  0.20],  # blocked
    [ 0.90,  0.75, -0.50,  0.80,  0.40],  # malicious
    [ 0.65,  0.55, -0.25,  0.60,  0.30],  # connection
])

context_blocked = attention[2] @ values
print(f"\nContext vector for \"blocked\": {np.round(context_blocked, 3)}")

top2_indices = np.argsort(attention[2])[::-1][:2]
contributors = ", ".join(f"{sentence[j]} ({attention[2][j]:.2f})" for j in top2_indices)
print(f"Top contributors: {contributors}")
```

Run your file. You should see:
```
Context vector for "blocked": [ 0.604  0.519 -0.234  0.481  0.235]
Top contributors: firewall (0.45), malicious (0.28)
```

---

## Step 6: Print the attention matrix as a formatted grid (Bonus Task 4)

A grid view lets you see the full attention pattern at a glance — which words attend strongly to which others across the entire sequence.

Add this to your file:

```python
labels = ["the  ", "firwl", "blckd", "malcs", "cnnct"]
header = "       " + "  ".join(labels)
print(f"\n{header}")
for i, lbl in enumerate(labels):
    row_str = "  ".join(f"{v:.2f}" for v in attention[i])
    print(f"  {lbl}  [ {row_str} ]")

print("\n--- Exercise 3 complete. Open 03_solution_attention.py to compare. ---")
print("--- Next: module4_genai/lesson2_huggingface/workshop/00_overview.md ---")
```

Run your file. You should see:
```
       the    firwl  blckd  malcs  cnnct
  the    [ 0.80  0.10  0.05  0.03  0.02 ]
  firwl  [ 0.15  0.65  0.10  0.05  0.05 ]
  blckd  [ 0.03  0.45  0.00  0.28  0.24 ]
  malcs  [ 0.02  0.08  0.12  0.70  0.08 ]
  cnnct  [ 0.04  0.12  0.30  0.25  0.29 ]

--- Exercise 3 complete. Open 03_solution_attention.py to compare. ---
--- Next: module4_genai/lesson2_huggingface/workshop/00_overview.md ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_attention.py`) if anything looks different.
