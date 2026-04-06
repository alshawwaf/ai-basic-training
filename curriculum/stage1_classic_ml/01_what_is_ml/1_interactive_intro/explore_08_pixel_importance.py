"""
Explore 08 — Which Pixels Carry the Signal?
===========================================
Forget images. Treat each of the 64 pixels as a feature column. Some
columns are strongly correlated with the digit label; others are noise.

Drag the slider to set a *correlation threshold*. Pixels at or above
the threshold light up green and overlay the average digit. Hit "Show
top-10" to print the most predictive pixel positions.

This is exactly the kind of feature ranking you'd run on a real dataset
before training — keep the columns that matter, drop the rest.

CHALLENGES:
1. The most predictive pixels cluster in two regions of the image.
   Where? What does that say about how digits 0-9 differ?
2. Push the slider above 0.4. How many pixels survive? Could a model
   actually classify with that few features?
3. Compare the highlight pattern to the variance map from
   explore_04_useless_pixels.py. High-variance != high-correlation.
   Why?
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_08_pixel_importance.py")
    sys.exit(1)

digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target

# correlation of each pixel with the (numeric) label
correlations = df.corr()["target"].drop("target").abs().values  # (64,)
corr_grid = correlations.reshape(8, 8)
mean_image = digits.images.mean(axis=0)

print("Top-5 most label-correlated pixels:")
order = correlations.argsort()[::-1]
for rank, idx in enumerate(order[:5], 1):
    r, c = divmod(int(idx), 8)
    print(f"  {rank}. pixel_{int(idx):02d}  (row {r}, col {c})  "
          f"|corr| = {correlations[int(idx)]:.3f}")

fig = plt.figure(figsize=(11, 5.5))
fig.suptitle("Pixel Importance — drag the slider to highlight signal pixels",
             fontsize=12)

ax_avg = fig.add_axes([0.05, 0.30, 0.27, 0.55])
ax_corr = fig.add_axes([0.36, 0.30, 0.27, 0.55])
ax_overlay = fig.add_axes([0.67, 0.30, 0.27, 0.55])
ax_slider = fig.add_axes([0.20, 0.13, 0.50, 0.04])
ax_btn = fig.add_axes([0.78, 0.11, 0.18, 0.07])

ax_avg.imshow(mean_image, cmap="gray_r")
ax_avg.set_title("average digit")
ax_avg.axis("off")

im_corr = ax_corr.imshow(corr_grid, cmap="viridis")
ax_corr.set_title("|correlation with label|")
ax_corr.axis("off")
fig.colorbar(im_corr, ax=ax_corr, fraction=0.046, pad=0.04)

slider = Slider(ax_slider, "correlation threshold",
                0.0, float(corr_grid.max()),
                valinit=0.15, valstep=0.01)
btn = Button(ax_btn, "Show top-10")


def redraw(threshold):
    keep = (corr_grid >= threshold).astype(float)
    n_keep = int(keep.sum())

    ax_overlay.cla()
    ax_overlay.imshow(mean_image, cmap="gray_r", alpha=0.4)
    # green overlay where pixel is "important"
    overlay = np.zeros((8, 8, 4))
    overlay[..., 1] = 0.85  # green
    overlay[..., 3] = keep * 0.75  # alpha mask
    ax_overlay.imshow(overlay)
    ax_overlay.set_title(f"signal pixels = {n_keep} / 64")
    ax_overlay.axis("off")
    fig.canvas.draw_idle()


def on_slider(val):
    redraw(val)


def on_btn(_event):
    print()
    print("Top-10 most label-correlated pixels:")
    for rank, idx in enumerate(order[:10], 1):
        r, c = divmod(int(idx), 8)
        print(f"  {rank:2d}. pixel_{int(idx):02d}  (row {r}, col {c})  "
              f"|corr| = {correlations[int(idx)]:.3f}")
    print()


slider.on_changed(on_slider)
btn.on_clicked(on_btn)
redraw(0.15)
plt.show()

print()
print("Takeaway: feature importance is the same idea whether you're")
print("looking at pixel positions, network packet fields, or sensor")
print("readings. Some columns carry signal, most don't. A good first")
print("step on any dataset is to ask 'which features actually matter?'")
print()
print("Next: explore_09_model_eye_view.py")
