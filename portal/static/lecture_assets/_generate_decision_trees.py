"""
Generate visuals for the four Decision Tree lectures (Stage 1.4).
    python portal/static/lecture_assets/_generate_decision_trees.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED = "#dc2626"
ORANGE = "#f59e0b"
GREEN = "#16a34a"

CLASS_COLORS = [ACCENT, VIOLET, GREEN, RED]
CLASS_NAMES = ["benign", "port_scan", "exfil", "DoS"]


# ── Build the lab dataset (matches solution_how_trees_make_decisions.py) ──
np.random.seed(42)
n_per_class = 500

benign = pd.DataFrame({
    'connection_rate':    np.random.normal(10, 3, n_per_class).clip(1, 25),
    'bytes_sent':         np.random.normal(5000, 1500, n_per_class).clip(100, 15000),
    'bytes_received':     np.random.normal(8000, 2000, n_per_class).clip(100, 20000),
    'unique_dest_ports':  np.random.poisson(3, n_per_class).clip(1, 10),
    'duration_seconds':   np.random.normal(30, 10, n_per_class).clip(1, 120),
    'failed_connections': np.random.poisson(0.5, n_per_class),
    'label': 0,
})
port_scan = pd.DataFrame({
    'connection_rate':    np.random.normal(25, 8, n_per_class).clip(5, 60),
    'bytes_sent':         np.random.normal(500, 200, n_per_class).clip(50, 2000),
    'bytes_received':     np.random.normal(300, 100, n_per_class).clip(0, 1000),
    'unique_dest_ports':  np.random.normal(45, 10, n_per_class).clip(20, 100).astype(int),
    'duration_seconds':   np.random.normal(5, 2, n_per_class).clip(1, 20),
    'failed_connections': np.random.poisson(8, n_per_class),
    'label': 1,
})
exfil = pd.DataFrame({
    'connection_rate':    np.random.normal(8, 2, n_per_class).clip(1, 20),
    'bytes_sent':         np.random.normal(80000, 25000, n_per_class).clip(20000, 250000),
    'bytes_received':     np.random.normal(1000, 300, n_per_class).clip(100, 5000),
    'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
    'duration_seconds':   np.random.normal(180, 60, n_per_class).clip(60, 600),
    'failed_connections': np.random.poisson(0.2, n_per_class),
    'label': 2,
})
dos = pd.DataFrame({
    'connection_rate':    np.random.normal(200, 40, n_per_class).clip(80, 500),
    'bytes_sent':         np.random.normal(200, 80, n_per_class).clip(40, 600),
    'bytes_received':     np.random.normal(100, 40, n_per_class).clip(0, 400),
    'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
    'duration_seconds':   np.random.normal(0.5, 0.2, n_per_class).clip(0.1, 2),
    'failed_connections': np.random.poisson(3, n_per_class),
    'label': 3,
})
df = pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(
    frac=1, random_state=42).reset_index(drop=True)
# Inject 10% label noise — matches the lab solution files
rng = np.random.default_rng(7)
noise_mask = rng.random(len(df)) < 0.10
df.loc[noise_mask, 'label'] = rng.integers(0, 4, noise_mask.sum())
FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df[FEATURES].values
y = df['label'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)


# ── 1. Gini impurity intuition — three nodes pure / mixed / max ──────────
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
node_data = [
    ([100, 0, 0, 0], "Pure node\n(all benign)", "Gini = 0.000"),
    ([60, 0, 0, 40], "Mixed (binary)\n60 benign / 40 DoS", "Gini = 0.480"),
    ([25, 25, 25, 25], "Maximum impurity\n4 classes equal", "Gini = 0.750"),
]
for ax, (counts, title, gini_label) in zip(axes, node_data):
    ax.bar(CLASS_NAMES, counts, color=CLASS_COLORS,
           edgecolor="#222", linewidth=0.8)
    ax.set_title(title + "\n" + gini_label,
                 fontsize=10, family="monospace")
    ax.set_ylim(0, 110)
    ax.set_ylabel("samples", family="monospace", fontsize=8)
    ax.tick_params(axis='x', rotation=30, labelsize=8)
    ax.grid(axis="y", alpha=0.3)
fig.suptitle("Gini impurity: 0 = perfectly pure   ➜   higher = more mixed",
             fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "dt_gini_intuition.png", **SAVE)
plt.close(fig)


# ── 2. Information gain split visualisation ─────────────────────────────
# Hand-built example (matches the lecture's worked numbers exactly):
# 100 samples (60 benign, 40 DoS).  Split on connection_rate ≤ 55:
#   left  child:  58 benign,  2 DoS
#   right child:   2 benign, 38 DoS
def gini_counts(c):
    c = np.array(c)
    if c.sum() == 0:
        return 0
    p = c / c.sum()
    return 1 - np.sum(p ** 2)


parent_counts = [60, 40]
left_counts = [58, 2]
right_counts = [2, 38]
g_p = gini_counts(parent_counts)
g_l = gini_counts(left_counts)
g_r = gini_counts(right_counts)
n_p = sum(parent_counts)
weighted = (sum(left_counts) / n_p) * g_l + (sum(right_counts) / n_p) * g_r
gain = g_p - weighted

fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
panels = [
    (parent_counts, f"Parent (all data)\nGini = {g_p:.3f}",
     f"{n_p} samples"),
    (left_counts,
     f"Left: rate ≤ 55\nGini = {g_l:.3f}",
     f"{sum(left_counts)} samples"),
    (right_counts,
     f"Right: rate > 55\nGini = {g_r:.3f}",
     f"{sum(right_counts)} samples"),
]
for ax, (counts, title, sub_title) in zip(axes, panels):
    bars = ax.bar(["benign", "DoS"], counts, color=[ACCENT, RED],
                  edgecolor="#222", linewidth=0.8)
    for b, v in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, v + 8, str(v),
                ha="center", fontsize=9, family="monospace", weight="bold")
    ax.set_title(title, fontsize=10, family="monospace")
    ax.set_xlabel(sub_title, fontsize=8, family="monospace")
    ax.set_ylim(0, max(parent_counts) * 1.18)
    ax.grid(axis="y", alpha=0.3)
fig.suptitle(
    f"Splitting on connection_rate ≤ 55 → Information gain = "
    f"{g_p:.3f} − {weighted:.3f} = {gain:.3f}",
    fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "dt_information_gain.png", **SAVE)
plt.close(fig)


# ── 3. Class scatter — connection_rate vs bytes_sent ─────────────────────
fig, ax = plt.subplots(figsize=(8, 5.4))
for label_i, name in enumerate(CLASS_NAMES):
    mask = y == label_i
    ax.scatter(df.loc[mask, 'connection_rate'],
               df.loc[mask, 'bytes_sent'],
               s=14, alpha=0.55, color=CLASS_COLORS[label_i],
               edgecolor="none", label=name)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("connection_rate (log)", family="monospace")
ax.set_ylabel("bytes_sent (log)", family="monospace")
ax.set_title("Two features separate the four classes — log axes",
             fontsize=11, family="monospace")
ax.legend(loc="lower left", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3, which="both")
plt.tight_layout()
plt.savefig(OUT / "dt_class_scatter.png", **SAVE)
plt.close(fig)


# ── 4. Trained tree (depth=4) plot_tree ─────────────────────────────────
tree4 = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train, y_train)
fig, ax = plt.subplots(figsize=(20, 11))
plot_tree(
    tree4,
    feature_names=FEATURES,
    class_names=CLASS_NAMES,
    filled=True,
    rounded=True,
    fontsize=11,
    ax=ax,
)
ax.set_title("DecisionTreeClassifier(max_depth=4) trained on the network dataset",
             fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "dt_tree_depth4.png", **SAVE)
plt.close(fig)


# ── 5. Decision regions on a 2D slice (connection_rate, bytes_sent) ───
# Train a 2-feature tree and plot regions
two_features_idx = [FEATURES.index('connection_rate'), FEATURES.index('bytes_sent')]
X_train_2 = X_train[:, two_features_idx]
tree2 = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train_2, y_train)

x_min = max(1, X_train_2[:, 0].min())
x_max = X_train_2[:, 0].max()
y_min = max(40, X_train_2[:, 1].min())
y_max = X_train_2[:, 1].max()
xs = np.logspace(np.log10(x_min), np.log10(x_max), 300)
ys = np.logspace(np.log10(y_min), np.log10(y_max), 300)
XX, YY = np.meshgrid(xs, ys)
ZZ = tree2.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)

from matplotlib.colors import ListedColormap
region_cmap = ListedColormap(["#cffafe", "#ede9fe", "#dcfce7", "#fee2e2"])
fig, ax = plt.subplots(figsize=(8, 5.4))
ax.pcolormesh(XX, YY, ZZ, cmap=region_cmap, shading="auto", alpha=0.85)
for label_i, name in enumerate(CLASS_NAMES):
    mask = y_train == label_i
    ax.scatter(X_train_2[mask, 0], X_train_2[mask, 1],
               s=14, color=CLASS_COLORS[label_i],
               edgecolor="#222", linewidth=0.2, label=name, alpha=0.85)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("connection_rate (log)", family="monospace")
ax.set_ylabel("bytes_sent (log)", family="monospace")
ax.set_title("Decision regions: tree carves the feature space into rectangles",
             fontsize=11, family="monospace")
ax.legend(loc="lower left", fontsize=9, framealpha=0.95)
plt.tight_layout()
plt.savefig(OUT / "dt_decision_regions.png", **SAVE)
plt.close(fig)


# ── 6. Feature importance bar chart ────────────────────────────────────
full_tree = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train, y_train)
imp = full_tree.feature_importances_
order = np.argsort(imp)
fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.barh([FEATURES[i] for i in order], imp[order],
               color=ACCENT, edgecolor="#055e76", linewidth=0.6)
# Highlight top-3
top3_idx = np.argsort(imp)[-3:]
for i, b in zip(order, bars):
    if i in top3_idx:
        b.set_color(RED)
        b.set_edgecolor("#7f1d1d")
for b, v in zip(bars, imp[order]):
    ax.text(v + 0.005, b.get_y() + b.get_height() / 2,
            f"{v:.3f}", va="center", fontsize=9, family="monospace")
ax.set_xlabel("feature_importances_  (sums to 1.0)", family="monospace")
ax.set_title("DecisionTreeClassifier feature importances — top 3 in red",
             fontsize=11, family="monospace")
ax.set_xlim(0, max(imp) * 1.18)
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "dt_feature_importance.png", **SAVE)
plt.close(fig)


# ── 7. Top-3 vs full feature accuracy comparison ───────────────────────
top3 = [FEATURES[i] for i in np.argsort(imp)[-3:][::-1]]
top3_idx = [FEATURES.index(f) for f in top3]
small_tree = DecisionTreeClassifier(max_depth=4, random_state=42).fit(
    X_train[:, top3_idx], y_train)
acc_full = full_tree.score(X_test, y_test)
acc_small = small_tree.score(X_test[:, top3_idx], y_test)

fig, ax = plt.subplots(figsize=(6.4, 3.8))
labels = [f"Full\n(6 features)", f"Top-3\n({', '.join(top3)})"]
vals = [acc_full, acc_small]
bars = ax.bar(labels, vals, color=[ACCENT, RED],
              edgecolor="#222", linewidth=0.8, width=0.55)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.005,
            f"{v:.3f}", ha="center", fontsize=11,
            family="monospace", weight="bold")
ax.set_ylabel("test accuracy", family="monospace")
ax.set_ylim(0.85, 1.005)
ax.set_title(f"Dropping 3 features costs only {(acc_full - acc_small) * 100:.1f} pp",
             fontsize=10, family="monospace")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "dt_top3_comparison.png", **SAVE)
plt.close(fig)


# ── 8. Depth sweep — train vs test accuracy ─────────────────────────────
depths = list(range(1, 16))
train_acc, test_acc = [], []
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    train_acc.append(m.score(X_train, y_train))
    test_acc.append(m.score(X_test, y_test))

best_depth = depths[int(np.argmax(test_acc))]

fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.plot(depths, train_acc, "-o", color=ACCENT, linewidth=2,
        markersize=6, label="train accuracy")
ax.plot(depths, test_acc, "--o", color=RED, linewidth=2,
        markersize=6, label="test accuracy")
ax.axvline(best_depth, color=VIOLET, linestyle=":", linewidth=2,
           label=f"sweet spot: depth={best_depth}")
ax.fill_between(depths, train_acc, test_acc, color=RED, alpha=0.08)
# Annotate the underfit and overfit zones
ax.annotate("underfit\n(both low)", xy=(1.5, 0.7), fontsize=9,
            family="monospace", color="#444", ha="center")
ax.annotate("overfit gap →", xy=(13, 0.97), fontsize=9,
            family="monospace", color=RED, ha="center")
ax.set_xlabel("max_depth", family="monospace")
ax.set_ylabel("accuracy", family="monospace")
ax.set_title("Depth sweep — train vs test accuracy reveals overfitting",
             fontsize=11, family="monospace")
ax.set_xticks(depths)
ax.legend(loc="lower right", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
ax.set_ylim(0.6, 1.02)
plt.tight_layout()
plt.savefig(OUT / "dt_depth_sweep.png", **SAVE)
plt.close(fig)


# ── 9. Three trees side by side — depth 1, sweet, 15 ───────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5.4))
configs = [
    (1, "max_depth=1\nUNDERFIT"),
    (best_depth, f"max_depth={best_depth}\nGOOD FIT"),
    (15, "max_depth=15\nOVERFIT"),
]
for ax, (d, title) in zip(axes, configs):
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train_2, y_train)
    Z = m.predict(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
    ax.pcolormesh(XX, YY, Z, cmap=region_cmap, shading="auto", alpha=0.85)
    for label_i in range(4):
        mask = y_train == label_i
        ax.scatter(X_train_2[mask, 0], X_train_2[mask, 1],
                   s=8, color=CLASS_COLORS[label_i],
                   edgecolor="#222", linewidth=0.15, alpha=0.7)
    ax.set_xscale("log")
    ax.set_yscale("log")
    tr = m.score(X_train_2, y_train)
    te = m.score(X_test[:, two_features_idx], y_test)
    ax.set_title(f"{title}\ntrain={tr:.3f}  test={te:.3f}",
                 fontsize=10, family="monospace")
    ax.set_xlabel("connection_rate", family="monospace", fontsize=8)
axes[0].set_ylabel("bytes_sent", family="monospace", fontsize=8)
fig.suptitle("Same data, three depths — boundaries get jagged as the tree memorises",
             fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "dt_overfit_compare.png", **SAVE)
plt.close(fig)


print("Wrote 9 decision-tree images")
