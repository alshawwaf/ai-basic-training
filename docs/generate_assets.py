# generate_assets.py
#
# Generates all educational diagram images used in the lesson notes.
# Run this once from the repo root:
#
#   python generate_assets.py
#
# All images are saved to assets/ and referenced in the .md lesson files.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import os

os.makedirs("assets", exist_ok=True)

# ── Shared style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#e8e8e8",
    "axes.facecolor":   "#f0f0f0",
    "axes.grid":        True,
    "grid.color":       "#cccccc",
    "grid.linewidth":   0.8,
    "font.family":      "sans-serif",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

BLUE   = "#3b82f6"
RED    = "#ef4444"
GREEN  = "#22c55e"
ORANGE = "#f97316"
PURPLE = "#8b5cf6"
GRAY   = "#6b7280"


# ── 1. Traditional Programming vs ML ──────────────────────────────────────────
def fig_ml_vs_programming():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Traditional Programming vs Machine Learning", fontsize=14, fontweight="bold")

    # Traditional
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")
    ax1.set_title("Traditional Programming", color=RED)
    boxes = [
        (1, 7.5, "Rules\n(you write)", RED),
        (1, 4.5, "Data\n(input)",      BLUE),
        (6, 6,   "Program",            GRAY),
        (6, 3,   "Output",             GREEN),
    ]
    for x, y, label, color in boxes:
        ax1.add_patch(mpatches.FancyBboxPatch((x, y), 2.5, 1.5,
            boxstyle="round,pad=0.1", facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))
        ax1.text(x+1.25, y+0.75, label, ha="center", va="center", fontsize=10, fontweight="bold", color=color)
    for (x1,y1), (x2,y2) in [((3.5,8.25),(6,7.0)), ((3.5,5.25),(6,6.5))]:
        ax1.annotate("", xy=(x2,y2), xytext=(x1,y1),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))
    ax1.annotate("", xy=(7.25,4.5), xytext=(7.25,6),
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))

    # ML
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("Machine Learning", color=GREEN)
    boxes2 = [
        (1, 7.5, "Data\n(input)",          BLUE),
        (1, 4.5, "Answers\n(labels)",       ORANGE),
        (6, 6,   "Training",                GRAY),
        (6, 3,   "Model\n(learned rules)",  GREEN),
    ]
    for x, y, label, color in boxes2:
        ax2.add_patch(mpatches.FancyBboxPatch((x, y), 2.5, 1.5,
            boxstyle="round,pad=0.1", facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))
        ax2.text(x+1.25, y+0.75, label, ha="center", va="center", fontsize=10, fontweight="bold", color=color)
    for (x1,y1), (x2,y2) in [((3.5,8.25),(6,7.0)), ((3.5,5.25),(6,6.5))]:
        ax2.annotate("", xy=(x2,y2), xytext=(x1,y1),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))
    ax2.annotate("", xy=(7.25,4.5), xytext=(7.25,6),
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))

    plt.tight_layout()
    fig.savefig("assets/ml_vs_programming.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/ml_vs_programming.png")


