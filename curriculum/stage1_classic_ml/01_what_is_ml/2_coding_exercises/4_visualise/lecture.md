# Visualising Your Data

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

Before reaching for code, picture what you are building: **a grid of small images**, each one a numeric array painted as pixels, optionally with titles. The functions below each handle one piece of that picture. We introduce each one in plain English first, then show the call.

---

### 1. Reserve an empty grid → `plt.subplots()`

You start with a blank canvas. The first decision is **how many panels you need and how they should be laid out**. `plt.subplots(rows, cols)` reserves an empty `rows × cols` grid and hands you back an array of panel handles, addressed by `axes[row][col]`. Calling it with `2, 3` produces these six empty panels — you can then drop an image into any of them by index:

<div class="lecture-visual">
  <img src="/static/lecture_assets/subplots_grid.png" alt="2x3 grid of empty matplotlib panels labelled axes[0][0] through axes[1][2]">
  <div class="vis-caption">Real output of <code>plt.subplots(2, 3)</code>. Write to any panel with <code>axes[0][2].imshow(...)</code>.</div>
</div>

```python
fig, axes = plt.subplots(rows, cols, figsize=(width, height))
```

- `fig` — the whole figure (used for the overall title and `savefig`)
- `axes` — the NumPy array of panels you just saw
- `figsize` — width × height **in inches**

**One panel vs many panels — `ax` vs `axes`**

`axes` (plural) is the *whole grid* of panels. A single panel inside it is conventionally called `ax` (singular). You pick a panel out of the grid by indexing into it, exactly like a list. Here is the simplest possible full example — three digits side by side:

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()

# Reserve a 1-row, 3-column grid.
# fig  = the whole figure (the outer canvas, one per call)
# axes = the list of 3 panels inside it
fig, axes = plt.subplots(1, 3, figsize=(6, 2))

# Pick each panel by index and draw a digit into it
axes[0].imshow(digits.images[0], cmap="gray_r")
axes[1].imshow(digits.images[1], cmap="gray_r")
axes[2].imshow(digits.images[2], cmap="gray_r")

# fig is the handle to the WHOLE figure, so anything that applies to
# every panel at once goes through fig:
fig.suptitle("First three digits")     # one heading above all panels
fig.savefig("first_three_digits.png")  # save the whole figure to disk

plt.show()
```

<div class="lecture-visual">
  <img src="/static/lecture_assets/ax_vs_axes_example.png" alt="Three matplotlib panels in a single row showing the first three sklearn digit images (0, 1, 2) rendered as greyscale 8x8 grids, with the figure-level title 'First three digits' above them">
  <div class="vis-caption">Real output of the script above. Three panels in one row, one digit each, with a single <code>fig.suptitle</code> heading above all of them.</div>
</div>

That is the whole pattern. `axes[0]` is the leftmost panel, `axes[1]` is the middle one, `axes[2]` is the rightmost. Whenever you see `ax.something(...)` in the code below, picture **one of those three rectangles** and that call drawing into it.

**`fig` vs `axes` — when do you use which?** Think of `fig` as the outer picture frame and each `ax` as one painting hanging inside it. Anything that affects *one panel* (drawing the image, hiding its ticks, setting its title) is a method on `ax`. Anything that affects the *entire figure at once* (a single overall title, saving the whole thing to a file) is a method on `fig`. We will see `fig.suptitle()` again in section 4 below.

If you have *many* panels and don't want to write `axes[0]`, `axes[1]`, … by hand, a regular `for` loop with an index works:

```python
for i in range(10):
    axes[i].imshow(digits.images[i], cmap="gray_r")
