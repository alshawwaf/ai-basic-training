# Loading a Dataset

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

1. **Raw Data** — logs, images, URLs, packets, sensor data — whatever you have
2. **Extract Features (X) and Labels (y)** — turn raw data into numbers, identify what you're predicting
3. **`model.fit(X, y)`** — the model finds the pattern
4. **`model.predict(X_new)`** — apply the pattern to new data

> **Want to go deeper?** [Supervised Learning — Wikipedia](https://en.wikipedia.org/wiki/Supervised_learning)

---

## Concept: The Digits Dataset

We use the UCI Optical Recognition of Handwritten Digits dataset — a classic benchmark that ships inside scikit-learn. No download required.

Each sample is an 8×8 greyscale image of a handwritten digit. Each cell is a pixel brightness from 0 (white) to 16 (full ink). On the left are the raw numbers, on the right is what those same numbers look like when painted as pixels:

<div class="lecture-visual">
  <img src="/static/lecture_assets/loading_digit_sample.png" alt="The 8x8 numpy array of pixel values for the first digit sample on the left, and the same array rendered as a greyscale handwritten 0 on the right">
  <div class="vis-caption">Real output of <code>digits.images[0]</code>. The hollow centre of the 0 is visible in both views — the right column rows 3–6 are 0 (white background).</div>
</div>

The image is then flattened to a single row of 64 numbers before the model receives it.

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

That bundle is called a `Bunch` — a container object that works like a Python dictionary with dot-notation access. Calling `load_digits()` once gives you the four fields you actually need:

<div class="lecture-visual">
  <img src="/static/lecture_assets/loading_bunch_structure.png" alt="Diagram showing load_digits() at the top with arrows pointing down to four child boxes labelled .data, .target, .images, and .DESCR with their shapes and roles">
  <div class="vis-caption">A Bunch is a dictionary you can also access with dot notation — <code>digits.data</code> and <code>digits["data"]</code> return the same array.</div>
</div>

Most of the fields inside are **ndarray** objects. An `ndarray` (short for *n-dimensional array*) is NumPy's core data type — a grid of numbers that can have any number of dimensions. A 1D ndarray is a list of numbers, a 2D ndarray is a table (rows and columns), and a 3D ndarray is a stack of tables. All ML data flows through ndarrays because they are fast and memory-efficient.

| Field | Type | What it is |
|:---|:---|:---|
| `digits.data` | ndarray (1797, 64) | Raw pixel values — one row per image, one column per pixel. **Feed this to the model.** |
| `digits.target` | ndarray (1797,) | Correct label (0-9) for each image. **These are the answers.** |
| `digits.images` | ndarray (1797, 8, 8) | Same pixel values arranged as 8x8 grids — **only used for plotting.** |
| `digits.target_names` | ndarray ([0..9]) | The list of all unique class labels |
| `digits.DESCR` | str | Full text description of the dataset |

`digits.data` and `digits.images` contain **identical pixel values** — just different shapes. Use `.data` for feeding the model (it wants flat rows), `.images` for plotting (you need the 8x8 grid).

**Same pixels, two shapes:**

| Field | Shape | Looks like | Used for |
|---|---|---|---|
| `.data[0]`   | `(64,)`   | `[0, 0, 5, 13, 9, 1, 0, 0, 0, 0, …]` — 64 values in one flat row | what the **model** sees |
| `.images[0]` | `(8, 8)`  | the same 64 numbers reshaped into an 8 × 8 grid                  | what the **image** looks like (for plotting) |

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/loading_mask_filter.png" alt="Three panels: target column with values 5 3 7 3 1 8 3 0; the same column after == 3 with green True boxes for the threes and red False boxes for the rest; the filtered result showing only the three 3s">
  <div class="vis-caption">Boolean-mask filtering — <code>== 3</code> turns the target column into True/False, then <code>df[mask]</code> keeps only the True rows.</div>
</div>

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

**Two ndarrays go in:**

| Source | Shape | Becomes |
|---|---|---|
| `digits.data` | `(1797, 64)` — 64 pixel values per row | 64 columns named `pixel_0` … `pixel_63` |
| `digits.target` | `(1797,)` — one label per row | 1 column named `target` |

**One DataFrame comes out** — `df` with shape `(1797, 65)`. Here are the first six rows of the real DataFrame, with a few representative pixel columns and the target column highlighted in yellow:

<div class="lecture-visual">
  <img src="/static/lecture_assets/loading_dataframe_preview.png" alt="Pandas DataFrame head with cyan header row showing pixel_0 pixel_1 pixel_21 pixel_32 pixel_43 pixel_63 target columns and six rows of integer values">
  <div class="vis-caption">Real output of <code>df.head(6)</code> after wrapping <code>digits.data</code>. 64 feature columns + 1 target column = shape <code>(1797, 65)</code>.</div>
</div>

`columns=` gave each of the 64 data columns a name (`pixel_0` … `pixel_63`). `df["target"] =` added a 65th column with the labels — so the final shape is **64 feature columns + 1 target column**.

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