# ── 2. Three Types of ML ──────────────────────────────────────────────────────
def fig_three_types_of_ml():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle("The Three Types of Machine Learning", fontsize=14, fontweight="bold")

    # Supervised
    ax = axes[0]
    ax.set_title("Supervised Learning", color=BLUE)
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    examples = [("URL features", "phishing", RED), ("URL features", "legitimate", GREEN),
                ("PE file", "malware", RED), ("log record", "attack", RED), ("log record", "normal", GREEN)]
    for i, (inp, lbl, c) in enumerate(examples):
        y = 8 - i*1.5
        ax.text(0.3, y, inp, fontsize=9, va="center", color=GRAY)
        ax.add_patch(mpatches.FancyBboxPatch((3.5, y-0.3), 1.5, 0.7,
            boxstyle="round,pad=0.05", facecolor=c, alpha=0.25, edgecolor=c))
        ax.text(4.25, y+0.05, lbl, fontsize=8, ha="center", va="center", color=c, fontweight="bold")
    ax.text(5, 0.5, "Labelled examples -> model", fontsize=9, ha="center", color=BLUE, style="italic")

    # Unsupervised
    ax = axes[1]
    ax.set_title("Unsupervised Learning", color=ORANGE)
    np.random.seed(42)
    c1 = np.random.randn(20, 2) * 0.6 + [2, 7]
    c2 = np.random.randn(20, 2) * 0.6 + [7, 7]
    c3 = np.random.randn(20, 2) * 0.6 + [4.5, 3]
    outlier = np.array([[8.5, 1.5]])
    ax.scatter(*c1.T, color=BLUE, alpha=0.6, s=40)
    ax.scatter(*c2.T, color=GREEN, alpha=0.6, s=40)
    ax.scatter(*c3.T, color=PURPLE, alpha=0.6, s=40)
    ax.scatter(*outlier.T, color=RED, s=120, marker="*", zorder=5, label="Anomaly")
    ax.set_xlim(0,10); ax.set_ylim(0,10)
    ax.set_xlabel("bytes_sent"); ax.set_ylabel("duration")
    ax.legend(fontsize=9)
    ax.text(5, 0.3, "No labels -> find structure", fontsize=9, ha="center", color=ORANGE, style="italic")

    # Reinforcement
    ax = axes[2]
    ax.set_title("Reinforcement Learning", color=PURPLE)
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    steps = [("Agent takes action", 8, PURPLE), ("Environment responds", 6, BLUE),
             ("Reward / Penalty", 4, ORANGE), ("Agent improves policy", 2, GREEN)]
    for label, y, color in steps:
        ax.add_patch(mpatches.FancyBboxPatch((1.5, y-0.4), 7, 0.9,
            boxstyle="round,pad=0.1", facecolor=color, alpha=0.15, edgecolor=color, linewidth=1.5))
        ax.text(5, y+0.05, label, ha="center", va="center", fontsize=10, color=color, fontweight="bold")
    for y_from, y_to in [(7.6,6.9),(5.6,4.9),(3.6,2.9)]:
        ax.annotate("", xy=(5,y_to), xytext=(5,y_from),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))
    ax.text(5, 0.3, "Trial & error -> policy", fontsize=9, ha="center", color=PURPLE, style="italic")

    plt.tight_layout()
    fig.savefig("assets/three_types_of_ml.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/three_types_of_ml.png")


# ── 3. Class Imbalance ────────────────────────────────────────────────────────
def fig_class_imbalance():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    fig.suptitle("Class Imbalance: Ideal Training Data vs Real-World Security Data", fontsize=13, fontweight="bold")

    # Balanced (ideal security dataset)
    classes = ["Normal\nTraffic", "Port\nScan", "DoS\nAttack", "Data\nExfil"]
    counts_balanced = [25000, 24500, 25200, 25300]
    colors = [GREEN, ORANGE, RED, PURPLE]
    bars1 = ax1.bar(classes, counts_balanced, color=colors, alpha=0.8, edgecolor="white")
    ax1.set_title("Ideal Training Dataset — Well Balanced", color=GREEN)
    ax1.set_ylabel("Number of Samples")
    ax1.set_ylim(0, 32000)
    mean_val = np.mean(counts_balanced)
    ax1.axhline(mean_val, color=GREEN, linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:,.0f}")
    for bar, count in zip(bars1, counts_balanced):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
                 f"{count:,}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax1.legend()
    ax1.text(1.5, 5000,
        "Each attack type has enough\nexamples for the model to learn.",
        ha="center", va="center", fontsize=9, color=GREEN,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor=GREEN, alpha=0.9))

    # Imbalanced (security)
    classes = ["Normal\nTraffic", "Port\nScan", "DoS\nAttack", "Data\nExfil"]
    counts_imbalanced = [95000, 2800, 1500, 700]
    colors = [GREEN, ORANGE, RED, PURPLE]
    bars = ax2.bar(classes, counts_imbalanced, color=colors, alpha=0.8, edgecolor="white")
    ax2.set_title("Typical Security Dataset — Imbalanced", color=RED)
    ax2.set_ylabel("Number of Samples")
    ax2.set_ylim(0, 108000)
    for bar, count in zip(bars, counts_imbalanced):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
                 f"{count:,}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax2.text(1.5, 70000,
        "A model predicting 'Normal'\nfor everything gets 95% accuracy\n— but catches ZERO attacks.",
        ha="center", va="center", fontsize=9, color=RED,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor=RED, alpha=0.9))

    plt.tight_layout()
    fig.savefig("assets/class_imbalance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/class_imbalance.png")