```

---

### 2. Numbers become pixels → `ax.imshow()`

The name `imshow` is short for **image show**: take a 2D array of numbers, paint each number as a coloured square, and display the result inside a panel. It is a *method on a panel* — you call it as `ax.imshow(...)`, and the picture appears inside that specific `ax`.

**What the call needs:**

```python
ax.imshow(array_2d, cmap="gray_r")
```

| Argument | What it is | Example |
|---|---|---|
| `array_2d` | the 2D NumPy array of pixel values you want to draw | shape `(8, 8)` for a digit |
| `cmap` | the **colour map** — the rule that turns each number into a colour | `"gray_r"`, `"hot"`, `"viridis"`, … |

`imshow` walks the array row by row, looks up each value in the colour map, and paints that colour into the corresponding square. With `cmap="gray_r"` (reversed greyscale), **high values become dark ink and low values stay as white background** — matching how you would draw on paper. The same digit-3 sample, shown as raw numbers on the left and as pixels on the right:

<div class="lecture-visual">
  <img src="/static/lecture_assets/imshow_demo.png" alt="An 8x8 array of numbers from 0 to 16 next to the same array rendered as a greyscale handwritten 3">
  <div class="vis-caption">Real digit-3 sample from sklearn. The numbers on the left literally are the pixels on the right — <code>imshow</code> just does the lookup.</div>
</div>

The `cmap` is the only knob that decides what colours come out. The same digit, painted with four different colour maps, looks like this:

<div class="lecture-visual">
  <img src="/static/lecture_assets/cmap_compare.png" alt="The same digit-3 image rendered with four colourmaps: gray_r, gray, hot, and viridis">
  <div class="vis-caption">Four cmaps applied to the same array. Pick the one that matches your data type.</div>
</div>

| cmap | Low &rarr; high | Best for |
|---|---|---|
| `"gray_r"` | white &rarr; black | digits, scanned text |
| `"gray"` | black &rarr; white | astronomy, MRI scans |
| `"hot"` | black &rarr; red &rarr; yellow | heatmaps, feature importance |
| `"viridis"` | dark blue &rarr; green &rarr; yellow | scientific data (perceptually uniform) |

---

### 3. Hide the rulers → `ax.axis("off")`

By default every panel ships with x/y tick marks and numeric labels along its edges. For pixel images those numbers are noise — they refer to row and column indices nobody needs to read. Switch them off so the eye lands directly on the digit.

<div class="lecture-visual">
  <img src="/static/lecture_assets/axis_on_off.png" alt="The same digit with default x/y tick marks on the left and a clean borderless version on the right">
  <div class="vis-caption">Same image, same data. <code>ax.axis("off")</code> removes the borders, ticks, and numeric labels.</div>
</div>

```python
ax.axis("off")
```

---

### 4. One title above the whole figure → `fig.suptitle()`

Each panel can carry its own `set_title("3")` for the digit it shows, but you usually want one heading **above the entire figure** as well. That is the figure-level "super title". Notice the per-panel labels (`3`, `5`, `8`) and the suptitle sitting above all of them:

<div class="lecture-visual">
  <img src="/static/lecture_assets/suptitle_demo.png" alt="Three digit panels with individual titles 3, 5, 8 and a single figure-level suptitle above them">
  <div class="vis-caption">Per-panel titles via <code>ax.set_title()</code>, plus one figure-level heading via <code>fig.suptitle()</code>.</div>
</div>

```python
fig.suptitle("Average digit per class", fontsize=12)
```

---

### 5. Stop the overlap → `plt.tight_layout()`

Without this call, the per-panel titles from the previous step often collide with the next row of panels. `tight_layout()` measures every label and nudges things until they fit. Compare these two figures — same code, same data, only difference is the call to `tight_layout()`:

<div class="lecture-visual lecture-visual-pair">
  <img src="/static/lecture_assets/tight_layout_off.png" alt="A 2x3 figure where the panel titles overlap the row beneath them">
  <img src="/static/lecture_assets/tight_layout_on.png" alt="The same 2x3 figure with tight_layout applied — titles no longer overlap">
  <div class="vis-caption">Left: default spacing — titles crash into the row beneath. Right: <code>plt.tight_layout()</code> nudges everything until it fits.</div>
</div>

```python
plt.tight_layout()
```

Always call it just before `savefig` or `show`.

---

### 6. Save and display → `plt.savefig()` and `plt.show()`

```python
plt.savefig("path/filename.png")  # write to disk first…
plt.show()                         # …then open the window (may block)
```

Save **before** show — on some systems `show()` clears the figure when the window closes, leaving you with an empty PNG.

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
