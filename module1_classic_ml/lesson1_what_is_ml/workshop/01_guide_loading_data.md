# Exercise 1 — Loading a Dataset

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How scikit-learn packages and delivers datasets
- What a `Bunch` object is and how to navigate it
- How to wrap raw data in a pandas `DataFrame`
- The difference between **features** and **labels** — the most fundamental concept in all of supervised ML

---

## Concept: The Anatomy of a Dataset

Every supervised ML problem has exactly two things:

- **Features (X)** — what you measure about each sample (the inputs)
- **Labels (y)** — the correct answer for each sample (the output the model learns to predict)

The structure is always the same. Only the domain changes:

| Problem | Features (X) — *what you measure* | Label (y) — *what you predict* |
|:---|:---|:---|
| **Digit recognition** | 64 pixel brightness values | `digit 0-9` |
| **Phishing detection** | URL length, # of dots, has `@` | `phishing 0/1` |
| **Network intrusion** | bytes sent, duration, SYN flags | `malicious 0/1` |
| **Malware classification** | file size, entropy, imports | `family name` |

No matter the domain, the code follows the same pattern:

```
      ┌──────────────────────────────┐
      │          Raw Data            │
      │   (logs, images, URLs,       │
      │    packets, sensor data)     │
      └──────────────┬───────────────┘
                     ▼
      ┌──────────────────────────────┐
      │   Extract Features (X)       │   ← turn raw data into numbers
      │   and Labels (y)             │   ← identify what you're predicting
      └──────────────┬───────────────┘
                     ▼
      ┌──────────────────────────────┐
      │       model.fit(X, y)        │   ← the model finds the pattern
      └──────────────┬───────────────┘
                     ▼
      ┌──────────────────────────────┐
      │      model.predict(X_new)    │   ← apply the pattern to new data
      └──────────────────────────────┘
```

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

---

## Concept: The Digits Dataset

We use the UCI Optical Recognition of Handwritten Digits dataset — a classic benchmark that ships inside scikit-learn. No download required.

Each sample is an 8×8 greyscale image of a handwritten digit. Each cell is a pixel brightness from 0 (white) to 16 (full ink):

```
 Raw pixel values              Ink level — same data, visualised

  0  0  5 13  9  1  0  0      ·  ·  ▒  █  ▓  ░  ·  ·
  0  0 13 15 10 15  5  0      ·  ·  █  █  ▓  █  ▒  ·
  0  3 15  2  0 11  8  0      ·  ░  █  ░  ·  ▓  ▒  ·
  0  4 12  0  0  8  8  0      ·  ░  ▓  ·  ·  ▒  ▒  ·   ← the digit "0"
  0  5  8  0  0  9  8  0      ·  ▒  ▒  ·  ·  ▓  ▒  ·
  0  4 11  0  1 12  7  0      ·  ░  ▓  ·  ░  ▓  ▒  ·
  0  2 14  5 10 12  0  0      ·  ░  █  ▒  ▓  ▓  ·  ·
  0  0  6 13 10  0  0  0      ·  ·  ▒  █  ▓  ·  ·  ·

  Key:  · = 0 (empty)   ░ = 1–4   ▒ = 5–8   ▓ = 9–12   █ = 13–16 (full ink)
```

The hollow centre of the 0 is visible in the right column — rows 3–6 have `·` in the middle. The image is then flattened to a single row of 64 numbers before the model receives it.

The full dataset: **1,797 images**, **10 classes** (digits 0–9), **64 features** per image.

