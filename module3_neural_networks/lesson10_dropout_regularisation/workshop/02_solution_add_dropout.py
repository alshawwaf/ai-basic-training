# Exercise 2 — Add Dropout
#
# Dropout(rate) randomly silences a fraction of neurons each training batch,
# forcing every neuron to learn independently useful features. At prediction
# time, all neurons are active — giving an implicit ensemble effect.
#
# Prerequisite: pip install tensorflow scikit-learn matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 2 — Add Dropout")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup (same as exercise 1) ───────────────────────────────────────────
X, y = make_classification(
    n_samples=8000, n_features=15, n_informative=10, n_redundant=3,
    weights=[0.92, 0.08], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)
input_dim = X_train_s.shape[1]

# ── Train baseline (no dropout) for comparison ──────────────────────────────────
print("Training baseline (no dropout)...")
baseline = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
], name='baseline')
baseline.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
h_base = baseline.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)
base_val_loss = h_base.history['val_loss'][-1]
base_val_acc  = h_base.history['val_accuracy'][-1]
print(f"Baseline (no dropout): val_loss={base_val_loss:.4f}, val_acc={base_val_acc:.4f}")

# ── TASK 1 — Add Dropout(0.3) After Each Dense Layer ────────────────────────────
# Dropout(0.3) zeroes 30% of neurons randomly in each training batch.
# Different neurons are zeroed each batch — like training thousands of
# slightly different networks simultaneously (ensemble effect).
# IMPORTANT: never add Dropout after the output layer.
print("\n" + "=" * 60)
print("TASK 1 — Add Dropout(0.3) After Each Dense Layer")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_dropout = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dropout(0.3),   # 30% of 256 neurons zeroed each batch
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1,   activation='sigmoid')   # no dropout here
], name='with_dropout')

model_dropout.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

h_drop = model_dropout.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

drop_val_loss = h_drop.history['val_loss'][-1]
drop_val_acc  = h_drop.history['val_accuracy'][-1]
print(f"With Dropout(0.3): val_loss={drop_val_loss:.4f}, val_acc={drop_val_acc:.4f}")
print(f"Val loss improvement: {base_val_loss - drop_val_loss:.4f}")

# ── TASK 2 — Plot Val Loss Comparison ────────────────────────────────────────────
# The dropout curve should be lower and less spiky than the baseline.
print("\n" + "=" * 60)
print("TASK 2 — Plot Val Loss Comparison")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(h_base.history['val_loss'], label='No dropout', color='steelblue')
axes[0].plot(h_drop.history['val_loss'], label='Dropout(0.3)', color='crimson')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Validation Loss')
axes[0].set_title('Val Loss: Baseline vs Dropout')
axes[0].legend()

axes[1].plot(h_base.history['val_accuracy'], label='No dropout', color='steelblue')
axes[1].plot(h_drop.history['val_accuracy'], label='Dropout(0.3)', color='crimson')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation Accuracy')
axes[1].set_title('Val Accuracy: Baseline vs Dropout')
axes[1].legend()

plt.tight_layout()
plt.savefig('lesson10_ex2_dropout.png')
plt.show()
print("Plot saved to lesson10_ex2_dropout.png")

# ── TASK 3 — Compare Rates 0.1, 0.3, 0.5 ───────────────────────────────────────
# 0.1 = very mild regularisation
# 0.3 = standard starting point (usually best)
# 0.5 = strong — may cause underfitting (too much capacity lost)
print("\n" + "=" * 60)
print("TASK 3 — Compare Dropout Rates 0.1, 0.3, 0.5")
print("=" * 60)

rate_results = {}

for rate in [0.1, 0.3, 0.5]:
    np.random.seed(42)
    tf.random.set_seed(42)

    m = keras.Sequential([
        keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(rate),
        keras.layers.Dense(1,   activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    h = m.fit(X_train_s, y_train, epochs=50, batch_size=64,
              validation_split=0.15, verbose=0)

    val_acc = h.history['val_accuracy'][-1]
    rate_results[rate] = val_acc

print(f"{'Rate':>6} | {'Val Accuracy':>12}")
print("-" * 22)
for rate, acc in rate_results.items():
    print(f"  {rate:.1f}  |  {acc:.4f}")

# ── TASK 4 (BONUS) — Verify Dropout Is Off During Prediction ────────────────────
# Dropout is only active during training (model.fit).
# During prediction (model.predict), all neurons are active.
# Multiple identical predict() calls must return identical results.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Verify Dropout Is Off During Prediction")
print("=" * 60)

X_sample = X_test_s[:5]   # 5 test samples
predictions = []
for i in range(5):
    pred = model_dropout.predict(X_sample, verbose=0)
    predictions.append(pred.flatten())

# Check all 5 runs produced identical output
all_same = all(np.allclose(predictions[0], p) for p in predictions[1:])
print(f"5 repeated predictions on same input: all identical = {all_same}")
if all_same:
    print("Confirmed: Dropout is disabled during inference (model.predict).")

print("\n--- Exercise 2 complete. Move to 03_solution_batch_normalisation.py ---")