# ── 4. Linear Regression ──────────────────────────────────────────────────────
def fig_linear_regression():
    np.random.seed(7)
    x = np.linspace(50, 500, 120)
    y = 0.6 * x + 60 + np.random.randn(120) * 28
    coef = np.polyfit(x, y, 1)
    line = np.poly1d(coef)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Linear Regression — Server Response Time vs Traffic Load", fontsize=13, fontweight="bold")

    # Scatter + line
    ax = axes[0]
    ax.scatter(x, y, alpha=0.5, color=BLUE, s=25, label="Observed data")
    ax.plot(x, line(x), color=RED, linewidth=2.5, label=f"Fitted line\ny = {coef[0]:.2f}x + {coef[1]:.0f}")
    ax.set_xlabel("Requests per Second"); ax.set_ylabel("Response Time (ms)")
    ax.set_title("The Line of Best Fit")
    ax.legend()

    # Residuals (errors)
    ax = axes[1]
    sample_x = x[::8]
    sample_y = y[::8]
    ax.scatter(sample_x, sample_y, color=BLUE, s=50, zorder=5)
    ax.plot(x, line(x), color=RED, linewidth=2, label="Model prediction")
    for xi, yi in zip(sample_x, sample_y):
        pred = line(xi)
        ax.plot([xi, xi], [yi, pred], color=ORANGE, linewidth=1, linestyle="--", alpha=0.8)
    ax.set_xlabel("Requests per Second"); ax.set_ylabel("Response Time (ms)")
    ax.set_title("Residuals — the Errors We Minimise")
    ax.legend()
    ax.text(280, 50, "Each dashed line = prediction error\nTraining minimises the total error",
            fontsize=9, color=ORANGE,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor=ORANGE, alpha=0.9))

    plt.tight_layout()
    fig.savefig("assets/linear_regression.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/linear_regression.png")


# ── 5. Sigmoid Curve ──────────────────────────────────────────────────────────
def fig_sigmoid():
    x = np.linspace(-7, 7, 300)
    y = 1 / (1 + np.exp(-x))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Logistic Regression — The Sigmoid Function", fontsize=13, fontweight="bold")

    ax1.plot(x, y, color=BLUE, linewidth=3)
    ax1.axhline(0.5, color=RED, linestyle="--", linewidth=1.5, label="Decision threshold (0.5)")
    ax1.axvline(0, color=GRAY, linestyle=":", linewidth=1)
    ax1.fill_between(x, y, 0.5, where=(y > 0.5), alpha=0.15, color=RED, label="Predicted: Phishing")
    ax1.fill_between(x, y, 0.5, where=(y < 0.5), alpha=0.15, color=GREEN, label="Predicted: Legitimate")
    ax1.set_xlabel("Linear combination of features (x·weights + bias)")
    ax1.set_ylabel("P(phishing)")
    ax1.set_title("sigmoid(x) = 1 / (1 + e^-x)")
    ax1.legend(fontsize=9)
    ax1.set_ylim(-0.05, 1.05)
    ax1.annotate("Very suspicious URL\nP(phishing) ≈ 0.97", xy=(5, 0.97),
        xytext=(2.5, 0.80), fontsize=9,
        arrowprops=dict(arrowstyle="->", color=RED), color=RED)
    ax1.annotate("Looks legitimate\nP(phishing) ≈ 0.03", xy=(-5, 0.03),
        xytext=(-6.5, 0.20), fontsize=9,
        arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN)

    # Threshold effect
    thresholds = np.linspace(0.1, 0.9, 100)
    # simulate precision/recall tradeoff
    precision = 0.5 + 0.5 * thresholds
    recall = 1.0 - 0.85 * thresholds
    ax2.plot(thresholds, precision, color=BLUE, linewidth=2.5, label="Precision")
    ax2.plot(thresholds, recall, color=RED, linewidth=2.5, label="Recall")
    ax2.axvline(0.5, color=GRAY, linestyle="--", linewidth=1.5, label="Default threshold")
    ax2.set_xlabel("Decision Threshold"); ax2.set_ylabel("Score")
    ax2.set_title("Threshold Controls the Precision/Recall Tradeoff")
    ax2.legend()
    ax2.text(0.15, 0.55, "Lower threshold:\ncatch more attacks\n(more false alarms)",
             fontsize=9, color=RED,
             bbox=dict(boxstyle="round", facecolor="white", edgecolor=RED, alpha=0.8))
    ax2.text(0.62, 0.82, "Higher threshold:\nfewer false alarms\n(miss more attacks)",
             fontsize=9, color=BLUE,
             bbox=dict(boxstyle="round", facecolor="white", edgecolor=BLUE, alpha=0.8))

    plt.tight_layout()
    fig.savefig("assets/sigmoid_curve.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/sigmoid_curve.png")


