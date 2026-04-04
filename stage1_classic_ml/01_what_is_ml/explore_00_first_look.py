# Explore 0 — See a Digit
#
# Run this FIRST. Before reading anything.
#
#   python explore_00_first_look.py
#
# A picture will appear. What digit do you see?
# Close the window to find out.

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_00_first_look.py")
    sys.exit(1)

digits = load_digits()

# Pick a random digit image
idx = np.random.randint(len(digits.images))
image = digits.images[idx]
label = digits.target[idx]

# Show it — no label, no hint
fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(image, cmap="gray_r", interpolation="nearest")
ax.set_title("What digit is this?", fontsize=16)
ax.axis("off")
plt.tight_layout()
plt.show()

# After the learner closes the window, reveal
print(f"\nThat was a {label}.")
print(f"\nBut to a machine learning model, it's not a picture.")
print(f"It's just {image.size} numbers:\n")
print(image.astype(int).flatten())
print(f"\nEvery value is between 0 (white) and 16 (black).")
print(f"The image is {image.shape[0]}x{image.shape[1]} pixels = {image.size} numbers total.")
print(f"\nThis lesson shows you why those numbers matter.")
print(f"\n  Next: python explore_01_draw_digit.py")
