"""
Explore 07 — Average Digits & Prototypes
========================================
Average all the 1s together. Now average all the 7s. Those two pictures
are the *prototype* the simplest classifier compares against.

Pick any pair of digits with the radio buttons. The third panel shows
how similar their prototypes are (lower number = more confusable). Then
hit "Rank all pairs" to see which digit pair is the model's nightmare.

CHALLENGES:
1. Which digit pair has the smallest distance? Why?
2. Which pair has the largest? Are they visually unrelated?
3. Compare the (4, 9) pair to (3, 8). Which would *you* find harder?
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from sklearn.datasets import load_digits

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_07_average_digits.py")
    sys.exit(1)

digits = load_digits()
prototypes = np.stack([
    digits.images[digits.target == d].mean(axis=0)
    for d in range(10)
])  # (10, 8, 8)

state = {"a": 4, "b": 9}


def distance(i, j):
    """Euclidean distance between two prototypes (lower = more similar)."""
    return float(np.linalg.norm(prototypes[i] - prototypes[j]))


fig = plt.figure(figsize=(11, 5.5))
fig.suptitle("Average Digits — the simplest 'classifier' is just a distance",
             fontsize=12)

ax_a = fig.add_axes([0.30, 0.32, 0.18, 0.55])
ax_b = fig.add_axes([0.50, 0.32, 0.18, 0.55])
ax_diff = fig.add_axes([0.72, 0.32, 0.18, 0.55])

ax_radio_a = fig.add_axes([0.04, 0.32, 0.08, 0.55])
ax_radio_b = fig.add_axes([0.14, 0.32, 0.08, 0.55])
ax_btn = fig.add_axes([0.40, 0.10, 0.20, 0.08])

ax_radio_a.set_title("A", fontsize=10)
ax_radio_b.set_title("B", fontsize=10)
radio_a = RadioButtons(ax_radio_a, [str(i) for i in range(10)], active=4)
radio_b = RadioButtons(ax_radio_b, [str(i) for i in range(10)], active=9)
btn = Button(ax_btn, "Rank all pairs")


def redraw():
    a, b = state["a"], state["b"]
    for ax in (ax_a, ax_b, ax_diff):
        ax.cla()
        ax.axis("off")

    ax_a.imshow(prototypes[a], cmap="gray_r")
    ax_a.set_title(f"prototype {a}")

    ax_b.imshow(prototypes[b], cmap="gray_r")
    ax_b.set_title(f"prototype {b}")

    diff = np.abs(prototypes[a] - prototypes[b])
    ax_diff.imshow(diff, cmap="hot")
    d = distance(a, b)
    ax_diff.set_title(f"|A - B|\ndistance = {d:.2f}")

    fig.canvas.draw_idle()


def on_a(label):
    state["a"] = int(label)
    redraw()


def on_b(label):
    state["b"] = int(label)
    redraw()


def on_rank(_event):
    pairs = []
    for i in range(10):
        for j in range(i + 1, 10):
            pairs.append(((i, j), distance(i, j)))
    pairs.sort(key=lambda x: x[1])
    print()
    print("Most-confusable digit pairs (smallest distance first):")
    for rank, ((i, j), d) in enumerate(pairs, 1):
        marker = "  <- hardest" if rank == 1 else ""
        marker_end = "  <- easiest" if rank == len(pairs) else ""
        print(f"  {rank:2d}. ({i}, {j})  distance = {d:6.2f}{marker}{marker_end}")
    print()


radio_a.on_clicked(on_a)
radio_b.on_clicked(on_b)
btn.on_clicked(on_rank)

redraw()
plt.show()

print()
print("Takeaway: a 'nearest prototype' classifier already works pretty")
print("well — it gets ~80% accuracy on this dataset with zero training.")
print("Real classifiers are smarter, but they're solving the same shape")
print("of problem: which class prototype is your sample closest to?")
print()
print("Next: explore_08_pixel_importance.py")
