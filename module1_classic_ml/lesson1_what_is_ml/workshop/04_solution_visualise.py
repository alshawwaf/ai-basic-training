import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

# Plot one representative sample for each digit class (0-9)
fig, axes = plt.subplots(1, 10, figsize=(18, 2))
fig.suptitle("One example of each digit class (0-9)", fontsize=12)
for digit in range(10):
    ax = axes[digit]
    # Boolean-index into .images to grab the first sample matching this label
    sample = digits.images[digits.target == digit][0]
    ax.imshow(sample, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")
plt.tight_layout()
plt.show()

# Show two examples per class to illustrate within-class variation
fig, axes = plt.subplots(2, 10, figsize=(18, 4))
fig.suptitle("Two examples of each digit class (0-9)", fontsize=12)
for digit in range(10):
    samples = digits.images[digits.target == digit]
    for row_idx, sample in zip(axes, samples[:2]):
        row_idx[digit].imshow(sample, cmap="gray_r")
        row_idx[digit].set_title(str(digit))
        row_idx[digit].axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/sample_digits.png")
plt.show()

# Average all images in each class — reveals the "prototype" shape the model learns
fig, axes = plt.subplots(1, 10, figsize=(18, 2))
fig.suptitle("Average image per digit class", fontsize=12)
for digit, ax in enumerate(axes):
    mean_image = digits.images[digits.target == digit].mean(axis=0)
    ax.imshow(mean_image, cmap="gray_r")
    ax.set_title(str(digit))
    ax.axis("off")

plt.tight_layout()
plt.savefig("module1_classic_ml/lesson1_what_is_ml/workshop/average_digits.png")
plt.show()

print("\n--- Exercise 4 complete. Move to 05_what_model_sees.py ---")
