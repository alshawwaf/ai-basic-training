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

print("=" * 60)
print("TASK 1 — Dataset Inspection")
print("=" * 60)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

print("\n" + "=" * 60)
print("TASK 2 — Summary Statistics")
print("=" * 60)

print(df.describe())

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

print("\n--- Exercise 1 complete. Move to exercise2_train_test_split.py ---")
