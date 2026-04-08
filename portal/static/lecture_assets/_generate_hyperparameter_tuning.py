"""
Generate visuals for the four Hyperparameter Tuning lectures (Stage 3.4).
    python portal/static/lecture_assets/_generate_hyperparameter_tuning.py

Reproduces the make_classification(2000, 20) dataset used by every Stage 3.4
solution_*.py and runs the same Adam(0.001) Dense(64,32,1) network across
the same learning rate, batch size, and architecture grids — so the numbers
in the visuals match what learners see when they run the labs.
"""
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import warnings
warnings.filterwarnings("ignore")

import time
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from tensorflow import keras

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
DARK   = "#0f172a"
GOLD   = "#facc15"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})


def save(fig, name):
    fig.savefig(OUT / name, **SAVE)
    plt.close(fig)
    print(f"  wrote {name}")


# ── Reproduce the lab dataset (same as every Stage 3.4 solution) ──────────────
np.random.seed(42)
tf.random.set_seed(42)

print("  → building dataset ...")
X, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                           n_redundant=5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)


def build_model(lr=0.001, units=(64, 32)):
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential()
    m.add(keras.layers.Input(shape=(20,)))
    for u in units:
        m.add(keras.layers.Dense(u, activation='relu'))
    m.add(keras.layers.Dense(1, activation='sigmoid'))
    m.compile(optimizer=keras.optimizers.Adam(learning_rate=lr),
              loss='binary_crossentropy',
              metrics=['accuracy'])
    return m


def build_model_search(units, depth):
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential()
    m.add(keras.layers.Input(shape=(20,)))
    for _ in range(depth):
        m.add(keras.layers.Dense(units, activation='relu'))
    m.add(keras.layers.Dense(1, activation='sigmoid'))
    m.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])
    return m


# ============================================================
# LECTURE 1 — What Are Hyperparameters?
# ============================================================

# 1. hp_params_vs_hyperparams.png — two clearly separated buckets
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11); ax.set_ylim(0, 6)
ax.axis('off')

# Left bucket — YOU set
left = FancyBboxPatch((0.3, 0.5), 5, 5, boxstyle="round,pad=0.05,rounding_size=0.15",
                      facecolor="#fff7ed", edgecolor=ORANGE, linewidth=2.5)
ax.add_patch(left)
ax.text(2.8, 5.05, "YOU set (hyperparameters)", ha='center', fontsize=13,
        color=ORANGE, fontweight='bold')
ax.text(2.8, 4.55, "before model.fit() — define the training", ha='center',
        fontsize=10, color=GREY, style='italic')
hp_lines = [
    "units=64",
    "learning_rate=0.001",
    "batch_size=32",
    "epochs=20",
    "activation='relu'",
    "dropout_rate=0.3",
]
for i, line in enumerate(hp_lines):
    ax.text(2.8, 3.85 - 0.5 * i, line, ha='center', fontsize=11,
            color=DARK, family='monospace')

# Right bucket — TRAINING learns
right = FancyBboxPatch((5.7, 0.5), 5, 5, boxstyle="round,pad=0.05,rounding_size=0.15",
                       facecolor="#ecfeff", edgecolor=ACCENT, linewidth=2.5)
ax.add_patch(right)
ax.text(8.2, 5.05, "TRAINING learns (parameters)", ha='center', fontsize=13,
        color=ACCENT, fontweight='bold')
ax.text(8.2, 4.55, "inside model.fit() — gradient descent", ha='center',
        fontsize=10, color=GREY, style='italic')
param_lines = [
    "W1 (20, 64) → 1280 weights",
    "b1 (64,)    →   64 biases",
    "W2 (64, 32) → 2048 weights",
    "b2 (32,)    →   32 biases",
    "W3 (32, 1)  →   32 weights",
    "b3 (1,)     →    1 bias",
]
for i, line in enumerate(param_lines):
    ax.text(8.2, 3.85 - 0.5 * i, line, ha='center', fontsize=10,
            color=DARK, family='monospace')

ax.text(5.5, 0.15, "you wire it up → training fills it in",
        ha='center', fontsize=10, color=GREY, style='italic')
fig.suptitle("Parameters vs Hyperparameters — two separate buckets", y=1.02)
save(fig, "hp_params_vs_hyperparams.png")


