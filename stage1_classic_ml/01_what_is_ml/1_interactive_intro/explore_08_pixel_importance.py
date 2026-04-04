# Explore 8 — Which Pixels Matter Most?
#
# Not all features are created equal. Some pixels strongly predict the digit.
# Drag the slider to set a correlation threshold and see which pixels survive.
#
#   python explore_08_pixel_importance.py

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from sklearn.datasets import load_digits

if plt.get_backend().lower() == "agg":
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_08_pixel_importance.py")
    sys.exit(1)

digits = load_digits()

# Compute absolute correlation of each pixel with the target label
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
correlations = df.corr()["target"].abs().drop("target").values  # shape (64,)
corr_grid = correlations.reshape(8, 8)

# Setup figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
plt.subplots_adjust(bottom=0.25, top=0.85)

# Left: correlation heatmap (fixed)
im1 = ax1.imshow(corr_grid, cmap="YlOrRd", interpolation="nearest", vmin=0, vmax=0.7)
ax1.set_title("Pixel–label correlation", fontsize=12)
ax1.axis("off")
fig.colorbar(im1, ax=ax1, shrink=0.8)

# Middle: important pixel mask (updates with slider)
threshold_init = 0.3
mask = (corr_grid >= threshold_init).astype(float)
im2 = ax2.imshow(mask, cmap="RdYlGn", interpolation="nearest", vmin=0, vmax=1)
ax2.set_title("Important pixels", fontsize=12)
ax2.axis("off")

# Right: overlay on a real digit (updates with button)
sample_idx = [0]
overlay_data = [None]

real_img = digits.images[sample_idx[0]]
im3 = ax3.imshow(real_img, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
ax3.set_title(f"Sample digit {digits.target[sample_idx[0]]}", fontsize=12)
ax3.axis("off")

# Status text
count = mask.sum()
txt = fig.text(
    0.5, 0.06,
    f"Keeping {int(count)} of 64 pixels (correlation >= {threshold_init:.2f})",
    ha="center", fontsize=12,
)

fig.suptitle(
    "Drag the slider to set the minimum correlation threshold",
    fontsize=14,
)

# Slider
ax_slider = plt.axes([0.20, 0.12, 0.55, 0.04])
slider = Slider(ax_slider, "Min corr", 0.0, 0.65, valinit=threshold_init, valstep=0.05)


def update_mask(val):
    threshold = slider.val
    mask = (corr_grid >= threshold).astype(float)
    im2.set_data(mask)
    count = mask.sum()
    txt.set_text(
        f"Keeping {int(count)} of 64 pixels (correlation >= {threshold:.2f})"
    )

    # Update overlay if active
    if overlay_data[0] is not None:
        masked_img = digits.images[sample_idx[0]].copy()
        masked_img[corr_grid < threshold] = -1
        im3.set_data(masked_img)
        im3.set_clim(vmin=-1, vmax=16)

    fig.canvas.draw_idle()


slider.on_changed(update_mask)

# Button: show on real digit
ax_btn = plt.axes([0.82, 0.12, 0.14, 0.04])
btn = Button(ax_btn, "Show on digit")


def on_overlay(event):
    # Pick a new random sample
    sample_idx[0] = np.random.randint(len(digits.images))
    threshold = slider.val

    masked_img = digits.images[sample_idx[0]].copy()
    masked_img[corr_grid < threshold] = -1  # mark unimportant as dark blue
    overlay_data[0] = True

    im3.set_data(masked_img)
    im3.set_clim(vmin=-1, vmax=16)
    ax3.set_title(f"Digit {digits.target[sample_idx[0]]} (masked)", fontsize=12)
    fig.canvas.draw_idle()


btn.on_clicked(on_overlay)

plt.show()

# After closing
top_pixels = np.argsort(correlations)[::-1][:10]
print("\nTop 10 most predictive pixels (by correlation with label):")
for rank, px in enumerate(top_pixels, 1):
    row, col = divmod(px, 8)
    print(f"  {rank}. pixel_{px} (row {row}, col {col}) — corr = {correlations[px]:.3f}")

print()
print("Pixels near the center carry the most signal.")
print("Corner pixels (always 0) carry none — just like explore_04 showed.")
print()
print("In security logs, this is feature selection:")
print("  - High-correlation features: dest_port, bytes_sent, entropy")
print("  - Low-correlation features: source MAC address, TTL")
print("  - Dropping useless features makes models faster and more accurate.")
print(f"\n  Next: python explore_09_model_eye_view.py")
