# Lab — Exercise 2: Train/Test Split

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_train_test_split.py` in this folder.

---

## Step 2: Add the imports and setup

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

np.random.seed(42)
n = 500
requests_per_second = np.random.uniform(5, 200, n)
response_time_ms = 1.8 * requests_per_second + 30 + np.random.normal(0, 15, n)
df = pd.DataFrame({
    "requests_per_second": requests_per_second,
    "response_time_ms": response_time_ms
})
X = df[["requests_per_second"]]
y = df["response_time_ms"]
```

---

## Step 3: Evaluate on training data (the wrong way)

This step intentionally demonstrates the problem — a model that has "seen" all the data scores too well. Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Evaluating on training data (WRONG)")
print("=" * 60)

model = LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)
print(f"R² on full dataset (train=test): {r2:.3f}")
```

Run your file. You should see:
```
R² on full dataset (train=test): 0.978
```

---

## Step 4: Perform the train/test split

`train_test_split` shuffles the data randomly and holds out 20% for testing. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Train/test split shapes")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"X_train: {X_train.shape}   y_train: {y_train.shape}")
print(f"X_test:  {X_test.shape}    y_test:  {y_test.shape}")
total = len(X_train) + len(X_test)
print(f"Total rows: {total} {'✓' if total == 500 else '✗'}")
```

Run your file. You should see:
```
X_train: (400, 1)   y_train: (400,)
X_test:  (100, 1)   y_test:  (100,)
Total rows: 500 ✓
```

---

## Step 5: Compare train vs test R²

Train a fresh model on training data only, then evaluate on both sets. The gap reveals overfitting. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Train vs Test R²")
print("=" * 60)

model2 = LinearRegression()
model2.fit(X_train, y_train)
train_r2 = model2.score(X_train, y_train)
test_r2  = model2.score(X_test,  y_test)
print(f"Training R²: {train_r2:.3f}")
print(f"Test R²:     {test_r2:.3f}")
print(f"Gap (overfit indicator): {abs(train_r2 - test_r2):.3f}")
```

Run your file. You should see:
```
Training R²: 0.977
Test R²:     0.973
Gap (overfit indicator): 0.004
```

A gap of 0.004 is very small — the model generalises well.

---

## Step 6: Add the completion message

```python
print("\n--- Exercise 2 complete. Move to 03_fit_and_predict.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `solution_train_test_split.py` file if anything looks different.