# 2. hp_weights_before_after.png — real weight matrix before vs after training
print("  → training tiny model for weights snapshot ...")
snap_model = build_model(lr=0.001, units=(64, 32))
W_before = snap_model.layers[0].get_weights()[0].copy()
snap_model.fit(X_train, y_train, epochs=20, batch_size=32,
               validation_data=(X_val, y_val), verbose=0)
W_after = snap_model.layers[0].get_weights()[0].copy()
delta = W_after - W_before

fig, axes = plt.subplots(1, 3, figsize=(11, 4.5))
vmax = max(abs(W_before).max(), abs(W_after).max())
im0 = axes[0].imshow(W_before, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')
axes[0].set_title('Layer 1 weights — BEFORE training', color=GREY, fontsize=11)
axes[0].set_xlabel('output unit'); axes[0].set_ylabel('input feature')

im1 = axes[1].imshow(W_after, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')
axes[1].set_title('AFTER 20 epochs', color=ACCENT, fontsize=11)
axes[1].set_xlabel('output unit')

dvmax = abs(delta).max()
im2 = axes[2].imshow(delta, cmap='RdBu_r', vmin=-dvmax, vmax=dvmax, aspect='auto')
axes[2].set_title('Δ = AFTER − BEFORE  (what was learned)', color=ORANGE, fontsize=11)
axes[2].set_xlabel('output unit')

fig.suptitle('The same 1,280 weights before and after training', y=1.02)
fig.tight_layout()
save(fig, "hp_weights_before_after.png")


# 3. hp_inventory.png — categorised hyperparameter inventory
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_xlim(0, 11); ax.set_ylim(0, 6)
ax.axis('off')

categories = [
    ("Architecture", ACCENT, [
        "n_hidden_layers     1 – 5",
        "units_per_layer     8 – 512",
        "activation (hidden) relu / elu / tanh",
        "activation (out)    sigmoid / softmax",
    ]),
    ("Regularisation", VIOLET, [
        "dropout_rate        0.1 – 0.5",
        "L2 weight decay     0 – 0.01",
        "early stopping      patience 3 – 10",
        "data augmentation   yes / no",
    ]),
    ("Optimiser & Training", ORANGE, [
        "optimizer           Adam / SGD / RMSProp",
        "learning_rate       1e-4 – 1e-1",
        "batch_size          16 – 2048",
        "epochs              10 – 500",
    ]),
]

col_w = 3.5
for ci, (title, colour, items) in enumerate(categories):
    x = 0.3 + ci * 3.6
    box = FancyBboxPatch((x, 0.4), col_w, 5.1,
                         boxstyle="round,pad=0.05,rounding_size=0.15",
                         facecolor='white', edgecolor=colour, linewidth=2.5)
    ax.add_patch(box)
    header = Rectangle((x, 4.7), col_w, 0.8, facecolor=colour, edgecolor='none')
    ax.add_patch(header)
    ax.text(x + col_w / 2, 5.1, title, ha='center', va='center',
            fontsize=12, color='white', fontweight='bold')
    for i, item in enumerate(items):
        ax.text(x + 0.2, 4.2 - 0.55 * i, item, fontsize=10,
                color=DARK, family='monospace', va='top')

fig.suptitle('Hyperparameter inventory — what tuning means in practice', y=1.0)
save(fig, "hp_inventory.png")


# ============================================================
# LECTURE 2 — Learning Rate Sensitivity
# ============================================================

# 4. hp_lr_step_size.png — three step sizes on a 1D loss landscape
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
xs = np.linspace(-3, 3, 400)
loss = xs ** 2 + 0.3
for ax in axes:
    ax.plot(xs, loss, color=GREY, linewidth=2)
    ax.set_xlabel('weight'); ax.set_ylabel('loss')
    ax.set_xlim(-3, 3); ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)

# lr too small — tiny steps
xs_small = [-2.6]
for _ in range(8):
    g = 2 * xs_small[-1]
    xs_small.append(xs_small[-1] - 0.05 * g)
ys_small = [x ** 2 + 0.3 for x in xs_small]
axes[0].plot(xs_small, ys_small, 'o-', color=RED, markersize=7, linewidth=2)
axes[0].set_title('lr = 0.0001 (too small)\ncrawls — never reaches minimum',
                  color=RED, fontsize=11)

# lr just right — converges
xs_ok = [-2.6]
for _ in range(8):
    g = 2 * xs_ok[-1]
    xs_ok.append(xs_ok[-1] - 0.3 * g)
ys_ok = [x ** 2 + 0.3 for x in xs_ok]
axes[1].plot(xs_ok, ys_ok, 'o-', color=GREEN, markersize=7, linewidth=2)
axes[1].set_title('lr = 0.001 (just right)\nsmooth descent to the minimum',
                  color=GREEN, fontsize=11)

# lr too large — overshoot/oscillate
xs_big = [-2.6]
for _ in range(8):
    g = 2 * xs_big[-1]
    xs_big.append(xs_big[-1] - 1.05 * g)
ys_big = [x ** 2 + 0.3 for x in xs_big]
axes[2].plot(xs_big, ys_big, 'o-', color=ORANGE, markersize=7, linewidth=2)
axes[2].set_title('lr = 0.1 (too large)\novershoots, oscillates / diverges',
                  color=ORANGE, fontsize=11)

fig.suptitle('Same loss surface, three step sizes', y=1.02)
fig.tight_layout()
save(fig, "hp_lr_step_size.png")


# 5. hp_lr_loss_curves.png — REAL training curves at three learning rates
print("  → training 3 LR experiments (lr = 1e-3, 1e-1, 1e-5) ...")
EPOCHS_LR = 30

m_ok = build_model(lr=0.001)
h_ok = m_ok.fit(X_train, y_train, epochs=EPOCHS_LR,
                validation_data=(X_val, y_val), verbose=0)

m_big = build_model(lr=0.1)
h_big = m_big.fit(X_train, y_train, epochs=EPOCHS_LR,
                  validation_data=(X_val, y_val), verbose=0)

m_tiny = build_model(lr=0.00001)
h_tiny = m_tiny.fit(X_train, y_train, epochs=EPOCHS_LR,
                    validation_data=(X_val, y_val), verbose=0)

print(f"     lr=0.001    val_acc = {h_ok.history['val_accuracy'][-1]:.4f}")
print(f"     lr=0.1      val_acc = {h_big.history['val_accuracy'][-1]:.4f}")
print(f"     lr=0.00001  val_acc = {h_tiny.history['val_accuracy'][-1]:.4f}")

fig, ax = plt.subplots(figsize=(10, 5))
epochs_x = np.arange(1, EPOCHS_LR + 1)
ax.plot(epochs_x, h_ok.history['loss'],   color=GREEN,  linewidth=2.4,
        label='lr = 0.001 (just right)')
ax.plot(epochs_x, h_big.history['loss'],  color=ORANGE, linewidth=2.4,
        label='lr = 0.1 (too large)')
ax.plot(epochs_x, h_tiny.history['loss'], color=RED,    linewidth=2.4,
        label='lr = 0.00001 (too small)')
ax.set_xlabel('epoch')
ax.set_ylabel('training loss')
ax.set_title('Real training loss — three Adam learning rates on the same data')
ax.legend(loc='upper right', framealpha=0.95)
ax.grid(True, alpha=0.3)
save(fig, "hp_lr_loss_curves.png")


# 6. hp_lr_diagnosis.png — diagnostic table linking pattern to lr issue
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.set_xlim(0, 11); ax.set_ylim(0, 5)
ax.axis('off')

rows = [
    ("Loss barely moves",         "lr too small",        "↑ 10×",   RED),
    ("Slow then plateaus",        "lr slightly small",   "↑ 2-3×",  ORANGE),
    ("Falls then spikes upward",  "lr too large",        "↓ 10×",   ORANGE),
    ("Immediately NaN",           "lr way too large",    "↓ 100×",  RED),
    ("Smooth, levels off",        "Goldilocks zone",     "keep it", GREEN),
]
header_y = 4.4
ax.text(1.5, header_y, "Symptom in loss curve", fontsize=11, color=DARK, fontweight='bold')
ax.text(6.0, header_y, "Diagnosis", fontsize=11, color=DARK, fontweight='bold')
ax.text(9.4, header_y, "Fix", fontsize=11, color=DARK, fontweight='bold')
ax.plot([0.3, 10.7], [4.15, 4.15], color=GREY, linewidth=1)
for i, (sym, diag, fix, col) in enumerate(rows):
    y = 3.7 - 0.7 * i
    ax.text(1.5, y, sym, fontsize=10.5, color=DARK)
    ax.text(6.0, y, diag, fontsize=10.5, color=col, fontweight='bold')
    box = FancyBboxPatch((9.0, y - 0.18), 1.5, 0.4,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         facecolor=col, edgecolor='none', alpha=0.85)
    ax.add_patch(box)
    ax.text(9.75, y, fix, fontsize=10, color='white',
            fontweight='bold', ha='center', va='center')

fig.suptitle('Diagnose learning rate problems by reading the loss curve', y=1.0)
save(fig, "hp_lr_diagnosis.png")


# ============================================================
# LECTURE 3 — Batch Size Effects
# ============================================================

# 7. hp_batch_updates.png — many small steps vs one big step (same epoch)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

# Left: 50 small noisy steps
np.random.seed(0)
ax = axes[0]
ax.plot(xs, loss, color=GREY, linewidth=2)
xs_path = [-2.7]
for _ in range(50):
    g = 2 * xs_path[-1] + np.random.normal(0, 1.2)
    xs_path.append(xs_path[-1] - 0.06 * g)
ys_path = [x ** 2 + 0.3 for x in xs_path]
ax.plot(xs_path, ys_path, 'o-', color=ACCENT, markersize=4, linewidth=1.2,
        alpha=0.85)
ax.scatter([xs_path[0]], [ys_path[0]], color=ORANGE, s=80, zorder=5,
           edgecolor='white', linewidth=1.5, label='start')
ax.scatter([xs_path[-1]], [ys_path[-1]], color=GREEN, s=100, zorder=5,
           edgecolor='white', linewidth=1.5, label='end')
ax.set_title('batch_size = 32  → 50 small noisy steps per epoch',
             color=ACCENT, fontsize=11)
ax.set_xlabel('weight'); ax.set_ylabel('loss')
ax.set_xlim(-3, 3); ax.set_ylim(0, 10)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')

# Right: 1 big stable step (full batch)
ax = axes[1]
ax.plot(xs, loss, color=GREY, linewidth=2)
arrow = FancyArrowPatch((-2.7, 7.59), (-0.05, 0.3),
                        arrowstyle='->', mutation_scale=22,
                        color=VIOLET, linewidth=2.6)
ax.add_patch(arrow)
ax.scatter([-2.7], [7.59], color=ORANGE, s=80, zorder=5,
           edgecolor='white', linewidth=1.5, label='start')
ax.scatter([0], [0.3], color=GREEN, s=100, zorder=5,
           edgecolor='white', linewidth=1.5, label='end')
ax.set_title('batch_size = 1600 (full batch) → 1 big stable step',
             color=VIOLET, fontsize=11)
ax.set_xlabel('weight'); ax.set_ylabel('loss')
ax.set_xlim(-3, 3); ax.set_ylim(0, 10)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')

fig.suptitle('One epoch, two extremes — same total samples seen', y=1.02)
fig.tight_layout()
save(fig, "hp_batch_updates.png")


# 8. hp_sharp_vs_flat.png — sharp vs flat minima
fig, ax = plt.subplots(figsize=(10.5, 4.8))
xs2 = np.linspace(-5, 5, 800)
sharp = 0.6 + 14 * np.exp(-((xs2 - 2.4) ** 2) / 0.08)
flat  = 0.6 + 6  * np.exp(-((xs2 + 1.8) ** 2) / 1.4)
loss_curve = 12 - sharp + (12 - flat) - 12
loss_curve = 12 - np.maximum(sharp, flat)
ax.plot(xs2, loss_curve, color=GREY, linewidth=2.4)
ax.fill_between(xs2, loss_curve, 12, color=LIGHT, alpha=0.4)

# mark sharp minimum
ax.scatter([2.4], [12 - sharp.max()], color=RED, s=140, zorder=5,
           edgecolor='white', linewidth=2)
ax.annotate('Sharp minimum\n(large-batch training)\npoor generalisation',
            xy=(2.4, 12 - sharp.max()), xytext=(3.4, 8),
            fontsize=10, color=RED, fontweight='bold', ha='left',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))

