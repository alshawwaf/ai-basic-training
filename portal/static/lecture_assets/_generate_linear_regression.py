"""
Generate visuals for the four Linear Regression lectures (Stage 1.2).
    python portal/static/lecture_assets/_generate_linear_regression.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

OUT = Path(__file__).resolve().parent

DPI = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"
VIOLET = "#8b5cf6"
RED = "#dc2626"
ORANGE = "#f59e0b"
GREEN = "#16a34a"
DIM = "#9ca3af"

# ── Shared synthetic dataset (EXACTLY matches the labs) ───────────────────
# Reproduces solution_understanding_regression.py:
#   np.random.seed(42); n=500
#   rps = uniform(5, 200, n); response_ms = 1.8 * rps + 30 + N(0, 15)
np.random.seed(42)
N = 500
rps = np.random.uniform(5, 200, N)
response_ms = 1.8 * rps + 30 + np.random.normal(0, 15, N)
X = rps.reshape(-1, 1)
y = response_ms

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
slope = model.coef_[0]
intercept = model.intercept_


# ── 1. Regression vs Classification ────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))

# Left: regression — number line with predicted/actual ticks
ax = axes[0]
ax.set_xlim(0, 300)
ax.set_ylim(-1, 2)
ax.axis("off")
ax.hlines(0, 0, 300, color="#444", linewidth=2)
for x in [0, 50, 100, 150, 200, 250, 300]:
    ax.vlines(x, -0.1, 0.1, color="#444", linewidth=1)
    ax.text(x, -0.45, f"{x} ms", ha="center", fontsize=8, family="monospace", color="#666")
# predicted and actual marks
ax.plot(145.2, 0, "o", color=ACCENT, markersize=12, zorder=5)
ax.plot(148.0, 0, "o", color=GREEN, markersize=12, zorder=5)
ax.text(145.2, 0.45, "predicted\n145.2", ha="center", fontsize=8,
        family="monospace", color=ACCENT, weight="bold")
ax.text(148.0, 0.85, "actual\n148.0", ha="center", fontsize=8,
        family="monospace", color=GREEN, weight="bold")
ax.annotate("", xy=(148.0, 1.4), xytext=(145.2, 1.4),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
ax.text(146.6, 1.55, "error = 2.8 ms", ha="center", fontsize=8,
        family="monospace", color=RED, weight="bold")
ax.set_title("REGRESSION  -  output is a number on a line",
             fontsize=10, family="monospace", color=ACCENT)

# Right: classification — two buckets
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
# Two big bucket boxes
from matplotlib.patches import FancyBboxPatch
box1 = FancyBboxPatch((0.7, 1.5), 3.6, 3,
                     boxstyle="round,pad=0.05,rounding_size=0.2",
                     facecolor=ACCENT, edgecolor="#055e76", linewidth=2)
ax.add_patch(box1)
ax.text(2.5, 3.0, "BENIGN", ha="center", va="center",
        fontsize=14, color="white", family="monospace", weight="bold")

box2 = FancyBboxPatch((5.7, 1.5), 3.6, 3,
                     boxstyle="round,pad=0.05,rounding_size=0.2",
                     facecolor=RED, edgecolor="#7f1d1d", linewidth=2)
ax.add_patch(box2)
ax.text(7.5, 3.0, "ATTACK", ha="center", va="center",
        fontsize=14, color="white", family="monospace", weight="bold")

# A sample point landing in ATTACK
ax.annotate("predicted:\nATTACK", xy=(7.5, 4.7), xytext=(7.5, 5.6),
            ha="center", fontsize=8, family="monospace",
            color=RED, weight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.set_title("CLASSIFICATION  -  output is one of N buckets",
             fontsize=10, family="monospace", color=RED)

plt.tight_layout()
plt.savefig(OUT / "regression_vs_classification.png", **SAVE)
plt.close(fig)


# ── 2. Server scatter plot — the synthetic dataset ────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.scatter(X, y, alpha=0.45, color=ACCENT, s=18, edgecolor="none")
ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title("Server response time vs load (500 samples)",
             fontsize=11, family="monospace")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_scatter_raw.png", **SAVE)
plt.close(fig)


# ── 3. Train/Test split visualisation ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
# Plot all data first (faded), then train (cyan) and test (orange)
ax.scatter(X_train, y_train, alpha=0.55, color=ACCENT, s=22,
           edgecolor="none", label=f"train  ({len(X_train)} rows, 80%)")
ax.scatter(X_test, y_test, alpha=0.85, color=ORANGE, s=32,
           edgecolor="#222", linewidth=0.4, label=f"test   ({len(X_test)} rows, 20%)")
ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title("train_test_split(test_size=0.2, random_state=42)",
             fontsize=11, family="monospace")
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_train_test_split.png", **SAVE)
plt.close(fig)


# ── 4. Data leakage — fit on full vs train only ────────────────────────────
# This shows the mean line shifting due to "seeing" extreme test values
fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
for ax, title, color, fit_X, fit_y in [
    (axes[0], "WRONG: fit on FULL dataset", RED, X, y),
    (axes[1], "RIGHT: fit on TRAIN only", GREEN, X_train, y_train),
]:
    ax.scatter(X_train, y_train, alpha=0.4, color=ACCENT, s=15,
               edgecolor="none", label="train")
    ax.scatter(X_test, y_test, alpha=0.8, color=ORANGE, s=25,
               edgecolor="#222", linewidth=0.3, label="test")
    m = LinearRegression().fit(fit_X, fit_y)
    xline = np.linspace(0, 200, 100).reshape(-1, 1)
    ax.plot(xline, m.predict(xline), color=color, linewidth=2.5,
            label="fitted line")
    ax.set_xlabel("requests_per_second", family="monospace", fontsize=9)
    ax.set_title(title, fontsize=10, family="monospace", color=color)
    ax.legend(loc="upper left", fontsize=7, framealpha=0.9)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("response_time_ms", family="monospace", fontsize=9)
fig.suptitle("Data leakage in action — left peeked at test rows during fit",
             fontsize=10, family="monospace")
plt.tight_layout()
plt.savefig(OUT / "lr_data_leakage.png", **SAVE)
plt.close(fig)


# ── 5. The fitting process — scatter + line + residuals ───────────────────
fig, ax = plt.subplots(figsize=(8, 4.4))
# Use a smaller subset so the residual lines are visible
np.random.seed(7)
sample_idx = np.random.choice(len(X_train), 30, replace=False)
xs = X_train[sample_idx]
ys = y_train[sample_idx]
ax.scatter(xs, ys, alpha=0.85, color=ACCENT, s=40,
           edgecolor="#055e76", linewidth=1, zorder=3, label="actual")
xline = np.linspace(0, 200, 100).reshape(-1, 1)
ax.plot(xline, model.predict(xline), color=RED, linewidth=2.5,
        label=f"y = {slope:.2f}x + {intercept:.1f}")
# Draw residual lines
for xi, yi in zip(xs.flatten(), ys):
    yi_pred = slope * xi + intercept
    ax.plot([xi, xi], [yi, yi_pred], color=DIM, linewidth=1, zorder=1)
ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title("LinearRegression.fit() — minimise the sum of (vertical gaps)²",
             fontsize=11, family="monospace")
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_fit_residuals.png", **SAVE)
plt.close(fig)


# ── 6. Slope and intercept annotated on the line ──────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.4))
xline = np.linspace(0, 200, 100).reshape(-1, 1)
yline = model.predict(xline).flatten()
ax.plot(xline, yline, color=RED, linewidth=2.5, zorder=3)

# Intercept marker
ax.plot(0, intercept, "o", color=VIOLET, markersize=14, zorder=5)
ax.annotate(f"intercept = {intercept:.1f} ms\n(y when x=0)",
            xy=(0, intercept), xytext=(35, intercept - 35),
            fontsize=9, family="monospace", color=VIOLET, weight="bold",
            arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1.4))

# Slope triangle
x1, x2 = 100, 150
y1 = slope * x1 + intercept
y2 = slope * x2 + intercept
ax.plot([x1, x2], [y1, y1], "--", color=ACCENT, linewidth=1.5)
ax.plot([x2, x2], [y1, y2], "--", color=ACCENT, linewidth=1.5)
ax.text((x1 + x2) / 2, y1 - 18, f"+50 rps",
        ha="center", fontsize=9, family="monospace", color=ACCENT, weight="bold")
ax.text(x2 + 5, (y1 + y2) / 2, f"+{slope*50:.1f} ms",
        ha="left", va="center", fontsize=9, family="monospace",
        color=ACCENT, weight="bold")
ax.text(170, 80, f"slope = {slope:.2f}\nms per rps",
        ha="center", fontsize=9, family="monospace", color=ACCENT, weight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor=ACCENT, linewidth=1.2))

ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title("Slope and intercept of the fitted line",
             fontsize=11, family="monospace")
ax.set_xlim(-10, 210)
ax.set_ylim(-10, max(yline) + 30)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_slope_intercept.png", **SAVE)
plt.close(fig)


# ── 7. Predictions at specific values ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.4))
xline = np.linspace(0, 200, 100).reshape(-1, 1)
ax.plot(xline, model.predict(xline), color=RED, linewidth=2.5, zorder=2)

for x_target in [50, 100, 150]:
    y_target = slope * x_target + intercept
    ax.plot([x_target, x_target], [0, y_target], "--", color=ACCENT, linewidth=1)
    ax.plot([0, x_target], [y_target, y_target], "--", color=ACCENT, linewidth=1)
    ax.plot(x_target, y_target, "o", color=ACCENT, markersize=11, zorder=5)
    ax.text(x_target + 4, y_target - 18, f"{y_target:.1f} ms",
            fontsize=9, family="monospace", color=ACCENT, weight="bold")

ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title("model.predict([[50]]), predict([[100]]), predict([[150]])",
             fontsize=10, family="monospace")
ax.set_xlim(-5, 210)
ax.set_ylim(0, max(model.predict(xline).flatten()) + 30)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_predict_points.png", **SAVE)
plt.close(fig)


# ── 8. Residuals histogram ────────────────────────────────────────────────
y_pred_train = model.predict(X_train)
residuals = y_train - y_pred_train

fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))

# Left: histogram
ax = axes[0]
ax.hist(residuals, bins=30, color=ACCENT, edgecolor="#055e76", linewidth=0.6)
ax.axvline(0, color=RED, linewidth=2, linestyle="--", label="zero error")
ax.set_xlabel("residual (ms)  =  actual - predicted", family="monospace", fontsize=9)
ax.set_ylabel("count", family="monospace", fontsize=9)
ax.set_title("Residuals are centred and roughly normal",
             fontsize=10, family="monospace")
ax.legend(fontsize=8, framealpha=0.9)
ax.grid(alpha=0.3)

# Right: residual vs fitted (scatter)
ax = axes[1]
ax.scatter(y_pred_train, residuals, alpha=0.5, color=ACCENT, s=18, edgecolor="none")
ax.axhline(0, color=RED, linewidth=2, linestyle="--")
ax.set_xlabel("predicted (ms)", family="monospace", fontsize=9)
ax.set_ylabel("residual (ms)", family="monospace", fontsize=9)
ax.set_title("Residuals scatter randomly — good fit",
             fontsize=10, family="monospace")
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "lr_residuals.png", **SAVE)
plt.close(fig)


# ── 9. The 3σ security baseline ───────────────────────────────────────────
sigma = residuals.std()
fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.scatter(X_train, y_train, alpha=0.4, color=ACCENT, s=15,
           edgecolor="none", label="normal traffic")

xline = np.linspace(0, 200, 200).reshape(-1, 1)
yline = model.predict(xline).flatten()

# Bands
ax.fill_between(xline.flatten(), yline - 3 * sigma, yline + 3 * sigma,
                color=GREEN, alpha=0.12, label="±3σ normal zone")
ax.fill_between(xline.flatten(), yline + 2 * sigma, yline + 3 * sigma,
                color=ORANGE, alpha=0.18, label="+2σ to +3σ warning")
ax.plot(xline, yline + 3 * sigma, color=RED, linewidth=1.5, linestyle="--",
        label=f"alert threshold (+3σ = +{3*sigma:.1f} ms)")
ax.plot(xline, yline, color="#222", linewidth=2, label="baseline (model)")

# Synthetic anomaly points above the +3σ line
anomalies_x = [70, 120, 160]
for ax_x in anomalies_x:
    base = slope * ax_x + intercept
    anomaly_y = base + 3.5 * sigma + np.random.uniform(5, 25)
    ax.plot(ax_x, anomaly_y, "X", color=RED, markersize=14,
            markeredgecolor="#7f1d1d", markeredgewidth=1.5, zorder=10)
ax.plot([], [], "X", color=RED, markersize=10, label="anomaly!")

ax.set_xlabel("requests_per_second", family="monospace")
ax.set_ylabel("response_time_ms", family="monospace")
ax.set_title(f"Security baseline — flag any point > 3σ above the line",
             fontsize=11, family="monospace")
ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lr_security_baseline.png", **SAVE)
plt.close(fig)


print("Wrote 9 linear-regression images")
