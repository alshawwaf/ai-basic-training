# Lesson 1.1 — ML Concepts and Exploring Data
#
# Before training any model, we need to understand our data.
# A model is only as good as the data you feed it.
#
# We'll use scikit-learn's built-in digits dataset:
# 1,797 handwritten digits (0–9), each represented as an 8x8 pixel image.
#
# Why this example?
#   - It's visual — you can literally see what the model will learn
#   - It's the same structure as any pattern recognition problem in security:
#     raw measurements (pixels / log fields) → label (digit / attack type)
#   - We'll come back to digits with a neural network in Module 3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

# ── 1. Load the dataset ────────────────────────────────────────────────────────
digits = load_digits()

# digits.data   → 1797 rows × 64 columns (each pixel is a feature)
# digits.target → the correct digit label for each image (0–9)
# digits.images → same data reshaped as 8×8 grids (useful for plotting)

df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

# ── 2. First look ──────────────────────────────────────────────────────────────
print("=== Dataset shape ===")
print(f"Images : {digits.data.shape[0]}")
print(f"Features per image : {digits.data.shape[1]}  (8×8 pixels, flattened)")
print(f"Classes : {len(digits.target_names)}  → {list(digits.target_names)}")

print("\n=== Class balance (samples per digit) ===")
print(df["target"].value_counts().sort_index().to_string())

print("\n=== Pixel value range ===")
print(f"Min: {digits.data.min():.0f}  |  Max: {digits.data.max():.0f}  (0 = white, 16 = black)")

# ── 3. Visualise sample images ─────────────────────────────────────────────────
# Each row in the dataset is a flat list of 64 numbers.
# Reshaping it to 8×8 turns it back into an image.

fig, axes = plt.subplots(2, 10, figsize=(18, 4))
fig.suptitle("Sample images — one per digit class (two different examples each)", fontsize=12)

for digit in range(10):
    samples = digits.images[digits.target == digit]
    for row, sample in zip(axes, samples[:2]):
        row[digit].imshow(sample, cmap="gray_r")
        row[digit].set_title(str(digit))
        row[digit].axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_sample_digits.png")
plt.show()
print("\nPlot saved → module1_classic_ml/lesson1_sample_digits.png")

# ── 4. What does the data actually look like as numbers? ───────────────────────
print("\n=== One image as an 8×8 grid of pixel values ===")
print("(Each number is a pixel brightness — 0 = white, 16 = black)")
print()
sample_image = digits.images[0]
for row in sample_image.astype(int):
    print("  " + "  ".join(f"{v:2d}" for v in row))
print(f"\n  ↑ This is the digit '{digits.target[0]}'")

# ── 5. Visualise average images per class ─────────────────────────────────────
# The "average" of all 0s, all 1s, etc. shows you what a typical digit looks like.
# If two classes look very similar on average → harder for the model to separate them.

fig, axes = plt.subplots(1, 10, figsize=(18, 2))
fig.suptitle("Average pixel pattern for each digit class", fontsize=12)

for digit, ax in enumerate(axes):
    mean_image = digits.images[digits.target == digit].mean(axis=0)
    ax.imshow(mean_image, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_average_digits.png")
plt.show()
print("Plot saved → module1_classic_ml/lesson1_average_digits.png")

# ── Key takeaway ───────────────────────────────────────────────────────────────
# The model never sees images — it sees rows of 64 numbers.
# Your job as an ML practitioner is to make sure those numbers carry enough
# signal for the model to find the pattern.
#
# In security: instead of pixel values, your features might be
# bytes_per_second, unique_ports, entropy, protocol_flags — same idea.
#
# Next lesson: we feed these features into our first ML model.
