# Exercise 3 — Batch Normalisation
#
# BatchNormalization normalises each layer's activations to mean~0, std~1
# within each mini-batch. This stabilises training (smoother loss curves)
# and allows higher learning rates, but is NOT a strong regulariser by
# itself — combine it with Dropout for best results.
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
print("EXERCISE 3 — Batch Normalisation")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup (same as exercises 1-2) ────────────────────────────────────────
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

# ── TASK 1 — Add BatchNorm After Each Dense Layer ───────────────────────────────
# BatchNorm computes per-feature mean and variance within each batch,
# normalises, then applies learned scale (gamma) and shift (beta).
# Effect: each layer always receives inputs with ~mean=0, ~std=1,
# regardless of how earlier layers changed their weights.
print("\n" + "=" * 60)
print("TASK 1 — Add BatchNorm After Each Dense Layer")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_bn = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.BatchNormalization(),   # normalise after activation
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1,   activation='sigmoid')   # no BN on output
], name='with_batchnorm')

model_bn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_bn.summary()

h_bn = model_bn.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

bn_val_loss = h_bn.history['val_loss'][-1]
bn_val_acc  = h_bn.history['val_accuracy'][-1]
print(f"\nFinal val_loss: {bn_val_loss:.4f}")
print(f"Final val_acc:  {bn_val_acc:.4f}")

# ── TASK 2 — Compare Training Stability ─────────────────────────────────────────
# Build an identical architecture without BatchNorm and compare loss curves.
# The BatchNorm version should show a smoother, less spiky training loss.
print("\n" + "=" * 60)
print("TASK 2 — Compare Training Stability (BatchNorm vs No BatchNorm)")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_no_bn = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1,   activation='sigmoid')
], name='no_batchnorm')

model_no_bn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

h_no_bn = model_no_bn.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Training loss comparison
axes[0].plot(h_no_bn.history['loss'], label='No BatchNorm', color='steelblue', alpha=0.7)
axes[0].plot(h_bn.history['loss'],    label='With BatchNorm', color='crimson', alpha=0.7)
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Training Loss')
axes[0].set_title('Training Loss — BatchNorm Smooths the Curve')
axes[0].legend()

# Validation loss comparison
axes[1].plot(h_no_bn.history['val_loss'], label='No BatchNorm', color='steelblue', alpha=0.7)
axes[1].plot(h_bn.history['val_loss'],    label='With BatchNorm', color='crimson', alpha=0.7)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation Loss')
axes[1].set_title('Validation Loss')
axes[1].legend()

plt.tight_layout()
plt.savefig('lesson10_ex3_batchnorm.png')
plt.show()
print("Plot saved to lesson10_ex3_batchnorm.png")

# ── TASK 3 — Combine BatchNorm + Dropout ─────────────────────────────────────────
# Standard order: Dense → BatchNorm → Dropout → next Dense
# BatchNorm before Dropout because Dropout changes the scale of inputs.
# The combination often gives the best results: stability + regularisation.
print("\n" + "=" * 60)
print("TASK 3 — Combine BatchNorm + Dropout")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_combined = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1,   activation='sigmoid')
], name='batchnorm_plus_dropout')

model_combined.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

h_combined = model_combined.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

combined_val_acc = h_combined.history['val_accuracy'][-1]

print(f"BatchNorm only  val_acc: {bn_val_acc:.4f}")
print(f"Combined BN+DO  val_acc: {combined_val_acc:.4f}")
print(f"Improvement:             {combined_val_acc - bn_val_acc:+.4f}")

# ── TASK 4 (BONUS) — Asymmetric Placement ───────────────────────────────────────
# Remove BatchNorm from the middle layer only. Measure std of training loss
# over first 20 epochs. Higher std = noisier, less stable training.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Asymmetric Placement")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# Asymmetric: BN on layers 1 and 3 but NOT layer 2
model_asymm = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(input_dim,)),
    keras.layers.BatchNormalization(),    # present
    keras.layers.Dense(256, activation='relu'),
    # NO BatchNorm here — middle layer misses normalisation
    keras.layers.Dense(256, activation='relu'),
    keras.layers.BatchNormalization(),    # present
    keras.layers.Dense(1,   activation='sigmoid')
], name='asymmetric_batchnorm')

model_asymm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

h_asymm = model_asymm.fit(
    X_train_s, y_train, epochs=50, batch_size=64,
    validation_split=0.15, verbose=0
)

# Compare stability: standard deviation of training loss in the first 20 epochs
full_bn_std  = np.std(h_bn.history['loss'][:20])
asymm_std    = np.std(h_asymm.history['loss'][:20])

print(f"Full BN train loss std (first 20 epochs):  {full_bn_std:.4f}")
print(f"Asymm train loss std (first 20 epochs):    {asymm_std:.4f}")
if asymm_std > full_bn_std:
    print("Asymmetric placement shows noisier training — consistent BN is better.")

print("\n--- Exercise 3 complete. Move to ../4_early_stopping/solution.py ---")
