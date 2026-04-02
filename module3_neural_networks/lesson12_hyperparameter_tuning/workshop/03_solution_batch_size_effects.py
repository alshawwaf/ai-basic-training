# Exercise 3 — Batch Size Effects
#
# Batch size controls how many samples are used per gradient update.
# Small batches (32): noisy gradients, good generalisation, slower wall-clock.
# Large batches (512): smooth gradients, faster training, may generalise worse.
# Full batch (all samples): exact gradient, fastest per-epoch, often underfits.
#
# Prerequisite: pip install tensorflow scikit-learn

import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 3 — Batch Size Effects")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup ─────────────────────────────────────────────────────────────
X, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                            n_redundant=5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)

EPOCHS = 30

def build_model():
    """Build and compile a fresh model (same architecture every time)."""
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ])
    m.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return m

# Store results for the summary table
results = {}

# ── TASK 1 — Small batch: batch_size=32 ──────────────────────────────────────
# Each epoch does len(X_train)/32 = 50 gradient updates.
# More updates per epoch means noisier but more frequent corrections.
# This noise acts as implicit regularisation, often improving generalisation.
print("\n" + "=" * 60)
print("TASK 1 — Small batch: batch_size=32")
print("=" * 60)

model1 = build_model()
t0 = time.time()
h1 = model1.fit(X_train, y_train, epochs=EPOCHS,
                batch_size=32, validation_data=(X_val, y_val), verbose=0)
t1 = time.time() - t0
val_acc1 = h1.history['val_accuracy'][-1]
results[32] = (val_acc1, t1)
print(f"batch_size=  32 | val_accuracy: {val_acc1:.4f} | time: {t1:.1f}s")

# ── TASK 2 — Large batch: batch_size=512 ─────────────────────────────────────
# Each epoch does len(X_train)/512 ~ 3 gradient updates.
# Fewer updates per epoch, but each is a more accurate estimate of the
# true gradient. Training is faster wall-clock but may converge to a
# sharper (less generalisable) minimum.
print("\n" + "=" * 60)
print("TASK 2 — Large batch: batch_size=512")
print("=" * 60)

model2 = build_model()
t0 = time.time()
h2 = model2.fit(X_train, y_train, epochs=EPOCHS,
                batch_size=512, validation_data=(X_val, y_val), verbose=0)
t2 = time.time() - t0
val_acc2 = h2.history['val_accuracy'][-1]
results[512] = (val_acc2, t2)
print(f"batch_size= 512 | val_accuracy: {val_acc2:.4f} | time: {t2:.1f}s")

# ── TASK 3 — Full batch: batch_size=len(X_train) ────────────────────────────
# One gradient update per epoch using every sample. This is classic
# gradient descent (not stochastic). Fastest per-epoch but the exact
# gradient can lead to sharp minima that generalise poorly.
print("\n" + "=" * 60)
print("TASK 3 — Full batch: batch_size=len(X_train)")
print("=" * 60)

full_bs = len(X_train)
model3 = build_model()
t0 = time.time()
h3 = model3.fit(X_train, y_train, epochs=EPOCHS,
                batch_size=full_bs, validation_data=(X_val, y_val), verbose=0)
t3 = time.time() - t0
val_acc3 = h3.history['val_accuracy'][-1]
results[full_bs] = (val_acc3, t3)
print(f"batch_size={full_bs:>4} | val_accuracy: {val_acc3:.4f} | time: {t3:.1f}s")

# ── TASK 4 (BONUS) — Summary comparison ─────────────────────────────────────
# Side-by-side table showing the trade-off: smaller batches usually give
# better accuracy but take longer; larger batches are faster but may
# sacrifice generalisation quality.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Summary comparison")
print("=" * 60)

print(f"\n{'Batch Size':>12} | {'Val Accuracy':>14} | {'Time (s)':>10}")
print("-" * 44)
for bs, (acc, elapsed) in sorted(results.items()):
    print(f"{bs:>12} | {acc:>14.4f} | {elapsed:>10.1f}")

print("\nKey trade-off:")
print("  - Smaller batches: noisier gradients, better generalisation, slower")
print("  - Larger batches:  smoother gradients, faster training, may overfit")
print("  - In practice, 32-128 is a good starting range for most problems")

print("\n--- Exercise 3 complete. Move to 04_solution_architecture_search.py ---")
