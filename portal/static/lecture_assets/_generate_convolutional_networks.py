"""
Generate visuals for the four CNN lectures (Stage 3.3).
    python portal/static/lecture_assets/_generate_convolutional_networks.py

Trains the same Dense baseline and 2-conv CNN on MNIST that the
Stage 3.3 solution_*.py files use, then renders 10 visuals (image vs
flat vector, parameter comparison, shuffled-pixels demo, filter sliding,
max-pooling, shape trace, full architecture, real training curves,
CNN vs Dense bar chart, synthetic malware-family fingerprints).
"""
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

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


# ── Load MNIST ────────────────────────────────────────────────────────────────
print("\n  → loading MNIST ...")
np.random.seed(42)
tf.random.set_seed(42)
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0
X_train_4d = X_train[..., np.newaxis]
X_test_4d  = X_test[..., np.newaxis]
X_train_flat = X_train.reshape(-1, 784)
X_test_flat  = X_test.reshape(-1, 784)


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 1 — Why Dense Fails on Images
# ═════════════════════════════════════════════════════════════════════════════

# 1. cnn_image_vs_flat.png — same digit as 2D grid AND as 784-bar vector
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6),
                         gridspec_kw={'width_ratios': [1, 3]})
sample_idx = 7
img = X_test[sample_idx]
flat = X_test_flat[sample_idx]

axes[0].imshow(img, cmap='gray', interpolation='nearest')
axes[0].set_title(f'What you see — 28 × 28 image (digit: {y_test[sample_idx]})',
                  fontsize=11, color=DARK)
axes[0].set_xticks([]); axes[0].set_yticks([])
for s in axes[0].spines.values():
    s.set_color(ACCENT); s.set_linewidth(2)

axes[1].bar(range(784), flat, width=1.0, color=GREY)
axes[1].set_title('What Dense sees — 784 numbers, no spatial relationship',
                  fontsize=11, color=DARK)
axes[1].set_xlabel('pixel index (0 → 783)')
axes[1].set_ylabel('pixel value')
axes[1].set_xlim(0, 784)
axes[1].set_ylim(0, 1.05)
axes[1].grid(True, alpha=0.3, axis='y')

fig.suptitle('Same image, two representations', y=1.02)
fig.tight_layout()
save(fig, "cnn_image_vs_flat.png")


# 2. cnn_dense_vs_cnn_params.png — parameter cost comparison
fig, ax = plt.subplots(figsize=(10, 5))
labels = ['Dense(128)\non flat 784', 'Conv2D(32, 3×3)\non 28×28×1']
counts = [(784 * 128) + 128, (3 * 3 * 1 * 32) + 32]
colours = [RED, ACCENT]
bars = ax.bar(labels, counts, color=colours, edgecolor='white', linewidth=2,
              width=0.55)
for bar, c in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, c + 2000,
            f'{c:,}', ha='center', va='bottom', fontsize=14,
            color=DARK, fontweight='bold')
ax.set_ylabel('Trainable parameters')
ax.set_title('Parameter cost — Dense vs Conv2D for the same MNIST input')
ax.set_ylim(0, max(counts) * 1.15)
ax.grid(True, alpha=0.3, axis='y')
ratio = counts[0] / counts[1]
ax.text(0.5, 0.85, f'Dense uses {ratio:.0f}× more parameters',
        ha='center', fontsize=12, color=ORANGE, fontweight='bold',
        transform=ax.transAxes)
save(fig, "cnn_dense_vs_cnn_params.png")


# 3. cnn_shuffled_pixels.png — original vs shuffled-pixel digit (Dense indifferent)
fig, axes = plt.subplots(1, 2, figsize=(9, 4.4))
np.random.seed(42)
perm = np.random.permutation(784)
shuffled_img = flat[perm].reshape(28, 28)

axes[0].imshow(img, cmap='gray', interpolation='nearest')
axes[0].set_title('Original — humans see "7"', color=ACCENT, fontsize=12)
axes[0].set_xticks([]); axes[0].set_yticks([])

axes[1].imshow(shuffled_img, cmap='gray', interpolation='nearest')
axes[1].set_title('Same pixels, shuffled positions', color=RED, fontsize=12)
axes[1].set_xticks([]); axes[1].set_yticks([])

fig.suptitle('Dense scores ≈ identically on both — it has no spatial awareness',
             y=1.02, fontsize=12)