# ── 6. Confusion Matrix ───────────────────────────────────────────────────────
def fig_confusion_matrix():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Confusion Matrix — What the Model Got Right and Wrong", fontsize=13, fontweight="bold")

    # Annotated explanation
    matrix = np.array([[850, 30], [15, 105]])
    labels = [["True Negative (TN)\nCorrectly said: Benign", "False Positive (FP)\nFalse alarm — said Attack"],
              ["False Negative (FN)\nMissed attack!", "True Positive (TP)\nCorrectly caught attack"]]
    colors = np.array([[GREEN, ORANGE], [RED, BLUE]])
    ax1.set_xlim(0, 2); ax1.set_ylim(0, 2); ax1.axis("off")
    ax1.set_title("What Each Cell Means")
    for i in range(2):
        for j in range(2):
            color = [[GREEN, ORANGE], [RED, BLUE]][i][j]
            ax1.add_patch(plt.Rectangle((j, 1-i), 1, 1,
                facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))
            ax1.text(j+0.5, 1.5-i, labels[i][j], ha="center", va="center",
                     fontsize=9, color=color, fontweight="bold")
    ax1.text(-0.15, 1.5, "Actual:\nAttack", ha="center", va="center", fontsize=10, rotation=90)
    ax1.text(-0.15, 0.5, "Actual:\nBenign", ha="center", va="center", fontsize=10, rotation=90)
    ax1.text(0.5, 2.08, "Predicted:\nBenign", ha="center", va="center", fontsize=10)
    ax1.text(1.5, 2.08, "Predicted:\nAttack", ha="center", va="center", fontsize=10)

    # Actual heatmap
    im = ax2.imshow(matrix, cmap="Blues", aspect="auto")
    ax2.set_xticks([0, 1]); ax2.set_yticks([0, 1])
    ax2.set_xticklabels(["Predicted: Benign", "Predicted: Attack"])
    ax2.set_yticklabels(["Actual: Benign", "Actual: Attack"])
    ax2.set_title("Example Results (1000 connections)")
    for i in range(2):
        for j in range(2):
            ax2.text(j, i, f"{matrix[i,j]}", ha="center", va="center",
                     fontsize=16, fontweight="bold",
                     color="white" if matrix[i,j] > 400 else "black")
    precision = matrix[1,1] / (matrix[0,1] + matrix[1,1])
    recall = matrix[1,1] / (matrix[1,0] + matrix[1,1])
    ax2.set_xlabel(f"Precision: {precision:.0%} of alerts were real attacks  |  Recall: {recall:.0%} of attacks were caught",
                   fontsize=9)

    plt.tight_layout()
    fig.savefig("assets/confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/confusion_matrix.png")


# ── 7. ROC Curve ──────────────────────────────────────────────────────────────
def fig_roc_curve():
    fig, ax = plt.subplots(figsize=(6, 5))
    t = np.linspace(0, 1, 300)

    models = [
        ("Great model (AUC=0.96)",  lambda t: 1 - (1-t)**0.15, BLUE, "-"),
        ("Good model (AUC=0.82)",   lambda t: 1 - (1-t)**0.5,  GREEN, "-"),
        ("Weak model (AUC=0.62)",   lambda t: 1 - (1-t)**1.8,  ORANGE, "--"),
        ("Random (AUC=0.50)",       lambda t: t,                GRAY, ":"),
    ]
    for label, fn, color, ls in models:
        fpr = t
        tpr = fn(t)
        auc = np.trapezoid(tpr, fpr)
        ax.plot(fpr, tpr, color=color, linewidth=2.5, linestyle=ls,
                label=f"{label} ({auc:.2f})")

    ax.fill_between(t, models[0][1](t), t, alpha=0.08, color=BLUE)
    ax.set_xlabel("False Positive Rate\n(fraction of benign traffic flagged as attack)")
    ax.set_ylabel("True Positive Rate\n(fraction of attacks caught)")
    ax.set_title("ROC Curve — Comparing Detector Quality", fontweight="bold")
    ax.legend(fontsize=9, loc="lower right")
    ax.plot([0,1],[0,1], color=GRAY, linestyle=":", linewidth=1)
    ax.text(0.55, 0.15, "Coin flip — useless", fontsize=9, color=GRAY, style="italic")

    plt.tight_layout()
    fig.savefig("assets/roc_curve.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/roc_curve.png")


