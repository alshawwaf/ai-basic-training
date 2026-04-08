"""
Generate visuals for the four Overfitting / Cross-Validation lectures (Stage 2.4).
    python portal/static/lecture_assets/_generate_overfitting_cv.py

Reproduces the synthetic intrusion dataset (2 000 samples, 6 features) and
the same depth sweeps / CV runs the four solution_*.py files do, with
sigma=1.5 Gaussian noise so depth=1 actually underfits.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (train_test_split, cross_val_score,
                                     learning_curve, validation_curve)
from sklearn.decomposition import PCA

OUT = Path(__file__).resolve().parent

DPI  = 140
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

# ── Reproduce the lab dataset (matches every Stage 2.4 solution) ─────────────
np.random.seed(42)
n_per = 1000

benign = pd.DataFrame({
    'connection_rate':    np.random.normal(10, 3, n_per).clip(1, 25),
    'bytes_sent':         np.random.normal(5000, 1500, n_per).clip(100, 15000),
    'bytes_received':     np.random.normal(8000, 2000, n_per).clip(100, 20000),
    'unique_dest_ports':  np.random.poisson(3, n_per).clip(1, 10),
    'duration_seconds':   np.random.normal(30, 10, n_per).clip(1, 120),
    'failed_connections': np.random.poisson(0.5, n_per),
    'label': 0})
attack = pd.DataFrame({
    'connection_rate':    np.random.normal(80, 25, n_per).clip(10, 250),
    'bytes_sent':         np.random.normal(30000, 15000, n_per).clip(100, 200000),
    'bytes_received':     np.random.normal(2000, 1000, n_per).clip(0, 20000),
    'unique_dest_ports':  np.random.normal(20, 10, n_per).clip(1, 60).astype(int),
    'duration_seconds':   np.random.normal(10, 5, n_per).clip(0.1, 60),
    'failed_connections': np.random.poisson(3, n_per),
    'label': 1})
df = pd.concat([benign, attack], ignore_index=True).sample(frac=1, random_state=42)
FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df[FEATURES].astype(float).values
y = df['label'].values

rng = np.random.default_rng(13)
X = X + rng.normal(0, X.std(axis=0) * 1.5, X.shape)

# Three-way split (Exercise 1) and two-way split (Exercises 3 & 4)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

X_train_all = X_temp  # 80% — used by k-fold CV exercises
y_train_all = y_temp


def save(fig, name):
    path = OUT / name
    fig.savefig(path, **SAVE)
    plt.close(fig)
    print(f"  wrote {name}")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 1 — Overfitting Demo
# ═════════════════════════════════════════════════════════════════════════════

# 1. cv_three_way_split.png — horizontal bar showing 60/20/20 split
fig, ax = plt.subplots(figsize=(11, 2.8))
total = 2000
sizes = [int(total * 0.6), int(total * 0.2), int(total * 0.2)]
labels = ['Train (60%)', 'Validation (20%)', 'Test (20%)']
roles  = ['fit the model', 'tune hyperparameters', 'final evaluation only']
colours = [ACCENT, ORANGE, RED]

start = 0
for n, lab, role, col in zip(sizes, labels, roles, colours):
    ax.barh(0, n, left=start, height=0.55, color=col, edgecolor='white', linewidth=2)
    ax.text(start + n / 2, 0, f'{lab}\n{n} samples',
            ha='center', va='center', color='white', fontsize=11, fontweight='bold')
    ax.text(start + n / 2, -0.55, role,
            ha='center', va='center', color=col, fontsize=10, style='italic')
    start += n

ax.set_xlim(0, total)
ax.set_ylim(-1.2, 0.7)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title('Three-way split: train / validation / test', pad=12)
save(fig, "cv_three_way_split.png")


# Compute the depth sweep used by the next two visuals
depths = np.arange(1, 21)
train_accs, val_accs = [], []
for d in depths:
    m = DecisionTreeClassifier(max_depth=int(d), random_state=42).fit(X_train, y_train)
    train_accs.append(m.score(X_train, y_train))
    val_accs.append(m.score(X_val, y_val))
train_accs = np.array(train_accs)
val_accs   = np.array(val_accs)
best_depth = int(depths[np.argmax(val_accs)])
best_val   = float(val_accs.max())


# 2. cv_overfit_curve.png — train vs val curves with sweet spot
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(depths, train_accs, '-o', color=ACCENT, lw=2.4, markersize=6, label='Train accuracy')
ax.plot(depths, val_accs,   '-s', color=RED,    lw=2.4, markersize=6, label='Validation accuracy')
ax.axvline(best_depth, color=GREEN, linestyle='--', lw=2,
           label=f'Sweet spot — depth={best_depth}')

# Annotate the gap at depth 20
gap = train_accs[-1] - val_accs[-1]
ax.annotate('', xy=(20, train_accs[-1]), xytext=(20, val_accs[-1]),
            arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=2))
ax.text(20.3, (train_accs[-1] + val_accs[-1]) / 2,
        f'Overfit\ngap = {gap:.2f}', va='center', color=ORANGE, fontsize=10)

ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy')
ax.set_title('Overfitting demo: train climbs to 1.0, validation stalls')
ax.set_xticks(depths)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
save(fig, "cv_overfit_curve.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 2 — Bias / Variance Tradeoff
# ═════════════════════════════════════════════════════════════════════════════

# 3. cv_decision_boundaries.png — depth 1 / 5 / 50 boundaries in PCA space
pca = PCA(n_components=2, random_state=42)
X_train_2d = pca.fit_transform(X_train)
X_val_2d   = pca.transform(X_val)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
configs = [(1, 'UNDERFIT', RED), (5, 'GOOD FIT', GREEN), (50, 'OVERFIT', ORANGE)]
for ax, (d, label, edge) in zip(axes, configs):
    m2 = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train_2d, y_train)
    xx, yy = np.meshgrid(
        np.linspace(X_train_2d[:, 0].min() - 0.5, X_train_2d[:, 0].max() + 0.5, 250),
        np.linspace(X_train_2d[:, 1].min() - 0.5, X_train_2d[:, 1].max() + 0.5, 250))
    Z = m2.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.30, levels=[-0.5, 0.5, 1.5],
                colors=[ACCENT, RED])
    ax.scatter(X_val_2d[y_val == 0, 0], X_val_2d[y_val == 0, 1],
               s=8, color=ACCENT, alpha=0.55, edgecolor='none', label='benign')
    ax.scatter(X_val_2d[y_val == 1, 0], X_val_2d[y_val == 1, 1],
               s=8, color=RED, alpha=0.55, edgecolor='none', label='attack')
    acc = m2.score(X_val_2d, y_val)
    ax.set_title(f'depth={d}  ({label})\nval acc={acc:.3f}', color=edge)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(edge); s.set_linewidth(1.6)

fig.suptitle('Decision boundaries in 2-D PCA space', y=1.02)
fig.tight_layout()
save(fig, "cv_decision_boundaries.png")


# 4. cv_learning_curves.png — learning curves for d=1, 5, 50
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=True)
for ax, (d, label, col) in zip(axes, configs):
    m = DecisionTreeClassifier(max_depth=d, random_state=42)
    sizes, tr_scores, va_scores = learning_curve(
        m, X_train_all, y_train_all, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 8), scoring='accuracy')
    tr_mean = tr_scores.mean(axis=1)
    va_mean = va_scores.mean(axis=1)
    tr_std  = tr_scores.std(axis=1)
    va_std  = va_scores.std(axis=1)
    ax.plot(sizes, tr_mean, '-o', color=ACCENT, lw=2.2, label='Train')
    ax.fill_between(sizes, tr_mean - tr_std, tr_mean + tr_std,
                    alpha=0.15, color=ACCENT)
    ax.plot(sizes, va_mean, '-s', color=RED, lw=2.2, label='Validation')
    ax.fill_between(sizes, va_mean - va_std, va_mean + va_std,
                    alpha=0.15, color=RED)
    ax.set_title(f'depth={d}  ({label})', color=col)
    ax.set_xlabel('Training set size')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3)
axes[0].set_ylabel('Accuracy')
fig.suptitle('Learning curves — bias / variance signature per regime', y=1.02)
fig.tight_layout()
save(fig, "cv_learning_curves.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 3 — K-Fold Cross-Validation
# ═════════════════════════════════════════════════════════════════════════════

# 5. cv_kfold_diagram.png — 5-fold layout, each row highlighting that fold's TEST chunk
fig, ax = plt.subplots(figsize=(11, 4.5))
K = 5
chunk_w = 1.0
gap_w = 0.04
row_h = 0.55
row_gap = 0.12

for i in range(K):
    y_pos = (K - 1 - i) * (row_h + row_gap)
    for j in range(K):
        is_test = (j == i)
        col = ORANGE if is_test else ACCENT
        x_pos = j * (chunk_w + gap_w)
        ax.add_patch(Rectangle((x_pos, y_pos), chunk_w, row_h,
                                facecolor=col, edgecolor='white', linewidth=2))
        ax.text(x_pos + chunk_w / 2, y_pos + row_h / 2,
                'TEST' if is_test else 'train',
                ha='center', va='center', color='white',
                fontsize=10, fontweight='bold')
    ax.text(-0.18, y_pos + row_h / 2, f'Fold {i + 1}',
            ha='right', va='center', fontsize=11, fontweight='bold')

# Column labels at bottom
for j in range(K):
    x_pos = j * (chunk_w + gap_w)
    ax.text(x_pos + chunk_w / 2, -0.25, f'Chunk {j + 1}',
            ha='center', va='top', fontsize=10, color=GREY)

ax.set_xlim(-0.5, K * (chunk_w + gap_w) + 0.1)
ax.set_ylim(-0.6, K * (row_h + row_gap))
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title('5-fold cross-validation: every chunk is the test set exactly once')
save(fig, "cv_kfold_diagram.png")


# 6. cv_single_vs_kfold.png — single split vs 5-fold and 10-fold CV with fold scores
m_demo = DecisionTreeClassifier(max_depth=5, random_state=42)
m_demo.fit(X_train_all, y_train_all)
single_score = m_demo.score(X_test, y_test)

cv5 = cross_val_score(DecisionTreeClassifier(max_depth=5, random_state=42),
                      X_train_all, y_train_all, cv=5)
cv10 = cross_val_score(DecisionTreeClassifier(max_depth=5, random_state=42),
                       X_train_all, y_train_all, cv=10)

fig, ax = plt.subplots(figsize=(9.5, 5.2))
positions = [0, 1.6, 3.2]
ax.bar([positions[0]], [single_score], width=0.55, color=GREY, edgecolor='white',
       label='single split (one number)')
ax.text(positions[0], single_score + 0.005, f'{single_score:.3f}',
        ha='center', va='bottom', fontsize=10, color=GREY)

# 5-fold: bar = mean, errorbar = std, dots = individual folds
ax.bar([positions[1]], [cv5.mean()], width=0.55,
       color=ACCENT, edgecolor='white', alpha=0.85,
       yerr=[cv5.std()], capsize=8, ecolor=ORANGE,
       label='5-fold CV (mean ± std)')
ax.scatter([positions[1]] * len(cv5), cv5, s=42, color='white',
           edgecolor=ACCENT, linewidth=1.6, zorder=5)
ax.text(positions[1], cv5.mean() + cv5.std() + 0.005,
        f'{cv5.mean():.3f} ± {cv5.std():.3f}',
        ha='center', va='bottom', fontsize=10, color=ACCENT)

ax.bar([positions[2]], [cv10.mean()], width=0.55,
       color=VIOLET, edgecolor='white', alpha=0.85,
       yerr=[cv10.std()], capsize=8, ecolor=ORANGE,
       label='10-fold CV (mean ± std)')
ax.scatter([positions[2]] * len(cv10), cv10, s=42, color='white',
           edgecolor=VIOLET, linewidth=1.6, zorder=5)
ax.text(positions[2], cv10.mean() + cv10.std() + 0.005,
        f'{cv10.mean():.3f} ± {cv10.std():.3f}',
        ha='center', va='bottom', fontsize=10, color=VIOLET)

ax.set_xticks(positions)
ax.set_xticklabels(['Single 80/20', '5-fold CV', '10-fold CV'])
ax.set_ylabel('Accuracy (depth=5)')
ax.set_ylim(0.7, max(cv10.mean() + cv10.std(), single_score) + 0.05)
ax.set_title('Single split gives one number; CV gives a distribution')
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3, axis='y')
save(fig, "cv_single_vs_kfold.png")


# 7. cv_depth_sweep.png — 5-fold CV mean ± std vs depth
ds = np.arange(1, 16)
cv_means, cv_stds = [], []
for d in ds:
    s = cross_val_score(DecisionTreeClassifier(max_depth=int(d), random_state=42),
                        X_train_all, y_train_all, cv=5)
    cv_means.append(s.mean())
    cv_stds.append(s.std())
cv_means = np.array(cv_means)
cv_stds  = np.array(cv_stds)
best_cv_depth = int(ds[np.argmax(cv_means)])

fig, ax = plt.subplots(figsize=(10, 5.4))
ax.plot(ds, cv_means, '-o', color=ACCENT, lw=2.4, markersize=7, label='5-fold CV mean')
ax.fill_between(ds, cv_means - cv_stds, cv_means + cv_stds,
                alpha=0.20, color=ACCENT, label='± 1 std')
ax.axvline(best_cv_depth, color=GREEN, linestyle='--', lw=2,
           label=f'Best depth = {best_cv_depth}')
ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy (5-fold CV)')
ax.set_title('Cross-validated accuracy vs depth — picks the same sweet spot, with confidence')
ax.set_xticks(ds)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
save(fig, "cv_depth_sweep.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 4 — Validation Curve
# ═════════════════════════════════════════════════════════════════════════════

# Compute validation_curve over depths with std bands
param_range = np.arange(1, 21)
tr_scores, va_scores = validation_curve(
    DecisionTreeClassifier(random_state=42),
    X_train_all, y_train_all,
    param_name='max_depth', param_range=param_range, cv=5, scoring='accuracy')
tr_mean = tr_scores.mean(axis=1); tr_std = tr_scores.std(axis=1)
va_mean = va_scores.mean(axis=1); va_std = va_scores.std(axis=1)
best_vc_depth = int(param_range[np.argmax(va_mean)])

# 8. cv_validation_curve.png — train and val with std bands
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(param_range, tr_mean, '-o', color=ACCENT, lw=2.4, label='Train (CV mean)')
ax.fill_between(param_range, tr_mean - tr_std, tr_mean + tr_std, alpha=0.2, color=ACCENT)
ax.plot(param_range, va_mean, '-s', color=RED, lw=2.4, label='Validation (CV mean)')
ax.fill_between(param_range, va_mean - va_std, va_mean + va_std, alpha=0.2, color=RED)
ax.axvline(best_vc_depth, color=GREEN, linestyle='--', lw=2,
           label=f'Best depth = {best_vc_depth}')
ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy')
ax.set_title('validation_curve(): train and validation with ±1 std bands')
ax.set_xticks(param_range)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
save(fig, "cv_validation_curve.png")


# 9. cv_three_regions.png — same curve, annotated underfit / sweet / overfit
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(param_range, tr_mean, '-o', color=ACCENT, lw=2.4, label='Train')
ax.plot(param_range, va_mean, '-s', color=RED,    lw=2.4, label='Validation')

# Background shading
ax.axvspan(0.5, 2.5,  alpha=0.10, color=RED)
ax.axvspan(2.5, 9.5,  alpha=0.10, color=GREEN)
ax.axvspan(9.5, 20.5, alpha=0.10, color=ORANGE)

ax.text(1.5, 1.02, 'UNDERFIT\n(high bias)', ha='center', fontsize=10, color=RED, fontweight='bold')
ax.text(6.0, 1.02, 'SWEET SPOT', ha='center', fontsize=10, color=GREEN, fontweight='bold')
ax.text(15.0, 1.02, 'OVERFIT\n(high variance)', ha='center', fontsize=10, color=ORANGE, fontweight='bold')

ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy')
ax.set_title('Three regions of the validation curve')
ax.set_xticks(param_range)
ax.set_ylim(va_mean.min() - 0.05, 1.10)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
save(fig, "cv_three_regions.png")


# 10. cv_rf_validation_curve.png — RF n_estimators sweep, plateau
rf_range = [5, 10, 25, 50, 75, 100, 150, 200, 300]
tr_rf, va_rf = validation_curve(
    RandomForestClassifier(random_state=42),
    X_train_all, y_train_all,
    param_name='n_estimators', param_range=rf_range, cv=5, scoring='accuracy')
tr_rf_mean = tr_rf.mean(axis=1)
va_rf_mean = va_rf.mean(axis=1)
va_rf_std  = va_rf.std(axis=1)

fig, ax = plt.subplots(figsize=(9.5, 5))
ax.plot(rf_range, tr_rf_mean, '-o', color=ACCENT, lw=2.4, label='Train')
ax.plot(rf_range, va_rf_mean, '-s', color=RED, lw=2.4, label='Validation')
ax.fill_between(rf_range, va_rf_mean - va_rf_std, va_rf_mean + va_rf_std,
                alpha=0.2, color=RED)
ax.axhline(va_rf_mean[-1], color=GREEN, linestyle=':', lw=1.6,
           label=f'Plateau ≈ {va_rf_mean[-1]:.3f}')
ax.set_xlabel('n_estimators')
ax.set_ylabel('Accuracy')
ax.set_title('Random Forest validation curve — climbs, then plateaus, never drops')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
save(fig, "cv_rf_validation_curve.png")


print("\n10 overfitting / cross-validation visuals written to portal/static/lecture_assets/")
print(f"  best depth (single split):  {best_depth} (val={best_val:.3f})")
print(f"  best depth (5-fold CV):     {best_cv_depth} ({cv_means.max():.3f})")
print(f"  best depth (validation_curve): {best_vc_depth} ({va_mean.max():.3f})")
print(f"  single split vs CV: {single_score:.3f} vs {cv5.mean():.3f} ± {cv5.std():.3f}")
