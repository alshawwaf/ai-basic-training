import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate a synthetic dataset simulating server load vs response time
# The relationship is linear (1.8x + 30) with random noise to mimic real-world variance
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

# Check structure, types, and completeness — standard first steps before any analysis
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

print("\n" + "=" * 60)
print("TASK 2 — Summary Statistics")
print("=" * 60)

# describe() gives count, mean, std, min/max — helps spot outliers and skew
print(df.describe())

print("\n" + "=" * 60)
print("TASK 3 — Scatter Plot")
print("=" * 60)

# Scatter plot reveals whether a linear model is appropriate for this data
plt.figure(figsize=(8, 5))
plt.scatter(df["requests_per_second"], df["response_time_ms"], alpha=0.4)
plt.xlabel("Requests per Second")
plt.ylabel("Response Time (ms)")
plt.title("Server Load vs Response Time")
plt.tight_layout()
plt.show()

print("\n--- Exercise 1 complete. Move to 02_train_test_split.py ---")