# mark flat minimum
ax.scatter([-1.8], [12 - flat.max()], color=GREEN, s=140, zorder=5,
           edgecolor='white', linewidth=2)
ax.annotate('Flat minimum\n(small-batch training)\nrobust to perturbation',
            xy=(-1.8, 12 - flat.max()), xytext=(-4.8, 4),
            fontsize=10, color=GREEN, fontweight='bold', ha='left',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))

ax.set_xlabel('weight space')
ax.set_ylabel('loss')
ax.set_title('Sharp vs flat minima — why small batches generalise better')
ax.set_xlim(-5, 5); ax.set_ylim(0, 12)
ax.grid(True, alpha=0.3)
save(fig, "hp_sharp_vs_flat.png")


# 9. hp_batch_results.png — REAL bar chart of accuracy + time
print("  → training 3 batch_size experiments (32, 512, full=1600) ...")
EPOCHS_BS = 30

m_b32 = build_model(lr=0.001)
t0 = time.time()
h_b32 = m_b32.fit(X_train, y_train, epochs=EPOCHS_BS, batch_size=32,
                  validation_data=(X_val, y_val), verbose=0)
t_b32 = time.time() - t0
acc_b32 = h_b32.history['val_accuracy'][-1]

m_b512 = build_model(lr=0.001)
t0 = time.time()
h_b512 = m_b512.fit(X_train, y_train, epochs=EPOCHS_BS, batch_size=512,
                    validation_data=(X_val, y_val), verbose=0)
