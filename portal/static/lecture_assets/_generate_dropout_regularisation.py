"""
Generate visuals for the four Dropout / Regularisation lectures (Stage 3.2).
    python portal/static/lecture_assets/_generate_dropout_regularisation.py

Reproduces the imbalanced intrusion dataset (8000 samples, 15 features) used
by every Stage 3.2 solution_*.py file and trains the same 3 × Dense(256)
networks (baseline, dropout, batchnorm, batchnorm+dropout, early stopping)
so the curves match what learners see when they run the labs.
"""
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import warnings
warnings.filterwarnings("ignore")

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


# ── Reproduce the lab dataset (same as every Stage 3.2 solution) ──────────────
np.random.seed(42)
tf.random.set_seed(42)

X, y = make_classification(
    n_samples=8000, n_features=15, n_informative=10, n_redundant=3,
    weights=[0.92, 0.08], flip_y=0.03, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
sc = StandardScaler()
X_train_s = sc.fit_transform(X_train)
X_test_s  = sc.transform(X_test)
input_dim = X_train_s.shape[1]


def build_baseline():
    return keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dense(1,   activation='sigmoid'),
    ])


def build_dropout(rate=0.3):
    return keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(1,   activation='sigmoid'),
    ])


def build_batchnorm():
    return keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(1,   activation='sigmoid'),
    ])


def build_combined():
    return keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1,   activation='sigmoid'),
    ])


def fit(model, epochs=50, callbacks=None):
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model.fit(X_train_s, y_train, epochs=epochs, batch_size=64,
                     validation_split=0.15, callbacks=callbacks, verbose=0)


# ═════════════════════════════════════════════════════════════════════════════
# Train all the networks once, reuse histories for multiple visuals
# ═════════════════════════════════════════════════════════════════════════════
print("\n  → training baseline (no regularisation, 50 epochs)...")
np.random.seed(42); tf.random.set_seed(42)
m_base = build_baseline()
h_base = fit(m_base)

print("  → training Dropout(0.3) ...")
np.random.seed(42); tf.random.set_seed(42)
m_drop = build_dropout(0.3)
h_drop = fit(m_drop)

print("  → training rates 0.1 / 0.3 / 0.5 ...")
rate_results = {}
for r in [0.1, 0.3, 0.5]:
    np.random.seed(42); tf.random.set_seed(42)
    h = fit(build_dropout(r))
    rate_results[r] = h.history['val_accuracy'][-1]

print("  → training BatchNorm ...")
np.random.seed(42); tf.random.set_seed(42)
m_bn = build_batchnorm()
h_bn = fit(m_bn)

print("  → training BatchNorm + Dropout combined ...")
np.random.seed(42); tf.random.set_seed(42)
m_combined = build_combined()
h_combined = fit(m_combined)

print("  → training with EarlyStopping(patience=5) ...")
np.random.seed(42); tf.random.set_seed(42)
m_es = build_combined()
es_cb = keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=5, restore_best_weights=True, verbose=0)
h_es = fit(m_es, epochs=200, callbacks=[es_cb])

epochs_run = len(h_es.history['loss'])
val_losses = h_es.history['val_loss']
best_epoch = int(np.argmin(val_losses))
best_val_loss = val_losses[best_epoch]


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 1 — Demonstrate Overfitting
# ═════════════════════════════════════════════════════════════════════════════

# 1. dr_capacity_vs_data.png — visual: 134k params vs 5440 training samples
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis('off')

# Big block: parameters
n_params = m_base.count_params()
ax.add_patch(FancyBboxPatch((0.4, 1.0), 5.2, 3.2,
                            boxstyle="round,pad=0.05",
                            facecolor=RED, edgecolor='white', lw=2, alpha=0.85))
ax.text(3.0, 3.2, f'{n_params:,}', ha='center', va='center',
        fontsize=32, color='white', fontweight='bold')
ax.text(3.0, 2.0, 'trainable parameters', ha='center', va='center',
        fontsize=12, color='white')
ax.text(3.0, 1.4, '(3 × Dense(256))', ha='center', va='center',
        fontsize=10, color='white', style='italic')

# Small block: samples
n_train = int(len(X_train_s) * 0.85)
ax.add_patch(FancyBboxPatch((6.5, 1.7), 3.2, 1.8,
                            boxstyle="round,pad=0.05",
                            facecolor=ACCENT, edgecolor='white', lw=2, alpha=0.85))
ax.text(8.1, 2.9, f'{n_train:,}', ha='center', va='center',
        fontsize=22, color='white', fontweight='bold')
ax.text(8.1, 2.2, 'training samples', ha='center', va='center',
        fontsize=11, color='white')

# Ratio line
ratio = n_params / n_train
ax.text(5.5, 0.4, f'≈ {ratio:.0f} parameters per training sample — far too much capacity',
        ha='center', va='center', fontsize=12, color=DARK, fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor=LIGHT, edgecolor=GREY))

