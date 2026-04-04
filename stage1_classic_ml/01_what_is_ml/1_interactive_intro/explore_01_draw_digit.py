# Explore 1 — Draw Your Own Digit
#
# Can you draw a "7" using only numbers from 0 to 16?
#
# Edit the grid below, then run:
#   python explore_01_draw_digit.py
#
# 0 = white (no ink)
# 16 = black (full ink)
# Values in between = shades of grey

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

if plt.get_backend().lower() == "agg":
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_01_draw_digit.py")
    sys.exit(1)

# ╔══════════════════════════════════════════════════════════════╗
# ║  EDIT THIS GRID — draw a digit using numbers 0 to 16       ║
# ║  0 = white, 16 = black                                     ║
# ║                                                             ║
# ║  Try drawing a 7, then try other digits.                    ║
# ╚══════════════════════════════════════════════════════════════╝

my_digit = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
], dtype=float)

# Load a real digit for comparison
digits = load_digits()
real_7 = digits.images[digits.target == 7][0]

# Show side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

ax1.imshow(my_digit, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
ax1.set_title("Your digit", fontsize=14)
ax1.axis("off")

ax2.imshow(real_7, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
ax2.set_title("Real 7 from dataset", fontsize=14)
ax2.axis("off")

fig.suptitle("Can you match the real one?", fontsize=16)
plt.tight_layout()
plt.show()

# After closing, show both as flat arrays
print("\nYour digit as 64 numbers:")
print(my_digit.astype(int).flatten())
print(f"\nReal 7 as 64 numbers:")
print(real_7.astype(int).flatten())

diff = np.abs(my_digit - real_7).sum()
print(f"\nTotal pixel difference: {diff:.0f}")
print(f"(Lower is more similar. 0 means identical.)")
print(f"\n  Next: python explore_02_spot_difference.py")
