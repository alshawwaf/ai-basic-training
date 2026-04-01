# Lab — Exercise 1: Understanding Regression

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_understanding_regression.py` in this folder.

---

## Step 2: Add the imports and dataset generation

The dataset is generated with a fixed seed so your results will match the expected output. Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
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

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
```

Run your file. You should see shape `(500, 2)`, both columns as `float64`, and zero missing values.

---

## Step 4: Print summary statistics

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Summary Statistics")
print("=" * 60)

print(df.describe())
```

Run your file. You should see mean `requests_per_second` around 103 and mean `response_time_ms` around 215.

---

## Step 5: Create a scatter plot

A scatter plot shows whether a linear relationship exists before you build any model. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Scatter Plot")
print("=" * 60)

plt.figure(figsize=(8, 5))
plt.scatter(df["requests_per_second"], df["response_time_ms"], alpha=0.4)
plt.xlabel("Requests per Second")
plt.ylabel("Response Time (ms)")
plt.title("Server Load vs Response Time")
plt.tight_layout()
plt.show()
```

Run your file. You should see a clear upward trend with noise around a straight line — confirming that linear regression is appropriate.

---

## Step 6: Add the completion message

```python
print("\n--- Exercise 1 complete. Move to exercise2_train_test_split.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
