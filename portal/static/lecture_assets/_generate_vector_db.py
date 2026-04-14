"""
Generate two separate PNGs that explain a vector database step-by-step:
    gn_vector_db_index.png    — INDEX phase: docs become points
    gn_vector_db_search.png   — SEARCH phase: query lands, find K nearest

Splitting them into two larger figures (vs one 2-panel chart) gives the
labels enough breathing room to be readable inside the lecture drawer.

This is a *teaching diagram*, not a benchmark. The 2D positions are
hand-crafted so the clusters are unambiguous and labels do not collide.
No sentence-transformers / torch dependency.

Run:
    venv/Scripts/python portal/static/lecture_assets/_generate_vector_db.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"   # cyan — network
VIOLET = "#8b5cf6"   # query marker
RED    = "#dc2626"   # threat cluster
GREY   = "#64748b"   # unrelated
DARK   = "#0f172a"
GOLD   = "#facc15"   # top-K highlight ring

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 15,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 11,
})

# ── Hand-crafted "embedding" coordinates ──────────────────────────────
# Each entry: (text, group, x, y, label_dx, label_dy, label_anchor)
# Positions and label offsets are tuned by hand so nothing overlaps in
# either figure. Threat cluster spread out wider on the left so the
# query star + 3 ring annotations on the SEARCH chart all have room.
docs = [
    # threat cluster (wider spread, biased to the left half)
    ("Ransomware encrypted the file server",   "threat",  -3.4,  2.2,  10,  6,  "left"),
    ("Phishing email impersonating IT",        "threat",  -3.2,  0.9,  10,  6,  "left"),
    ("SQL injection in login form",            "threat",  -3.6, -0.4,  10,  6,  "left"),
    ("Suspicious PowerShell process",          "threat",  -2.0,  2.6,  10,  6,  "left"),
    ("Credential dump on a leak site",         "threat",  -1.6,  1.3,  10,  6,  "left"),

    # network cluster (right half, upper)
    ("Firewall rule allows port 443",          "network",  3.0,  2.4,  10,  6,  "left"),
    ("Router BGP session reconverged",         "network",  3.6,  1.0,  10,  6,  "left"),
    ("VPN tunnel renegotiated keys",           "network",  2.4,  0.4,  10,  6,  "left"),
    ("Switch spanning-tree change",            "network",  3.4, -0.7,  10,  6,  "left"),

    # unrelated cluster (lower middle)
    ("Recipe for chocolate cake",              "other",   -1.2, -2.6,  10,  6,  "left"),
    ("Football match results",                 "other",    1.0, -2.9,  10,  6,  "left"),
    ("Coffee shop opening hours",              "other",    0.0, -1.9,  10,  6,  "left"),
]

texts   = [d[0] for d in docs]
groups  = [d[1] for d in docs]
V2      = np.array([[d[2], d[3]] for d in docs], dtype=float)
ldx     = [d[4] for d in docs]
ldy     = [d[5] for d in docs]
lanchor = [d[6] for d in docs]

# Query lands among the threat docs but offset enough that ring labels
# do not crash into each other. Sits just below the cluster centroid.
query_text = "How do I detect ransomware on a host?"
q2 = np.array([-2.6,  1.7])

# Top-3 nearest by Euclidean distance
dists = np.linalg.norm(V2 - q2, axis=1)
topk_idx = np.argsort(dists)[:3]

colour = {"threat": RED, "network": ACCENT, "other": GREY}
GROUP_LABEL = {
    "threat":  "threat docs",
    "network": "network docs",
    "other":   "other docs",
}

XLIM = (-5.0, 5.5)
YLIM = (-3.6, 3.4)


def style_axes(ax):
    ax.set_xlabel('embedding dim 1 (illustrative)')
    ax.set_ylabel('embedding dim 2 (illustrative)')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.tick_params(colors=DARK)


# ─────────────────────────────────────────────────────────────────────
# FIGURE 1 — INDEX
# ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

for grp in ["threat", "network", "other"]:
    mask = [g == grp for g in groups]
    ax.scatter(V2[mask, 0], V2[mask, 1], s=320, color=colour[grp],
               edgecolor='white', linewidth=2.5, zorder=3,
               label=GROUP_LABEL[grp], alpha=0.95)

for (x, y), txt, dx, dy, anch in zip(V2, texts, ldx, ldy, lanchor):
    ax.annotate(txt, (x, y),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=10, color=DARK, ha=anch,
                bbox=dict(boxstyle="round,pad=0.25",
                          facecolor='white', edgecolor='#cbd5e1', lw=0.8,
                          alpha=0.92))

ax.set_title("STEP 1 — INDEX:  every document becomes a point in space\n"
             "similar meaning ⇒ nearby coordinates  (no labels needed)",
             pad=14)
style_axes(ax)
ax.legend(loc='lower right', framealpha=0.97, fontsize=11)

fig.tight_layout()
fig.savefig(OUT / "gn_vector_db_index.png", **SAVE)
plt.close(fig)
print("  wrote gn_vector_db_index.png")


# ─────────────────────────────────────────────────────────────────────
# FIGURE 2 — SEARCH
# ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

# faded background docs
for grp in ["threat", "network", "other"]:
    mask = [g == grp for g in groups]
    ax.scatter(V2[mask, 0], V2[mask, 1], s=200, color=colour[grp],
               edgecolor='white', linewidth=1.5, zorder=2,
               alpha=0.30, label=GROUP_LABEL[grp])

# arrows from query to each top-K hit (drawn first, behind markers)
for idx in topk_idx:
    ax.annotate("", xy=(V2[idx, 0], V2[idx, 1]),
                xytext=(q2[0], q2[1]),
                arrowprops=dict(arrowstyle='->', color=GOLD,
                                lw=2.5, alpha=0.92,
                                shrinkA=14, shrinkB=14),
                zorder=4)

# top-K highlighted markers + ring + non-overlapping labels
# Place each label on a distinct side of the dot so nothing collides.
RANK_LABEL_OFFSETS = [
    (14, 14),    # #1 — up-right
    (14, -22),   # #2 — down-right
    (-14, 14),   # #3 — up-left
]
RANK_LABEL_HA = ['left', 'left', 'right']

for rank, idx in enumerate(topk_idx):
    x, y = V2[idx]
    ax.scatter([x], [y], s=720, facecolors='none',
               edgecolor=GOLD, linewidth=3.5, zorder=5)
    ax.scatter([x], [y], s=320, color=colour[groups[idx]],
               edgecolor='white', linewidth=2.5, zorder=6)

    dx, dy = RANK_LABEL_OFFSETS[rank]
    ax.annotate(f"#{rank + 1}    d = {dists[idx]:.2f}", (x, y),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=11, color=DARK, fontweight='bold',
                ha=RANK_LABEL_HA[rank],
                bbox=dict(boxstyle="round,pad=0.3",
                          facecolor='#fef9c3', edgecolor=GOLD, lw=1.5))

# query star — placed AFTER the rings so it sits on top
ax.scatter([q2[0]], [q2[1]], s=820, marker='*', color=VIOLET,
           edgecolor='white', linewidth=3, zorder=7, label='query')

# query text label is anchored well below the cluster, on the right side,
# so it never overlaps any of the top-K rings.
ax.annotate(f'query:\n"{query_text}"',
            (q2[0], q2[1]),
            xytext=(60, -90), textcoords='offset points',
            fontsize=11, color=VIOLET, fontweight='bold',
            ha='left',
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor='white', edgecolor=VIOLET, lw=1.5),
            arrowprops=dict(arrowstyle='->', color=VIOLET,
                            lw=1.5, alpha=0.85,
                            shrinkA=4, shrinkB=12,
                            connectionstyle="arc3,rad=-0.2"))

ax.set_title("STEP 2 — SEARCH:  encode the query, return top-K nearest\n"
             "this is the entire vector-DB lookup",
             pad=14)
style_axes(ax)
ax.legend(loc='lower right', framealpha=0.97, fontsize=11)

fig.tight_layout()
fig.savefig(OUT / "gn_vector_db_search.png", **SAVE)
plt.close(fig)
print("  wrote gn_vector_db_search.png")
