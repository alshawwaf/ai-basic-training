"""
Generate visuals for the four First-Neural-Network lectures (Stage 3.1).
    python portal/static/lecture_assets/_generate_first_neural_network.py

Reproduces the binary intrusion-detection dataset used by every Stage 3.1
solution_*.py file and trains the same Keras Sequential model so the
training-curve and AUC visuals match exactly what learners see when they
run the labs.
"""
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

import tensorflow as tf
from tensorflow import keras

OUT = Path(__file__).resolve().parent

DPI  = 140
SAVE = dict(dpi=DPI, bbox_inches="tight", facecolor="white")
ACCENT = "#0891b2"   # cyan — train / hidden
VIOLET = "#8b5cf6"
RED    = "#dc2626"   # validation / attack
ORANGE = "#f59e0b"
GREEN  = "#16a34a"
GREY   = "#64748b"
LIGHT  = "#e2e8f0"
DARK   = "#0f172a"

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


# ── Reproduce the lab dataset (same as solution_compile_and_train.py) ─────────
np.random.seed(42)
tf.random.set_seed(42)

X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=7, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 1 — From NumPy to Keras
# ═════════════════════════════════════════════════════════════════════════════

# 1. nn_dense_neuron.png — anatomy of a single Dense neuron
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis('off')

# Inputs on the left
input_y = [4.0, 3.0, 2.0, 1.0]
input_labels = ['x₁', 'x₂', 'x₃', 'x₄']
weights = ['w₁', 'w₂', 'w₃', 'w₄']
for yi, lab in zip(input_y, input_labels):
    ax.add_patch(Circle((1.0, yi), 0.30, facecolor=LIGHT, edgecolor=GREY, lw=1.6))
    ax.text(1.0, yi, lab, ha='center', va='center', fontsize=12, fontweight='bold', color=DARK)

# Sum node
sum_x, sum_y = 5.5, 2.5
ax.add_patch(Circle((sum_x, sum_y), 0.55, facecolor=ACCENT, edgecolor='white', lw=2))
ax.text(sum_x, sum_y, 'Σ', ha='center', va='center', fontsize=22, color='white', fontweight='bold')

# Lines from inputs to sum, with weight labels
for yi, w in zip(input_y, weights):
    ax.annotate('', xy=(sum_x - 0.55, sum_y), xytext=(1.30, yi),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
    mid_x = (1.30 + sum_x - 0.55) / 2
    mid_y = (yi + sum_y) / 2
    ax.text(mid_x, mid_y + 0.10, w, fontsize=10, color=ACCENT, fontweight='bold',
            ha='center', va='bottom')

# Bias
ax.add_patch(Circle((sum_x, 0.4), 0.25, facecolor=ORANGE, edgecolor='white', lw=1.5))
ax.text(sum_x, 0.4, 'b', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
ax.annotate('', xy=(sum_x, sum_y - 0.55), xytext=(sum_x, 0.65),
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.6))

# z label
ax.text(sum_x + 0.85, sum_y, 'z', fontsize=14, color=DARK, fontweight='bold')

# Activation box
act_x = 8.2
ax.add_patch(FancyBboxPatch((act_x - 0.55, sum_y - 0.55), 1.5, 1.1,
                            boxstyle="round,pad=0.05", facecolor=VIOLET,
                            edgecolor='white', lw=2))
ax.text(act_x + 0.20, sum_y, 'relu', ha='center', va='center',
        fontsize=14, color='white', fontweight='bold')
ax.annotate('', xy=(act_x - 0.55, sum_y), xytext=(sum_x + 0.55, sum_y),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=1.8))

# Output
out_x = 10.4
ax.annotate('', xy=(out_x, sum_y), xytext=(act_x + 0.95, sum_y),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=1.8))
ax.text(out_x + 0.15, sum_y, 'output', fontsize=11, color=DARK, ha='left', va='center')

# Stage labels
ax.text(1.0, 4.7, '1. inputs', ha='center', fontsize=10, color=GREY, style='italic')
ax.text(3.4, 4.7, '2. multiply by weights', ha='center', fontsize=10, color=GREY, style='italic')
ax.text(sum_x, 4.7, '3. sum + bias', ha='center', fontsize=10, color=GREY, style='italic')
ax.text(act_x + 0.2, 4.7, '4. activation', ha='center', fontsize=10, color=GREY, style='italic')

