import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

digits = load_digits()

print("Dataset loaded.")
print(f"Type: {type(digits)}")
print(f"Fields available: {list(digits.keys())}")

print(f"Features (X) shape: {digits.data.shape}")
print(f"Labels   (y) shape: {digits.target.shape}")

df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

print("\nFirst 3 rows of the DataFrame:")
print(df.head(3).to_string())
print(f"\nDataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")

print(f"\nFirst sample — label: {digits.target[0]}")
print(f"First 10 pixel values: {digits.data[0, :10]}")

print("\n--- Exercise 1 complete. Move to exercise2_statistics.py ---")
