"""
Generate visuals for the Shape, Statistics, and Missing Values lecture.
    python portal/static/lecture_assets/_generate_statistics.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

OUT = Path(__file__).resolve().parent
digits = load_digits()

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
RED = "#dc2626"
ORANGE = "#f59e0b"
GREEN = "#16a34a"


# ── 1. .describe() output as a real styled table ───────────────────────────
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
desc = df[["pixel_0", "pixel_28", "pixel_36", "pixel_63", "target"]].describe().round(2)

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.axis("off")
table = ax.table(
    cellText=desc.values,
    colLabels=desc.columns,
    rowLabels=desc.index,
    cellLoc="center",
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.0, 1.4)

# Header row styling
for i, col in enumerate(desc.columns):
    cell = table[(0, i)]
    cell.set_facecolor(ACCENT)
    cell.set_text_props(color="white", family="monospace", weight="bold")

# Highlight std row (row 2 in describe -> table row 3 since header row is 0)
std_row_idx = list(desc.index).index("std") + 1
for j in range(len(desc.columns)):
    cell = table[(std_row_idx, j)]
    cell.set_facecolor("#fef3c7")

# Highlight pixel_0 column (col 0) — entirely zero, useless
for r in range(1, len(desc.index) + 1):
    cell = table[(r, 0)]
    cell.set_text_props(color=RED, weight="bold")

# Row labels styling
for r in range(1, len(desc.index) + 1):
    cell = table[(r, -1)]
    cell.set_facecolor("#f3f4f6")
    cell.set_text_props(family="monospace", weight="bold")

ax.set_title('df[[...]].describe().round(2)  -  std=0 row highlighted, pixel_0 in red',
             fontsize=10, family="monospace", pad=12)
plt.tight_layout()
plt.savefig(OUT / "statistics_describe.png", **SAVE)
plt.close(fig)


# ── 2. Standard deviation per pixel — a bar chart of all 64 ────────────────
stds = df.drop(columns=["target"]).std().values
fig, ax = plt.subplots(figsize=(9, 3.6))
colors = [RED if s < 0.5 else (ORANGE if s < 3 else ACCENT) for s in stds]
ax.bar(range(64), stds, color=colors, edgecolor="#222", linewidth=0.4)
ax.set_xlabel("Pixel index (0-63)", family="monospace")
ax.set_ylabel("Standard deviation", family="monospace")
ax.set_title("Per-pixel standard deviation across all 1,797 digits",
             fontsize=11, family="monospace")
ax.grid(axis="y", alpha=0.3)
ax.set_xticks([0, 8, 16, 24, 32, 40, 48, 56, 63])

# Legend
from matplotlib.patches import Patch
legend_elems = [
    Patch(facecolor=RED, label="std < 0.5  -  useless"),
    Patch(facecolor=ORANGE, label="std 0.5-3  -  weak signal"),
    Patch(facecolor=ACCENT, label="std > 3  -  informative"),
]
ax.legend(handles=legend_elems, loc="upper right", fontsize=8, framealpha=0.9)
plt.tight_layout()
plt.savefig(OUT / "statistics_pixel_std.png", **SAVE)
plt.close(fig)


# ── 3. Useless pixels overlaid on the digit grid ───────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6))

# Mean image of all digits — to show what positions have ink
mean_img = digits.images.mean(axis=0)

# Left: the mean image
ax = axes[0]
ax.imshow(mean_img, cmap="gray_r")
ax.set_title("Average of all 1,797 digits",
             fontsize=10, family="monospace")
ax.axis("off")

# Right: same mean image, with corner pixels boxed in red (the std=0 ones)
ax = axes[1]
ax.imshow(mean_img, cmap="gray_r")
std_grid = stds.reshape(8, 8)
for i in range(8):
    for j in range(8):
        if std_grid[i, j] < 0.5:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       fill=False, edgecolor=RED, linewidth=2))
ax.set_title("Red = std < 0.5 (useless)",
             fontsize=10, family="monospace", color=RED)
ax.axis("off")

plt.tight_layout()
plt.savefig(OUT / "statistics_useless_pixels.png", **SAVE)
plt.close(fig)


# ── 4. Feature scale problem — three features on wildly different scales ──
fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))

features = [
    ("bytes_sent", [1_000_000_000, 1_000_000_500], 0, 2_000_000_000, ACCENT),
    ("unique_ports", [443, 80], 0, 65535, ORANGE),
    ("syn_flag_ratio", [0.8, 0.1], 0, 1.0, GREEN),
]

for ax, (name, vals, lo, hi, color) in zip(axes, features):
    ax.barh(["P1", "P2"], vals, color=color, edgecolor="#222", linewidth=1)
    ax.set_xlim(lo, hi * 1.05)
    ax.set_title(name, fontsize=10, family="monospace", color=color)
    for i, v in enumerate(vals):
        if v >= 1000:
            label = f"{v:,}"
        elif v >= 1:
            label = f"{int(v)}" if v == int(v) else f"{v:.2f}"
        else:
            label = f"{v:.2f}"
        # Place label outside to the right of the bar so it never clips
        ax.text(v + hi * 0.02, i, label, ha="left", va="center",
                fontsize=9, family="monospace", color="#222", weight="bold")
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xlabel(f"range 0 - {hi:,}", fontsize=7, family="monospace", color="#666")

fig.suptitle("Same two data points, three features — scales differ by 9 orders of magnitude",
             fontsize=10, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "statistics_scale_problem.png", **SAVE)
plt.close(fig)


print("Wrote 4 statistics images")
