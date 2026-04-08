# Lab — Exercise 1: Understanding Regression

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_understanding_regression.py` in this folder.

---

## Step 2: Add the imports and dataset generation

The dataset is generated with a fixed seed so your results will match the expected output. Add these imports to the top of your file:

```python
import numpy as np                          # NumPy: random sampling + array math
import pandas as pd                         # pandas: tabular data with labels
import matplotlib.pyplot as plt             # matplotlib: plotting

np.random.seed(42)                           # fix the RNG so everyone gets the same numbers
n = 500                                      # number of synthetic server-load samples
requests_per_second = np.random.uniform(5, 200, n)   # uniform load between 5 and 200 req/s
# True relationship: 1.8 ms per request + 30 ms baseline + Gaussian noise (std=15)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({                          # bundle the two arrays into a labelled table
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
```

---

## Step 3: Inspect the dataset

Check shape, column names, data types, first rows, and missing values before touching any modelling code. Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Dataset Inspection")
print("=" * 60)

print(f"Dataset shape: {df.shape}")           # (rows, cols) — should be (500, 2)
print(f"Columns: {list(df.columns)}")          # the two column names
print(f"Dtypes:\n{df.dtypes}")                 # both should be float64
print(f"\nFirst 5 rows:\n{df.head()}")         # quick sanity check on the data
print(f"\nMissing values:\n{df.isnull().sum()}")  # should be all zeros for a clean dataset
```

Run your file. You should see shape `(500, 2)`, both columns as `float64`, and zero missing values.

---

## Step 4: Print summary statistics

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Summary Statistics")
print("=" * 60)

print(df.describe())                           # count, mean, std, min/max, quartiles per column
```

Run your file. You should see mean `requests_per_second` around 103 and mean `response_time_ms` around 215.

---

## Step 5: Create a scatter plot

A scatter plot shows whether a linear relationship exists before you build any model. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Scatter Plot")
print("=" * 60)

plt.figure(figsize=(8, 5))                     # 8x5 inch canvas
# alpha=0.4 makes points semi-transparent so overlapping clusters become visible
plt.scatter(df["requests_per_second"], df["response_time_ms"], alpha=0.4)
plt.xlabel("Requests per Second")              # x-axis = the input feature
plt.ylabel("Response Time (ms)")               # y-axis = what we want to predict
plt.title("Server Load vs Response Time")
plt.tight_layout()                              # auto-adjust margins to avoid clipping
plt.show()                                      # open the figure window
```

Run your file. You should see a clear upward trend with noise around a straight line — confirming that linear regression is appropriate.

---

## Step 6: Add the completion message

```python
print("\n--- Exercise 1 complete. Move to 02_train_test_split.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `solution_understanding_regression.py` file if anything looks different.
