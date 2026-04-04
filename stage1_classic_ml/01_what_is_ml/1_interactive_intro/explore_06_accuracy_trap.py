# Explore 6 — The Accuracy Trap
#
# Accuracy is the most dangerous metric in security.
# Drag the slider to increase class imbalance and watch what happens
# to a REAL model's metrics — accuracy stays high while recall collapses.
#
#   python explore_06_accuracy_trap.py

import sys
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

if plt.get_backend().lower() == "agg":
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run this from a terminal:  python explore_06_accuracy_trap.py")
    sys.exit(1)

warnings.filterwarnings("ignore")  # suppress convergence warnings during slider drag

digits = load_digits()
X_all, y_all = digits.data, digits.target

# State
target_class = [9]
remove_pcts = list(range(0, 100, 5))

# Pre-compute metrics for each class at each removal level to keep slider responsive
cache = {}


def compute_metrics(cls, pct):
    key = (cls, pct)
    if key in cache:
        return cache[key]

    # Create imbalanced dataset by removing samples from the target class
    mask_target = y_all == cls
    mask_other = ~mask_target
    idx_target = np.where(mask_target)[0]
    idx_other = np.where(mask_other)[0]

    keep = max(1, int(len(idx_target) * (1 - pct / 100)))
    np.random.seed(42)  # reproducible
    idx_keep = np.concatenate([
        np.random.choice(idx_target, size=keep, replace=False),
        idx_other,
    ])

    X = X_all[idx_keep]
    y = (y_all[idx_keep] == cls).astype(int)  # binary: target vs everything else

    if y.sum() < 2:
        result = {"acc": 1 - y.mean(), "prec": 0.0, "rec": 0.0, "f1": 0.0,
                  "n_target": int(y.sum()), "n_total": len(y), "ratio": len(y)}
        cache[key] = result
        return result

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y,
    )

    model = LogisticRegression(max_iter=200, solver="lbfgs", random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    n_target = int(mask_target.sum() * (1 - pct / 100))
    n_other = int(mask_other.sum())
    ratio = n_other / max(1, n_target)

    result = {
        "acc": accuracy_score(y_test, y_pred),
        "prec": precision_score(y_test, y_pred, zero_division=0),
        "rec": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "n_target": n_target,
        "n_total": n_target + n_other,
        "ratio": ratio,
    }
    cache[key] = result
    return result


# Pre-compute default class to make first draw fast
for pct in remove_pcts:
    compute_metrics(target_class[0], pct)

# Setup figure
fig, (ax_bar, ax_line) = plt.subplots(1, 2, figsize=(14, 6))
plt.subplots_adjust(left=0.22, bottom=0.22, top=0.88, wspace=0.35)

# Status text
status_txt = fig.text(0.55, 0.92, "", ha="center", fontsize=11)


def draw(pct):
    cls = target_class[0]
    m = compute_metrics(cls, pct)

    # Left: bar chart of metrics
    ax_bar.cla()
    metrics = ["Accuracy", "Precision", "Recall", "F1"]
    values = [m["acc"], m["prec"], m["rec"], m["f1"]]
    colors = []
    for name, val in zip(metrics, values):
        if name == "Accuracy" and val > 0.9 and m["rec"] < 0.5:
            colors.append("#e94560")  # red — deceptively high
        elif val < 0.5:
            colors.append("#e94560")  # red — collapsed
        else:
            colors.append("#16537e")  # blue — healthy

    bars = ax_bar.bar(metrics, values, color=colors)
    ax_bar.set_ylim(0, 1.15)
    ax_bar.set_ylabel("Score", fontsize=11)
    ax_bar.set_title(f"Model metrics (detecting digit {cls})", fontsize=12)

    for bar, val in zip(bars, values):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, val + 0.03,
                    f"{val:.0%}", ha="center", fontsize=11, fontweight="bold")

    # Right: line chart showing metric trajectories
    ax_line.cla()
    pcts_so_far = remove_pcts
    acc_vals, prec_vals, rec_vals, f1_vals = [], [], [], []
    for p in pcts_so_far:
        r = compute_metrics(cls, p)
        acc_vals.append(r["acc"])
        prec_vals.append(r["prec"])
        rec_vals.append(r["rec"])
        f1_vals.append(r["f1"])

    ax_line.plot(pcts_so_far, acc_vals, "o-", label="Accuracy", color="#2ecc71", lw=2)
    ax_line.plot(pcts_so_far, prec_vals, "s-", label="Precision", color="#3498db", lw=2)
    ax_line.plot(pcts_so_far, rec_vals, "^-", label="Recall", color="#e94560", lw=2)
    ax_line.plot(pcts_so_far, f1_vals, "d-", label="F1", color="#f39c12", lw=2)

    # Mark current position
    ax_line.axvline(pct, color="gray", linestyle="--", alpha=0.6)

    ax_line.set_xlim(0, 95)
    ax_line.set_ylim(0, 1.05)
    ax_line.set_xlabel("% of target class removed", fontsize=11)
    ax_line.set_ylabel("Score", fontsize=11)
    ax_line.set_title("Metric trajectories", fontsize=12)
    ax_line.legend(loc="lower left", fontsize=9)

    # Status
    if m["acc"] > 0.9 and m["rec"] < 0.5:
        status_txt.set_text(
            f"THE TRAP: {m['acc']:.0%} accuracy but only {m['rec']:.0%} recall — "
            f"model misses most digit-{cls} samples!"
        )
        status_txt.set_color("#e94560")
        status_txt.set_fontweight("bold")
    elif pct == 0:
        status_txt.set_text(
            f"Balanced: {m['n_target']} target samples, ratio {m['ratio']:.1f}:1"
        )
        status_txt.set_color("#16537e")
        status_txt.set_fontweight("normal")
    else:
        status_txt.set_text(
            f"Imbalance ratio: {m['ratio']:.0f}:1  |  "
            f"{m['n_target']} target vs {m['n_total'] - m['n_target']} other"
        )
        status_txt.set_color("#16537e")
        status_txt.set_fontweight("normal")

    fig.canvas.draw_idle()


# Radio buttons — which class is the "rare" class
ax_radio = plt.axes([0.02, 0.30, 0.14, 0.55])
labels = [f"Digit {d}" for d in range(10)]
radio = RadioButtons(ax_radio, labels, active=target_class[0])


def on_radio(label):
    target_class[0] = int(label.split()[1])
    # Pre-compute this class if needed
    for pct in remove_pcts:
        compute_metrics(target_class[0], pct)
    draw(int(slider.val))


radio.on_clicked(on_radio)

# Slider — how much to remove
ax_slider = plt.axes([0.22, 0.08, 0.55, 0.04])
slider = Slider(ax_slider, "Remove %", 0, 95, valinit=0, valstep=5)


def on_slider(val):
    draw(int(val))


slider.on_changed(on_slider)

fig.suptitle(
    "Select a rare class and drag the slider to create imbalance",
    fontsize=14,
)
draw(0)
plt.show()

print("\nWhat you discovered:")
print("  - Accuracy stays above 90% even when the model can barely detect the target")
print("  - Recall collapses first — the model stops finding rare-class samples")
print("  - F1 score catches the problem because it balances precision and recall")
print()
print("In security, the 'rare class' is the attack:")
print("  - 99.9% of traffic is normal → a model that says 'normal' every time gets 99.9% accuracy")
print("  - But it catches 0% of attacks — recall = 0%")
print("  - This is why security models use F1, precision/recall, and ROC-AUC, not accuracy")
print(f"\n  Next: python explore_07_average_digits.py")
