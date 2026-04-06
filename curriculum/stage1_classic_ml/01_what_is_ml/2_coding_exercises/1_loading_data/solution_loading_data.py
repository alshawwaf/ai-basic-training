import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

# Load a built-in dataset of 1797 handwritten digit images (8x8 pixels each)
digits = load_digits()

print("##SECTION:Load the dataset##")
# Inspect the Bunch object — it behaves like a dict with .attribute access
print("Dataset loaded.")
print(f"Type: {type(digits)}")
print(f"Fields available: {list(digits.keys())}")

# .data holds the feature matrix (samples x features), .target holds the labels
print(f"Features (X) shape: {digits.data.shape}")
print(f"Labels   (y) shape: {digits.target.shape}")

print("##SECTION:Convert to DataFrame##")
# Convert the numpy arrays into a DataFrame for easier exploration
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

# Show a few selected columns instead of all 65 — keeps the output readable
# Centre pixels (21, 28, 36, 43) — edge pixels are mostly zero
preview_cols = ["pixel_21", "pixel_28", "pixel_36", "pixel_43", "target"]
print("\nFirst 5 rows (selected columns):")
print(df[preview_cols].head().to_string())
print(f"\nFull DataFrame shape: {df.shape}")
print(f"Columns: pixel_0 ... pixel_63, target  ({df.shape[1]} total)")

print("##SECTION:Inspect a single sample##")
# Sanity-check: look at one sample to see what the raw data looks like
print(f"\nFirst sample — label: {digits.target[0]}")
print(f"First 10 pixel values: {digits.data[0, :10]}")

print("\n--- Exercise 1 complete. Move to 02_statistics.py ---")
