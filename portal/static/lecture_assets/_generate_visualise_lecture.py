"""
Generate matplotlib PNGs for the "Visualising Your Data" lecture
(curriculum/stage1_classic_ml/01_what_is_ml/2_coding_exercises/4_visualise/lecture.md).

Re-run this any time you want to regenerate the visuals:
    python portal/static/lecture_assets/_generate_visualise_lecture.py

Outputs land alongside this script in portal/static/lecture_assets/.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

OUT = Path(__file__).resolve().parent
digits = load_digits()

# Pick one obvious sample per digit class
sample_3 = digits.images[digits.target == 3][0]
sample_5 = digits.images[digits.target == 5][0]
sample_8 = digits.images[digits.target == 8][0]

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"  # brand cyan (light-theme accent)


# ── 0. ax-vs-axes bridge example output ────────────────────────────────────
# Exactly the script that appears in the lecture's "ax vs axes" bridge box,
# so the reader sees the literal output of the code they just read.
fig, axes = plt.subplots(1, 3, figsize=(6, 2))
axes[0].imshow(digits.images[0], cmap="gray_r")
axes[1].imshow(digits.images[1], cmap="gray_r")
axes[2].imshow(digits.images[2], cmap="gray_r")
fig.suptitle("First three digits")
plt.savefig(OUT / "ax_vs_axes_example.png", **SAVE)
plt.close(fig)


# ── 1. plt.subplots() — empty 2x3 grid with axes[r][c] labels ───────────────
fig, axes = plt.subplots(2, 3, figsize=(6, 3.6))
for r in range(2):
    for c in range(3):
        ax = axes[r][c]
        ax.text(0.5, 0.5, f"axes[{r}][{c}]",
                ha="center", va="center",
                family="monospace", fontsize=14, color=ACCENT)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(ACCENT)
            spine.set_linewidth(1.5)
fig.suptitle("plt.subplots(2, 3)  →  6 empty panels",
             fontsize=12, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "subplots_grid.png", **SAVE)
plt.close(fig)


# ── 2. ax.imshow() — numbers on the left, rendered image on the right ──────
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6))

# Left: same shape, uniform light bg, numbers overlaid
ax = axes[0]
ax.imshow(np.ones_like(sample_3), cmap="gray_r", vmin=0, vmax=20)
for i in range(8):
    for j in range(8):
        v = int(sample_3[i, j])
        ax.text(j, i, v, ha="center", va="center",
                fontsize=9, color=ACCENT, family="monospace")
ax.set_title("the 8x8 numpy array", fontsize=10, family="monospace")
ax.set_xticks([])
ax.set_yticks([])

# Right: rendered as pixels
ax = axes[1]
ax.imshow(sample_3, cmap="gray_r")
ax.set_title('imshow(arr, cmap="gray_r")', fontsize=10, family="monospace")
ax.axis("off")

# Arrow between the two panels
fig.text(0.5, 0.5, "→", ha="center", va="center",
         fontsize=28, color=ACCENT, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT / "imshow_demo.png", **SAVE)
plt.close(fig)


# ── 3. cmap comparison — same digit, four colourmaps ───────────────────────
fig, axes = plt.subplots(1, 4, figsize=(8, 2.6))
for ax, cmap in zip(axes, ["gray_r", "gray", "hot", "viridis"]):
    ax.imshow(sample_3, cmap=cmap)
    ax.set_title(f'"{cmap}"', fontsize=10, family="monospace")
    ax.axis("off")
fig.suptitle("Same digit, four cmaps", fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "cmap_compare.png", **SAVE)
plt.close(fig)


# ── 4. axis on vs axis off ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.2))
axes[0].imshow(sample_3, cmap="gray_r")
axes[0].set_title("default (rulers visible)", fontsize=10, family="monospace")
axes[1].imshow(sample_3, cmap="gray_r")
axes[1].set_title('after ax.axis("off")', fontsize=10, family="monospace")
axes[1].axis("off")
plt.tight_layout()
plt.savefig(OUT / "axis_on_off.png", **SAVE)
plt.close(fig)


# ── 5. fig.suptitle() — three panels with one heading above ────────────────
fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.8))
for ax, img, label in zip(axes, [sample_3, sample_5, sample_8], ["3", "5", "8"]):
    ax.imshow(img, cmap="gray_r")
    ax.set_title(label, fontsize=11, family="monospace")
    ax.axis("off")
fig.suptitle('fig.suptitle("Sample digits per class")',
             fontsize=12, family="monospace", color=ACCENT)
plt.tight_layout()
plt.savefig(OUT / "suptitle_demo.png", **SAVE)
plt.close(fig)


# ── 6. tight_layout() — collision vs cleaned up ────────────────────────────
def _make_collision_fig(use_tight, fname):
    fig, axes = plt.subplots(2, 3, figsize=(5.5, 3.2))
    samples = [sample_3, sample_5, sample_8] * 2
    for ax, img in zip(axes.flat, samples):
        ax.imshow(img, cmap="gray_r")
        ax.set_title("a long panel title", fontsize=9, family="monospace")
        ax.axis("off")
    suffix = "with tight_layout()" if use_tight else "default — titles collide"
    fig.suptitle(suffix, fontsize=11, family="monospace",
                 color=ACCENT if use_tight else "#dc2626")
    if use_tight:
        plt.tight_layout()
    plt.savefig(OUT / fname, **SAVE)
    plt.close(fig)


_make_collision_fig(False, "tight_layout_off.png")
_make_collision_fig(True, "tight_layout_on.png")


# ── 7. plt.show() vs plt.savefig() — schematic of the workflow ─────────────
# (skipped — savefig/show are pure I/O, no useful visual)


print(f"Wrote 8 images to {OUT}")
for p in sorted(OUT.glob("*.png")):
    print("  -", p.name)
