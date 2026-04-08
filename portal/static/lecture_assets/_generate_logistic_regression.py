"""
Generate visuals for the four Logistic Regression lectures (Stage 1.3).
    python portal/static/lecture_assets/_generate_logistic_regression.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score, f1_score,
    precision_recall_curve,
)

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED = "#dc2626"
ORANGE = "#f59e0b"
GREEN = "#16a34a"


# ── Build the lab dataset (matches solution_feature_engineering_urls.py) ──
np.random.seed(42)
n = 1000
half = n // 2

legit = pd.DataFrame({
    'url_length':     np.random.normal(45, 12, half).clip(10, 100).astype(int),
    'num_dots':       np.random.poisson(2.1, half),
    'has_at_symbol':  (np.random.rand(half) < 0.05).astype(int),
    'uses_https':     (np.random.rand(half) < 0.82).astype(int),
    'num_subdomains': np.random.poisson(0.8, half),
    'has_ip_address': (np.random.rand(half) < 0.02).astype(int),
    'num_hyphens':    np.random.poisson(0.3, half),
    'path_length':    np.random.normal(15, 8, half).clip(0, 60).astype(int),
    'is_phishing':    0,
})
phish = pd.DataFrame({
    'url_length':     np.random.normal(98, 25, half).clip(30, 250).astype(int),
    'num_dots':       np.random.poisson(4.8, half),
    'has_at_symbol':  (np.random.rand(half) < 0.31).astype(int),
    'uses_https':     (np.random.rand(half) < 0.61).astype(int),
    'num_subdomains': np.random.poisson(2.5, half),
    'has_ip_address': (np.random.rand(half) < 0.21).astype(int),
    'num_hyphens':    np.random.poisson(2.1, half),
    'path_length':    np.random.normal(48, 18, half).clip(0, 150).astype(int),
    'is_phishing':    1,
})
df = pd.concat([legit, phish], ignore_index=True).sample(frac=1, random_state=42)

FEATURES = ['url_length', 'num_dots', 'has_at_symbol', 'uses_https',
            'num_subdomains', 'has_ip_address', 'num_hyphens', 'path_length']
X = df[FEATURES].values
y = df['is_phishing'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000).fit(X_train_s, y_train)


# ── 1. Linear regression fails for classification ─────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.4))
np.random.seed(11)
short_lengths = np.random.uniform(15, 60, 10)
long_lengths = np.random.uniform(80, 220, 10)
labels = np.array([0] * 10 + [1] * 10)
xs = np.concatenate([short_lengths, long_lengths]).reshape(-1, 1)

linreg = LinearRegression().fit(xs, labels)
xline = np.linspace(0, 250, 200).reshape(-1, 1)
yline = linreg.predict(xline)

ax.scatter(xs[labels == 0], labels[labels == 0],
           color=ACCENT, s=80, edgecolor="#055e76", linewidth=1.2,
           label="legitimate (0)", zorder=4)
ax.scatter(xs[labels == 1], labels[labels == 1],
           color=RED, s=80, edgecolor="#7f1d1d", linewidth=1.2,
           label="phishing (1)", zorder=4)
ax.plot(xline, yline, color=VIOLET, linewidth=2.5,
        label="LinearRegression fit")
ax.axhline(0, color="#888", linewidth=0.8)
ax.axhline(1, color="#888", linewidth=0.8)
ax.fill_between(xline.flatten(), yline.flatten(), 0,
                where=(yline.flatten() < 0), color=RED, alpha=0.15)
ax.fill_between(xline.flatten(), yline.flatten(), 1,
                where=(yline.flatten() > 1), color=RED, alpha=0.15)
# Annotate the bad regions
ax.annotate("predicts < 0\n(invalid!)", xy=(10, -0.15), xytext=(20, -0.45),
            ha="center", fontsize=9, color=RED, family="monospace", weight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.annotate("predicts > 1\n(invalid!)", xy=(230, 1.15), xytext=(220, 1.45),
            ha="center", fontsize=9, color=RED, family="monospace", weight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.set_xlabel("url_length", family="monospace")
ax.set_ylabel("predicted label", family="monospace")
ax.set_title("LinearRegression on a binary target — output escapes [0, 1]",
             fontsize=11, family="monospace")
ax.set_ylim(-0.7, 1.7)
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "logreg_linear_fails.png", **SAVE)
plt.close(fig)


# ── 2. The sigmoid curve ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.4))
z = np.linspace(-8, 8, 400)
sig = 1 / (1 + np.exp(-z))
ax.plot(z, sig, color=ACCENT, linewidth=3, zorder=3)
ax.axhline(0.5, color="#888", linestyle="--", linewidth=1, label="threshold = 0.5")
ax.axvline(0, color="#888", linestyle="--", linewidth=1)

# Decision regions
ax.fill_between(z, 0, 1, where=(z < 0), color=ACCENT, alpha=0.1)
ax.fill_between(z, 0, 1, where=(z >= 0), color=RED, alpha=0.1)

# Marker dots
for zi in [-5, -2, 0, 2, 5]:
    pi = 1 / (1 + np.exp(-zi))
    ax.plot(zi, pi, "o", color=VIOLET, markersize=10,
            markeredgecolor="#5b21b6", markeredgewidth=1.2, zorder=5)
    ax.text(zi, pi + 0.06, f"{pi:.2f}", ha="center", fontsize=8,
            family="monospace", color=VIOLET, weight="bold")

ax.text(-6.5, 0.78, "predict\nlegitimate (0)", ha="center", fontsize=10,
        family="monospace", color=ACCENT, weight="bold")
ax.text(6.5, 0.22, "predict\nphishing (1)", ha="center", fontsize=10,
        family="monospace", color=RED, weight="bold")

ax.set_xlabel("z  (linear score = w·x + b)", family="monospace")
ax.set_ylabel("σ(z)  (probability)", family="monospace")
ax.set_title("Sigmoid function — squashes any real number into (0, 1)",
             fontsize=11, family="monospace")
ax.set_ylim(-0.05, 1.15)
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "logreg_sigmoid.png", **SAVE)
plt.close(fig)


# ── 3. Class balance bar (50/50) ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3.4))
counts = df['is_phishing'].value_counts().sort_index()
ax.bar(["legitimate", "phishing"], counts.values,
       color=[ACCENT, RED], edgecolor="#222", linewidth=1)
for i, v in enumerate(counts.values):
    ax.text(i, v + 8, f"{v}", ha="center", fontsize=11, family="monospace")
ax.set_ylabel("rows", family="monospace")
ax.set_title("Synthetic phishing dataset — 50/50 split (n=1000)",
             fontsize=11, family="monospace")
ax.set_ylim(0, max(counts.values) * 1.18)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "logreg_class_balance.png", **SAVE)
plt.close(fig)


# ── 4. Feature distribution histograms ────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
plot_features = ['url_length', 'num_dots', 'num_subdomains', 'path_length']
for ax, feat in zip(axes.flat, plot_features):
    df[df['is_phishing'] == 0][feat].hist(
        ax=ax, bins=20, alpha=0.55, color=ACCENT,
        edgecolor="#055e76", linewidth=0.4, label='legitimate')
    df[df['is_phishing'] == 1][feat].hist(
        ax=ax, bins=20, alpha=0.55, color=RED,
        edgecolor="#7f1d1d", linewidth=0.4, label='phishing')
    ax.set_title(feat, fontsize=10, family="monospace")
    ax.legend(fontsize=8, framealpha=0.9)
    ax.grid(alpha=0.3)
fig.suptitle("Feature distributions split by class — well-separated = predictive",
             fontsize=11, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "logreg_feature_distributions.png", **SAVE)
plt.close(fig)


# ── 5. Confusion matrix on the trained model ──────────────────────────────
y_pred = model.predict(X_test_s)
cm = confusion_matrix(y_test, y_pred)
TN, FP, FN, TP = cm.ravel()

fig, ax = plt.subplots(figsize=(5.6, 5))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["predicted: legit", "predicted: phishing"],
                   family="monospace", fontsize=9)
ax.set_yticklabels(["actual: legit", "actual: phishing"],
                   family="monospace", fontsize=9)
labels = [
    [f"TN\n{TN}", f"FP\n{FP}"],
    [f"FN\n{FN}", f"TP\n{TP}"],
]
for i in range(2):
    for j in range(2):
        v = cm[i, j]
        color = "white" if v > cm.max() * 0.55 else "#222"
        label_color = color
        if i == 1 and j == 0 and FN > 0:
            label_color = RED
        ax.text(j, i, labels[i][j], ha="center", va="center",
                fontsize=14, color=label_color, family="monospace", weight="bold")
ax.set_title(f"Logistic regression confusion matrix\n"
             f"acc={(TP+TN)/cm.sum():.2f}   "
             f"recall={TP/(TP+FN):.2f}   "
             f"precision={TP/(TP+FP):.2f}",
             fontsize=10, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "logreg_confusion_matrix.png", **SAVE)
plt.close(fig)


# ── 6. Coefficients bar chart ─────────────────────────────────────────────
coefs = model.coef_[0]
order = np.argsort(coefs)
fig, ax = plt.subplots(figsize=(8, 4.2))
colors = [RED if c > 0 else ACCENT for c in coefs[order]]
ax.barh([FEATURES[i] for i in order], coefs[order],
        color=colors, edgecolor="#222", linewidth=0.6)
ax.axvline(0, color="#222", linewidth=1)
ax.set_xlabel("coefficient (sign = direction, magnitude = strength)",
              family="monospace")
ax.set_title("Logistic regression coefficients — what drives the prediction",
             fontsize=10, family="monospace")
ax.grid(axis="x", alpha=0.3)
# Legend
from matplotlib.patches import Patch
legend_elems = [
    Patch(facecolor=RED, label="positive  -  pushes toward phishing"),
    Patch(facecolor=ACCENT, label="negative  -  pushes toward legitimate"),
]
ax.legend(handles=legend_elems, loc="lower right", fontsize=8, framealpha=0.95)
plt.tight_layout()
plt.savefig(OUT / "logreg_coefficients.png", **SAVE)
plt.close(fig)


# ── 7. Probability histogram split by true class ──────────────────────────
probs = model.predict_proba(X_test_s)[:, 1]
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(probs[y_test == 0], bins=25, alpha=0.6, color=ACCENT,
        edgecolor="#055e76", linewidth=0.4, label="actual legit")
ax.hist(probs[y_test == 1], bins=25, alpha=0.6, color=RED,
        edgecolor="#7f1d1d", linewidth=0.4, label="actual phishing")
ax.axvline(0.5, color="#222", linestyle="--", linewidth=2, label="default threshold = 0.5")
ax.set_xlabel("predict_proba()[:, 1]   (predicted probability of phishing)",
              family="monospace", fontsize=9)
ax.set_ylabel("count", family="monospace", fontsize=9)
ax.set_title("predict_proba() output split by true class",
             fontsize=11, family="monospace")
ax.legend(loc="upper center", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "logreg_proba_hist.png", **SAVE)
plt.close(fig)


# ── 8. Threshold sweep — precision/recall vs threshold ────────────────────
thresholds_to_show = np.linspace(0.05, 0.95, 19)
prec_list, rec_list, f1_list, flagged_list = [], [], [], []
for t in thresholds_to_show:
    pred = (probs >= t).astype(int)
    prec_list.append(precision_score(y_test, pred, zero_division=0))
    rec_list.append(recall_score(y_test, pred, zero_division=0))
    f1_list.append(f1_score(y_test, pred, zero_division=0))
    flagged_list.append(int(pred.sum()))

fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.plot(thresholds_to_show, prec_list, "-o", color=ACCENT,
        linewidth=2, markersize=5, label="precision")
ax.plot(thresholds_to_show, rec_list, "-o", color=RED,
        linewidth=2, markersize=5, label="recall")
ax.plot(thresholds_to_show, f1_list, "-o", color=VIOLET,
        linewidth=2, markersize=5, label="F1")
ax.axvline(0.5, color="#888", linestyle="--", linewidth=1.2,
           label="default 0.5")
ax.set_xlabel("threshold", family="monospace")
ax.set_ylabel("score", family="monospace")
ax.set_title("Precision-recall tradeoff as the threshold slides",
             fontsize=11, family="monospace")
ax.legend(loc="lower center", fontsize=9, framealpha=0.95, ncol=4)
ax.grid(alpha=0.3)
ax.set_ylim(0, 1.05)
plt.tight_layout()
plt.savefig(OUT / "logreg_threshold_sweep.png", **SAVE)
plt.close(fig)


# ── 9. Precision-Recall curve with operating point ───────────────────────
prec_curve, rec_curve, thr_curve = precision_recall_curve(y_test, probs)
# find idx closest to threshold 0.5
idx_05 = np.argmin(np.abs(thr_curve - 0.5))
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(rec_curve, prec_curve, color=ACCENT, linewidth=2.5)
ax.fill_between(rec_curve, 0, prec_curve, color=ACCENT, alpha=0.10)
ax.plot(rec_curve[idx_05], prec_curve[idx_05], "o",
        color=RED, markersize=12, markeredgecolor="#7f1d1d",
        markeredgewidth=1.5, zorder=5)
ax.annotate("threshold = 0.5", xy=(rec_curve[idx_05], prec_curve[idx_05]),
            xytext=(rec_curve[idx_05] - 0.18, prec_curve[idx_05] - 0.18),
            fontsize=9, family="monospace", color=RED, weight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.set_xlabel("recall", family="monospace")
ax.set_ylabel("precision", family="monospace")
ax.set_title("Precision-recall curve  -  every point is one threshold setting",
             fontsize=10, family="monospace")
ax.set_xlim(0, 1.02)
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "logreg_pr_curve.png", **SAVE)
plt.close(fig)


print("Wrote 9 logistic-regression images")
