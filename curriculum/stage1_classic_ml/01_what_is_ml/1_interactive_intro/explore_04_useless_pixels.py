"""
Explore 04 — Useless Pixels
===========================
Some pixels never change. They're always 0, or always near the same
value, no matter which digit was drawn. A model that uses them is just
wasting capacity.

Drag the slider to set a *variance threshold*. Pixels with variance
**below** that threshold get marked as "useless" — the model could
literally drop them with no loss in accuracy.

CHALLENGES:
1. At threshold 0, how many pixels are "useless"? (Watch the counter.)
   What does that say about the corners of the image?
2. Push the slider to 8. How many pixels survive? Could you still
   recognise digits with that few?
3. The dropped pixels concentrate in one region. Where? Why?
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_04_useless_pixels.py")
    sys.exit(1)

digits = load_digits()
X = digits.data  # (1797, 64)

# variance for each of the 64 pixel positions
pixel_variance = X.var(axis=0).reshape(8, 8)
mean_image = digits.images.mean(axis=0)

print("Pixel variance map (row, col):")
print(np.round(pixel_variance, 1))
print()
print(f"min variance: {pixel_variance.min():.2f}")
print(f"max variance: {pixel_variance.max():.2f}")

fig = plt.figure(figsize=(11, 5))
fig.suptitle("Useless Pixels — drag the slider to drop low-variance pixels",
             fontsize=12)

ax_avg = fig.add_axes([0.05, 0.30, 0.27, 0.55])
ax_var = fig.add_axes([0.36, 0.30, 0.27, 0.55])
ax_keep = fig.add_axes([0.67, 0.30, 0.27, 0.55])
ax_slider = fig.add_axes([0.20, 0.12, 0.60, 0.04])

ax_avg.imshow(mean_image, cmap="gray_r")
ax_avg.set_title("Average digit\n(reference)")
ax_avg.axis("off")

im_var = ax_var.imshow(pixel_variance, cmap="viridis")
ax_var.set_title("Pixel variance\n(brighter = more useful)")
ax_var.axis("off")
fig.colorbar(im_var, ax=ax_var, fraction=0.046, pad=0.04)

threshold_slider = Slider(ax_slider, "variance threshold",
                          0.0, float(pixel_variance.max()),
                          valinit=0.0, valstep=0.5)


def redraw(threshold):
    keep_mask = (pixel_variance >= threshold).astype(float)
    n_keep = int(keep_mask.sum())
    n_drop = 64 - n_keep

    ax_keep.cla()
    ax_keep.imshow(mean_image * keep_mask, cmap="gray_r",
                   vmin=0, vmax=mean_image.max())
    ax_keep.set_title(f"Pixels the model keeps\nkeep={n_keep}  drop={n_drop}")
    ax_keep.axis("off")
    fig.canvas.draw_idle()


def on_change(val):
    redraw(val)


threshold_slider.on_changed(on_change)
redraw(0.0)
plt.show()

print()
print("Takeaway: not every feature carries information. In real datasets")
print("(network logs, telemetry, EHR records) you'll often have hundreds")
print("of features and many will be near-constant. Dropping them speeds")
print("training and reduces overfitting.")
print()
print("Next: explore_05_class_balance.py")