# Formula at the bottom
ax.text(5.5, -0.05, r'output = relu( x₁·w₁ + x₂·w₂ + x₃·w₃ + x₄·w₄ + b )',
        ha='center', va='center', fontsize=12, color=DARK,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=LIGHT, edgecolor=GREY))

ax.set_title('Inside one Dense neuron: multiply, sum, activate', pad=10)
save(fig, "nn_dense_neuron.png")


# 2. nn_sequential_wiring.png — every input connects to every neuron
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis('off')

# Layer 0: 4 inputs
input_xs = [1.0] * 4
input_ys = np.linspace(1.0, 6.0, 4)
for x_, y_ in zip(input_xs, input_ys):
    ax.add_patch(Circle((x_, y_), 0.28, facecolor=LIGHT, edgecolor=GREY, lw=1.5))

# Layer 1: 8 hidden
hid_xs = [5.5] * 8
hid_ys = np.linspace(0.4, 6.6, 8)
for x_, y_ in zip(hid_xs, hid_ys):
    ax.add_patch(Circle((x_, y_), 0.30, facecolor=ACCENT, edgecolor='white', lw=1.6))

# Layer 2: 1 output
out_x, out_y = 9.5, 3.5
ax.add_patch(Circle((out_x, out_y), 0.36, facecolor=RED, edgecolor='white', lw=2))
ax.text(out_x, out_y, 'σ', ha='center', va='center', color='white',
        fontsize=14, fontweight='bold')

# All inputs → all hidden
for x_in, y_in in zip(input_xs, input_ys):
    for x_h, y_h in zip(hid_xs, hid_ys):
        ax.plot([x_in + 0.28, x_h - 0.30], [y_in, y_h],
                color=GREY, lw=0.7, alpha=0.45, zorder=0)

# All hidden → output
for x_h, y_h in zip(hid_xs, hid_ys):
    ax.plot([x_h + 0.30, out_x - 0.36], [y_h, out_y],
            color=GREY, lw=0.7, alpha=0.55, zorder=0)

# Layer headers
ax.text(1.0, 6.65, 'Input\n(4 features)', ha='center', fontsize=11, color=DARK, fontweight='bold')
ax.text(5.5, 6.95, 'Dense(8, relu)', ha='center', fontsize=11, color=ACCENT, fontweight='bold')
ax.text(9.5, 4.10, 'Dense(1, sigmoid)', ha='center', fontsize=11, color=RED, fontweight='bold')

# Param annotations under each layer
ax.text(5.5, -0.05, '(4 × 8) + 8  =  40 params', ha='center', fontsize=10, color=ACCENT)
ax.text(9.5, -0.05, '(8 × 1) + 1  =   9 params', ha='center', fontsize=10, color=RED)
ax.text(5.5, -0.55, 'Total: 49 trainable parameters', ha='center', fontsize=11, color=DARK,
        fontweight='bold')

ax.set_title('All-to-all wiring of a Sequential([Dense(8), Dense(1)]) network',
             pad=12)
save(fig, "nn_sequential_wiring.png")