# ── 8. Overfitting Curves ─────────────────────────────────────────────────────
def fig_overfitting():
    depths = np.arange(1, 21)
    train_acc = 1 - 0.35 * np.exp(-0.3 * depths)
    val_acc   = 1 - 0.35 * np.exp(-0.3 * depths) - np.maximum(0, 0.015*(depths-6)**1.5)
    val_acc   = np.clip(val_acc, 0.6, 1.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Overfitting — When the Model Memorises Instead of Learning", fontsize=13, fontweight="bold")

    ax1.plot(depths, train_acc, color=BLUE, linewidth=2.5, marker="o", markersize=4, label="Training accuracy")
    ax1.plot(depths, val_acc,   color=RED,  linewidth=2.5, marker="o", markersize=4, label="Validation accuracy")
    best = np.argmax(val_acc)
    ax1.axvline(depths[best], color=GREEN, linestyle="--", linewidth=2, label=f"Best depth = {depths[best]}")
    ax1.fill_between(depths, train_acc, val_acc, alpha=0.15, color=RED,
                     label="Overfitting gap")
    ax1.set_xlabel("Decision Tree max_depth"); ax1.set_ylabel("Accuracy")
    ax1.set_title("Accuracy vs Model Complexity")
    ax1.legend(fontsize=9)
    ax1.set_ylim(0.55, 1.02)

    epochs = np.arange(1, 81)
    t_loss = 0.9 * np.exp(-0.05 * epochs) + 0.05
    v_loss = 0.9 * np.exp(-0.04 * epochs) + 0.05 + np.maximum(0, 0.003*(epochs-40)**1.3)
    v_loss = np.clip(v_loss, 0, 1)

    ax2.plot(epochs, t_loss, color=BLUE, linewidth=2.5, label="Training loss")
    ax2.plot(epochs, v_loss, color=RED,  linewidth=2.5, label="Validation loss")
    stop = np.argmin(v_loss)
    ax2.axvline(stop, color=GREEN, linestyle="--", linewidth=2, label=f"Early stopping (epoch {stop})")
    ax2.fill_between(epochs[stop:], t_loss[stop:], v_loss[stop:], alpha=0.15, color=RED)
    ax2.set_xlabel("Training Epoch"); ax2.set_ylabel("Loss")
    ax2.set_title("Loss Curves — Catching Overfitting Early")
    ax2.legend(fontsize=9)

    plt.tight_layout()
    fig.savefig("assets/overfitting_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/overfitting_curves.png")


# ── 9. k-Means Clustering ─────────────────────────────────────────────────────
def fig_kmeans():
    np.random.seed(1)
    c1 = np.random.randn(40,2)*0.8 + [2,8]
    c2 = np.random.randn(40,2)*0.8 + [8,8]
    c3 = np.random.randn(40,2)*0.8 + [5,3]
    outliers = np.array([[9.5, 1.2],[1.2,2.0],[9.2,5.5]])

    fig, axes = plt.subplots(1,2, figsize=(12,4))
    fig.suptitle("k-Means Clustering — Finding Behaviour Groups Without Labels", fontsize=13, fontweight="bold")

    ax = axes[0]
    all_pts = np.vstack([c1,c2,c3,outliers])
    ax.scatter(*all_pts.T, color=GRAY, alpha=0.5, s=35, label="Connections (no labels)")
    ax.set_xlabel("Bytes Sent (normalised)"); ax.set_ylabel("Session Duration (normalised)")
    ax.set_title("Before Clustering — Raw Unlabelled Data")
    ax.legend()

    ax = axes[1]
    ax.scatter(*c1.T, color=BLUE,   alpha=0.6, s=35, label="Cluster 1: Normal browsing")
    ax.scatter(*c2.T, color=GREEN,  alpha=0.6, s=35, label="Cluster 2: File transfers")
    ax.scatter(*c3.T, color=PURPLE, alpha=0.6, s=35, label="Cluster 3: Short bursts")
    ax.scatter(*outliers.T, color=RED, s=150, marker="*", zorder=5, label="Anomalies (far from all clusters)")
    centroids = np.array([[2,8],[8,8],[5,3]])
    ax.scatter(*centroids.T, color="black", s=200, marker="X", zorder=6, label="Centroids")
    for c, pts in zip(centroids, [c1,c2,c3]):
        for pt in pts[::5]:
            ax.plot([pt[0],c[0]],[pt[1],c[1]], color=GRAY, alpha=0.15, linewidth=0.8)
    ax.set_xlabel("Bytes Sent (normalised)"); ax.set_ylabel("Session Duration (normalised)")
    ax.set_title("After Clustering — Groups + Anomaly Detection")
    ax.legend(fontsize=8)

    plt.tight_layout()
    fig.savefig("assets/kmeans_clustering.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/kmeans_clustering.png")


# ── 10. k-Fold Cross-Validation ───────────────────────────────────────────────
def fig_kfold():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.5, 5.5); ax.axis("off")
    ax.set_title("5-Fold Cross-Validation — A More Reliable Accuracy Estimate", fontweight="bold", fontsize=13)

    scores = [0.91, 0.89, 0.93, 0.90, 0.92]
    for fold in range(5):
        y = 4 - fold
        ax.text(-0.3, y+0.3, f"Fold {fold+1}", ha="right", va="center", fontsize=10, fontweight="bold")
        for block in range(5):
            is_eval = (block == fold)
            color = RED if is_eval else BLUE
            alpha = 0.85 if is_eval else 0.35
            label = "EVAL" if is_eval else "train"
            ax.add_patch(plt.Rectangle((block, y), 0.95, 0.7,
                facecolor=color, alpha=alpha, edgecolor="white", linewidth=2))
            ax.text(block+0.475, y+0.35, label, ha="center", va="center",
                    fontsize=8, color="white", fontweight="bold")
        ax.text(5.1, y+0.35, f"Score: {scores[fold]:.2f}", va="center", fontsize=10, color=GRAY)

    mean = np.mean(scores); std = np.std(scores)
    ax.text(2.5, -0.2,
        f"Final result: {mean:.2f} ± {std:.2f}   "
        f"(low std = model is stable across different data splits)",
        ha="center", va="center", fontsize=10,
        bbox=dict(boxstyle="round", facecolor=GREEN, alpha=0.15, edgecolor=GREEN))

    plt.tight_layout()
    fig.savefig("assets/kfold_crossval.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/kfold_crossval.png")


