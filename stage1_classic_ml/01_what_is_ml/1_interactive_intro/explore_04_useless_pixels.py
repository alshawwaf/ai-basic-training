# Explore 4 — Find the Useless Pixels
#
# Some pixels in this dataset never change. They carry zero information.
# Drag the slider to set a variance threshold and watch useless pixels disappear.
#
#   python explore_04_useless_pixels.py

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sklearn.datasets import load_digits

if plt.get_backend().lower() == "agg":
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_04_useless_pixels.py")
    sys.exit(1)

digits = load_digits()

# Compute standard deviation of each pixel across all samples
pixel_std = digits.data.std(axis=0).reshape(8, 8)

# Setup figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.22)

# Left: variance heatmap (fixed)
im1 = ax1.imshow(pixel_std, cmap="hot", interpolation="nearest")
ax1.set_title("Pixel variance (std dev)", fontsize=13)
ax1.axis("off")
fig.colorbar(im1, ax=ax1, shrink=0.8)

# Right: useful pixel mask (updates with slider)
threshold_init = 1.0
mask = (pixel_std >= threshold_init).astype(float)
im2 = ax2.imshow(mask, cmap="RdYlGn", interpolation="nearest", vmin=0, vmax=1)
ax2.set_title("Useful pixels", fontsize=13)
ax2.axis("off")

count = mask.sum()
txt = fig.text(
    0.5, 0.04,
    f"Keeping {int(count)} of 64 pixels ({count/64:.0%} of features)",
    ha="center", fontsize=13,
)

fig.suptitle("Drag the slider to change the minimum variance threshold", fontsize=14)

# Slider
ax_slider = plt.axes([0.25, 0.1, 0.50, 0.04])
slider = Slider(ax_slider, "Min std dev", 0.0, 6.0, valinit=threshold_init, valstep=0.1)


def update(val):
    threshold = slider.val
    mask = (pixel_std >= threshold).astype(float)
    im2.set_data(mask)
    count = mask.sum()
    txt.set_text(f"Keeping {int(count)} of 64 pixels ({count/64:.0%} of features)")
    fig.canvas.draw_idle()


slider.on_changed(update)
plt.show()

# After closing
zero_var = np.where(pixel_std.flatten() == 0)[0]
print(f"\nPixels with zero variance (completely useless): {list(zero_var)}")
print(f"These are the corner pixels — they are always background.")
print(f"\nIn security data, this is equivalent to a log field that's always empty.")
print(f"Removing useless features makes models faster and often more accurate.")
print(f"\n  Next: python explore_05_class_balance.py")