fig.tight_layout()
save(fig, "cnn_shuffled_pixels.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 2 — Conv2D and MaxPooling2D
# ═════════════════════════════════════════════════════════════════════════════

# 4. cnn_filter_slide.png — 3×3 filter sliding over a 6×6 input, three positions
fig, ax = plt.subplots(figsize=(11, 5.6))
ax.set_xlim(0, 14); ax.set_ylim(0, 7); ax.axis('off')

# Input grid (6×6)
grid_x0, grid_y0 = 0.5, 0.5
cell = 0.6
np.random.seed(3)
input_vals = np.random.randint(0, 10, (6, 6))
for i in range(6):
    for j in range(6):
        v = input_vals[i, j]
        shade = 0.92 - v * 0.06
        ax.add_patch(Rectangle((grid_x0 + j * cell, grid_y0 + (5 - i) * cell),
                               cell, cell, facecolor=(shade, shade, shade),
                               edgecolor='white', lw=1))
        ax.text(grid_x0 + j * cell + cell / 2,
                grid_y0 + (5 - i) * cell + cell / 2,
                str(v), ha='center', va='center', fontsize=9, color=DARK)
ax.text(grid_x0 + 3 * cell, grid_y0 + 6 * cell + 0.15,
        '6 × 6 input', ha='center', fontsize=10, color=DARK)

# Highlight three sliding positions of a 3x3 filter
positions = [(0, 0, ORANGE), (1, 2, GREEN), (3, 3, VIOLET)]
for top_i, top_j, col in positions:
    x_ = grid_x0 + top_j * cell
    y_ = grid_y0 + (5 - top_i - 2) * cell
    ax.add_patch(Rectangle((x_, y_), 3 * cell, 3 * cell,
                           facecolor='none', edgecolor=col, lw=2.4))

# Filter (3×3) on the right
filt_x0 = 5.6
ax.text(filt_x0 + 1.5 * cell, grid_y0 + 5.6 * cell,
        '3 × 3 filter (shared weights)',
        ha='center', fontsize=10, color=ACCENT)
filt_vals = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
for i in range(3):
    for j in range(3):
        ax.add_patch(Rectangle((filt_x0 + j * cell, grid_y0 + (4 - i) * cell),
                               cell, cell, facecolor=ACCENT, edgecolor='white', lw=1))
        ax.text(filt_x0 + j * cell + cell / 2,
                grid_y0 + (4 - i) * cell + cell / 2,
                str(filt_vals[i, j]), ha='center', va='center',
                fontsize=11, color='white', fontweight='bold')

# Output grid (4×4) — small
out_x0 = 9.5
ax.text(out_x0 + 2 * cell, grid_y0 + 5.6 * cell,
        '4 × 4 output map', ha='center', fontsize=10, color=DARK)
np.random.seed(8)
out_vals = np.random.randint(-5, 8, (4, 4))
for i in range(4):
    for j in range(4):
        v = out_vals[i, j]
        ax.add_patch(Rectangle((out_x0 + j * cell, grid_y0 + (3 - i) * cell),
                               cell, cell, facecolor=LIGHT, edgecolor='white', lw=1))
        ax.text(out_x0 + j * cell + cell / 2,
                grid_y0 + (3 - i) * cell + cell / 2,
                str(v), ha='center', va='center', fontsize=9, color=DARK)

# Highlight where each filter position lands in the output
out_positions = [(0, 0, ORANGE), (1, 2, GREEN), (3, 3, VIOLET)]
for oi, oj, col in out_positions:
    if oi < 4 and oj < 4:
        x_ = out_x0 + oj * cell
        y_ = grid_y0 + (3 - oi) * cell
        ax.add_patch(Rectangle((x_, y_), cell, cell,
                               facecolor='none', edgecolor=col, lw=2.4))

# Annotation
ax.text(7.0, 6.4, 'every position = same filter weights × local 3×3 patch + bias',
        ha='center', fontsize=11, color=DARK,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=LIGHT, edgecolor=GREY))

ax.set_title('A 3 × 3 filter sliding over a 6 × 6 input → 4 × 4 output',
             pad=10)
save(fig, "cnn_filter_slide.png")


# 5. cnn_max_pooling.png — MaxPooling 2×2 example
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

# Input 4×4
in_vals = np.array([[1, 3, 2, 4],
                    [2, 0, 1, 3],
                    [0, 2, 3, 1],
                    [1, 0, 0, 3]])
