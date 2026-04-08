"""
Generate visuals for the Loading a Dataset lecture.
    python portal/static/lecture_assets/_generate_loading_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sklearn.datasets import load_digits

OUT = Path(__file__).resolve().parent
digits = load_digits()

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"

sample_0 = digits.images[0]            # the very first sample (a 0)


# ── 1. Real digit + its underlying numbers ─────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6))

ax = axes[0]
ax.imshow(np.ones_like(sample_0), cmap="gray_r", vmin=0, vmax=20)
for i in range(8):
    for j in range(8):
        v = int(sample_0[i, j])
        ax.text(j, i, v, ha="center", va="center",
                fontsize=9, color=ACCENT, family="monospace")
ax.set_title("the 8x8 numpy array (digits.images[0])",
             fontsize=10, family="monospace")
ax.set_xticks([])
ax.set_yticks([])

ax = axes[1]
ax.imshow(sample_0, cmap="gray_r")
ax.set_title('rendered as a digit ("0")', fontsize=10, family="monospace")
ax.axis("off")

fig.text(0.5, 0.5, "->", ha="center", va="center",
         fontsize=22, color=ACCENT, fontweight="bold", family="monospace")
plt.tight_layout()
plt.savefig(OUT / "loading_digit_sample.png", **SAVE)
plt.close(fig)


# ── 2. Bunch object structure ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

# Root node
root = FancyBboxPatch((3.5, 4.5), 3.0, 0.9,
                      boxstyle="round,pad=0.05,rounding_size=0.1",
                      facecolor=ACCENT, edgecolor="#055e76", linewidth=1.5)
ax.add_patch(root)
ax.text(5.0, 4.95, "load_digits()", ha="center", va="center",
        fontsize=12, color="white", family="monospace", fontweight="bold")

# Children: 4 fields of the Bunch
fields = [
    (".data",          "ndarray (1797, 64)", "feed to the model"),
    (".target",        "ndarray (1797,)",    "the answers (0-9)"),
    (".images",        "ndarray (1797, 8, 8)", "for plotting"),
    (".DESCR",         "str",                "human description"),
]
x_positions = [0.4, 2.6, 5.0, 7.4]
for x, (name, shape, role) in zip(x_positions, fields):
    box = FancyBboxPatch((x, 1.2), 2.2, 1.7,
                         boxstyle="round,pad=0.05,rounding_size=0.1",
                         facecolor="white", edgecolor=ACCENT, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + 1.1, 2.55, name, ha="center", va="center",
            fontsize=11, color=ACCENT, family="monospace", fontweight="bold")
    ax.text(x + 1.1, 2.05, shape, ha="center", va="center",
            fontsize=8, color="#555", family="monospace")
    ax.text(x + 1.1, 1.55, role, ha="center", va="center",
            fontsize=8, color="#777", family="monospace", style="italic")
    # Arrow from root to child
    arrow = FancyArrowPatch((5.0, 4.5), (x + 1.1, 2.9),
                            arrowstyle="->", mutation_scale=12,
                            color=ACCENT, linewidth=1.2)
    ax.add_patch(arrow)

ax.text(5.0, 0.4,
        "A Bunch is a dictionary you can also access with dot notation.",
        ha="center", va="center", fontsize=9, color="#555",
        family="monospace", style="italic")
plt.tight_layout()
plt.savefig(OUT / "loading_bunch_structure.png", **SAVE)
plt.close(fig)


# ── 3. DataFrame preview as a styled table ─────────────────────────────────
df = pd.DataFrame(digits.data[:6], columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target[:6]
preview_cols = ["pixel_0", "pixel_1", "pixel_21", "pixel_32", "pixel_43", "pixel_63", "target"]
preview = df[preview_cols].astype(int)

fig, ax = plt.subplots(figsize=(7.5, 2.6))
ax.axis("off")
table = ax.table(
    cellText=preview.values,
    colLabels=preview_cols,
    cellLoc="center",
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.0, 1.4)

# Style header row
for i, key in enumerate(preview_cols):
    cell = table[(0, i)]
    cell.set_facecolor(ACCENT)
    cell.set_text_props(color="white", family="monospace", weight="bold")
# Style target column
for r in range(1, len(preview) + 1):
    cell = table[(r, len(preview_cols) - 1)]
    cell.set_facecolor("#fef3c7")  # subtle yellow

ax.set_title("df.head(6)  -  64 pixel columns + 1 target column  -  shape (1797, 65)",
             fontsize=10, family="monospace", pad=12)
plt.tight_layout()
plt.savefig(OUT / "loading_dataframe_preview.png", **SAVE)
plt.close(fig)


# ── 4. Boolean mask filter ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(8, 3.4))

# Build a tiny example: 8 rows showing target values
example_targets = np.array([5, 3, 7, 3, 1, 8, 3, 0])
mask = example_targets == 3

# Panel 1: target column
ax = axes[0]
ax.axis("off")
ax.set_title('df["target"]', fontsize=10, family="monospace", color=ACCENT)
for i, t in enumerate(example_targets):
    ax.add_patch(plt.Rectangle((0.2, 7 - i), 1.0, 0.85,
                               facecolor="white", edgecolor="#888", linewidth=1))
    ax.text(0.7, 7.4 - i, str(t), ha="center", va="center",
            fontsize=12, family="monospace")
ax.set_xlim(0, 1.5)
ax.set_ylim(-0.2, 8.2)

# Panel 2: == 3 boolean mask
ax = axes[1]
ax.axis("off")
ax.set_title('== 3', fontsize=10, family="monospace", color=ACCENT)
for i, m in enumerate(mask):
    color = "#86efac" if m else "#fecaca"
    label = "True" if m else "False"
    ax.add_patch(plt.Rectangle((0.2, 7 - i), 1.4, 0.85,
                               facecolor=color, edgecolor="#888", linewidth=1))
    ax.text(0.9, 7.4 - i, label, ha="center", va="center",
            fontsize=10, family="monospace")
ax.set_xlim(0, 1.8)
ax.set_ylim(-0.2, 8.2)

# Panel 3: filtered result
ax = axes[2]
ax.axis("off")
ax.set_title('df[mask]', fontsize=10, family="monospace", color=ACCENT)
kept = 0
for i, (t, m) in enumerate(zip(example_targets, mask)):
    if m:
        ax.add_patch(plt.Rectangle((0.2, 7 - kept), 1.0, 0.85,
                                   facecolor="#86efac", edgecolor="#16a34a", linewidth=1))
        ax.text(0.7, 7.4 - kept, str(t), ha="center", va="center",
                fontsize=12, family="monospace", fontweight="bold")
        kept += 1
ax.text(0.7, 7 - kept - 0.5, f"{kept} rows kept",
        ha="center", fontsize=9, family="monospace", color="#16a34a")
ax.set_xlim(0, 1.5)
ax.set_ylim(-0.2, 8.2)

fig.suptitle("Boolean mask filtering: keep only the rows where target == 3",
             fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "loading_mask_filter.png", **SAVE)
plt.close(fig)


print("Wrote 4 loading-data images")