t_b512 = time.time() - t0
acc_b512 = h_b512.history['val_accuracy'][-1]

full_bs = len(X_train)
m_bfull = build_model(lr=0.001)
t0 = time.time()
h_bfull = m_bfull.fit(X_train, y_train, epochs=EPOCHS_BS, batch_size=full_bs,
                      validation_data=(X_val, y_val), verbose=0)
t_bfull = time.time() - t0
acc_bfull = h_bfull.history['val_accuracy'][-1]

print(f"     bs=32   acc={acc_b32:.4f} time={t_b32:.1f}s")
print(f"     bs=512  acc={acc_b512:.4f} time={t_b512:.1f}s")
print(f"     bs=full acc={acc_bfull:.4f} time={t_bfull:.1f}s")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
labels = ['bs = 32', 'bs = 512', f'bs = {full_bs}\n(full batch)']
accs   = [acc_b32, acc_b512, acc_bfull]
times  = [t_b32, t_b512, t_bfull]
colours = [ACCENT, VIOLET, ORANGE]

bars = axes[0].bar(labels, accs, color=colours, edgecolor='white', linewidth=2)
for bar, a in zip(bars, accs):
    axes[0].text(bar.get_x() + bar.get_width() / 2, a + 0.005,
                 f'{a:.3f}', ha='center', fontsize=11, color=DARK,
                 fontweight='bold')