# 3. nn_param_count.png — visual breakdown of Dense(8) parameters as a grid
fig, ax = plt.subplots(figsize=(9.5, 5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis('off')

# Weight matrix grid (4 inputs × 8 neurons)
grid_x0, grid_y0 = 0.7, 1.4
cell = 0.42
for i in range(4):
    for j in range(8):
        ax.add_patch(Rectangle((grid_x0 + j * cell, grid_y0 + (3 - i) * cell),
                               cell, cell, facecolor=ACCENT, edgecolor='white', lw=0.8))
ax.text(grid_x0 + 4 * cell, grid_y0 + 4.4 * cell,
        'Weight matrix W: shape (4, 8)', ha='center', fontsize=11, color=ACCENT,
        fontweight='bold')
ax.text(grid_x0 + 4 * cell, grid_y0 - 0.4,
        '4 × 8 = 32 weights', ha='center', fontsize=11, color=DARK)

# Bias vector (1 × 8)
bias_x0 = grid_x0 + 8 * cell + 0.6
bias_y0 = grid_y0 + 1.5 * cell
for j in range(8):
    ax.add_patch(Rectangle((bias_x0, bias_y0 + (7 - j) * cell * 0.3 + 0.3),
                           cell, cell * 0.3, facecolor=ORANGE, edgecolor='white', lw=0.8))
ax.text(bias_x0 + cell / 2, grid_y0 + 4.4 * cell,
        'Bias b: shape (8,)', ha='center', fontsize=11, color=ORANGE,
        fontweight='bold')
ax.text(bias_x0 + cell / 2, grid_y0 - 0.4,
        '8 biases', ha='center', fontsize=11, color=DARK)

# Plus / equals
ax.text(bias_x0 - 0.35, grid_y0 + 2 * cell, '+', ha='center', va='center',
        fontsize=24, color=DARK, fontweight='bold')
ax.text(bias_x0 + cell + 0.35, grid_y0 + 2 * cell, '=', ha='center', va='center',
        fontsize=24, color=DARK, fontweight='bold')

# Total
total_x = bias_x0 + cell + 0.95
ax.add_patch(FancyBboxPatch((total_x, grid_y0 + 1 * cell), 1.6, 1.4 * cell,
                            boxstyle="round,pad=0.05", facecolor=GREEN,
                            edgecolor='white', lw=2))
ax.text(total_x + 0.8, grid_y0 + 1.7 * cell, '40', ha='center', va='center',
        fontsize=24, color='white', fontweight='bold')
ax.text(total_x + 0.8, grid_y0 - 0.4, 'total params',
        ha='center', fontsize=11, color=GREEN, fontweight='bold')

ax.set_title('Counting parameters in Dense(8) over a 4-feature input', pad=15)
save(fig, "nn_param_count.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 2 — Build the Network (activations + output heads)
# ═════════════════════════════════════════════════════════════════════════════

# 4. nn_activation_functions.png — ReLU, Sigmoid, Softmax
fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))

x = np.linspace(-6, 6, 400)

# ReLU
axes[0].plot(x, np.maximum(0, x), color=ACCENT, lw=3)
axes[0].axhline(0, color=GREY, lw=0.6)
axes[0].axvline(0, color=GREY, lw=0.6)
axes[0].fill_between(x, np.maximum(0, x), 0, color=ACCENT, alpha=0.15)
axes[0].set_title('ReLU — for hidden layers', color=ACCENT)
axes[0].set_xlabel('input z')
axes[0].set_ylabel('relu(z) = max(0, z)')
axes[0].grid(True, alpha=0.3)
axes[0].text(-5, 4, '"off" for\nnegative input', fontsize=10, color=GREY)
axes[0].text(2, 1, 'linear ramp\nfor positive', fontsize=10, color=ACCENT)

# Sigmoid
sig = 1 / (1 + np.exp(-x))
axes[1].plot(x, sig, color=RED, lw=3)
axes[1].axhline(0, color=GREY, lw=0.6); axes[1].axhline(1, color=GREY, lw=0.6, ls=':')
axes[1].axvline(0, color=GREY, lw=0.6)
axes[1].fill_between(x, sig, 0, color=RED, alpha=0.12)
axes[1].set_title('Sigmoid — for binary output', color=RED)
axes[1].set_xlabel('input z')
axes[1].set_ylabel('1 / (1 + exp(-z))')
axes[1].set_ylim(-0.1, 1.15)
axes[1].grid(True, alpha=0.3)
axes[1].text(-5.5, 0.85, 'P(positive class)\n∈ [0, 1]', fontsize=10, color=RED)

# Softmax (3 classes)
labels = ['class A', 'class B', 'class C']
logits = np.array([2.0, 1.0, 0.1])
exps = np.exp(logits - logits.max())
probs = exps / exps.sum()
axes[2].bar(labels, probs, color=[VIOLET, ORANGE, ACCENT], edgecolor='white', lw=2)
for i, p in enumerate(probs):
    axes[2].text(i, p + 0.02, f'{p:.2f}', ha='center', fontsize=11, fontweight='bold')
axes[2].set_title('Softmax — for N-class output', color=VIOLET)
axes[2].set_ylabel('probability')
axes[2].set_ylim(0, 1)
axes[2].grid(True, alpha=0.3, axis='y')
axes[2].text(1.0, 0.92, f'sums to {probs.sum():.2f}',
             ha='center', fontsize=10, color=GREY, style='italic')

fig.suptitle('Three activation functions and where each one belongs', y=1.02)
fig.tight_layout()
save(fig, "nn_activation_functions.png")


# 5. nn_output_heads.png — binary vs multiclass output layer comparison
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

# Binary head
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
# Hidden layer (3 dots)
for yh in [2.0, 3.0, 4.0]:
    ax.add_patch(Circle((2.0, yh), 0.27, facecolor=ACCENT, edgecolor='white', lw=1.5))
ax.text(2.0, 5.0, 'Hidden\nDense(64, relu)', ha='center', fontsize=10, color=ACCENT,
        fontweight='bold')
# Single sigmoid output
ax.add_patch(Circle((5.5, 3.0), 0.40, facecolor=RED, edgecolor='white', lw=2))
ax.text(5.5, 3.0, 'σ', ha='center', va='center', color='white', fontsize=18, fontweight='bold')
ax.text(5.5, 4.2, 'Dense(1, sigmoid)', ha='center', fontsize=10, color=RED, fontweight='bold')
# Connect
for yh in [2.0, 3.0, 4.0]:
    ax.plot([2.27, 5.10], [yh, 3.0], color=GREY, lw=0.7, alpha=0.6)
# Output box
ax.add_patch(FancyBboxPatch((7.0, 2.5), 2.5, 1.0, boxstyle="round,pad=0.05",
                            facecolor=LIGHT, edgecolor=RED, lw=1.6))
ax.text(8.25, 3.0, '0.82', ha='center', va='center', fontsize=16, color=DARK,
        fontweight='bold')
ax.text(8.25, 1.95, 'P(attack)', ha='center', fontsize=10, color=GREY, style='italic')
ax.annotate('', xy=(7.0, 3.0), xytext=(5.90, 3.0),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=1.6))
ax.set_title('Binary classification', color=RED, fontsize=13, fontweight='bold')
ax.text(5, 0.6, 'loss: binary_crossentropy', ha='center', fontsize=10, color=GREY,
        style='italic')

