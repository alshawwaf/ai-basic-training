# Explore 5 — Is This Dataset Fair?
#
# Are all digits equally represented? What happens when they're not?
# Use the slider to remove samples from one class and watch the imbalance grow.
#
#   python explore_05_class_balance.py

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from sklearn.datasets import load_digits

if plt.get_backend().lower() == "agg":
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_05_class_balance.py")
    sys.exit(1)

digits = load_digits()

# Original class counts
original_counts = np.array([(digits.target == d).sum() for d in range(10)])

# Setup figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.28, bottom=0.25)

# State
selected_class = [5]
remove_pct = [0]


def draw():
    ax.cla()
    counts = original_counts.copy()
    keep = max(1, int(counts[selected_class[0]] * (1 - remove_pct[0] / 100)))
    counts[selected_class[0]] = keep

    colors = ["#16537e"] * 10
    colors[selected_class[0]] = "#e94560"

    bars = ax.barh(range(10), counts, color=colors)
    ax.set_yticks(range(10))
    ax.set_yticklabels([f"Digit {d}" for d in range(10)])
    ax.set_xlabel("Number of samples", fontsize=12)
    ax.set_xlim(0, max(original_counts) + 10)

    # Add count labels
    for i, (bar, c) in enumerate(zip(bars, counts)):
        ax.text(c + 2, i, str(c), va="center", fontsize=10)

    # Compute stats
    majority = counts.max()
    minority = counts.min()
    ratio = majority / minority
    naive_acc = majority / counts.sum()

    title = f"Imbalance ratio: {ratio:.1f}:1"
    if ratio > 5:
        title += f"  |  A lazy model gets {naive_acc:.0%} accuracy by always guessing the majority"
        ax.set_title(title, fontsize=12, color="#e94560", fontweight="bold")
    else:
        ax.set_title(title, fontsize=12)

    fig.canvas.draw_idle()


# Radio buttons — which class to shrink
ax_radio = plt.axes([0.02, 0.30, 0.15, 0.55])
labels = [f"Digit {d}" for d in range(10)]
radio = RadioButtons(ax_radio, labels, active=5)


def on_radio(label):
    selected_class[0] = int(label.split()[1])
    draw()


radio.on_clicked(on_radio)

# Slider — how much to remove
ax_slider = plt.axes([0.28, 0.1, 0.55, 0.04])
slider = Slider(ax_slider, "Remove %", 0, 95, valinit=0, valstep=5)


def on_slider(val):
    remove_pct[0] = val
    draw()


slider.on_changed(on_slider)

fig.suptitle("Select a digit class and drag the slider to remove samples", fontsize=14)
draw()
plt.show()

print("\nWhat did you notice?")
print("  - At 0% removed, all classes are roughly equal (~178 samples each)")
print("  - At 90%+ removed, the ratio exceeds 10:1")
print("  - A model could 'cheat' by always predicting the majority class")
print("  - This is called the ACCURACY TRAP — next step shows it in action")
print(f"\n  Next: python explore_06_accuracy_trap.py")