> **Want to go deeper?** [UCI Optical Recognition of Handwritten Digits — Wikipedia](https://en.wikipedia.org/wiki/MNIST_database)

---

## Concept: The `load_digits()` Return Value — a Bunch Object

scikit-learn ships several real datasets that load with a single function call — no downloading, no CSV files, no file paths. `load_digits()` is one of them. You call it once and it hands back everything: the pixel data, the correct labels, and metadata all bundled together.

**Other built-in datasets you can explore the same way:**

| Function | Dataset | Task |
|----------|---------|------|
| `load_iris()` | Iris flower measurements | Classify species (3 classes) |
| `load_wine()` | Chemical analysis of wines | Classify origin (3 classes) |
| `load_breast_cancer()` | Tumour measurements | Malignant vs benign (2 classes) |
| `load_diabetes()` | Patient measurements | Predict disease progression (regression) |

Each returns a `Bunch` with the same `.data`, `.target`, and `.DESCR` fields — the code you write today works on all of them.

> **Want to go deeper?** [scikit-learn toy datasets — official docs](https://scikit-learn.org/stable/datasets/toy_dataset.html)

That bundle is called a `Bunch` — a container object that works like a Python dictionary with dot-notation access.

Most of the fields inside are **ndarray** objects. An `ndarray` (short for *n-dimensional array*) is NumPy's core data type — a grid of numbers that can have any number of dimensions. A 1D ndarray is a list of numbers, a 2D ndarray is a table (rows and columns), and a 3D ndarray is a stack of tables. All ML data flows through ndarrays because they are fast and memory-efficient.

| Field | Type | What it is |
|:---|:---|:---|
| `digits.data` | ndarray (1797, 64) | Raw pixel values — one row per image, one column per pixel. **Feed this to the model.** |
| `digits.target` | ndarray (1797,) | Correct label (0-9) for each image. **These are the answers.** |
| `digits.images` | ndarray (1797, 8, 8) | Same pixel values arranged as 8x8 grids — **only used for plotting.** |
| `digits.target_names` | ndarray ([0..9]) | The list of all unique class labels |
| `digits.DESCR` | str | Full text description of the dataset |

`digits.data` and `digits.images` contain **identical pixel values** — just different shapes. Use `.data` for feeding the model (it wants flat rows), `.images` for plotting (you need the 8x8 grid).

```
Same pixels, two shapes:

.data[0]    →  [ 0, 0, 5, 13, 9, 1, 0, 0, 0, 0, ... ]    64 values in a flat row
                 ↑  ↑  ↑   ↑                               (what the model sees)

.images[0]  →  ┌  0  0  5 13  9  1  0  0  ┐               8 rows × 8 columns
               │  0  0 13 15 10 15  5  0  │                (what the image looks like)
               │  0  3 15  2  0 11  8  0  │
               │  ...                     │
               └  0  0  6 13 10  0  0  0  ┘
```

> **Want to go deeper?** [NumPy ndarray — Wikipedia](https://en.wikipedia.org/wiki/NumPy)

---

## Concept: Why We Wrap Data in a DataFrame

`digits.data` is a raw NumPy array — just a block of numbers with no column names. Feeding raw arrays into ML pipelines works, but it makes debugging much harder.

Wrapping it in a pandas `DataFrame` gives you:

- **Named columns** — `pixel_0`, `pixel_1`, ... so you can refer to features by name
- **Easy inspection** — `.head()`, `.describe()`, `.value_counts()` all work
- **Filtering** — pull out exactly the rows you need (see example below)
- **Consistent interface** — most scikit-learn functions accept DataFrames directly

**How filtering works:**

```python
df[df["target"] == 3]
```

Read this from the inside out. `df["target"]` grabs the target column. `== 3` compares every value to 3 and produces a column of `True`/`False`. Wrapping that back in `df[...]` keeps only the rows where the result is `True`:

```
df["target"]      == 3       df[df["target"] == 3]

  0                False
  1                False     (skipped)
  2                False     (skipped)
  3        -->     True   -->  row kept
  4                False     (skipped)
  3                True   -->  row kept
  ...                        ...
```

This is how you slice a dataset down to a single class — useful when you want to inspect or plot just the "3" digits, for example.

**How column names appear:**

The raw ndarray has no column names — just numbered positions. When you create a DataFrame, two things happen:

1. `columns=[f"pixel_{i}" for i in range(64)]` — gives each of the 64 data columns a name (`pixel_0`, `pixel_1`, ... `pixel_63`)
2. `df["target"] = digits.target` — creates a new 65th column called `target` and fills it with the labels

```python
# Step 1: wrap the pixel data and name the columns
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])

# Step 2: add the labels as a new column
df["target"] = digits.target
```

```
digits.data (ndarray)                   digits.target (ndarray)
┌───────────────────────────┐           ┌───┐
│  0  0  5 13  9 ...  (x64) │           │ 0 │
│  0  0  0 12  6 ...  (x64) │           │ 1 │
│  ...      (1797 rows)     │           │...│
└─────────────┬─────────────┘           └─┬─┘
              │                           │
              │  64 pixel columns         │
              │  + target column          │
              │       pd.DataFrame()      │
              └────────────┬──────────────┘
                           ▼
┌─────────────────────────────────────────────┐
│  DataFrame  (1797 rows x 65 columns)        │
│                                             │
│  pixel_0  pixel_21  ...  pixel_63   target  │
│  ------   --------       --------   ------  │
│     0.0      11.0   ...     0.0        0    │
│     0.0       6.0   ...     0.0        1    │
│     0.0      16.0   ...     0.0        2    │
│    ...                                      │
└─────────────────────────────────────────────┘
  <---- 64 feature columns ---->  + 1 target

columns= gave each of the 64 data columns a name (pixel_0 ... pixel_63).
df["target"] = added a 65th column with the labels.
```

> **Want to go deeper?** [pandas — Wikipedia](https://en.wikipedia.org/wiki/Pandas_(software))

---

## Concept: f-Strings and List Comprehensions

Two Python patterns you will see constantly:

**f-string** — embed a variable inside a string:
```python
i = 5
print(f"pixel_{i}")   # prints:  pixel_5
```

**List comprehension** — a concise loop that builds a list:
```python
names = [f"pixel_{i}" for i in range(5)]
# result: ["pixel_0", "pixel_1", "pixel_2", "pixel_3", "pixel_4"]
```

Together: `[f"pixel_{i}" for i in range(64)]` generates all 64 column names in one line.

> **Want to go deeper?** [List comprehension — Wikipedia](https://en.wikipedia.org/wiki/List_comprehension)

---

## What Each Task Asks You to Do

### Task 1 — Load the dataset
Call `load_digits()` and store the result. Print its type and field names.

This confirms the library is available and gives you a first look at the object structure.

### Task 2 — Access the raw arrays
Print the `.shape` of `digits.data` and `digits.target`.

`.shape` returns a tuple: `(rows, columns)`. For data that is 1797 rows × 64 columns, shape is `(1797, 64)`. For a 1D label array of 1797 values, shape is `(1797,)` — note the trailing comma meaning 1-dimensional.

### Task 3 — Wrap in a DataFrame
Create a DataFrame with 64 feature columns named `pixel_0` through `pixel_63`, then add a `target` column.

After this step, `df.shape` should be `(1797, 65)` — 64 features plus the target column.

### Task 4 — Inspect one sample
Print the label and first 10 pixel values of the very first row.

`digits.data[0, :10]` means: row 0, columns 0 through 9. The `:10` is Python slice notation — it means "up to but not including index 10."

---

## Common Mistakes

**`NameError: name 'digits' is not defined`**
You haven't run the `load_digits()` line yet. Make sure Task 1 code is above Task 2.

**Shape shows `(1797, 65)` instead of `(1797, 64)`**
You accidentally included the `target` column when creating the DataFrame. Pass only `digits.data`, not `df`, to `pd.DataFrame()`.

**`KeyError: 'target'`**
You haven't added the target column yet. The line `df["target"] = digits.target` must come after the DataFrame is created.

---

## Now Open the Lab

[01_lab_loading_data.md](01_lab_loading_data.md)

---

## Next

[02_guide_statistics.md](02_guide_statistics.md) — shape, value ranges, `.describe()`, and how to find useless features before you even start training.