axes[0].set_ylabel('val_accuracy')
axes[0].set_title('Final validation accuracy')
axes[0].set_ylim(0, 1.05)
axes[0].grid(True, alpha=0.3, axis='y')

bars2 = axes[1].bar(labels, times, color=colours, edgecolor='white', linewidth=2)
for bar, t in zip(bars2, times):
    axes[1].text(bar.get_x() + bar.get_width() / 2, t + max(times) * 0.02,
                 f'{t:.1f}s', ha='center', fontsize=11, color=DARK,
                 fontweight='bold')
axes[1].set_ylabel('wall-clock time (s)')
axes[1].set_title('Wall-clock training time (30 epochs)')
axes[1].set_ylim(0, max(times) * 1.18)
axes[1].grid(True, alpha=0.3, axis='y')

fig.suptitle('Batch size trade-off — accuracy vs time (real lab numbers)',
             y=1.03)
fig.tight_layout()
save(fig, "hp_batch_results.png")


# ============================================================
# LECTURE 4 — Architecture Search
# ============================================================

# 10. hp_grid_heatmap.png — REAL grid search results
print("  → running grid search (3 widths × 3 depths = 9 models) ...")
units_options = [32, 64, 128]
depth_options = [1, 2, 3]
EPOCHS_GS = 30