g_x0, g_y0 = 0.6, 1.0
cell2 = 0.85

block_colours = [(ORANGE, 0, 0), (GREEN, 0, 2), (VIOLET, 2, 0), (RED, 2, 2)]

# Map each cell to its pooling block colour
for bi, bj, col in [(b[1], b[2], b[0]) for b in block_colours]:
    pass  # block tints handled below

cell_block = np.array([[0, 0, 1, 1],
                       [0, 0, 1, 1],
                       [2, 2, 3, 3],
                       [2, 2, 3, 3]])
block_colours_idx = [ORANGE, GREEN, VIOLET, RED]

for i in range(4):
    for j in range(4):
        bcol = block_colours_idx[cell_block[i, j]]
        ax.add_patch(Rectangle((g_x0 + j * cell2, g_y0 + (3 - i) * cell2),
                               cell2, cell2,
                               facecolor=bcol, edgecolor='white', lw=1.4, alpha=0.40))
        ax.text(g_x0 + j * cell2 + cell2 / 2,
                g_y0 + (3 - i) * cell2 + cell2 / 2,
                str(in_vals[i, j]), ha='center', va='center',
                fontsize=14, color=DARK, fontweight='bold')

ax.text(g_x0 + 2 * cell2, g_y0 + 4 * cell2 + 0.2,
        '4 × 4 input', ha='center', fontsize=11, color=DARK)

# Arrow → pool
ax.annotate('', xy=(7.6, 2.7), xytext=(5.2, 2.7),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2))
ax.text(6.4, 3.1, 'MaxPool(2,2)', ha='center', fontsize=11, color=DARK,
        fontweight='bold')
ax.text(6.4, 2.4, 'keep max\nof each block', ha='center', fontsize=9,
        color=GREY, style='italic')

# Output 2×2
out_vals = np.array([[3, 4], [2, 3]])
out_blocks = [ORANGE, GREEN, VIOLET, RED]
o_x0, o_y0 = 8.0, 1.4
cell3 = 1.2
for idx in range(4):
    i = idx // 2
    j = idx % 2
    col = out_blocks[i * 2 + j]
    ax.add_patch(Rectangle((o_x0 + j * cell3, o_y0 + (1 - i) * cell3),
                           cell3, cell3, facecolor=col,
                           edgecolor='white', lw=1.6, alpha=0.85))
    ax.text(o_x0 + j * cell3 + cell3 / 2,
            o_y0 + (1 - i) * cell3 + cell3 / 2,
            str(out_vals[i, j]), ha='center', va='center',
            fontsize=18, color='white', fontweight='bold')

ax.text(o_x0 + cell3, o_y0 + 2 * cell3 + 0.2,
        '2 × 2 output', ha='center', fontsize=11, color=DARK)

ax.set_title('MaxPooling2D((2,2)) — keep the maximum of every 2 × 2 block', pad=8)
save(fig, "cnn_max_pooling.png")


# 6. cnn_shape_trace.png — Shape trace Conv → Pool → Conv → Pool
fig, ax = plt.subplots(figsize=(13, 4.4))
ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off')

stages = [
    ("Input\n(28, 28, 1)", 1.0, GREY, "greyscale image"),
    ("Conv2D(32)\n(26, 26, 32)", 4.0, ACCENT, "28 - 3 + 1 = 26\n32 filters"),
    ("MaxPool(2,2)\n(13, 13, 32)", 7.0, ORANGE, "26 / 2 = 13\nhalf the size"),
    ("Conv2D(64)\n(11, 11, 64)", 10.0, ACCENT, "13 - 3 + 1 = 11\n64 filters"),
    ("MaxPool(2,2)\n(5, 5, 64)", 13.0, ORANGE, "11 / 2 = 5\nhalf again"),
]
for label, x_, col, sub in stages:
    ax.add_patch(FancyBboxPatch((x_ - 1.0, 1.8), 2.0, 1.6,
                                boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2))
    ax.text(x_, 2.6, label, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')
    ax.text(x_, 0.9, sub, ha='center', va='center', color=col,
            fontsize=9, style='italic')
for i in range(4):
    ax.annotate('', xy=(stages[i + 1][1] - 1.0, 2.6),
                xytext=(stages[i][1] + 1.0, 2.6),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.8))

ax.set_title('Shape trace through one CNN block: Conv shrinks by (k − 1), Pool halves',
             pad=12)
