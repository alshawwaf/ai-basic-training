"""
Generate visuals for the four Clustering & Anomaly Detection lectures (Stage 2.3).
    python portal/static/lecture_assets/_generate_clustering_anomaly.py

Reproduces the synthetic 4-class network traffic dataset (3 000 samples,
6 features) and runs the same K-Means / scoring pipeline the four
solution_*.py files do, with sigma=0.8 noise on scaled features.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples

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

# ── Reproduce the lab dataset (matches every Stage 2.3 solution) ─────────────
np.random.seed(42)
n_per = 750

def make_full_dataset():
    benign = pd.DataFrame({
        'connection_rate':    np.random.normal(10, 3, n_per).clip(1, 25),
        'bytes_sent':         np.random.normal(5000, 1500, n_per).clip(100, 15000),
        'bytes_received':     np.random.normal(8000, 2000, n_per).clip(100, 20000),
        'unique_dest_ports':  np.random.poisson(3, n_per).clip(1, 10),
        'duration_seconds':   np.random.normal(30, 10, n_per).clip(1, 120),
        'failed_connections': np.random.poisson(0.5, n_per),
        'true_label': 0, 'true_class': 'benign'})
    port_scan = pd.DataFrame({
        'connection_rate':    np.random.normal(25, 8, n_per).clip(5, 60),
        'bytes_sent':         np.random.normal(500, 200, n_per).clip(50, 2000),
        'bytes_received':     np.random.normal(300, 100, n_per).clip(0, 1000),
        'unique_dest_ports':  np.random.normal(45, 10, n_per).clip(20, 100).astype(int),
        'duration_seconds':   np.random.normal(5, 2, n_per).clip(1, 20),
        'failed_connections': np.random.poisson(8, n_per),
        'true_label': 1, 'true_class': 'port_scan'})
    exfil = pd.DataFrame({
        'connection_rate':    np.random.normal(8, 2, n_per).clip(1, 20),
        'bytes_sent':         np.random.normal(80000, 25000, n_per).clip(20000, 250000),
        'bytes_received':     np.random.normal(1000, 300, n_per).clip(100, 5000),
        'unique_dest_ports':  np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds':   np.random.normal(180, 60, n_per).clip(60, 600),
        'failed_connections': np.random.poisson(0.2, n_per),
        'true_label': 2, 'true_class': 'exfil'})
    dos = pd.DataFrame({
        'connection_rate':    np.random.normal(200, 40, n_per).clip(80, 500),
        'bytes_sent':         np.random.normal(200, 80, n_per).clip(40, 600),
        'bytes_received':     np.random.normal(100, 40, n_per).clip(0, 400),
        'unique_dest_ports':  np.random.poisson(2, n_per).clip(1, 5),
        'duration_seconds':   np.random.normal(0.5, 0.2, n_per).clip(0.1, 2),
        'failed_connections': np.random.poisson(3, n_per),
        'true_label': 3, 'true_class': 'DoS'})
    return pd.concat([benign, port_scan, exfil, dos],
                     ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

df = make_full_dataset()
FEATURES = ['connection_rate', 'bytes_sent', 'bytes_received',
            'unique_dest_ports', 'duration_seconds', 'failed_connections']
X = df[FEATURES].astype(float).values
true_labels  = df['true_label'].values
true_classes = df['true_class'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
rng = np.random.default_rng(13)
X_scaled = X_scaled + rng.normal(0, 0.8, X_scaled.shape)

# 2-D PCA projection used by every cluster scatter plot
pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X_scaled)

# K=4 clustering used by lectures 2 & 4
km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = km4.fit_predict(X_scaled)
centroids_2d = pca.transform(km4.cluster_centers_)

CLASS_COLOURS = {'benign': ACCENT, 'port_scan': ORANGE, 'exfil': GREEN, 'DoS': RED}
CLASS_ORDER   = ['benign', 'port_scan', 'exfil', 'DoS']


def save(fig, name):
    path = OUT / name
    fig.savefig(path, **SAVE)
    plt.close(fig)
    print(f"  wrote {name}")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 1 — Unsupervised Framing
# ═════════════════════════════════════════════════════════════════════════════

# 1. cluster_no_labels.png — what an analyst actually sees: a grey blob
fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.scatter(X_2d[:, 0], X_2d[:, 1], s=10, color=GREY, alpha=0.45, edgecolor='none')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_title('What the analyst sees: 3 000 connections, no labels')
ax.text(0.02, 0.97, "No colours.\nNo classes.\nJust shape.",
        transform=ax.transAxes, va='top', ha='left',
        fontsize=11, color=GREY,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=LIGHT))
ax.set_xticks([]); ax.set_yticks([])
save(fig, "cluster_no_labels.png")


# 2. cluster_truth_revealed.png — same plot, real labels exposed
fig, ax = plt.subplots(figsize=(7.5, 5.5))
for cls in CLASS_ORDER:
    mask = true_classes == cls
    ax.scatter(X_2d[mask, 0], X_2d[mask, 1], s=12, alpha=0.55,
               color=CLASS_COLOURS[cls], label=cls, edgecolor='none')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_title('Truth revealed: four traffic types occupy four regions')
ax.legend(loc='best', framealpha=0.9)
ax.set_xticks([]); ax.set_yticks([])
save(fig, "cluster_truth_revealed.png")


# 3. cluster_attack_signatures.png — small multiples: signature feature per class
fig, axes = plt.subplots(1, 4, figsize=(13, 3.6), sharey=False)
sig_features = [
    ('benign',    'bytes_sent',         'Bytes sent (B)',    None),
    ('port_scan', 'unique_dest_ports',  'Unique dest ports', None),
    ('exfil',     'bytes_sent',         'Bytes sent (B)',    'log'),
    ('DoS',       'connection_rate',    'Conn / sec',        None),
]
for ax, (cls, feat, label, scale) in zip(axes, sig_features):
    for c in CLASS_ORDER:
        mask = true_classes == c
        is_focus = (c == cls)
        ax.hist(df.loc[mask, feat],
                bins=30, alpha=0.85 if is_focus else 0.35,
                color=CLASS_COLOURS[c] if is_focus else LIGHT,
                edgecolor='none', label=c if is_focus else None)
    ax.set_title(f'{cls}\nsignature: {feat}', fontsize=11, color=CLASS_COLOURS[cls])
    ax.set_xlabel(label)
    if scale:
        ax.set_xscale(scale)
    ax.set_yticks([])
fig.suptitle('Each attack type stands out on a different feature', y=1.02)
fig.tight_layout()
save(fig, "cluster_attack_signatures.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 2 — K-Means and Visualisation
# ═════════════════════════════════════════════════════════════════════════════

# 4. cluster_kmeans_iterations.png — show K-Means converging on a 2-D toy
toy_rng = np.random.default_rng(7)
toy_blobs = []
for cx, cy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
    toy_blobs.append(toy_rng.normal(loc=[cx, cy], scale=1.1, size=(60, 2)))
toy = np.vstack(toy_blobs)

# Fixed initial centroids that are deliberately bad
init_centroids = np.array([[-4, 0], [4, 0], [0, -4], [0, 4]], dtype=float)

def kmeans_step(points, centroids):
    d = np.linalg.norm(points[:, None, :] - centroids[None, :, :], axis=2)
    labels = d.argmin(axis=1)
    new_centroids = np.array([points[labels == k].mean(axis=0)
                              if (labels == k).any() else centroids[k]
                              for k in range(len(centroids))])
    return labels, new_centroids

palette = [ACCENT, ORANGE, GREEN, RED]
centroids = init_centroids.copy()
fig, axes = plt.subplots(1, 4, figsize=(13.5, 3.6), sharex=True, sharey=True)
for it, ax in enumerate(axes):
    labels, new_centroids = kmeans_step(toy, centroids)
    for k in range(4):
        m = labels == k
        ax.scatter(toy[m, 0], toy[m, 1], s=22, color=palette[k], alpha=0.7,
                   edgecolor='none')
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=220,
               c='black', edgecolor='white', linewidth=1.6, zorder=5)
    ax.set_title(f'Iteration {it}')
    ax.set_xticks([]); ax.set_yticks([])
    centroids = new_centroids
fig.suptitle('K-Means: assign → recompute → assign → converge', y=1.04)
fig.tight_layout()
save(fig, "cluster_kmeans_iterations.png")


# 5. cluster_kmeans_pca.png — real lab clusters in PCA space with centroids
fig, ax = plt.subplots(figsize=(8.5, 6))
for c in range(4):
    mask = cluster_labels == c
    ax.scatter(X_2d[mask, 0], X_2d[mask, 1], s=12, alpha=0.55,
               color=palette[c], label=f'Cluster {c}', edgecolor='none')
ax.scatter(centroids_2d[:, 0], centroids_2d[:, 1],
           marker='X', s=240, c='black', edgecolor='white',
           linewidth=1.6, zorder=10, label='Centroid')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_title('K-Means K=4 — clusters in 2-D PCA space')
ax.legend(loc='best', framealpha=0.9)
ax.set_xticks([]); ax.set_yticks([])
save(fig, "cluster_kmeans_pca.png")


# 6. cluster_purity_grid.png — heatmap rows=cluster, cols=true class
purity_grid = np.zeros((4, 4), dtype=int)
for c in range(4):
    for j, cls in enumerate(CLASS_ORDER):
        purity_grid[c, j] = np.sum((cluster_labels == c) & (true_classes == cls))

# Re-order rows so the dominant class lines up on the diagonal where possible.
row_order = []
remaining_cls = list(range(4))
for c in range(4):
    dom = np.argmax(purity_grid[c])
    row_order.append(c)
labelled_rows = []
for c in row_order:
    dom = CLASS_ORDER[np.argmax(purity_grid[c])]
    labelled_rows.append(f'C{c}\n→ {dom}')

fig, ax = plt.subplots(figsize=(7.5, 5.5))
im = ax.imshow(purity_grid, cmap='Blues', aspect='auto')
ax.set_xticks(range(4))
ax.set_xticklabels(CLASS_ORDER, rotation=20)
ax.set_yticks(range(4))
ax.set_yticklabels(labelled_rows)
ax.set_xlabel('True class')
ax.set_ylabel('K-Means cluster')
ax.set_title('Cluster purity grid — counts of each class per cluster')
for i in range(4):
    for j in range(4):
        v = purity_grid[i, j]
        ax.text(j, i, str(v), ha='center', va='center',
                color='white' if v > purity_grid.max() * 0.55 else 'black',
                fontsize=11, fontweight='bold')
fig.colorbar(im, ax=ax, fraction=0.04)
save(fig, "cluster_purity_grid.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 3 — Choosing K
# ═════════════════════════════════════════════════════════════════════════════

# Compute elbow + silhouette curves
ks = list(range(2, 11))
inertias = []
sils = []
for k in ks:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X_scaled, labels, sample_size=1000, random_state=42))

# 7. cluster_elbow_curve.png — inertia vs K with elbow at 4
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ks, inertias, '-o', color=ACCENT, lw=2.5, markersize=9)
ax.axvline(4, color=ORANGE, linestyle='--', lw=2, label='Elbow at K=4')
ax.set_xlabel('K (number of clusters)')
ax.set_ylabel('Inertia (within-cluster sum of squares)')
ax.set_title('Elbow method — inertia drops sharply, then flattens at K=4')
ax.set_xticks(ks)
ax.legend()
ax.grid(True, alpha=0.3)
# Annotate the actual numbers
for k, v in zip(ks, inertias):
    if k <= 5:
        ax.annotate(f'{v:.0f}', (k, v), textcoords="offset points",
                    xytext=(8, 8), fontsize=9, color=GREY)
save(fig, "cluster_elbow_curve.png")


# 8. cluster_silhouette_curve.png — silhouette score vs K with peak at K=4
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ks, sils, '-s', color=VIOLET, lw=2.5, markersize=9)
peak = int(np.argmax(sils))
ax.scatter([ks[peak]], [sils[peak]], s=220, facecolor='none',
           edgecolor=ORANGE, linewidth=2.5, zorder=5,
           label=f'Peak at K={ks[peak]} ({sils[peak]:.3f})')
ax.set_xlabel('K (number of clusters)')
ax.set_ylabel('Silhouette score (higher is better)')
ax.set_title('Silhouette score — separation peaks where domain knowledge expects it')
ax.set_xticks(ks)
ax.legend()
ax.grid(True, alpha=0.3)
save(fig, "cluster_silhouette_curve.png")


# 9. cluster_silhouette_diagram.png — per-sample silhouette bars grouped by cluster
sample_idx = np.random.choice(len(X_scaled), 600, replace=False)
X_samp = X_scaled[sample_idx]
labels4 = cluster_labels[sample_idx]
sil_vals = silhouette_samples(X_samp, labels4)
mean_sil = sil_vals.mean()

fig, ax = plt.subplots(figsize=(8.5, 5.5))
y_lower = 0
for c in range(4):
    cluster_sil = np.sort(sil_vals[labels4 == c])
    size_c = len(cluster_sil)
    y_upper = y_lower + size_c
    ax.barh(np.arange(y_lower, y_upper), cluster_sil, height=1.0,
            color=palette[c], alpha=0.85, edgecolor='none')
    ax.text(-0.04, y_lower + size_c / 2, f'C{c}', fontsize=10,
            va='center', ha='right', color=palette[c], fontweight='bold')
    y_lower = y_upper + 8

ax.axvline(mean_sil, color='black', linestyle='--', lw=1.6,
           label=f'Mean silhouette = {mean_sil:.2f}')
ax.set_xlabel('Silhouette coefficient')
ax.set_ylabel('Samples (sorted within each cluster)')
ax.set_title('Silhouette diagram for K=4 — wide bands, most bars on the right')
ax.set_yticks([])
ax.legend(loc='lower right')
save(fig, "cluster_silhouette_diagram.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 4 — Anomaly Scoring
# ═════════════════════════════════════════════════════════════════════════════

# 10. cluster_distance_concept.png — diagram: point-to-nearest-centroid
fig, ax = plt.subplots(figsize=(8, 5.5))
toy_rng2 = np.random.default_rng(11)
norm_pts  = toy_rng2.normal(loc=[2, 2], scale=0.6, size=(50, 2))
norm_pts2 = toy_rng2.normal(loc=[-2, -1], scale=0.7, size=(45, 2))
ax.scatter(norm_pts[:, 0],  norm_pts[:, 1],  s=22, color=ACCENT, alpha=0.6, edgecolor='none')
ax.scatter(norm_pts2[:, 0], norm_pts2[:, 1], s=22, color=VIOLET, alpha=0.6, edgecolor='none')

centroid_a = np.array([2.0, 2.0])
centroid_b = np.array([-2.0, -1.0])
ax.scatter(*centroid_a, marker='X', s=320, c='black', edgecolor='white', lw=1.6, zorder=10)
ax.scatter(*centroid_b, marker='X', s=320, c='black', edgecolor='white', lw=1.6, zorder=10)
ax.text(centroid_a[0] + 0.15, centroid_a[1] + 0.15, 'centroid A', fontsize=10)
ax.text(centroid_b[0] + 0.15, centroid_b[1] + 0.15, 'centroid B', fontsize=10)

# A "normal" point with a short arrow to its centroid
normal_pt = np.array([1.6, 2.4])
ax.scatter(*normal_pt, s=90, color=GREEN, edgecolor='black', lw=1.2, zorder=8)
ax.annotate('', xy=centroid_a, xytext=normal_pt,
            arrowprops=dict(arrowstyle='-', color=GREEN, lw=2))
ax.text(1.85, 2.7, 'normal\nshort distance', fontsize=10, color=GREEN)

# An "anomaly" far from both
anomaly_pt = np.array([4.5, -2.0])
ax.scatter(*anomaly_pt, s=140, color=RED, edgecolor='black', lw=1.4, zorder=8, marker='*')
ax.annotate('', xy=centroid_a, xytext=anomaly_pt,
            arrowprops=dict(arrowstyle='-', color=RED, lw=2, linestyle='--'))
ax.text(4.6, -1.6, 'anomaly\nfar from every centroid', fontsize=10, color=RED)

ax.set_xlim(-5, 6.5)
ax.set_ylim(-4, 4.5)
ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Anomaly score = distance to nearest centroid')
save(fig, "cluster_distance_concept.png")


# 11. cluster_anomaly_histogram.png — real lab histogram with threshold + TP/FP
distances = km4.transform(X_scaled)
anomaly_scores = distances.min(axis=1)
threshold = np.percentile(anomaly_scores, 95)
flagged = anomaly_scores > threshold
is_attack = true_labels != 0
tp = int((flagged & is_attack).sum())
fp = int((flagged & ~is_attack).sum())
recall = tp / int(is_attack.sum())
precision = tp / int(flagged.sum())

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.hist(anomaly_scores[~flagged], bins=60, color=ACCENT, alpha=0.75,
        edgecolor='none', label='Below threshold (kept)')
ax.hist(anomaly_scores[flagged], bins=20, color=RED, alpha=0.85,
        edgecolor='none', label='Flagged anomalies (top 5%)')
ax.axvline(threshold, color='black', linestyle='--', lw=1.8,
           label=f'95th percentile = {threshold:.2f}')
ax.set_xlabel('Anomaly score (distance to nearest centroid)')
ax.set_ylabel('Connection count')
ax.set_title('Anomaly score distribution — top 5% gets reviewed')
ax.legend(loc='upper right')
ax.text(0.02, 0.97,
        f'Flagged: {flagged.sum()} / {len(flagged)}\n'
        f'True positives: {tp}\n'
        f'Precision: {precision:.0%}\n'
        f'Recall: {recall:.1%}',
        transform=ax.transAxes, va='top', ha='left',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=LIGHT))
save(fig, "cluster_anomaly_histogram.png")


# 12. cluster_pr_recall_tradeoff.png — sweep threshold percentile, plot P/R
percentiles = np.arange(80, 99.5, 0.5)
pr, rc = [], []
for p in percentiles:
    t = np.percentile(anomaly_scores, p)
    f = anomaly_scores > t
    if f.sum() == 0:
        pr.append(np.nan); rc.append(0)
    else:
        pr.append((f & is_attack).sum() / f.sum())
        rc.append((f & is_attack).sum() / is_attack.sum())

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(percentiles, pr, '-o', color=ACCENT, label='Precision', markersize=5)
ax.plot(percentiles, rc, '-s', color=ORANGE, label='Recall',    markersize=5)
ax.axvline(95, color='black', linestyle='--', lw=1.4, label='Default threshold (95th pct)')
ax.set_xlabel('Threshold percentile of anomaly score')
ax.set_ylabel('Score')
ax.set_title('Threshold tuning — precision stays high, recall stays painfully low')
ax.legend(loc='center right')
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)
save(fig, "cluster_pr_recall_tradeoff.png")


print("\n12 clustering / anomaly visuals written to portal/static/lecture_assets/")
