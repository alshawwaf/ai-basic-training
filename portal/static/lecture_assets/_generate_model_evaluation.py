"""
Generate visuals for the five Model Evaluation lectures (Stage 1.5).
    python portal/static/lecture_assets/_generate_model_evaluation.py

Reproduces the lab dataset (10 000 events, 95% benign / 5% attack) and trains
LogisticRegression / DecisionTree / DummyClassifier exactly as the solutions do.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (confusion_matrix, precision_score, recall_score,
                             f1_score, fbeta_score, roc_curve, roc_auc_score,
                             precision_recall_curve)

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"   # cyan — benign / good
VIOLET = "#8b5cf6"
RED    = "#dc2626"   # attack / bad
ORANGE = "#f59e0b"
GREEN  = "#16a34a"
GREY   = "#64748b"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

# ── Lab dataset (matches every Stage 1.5 solution file) ───────────────────────
np.random.seed(42)
n_benign, n_attack = 9_500, 500
benign_data = np.column_stack([
    np.random.normal(10, 3, n_benign),
    np.random.normal(5000, 1500, n_benign),
    np.random.poisson(3, n_benign),
])
attack_data = np.column_stack([
    np.random.normal(80, 30, n_attack),
    np.random.normal(500, 300, n_attack),
    np.random.poisson(30, n_attack),
])
X = np.vstack([benign_data, attack_data])
y = np.array([0] * n_benign + [1] * n_attack)
# Add per-feature Gaussian noise so classes overlap a bit — without it the
# synthetic distributions are perfectly separable and the precision-recall
# story has no tradeoff to teach.
rng = np.random.default_rng(7)
noise_scale = X.std(axis=0) * 1.9
X = X + rng.normal(0, noise_scale, X.shape)
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
lr    = LogisticRegression(max_iter=1000, random_state=42).fit(X_tr_sc, y_train)
dt    = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train)

dummy_pred  = dummy.predict(X_test)
lr_pred     = lr.predict(X_te_sc)
dt_pred     = dt.predict(X_test)
lr_proba    = lr.predict_proba(X_te_sc)[:, 1]
dt_proba    = dt.predict_proba(X_test)[:, 1]
dummy_proba = np.zeros(len(y_test))


# ════════════════════════════════════════════════════════════════════════════
# 1.5.1 — The Accuracy Trap
# ════════════════════════════════════════════════════════════════════════════

# ── me_imbalance_bar.png ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8.5, 4.2))
counts = [n_benign, n_attack]
bars = ax.bar(["benign", "attack"], counts, color=[ACCENT, RED],
              edgecolor="white", linewidth=2, width=0.55)
ax.set_ylim(0, 11000)
ax.set_ylabel("Number of events")
ax.set_title("10 000 network events  ·  95% benign  /  5% attack")
for bar, c in zip(bars, counts):
    pct = 100 * c / sum(counts)
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 250,
            f"{c:,}\n({pct:.0f}%)", ha="center", fontsize=12,
            family="monospace", weight="bold")
# Annotate the "always-benign trap"
ax.annotate("a model that always says\n\"benign\" already scores 95% accuracy",
            xy=(0, 9500), xytext=(0.55, 7400),
            fontsize=10, color=GREY, ha="left",
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_imbalance_bar.png", **SAVE)
plt.close()

# ── me_dummy_vs_lr.png ───────────────────────────────────────────────────────
from sklearn.metrics import accuracy_score
acc_dummy = accuracy_score(y_test, dummy_pred)
rec_dummy = recall_score(y_test, dummy_pred)
acc_lr    = accuracy_score(y_test, lr_pred)
rec_lr    = recall_score(y_test, lr_pred)

fig, ax = plt.subplots(figsize=(8.8, 4.6))
labels = ["DummyClassifier\n(always benign)", "LogisticRegression"]
xpos = np.arange(len(labels))
w = 0.35
b1 = ax.bar(xpos - w/2, [acc_dummy, acc_lr], w, label="Accuracy",
            color=ACCENT, edgecolor="white", linewidth=1.5)
b2 = ax.bar(xpos + w/2, [rec_dummy, rec_lr], w, label="Attack-class recall",
            color=RED, edgecolor="white", linewidth=1.5)
ax.set_xticks(xpos)
ax.set_xticklabels(labels)
ax.set_ylim(0, 1.1)
ax.set_ylabel("Score")
ax.set_title("Same accuracy story, very different security stories")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{bar.get_height():.2f}", ha="center", fontsize=10,
                family="monospace", weight="bold")
ax.legend(loc="upper left", framealpha=0.95)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_dummy_vs_lr.png", **SAVE)
plt.close()


# ════════════════════════════════════════════════════════════════════════════
# 1.5.2 — Confusion Matrix
# ════════════════════════════════════════════════════════════════════════════

cm = confusion_matrix(y_test, lr_pred)   # rows actual, cols predicted
TN, FP = cm[0, 0], cm[0, 1]
FN, TP = cm[1, 0], cm[1, 1]

# ── me_confusion_heatmap.png ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.6, 5.6))
norm = cm / cm.max()
ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
labels = [["TN", "FP"], ["FN", "TP"]]
notes  = [["benign correctly\nignored", "false alarm\n(analyst burden)"],
          ["MISSED ATTACK\n(high cost)", "attack correctly\ncaught"]]
for i in range(2):
    for j in range(2):
        text_color = "white" if norm[i, j] > 0.5 else "#0f172a"
        ax.text(j, i - 0.15, f"{labels[i][j]} = {cm[i, j]:,}",
                ha="center", va="center", fontsize=14,
                family="monospace", weight="bold", color=text_color)
        ax.text(j, i + 0.18, notes[i][j],
                ha="center", va="center", fontsize=9, color=text_color)
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["Predicted Benign", "Predicted Attack"])
ax.set_yticklabels(["Actual Benign", "Actual Attack"])
ax.set_title("Confusion matrix  ·  LogisticRegression on the test set")
plt.tight_layout()
plt.savefig(OUT / "me_confusion_heatmap.png", **SAVE)
plt.close()

# ── me_metric_zones.png ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8.4, 5.2))
ax.set_xlim(0, 4)
ax.set_ylim(0, 3)
ax.set_aspect("equal")
ax.axis("off")
# 2x2 cells (centered on 1.5,1.5 / 2.5,1.5 / 1.5,0.5 / 2.5,0.5)
cells = [
    (1, 1, "TN", f"{TN:,}", "benign\nignored", ACCENT),
    (2, 1, "FP", f"{FP:,}", "false alarm",     ORANGE),
    (1, 0, "FN", f"{FN:,}", "missed attack",   RED),
    (2, 0, "TP", f"{TP:,}", "attack caught",   GREEN),
]
for x, y0, name, val, note, col in cells:
    ax.add_patch(Rectangle((x, y0), 1, 1, facecolor=col, alpha=0.18,
                           edgecolor=col, linewidth=2))
    ax.text(x + 0.5, y0 + 0.72, name, ha="center", fontsize=13,
            family="monospace", weight="bold", color="#0f172a")
    ax.text(x + 0.5, y0 + 0.45, val, ha="center", fontsize=14,
            family="monospace", weight="bold", color=col)
    ax.text(x + 0.5, y0 + 0.18, note, ha="center", fontsize=9, color="#334155")

# Row / column header
ax.text(0.95, 2.1, "Predicted →", ha="right", fontsize=11, color="#334155")
ax.text(1.5, 2.05, "Benign", ha="center", fontsize=11, weight="bold")
ax.text(2.5, 2.05, "Attack", ha="center", fontsize=11, weight="bold")
ax.text(0.95, 1.5, "Actual\nBenign", ha="right", va="center", fontsize=11, weight="bold")
ax.text(0.95, 0.5, "Actual\nAttack", ha="right", va="center", fontsize=11, weight="bold")

# Recall bracket on the Actual Attack ROW
ax.add_patch(Rectangle((1, 0), 2, 1, fill=False, edgecolor=RED,
                       linewidth=2, linestyle="--"))
ax.text(3.05, 0.5, "Recall\nTP / (TP+FN)\n= of all real\nattacks, how\nmany did we\ncatch?",
        va="center", fontsize=9, color=RED)

# Precision bracket on the Predicted Attack COLUMN
ax.add_patch(Rectangle((2, 0), 1, 2, fill=False, edgecolor=VIOLET,
                       linewidth=2, linestyle="--"))
ax.text(2.5, 2.45, "Precision\nTP / (TP+FP)  ·  of every alert, how many were real?",
        ha="center", fontsize=9, color=VIOLET)

ax.set_title("Where each metric lives inside the confusion matrix",
             fontsize=13, pad=8)
plt.tight_layout()
plt.savefig(OUT / "me_metric_zones.png", **SAVE)
plt.close()


# ════════════════════════════════════════════════════════════════════════════
# 1.5.3 — Precision, Recall, F1
# ════════════════════════════════════════════════════════════════════════════

# ── me_pr_tradeoff.png ───────────────────────────────────────────────────────
prec_curve, rec_curve, thr_curve = precision_recall_curve(y_test, lr_proba)
# precision_recall_curve returns one extra precision/recall, drop last
prec_curve = prec_curve[:-1]
rec_curve  = rec_curve[:-1]
f1_curve   = 2 * prec_curve * rec_curve / (prec_curve + rec_curve + 1e-12)
best_f1_idx = int(np.argmax(f1_curve))
best_thr = thr_curve[best_f1_idx]

fig, ax = plt.subplots(figsize=(9.2, 5.0))
ax.plot(thr_curve, prec_curve, color=VIOLET, lw=2.4, label="Precision")
ax.plot(thr_curve, rec_curve,  color=RED,    lw=2.4, label="Recall")
ax.plot(thr_curve, f1_curve,   color=ACCENT, lw=2.0, ls="--", label="F1")
ax.axvline(0.5, color=GREY, lw=1, ls=":", alpha=0.7)
ax.text(0.51, 0.04, "default\nthreshold = 0.5", color=GREY, fontsize=9)
ax.axvline(best_thr, color=ORANGE, lw=1.4, ls="-", alpha=0.8)
ax.text(best_thr + 0.01, 0.92, f"max F1 @ {best_thr:.2f}", color=ORANGE, fontsize=9)
ax.set_xlim(0.05, 0.95)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Decision threshold (LogisticRegression P(attack))")
ax.set_ylabel("Score on attack class")
ax.set_title("The precision-recall tradeoff: every threshold is a different model")
ax.legend(loc="lower left", framealpha=0.95)
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "me_pr_tradeoff.png", **SAVE)
plt.close()

# ── me_f1_f2_compare.png ─────────────────────────────────────────────────────
models = [
    ("DummyClassifier",     dummy_pred),
    ("LogisticRegression",  lr_pred),
    ("DecisionTree",        dt_pred),
]
f1s = [f1_score(y_test, p, zero_division=0) for _, p in models]
f2s = [fbeta_score(y_test, p, beta=2, zero_division=0) for _, p in models]

fig, ax = plt.subplots(figsize=(9.0, 4.6))
xpos = np.arange(len(models))
w = 0.35
b1 = ax.bar(xpos - w/2, f1s, w, label="F1 (balanced)",
            color=ACCENT, edgecolor="white", linewidth=1.5)
b2 = ax.bar(xpos + w/2, f2s, w, label="F2 (recall-weighted)",
            color=RED, edgecolor="white", linewidth=1.5)
ax.set_xticks(xpos)
ax.set_xticklabels([m[0] for m in models])
ax.set_ylim(0, 1.05)
ax.set_ylabel("Score on attack class")
ax.set_title("F1 vs F2  ·  F2 weighs recall higher — better for security")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{bar.get_height():.2f}", ha="center", fontsize=10,
                family="monospace", weight="bold")
ax.legend(loc="upper left", framealpha=0.95)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_f1_f2_compare.png", **SAVE)
plt.close()


# ════════════════════════════════════════════════════════════════════════════
# 1.5.4 — ROC and AUC
# ════════════════════════════════════════════════════════════════════════════

# ── me_roc_single.png ────────────────────────────────────────────────────────
fpr, tpr, thr = roc_curve(y_test, lr_proba)
auc_lr = roc_auc_score(y_test, lr_proba)
idx_05 = int(np.argmin(np.abs(thr - 0.5)))

fig, ax = plt.subplots(figsize=(7.0, 6.0))
ax.fill_between(fpr, tpr, color=ACCENT, alpha=0.18,
                label=f"AUC = {auc_lr:.3f}")
ax.plot(fpr, tpr, color=ACCENT, lw=2.5, label="LogisticRegression")
ax.plot([0, 1], [0, 1], "--", color=GREY, lw=1.4, label="Random  (AUC = 0.50)")
ax.scatter([fpr[idx_05]], [tpr[idx_05]], s=90, color=RED, zorder=5,
           edgecolor="white", linewidth=1.5)
ax.annotate(f"threshold = 0.5\nFPR={fpr[idx_05]:.03f}  TPR={tpr[idx_05]:.03f}",
            xy=(fpr[idx_05], tpr[idx_05]), xytext=(0.32, 0.55),
            fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.text(0.02, 0.97, "(0,1) perfect classifier\n— catches every attack,\n   zero false alarms",
        fontsize=8.5, color="#0f172a", va="top")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xlabel("False Positive Rate  =  FP / (FP + TN)")
ax.set_ylabel("True Positive Rate  =  TP / (TP + FN)  =  Recall")
ax.set_title("ROC curve  ·  the closer to the top-left corner, the better")
ax.legend(loc="lower right", framealpha=0.95)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_roc_single.png", **SAVE)
plt.close()

# ── me_roc_compare.png ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.6, 6.0))
auc_dummy = roc_auc_score(y_test, dummy_proba)
auc_dt    = roc_auc_score(y_test, dt_proba)
for name, scores, col in [
    ("DummyClassifier",    dummy_proba, GREY),
    ("DecisionTree",       dt_proba,    VIOLET),
    ("LogisticRegression", lr_proba,    ACCENT),
]:
    fpr_m, tpr_m, _ = roc_curve(y_test, scores)
    auc_m = roc_auc_score(y_test, scores)
    ax.plot(fpr_m, tpr_m, lw=2.6, color=col,
            label=f"{name}  (AUC = {auc_m:.3f})")
ax.plot([0, 1], [0, 1], "--", color="#0f172a", lw=1.0, alpha=0.6, label="Random")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate (Recall)")
ax.set_title("Three models on one ROC plot  ·  AUC ranks them objectively")
ax.legend(loc="lower right", framealpha=0.95)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_roc_compare.png", **SAVE)
plt.close()


# ════════════════════════════════════════════════════════════════════════════
# 1.5.5 — Threshold Tuning
# ════════════════════════════════════════════════════════════════════════════

# ── me_threshold_table.png ───────────────────────────────────────────────────
# Sample a few thresholds and compute alert volume / TP / FP
sample_thr = [0.20, 0.30, 0.50, 0.70, 0.90]
totals = {"alerts": [], "caught": [], "false_alarms": []}
n_test_attacks = int((y_test == 1).sum())
for t in sample_thr:
    pred_t = (lr_proba >= t).astype(int)
    tp = int(((pred_t == 1) & (y_test == 1)).sum())
    fp = int(((pred_t == 1) & (y_test == 0)).sum())
    totals["alerts"].append(tp + fp)
    totals["caught"].append(tp)
    totals["false_alarms"].append(fp)

fig, ax = plt.subplots(figsize=(9.4, 4.8))
xpos = np.arange(len(sample_thr))
w = 0.27
b1 = ax.bar(xpos - w, totals["alerts"], w, label="Total alerts",
            color=GREY, edgecolor="white", linewidth=1.2)
b2 = ax.bar(xpos,     totals["caught"], w, label="True attacks caught",
            color=GREEN, edgecolor="white", linewidth=1.2)
b3 = ax.bar(xpos + w, totals["false_alarms"], w, label="False alarms",
            color=ORANGE, edgecolor="white", linewidth=1.2)
ax.axhline(n_test_attacks, color=RED, ls="--", lw=1.2, alpha=0.7)
ax.text(len(sample_thr) - 0.6, n_test_attacks + 4,
        f"{n_test_attacks} actual attacks in test set",
        color=RED, fontsize=9)
ax.set_xticks(xpos)
ax.set_xticklabels([f"{t:.2f}" for t in sample_thr])
ax.set_xlabel("Decision threshold")
ax.set_ylabel("Count (test set, 2 000 events)")
ax.set_title("Sliding the threshold reshapes the SOC's daily alert load")
for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 3, f"{int(h)}",
                ha="center", fontsize=8.5, family="monospace")
ax.legend(loc="upper right", framealpha=0.95)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "me_threshold_table.png", **SAVE)
plt.close()

# ── me_scenario_compare.png ──────────────────────────────────────────────────
# Find Scenario A (recall>=0.95) and Scenario B (precision>=0.95)
def find_scenario_a(probs, y_true):
    for t in np.arange(0.9, 0.0, -0.01):
        pred = (probs >= t).astype(int)
        if recall_score(y_true, pred) >= 0.95:
            return t, pred
    return 0.5, (probs >= 0.5).astype(int)

def find_scenario_b(probs, y_true):
    for t in np.arange(0.0, 0.95, 0.01):
        pred = (probs >= t).astype(int)
        if precision_score(y_true, pred, zero_division=0) >= 0.95:
            return t, pred
    return 0.5, (probs >= 0.5).astype(int)

t_a, pred_a = find_scenario_a(lr_proba, y_test)
t_b, pred_b = find_scenario_b(lr_proba, y_test)

def metrics_for(pred):
    tp = int(((pred == 1) & (y_test == 1)).sum())
    fp = int(((pred == 1) & (y_test == 0)).sum())
    fn = int(((pred == 0) & (y_test == 1)).sum())
    return dict(tp=tp, fp=fp, fn=fn,
                precision=tp / max(tp + fp, 1),
                recall=tp / max(tp + fn, 1),
                alerts=tp + fp)

ma = metrics_for(pred_a)
mb = metrics_for(pred_b)

fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.2))
for ax, m, t, title, col in [
    (axes[0], ma, t_a, f"Scenario A · catch every attack\n(threshold = {t_a:.2f})", RED),
    (axes[1], mb, t_b, f"Scenario B · trusted alerts only\n(threshold = {t_b:.2f})", ACCENT),
]:
    cats = ["Total\nalerts", "Attacks\ncaught", "False\nalarms", "Attacks\nMISSED"]
    vals = [m["alerts"], m["tp"], m["fp"], m["fn"]]
    cols = [GREY, GREEN, ORANGE, RED]
    bars = ax.bar(cats, vals, color=cols, edgecolor="white", linewidth=1.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                f"{int(bar.get_height())}", ha="center", fontsize=11,
                family="monospace", weight="bold")
    ax.set_ylim(0, max(ma["alerts"], mb["alerts"]) * 1.25)
    ax.set_title(title, color=col, fontsize=12, weight="bold")
    ax.text(0.5, -0.22,
            f"precision = {m['precision']:.2f}   ·   recall = {m['recall']:.2f}",
            transform=ax.transAxes, ha="center", fontsize=10, color="#334155")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
fig.suptitle("Two thresholds, two operational realities", fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig(OUT / "me_scenario_compare.png", **SAVE)
plt.close()


print("Generated 10 model-evaluation visuals in", OUT)
print(f"  Scenario A: t={t_a:.2f}  prec={ma['precision']:.3f}  rec={ma['recall']:.3f}  alerts={ma['alerts']}")
print(f"  Scenario B: t={t_b:.2f}  prec={mb['precision']:.3f}  rec={mb['recall']:.3f}  alerts={mb['alerts']}")
print(f"  LR confusion: TN={TN} FP={FP} FN={FN} TP={TP}")
print(f"  AUCs: dummy={auc_dummy:.3f}  lr={auc_lr:.3f}  dt={auc_dt:.3f}")
print(f"  PR-curve max F1 threshold = {best_thr:.3f}")
