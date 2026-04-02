# Exercise 2 — Learning Rate Sensitivity
#
# The learning rate controls how large each weight update step is.
# Too high (0.1): overshoots minima, loss oscillates or diverges.
# Too low (0.00001): barely moves, needs many more epochs to converge.
# Just right (0.001): smooth descent, reaches good accuracy quickly.
#
# Prerequisite: pip install tensorflow scikit-learn

import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 2 — Learning Rate Sensitivity")
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

def build_model(learning_rate):
    """Build and compile the same architecture with a given learning rate."""
    tf.random.set_seed(42)
    np.random.seed(42)
    m = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ])
    m.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    return m

EPOCHS = 30

# ── TASK 1 — Baseline: lr = 0.001 ────────────────────────────────────────────
# The default Adam learning rate. Produces smooth, steady convergence.
# Loss declines consistently epoch over epoch without oscillation.
print("\n" + "=" * 60)
print("TASK 1 — Baseline: lr = 0.001")
print("=" * 60)

model1 = build_model(0.001)
history1 = model1.fit(X_train, y_train, epochs=EPOCHS,
                      validation_data=(X_val, y_val), verbose=0)
val_acc1 = history1.history['val_accuracy'][-1]
print(f"lr=0.001000 | final val_accuracy: {val_acc1:.4f}")
print(f"Loss trajectory: smooth decline from "
      f"{history1.history['loss'][0]:.2f} to {history1.history['loss'][-1]:.2f}")

# ── TASK 2 — Too large: lr = 0.1 ─────────────────────────────────────────────
# With lr=0.1, each update step is 100x larger than the baseline.
# The optimiser overshoots the loss minimum, causing the loss curve
# to oscillate or spike. Final accuracy is worse and less stable.
print("\n" + "=" * 60)
print("TASK 2 — Too large: lr = 0.1")
print("=" * 60)

model2 = build_model(0.1)
history2 = model2.fit(X_train, y_train, epochs=EPOCHS,
                      validation_data=(X_val, y_val), verbose=0)
val_acc2 = history2.history['val_accuracy'][-1]
print(f"lr=0.100000 | final val_accuracy: {val_acc2:.4f}")
print(f"Loss trajectory: erratic, may spike upward mid-training")

# ── TASK 3 — Too small: lr = 0.00001 ─────────────────────────────────────────
# With lr=0.00001, each step is 100x smaller than the baseline.
# The model barely learns anything in 30 epochs — it would need
# thousands of epochs to approach the baseline's performance.
print("\n" + "=" * 60)
print("TASK 3 — Too small: lr = 0.00001")
print("=" * 60)

model3 = build_model(0.00001)
history3 = model3.fit(X_train, y_train, epochs=EPOCHS,
                      validation_data=(X_val, y_val), verbose=0)
val_acc3 = history3.history['val_accuracy'][-1]
print(f"lr=0.000010 | final val_accuracy: {val_acc3:.4f}")
print(f"Loss trajectory: almost flat — very slow descent")

# ── TASK 4 (BONUS) — Compare loss trajectories ──────────────────────────────
# Side-by-side comparison at key epochs shows how each learning rate
# progresses. The "just right" rate (0.001) reaches low loss fastest.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare loss trajectories")
print("=" * 60)

histories = {0.001: history1, 0.1: history2, 0.00001: history3}
checkpoints = [0, 4, 9, 19, 29]   # epochs 1, 5, 10, 20, 30 (0-indexed)

print(f"\n{'Epoch':>7}", end="")
for lr in histories:
    print(f" | lr={lr:<10}", end="")
print()
print("-" * 50)

for ep in checkpoints:
    print(f"{ep+1:>7}", end="")
    for lr, h in histories.items():
        loss = h.history['loss'][ep]
        print(f" | {loss:<14.4f}", end="")
    print()

print(f"\nFinal val_accuracy:")
print(f"  lr=0.001  : {val_acc1:.4f}  (good)")
print(f"  lr=0.1    : {val_acc2:.4f}  (too high — overshooting)")
print(f"  lr=0.00001: {val_acc3:.4f}  (too low — barely learning)")

print("\n--- Exercise 2 complete. Move to ../3_batch_size_effects/solution.py ---")
