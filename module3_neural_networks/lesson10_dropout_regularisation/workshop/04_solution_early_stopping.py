# Exercise 4 — Early Stopping
#
# EarlyStopping monitors val_loss each epoch and halts training when
# it stops improving. With restore_best_weights=True, the model
# automatically reverts to its best epoch — no manual checkpoint needed.
#
# Prerequisite: pip install tensorflow scikit-learn matplotlib

import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

print("=" * 60)
print("EXERCISE 4 — Early Stopping")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup (same as exercises 1-3) ────────────────────────────────────────
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

# ── Helper: build the regularised model (from exercises 2-3) ─────────────────────
def build_model():
    """Returns a fresh 3x256 model with BatchNorm + Dropout."""
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
        keras.layers.Dense(1,   activation='sigmoid')
    ])

# ── TASK 1 — Train with EarlyStopping ───────────────────────────────────────────
# patience=5: stop after 5 consecutive non-improving epochs.
# restore_best_weights=True: rewind to the epoch with lowest val_loss.
# Set epochs=200 as an upper bound — early stopping will halt well before 200.
print("\n" + "=" * 60)
print("TASK 1 — Train with EarlyStopping")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model = build_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Create the EarlyStopping callback
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',           # watch validation loss each epoch
    patience=5,                   # wait 5 non-improving epochs before stopping
    restore_best_weights=True,    # rewind to the best epoch automatically
    verbose=1                     # print a message when stopping
)

start_time = time.time()
history = model.fit(
    X_train_s, y_train,
    epochs=200,                   # upper bound — early stopping will halt sooner
    batch_size=64,
    validation_split=0.15,
    callbacks=[early_stop],       # must be a list
    verbose=0
)
train_time = time.time() - start_time

epochs_run = len(history.history['loss'])
final_val_loss = history.history['val_loss'][-1]
final_val_acc  = history.history['val_accuracy'][-1]

print(f"Stopped at epoch: {epochs_run}  (out of 200)")
print(f"Final val_loss:   {final_val_loss:.4f}")
print(f"Final val_acc:    {final_val_acc:.4f}")
print(f"Training time:    {train_time:.1f}s")

# ── TASK 2 — Plot with Stop Marker ──────────────────────────────────────────────
# Vertical dashed line at the actual stop epoch.
# Gold dot at the epoch where val_loss reached its minimum.
print("\n" + "=" * 60)
print("TASK 2 — Plot with Stop Marker")
print("=" * 60)

val_losses = history.history['val_loss']
best_epoch = int(np.argmin(val_losses))  # 0-indexed
best_val_loss = val_losses[best_epoch]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(history.history['loss'],     label='Train loss', color='steelblue')
ax.plot(history.history['val_loss'], label='Val loss', color='crimson')

# Mark the best epoch with a gold dot
ax.plot(best_epoch, best_val_loss, 'o', color='gold', markersize=10,
        zorder=5, label=f'Best val_loss (epoch {best_epoch + 1})')

# Vertical line at stop epoch
ax.axvline(x=epochs_run - 1, color='grey', linestyle='--', alpha=0.7,
           label=f'Training stopped (epoch {epochs_run})')

ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_title('Early Stopping — Training Halted at the Right Time')
ax.legend()

plt.tight_layout()
plt.savefig('lesson10_ex4_early_stopping.png')
plt.show()
print("Plot saved to lesson10_ex4_early_stopping.png")

# ── TASK 3 — Training Efficiency Report ─────────────────────────────────────────
# Calculate how many epochs were saved and estimate time savings.
# On real datasets with millions of samples, early stopping can save hours.
print("\n" + "=" * 60)
print("TASK 3 — Training Efficiency Report")
print("=" * 60)

scheduled = 200
saved     = scheduled - epochs_run
# Estimate time per epoch from actual training
time_per_epoch  = train_time / epochs_run
est_time_saved  = saved * time_per_epoch

print(f"Scheduled epochs: {scheduled}")
print(f"Epochs ran:       {epochs_run}")
print(f"Epochs saved:     {saved}")
print(f"Time per epoch:   {time_per_epoch:.2f}s")
print(f"Estimated time saved: {est_time_saved:.1f}s")

# ── TASK 4 (BONUS) — Compare Patience Values ────────────────────────────────────
# patience=1: stops very aggressively — may stop before converging.
# patience=5: standard balanced choice.
# patience=20: lenient — allows plateaus but may allow some overfitting.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Compare Patience Values (1, 5, 20)")
print("=" * 60)

patience_results = {}

for p in [1, 5, 20]:
    np.random.seed(42)
    tf.random.set_seed(42)

    m = build_model()
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    es = keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=p,
        restore_best_weights=True, verbose=0
    )
    h = m.fit(
        X_train_s, y_train, epochs=200, batch_size=64,
        validation_split=0.15, callbacks=[es], verbose=0
    )

    ep = len(h.history['loss'])
    va = h.history['val_accuracy'][-1]
    patience_results[p] = (ep, va)

print(f"{'Patience':>8} | {'Epochs ran':>10} | {'Val accuracy':>12}")
print("-" * 38)
for p, (ep, va) in patience_results.items():
    print(f"      {p:>2} | {ep:>10} | {va:>12.4f}")

print("\npatience=1 often stops too early (lower accuracy).")
print("patience=5 is the standard balanced choice.")
print("patience=20 allows more training but may permit gradual overfitting.")

print("\n--- Lesson 10 done. All exercises complete! ---")
