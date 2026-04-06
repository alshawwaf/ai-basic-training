"""
Explore 06 — The Accuracy Trap
==============================
A real model. A real slider. Watch accuracy lie to your face.

Setup (security-style binary task):
  - "Normal" class = digits 0-8           (1617 samples)
  - "Attack" class = digit 9               (rare, you control how many)
  - Train a LogisticRegression on each slider change
  - Report: accuracy, attack-recall, attack-precision

Drag the slider from "all 180 attack samples" down to "5 samples".
- Accuracy barely moves.
- Attack recall collapses.
- The model learns to ignore the rare class entirely. 95% accuracy.
  Catches zero attacks.

CHALLENGES:
1. At 5 attack samples, what's the accuracy? What's the recall?
   Which number would you put in a status report? Which number
   actually matters?
2. Push the slider back up. At what point does recall recover?
3. The model always retrains from scratch. Why is it making this
   choice? (Hint: the loss function rewards correct *counts*,
   not correct *kinds*.)
"""
import sys
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score

warnings.filterwarnings("ignore")

if "agg" in plt.get_backend().lower():
    print("ERROR: Non-interactive matplotlib backend detected.")
    print("Run from a normal terminal: python explore_06_accuracy_trap.py")
    sys.exit(1)

digits = load_digits()
X_all = digits.data
y_all = (digits.target == 9).astype(int)  # 1 = "attack", 0 = "normal"

normal_idx = np.where(y_all == 0)[0]
attack_idx = np.where(y_all == 1)[0]
max_attacks = len(attack_idx)

print(f"normal samples : {len(normal_idx)}")
print(f"attack samples : {max_attacks}  (digit 9)")
print()

rng = np.random.default_rng(42)


def train_with(n_attacks):
    """Train a fresh logistic regression with `n_attacks` rare samples."""
    chosen_attacks = rng.choice(attack_idx, size=n_attacks, replace=False)
    keep = np.concatenate([normal_idx, chosen_attacks])
    X = X_all[keep]
    y = y_all[keep]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, random_state=0, stratify=y
    )
    model = LogisticRegression(max_iter=200, solver="liblinear")
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)

    return {
        "n_attacks_total": n_attacks,
        "n_attacks_test": int((y_te == 1).sum()),
        "acc": accuracy_score(y_te, y_pred),
        "rec": recall_score(y_te, y_pred, zero_division=0),
        "prec": precision_score(y_te, y_pred, zero_division=0),
        "preds_pos": int((y_pred == 1).sum()),
    }


fig = plt.figure(figsize=(11, 5.5))
fig.suptitle("The Accuracy Trap — drag the slider, watch accuracy lie",
             fontsize=12)

ax_text = fig.add_axes([0.05, 0.30, 0.40, 0.55])
ax_bar = fig.add_axes([0.55, 0.30, 0.42, 0.55])
ax_slider = fig.add_axes([0.20, 0.12, 0.60, 0.04])

ax_text.axis("off")
text_handle = ax_text.text(0.0, 0.95, "", va="top", ha="left",
                           fontsize=10, family="monospace")

slider = Slider(ax_slider, "attack samples kept",
                2, max_attacks, valinit=max_attacks, valstep=1)


def redraw(n):
    n = int(n)
    res = train_with(n)

    msg = (
        f"Training set has {len(normal_idx)} 'normal' + {n} 'attack' samples\n"
        f"Imbalance ratio       : {len(normal_idx) / max(n, 1):6.1f} : 1\n"
        f"\n"
        f"--- evaluated on a 30% test split ---\n"
        f"Accuracy              : {res['acc'] * 100:6.2f} %\n"
        f"Attack RECALL         : {res['rec'] * 100:6.2f} %  <- catches?\n"
        f"Attack PRECISION      : {res['prec'] * 100:6.2f} %  <- correct?\n"
        f"Attacks in test set   : {res['n_attacks_test']}\n"
        f"Predictions = attack  : {res['preds_pos']}\n"
    )
    text_handle.set_text(msg)

    ax_bar.cla()
    metrics = ["accuracy", "recall", "precision"]
    values = [res["acc"] * 100, res["rec"] * 100, res["prec"] * 100]
    colours = ["#94a3b8", "#06d6e0", "#a855f7"]
    bars = ax_bar.bar(metrics, values, color=colours, edgecolor="#1a2332")
    for bar_, value in zip(bars, values):
        ax_bar.text(bar_.get_x() + bar_.get_width() / 2,
                    value + 1.5,
                    f"{value:.1f}%",
                    ha="center", fontsize=10)
    ax_bar.set_ylim(0, 110)
    ax_bar.set_ylabel("score (%)")
    ax_bar.axhline(50, color="#475569", linewidth=0.8, linestyle="--")
    ax_bar.set_title("Metrics on the rare 'attack' class", fontsize=10)
    fig.canvas.draw_idle()


def on_slider(val):
    redraw(val)


slider.on_changed(on_slider)
redraw(max_attacks)
plt.show()

print()
print("Takeaway: accuracy is the wrong metric when one class is rare.")
print("Use recall when missing the rare class is expensive (security,")
print("medical screening, fraud). Use precision when false alarms are")
print("expensive. F1 balances both. We will use these metrics for the")
print("rest of the program.")
print()
print("Next: explore_07_average_digits.py")