save(fig, "cnn_shape_trace.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 3 — Build and Train a Full CNN
# ═════════════════════════════════════════════════════════════════════════════

# 7. cnn_full_architecture.png — full CNN diagram with shapes
fig, ax = plt.subplots(figsize=(13.5, 5))
ax.set_xlim(0, 16); ax.set_ylim(0, 6); ax.axis('off')

arch = [
    ("Input",      "(28, 28, 1)",   1.0,  GREY),
    ("Conv2D(32)", "(26, 26, 32)",  3.0,  ACCENT),
    ("MaxPool",    "(13, 13, 32)",  5.0,  ORANGE),
    ("Conv2D(64)", "(11, 11, 64)",  7.0,  ACCENT),
    ("MaxPool",    "(5, 5, 64)",    9.0,  ORANGE),
    ("Flatten",    "(1600,)",      11.0,  VIOLET),
    ("Dense(128)", "(128,)",       13.0,  GREEN),
    ("Dense(10)",  "(10,)",        15.0,  RED),
]
for label, shape, x_, col in arch:
    ax.add_patch(FancyBboxPatch((x_ - 0.85, 2.2), 1.7, 1.6,
                                boxstyle="round,pad=0.05",
                                facecolor=col, edgecolor='white', lw=2))
    ax.text(x_, 3.0, label, ha='center', va='center', color='white',
            fontsize=10, fontweight='bold')
    ax.text(x_, 1.85, shape, ha='center', fontsize=9, color=col)

for i in range(len(arch) - 1):
    ax.annotate('', xy=(arch[i + 1][2] - 0.85, 3.0),
                xytext=(arch[i][2] + 0.85, 3.0),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.4))

# Top labels
ax.text(6.0, 4.5, 'feature extractor (convolutional)', ha='center',
        fontsize=11, color=ACCENT, fontweight='bold')
ax.text(13.0, 4.5, 'classifier head (Dense)', ha='center',
        fontsize=11, color=GREEN, fontweight='bold')

ax.set_title('Standard MNIST CNN — feature extractor + classifier head', pad=10)
save(fig, "cnn_full_architecture.png")


# 8. cnn_training_curves.png + 9. cnn_vs_dense_accuracy.png
print("\n  → training Dense baseline (3 epochs, fast) ...")
np.random.seed(42); tf.random.set_seed(42)
m_dense = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10,  activation='softmax'),
])
m_dense.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
m_dense.fit(X_train_flat, y_train, epochs=3, batch_size=128,
            validation_split=0.1, verbose=0)
_, dense_acc = m_dense.evaluate(X_test_flat, y_test, verbose=0)
print(f"     Dense test accuracy = {dense_acc:.4f}")

print("\n  → training 2-conv CNN (5 epochs) ...")
np.random.seed(42); tf.random.set_seed(42)
m_cnn = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10,  activation='softmax'),
])
m_cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
h_cnn = m_cnn.fit(X_train_4d, y_train, epochs=5, batch_size=128,
                  validation_split=0.1, verbose=0)
_, cnn_acc = m_cnn.evaluate(X_test_4d, y_test, verbose=0)
print(f"     CNN test accuracy = {cnn_acc:.4f}")

print("\n  → training 3-conv CNN (5 epochs) ...")
np.random.seed(42); tf.random.set_seed(42)
m_cnn3 = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10,  activation='softmax'),
])
m_cnn3.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])
m_cnn3.fit(X_train_4d, y_train, epochs=5, batch_size=128,
           validation_split=0.1, verbose=0)
_, cnn3_acc = m_cnn3.evaluate(X_test_4d, y_test, verbose=0)
print(f"     3-conv CNN accuracy = {cnn3_acc:.4f}")

# 8. cnn_training_curves.png — REAL CNN training curves
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
ep = range(1, len(h_cnn.history['loss']) + 1)
axes[0].plot(ep, h_cnn.history['loss'],     '-o', color=ACCENT, lw=2.4, label='Train loss')
axes[0].plot(ep, h_cnn.history['val_loss'], '-s', color=RED,    lw=2.4, label='Val loss')
axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('Loss')
axes[0].set_title('CNN training loss — drops fast and stays low')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

