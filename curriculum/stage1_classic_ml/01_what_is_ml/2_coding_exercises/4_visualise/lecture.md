# Exercise 4 — Visualising Your Data

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How matplotlib creates figure grids with `subplots()`
- How to render a NumPy array as a greyscale image with `imshow()`
- Why visual inspection before training is not optional
- How to compute average images per class — and what they predict about model difficulty

---

## Concept: Always Look at Your Data

> "If you haven't looked at your data, you don't understand your data."
> — A lesson most ML practitioners learn the hard way.

You cannot catch data problems by looking at statistics alone. You need to see examples. Problems that visual inspection catches:

- **Mislabelled samples** — a digit 7 labelled as 1; a benign file labelled malicious
- **Corrupted data** — broken log entries that look like all-zero rows
- **Wrong class** — an attacker that uploaded adversarial examples to pollute your training set
- **Unexpected patterns** — all samples of class 8 happen to come from one sensor, giving the model an artifact to exploit instead of learning the real signal

In security you have an additional concern: if your training data contains data from a specific network or time period, visually checking it confirms you are not accidentally building a model that works only for that context.

---

## Concept: matplotlib — The Core Functions

```
plt.subplots(rows, cols, figsize=(width, height))
```
Creates a grid of empty panels. Returns two things:
- `fig` — the whole figure (used for overall title and saving)
- `axes` — a NumPy array of panels, shape `(rows, cols)`

Access individual panels: `axes[0][3]` is row 0, column 3.

```
ax.imshow(array_2d, cmap="gray_r")
```
Renders a 2D NumPy array as an image. `cmap="gray_r"` means reversed greyscale: high values (ink = 16) appear dark, low values (background = 0) appear white — matching how you would draw on paper.

Other useful colourmaps:
- `"gray"` — standard greyscale (high = white)
- `"hot"` — black → red → yellow → white, useful for heatmaps
- `"viridis"` — blue → green → yellow, perceptually uniform

```
ax.axis("off")
```
Hides the tick marks and axis labels — cleaner for image grids.

```
fig.suptitle("text", fontsize=12)
```
Adds a centred title above the entire figure.

```
plt.tight_layout()
```
Automatically adjusts spacing so panels don't overlap each other or the title.

```
plt.savefig("path/filename.png")
```
Saves the figure to disk. Call this before `plt.show()`.

```
plt.show()
```
Opens the display window. On some systems this blocks execution until you close it.

---

## Concept: Filtering with Boolean Masks

> **Want to go deeper?** [pandas — Wikipedia](https://en.wikipedia.org/wiki/Pandas_(software))

```python
samples = digits.images[digits.target == 3]
```

`digits.target == 3` creates a Boolean array — `True` wherever the label is 3, `False` elsewhere. Using it as an index into `digits.images` returns only the images labelled 3.

This is the pandas/NumPy pattern for "give me all samples of class X":

```python
# NumPy version
class_images = digits.images[digits.target == digit]

# pandas equivalent
class_rows = df[df["target"] == digit]
```

You will use this in every lesson.

---

## Concept: Average Images — Predicting Model Difficulty

If you average all images of digit 3 together, pixel by pixel, you get a "prototype" — the typical shape of a 3.

```python
mean_image = digits.images[digits.target == 3].mean(axis=0)
# axis=0 means: average across the first axis (samples)
# result shape: (8, 8) — one value per pixel position
```

**Why this is useful:**

Two prototypes that look nearly identical mean the model will struggle to separate those classes. The model has to find subtle pixel-level differences to distinguish them.

```
Prototype for 1:     Prototype for 7:
  . . . X .            . . X X X .
  . . X X .            . . . . X .
  . . . X .            . . . X . .
  . . . X .            . . X . . .

Nearly identical in the top half.
The model has to learn that 1 is narrow, 7 is wider at top.
```

Pairs with the most similar prototypes will produce the highest confusion rates in the final model. You can predict this before training anything — and verify it in Lesson 1.5.

**Average images → predict model confusion**

For each digit, take the mean of every sample of that class. The result is a *prototype* — what that digit looks like "on average". Then compare prototypes pairwise:

| All samples of… | Average together → | Prototype | Compared to | Pixel difference | What it tells you |
|---|---|---|---|---|---|
| digit **3** | `mean(axis=0)` per class | `proto(3)` | `proto(8)` | **LOW** | model will confuse 3 and 8 |
| digit **8** | `mean(axis=0)` per class | `proto(8)` | `proto(0)` | **HIGH** | model will separate them easily |

The lower the difference between two prototypes, the more often the model will mix those two classes up.

---

## What Each Task Asks You to Do

### Task 1 — One sample per class (1×10 grid)
Create a 1-row, 10-column figure. For each digit 0–9, show one example image with the digit number as the panel title.

Use: `digits.images[digits.target == digit][0]` — the `[0]` at the end takes the first example.

### Task 2 — Two samples per class (2×10 grid)
Create a 2-row, 10-column figure. Show two different examples of each digit.

The key: `zip(axes, samples[:2])` pairs the two rows of the `axes` grid with the first two sample images. `axes` has shape `(2, 10)` — iterating over it gives you `axes[0]` (first row) then `axes[1]` (second row).

This shows how much variation exists within a single class — the model must generalise across all that variation.

### Task 3 — Average image per class (1×10 grid)
For each digit, compute the mean across all its images using `.mean(axis=0)`. Plot the results.

After this, identify visually which digit pairs look most alike.

### Task 4 — Find the most similar class pair (Bonus)
Compute the mean absolute difference between every pair of average images. The pair with the lowest difference is the one the model will confuse most. Print the top 3.

---

## Common Mistakes

**`IndexError: index 2 is out of bounds for axis 0 with size 2`**
`axes` is a 2D array — you need `axes[row][col]` not `axes[col]`. When iterating with `zip(axes, samples[:2])`, the variable from `axes` is already the full row — use `row[digit]` to get the individual panel.

**Plot window appears but is blank**
`plt.tight_layout()` must come before `plt.show()`. Also make sure you called `ax.imshow()` before `plt.show()`.

**`savefig` gives a `FileNotFoundError`**
The directory in the save path must already exist. Run from the repo root so the path resolves correctly.
