"""
Generate visuals for the Class Balance & Accuracy Trap lecture.
    python portal/static/lecture_assets/_generate_class_balance.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

OUT = Path(__file__).resolve().parent
digits = load_digits()

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
RED = "#dc2626"


# ── 1. Balanced digits class distribution ──────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 3.6))
counts = [(digits.target == d).sum() for d in range(10)]
bars = ax.bar(range(10), counts, color=ACCENT, edgecolor="#055e76", linewidth=1)
for i, c in enumerate(counts):
    ax.text(i, c + 3, str(c), ha="center", fontsize=9, family="monospace")
ax.set_xticks(range(10))
ax.set_xlabel("Digit class", family="monospace")
ax.set_ylabel("Number of samples", family="monospace")
ax.set_title("Digits dataset — balanced (~178 per class, ratio 1.0:1)",
             fontsize=11, family="monospace")
ax.set_ylim(0, max(counts) * 1.15)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "class_balance_digits.png", **SAVE)
plt.close(fig)


# ── 2. Imbalanced security dataset (95 / 5) ────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3.6))
labels = ["Normal", "Attack"]
values = [9500, 500]
colors = [ACCENT, RED]
bars = ax.bar(labels, values, color=colors, edgecolor="#222", linewidth=1)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 150, f"{v:,}",
            ha="center", fontsize=12, family="monospace")
ax.set_ylabel("Number of samples", family="monospace")
ax.set_title("Real security dataset — 19:1 imbalance (95% / 5%)",
             fontsize=11, family="monospace")
ax.set_ylim(0, max(values) * 1.2)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "class_balance_security.png", **SAVE)
plt.close(fig)


# ── 3. The accuracy trap — confusion matrix of "always Normal" model ──────
fig, ax = plt.subplots(figsize=(5.2, 4.8))
cm = np.array([[9500, 0], [500, 0]])  # rows = actual, cols = predicted
im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=10000)
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["predicted: normal", "predicted: attack"],
                   family="monospace", fontsize=10)
ax.set_yticklabels(["actual: normal", "actual: attack"],
                   family="monospace", fontsize=10)
labels = [["TN\n9,500", "FP\n0"], ["FN\n500", "TP\n0"]]
for i in range(2):
    for j in range(2):
        v = cm[i, j]
        color = "white" if v > 5000 else "#222"
        ax.text(j, i, labels[i][j], ha="center", va="center",
                fontsize=14, color=color, family="monospace", fontweight="bold")
ax.set_title('"Always predict Normal"\naccuracy = 95%   ·   recall = 0%',
             fontsize=11, family="monospace", color=RED)
plt.tight_layout()
plt.savefig(OUT / "class_balance_trap.png", **SAVE)
plt.close(fig)


print("Wrote 3 class-balance images")
