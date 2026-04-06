"""
Explore 05 — Class Balance
==========================
Pick a class. Drag the slider to throw away most of its samples. Watch
the bar chart tilt — and watch the imbalance ratio explode.

This is what real-world security data looks like out of the box. There
are millions of normal events and a handful of attacks. The class you
care about is the rare one.

CHALLENGES:
1. Drop class 0 to 10 samples. What's the new imbalance ratio?
2. Try dropping different classes — does the *worst* class matter, or
   only the *rarest*?
3. At what point does the chart stop being a chart and start being a
   single dominant bar? That's the moment a "naive" model wins big.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_05_class_balance.py")
    sys.exit(1)

digits = load_digits()
y = digits.target
original_counts = np.bincount(y, minlength=10)
state = {"target_class": 0, "keep": int(original_counts[0])}

fig = plt.figure(figsize=(11, 5.5))
fig.suptitle("Class Balance — drop samples and watch the imbalance grow",
             fontsize=12)

ax_bar = fig.add_axes([0.30, 0.30, 0.65, 0.55])
ax_radio = fig.add_axes([0.04, 0.30, 0.18, 0.55])
ax_slider = fig.add_axes([0.30, 0.13, 0.65, 0.04])

ax_radio.set_title("Class to shrink", fontsize=10)
radio = RadioButtons(ax_radio, [str(i) for i in range(10)], active=0)

slider = Slider(ax_slider, "samples to keep",
                1, int(original_counts.max()),
                valinit=int(original_counts[0]),
                valstep=1)


def redraw():
    counts = original_counts.copy()
    counts[state["target_class"]] = state["keep"]

    colours = ["#d1d5db"] * 10
    colours[state["target_class"]] = "#06d6e0"

    ax_bar.cla()
    bars = ax_bar.bar(range(10), counts, color=colours, edgecolor="#1a2332")
    for digit, count in enumerate(counts):
        ax_bar.text(digit, count + 4, str(count),
                    ha="center", va="bottom", fontsize=9)

    ratio = counts.max() / max(counts.min(), 1)
    naive_acc = counts.max() / counts.sum() * 100

    ax_bar.set_xticks(range(10))
    ax_bar.set_xlabel("digit class")
    ax_bar.set_ylabel("samples")
    ax_bar.set_ylim(0, original_counts.max() * 1.15)
    ax_bar.set_title(
        f"imbalance ratio = {ratio:.1f} : 1     "
        f"naive 'always-majority' accuracy = {naive_acc:.1f}%",
        fontsize=11
    )
    fig.canvas.draw_idle()


def on_radio(label):
    state["target_class"] = int(label)
    state["keep"] = int(original_counts[state["target_class"]])
    slider.set_val(state["keep"])
    redraw()


def on_slider(val):
    state["keep"] = int(val)
    redraw()


radio.on_clicked(on_radio)
slider.on_changed(on_slider)

redraw()
plt.show()

print()
print("Takeaway: when one class dominates, *accuracy* stops being a useful")
print("metric. A model that ignores the rare class entirely can score in")
print("the high 90s and still miss every single example you cared about.")
print()
print("That's the trap explore_06_accuracy_trap.py makes you feel.")
