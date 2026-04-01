import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

image = digits.images[0].astype(int)
print(f"Image index 0 — label: {digits.target[0]}")
for row in image:
    print("  ".join(f"{v:2d}" for v in row))

for digit in [1, 7]:
    example = digits.images[digits.target == digit][0].astype(int)
    print(f"\n--- Digit {digit} ---")
    for row in example:
        print("  ".join(f"{v:2d}" for v in row))

correlations = df.corr()["target"].abs().drop("target").sort_values(ascending=False)
print("\nTop 10 pixels most correlated with digit label:")
print(correlations.head(10).round(2))

print("\n=== Security Feature Analogy ===")
print("Digits:   [0, 0, 5, 13, 9, ...]  <- pixel brightnesses")
print("Network:  [1048576, 443, 0.24, 2, 14, ...]  <- bytes, port, duration, flags ...")
print("Same structure. Same algorithms. Different domain.")

print("\n--- Exercise 5 complete ---")
print("You have completed all 5 exercises for Lesson 1.1.")
print("")
print("Next steps:")
print("  1. Open the matching solution file to compare your code")
print("  2. Read the theory notes: ../notes.md")
print("  3. Move to Lesson 1.2: ../../../lesson2_linear_regression/")