# ── 11. Neural Network Architecture ──────────────────────────────────────────
def fig_neural_network():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("Neural Network Architecture — Input to Output", fontweight="bold", fontsize=13)

    layers = [
        (1.0,  [3,4,5,6,7],         "Input Layer\n(features)",      BLUE,   ["bytes_sent","duration","ports","protocol","entropy"]),
        (4.0,  [2,3.5,5,6.5,8],     "Hidden Layer 1\n(64 neurons)", PURPLE, None),
        (6.5,  [3,4.5,6,7.5],       "Hidden Layer 2\n(32 neurons)", PURPLE, None),
        (9.0,  [3.5,5,6.5],         "Output Layer\n(3 classes)",    GREEN,  ["Normal","Port Scan","DoS"]),
    ]

    node_positions = {}
    for lx, ys, label, color, node_labels in layers:
        for i, y in enumerate(ys):
            circle = plt.Circle((lx, y), 0.28, color=color, alpha=0.8, zorder=4)
            ax.add_patch(circle)
            if node_labels:
                ax.text(lx + 0.45, y, node_labels[i], va="center", fontsize=8, color=color)
        node_positions[lx] = ys
        ax.text(lx, 1.0, label, ha="center", va="top", fontsize=9,
                fontweight="bold", color=color)

    lxs = [l[0] for l in layers]
    for i in range(len(lxs)-1):
        for y1 in layers[i][1]:
            for y2 in layers[i+1][1]:
                ax.plot([lxs[i]+0.28, lxs[i+1]-0.28], [y1, y2],
                        color=GRAY, alpha=0.12, linewidth=0.8, zorder=1)

    ax.annotate("Each connection\nhas a weight", xy=(2.5, 6.5), xytext=(2.5, 9),
        fontsize=9, ha="center", color=GRAY,
        arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.annotate("Training adjusts\nall weights", xy=(5.5, 4), xytext=(5.5, 1.8),
        fontsize=9, ha="center", color=PURPLE,
        arrowprops=dict(arrowstyle="->", color=PURPLE))

    plt.tight_layout()
    fig.savefig("assets/neural_network_architecture.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/neural_network_architecture.png")


# ── 12. RAG Pipeline ──────────────────────────────────────────────────────────
def fig_rag_pipeline():
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")
    ax.set_title("RAG Pipeline — Grounding AI Answers in Your Own Documents", fontweight="bold", fontsize=13)

    def box(ax, x, y, w, h, label, color, fontsize=9):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.15", facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))
        ax.text(x+w/2, y+h/2, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=color)

    def arrow(ax, x1, y1, x2, y2):
        ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.8))

    # Indexing phase
    ax.text(3, 7.5, "INDEXING  (done once)", ha="center", fontsize=10,
            color=BLUE, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor=BLUE, alpha=0.1, edgecolor=BLUE))
    box(ax, 0.2, 5.5, 2.2, 1.5, "Your Documents\nCVEs, Runbooks\nThreat Reports", BLUE)
    box(ax, 3.0, 5.5, 2.0, 1.5, "Chunk\nDocuments\n~500 words", BLUE)
    box(ax, 5.5, 5.5, 2.0, 1.5, "Embed\nEach Chunk\n(vectors)", BLUE)
    box(ax, 8.0, 5.5, 2.2, 1.5, "Vector\nDatabase\n(index)", BLUE)
    arrow(ax, 2.4, 6.25, 3.0, 6.25)
    arrow(ax, 5.0, 6.25, 5.5, 6.25)
    arrow(ax, 7.5, 6.25, 8.0, 6.25)

    # Query phase
    ax.text(3, 4.5, "QUERYING  (every question)", ha="center", fontsize=10,
            color=ORANGE, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor=ORANGE, alpha=0.1, edgecolor=ORANGE))
    box(ax, 0.2, 2.8, 2.2, 1.5, "User Question\n\"What ports does\nMimikatz use?\"", ORANGE)
    box(ax, 3.0, 2.8, 2.0, 1.5, "Embed\nQuestion\n(vector)", ORANGE)
    box(ax, 5.5, 2.8, 2.0, 1.5, "Find Similar\nChunks\n(cosine sim)", ORANGE)
    arrow(ax, 2.4, 3.55, 3.0, 3.55)
    arrow(ax, 5.0, 3.55, 5.5, 3.55)
    arrow(ax, 8.0, 6.25, 6.5, 4.3)

    # Generation phase
    ax.text(10.5, 4.5, "GENERATION", ha="center", fontsize=10,
            color=GREEN, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor=GREEN, alpha=0.1, edgecolor=GREEN))
    box(ax, 9.0, 2.8, 2.3, 1.5, "Build Prompt:\nContext +\nQuestion", GREEN)
    box(ax, 11.6, 2.8, 2.2, 1.5, "LLM\nGenerates\nAnswer", GREEN)
    arrow(ax, 7.5, 3.55, 9.0, 3.55)
    arrow(ax, 11.3, 3.55, 11.6, 3.55)
    ax.text(12.7, 1.8, "Grounded answer\n(cites your docs)", ha="center",
            fontsize=9, color=GREEN,
            bbox=dict(boxstyle="round", facecolor=GREEN, alpha=0.15, edgecolor=GREEN))
    arrow(ax, 12.7, 2.8, 12.7, 2.2)

    plt.tight_layout()
    fig.savefig("assets/rag_pipeline.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  saved: assets/rag_pipeline.png")


# ── Run all ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating lesson diagrams...")
    fig_ml_vs_programming()
    fig_three_types_of_ml()
    fig_class_imbalance()
    fig_linear_regression()
    fig_sigmoid()
    fig_confusion_matrix()
    fig_roc_curve()
    fig_overfitting()
    fig_kmeans()
    fig_kfold()
    fig_neural_network()
    fig_rag_pipeline()
    print(f"\nDone. {12} diagrams saved to assets/")
