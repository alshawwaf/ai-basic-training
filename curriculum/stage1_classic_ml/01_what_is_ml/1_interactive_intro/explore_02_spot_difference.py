"""
Explore 02 — Spot the Difference
================================
The trick a classifier learns is *which pixels differ between classes*.
You can do the same thing with your eyes.

How to use:
- Pick two digits with the radio buttons.
- Click "New pair" to draw a fresh sample of each.
- The third panel shows the *absolute pixel difference*. Bright = the
  pixels that disagree most. Those are the pixels a model would weight.

CHALLENGES:
1. Which two digits look almost identical in the difference map? Those
   are the pairs a classifier confuses most.
2. Pick (1, 7). Click "New pair" 5 times. Does the difference map stay
   similar, or change a lot? What does that tell you about the digit 1?
3. Pick (4, 9). Where do they differ? Top, middle, or bottom?
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_02_spot_difference.py")
    sys.exit(1)

digits = load_digits()
state = {"left": 1, "right": 7}


def random_sample(label):
    pool = digits.images[digits.target == label]
    idx = np.random.randint(len(pool))
    return pool[idx]


fig = plt.figure(figsize=(11, 5))
fig.suptitle("Spot the Difference — what a classifier actually looks at",
             fontsize=12)

ax_left = fig.add_axes([0.28, 0.30, 0.18, 0.55])
ax_right = fig.add_axes([0.50, 0.30, 0.18, 0.55])
ax_diff = fig.add_axes([0.72, 0.30, 0.18, 0.55])

ax_radio_l = fig.add_axes([0.04, 0.30, 0.08, 0.55])
ax_radio_r = fig.add_axes([0.14, 0.30, 0.08, 0.55])
ax_btn = fig.add_axes([0.40, 0.10, 0.20, 0.08])

radio_l = RadioButtons(ax_radio_l, [str(i) for i in range(10)], active=1)
radio_r = RadioButtons(ax_radio_r, [str(i) for i in range(10)], active=7)
ax_radio_l.set_title("Left", fontsize=9)
ax_radio_r.set_title("Right", fontsize=9)
btn = Button(ax_btn, "New pair")


def redraw():
    a = random_sample(state["left"])
    b = random_sample(state["right"])
    diff = np.abs(a.astype(float) - b.astype(float))

    for ax in (ax_left, ax_right, ax_diff):
        ax.cla()
        ax.axis("off")

    ax_left.imshow(a, cmap="gray_r", vmin=0, vmax=16)
    ax_left.set_title(f"digit {state['left']}")

    ax_right.imshow(b, cmap="gray_r", vmin=0, vmax=16)
    ax_right.set_title(f"digit {state['right']}")

    ax_diff.imshow(diff, cmap="hot", vmin=0, vmax=16)
    total = float(diff.sum())
    ax_diff.set_title(f"|left - right|\ntotal = {total:.0f}")

    fig.canvas.draw_idle()


def on_left(label):
    state["left"] = int(label)
    redraw()


def on_right(label):
    state["right"] = int(label)
    redraw()


def on_button(_event):
    redraw()


radio_l.on_clicked(on_left)
radio_r.on_clicked(on_right)
btn.on_clicked(on_button)

redraw()
plt.show()

print()
print("That bright 'difference map' is essentially what a linear model")
print("learns to weight. Pixels that consistently differ between two")
print("classes get large coefficients; pixels that always look the same")
print("get coefficients near zero.")
print()
print("Next: explore_03_dataset_shape.ipynb")
