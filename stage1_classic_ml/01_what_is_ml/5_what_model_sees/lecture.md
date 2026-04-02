# Exercise 5 — What the Model Actually Sees

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How to print a 2D array as a formatted number grid
- Why the model receives numbers — never images, never log lines, never text
- How to measure which features carry the most predictive information
- How this structure maps directly onto real security data

---

## Concept: The Model's View of the World

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

This is the most important conceptual shift in all of machine learning.

A human sees this:

```
    ████
   █  █
   █  █
   ████
```

A model sees this:

```
0  0  5 13  9  1  0  0
0  0 13 15 10 15  5  0
0  3 15  2  0 11  8  0
0  4 12  0  0  8  8  0
0  5  8  0  0  9  8  0
0  4 11  0  1 12  7  0
0  2 14  5 10 12  0  0
0  0  6 13 10  0  0  0
```

And it is actually fed this — a flat, single row:

```
[0, 0, 5, 13, 9, 1, 0, 0, 0, 0, 13, 15, 10, 15, 5, 0, 0, 3, 15, 2, ...]
```

```
  How the 8x8 image becomes a flat input row:

  8x8 grid                     flatten                 model input
  ┌─────────────────┐          ───────►     ┌─────────────────────────────────┐
  │ 0  0  5 13  9  1│                       │ 0  0  5 13  9  1  0  0  0  0  │
  │ 0  0 13 15 10 15│   row 0 ++ row 1      │13 15 10 15  5  0  0  3 15  2  │
  │ 0  3 15  2  0 11│   ++ row 2 ++ ...     │ 0 11  8  0 ... (64 values)    │
  │ ...             │                       └─────────────────────────────────┘
  └─────────────────┘                         one row = one sample
    shape: (8, 8)                             shape: (64,)
```

64 numbers. That is the complete input. No concept of "up", "down", "left", "right." No idea that these are pixels. No visual intuition of any kind.

The model learns to map these 64 numbers to the correct digit label purely through exposure to thousands of labelled examples. This is both the power and the limitation of classical ML.

---

## Concept: The Security Equivalent

In a network intrusion detection dataset, one connection looks like this to the model:

```python
[1048576,  443,   2.4,   14,   0,   3,   1,   0.87,  2048, ...]
# bytes    port  secs  pkts  rst  syn  fin  entropy  pkt_size
```

A flat row of numbers. One per feature. The model never "sees" a packet — it sees numbers.

The table below maps the digits domain to the security domain:

| Concept | Digits | Network intrusion |
|---------|--------|-------------------|
| Features | 64 pixel values | bytes, ports, flags, duration, entropy... |
| Feature type | Pixel brightness 0–16 | Mixed: counts, rates, booleans, ratios |
| Label | Digit 0–9 | benign / malicious |
| Samples | 1,797 images | Millions of connections per day |
| Feature scale | All 0–16 | Wildly different scales — bytes vs ratios |
| Class balance | ~178 per class | Often 99:1 or worse |

The algorithm — logistic regression, decision tree, random forest — operates identically regardless of domain. You load the numbers, split them, fit the model, evaluate. The domain expertise comes in when you decide which numbers to include and how to engineer them.

```
  The universal ML pipeline — same for any domain

  ┌──────────────┐     ┌───────────┐     ┌──────────┐     ┌────────────┐
  │  Raw data    │────►│ Numeric   │────►│  Model   │────►│ Prediction │
  │ (images,     │     │ features  │     │ .fit()   │     │ .predict() │
  │  logs, URLs) │     │ (flat row │     │          │     │            │
  │              │     │  of nums) │     │          │     │ digit: 0   │
  └──────────────┘     └───────────┘     └──────────┘     └────────────┘
       domain              math              math             domain
      knowledge          agnostic          agnostic         knowledge
```

---

## Concept: Feature Correlation with the Target

A feature that is highly correlated with the label is likely to be useful.

