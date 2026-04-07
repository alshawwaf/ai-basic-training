import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

print("##SECTION:Dataset shape##")
# Get the basic shape of the data — how many samples, features, and output classes
print(f"Samples  : {digits.data.shape[0]}")
print(f"Features : {digits.data.shape[1]}")
print(f"Classes  : {digits.target_names}")

# Knowing the feature range matters — some ML algorithms expect normalised inputs
print(f"\nPixel value range: min={int(digits.data.min())}, max={int(digits.data.max())}")
print("(0 = white background, 16 = maximum ink density)")

print("##SECTION:Summary statistics (.describe)##")
# Use .describe() to spot outliers, skew, or features with near-zero variance
subset = df[["pixel_0", "pixel_10", "pixel_32", "pixel_63", "target"]]
print("\nSummary statistics:")
print(subset.describe().round(2))

print("##SECTION:Missing values check##")
# Check for missing values — real-world data almost always has gaps
missing = df.isnull().sum()
print("\nMissing values per column (showing first 5):")
print(missing.head())
print(f"\nTotal missing values: {df.isnull().sum().sum()}")

print("\n--- Shape, Statistics, and Missing Values — complete ---")
