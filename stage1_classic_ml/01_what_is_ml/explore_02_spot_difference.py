# Explore 2 — Spot the Difference
#
# Two digits appear side by side. Where do they differ?
# The heatmap on the right shows the answer.
#
# Use the buttons to compare different digit pairs.
# Which pairs are hardest to tell apart?
#
#   python explore_02_spot_difference.py

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_02_spot_difference.py")
    sys.exit(1)

digits = load_digits()

# Pre-compute average images for each digit
averages = {}
for d in range(10):
    averages[d] = digits.images[digits.target == d].mean(axis=0)

# Setup figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
plt.subplots_adjust(left=0.25, bottom=0.15)

# Initial pair
pair = [3, 8]


def draw(pair):
    a, b = pair
    img_a = averages[a]
    img_b = averages[b]
    diff = np.abs(img_a - img_b)
    similarity = 1 - diff.mean() / 16

    ax1.cla()
    ax2.cla()
    ax3.cla()

    ax1.imshow(img_a, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
    ax1.set_title(f"Digit {a}", fontsize=13)
    ax1.axis("off")

    ax2.imshow(img_b, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
    ax2.set_title(f"Digit {b}", fontsize=13)
    ax2.axis("off")

    ax3.imshow(diff, cmap="hot", interpolation="nearest", vmin=0, vmax=16)
    ax3.set_title("Difference", fontsize=13)
    ax3.axis("off")

    fig.suptitle(
        f"Comparing {a} vs {b}  —  Similarity: {similarity:.0%}",
        fontsize=14,
    )
    fig.canvas.draw_idle()


# Radio buttons for pair selection
pairs = ["1 vs 7", "3 vs 8", "4 vs 9", "0 vs 6", "5 vs 9", "2 vs 3"]
ax_radio = plt.axes([0.02, 0.25, 0.15, 0.55])
radio = RadioButtons(ax_radio, pairs, active=1)


def on_radio(label):
    a, b = label.split(" vs ")
    pair[0], pair[1] = int(a), int(b)
    draw(pair)


radio.on_clicked(on_radio)

# Random pair button
ax_btn = plt.axes([0.02, 0.1, 0.15, 0.08])
btn = Button(ax_btn, "Random pair")


def on_random(event):
    a = np.random.randint(10)
    b = np.random.randint(10)
    while b == a:
        b = np.random.randint(10)
    pair[0], pair[1] = a, b
    draw(pair)


btn.on_clicked(on_random)

# Initial draw
draw(pair)
plt.show()

print("\nWhich pair was most similar? That's the pair a model will confuse most.")
print("\n  Next: open explore_03_dataset_shape.ipynb in Jupyter")
print("  (or run: jupyter notebook explore_03_dataset_shape.ipynb)")
