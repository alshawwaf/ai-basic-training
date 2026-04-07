import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

print("##SECTION:Raw pixel grid##")
# Print the raw 8x8 pixel grid — this is exactly what the ML model receives as input
image = digits.images[0].astype(int)
print(f"Image index 0 — label: {digits.target[0]}")
for row in image:
    print("  ".join(f"{v:2d}" for v in row))

print("##SECTION:Side-by-side comparison (1 vs 7)##")
# Compare two digits side-by-side to see how different classes differ numerically
for digit in [1, 7]:
    example = digits.images[digits.target == digit][0].astype(int)
    print(f"\n--- Digit {digit} ---")
    for row in example:
        print("  ".join(f"{v:2d}" for v in row))

print("##SECTION:Most predictive pixels##")
# Find which pixel positions are most predictive of the label
# High correlation means that pixel carries useful signal for classification
correlations = df.corr()["target"].abs().drop("target").sort_values(ascending=False)
print("\nTop 10 pixels most correlated with digit label:")
print(correlations.head(10).round(2))

print("##SECTION:Security feature analogy##")
# Key takeaway: to the model, an image is just a row of numbers — same as network logs
print("\n=== Security Feature Analogy ===")
print("Digits:   [0, 0, 5, 13, 9, ...]  <- pixel brightnesses")
print("Network:  [1048576, 443, 0.24, 2, 14, ...]  <- bytes, port, duration, flags ...")
print("Same structure. Same algorithms. Different domain.")

print("\n--- What the Model Actually Sees — complete ---")
print("You have completed all 5 hands-on labs for Lesson 1.1.")
print("")
print("Next steps:")
print("  1. Open the matching solution file to compare your code")
print("  2. Read the theory notes: README.md")
print("  3. Move to Lesson 1.2: ../../../02_linear_regression/")