# Multiclass head
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
for yh in [2.0, 3.0, 4.0]:
    ax.add_patch(Circle((2.0, yh), 0.27, facecolor=ACCENT, edgecolor='white', lw=1.5))
ax.text(2.0, 5.0, 'Hidden\nDense(64, relu)', ha='center', fontsize=10, color=ACCENT,
        fontweight='bold')
# 3 softmax outputs
out_ys = [4.0, 3.0, 2.0]
out_cols = [VIOLET, ORANGE, ACCENT]
for yo, col in zip(out_ys, out_cols):
    ax.add_patch(Circle((5.5, yo), 0.32, facecolor=col, edgecolor='white', lw=1.6))
ax.text(5.5, 5.0, 'Dense(3, softmax)', ha='center', fontsize=10, color=VIOLET,
        fontweight='bold')
# Connect
for yh in [2.0, 3.0, 4.0]:
    for yo in out_ys:
        ax.plot([2.27, 5.18], [yh, yo], color=GREY, lw=0.6, alpha=0.5)
# Output box (3 numbers)
ax.add_patch(FancyBboxPatch((7.0, 2.0), 2.5, 2.0, boxstyle="round,pad=0.05",
                            facecolor=LIGHT, edgecolor=VIOLET, lw=1.6))
labels_out = [('0.66', VIOLET), ('0.24', ORANGE), ('0.10', ACCENT)]
for (val, col), yo in zip(labels_out, [3.55, 3.0, 2.45]):
    ax.text(7.6, yo, '●', color=col, fontsize=14, ha='center', va='center')
    ax.text(8.4, yo, val, fontsize=12, ha='left', va='center', color=DARK,
            fontweight='bold')
ax.text(8.25, 1.55, 'sums to 1.00', ha='center', fontsize=10, color=GREY, style='italic')
for yo, (_, col) in zip(out_ys, labels_out):
    ax.annotate('', xy=(7.0, [3.55, 3.0, 2.45][out_ys.index(yo)]), xytext=(5.82, yo),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.0, alpha=0.6))
