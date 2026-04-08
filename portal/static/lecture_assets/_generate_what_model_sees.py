"""
Generate visuals for the What the Model Actually Sees lecture.
    python portal/static/lecture_assets/_generate_what_model_sees.py
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


# ── 1. Human view -> model view -> flat vector ────────────────────────────
sample = digits.images[0]   # a 0
fig = plt.figure(figsize=(10, 5.2))
gs = fig.add_gridspec(2, 2, height_ratios=[2.4, 1], width_ratios=[1, 1.05],
                      hspace=0.5, wspace=0.25)

# Panel 1 (top-left): human view
ax = fig.add_subplot(gs[0, 0])
ax.imshow(sample, cmap="gray_r")
ax.set_title('1. Human sees\n(an image)', fontsize=10, family="monospace")
ax.axis("off")

# Panel 2 (top-right): model sees the 8x8 numbers
ax = fig.add_subplot(gs[0, 1])
ax.imshow(np.ones_like(sample), cmap="gray_r", vmin=0, vmax=20)
for i in range(8):
    for j in range(8):
        v = int(sample[i, j])
        ax.text(j, i, v, ha="center", va="center",
                fontsize=9, color=ACCENT, family="monospace")
ax.set_title('2. The 8x8 numpy array', fontsize=10, family="monospace")
ax.set_xticks([])
ax.set_yticks([])

# Panel 3 (bottom row, full width): flat 64-vector
ax = fig.add_subplot(gs[1, :])
flat = sample.flatten().astype(int)
ax.imshow(np.ones((1, 64)), cmap="gray_r", vmin=0, vmax=20, aspect="auto")
for k, v in enumerate(flat):
    ax.text(k, 0, str(v), ha="center", va="center",
            fontsize=8, color=ACCENT, family="monospace")
ax.set_xticks([0, 8, 16, 24, 32, 40, 48, 56, 63])
ax.set_yticks([])
ax.set_title('3. What the model actually receives — one flat row of 64 numbers',
             fontsize=10, family="monospace", color=RED)

plt.savefig(OUT / "model_sees_pipeline.png", **SAVE)
plt.close(fig)


# ── 2. Correlation heatmap on the 8x8 grid ────────────────────────────────
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target
corr_values = df.drop(columns=["target"]).corrwith(df["target"]).abs().values
corr_values = np.nan_to_num(corr_values, nan=0.0)  # zero-variance pixels -> 0
corr_grid = corr_values.reshape(8, 8)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.0))

# Left panel: heatmap of correlations
ax = axes[0]
im = ax.imshow(corr_grid, cmap="hot", vmin=0, vmax=corr_values.max())
ax.set_title("|correlation| with target",
             fontsize=10, family="monospace")
ax.set_xticks(range(8))
ax.set_yticks(range(8))
for i in range(8):
    for j in range(8):
        v = corr_grid[i, j]
        color = "white" if v < 0.2 else "#000"
        ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                fontsize=7, color=color, family="monospace")
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

# Right panel: top 3 most predictive pixels highlighted on a digit
ax = axes[1]
sample_3 = digits.images[digits.target == 3][0]
ax.imshow(sample_3, cmap="gray_r")
top_indices = np.argsort(corr_values)[::-1][:3]
for idx in top_indices:
    r, c = idx // 8, idx % 8
    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1,
                               fill=False, edgecolor=ACCENT, linewidth=2.5))
    ax.text(c, r - 0.85, f"#{idx}", ha="center", va="center",
            fontsize=8, color=ACCENT, family="monospace", weight="bold")
ax.set_title("top-3 predictive pixels on a real 3",
             fontsize=10, family="monospace", color=ACCENT)
ax.axis("off")

plt.tight_layout()
plt.savefig(OUT / "model_sees_correlation.png", **SAVE)
plt.close(fig)


# ── 3. Pixel-index → row,col mapping diagram ──────────────────────────────
fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(np.ones((8, 8)), cmap="gray_r", vmin=0, vmax=20)
for i in range(8):
    for j in range(8):
        idx = i * 8 + j
        ax.text(j, i, str(idx), ha="center", va="center",
                fontsize=10, color=ACCENT, family="monospace")
# Highlight pixel 43 (row 5, col 3)
r, c = 43 // 8, 43 % 8
ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1,
                           fill=False, edgecolor=RED, linewidth=2.5))
ax.set_xticks(range(8))
ax.set_yticks(range(8))
ax.set_xlabel("col = i % 8", family="monospace")
ax.set_ylabel("row = i // 8", family="monospace")
ax.set_title("Pixel index to row/col\n(pixel_43 = row 5, col 3)",
             fontsize=11, family="monospace", color=RED)
plt.tight_layout()
plt.savefig(OUT / "model_sees_index_grid.png", **SAVE)
plt.close(fig)


# ── 4. Security-equivalent comparison ─────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(9, 3.6))

# Top: digits flat vector
ax = axes[0]
ax.imshow(np.ones((1, 10)), cmap="gray_r", vmin=0, vmax=20, aspect="auto")
digit_vals = [0, 0, 5, 13, 9, 1, 0, 0, 0, 0]
for k, v in enumerate(digit_vals):
    ax.text(k, 0, str(v), ha="center", va="center",
            fontsize=12, color=ACCENT, family="monospace")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Digits: first 10 pixel values     ->     label = 0",
             fontsize=10, family="monospace", loc="left")

# Bottom: security flat vector
ax = axes[1]
ax.imshow(np.ones((1, 9)), cmap="gray_r", vmin=0, vmax=20, aspect="auto")
sec_vals = ["1048576", "443", "2.4", "14", "0", "3", "1", "0.87", "2048"]
sec_names = ["bytes", "port", "secs", "pkts", "rst", "syn", "fin", "entropy", "size"]
for k, (v, name) in enumerate(zip(sec_vals, sec_names)):
    ax.text(k, -0.05, v, ha="center", va="center",
            fontsize=10, color=ACCENT, family="monospace")
    ax.text(k, 0.45, name, ha="center", va="center",
            fontsize=8, color="#666", family="monospace", style="italic")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Security: 9 connection features     ->     label = malicious",
             fontsize=10, family="monospace", loc="left")

fig.suptitle("Same shape — flat row of numbers + label. Only the meaning changes.",
             fontsize=11, family="monospace", color=RED)
plt.tight_layout()
plt.savefig(OUT / "model_sees_security_parallel.png", **SAVE)
plt.close(fig)


print("Wrote 4 what-model-sees images")