ax.set_title('Capacity dwarfs the data — the model can simply memorise', pad=10)
save(fig, "dr_capacity_vs_data.png")


# 2. dr_overfit_curves.png — REAL diverging train/val loss + acc curves
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
ep = range(1, len(h_base.history['loss']) + 1)

axes[0].plot(ep, h_base.history['loss'],     '-', color=ACCENT, lw=2.4, label='Train loss')
axes[0].plot(ep, h_base.history['val_loss'], '-', color=RED,    lw=2.4, label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Loss — train falls forever, val turns upward')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)
# Annotate divergence point: where val loss reaches min
min_val_ep = int(np.argmin(h_base.history['val_loss']))
min_val = h_base.history['val_loss'][min_val_ep]
axes[0].axvline(min_val_ep + 1, color=GREEN, ls='--', lw=1.4, alpha=0.7)
axes[0].text(min_val_ep + 1.3, min_val + 0.02, f'val min @ ep {min_val_ep + 1}',
             fontsize=9, color=GREEN)

axes[1].plot(ep, h_base.history['accuracy'],     '-', color=ACCENT, lw=2.4, label='Train acc')
axes[1].plot(ep, h_base.history['val_accuracy'], '-', color=RED,    lw=2.4, label='Val acc')
gap_final = h_base.history['accuracy'][-1] - h_base.history['val_accuracy'][-1]
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title(f'Accuracy — gap = {gap_final:.3f} at epoch 50')
axes[1].legend(loc='lower right')
axes[1].grid(True, alpha=0.3)

fig.suptitle('No regularisation, 3 × Dense(256) — overfitting in plain sight',
             y=1.02)
fig.tight_layout()
save(fig, "dr_overfit_curves.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 2 — Add Dropout
# ═════════════════════════════════════════════════════════════════════════════

# 3. dr_dropout_concept.png — neuron grids: training (some off) vs prediction (all on)
fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
rng = np.random.default_rng(7)

def draw_layer(ax, mask, title, edge_col):
    ax.set_xlim(0, 4); ax.set_ylim(0, 9); ax.axis('off')
    cols = 2; rows = 4
    for i in range(8):
        c = i % cols; r = i // cols
        x_ = 1.0 + c * 1.5
        y_ = 7.5 - r * 1.7
        keep = bool(mask[i])
        face = ACCENT if keep else LIGHT
        edge = ACCENT if keep else GREY
        ax.add_patch(Circle((x_, y_), 0.45, facecolor=face, edgecolor=edge,
                            lw=2.0, alpha=1.0 if keep else 0.6))
        if not keep:
            ax.plot([x_ - 0.30, x_ + 0.30], [y_ - 0.30, y_ + 0.30],
                    color=RED, lw=2.5)
            ax.plot([x_ - 0.30, x_ + 0.30], [y_ + 0.30, y_ - 0.30],
                    color=RED, lw=2.5)
    ax.set_title(title, color=edge_col, fontsize=12, fontweight='bold')

# Training batch 1
mask1 = np.array([1, 0, 1, 1, 0, 1, 1, 0])  # 3 dropped out of 8 (~37%)
draw_layer(axes[0], mask1, 'TRAINING — batch 1\nDropout(0.3) zeroes 3/8 randomly', ORANGE)

# Training batch 2 (different mask)
mask2 = np.array([1, 1, 0, 1, 1, 0, 0, 1])
draw_layer(axes[1], mask2, 'TRAINING — batch 2\ndifferent random set zeroed', ORANGE)

# Prediction (all on)
mask3 = np.ones(8, dtype=int)
draw_layer(axes[2], mask3, 'PREDICTION (model.predict)\nall neurons active', GREEN)

fig.suptitle('Dropout(0.3) in action — random during training, off during inference',
             y=1.02)
fig.tight_layout()
save(fig, "dr_dropout_concept.png")


# 4. dr_dropout_vs_baseline.png — REAL val_loss curves baseline vs dropout
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

axes[0].plot(ep, h_base.history['val_loss'], '-', color=GREY,   lw=2.4, label='No dropout (baseline)')
axes[0].plot(ep, h_drop.history['val_loss'], '-', color=ACCENT, lw=2.4, label='Dropout(0.3)')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Validation loss')
axes[0].set_title('Val loss — Dropout flattens the upward drift')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

axes[1].plot(ep, h_base.history['val_accuracy'], '-', color=GREY,   lw=2.4, label='No dropout')
axes[1].plot(ep, h_drop.history['val_accuracy'], '-', color=ACCENT, lw=2.4, label='Dropout(0.3)')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation accuracy')
axes[1].set_title('Val accuracy — Dropout reaches and holds the peak')
axes[1].legend(loc='lower right')
axes[1].grid(True, alpha=0.3)

base_final = h_base.history['val_loss'][-1]
drop_final = h_drop.history['val_loss'][-1]
fig.suptitle(f'Dropout(0.3) reduces val_loss from {base_final:.3f} to {drop_final:.3f}',
             y=1.02)
fig.tight_layout()
save(fig, "dr_dropout_vs_baseline.png")


# 5. dr_dropout_rates.png — bar chart of rates 0.1, 0.3, 0.5
fig, ax = plt.subplots(figsize=(8, 5))
rates = list(rate_results.keys())
accs  = list(rate_results.values())
colours = [LIGHT, ACCENT, ORANGE]
bars = ax.bar([f'rate = {r}' for r in rates], accs,
              color=colours, edgecolor='white', linewidth=2)
for bar, val in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.003,
            f'{val:.3f}', ha='center', va='bottom', fontsize=12,
            fontweight='bold', color=DARK)
best_idx = int(np.argmax(accs))
bars[best_idx].set_edgecolor(GREEN)
bars[best_idx].set_linewidth(3)
ax.set_ylabel('Final validation accuracy')
ax.set_title('Choosing the dropout rate — too little leaks, too much underfits')
ax.set_ylim(min(accs) - 0.02, max(accs) + 0.02)
ax.grid(True, alpha=0.3, axis='y')
save(fig, "dr_dropout_rates.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 3 — Batch Normalisation
# ═════════════════════════════════════════════════════════════════════════════

# 6. dr_batchnorm_distribution.png — histograms before/after BN
fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
rng = np.random.default_rng(11)

# Before BN: drifted distribution (mean=2.1, std=3.8)
raw = rng.normal(2.1, 3.8, 4000)
axes[0].hist(raw, bins=40, color=GREY, edgecolor='white', alpha=0.85)
axes[0].axvline(raw.mean(), color=RED, ls='--', lw=2)
axes[0].set_title('Before BN — drifted', color=GREY)
axes[0].set_xlabel(f'mean={raw.mean():.2f}, std={raw.std():.2f}')
axes[0].set_yticks([])
axes[0].set_xlim(-15, 20)

# After centring + scaling: mean=0, std=1
centred = (raw - raw.mean()) / raw.std()
axes[1].hist(centred, bins=40, color=ACCENT, edgecolor='white', alpha=0.85)
axes[1].axvline(0, color=RED, ls='--', lw=2)
axes[1].set_title('Centred + scaled', color=ACCENT)
axes[1].set_xlabel(f'mean={centred.mean():.2f}, std={centred.std():.2f}')
axes[1].set_yticks([])
axes[1].set_xlim(-5, 5)

# After learnable γ·z + β: small reshape
gamma, beta = 0.8, 0.3
final = gamma * centred + beta
axes[2].hist(final, bins=40, color=GREEN, edgecolor='white', alpha=0.85)
axes[2].axvline(beta, color=RED, ls='--', lw=2)
axes[2].set_title('After learned γ·z + β', color=GREEN)
axes[2].set_xlabel(f'mean={final.mean():.2f}, std={final.std():.2f}')
axes[2].set_yticks([])
axes[2].set_xlim(-5, 5)

fig.suptitle('What BatchNormalization does to one feature inside a mini-batch',
             y=1.02)
fig.tight_layout()
save(fig, "dr_batchnorm_distribution.png")


# 7. dr_batchnorm_smoothing.png — REAL train loss with vs without BN
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

axes[0].plot(ep, h_base.history['loss'], '-', color=GREY,   lw=2.0, label='No BatchNorm', alpha=0.9)
axes[0].plot(ep, h_bn.history['loss'],   '-', color=ACCENT, lw=2.4, label='With BatchNorm')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Training loss')
axes[0].set_title('Training loss — BN smooths the curve')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

axes[1].plot(ep, h_base.history['val_loss'], '-', color=GREY,   lw=2.0, label='No BatchNorm', alpha=0.9)
axes[1].plot(ep, h_bn.history['val_loss'],   '-', color=ACCENT, lw=2.4, label='With BatchNorm')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation loss')
axes[1].set_title('Validation loss — same trend, less wobble')
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

fig.suptitle('BatchNorm reduces noise during training (real lab numbers)', y=1.02)
fig.tight_layout()
save(fig, "dr_batchnorm_smoothing.png")


# 8. dr_combined_block.png — Dense → BN → Dropout block diagram
fig, ax = plt.subplots(figsize=(11.5, 4))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis('off')

stages = [
    ("Dense(256, relu)", 1.5, ACCENT, "compute activations"),
    ("BatchNormalization()", 5.0, ORANGE, "stabilise mean ≈ 0, std ≈ 1"),
    ("Dropout(0.3)", 8.5, VIOLET, "zero 30% of neurons"),
    ("→ next block", 11.5, GREY, "or final Dense head"),
]
for label, x_, col, sub in stages:
    ax.add_patch(FancyBboxPatch((x_ - 1.0, 1.6), 2.0, 1.6,
                                boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2))
    ax.text(x_, 2.4, label, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')
    ax.text(x_, 0.9, sub, ha='center', va='center', color=col, fontsize=9,
            style='italic')
for i in range(3):
    ax.annotate('', xy=(stages[i + 1][1] - 1.0, 2.4), xytext=(stages[i][1] + 1.0, 2.4),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.8))

ax.set_title('Recommended layer block: Dense → BatchNorm → Dropout', pad=15)
save(fig, "dr_combined_block.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 4 — Early Stopping
# ═════════════════════════════════════════════════════════════════════════════

# 9. dr_early_stopping_curves.png — REAL early stopping run with stop marker
fig, ax = plt.subplots(figsize=(11, 5.4))
ep_es = range(1, epochs_run + 1)

ax.plot(ep_es, h_es.history['loss'],     '-', color=ACCENT, lw=2.4, label='Train loss')
ax.plot(ep_es, h_es.history['val_loss'], '-', color=RED,    lw=2.4, label='Val loss')

# Best epoch marker
ax.plot(best_epoch + 1, best_val_loss, 'o', color=GOLD, markersize=14,
        markeredgecolor=DARK, markeredgewidth=1.4, zorder=5,
        label=f'Best val_loss @ epoch {best_epoch + 1}')

# Stop line
ax.axvline(epochs_run, color=GREY, ls='--', lw=1.8, alpha=0.8,
           label=f'Training stopped @ epoch {epochs_run}')
# Patience window shading
patience_start = best_epoch + 1
ax.axvspan(patience_start + 0.5, epochs_run + 0.5,
           alpha=0.10, color=ORANGE, label='5 non-improving epochs')

ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_title(f'EarlyStopping(patience=5, restore_best_weights=True) — '
             f'stopped after {epochs_run}/200 epochs')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
save(fig, "dr_early_stopping_curves.png")


# 10. dr_patience_timeline.png — patience counter logical timeline
fig, ax = plt.subplots(figsize=(11.5, 4.6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

events = [
    ('Epoch 15', 'val_loss = 0.170', '↓ best', GREEN, 0),
    ('Epoch 16', 'val_loss = 0.172', 'count=1', ORANGE, 1),
    ('Epoch 17', 'val_loss = 0.175', 'count=2', ORANGE, 2),
    ('Epoch 18', 'val_loss = 0.178', 'count=3', ORANGE, 3),
    ('Epoch 19', 'val_loss = 0.180', 'count=4', ORANGE, 4),
    ('Epoch 20', 'val_loss = 0.182', 'STOP — restore epoch 15', RED, 5),
]

for i, (lab, vl, note, col, idx) in enumerate(events):
    x_ = 0.6 + i * 2.05
    ax.add_patch(FancyBboxPatch((x_, 2.0), 1.8, 2.4, boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2, alpha=0.85))
    ax.text(x_ + 0.9, 3.7, lab, ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')
    ax.text(x_ + 0.9, 3.0, vl, ha='center', va='center', fontsize=9, color='white')
    ax.text(x_ + 0.9, 2.4, note, ha='center', va='center', fontsize=9,
            color='white', fontweight='bold')

# Bracket indicating "restore_best_weights" arrow from end to start
ax.annotate('', xy=(0.6 + 0.9, 1.85), xytext=(0.6 + 5 * 2.05 + 0.9, 1.85),
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5,
                            connectionstyle="arc3,rad=-0.25"))
ax.text(6.0, 0.8, 'restore_best_weights=True → rewind to epoch 15',
        ha='center', va='center', fontsize=11, color=DARK, fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor=LIGHT, edgecolor=GOLD))

ax.set_title('Patience counter walkthrough — patience=5', pad=10)
save(fig, "dr_patience_timeline.png")


print("\n10 dropout / regularisation visuals written to portal/static/lecture_assets/")
print(f"  baseline:        train={h_base.history['accuracy'][-1]:.3f}, val={h_base.history['val_accuracy'][-1]:.3f}")
print(f"  dropout(0.3):    val_loss {h_base.history['val_loss'][-1]:.3f} → {h_drop.history['val_loss'][-1]:.3f}")
print(f"  rates 0.1/0.3/0.5: {[f'{v:.3f}' for v in rate_results.values()]}")
print(f"  batchnorm:       val_loss = {h_bn.history['val_loss'][-1]:.3f}")
print(f"  combined BN+DO:  val_acc = {h_combined.history['val_accuracy'][-1]:.3f}")
print(f"  early stopping:  ran {epochs_run}/200 epochs, best @ {best_epoch + 1}")
