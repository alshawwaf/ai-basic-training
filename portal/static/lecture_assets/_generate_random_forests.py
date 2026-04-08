"""
Generate visuals for the four Random Forest lectures (Stage 2.2).
    python portal/static/lecture_assets/_generate_random_forests.py

Reproduces the synthetic PE-file dataset (3 000 samples, 13 features) and
trains the same trees / forests the four solution_*.py files do.
"""
from pathlib import Path
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED    = "#dc2626"
ORANGE = "#f59e0b"
GREEN  = "#16a34a"
GREY   = "#64748b"
LIGHT  = "#e2e8f0"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

# ── Reproduce the PE feature dataset (matches every Stage 2.2 solution) ───────
np.random.seed(42)
n = 3000

def make_pe_features(n_samples, malware=False):
    if malware:
        return {
            'file_entropy':       np.random.normal(7.2, 0.5, n_samples).clip(4, 8),
            'num_sections':       np.random.poisson(6, n_samples).clip(2, 20),
            'num_imports':        np.random.poisson(15, n_samples).clip(0, 60),
            'num_exports':        np.random.poisson(2, n_samples).clip(0, 20),
            'has_debug_info':     np.random.binomial(1, 0.05, n_samples),
            'virtual_size_ratio': np.random.normal(3.5, 1, n_samples).clip(1, 10),
            'uses_network_dlls':  np.random.binomial(1, 0.75, n_samples),
            'uses_crypto_dlls':   np.random.binomial(1, 0.60, n_samples),
            'file_size_kb':       np.random.lognormal(7, 1.5, n_samples).clip(10, 20000),
            'code_section_size':  np.random.lognormal(9, 1, n_samples).clip(100, 500000),
            'suspicious_strings': np.random.poisson(8, n_samples).clip(0, 40),
            'has_valid_signature':np.random.binomial(1, 0.08, n_samples),
            'packer_detected':    np.random.binomial(1, 0.65, n_samples),
        }
    else:
        return {
            'file_entropy':       np.random.normal(5.5, 0.8, n_samples).clip(2, 7.5),
            'num_sections':       np.random.poisson(4, n_samples).clip(1, 8),
            'num_imports':        np.random.poisson(80, n_samples).clip(10, 250),
            'num_exports':        np.random.poisson(30, n_samples).clip(0, 150),
            'has_debug_info':     np.random.binomial(1, 0.60, n_samples),
            'virtual_size_ratio': np.random.normal(1.2, 0.3, n_samples).clip(0.8, 3),
            'uses_network_dlls':  np.random.binomial(1, 0.30, n_samples),
            'uses_crypto_dlls':   np.random.binomial(1, 0.20, n_samples),
            'file_size_kb':       np.random.lognormal(9, 1.2, n_samples).clip(50, 200000),
            'code_section_size':  np.random.lognormal(11, 1, n_samples).clip(1000, 10000000),
            'suspicious_strings': np.random.poisson(1, n_samples).clip(0, 5),
            'has_valid_signature':np.random.binomial(1, 0.80, n_samples),
            'packer_detected':    np.random.binomial(1, 0.05, n_samples),
        }

malware_df = pd.DataFrame(make_pe_features(n // 2, malware=True))
malware_df['label'] = 1
benign_df  = pd.DataFrame(make_pe_features(n // 2, malware=False))
benign_df['label'] = 0
df = pd.concat([malware_df, benign_df], ignore_index=True).sample(frac=1, random_state=42)
feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols].astype(float)
y = df['label']
# The synthetic malware/benign distributions are too cleanly separable
# (every classifier scores 1.000). Add per-feature Gaussian noise so the
# classes overlap the way real PE features do.
rng = np.random.default_rng(13)
noise_scale = X.std(axis=0).values * 1.4
X = X + rng.normal(0, noise_scale, X.shape)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ── Train baseline single tree and forest (used by several plots) ─────────────
single_tree = DecisionTreeClassifier(max_depth=None, random_state=42).fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=100, oob_score=True,
                                random_state=42, n_jobs=-1).fit(X_train, y_train)

single_train = accuracy_score(y_train, single_tree.predict(X_train))
single_test  = accuracy_score(y_test,  single_tree.predict(X_test))
forest_train = accuracy_score(y_train, forest.predict(X_train))
forest_test  = accuracy_score(y_test,  forest.predict(X_test))
forest_oob   = forest.oob_score_

print(f"Single tree:   train={single_train:.3f} test={single_test:.3f}")
print(f"Random forest: train={forest_train:.3f} test={forest_test:.3f} oob={forest_oob:.3f}")


def card(ax, x, y, w, h, label, fill=LIGHT, edge=GREY, fc_label="#0f172a", fontsize=10):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                         linewidth=1.4, edgecolor=edge, facecolor=fill)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, ha="center", va="center",
            fontsize=fontsize, color=fc_label)


