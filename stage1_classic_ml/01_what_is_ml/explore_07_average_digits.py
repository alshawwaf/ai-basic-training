# Explore 7 — What Does a "Typical" Digit Look Like?
#
# Average all images in a class and you get a prototype.
# Compare prototypes to see which digits a model will confuse.
#
#   python explore_07_average_digits.py

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_07_average_digits.py")
    sys.exit(1)

digits = load_digits()

# Pre-compute average images for each digit
averages = {}
for d in range(10):
    averages[d] = digits.images[digits.target == d].mean(axis=0)

# Pre-compute all pairwise similarities
all_pairs = []
for i in range(10):
    for j in range(i + 1, 10):
        diff = np.abs(averages[i] - averages[j]).mean() / 16
        similarity = 1 - diff
        all_pairs.append((i, j, similarity))
all_pairs.sort(key=lambda x: x[2], reverse=True)

# Setup figure
fig = plt.figure(figsize=(13, 7))
plt.subplots_adjust(left=0.22, bottom=0.15, top=0.88, right=0.95)

ax1 = fig.add_axes([0.22, 0.30, 0.20, 0.50])
ax2 = fig.add_axes([0.46, 0.30, 0.20, 0.50])
ax3 = fig.add_axes([0.70, 0.30, 0.20, 0.50])

# State
pair = [3, 8]


def draw():
    a, b = pair
    img_a = averages[a]
    img_b = averages[b]
    diff = np.abs(img_a - img_b)
    similarity = 1 - diff.mean() / 16

    for ax in (ax1, ax2, ax3):
        ax.cla()

    ax1.imshow(img_a, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
    ax1.set_title(f"Average {a}", fontsize=13)
    ax1.axis("off")

    ax2.imshow(img_b, cmap="gray_r", interpolation="nearest", vmin=0, vmax=16)
    ax2.set_title(f"Average {b}", fontsize=13)
    ax2.axis("off")

    ax3.imshow(diff, cmap="hot", interpolation="nearest", vmin=0, vmax=16)
    ax3.set_title("Difference", fontsize=13)
    ax3.axis("off")

    color = "#e94560" if similarity > 0.85 else "#16537e"
    fig.suptitle(
        f"Comparing prototypes: {a} vs {b}  —  Similarity: {similarity:.0%}",
        fontsize=14, color=color, fontweight="bold",
    )
    fig.canvas.draw_idle()


# Radio buttons — which pair to compare
preset_pairs = ["3 vs 8", "1 vs 7", "4 vs 9", "5 vs 9", "0 vs 6", "2 vs 3"]
ax_radio = plt.axes([0.02, 0.35, 0.15, 0.50])
radio = RadioButtons(ax_radio, preset_pairs, active=0)


def on_radio(label):
    a, b = label.split(" vs ")
    pair[0], pair[1] = int(a), int(b)
    draw()


radio.on_clicked(on_radio)

# Rank all pairs button
ax_btn = plt.axes([0.02, 0.15, 0.15, 0.08])
btn_rank = Button(ax_btn, "Rank all pairs")

# Text area for ranking
rank_text = [None]


def on_rank(event):
    # Clear previous ranking text if any
    if rank_text[0] is not None:
        rank_text[0].remove()
        rank_text[0] = None

    lines = ["Most similar pairs:"]
    for i, (a, b, sim) in enumerate(all_pairs[:5]):
        marker = " <-- hardest!" if i == 0 else ""
        lines.append(f"  {a} vs {b}: {sim:.0%}{marker}")
    lines.append("")
    lines.append("Most different pairs:")
    for a, b, sim in all_pairs[-3:]:
        lines.append(f"  {a} vs {b}: {sim:.0%}")

    rank_text[0] = fig.text(
        0.02, 0.02, "\n".join(lines), fontsize=9,
        fontfamily="monospace", va="bottom",
    )
    fig.canvas.draw_idle()


btn_rank.on_clicked(on_rank)

fig.text(
    0.55, 0.92,
    "Pick a pair or click 'Rank all pairs' to find the hardest ones",
    ha="center", fontsize=11, style="italic",
)

draw()
plt.show()

# After closing
print("\nWhat you discovered:")
print(f"  - Most similar pair: {all_pairs[0][0]} vs {all_pairs[0][1]} "
      f"({all_pairs[0][2]:.0%} similar)")
print(f"  - Most different pair: {all_pairs[-1][0]} vs {all_pairs[-1][1]} "
      f"({all_pairs[-1][2]:.0%} similar)")
print()
print("Prototypes are the 'ideal' shape a model learns for each class.")
print("When two prototypes look alike, the model struggles to tell them apart.")
print("In security: 'normal HTTPS traffic' and 'C2 beaconing' can look very similar.")
print(f"\n  Next: python explore_08_pixel_importance.py")
