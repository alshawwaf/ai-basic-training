# Lesson 1.1 — ML Concepts and Exploring Data
#
# Before training any model, we need to understand our data.
# A model is only as good as the data you feed it.
#
# We'll use scikit-learn's built-in breast cancer dataset as a warm-up —
# it's a clean, well-understood classification problem:
# given measurements of a cell nucleus, is the tumour malignant or benign?
# (Binary classification — same structure as "is this traffic malicious or not")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer

# ── 1. Load the dataset ────────────────────────────────────────────────────────
data = load_breast_cancer()

# Wrap in a DataFrame so it's easy to inspect
df = pd.DataFrame(data.data, columns=data.feature_names)
df["target"] = data.target           # 0 = malignant, 1 = benign
df["target_name"] = df["target"].map({0: "malignant", 1: "benign"})

# ── 2. First look ──────────────────────────────────────────────────────────────
print("=== Dataset shape ===")
print(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

print("\n=== First 5 rows ===")
print(df.head())

print("\n=== Class balance (how many malignant vs benign) ===")
print(df["target_name"].value_counts())

print("\n=== Basic statistics ===")
print(df.describe().round(2))

# ── 3. Visualise two features that might separate the classes ──────────────────
# In cybersecurity you'd do the same: plot two features and see if
# "attack" and "normal" traffic cluster differently.

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, feature in zip(axes, ["mean radius", "mean texture"]):
    for label, group in df.groupby("target_name"):
        ax.hist(group[feature], alpha=0.6, label=label, bins=30)
    ax.set_title(f"Distribution of '{feature}'")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")
    ax.legend()

plt.tight_layout()
plt.savefig("stage1_ml/lesson1_data_exploration.png")
plt.show()
print("\nPlot saved to stage1_ml/lesson1_data_exploration.png")

# ── 4. Key takeaway ────────────────────────────────────────────────────────────
# If the histograms for malignant vs benign barely overlap → easy for a model
# If they overlap a lot → the model will need to use multiple features together
#
# Next lesson: we feed these features into our first ML model.