axes[1].plot(ep, h_cnn.history['accuracy'],     '-o', color=ACCENT, lw=2.4, label='Train acc')
axes[1].plot(ep, h_cnn.history['val_accuracy'], '-s', color=RED,    lw=2.4, label='Val acc')
axes[1].set_xlabel('Epoch'); axes[1].set_ylabel('Accuracy')
axes[1].set_title(f'CNN accuracy — final test = {cnn_acc:.3f}')
axes[1].legend(loc='lower right')
axes[1].set_ylim(0.96, 1.001)
axes[1].grid(True, alpha=0.3)

fig.suptitle('Real 2-conv CNN training on MNIST (5 epochs, batch=128)', y=1.02)
fig.tight_layout()
save(fig, "cnn_training_curves.png")


# 9. cnn_vs_dense_accuracy.png — bar chart with param counts annotated
fig, ax = plt.subplots(figsize=(9, 5.4))
names = ['Dense baseline\n3 epochs', '2-conv CNN\n5 epochs', '3-conv CNN\n5 epochs']
accs  = [dense_acc, cnn_acc, cnn3_acc]
counts = [m_dense.count_params(), m_cnn.count_params(), m_cnn3.count_params()]
colours = [GREY, ACCENT, VIOLET]

bars = ax.bar(names, accs, color=colours, edgecolor='white', linewidth=2)
for bar, a, n in zip(bars, accs, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, a + 0.001,
            f'{a:.4f}', ha='center', va='bottom', fontsize=12,
            fontweight='bold', color=DARK)
    ax.text(bar.get_x() + bar.get_width() / 2, 0.962,
            f'{n:,} params', ha='center', va='bottom', fontsize=9,
            color='white', fontweight='bold')

ax.set_ylabel('MNIST test accuracy')
ax.set_ylim(0.96, 1.0)
ax.set_title('CNN beats Dense even with similar parameter counts')
ax.grid(True, alpha=0.3, axis='y')
save(fig, "cnn_vs_dense_accuracy.png")


# ═════════════════════════════════════════════════════════════════════════════
# LECTURE 4 — Malware Visualisation
# ═════════════════════════════════════════════════════════════════════════════

# 10. cnn_malware_families.png — 4 synthetic malware fingerprints
def make_ransomware(size=64, rng=None):
    rng = rng or np.random.default_rng(1)
    img = np.zeros((size, size), dtype=np.uint8)
    # Sharp blocks
    blocks = [(5, 5, 24, 24, 200), (30, 5, 25, 28, 30),
              (5, 32, 28, 28, 130), (35, 35, 26, 26, 220)]
    for r, c, h, w, v in blocks:
        img[r:r + h, c:c + w] = v + rng.integers(-10, 10, (h, w))
    return img.clip(0, 255).astype(np.uint8)

def make_worm(size=64):
    return np.tile(np.linspace(20, 235, size, dtype=np.uint8)[:, None],
                   (1, size))

def make_trojan(size=64, rng=None):
    rng = rng or np.random.default_rng(7)
    return rng.integers(0, 256, (size, size), dtype=np.uint8)

def make_rootkit(size=64):
    rows = []
    for i in range(size):
        v = 200 if (i // 4) % 2 == 0 else 60
        rows.append(np.full(size, v, dtype=np.uint8))
    return np.array(rows)

fig, axes = plt.subplots(1, 4, figsize=(14, 4))
fams = [
    ('Ransomware', make_ransomware(), 'sharp code/data blocks'),
    ('Worm',       make_worm(),       'smooth gradient (polymorphic)'),
    ('Trojan',     make_trojan(),     'high-entropy noise (encrypted)'),
    ('Rootkit',    make_rootkit(),    'regular packed bands'),
]
for ax, (name, im, sub) in zip(axes, fams):
    ax.imshow(im, cmap='gray', interpolation='nearest', vmin=0, vmax=255)
    ax.set_title(name, fontsize=12, color=DARK, fontweight='bold')
    ax.set_xlabel(sub, fontsize=9, color=GREY, style='italic')
    ax.set_xticks([]); ax.set_yticks([])

fig.suptitle('Four malware families — same CNN architecture, different visual fingerprints',
             y=1.02)
fig.tight_layout()
save(fig, "cnn_malware_families.png")


print("\n10 CNN visuals written to portal/static/lecture_assets/")
print(f"  Dense baseline: {dense_acc:.4f}")
print(f"  2-conv CNN:     {cnn_acc:.4f} ({m_cnn.count_params():,} params)")
print(f"  3-conv CNN:     {cnn3_acc:.4f}")
