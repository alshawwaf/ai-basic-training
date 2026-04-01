# Exercise 1 — Loading a Dataset

> Read this guide fully before opening the exercise file.

---

## What You Will Learn

- How scikit-learn packages and delivers datasets
- What a `Bunch` object is and how to navigate it
- How to wrap raw data in a pandas `DataFrame`
- The difference between **features** and **labels** — the most fundamental concept in all of supervised ML

---

## Concept: The Anatomy of a Dataset

Every supervised ML problem has exactly two things:

```
Features (X)  —  what you measure        (the inputs)
Labels   (y)  —  what you want to predict (the outputs)
```

In a digits recognition problem:

```
Features  =  64 pixel brightness values  (what the image looks like)
Label     =  the digit 0–9               (what the correct answer is)
```

In a phishing detection problem:

```
Features  =  URL length, number of dots, has @ symbol, ...
Label     =  phishing=1 or legitimate=0
```

In a network intrusion problem:

```
Features  =  bytes sent, duration, unique ports, SYN flag count, ...
Label     =  malicious=1 or benign=0
```

The structure is always the same. The domain changes; the math does not.

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

---

## Concept: The `load_digits()` Return Value — a Bunch Object

`load_digits()` returns a `Bunch` — a container object that works like a Python dictionary with dot-notation access:

| Field | Type | Contents |
|-------|------|----------|
| `digits.data` | ndarray (1797, 64) | Raw pixel values — one row per image, one column per pixel |
| `digits.target` | ndarray (1797,) | Correct label (0–9) for each image |
| `digits.images` | ndarray (1797, 8, 8) | Same pixel values arranged as 8×8 grids — only used for plotting |
| `digits.target_names` | ndarray ([0..9]) | The list of all unique class labels |
| `digits.DESCR` | str | Full text description of the dataset |

`digits.data` and `digits.images` contain **identical pixel values** — just different shapes. Use `.data` for feeding the model (it wants flat rows), `.images` for plotting (you need the 8×8 grid).

---

## Concept: Why We Wrap Data in a DataFrame

`digits.data` is a raw NumPy array — just a block of numbers with no column names. Feeding raw arrays into ML pipelines works, but it makes debugging much harder.

Wrapping it in a pandas `DataFrame` gives you:

- **Named columns** — `pixel_0`, `pixel_1`, ... so you can refer to features by name
- **Easy inspection** — `.head()`, `.describe()`, `.value_counts()` all work
- **Filtering** — `df[df["target"] == 3]` to slice to one class
- **Consistent interface** — most scikit-learn functions accept DataFrames directly

The pattern is the same for every dataset you will ever load:

```python
df = pd.DataFrame(raw_data, columns=column_names)
df["target"] = labels
```

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

## Expected Outputs at a Glance

**Task 1**
```
Dataset loaded.
Type: <class 'sklearn.utils._bunch.Bunch'>
Fields available: ['data', 'target', 'target_names', 'images', 'DESCR']
```

**Task 2**
```
Features (X) shape: (1797, 64)
Labels   (y) shape: (1797,)
```

**Task 3**
```
First 3 rows of the DataFrame:
   pixel_0  pixel_1  pixel_2  ...  pixel_63  target
0      0.0      0.0      5.0  ...       0.0       0
1      0.0      0.0      0.0  ...       0.0       1
2      0.0      0.0      0.0  ...       0.0       2

DataFrame shape: (1797, 65)
```

**Task 4**
```
First sample — label: 0
First 10 pixel values: [ 0.  0.  5. 13.  9.  1.  0.  0.]
```

---

## Common Mistakes

**`NameError: name 'digits' is not defined`**
You haven't run the `load_digits()` line yet. Make sure Task 1 code is above Task 2.

**Shape shows `(1797, 65)` instead of `(1797, 64)`**
You accidentally included the `target` column when creating the DataFrame. Pass only `digits.data`, not `df`, to `pd.DataFrame()`.

**`KeyError: 'target'`**
You haven't added the target column yet. The line `df["target"] = digits.target` must come after the DataFrame is created.

---

## Now Open the Exercise File

[exercise1_loading_data.py](exercise1_loading_data.py)

Fill in each `# >>> YOUR CODE HERE` block, run after each task, and verify your output matches.

---

## Next

[exercise2_statistics.md](exercise2_statistics.md) — shape, value ranges, `.describe()`, and how to find useless features before you even start training.
