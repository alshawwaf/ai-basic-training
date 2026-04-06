"""
Explore 01 — Draw a Digit by Hand
=================================
Pixels are just numbers. Edit the MY_DIGIT grid below, save the file,
re-run the script, and watch your numbers turn into a picture.

Rules of the game:
- 8 rows, 8 columns
- Each value is brightness, 0 (white) to 16 (black)
- Try drawing your favourite digit, then see how it compares to a
  real sample from the dataset

CHALLENGES (try at least 2):
1. Draw the digit "3" without looking at the sample below.
2. Use only values of 0 and 16 (no shades of grey). How does it look?
3. Replace MY_DIGIT with `np.random.randint(0, 17, (8, 8))`. Random noise
   or a recognisable digit?
4. Make a digit that even YOU can't recognise. That's how messy real
   data looks to a model.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_01_draw_digit.py")
    sys.exit(1)

# ===== EDIT THIS GRID =====
# Currently a hand-drawn "7". Change the numbers and re-run.
MY_DIGIT = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0, 16, 16, 16, 16, 16, 16,  0],
    [ 0,  0,  0,  0,  0, 12,  0,  0],
    [ 0,  0,  0,  0, 14,  0,  0,  0],
    [ 0,  0,  0, 16,  0,  0,  0,  0],
    [ 0,  0, 14,  0,  0,  0,  0,  0],
    [ 0,  0, 12,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
])
# ==========================

assert MY_DIGIT.shape == (8, 8), "MY_DIGIT must be 8 rows by 8 columns."
assert MY_DIGIT.min() >= 0 and MY_DIGIT.max() <= 16, "Values must be 0..16."

# Compare against a real sample with the same target you think you drew
digits = load_digits()
target_to_compare = 7  # change this to whichever digit you drew
real_sample = digits.images[digits.target == target_to_compare][0]

fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(MY_DIGIT, cmap="gray_r", vmin=0, vmax=16)
axes[0].set_title("Your hand-edited digit")
axes[0].axis("off")
for (i, j), v in np.ndenumerate(MY_DIGIT):
    if v > 0:
        axes[0].text(j, i, str(int(v)),
                     ha="center", va="center",
                     color="white" if v > 8 else "black", fontsize=8)

axes[1].imshow(real_sample, cmap="gray_r", vmin=0, vmax=16)
axes[1].set_title(f"Real digit {target_to_compare} from the dataset")
axes[1].axis("off")
for (i, j), v in np.ndenumerate(real_sample.astype(int)):
    if v > 0:
        axes[1].text(j, i, str(int(v)),
                     ha="center", va="center",
                     color="white" if v > 8 else "black", fontsize=8)

plt.tight_layout()
plt.show()

print()
print("Your grid:")
for row in MY_DIGIT:
    print("  ".join(f"{int(v):2d}" for v in row))
print()
print(f"Sum of brightness in your digit  : {int(MY_DIGIT.sum())}")
print(f"Sum of brightness in real sample : {int(real_sample.sum())}")
print()
print("Edit MY_DIGIT, save, re-run. Try the challenges in the file header.")
print("Next: explore_02_spot_difference.py")