```python
df.corr()["target"]
```

This computes the Pearson correlation between every column and the `target` column. Values range from -1 (perfect inverse relationship) to +1 (perfect positive relationship). We take the absolute value because either direction is useful.

```
pixel_43    0.55   <- this pixel is highly predictive
pixel_34    0.53
pixel_26    0.52
...
pixel_0     0.00   <- this pixel predicts nothing (always 0)
pixel_63    0.00
```

**Caveat:** Correlation only measures linear relationships. A feature can be highly useful for the model while having low linear correlation (if the relationship is non-linear). This is a useful fast filter, not a definitive answer. Feature importance from the trained model (Lesson 1.4) is a more reliable measure.

---

## Concept: Identifying Pixel Position from Index

In an 8×8 grid, pixel index `i` corresponds to:

```
row = i // 8      (integer division)
col = i % 8       (remainder)
```

So `pixel_43`:
```
row = 43 // 8 = 5
col = 43 % 8  = 3
```

That is row 5, column 3 — slightly right of centre, near the bottom. This makes intuitive sense: centre pixels vary more between digits (they carry ink from the actual strokes) while corner pixels are almost always blank background.

---

## Concept: f-String Number Formatting

To print a number in exactly 2 characters (so columns align):

```python
f"{v:2d}"    # integer, minimum 2 characters wide
```

Examples:
```
f"{0:2d}"   ->  " 0"    (padded with a space)
f"{9:2d}"   ->  " 9"
f"{13:2d}"  ->  "13"    (no padding needed)
f"{5:2d}"   ->  " 5"
```

Printing the whole row:
```python
"  ".join(f"{v:2d}" for v in row)
```
`"  ".join(...)` puts two spaces between each number. The result is a clean aligned grid.

---

## What Each Task Asks You to Do

### Task 1 — Print one image as a number grid
Take `digits.images[0]` — the first image as an 8×8 array.

Call `.astype(int)` on it first (converts float32 → int for cleaner printing).

Loop over each of the 8 rows. For each row, use `"  ".join(f"{v:2d}" for v in row)` to produce one formatted line.

### Task 2 — Compare digit 1 and digit 7 as number grids
Print one example of each, side by side. After printing, ask yourself:
- Which rows look the same?
- Which rows look different?
- Could you write an if/else rule to separate them?

The exercise of trying to write rules manually builds intuition for what the model has to figure out automatically.

### Task 3 — Feature correlations
```python
correlations = df.corr()["target"].abs().sort_values(ascending=False)
```

The first entry will always be `target` itself (correlation = 1.0). Slice it off with `.iloc[1:11]` or use `.drop("target")` before sorting.

### Task 4 — Visualise correlations as a heatmap (Bonus)
The correlation values per pixel can be reshaped from a 64-element array back into an 8×8 grid and plotted. This shows spatially which pixels drive predictions.

```python
corr_values = df.drop(columns=["target"]).corrwith(df["target"]).abs().values
corr_grid   = corr_values.reshape(8, 8)
plt.imshow(corr_grid, cmap="hot")
```

---

## Connecting It All

After completing all 5 exercises, you have done the full EDA cycle:

1. **Loaded** the data and understood its structure
2. **Checked statistics** — shape, ranges, missing values, useless features
3. **Checked class balance** — confirmed it is safe to use accuracy here
4. **Visualised** — confirmed data looks as expected, predicted hard class pairs
5. **Understood the model's input** — a flat row of numbers, no magic

This is not a one-time exercise. This is how every ML project begins — every single time. The specific dataset and domain change; the questions you ask do not.

---

## Now Open the Lab

[handson.md](handson.md)
## Workshop Complete

When all 5 exercises run cleanly, compare your code against the matching solution file for each exercise.

**Next lesson:** [Lesson 1.2 — Linear Regression](../../02_linear_regression/README.md) — build your first trained model.