# ══════════════════════════════════════════════════════════════════════════════
# 1. rf_overfit_gap — single tree train vs test bars
# ══════════════════════════════════════════════════════════════════════════════
def viz_overfit_gap():
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    bars = ax.bar(["Training accuracy", "Test accuracy"],
                  [single_train, single_test],
                  color=[GREEN, RED], edgecolor="white", linewidth=2)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("accuracy")
    ax.set_title("Single DecisionTree(max_depth=None) memorises the training set")
    for b, v in zip(bars, [single_train, single_test]):
        ax.text(b.get_x() + b.get_width()/2, v + 0.02, f"{v:.3f}",
                ha="center", fontsize=12, fontweight="bold")
    gap = single_train - single_test
    ax.annotate("", xy=(1, single_test + 0.005), xytext=(1, single_train - 0.005),
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=2))
    ax.text(1.18, (single_train + single_test) / 2,
            f"overfit gap\n= {gap:.3f}",
            ha="left", va="center", fontsize=10.5, color=ORANGE, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.savefig(OUT / "rf_overfit_gap.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 2. rf_bagging_flow — bootstrap → trees → vote diagram
# ══════════════════════════════════════════════════════════════════════════════
def viz_bagging_flow():
    fig, ax = plt.subplots(figsize=(11.0, 5.4))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")

    # Training data
    card(ax, 5.2, 6.5, 3.6, 1.0, "Training data (N rows)",
         fill="#f8fafc", edge=GREY, fontsize=11)

    # bootstrap labels
    samples = ["Sample 1", "Sample 2", "Sample 3", "Sample K"]
    trees   = ["Tree 1",   "Tree 2",   "Tree 3",   "Tree K"]
    preds   = [1, 0, 1, 1]
    x_centers = [1.7, 5.0, 8.3, 11.6]
    for i, (s, t, p, xc) in enumerate(zip(samples, trees, preds, x_centers)):
        # arrow from training data
        ax.add_patch(FancyArrowPatch((7.0, 6.4), (xc, 5.65), arrowstyle="-|>",
                                     mutation_scale=14, color=GREY, linewidth=1.4))
        # bootstrap sample card
        card(ax, xc-1.2, 4.6, 2.4, 1.0, s, fill="#ecfeff", edge=ACCENT, fc_label=ACCENT)
        # arrow to tree
        ax.add_patch(FancyArrowPatch((xc, 4.55), (xc, 3.85), arrowstyle="-|>",
                                     mutation_scale=14, color=GREY, linewidth=1.4))
        # tree card
        card(ax, xc-1.2, 2.85, 2.4, 1.0, t, fill="#f3e8ff", edge=VIOLET, fc_label=VIOLET)
        # arrow to prediction
        ax.add_patch(FancyArrowPatch((xc, 2.80), (xc, 2.10), arrowstyle="-|>",
                                     mutation_scale=14, color=GREY, linewidth=1.4))
        # prediction label
        c = GREEN if p == 1 else RED
        ax.add_patch(Circle((xc, 1.7), 0.30, facecolor=c, edgecolor="white", linewidth=2))
        ax.text(xc, 1.7, str(p), ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")

    # ellipsis between Tree 3 and Tree K
    for dx in [-0.18, 0, 0.18]:
        ax.add_patch(Circle((9.95 + dx, 3.35), 0.05, facecolor=GREY))

    # vote box
    ax.add_patch(FancyArrowPatch((6.7, 1.4), (6.7, 0.85), arrowstyle="-|>",
                                 mutation_scale=14, color=GREY, linewidth=1.4))
    card(ax, 4.6, 0.05, 4.2, 0.75, "Majority vote → final prediction = 1",
         fill="#0f172a", edge="#0f172a", fc_label="white", fontsize=11)
    plt.savefig(OUT / "rf_bagging_flow.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 3. rf_variance_reduction — 20 single trees vs 20 forests scatter
# ══════════════════════════════════════════════════════════════════════════════
def viz_variance_reduction():
    n_runs = 20
    tree_accs, forest_accs = [], []
    for i in range(n_runs):
        t = DecisionTreeClassifier(max_depth=None, random_state=i).fit(X_train, y_train)
        tree_accs.append(accuracy_score(y_test, t.predict(X_test)))
        rf = RandomForestClassifier(n_estimators=100, random_state=i, n_jobs=-1).fit(X_train, y_train)
        forest_accs.append(accuracy_score(y_test, rf.predict(X_test)))
    tree_accs = np.array(tree_accs); forest_accs = np.array(forest_accs)

    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    ax.scatter(range(n_runs), tree_accs,   s=80, color=RED,   label=f"Single tree   μ={tree_accs.mean():.3f}, σ={tree_accs.std():.3f}",
               edgecolor="white", linewidth=1.4, zorder=3)
    ax.scatter(range(n_runs), forest_accs, s=80, color=ACCENT, label=f"Random forest μ={forest_accs.mean():.3f}, σ={forest_accs.std():.3f}",
               edgecolor="white", linewidth=1.4, zorder=3)
    ax.axhline(tree_accs.mean(),   color=RED,    linestyle="--", linewidth=1, alpha=0.5)
    ax.axhline(forest_accs.mean(), color=ACCENT, linestyle="--", linewidth=1, alpha=0.5)
    ax.set_xlabel("run index (different random_state)")
    ax.set_ylabel("test accuracy")
    ax.set_title("Single trees scatter wildly across seeds; forests converge")
    ax.legend(loc="lower right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ratio = tree_accs.std() / forest_accs.std()
    ax.text(0.02, 0.97, f"σ ratio: single tree is {ratio:.1f}× more variable",
            transform=ax.transAxes, va="top", fontsize=10,
            color=ORANGE, fontweight="bold")
    plt.savefig(OUT / "rf_variance_reduction.png", **SAVE); plt.close(fig)
    return tree_accs, forest_accs


# ══════════════════════════════════════════════════════════════════════════════
# 4. rf_oob_concept — out-of-bag samples diagram
# ══════════════════════════════════════════════════════════════════════════════
def viz_oob_concept():
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.text(6, 5.5, "Each bootstrap leaves ≈ 37 % of rows untouched — those are the OOB sample",
            ha="center", fontsize=11, color="#0f172a")

    # Training rows as a strip of cells
    n_cells = 30
    cell_w = 11.0 / n_cells
    rng = np.random.default_rng(0)
    chosen = set(rng.choice(n_cells, size=int(n_cells*0.63), replace=False))
    for i in range(n_cells):
        c = ACCENT if i in chosen else ORANGE
        ax.add_patch(Rectangle((0.5 + i*cell_w, 3.4), cell_w-0.05, 0.9,
                               facecolor=c, edgecolor="white", linewidth=1))
    ax.text(0.5 + n_cells*cell_w/2, 4.5, "Training rows", ha="center",
            fontsize=10.5, color="#475569", fontweight="bold")
    # legend
    ax.add_patch(Rectangle((1.5, 1.7), 0.5, 0.45, facecolor=ACCENT))
    ax.text(2.15, 1.92, "in this tree's bootstrap (≈63%)  → used for fit",
            va="center", fontsize=10)
    ax.add_patch(Rectangle((1.5, 0.95), 0.5, 0.45, facecolor=ORANGE))
    ax.text(2.15, 1.17, "out-of-bag (≈37%)  → free validation set",
            va="center", fontsize=10)
    ax.text(6, 0.2,
            f"oob_score_ on the lab forest = {forest_oob:.3f}  (test = {forest_test:.3f}) — "
            "OOB tracks the held-out test score for free",
            ha="center", fontsize=10.5, color=ACCENT, fontweight="bold", style="italic")
    plt.savefig(OUT / "rf_oob_concept.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 5. rf_feature_subsampling — feature pool → random subset per tree
# ══════════════════════════════════════════════════════════════════════════════
def viz_feature_subsampling():
    pool = ['file_entropy', 'packer_detected', 'virtual_size_ratio',
            'num_imports', 'suspicious_strings', 'code_section_size', 'num_sections']
    subsets = [
        (['file_entropy', 'packer_detected', 'code_section_size'],   'file_entropy'),
        (['virtual_size_ratio', 'num_imports', 'num_sections'],      'virtual_size_ratio'),
        (['file_entropy', 'suspicious_strings', 'num_imports'],      'file_entropy'),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")
    ax.text(7, 7.4, "Full feature pool (7 features)", ha="center",
            fontsize=11, color="#475569", fontweight="bold")
    pool_w = 1.7
    for i, f in enumerate(pool):
        x0 = 0.7 + i*1.85
        ax.add_patch(FancyBboxPatch((x0, 6.2), pool_w, 0.85,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor="#f8fafc", edgecolor=GREY, linewidth=1.2))
        ax.text(x0+pool_w/2, 6.62, f, ha="center", va="center", fontsize=8.6,
                family="monospace")

    # three trees, each with their subset
    tree_colors = [ACCENT, VIOLET, ORANGE]
    for ti, ((subset, chosen), c) in enumerate(zip(subsets, tree_colors)):
        y = 4.4 - ti*1.55
        ax.text(0.4, y+0.4, f"Tree {ti+1}", fontsize=11, fontweight="bold", color=c)
        for i, f in enumerate(pool):
            x0 = 1.6 + i*1.85
            in_subset = f in subset
            face = "#ffffff"
            edge = c if in_subset else "#cbd5e1"
            ax.add_patch(FancyBboxPatch((x0, y), pool_w, 0.85,
                                        boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor=face, edgecolor=edge,
                                        linewidth=2 if in_subset else 1))
            text_color = "#0f172a" if in_subset else "#cbd5e1"
            weight = "bold" if f == chosen else "normal"
            ax.text(x0+pool_w/2, y+0.42, f, ha="center", va="center", fontsize=8.4,
                    family="monospace", color=text_color, fontweight=weight)
        # arrow + chosen split
        ax.add_patch(FancyArrowPatch((13.6, y+0.42), (14.2, y+0.42), arrowstyle="-|>",
                                     mutation_scale=12, color=c, linewidth=1.8))
        ax.text(13.9, y+0.95, "splits on", ha="center", fontsize=8, color=c)
    ax.text(7, 0.2,
            "max_features='sqrt' → each tree sees only √7 ≈ 3 features at every split. "
            "Different trees pick different splits even when one feature is genuinely strong.",
            ha="center", fontsize=10, color="#475569", style="italic")
    plt.savefig(OUT / "rf_feature_subsampling.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 6. rf_tree_vs_forest — side-by-side comparison bar chart
# ══════════════════════════════════════════════════════════════════════════════
def viz_tree_vs_forest():
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    labels = ["Train acc", "Test acc"]
    x = np.arange(len(labels)); w = 0.34
    tree_vals   = [single_train, single_test]
    forest_vals = [forest_train, forest_test]
    ax.bar(x - w/2, tree_vals,   w, label="Single Tree",   color=RED,    edgecolor="white", linewidth=2)
    ax.bar(x + w/2, forest_vals, w, label="Random Forest", color=ACCENT, edgecolor="white", linewidth=2)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.08); ax.set_ylabel("accuracy")
    ax.set_title("Both fit the train set — only the forest holds up on test")
    for xi, v in zip(x - w/2, tree_vals):
        ax.text(xi, v + 0.015, f"{v:.3f}", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    for xi, v in zip(x + w/2, forest_vals):
        ax.text(xi, v + 0.015, f"{v:.3f}", ha="center", fontsize=10.5, color=ACCENT, fontweight="bold")
    # OOB callout
    ax.axhline(forest_oob, color=ACCENT, linestyle=":", alpha=0.6)
    ax.text(1.5, forest_oob - 0.04, f"OOB = {forest_oob:.3f}",
            color=ACCENT, fontsize=9.5, ha="right", fontweight="bold")
    ax.legend(loc="lower left")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.savefig(OUT / "rf_tree_vs_forest.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 7. rf_feature_importance_bars — sorted bar chart with error bars
# ══════════════════════════════════════════════════════════════════════════════
def viz_feature_importance_bars():
    n_runs = 20
    imps = np.zeros((n_runs, len(feature_cols)))
    for i in range(n_runs):
        rf = RandomForestClassifier(n_estimators=100, random_state=i, n_jobs=-1)
        rf.fit(X_train, y_train)
        imps[i] = rf.feature_importances_
    mean = imps.mean(axis=0); se = imps.std(axis=0)
    order = np.argsort(mean)[::-1]
    feats_sorted = [feature_cols[i] for i in order]
    mean_sorted  = mean[order]
    se_sorted    = se[order]

    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    y_pos = np.arange(len(feats_sorted))
    bars  = ax.barh(y_pos, mean_sorted, xerr=se_sorted,
                    color=ACCENT, edgecolor="white", capsize=4,
                    error_kw=dict(ecolor=ORANGE, lw=1.6))
    ax.set_yticks(y_pos); ax.set_yticklabels(feats_sorted, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("mean Gini importance (20 random forest runs)")
    ax.set_title("PE feature importance — error bars = std across 20 seeds")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    for b, v in zip(bars, mean_sorted):
        ax.text(v + 0.005, b.get_y() + b.get_height()/2, f"{v:.3f}",
                va="center", fontsize=9, color="#0f172a")
    plt.tight_layout()
    plt.savefig(OUT / "rf_feature_importance_bars.png", **SAVE); plt.close(fig)
    return feats_sorted, mean_sorted, se_sorted


# ══════════════════════════════════════════════════════════════════════════════
# 8. rf_importance_stability — single tree std vs forest std
# ══════════════════════════════════════════════════════════════════════════════
def viz_importance_stability():
    n_runs = 20
    tree_imps   = np.zeros((n_runs, len(feature_cols)))
    forest_imps = np.zeros((n_runs, len(feature_cols)))
    for i in range(n_runs):
        t = DecisionTreeClassifier(max_depth=None, random_state=i).fit(X_train, y_train)
        tree_imps[i] = t.feature_importances_
        rf = RandomForestClassifier(n_estimators=100, random_state=i, n_jobs=-1).fit(X_train, y_train)
        forest_imps[i] = rf.feature_importances_
    tree_std   = tree_imps.std(axis=0)
    forest_std = forest_imps.std(axis=0)
    order = np.argsort(tree_std)[::-1]
    feats = [feature_cols[i] for i in order]

    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    y_pos = np.arange(len(feats))
    w = 0.4
    ax.barh(y_pos - w/2, tree_std[order],   w, color=RED,    label="Single tree", edgecolor="white")
    ax.barh(y_pos + w/2, forest_std[order], w, color=ACCENT, label="Random forest", edgecolor="white")
    ax.set_yticks(y_pos); ax.set_yticklabels(feats, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel("std of feature importance across 20 seeds  (lower = more stable)")
    ax.set_title("Forest importances are dramatically more stable per feature")
    ax.legend(loc="lower right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ratio = tree_std.mean() / forest_std.mean()
    ax.text(0.98, 0.02, f"mean σ ratio: {ratio:.1f}× more stable in the forest",
            transform=ax.transAxes, ha="right", va="bottom",
            color=ACCENT, fontsize=10.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "rf_importance_stability.png", **SAVE); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 9. rf_learning_curve — n_estimators vs accuracy
# ══════════════════════════════════════════════════════════════════════════════
def viz_learning_curve():
    tree_counts = [1, 5, 10, 25, 50, 100, 200, 500]
    accs, times = [], []
    for nt in tree_counts:
        t0 = time.time()
        rf = RandomForestClassifier(n_estimators=nt, random_state=42, n_jobs=-1).fit(X_train, y_train)
        times.append(time.time() - t0)
        accs.append(accuracy_score(y_test, rf.predict(X_test)))

    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.plot(tree_counts, accs, marker="o", color=ACCENT, linewidth=2.2, markersize=9,
            markerfacecolor="white", markeredgewidth=2)
    for x, a in zip(tree_counts, accs):
        ax.text(x, a + 0.004, f"{a:.3f}", ha="center", fontsize=9, color="#0f172a")
    ax.set_xscale("log")
    ax.set_xticks(tree_counts)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel("n_estimators (log scale)")
    ax.set_ylabel("test accuracy")
    ax.set_title("Random forest learning curve — diminishing returns past the elbow")
    # mark elbow
    elbow_idx = None
    for i in range(1, len(accs)):
        if accs[i] - accs[i-1] < 0.001:
            elbow_idx = i - 1; break
    if elbow_idx is not None:
        ax.axvline(tree_counts[elbow_idx], color=ORANGE, linestyle="--", linewidth=1.5)
        ax.text(tree_counts[elbow_idx]*1.1, min(accs) + 0.005,
                f"elbow ≈ {tree_counts[elbow_idx]}",
                color=ORANGE, fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "rf_learning_curve.png", **SAVE); plt.close(fig)
    return tree_counts, accs, times


# ══════════════════════════════════════════════════════════════════════════════
# 10. rf_max_features — bar chart for max_features comparison
# ══════════════════════════════════════════════════════════════════════════════
def viz_max_features():
    options = [1, 2, 3, 4, 5, 'sqrt', 'log2']
    accs = []
    for mf in options:
        rf = RandomForestClassifier(n_estimators=100, max_features=mf,
                                    random_state=42, n_jobs=-1).fit(X_train, y_train)
        accs.append(accuracy_score(y_test, rf.predict(X_test)))
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    labels = [str(o) for o in options]
    colours = [ACCENT if o == 'sqrt' else GREY for o in options]
    bars = ax.bar(labels, accs, color=colours, edgecolor="white", linewidth=2)
    ax.set_ylim(min(accs) - 0.01, max(accs) + 0.012)
    ax.set_ylabel("test accuracy")
    ax.set_xlabel("max_features")
    ax.set_title("Cyan = the default 'sqrt' — usually the right call")
    for b, v in zip(bars, accs):
        ax.text(b.get_x() + b.get_width()/2, v + 0.0015, f"{v:.3f}",
                ha="center", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "rf_max_features.png", **SAVE); plt.close(fig)
    return options, accs


# ══════════════════════════════════════════════════════════════════════════════
# 11. rf_time_vs_acc — scatter sweet spot plot
# ══════════════════════════════════════════════════════════════════════════════
def viz_time_vs_accuracy(tree_counts, accs, times):
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    ax.scatter(times, accs, s=160, color=ACCENT, edgecolor="white", linewidth=1.6, zorder=3)
    for t, a, n in zip(times, accs, tree_counts):
        ax.annotate(f"n={n}", (t, a), xytext=(8, 6), textcoords="offset points",
                    fontsize=9.5, color="#0f172a")
    ax.set_xlabel("training time (seconds)")
    ax.set_ylabel("test accuracy")
    ax.set_title("Sweet spot: cheapest training time at the accuracy plateau")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "rf_time_vs_accuracy.png", **SAVE); plt.close(fig)


if __name__ == "__main__":
    print("Generating Stage 2.2 Random Forests visuals...")
    viz_overfit_gap();          print("  ✓ rf_overfit_gap.png")
    viz_bagging_flow();         print("  ✓ rf_bagging_flow.png")
    viz_variance_reduction();   print("  ✓ rf_variance_reduction.png")
    viz_oob_concept();          print("  ✓ rf_oob_concept.png")
    viz_feature_subsampling();  print("  ✓ rf_feature_subsampling.png")
    viz_tree_vs_forest();       print("  ✓ rf_tree_vs_forest.png")
    viz_feature_importance_bars(); print("  ✓ rf_feature_importance_bars.png")
    viz_importance_stability(); print("  ✓ rf_importance_stability.png")
    tc, accs, times = viz_learning_curve(); print("  ✓ rf_learning_curve.png")
    viz_max_features();         print("  ✓ rf_max_features.png")
    viz_time_vs_accuracy(tc, accs, times); print("  ✓ rf_time_vs_accuracy.png")
    print("Done.")
