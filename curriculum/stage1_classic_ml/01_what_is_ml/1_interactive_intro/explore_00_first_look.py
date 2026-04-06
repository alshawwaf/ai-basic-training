"""
Explore 00 — First Look
=======================
A random handwritten digit pops up. Your job: name it before reading
anything below the image.

Run this a few times. Notice how some digits are easy, some are messy,
and a few would stump even a person. That uncertainty is exactly what
a machine learning model has to deal with.
"""
import sys
import random
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this script from a normal terminal (python explore_00_first_look.py).")
    sys.exit(1)

digits = load_digits()
idx = random.randint(0, len(digits.images) - 1)

fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(digits.images[idx], cmap="gray_r")
ax.set_title("What digit is this?", fontsize=14)
ax.axis("off")
fig.text(0.5, 0.02,
         f"(close the window when ready — answer: {digits.target[idx]})",
         ha="center", fontsize=9, color="#888")
plt.tight_layout()
plt.show()

print()
print(f"Sample index : {idx}")
print(f"True label   : {digits.target[idx]}")
print(f"Image shape  : {digits.images[idx].shape}  (8x8 grayscale)")
print()
print("Run this script again — you'll get a different digit each time.")
print("Next: explore_01_draw_digit.py")
