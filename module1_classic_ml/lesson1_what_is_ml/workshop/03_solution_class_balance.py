import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

# Count how many samples exist for each digit (0-9)
counts = df["target"].value_counts().sort_index()
print("Samples per class:")
print(counts)

# Compute the imbalance ratio — large ratios mean the model can "cheat"
# by always predicting the majority class
majority = counts.max()
minority = counts.min()
ratio = majority / minority

print(f"\nMajority class: {majority} samples")
print(f"Minority class: {minority} samples")
print(f"Imbalance ratio: {ratio:.2f} : 1")
print("This dataset is well balanced.")

# Simulate an imbalanced intrusion-detection scenario to show why balance matters
normal_count = 950
attack_count = 50
total = normal_count + attack_count

# A model that blindly labels everything "normal" gets 95% accuracy but catches nothing
naive_accuracy = normal_count / total
attack_recall = 0.0

print("\n--- Simulated Security Dataset ---")
print(f"Normal connections : {normal_count:4d}  ({normal_count/total*100:.1f}%)")
print(f"Attack connections : {attack_count:4d}   ({attack_count/total*100:.1f}%)")
print()
print("A naive model (always predicts 'normal'):")
print(f"  Accuracy       : {naive_accuracy*100:.1f}%   <- looks great!")
print(f"  Attacks caught :  {attack_recall*100:.1f}%   <- completely useless")
print()
print("This is why accuracy alone is a dangerous metric in security.")

# Simple text-based bar chart to visualise class distribution in the terminal
print("\nClass distribution:")
for label, count in counts.items():
    bar = "#" * count
    print(f"{label} | {bar} ({count})")

print("\n--- Exercise 3 complete. Move to 04_visualise.py ---")