grid = np.zeros((len(depth_options), len(units_options)))
params_grid = np.zeros_like(grid, dtype=int)
results = []
for di, depth in enumerate(depth_options):
    for ui, units in enumerate(units_options):
        m = build_model_search(units, depth)
        m.fit(X_train, y_train, epochs=EPOCHS_GS, batch_size=64,
              validation_data=(X_val, y_val), verbose=0)
        _, acc = m.evaluate(X_val, y_val, verbose=0)
        np_count = m.count_params()
        grid[di, ui] = acc
        params_grid[di, ui] = np_count
        results.append((units, depth, acc, np_count))
        print(f"     units={units:>3}, depth={depth} → acc={acc:.4f}, params={np_count:,}")

best_idx = np.unravel_index(np.argmax(grid), grid.shape)
best_units = units_options[best_idx[1]]
best_depth = depth_options[best_idx[0]]
best_acc = grid[best_idx]

fig, ax = plt.subplots(figsize=(8.5, 5.5))
im = ax.imshow(grid, cmap='YlGnBu', aspect='auto',
               vmin=grid.min() - 0.005, vmax=grid.max() + 0.005)
ax.set_xticks(range(len(units_options)))
ax.set_xticklabels([f'units={u}' for u in units_options])
ax.set_yticks(range(len(depth_options)))
ax.set_yticklabels([f'depth={d}' for d in depth_options])
for di in range(len(depth_options)):
    for ui in range(len(units_options)):
        is_best = (di, ui) == best_idx
        ax.text(ui, di - 0.12, f'{grid[di, ui]:.4f}', ha='center',
                fontsize=12, color=DARK,
                fontweight='bold' if is_best else 'normal')
        ax.text(ui, di + 0.22, f'{params_grid[di, ui]:,} params',
                ha='center', fontsize=9, color=GREY)
        if is_best:
            ax.add_patch(Rectangle((ui - 0.48, di - 0.48), 0.96, 0.96,
                                   fill=False, edgecolor=GOLD, linewidth=3.5))
ax.set_title(
    f'Grid search — every cell is one trained model\n'
    f'winner: units={best_units}, depth={best_depth}, val_acc={best_acc:.4f}',
    fontsize=12)
fig.colorbar(im, ax=ax, label='val_accuracy')
fig.tight_layout()
save(fig, "hp_grid_heatmap.png")


# 11. hp_grid_ranking.png — sorted bar chart of all 9 configs
results_sorted = sorted(results, key=lambda r: r[2], reverse=True)
labels = [f'u={u}, d={d}' for (u, d, _, _) in results_sorted]
accs   = [r[2] for r in results_sorted]
params = [r[3] for r in results_sorted]

fig, ax = plt.subplots(figsize=(11, 5))
colours = [GOLD if i == 0 else ACCENT for i in range(len(results_sorted))]
bars = ax.barh(range(len(labels)), accs, color=colours, edgecolor='white',
               linewidth=1.5)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel('val_accuracy')
ax.set_xlim(min(accs) - 0.01, max(accs) + 0.012)
for i, (bar, a, p) in enumerate(zip(bars, accs, params)):
    ax.text(a + 0.0008, bar.get_y() + bar.get_height() / 2,
            f'{a:.4f}  ({p:,} params)',
            va='center', fontsize=10, color=DARK,
            fontweight='bold' if i == 0 else 'normal')
ax.set_title('Architecture grid sorted by val_accuracy — winner highlighted in gold')
ax.grid(True, alpha=0.3, axis='x')
fig.tight_layout()
save(fig, "hp_grid_ranking.png")


print(f"\n11 hyperparameter tuning visuals written to {OUT}")
print(f"  LR results:    1e-3={h_ok.history['val_accuracy'][-1]:.4f}  "
      f"1e-1={h_big.history['val_accuracy'][-1]:.4f}  "
      f"1e-5={h_tiny.history['val_accuracy'][-1]:.4f}")
print(f"  Batch results: 32={acc_b32:.4f}  512={acc_b512:.4f}  "
      f"full={acc_bfull:.4f}")
print(f"  Grid winner:   units={best_units}, depth={best_depth}, "
      f"acc={best_acc:.4f}")
