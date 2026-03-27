# Lesson 1.1 — What is ML? Exploring Data

**Script:** [1_concepts_and_data.py](1_concepts_and_data.py)

---

## Concept: Before You Train Anything, Look at Your Data

One of the most common mistakes beginners make is jumping straight into training a model without understanding what the data looks like. Every experienced ML practitioner spends significant time on **exploratory data analysis (EDA)** first.

In cybersecurity terms: you wouldn't write detection rules without first looking at what the malicious traffic actually looks like. Same principle.

---

## The Dataset We Use

We use scikit-learn's built-in **digits dataset** — 1,797 handwritten digit images (0–9), each stored as an 8×8 grid of pixel brightness values.

```
  0  0  5 13  9  1  0  0
  0  0 13 15 10 15  5  0
  0  3 15  2  0 11  8  0
  0  4 12  0  0  8  8  0
  0  5  8  0  0  9  8  0
  0  4 11  0  1 12  7  0
  0  2 14  5 10 12  0  0
  0  0  6 13 10  0  0  0
  ↑ This is the digit '0'
```

Each image is **flattened into a row of 64 numbers** before the model sees it. The model never sees the picture — only the numbers. This is exactly how security ML works: a network connection becomes a row of numbers (bytes sent, packets per second, port, protocol...) and the model learns to classify it from those numbers alone.

---

## What the Script Does

### Step 1 — Load and inspect the data
```python
digits = load_digits()
# digits.data   → shape (1797, 64) — 1797 images, 64 pixel features each
# digits.target → shape (1797,)    — correct label for each image (0–9)
# digits.images → shape (1797, 8, 8) — same data as 2D grids for plotting
```

Always check the shape first. It tells you how much data you have and how many features each sample carries.

### Step 2 — Check class balance
```python
df["target"].value_counts().sort_index()
# 0    178
# 1    182
# 2    177
# ...
```

This dataset is well-balanced — roughly equal examples of each digit. In security data this is rarely true: you might have millions of normal connections and only hundreds of attacks. That imbalance matters enormously — you'll deal with it properly in Module 2.

### Step 3 — Visualise sample images

The script plots two examples of each digit side by side. This is your sanity check — do the images look like what you'd expect? Are there any obvious data quality problems?

In security EDA, you do the equivalent: plot a few raw log lines from each class and ask "does this actually look like an attack?"

### Step 4 — Print one image as raw numbers

```python
for row in digits.images[0].astype(int):
    print("  ".join(f"{v:2d}" for v in row))
```

This makes the point concrete: **the model sees numbers, not pictures**. Pixel brightness values, floats, integers — it's all just a row of features. The label tells the model what those numbers mean.

### Step 5 — Plot the average image per class

Averaging all the `0`s together, all the `1`s together, etc., gives you the "prototype" of each class. If two classes have very similar averages (e.g. `1` and `7` might overlap in some pixels) the model will find those harder to separate.

---

## What to Look for When You Run It

1. **Shape** — 1797 rows, 64 features
2. **Class balance** — roughly 178–182 examples per digit (well balanced)
3. **Sample images** — recognisable digits, some messier than others
4. **Average images** — each digit has a distinct shape; `1` and `7` are the most similar

---

## The Key Takeaway

> The model only ever sees rows of numbers. Your job is to make sure those numbers carry enough signal to find the pattern.

Before any training, ask:
- How many samples do I have?
- Are the classes balanced?
- Do the features look meaningful?
- Are there missing values? (`df.isnull().sum()`)

---

## Try It Yourself

```python
# Which pixel positions are most different between digit 0 and digit 1?
mean_0 = digits.data[digits.target == 0].mean(axis=0)
mean_1 = digits.data[digits.target == 1].mean(axis=0)
diff = abs(mean_0 - mean_1).reshape(8, 8)

import matplotlib.pyplot as plt
plt.imshow(diff, cmap="hot")
plt.title("Pixel differences between 0 and 1")
plt.colorbar()
plt.show()
# Bright areas = pixels that differ a lot → most useful features for separating these two classes
```

---

## Next Lesson

**[Lesson 1.2 — Linear Regression](2_linear_regression.md):** Predict a continuous number (server response time from traffic volume) using your first ML model.