ax.set_title('Multi-class (3 classes)', color=VIOLET, fontsize=13, fontweight='bold')
ax.text(5, 0.6, 'loss: sparse_categorical_crossentropy', ha='center', fontsize=10,
        color=GREY, style='italic')

fig.suptitle('Same hidden layer, two output heads — pick the one that matches the problem',
             y=1.02)
fig.tight_layout()
save(fig, "nn_output_heads.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 3 — Compile and Train (training loop + real curves)
# ═════════════════════════════════════════════════════════════════════════════

# 6. nn_training_loop.png — forward + backward pass diagram
fig, ax = plt.subplots(figsize=(12, 4.8))
ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis('off')

# Forward pass row (top)
boxes_fwd = [
    ("Batch input\n(32 × 10)", 1.0, ACCENT),
    ("Dense(64)\nrelu", 4.0, ACCENT),
    ("Dense(1)\nsigmoid", 7.0, ACCENT),
    ("Loss\n(BCE)", 10.0, RED),
]
for label, x_, col in boxes_fwd:
    ax.add_patch(FancyBboxPatch((x_ - 0.85, 4.2), 1.7, 1.2,
                                boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2))
    ax.text(x_, 4.8, label, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')

for i in range(3):
    x_a = boxes_fwd[i][1] + 0.85
    x_b = boxes_fwd[i + 1][1] - 0.85
    ax.annotate('', xy=(x_b, 4.8), xytext=(x_a, 4.8),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

ax.text(5.5, 5.7, 'FORWARD PASS — predict → compute loss', ha='center',
        fontsize=11, color=DARK, fontweight='bold')

# Backward pass row (bottom)
boxes_bwd = [
    ("Update W₁", 1.0, ORANGE),
    ("Grad W₁", 4.0, VIOLET),
    ("Grad W₂", 7.0, VIOLET),
    ("∂L/∂output", 10.0, RED),
]
for label, x_, col in boxes_bwd:
    ax.add_patch(FancyBboxPatch((x_ - 0.85, 1.4), 1.7, 1.2,
                                boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2))
    ax.text(x_, 2.0, label, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')

# Backward arrows go right-to-left
for i in range(3):
    x_a = boxes_bwd[i + 1][1] - 0.85
    x_b = boxes_bwd[i][1] + 0.85
    ax.annotate('', xy=(x_b, 2.0), xytext=(x_a, 2.0),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

ax.text(5.5, 0.7, 'BACKWARD PASS — propagate gradients → update weights',
        ha='center', fontsize=11, color=DARK, fontweight='bold')

# Vertical arrow loss → grad
ax.annotate('', xy=(10.0, 2.6), xytext=(10.0, 4.2),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

# Loop annotation on the right
ax.add_patch(FancyBboxPatch((12.3, 1.4), 1.5, 4.0,
                            boxstyle="round,pad=0.05",
                            facecolor=LIGHT, edgecolor=GREEN, lw=2))
ax.text(13.05, 4.6, 'one\nbatch', ha='center', va='center', fontsize=10,
        color=GREEN, fontweight='bold')
ax.text(13.05, 3.0, '×', ha='center', va='center', fontsize=20, color=GREEN)
ax.text(13.05, 2.0, 'one\nepoch', ha='center', va='center', fontsize=10,
        color=GREEN, fontweight='bold')

ax.set_title('One mini-batch step inside model.fit(): forward, then backward')
save(fig, "nn_training_loop.png")


# 7. nn_training_curves.png — REAL training curves from solution 3 model
print("\n  → training the lecture-3 model for real curves (this takes ~30s)...")
np.random.seed(42)
tf.random.set_seed(42)

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid'),
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
hist = model.fit(X_train_s, y_train, epochs=100, batch_size=32,
                 validation_split=0.2, verbose=0)

train_loss = hist.history['loss']
val_loss   = hist.history['val_loss']
train_acc  = hist.history['accuracy']
val_acc    = hist.history['val_accuracy']
best_epoch = int(np.argmax(val_acc)) + 1
best_val   = max(val_acc)
final_val  = val_acc[-1]
final_train = train_acc[-1]

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
epochs_range = range(1, len(train_loss) + 1)

# Loss
axes[0].plot(epochs_range, train_loss, '-', color=ACCENT, lw=2.4, label='Train loss')
axes[0].plot(epochs_range, val_loss,   '-', color=RED,    lw=2.4, label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss (binary cross-entropy)')
axes[0].set_title('Loss curves — both fall together')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

# Accuracy
axes[1].plot(epochs_range, train_acc, '-', color=ACCENT, lw=2.4, label='Train accuracy')
axes[1].plot(epochs_range, val_acc,   '-', color=RED,    lw=2.4, label='Val accuracy')
axes[1].axvline(best_epoch, color=GREEN, linestyle='--', lw=1.6,
                label=f'Peak val @ epoch {best_epoch}')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Accuracy curves — train climbs slightly above val')
axes[1].legend(loc='lower right')
axes[1].grid(True, alpha=0.3)

fig.suptitle(f'Real model.fit() history — 100 epochs, val peak={best_val:.3f} at epoch {best_epoch}',
             y=1.02)
fig.tight_layout()
save(fig, "nn_training_curves.png")


# 8. nn_validation_split.png — train / val / test split layout
fig, ax = plt.subplots(figsize=(11, 2.8))
total = 2000

# Top bar: X_train + X_test
sizes = [1280, 320, 400]   # 80% of 1600 training, 20% of 1600 (val), 400 test
labels = ['Training portion (1280)', 'Validation (320)', 'Test (400)']
roles  = ['weights actually update here',
          'per-epoch monitoring (no updates)',
          'sealed until the very end']
colours = [ACCENT, ORANGE, RED]

start = 0
for n, lab, role, col in zip(sizes, labels, roles, colours):
    ax.barh(0, n, left=start, height=0.55, color=col, edgecolor='white', linewidth=2)
    ax.text(start + n / 2, 0, lab, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')
    ax.text(start + n / 2, -0.55, role, ha='center', va='center',
            color=col, fontsize=9, style='italic')
    start += n

# Bracket showing X_train vs X_test
ax.annotate('', xy=(0, 0.45), xytext=(1600, 0.45),
            arrowprops=dict(arrowstyle='-', color=GREY, lw=1.5))
ax.text(800, 0.55, 'X_train (1600 — fed to model.fit)', ha='center', fontsize=9, color=GREY)
ax.annotate('', xy=(1600, 0.45), xytext=(2000, 0.45),
            arrowprops=dict(arrowstyle='-', color=GREY, lw=1.5))
ax.text(1800, 0.55, 'X_test (untouched)', ha='center', fontsize=9, color=GREY)

ax.set_xlim(0, total)
ax.set_ylim(-1.2, 0.9)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title('Where validation_split=0.2 carves the data inside model.fit()', pad=12)
save(fig, "nn_validation_split.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 4 — Evaluate and Improve
# ═════════════════════════════════════════════════════════════════════════════

# 9. nn_threshold_pipeline.png — probability → label flow
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off')

samples = [
    (0.92, 1, 'attack'),
    (0.14, 0, 'benign'),
    (0.67, 1, 'attack'),
    (0.03, 0, 'benign'),
]

# Probabilities column
ax.text(1.5, 5.4, 'sigmoid output', ha='center', fontsize=11, color=ACCENT, fontweight='bold')
for i, (p, lab, _) in enumerate(samples):
    y_pos = 4.4 - i * 0.9
    ax.add_patch(FancyBboxPatch((0.6, y_pos - 0.30), 1.8, 0.60,
                                boxstyle="round,pad=0.04",
                                facecolor=ACCENT, edgecolor='white', lw=1.6, alpha=0.85))
    ax.text(1.5, y_pos, f'{p:.2f}', ha='center', va='center',
            color='white', fontsize=12, fontweight='bold')

# Threshold step
thresh_x = 5.5
ax.text(thresh_x, 5.4, '> 0.5 ?', ha='center', fontsize=11, color=DARK, fontweight='bold')
for i, (p, lab, _) in enumerate(samples):
    y_pos = 4.4 - i * 0.9
    ax.annotate('', xy=(thresh_x - 0.5, y_pos), xytext=(2.4, y_pos),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
    mark = '✓' if p > 0.5 else '✗'
    col = GREEN if p > 0.5 else GREY
    ax.text(thresh_x, y_pos, mark, ha='center', va='center', fontsize=18, color=col,
            fontweight='bold')

# Labels column
label_x = 9.0
ax.text(label_x, 5.4, 'predicted label', ha='center', fontsize=11, color=RED,
        fontweight='bold')
for i, (p, lab, name) in enumerate(samples):
    y_pos = 4.4 - i * 0.9
    ax.annotate('', xy=(label_x - 0.85, y_pos), xytext=(thresh_x + 0.4, y_pos),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
    col = RED if lab == 1 else ACCENT
    ax.add_patch(FancyBboxPatch((label_x - 0.75, y_pos - 0.30), 2.4, 0.60,
                                boxstyle="round,pad=0.04",
                                facecolor=col, edgecolor='white', lw=1.6, alpha=0.85))
    ax.text(label_x + 0.45, y_pos, f'{lab} — {name}', ha='center', va='center',
            color='white', fontsize=11, fontweight='bold')

ax.set_title('From raw sigmoid probability to a class label', pad=10)
save(fig, "nn_threshold_pipeline.png")


# 10. nn_nn_vs_lr_auc.png — REAL AUC comparison from lecture-4 dataset
print("\n  → training the lecture-4 NN + LR for AUC comparison...")
np.random.seed(42)
tf.random.set_seed(42)

X4, y4 = make_classification(
    n_samples=5000, n_features=12, n_informative=8, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42)
X4_tr, X4_te, y4_tr, y4_te = train_test_split(
    X4, y4, test_size=0.2, random_state=42, stratify=y4)
sc4 = StandardScaler()
X4_trs = sc4.fit_transform(X4_tr)
X4_tes = sc4.transform(X4_te)

nn = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(X4_trs.shape[1],)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid'),
])
nn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
nn.fit(X4_trs, y4_tr, epochs=60, batch_size=64, validation_split=0.15, verbose=0)
nn_proba = nn.predict(X4_tes, verbose=0).flatten()
nn_auc = roc_auc_score(y4_te, nn_proba)

np.random.seed(42)
tf.random.set_seed(42)
nn_deep = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X4_trs.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid'),
])
nn_deep.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
nn_deep.fit(X4_trs, y4_tr, epochs=60, batch_size=64, validation_split=0.15, verbose=0)
nn_deep_proba = nn_deep.predict(X4_tes, verbose=0).flatten()
nn_deep_auc = roc_auc_score(y4_te, nn_deep_proba)

lr = LogisticRegression(max_iter=1000, random_state=42).fit(X4_trs, y4_tr)
lr_proba = lr.predict_proba(X4_tes)[:, 1]
lr_auc   = roc_auc_score(y4_te, lr_proba)

names  = ['Logistic\nRegression', '2-layer\nNN', '3-layer\nNN']
aucs   = [lr_auc, nn_auc, nn_deep_auc]
colours = [GREY, ACCENT, VIOLET]

fig, ax = plt.subplots(figsize=(8.5, 5.2))
bars = ax.bar(names, aucs, color=colours, edgecolor='white', linewidth=2)
for bar, val in zip(bars, aucs):
    ax.text(bar.get_x() + bar.get_width() / 2,
            val + 0.005, f'{val:.3f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold', color=DARK)
ax.set_ylabel('Test ROC-AUC')
ax.set_ylim(0.5, 1.02)
ax.axhline(0.5, color=GREY, ls='--', lw=1, label='random (AUC = 0.5)')
ax.set_title('AUC: simple baseline vs neural networks on the same test set')
ax.grid(True, alpha=0.3, axis='y')
ax.legend(loc='lower right', fontsize=9)
save(fig, "nn_nn_vs_lr_auc.png")


print("\n10 first-neural-network visuals written to portal/static/lecture_assets/")
print(f"  training-curves model: train={final_train:.3f}, val={final_val:.3f}, peak={best_val:.3f} @ epoch {best_epoch}")
print(f"  AUC: LR={lr_auc:.3f}, 2-NN={nn_auc:.3f}, 3-NN={nn_deep_auc:.3f}")
