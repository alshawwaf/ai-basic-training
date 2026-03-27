# Lesson 3.4 — Hyperparameter Tuning
#
# Demonstrates manual hyperparameter exploration:
#   - Learning rate sensitivity
#   - Batch size effects
#   - Network width/depth
#   - Building intuition for what to tune first

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

import tensorflow as tf
from tensorflow import keras

np.random.seed(42)
tf.random.set_seed(42)

# ── 1. Dataset ─────────────────────────────────────────────────────────────────
X, y = make_classification(
    n_samples=5000, n_features=12, n_informative=8,
    weights=[0.9, 0.1], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 2. Helper: build and train quickly ────────────────────────────────────────
def run_experiment(learning_rate=0.001, batch_size=64, units=(64, 32),
                   dropout=0.3, epochs=60, label=''):
    model = keras.Sequential(name=label or 'model')
    model.add(keras.layers.Input(shape=(X_train_s.shape[1],)))
    for u in units:
        model.add(keras.layers.Dense(u, activation='relu'))
        if dropout > 0:
            model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy'
    )
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=8, restore_best_weights=True, verbose=0
    )
    h = model.fit(
        X_train_s, y_train, epochs=epochs, batch_size=batch_size,
        validation_split=0.15, callbacks=[early_stop], verbose=0
    )
    y_proba = model.predict(X_test_s, verbose=0).flatten()
    auc = roc_auc_score(y_test, y_proba)
    return h, auc

# ── 3. Experiment 1: Learning rate ────────────────────────────────────────────
print("=== Experiment 1: Learning Rate ===")
lr_results = {}
for lr in [0.01, 0.001, 0.0001]:
    h, auc = run_experiment(learning_rate=lr, label=f'lr_{lr}')
    lr_results[lr] = (h, auc)
    print(f"  lr={lr:.4f}  → AUC={auc:.4f}  (trained {len(h.history['loss'])} epochs)")

# ── 4. Experiment 2: Batch size ───────────────────────────────────────────────
print("\n=== Experiment 2: Batch Size ===")
bs_results = {}
for bs in [16, 64, 256]:
    h, auc = run_experiment(batch_size=bs, label=f'bs_{bs}')
    bs_results[bs] = (h, auc)
    print(f"  batch_size={bs:<5} → AUC={auc:.4f}  (trained {len(h.history['loss'])} epochs)")

# ── 5. Experiment 3: Network size ─────────────────────────────────────────────
print("\n=== Experiment 3: Network Architecture ===")
arch_results = {}
architectures = {
    'Tiny (16)':       (16,),
    'Small (32,16)':   (32, 16),
    'Medium (64,32)':  (64, 32),
    'Large (128,64,32)':(128, 64, 32),
}
for name, units in architectures.items():
    h, auc = run_experiment(units=units, label=name)
    arch_results[name] = (h, auc)
    print(f"  {name:<25} → AUC={auc:.4f}")

# ── 6. Best configuration summary ─────────────────────────────────────────────
print("\n=== Best Configuration ===")
best_lr   = max(lr_results,   key=lambda k: lr_results[k][1])
best_bs   = max(bs_results,   key=lambda k: bs_results[k][1])
best_arch = max(arch_results, key=lambda k: arch_results[k][1])
print(f"  Learning rate   : {best_lr}")
print(f"  Batch size      : {best_bs}")
print(f"  Architecture    : {best_arch}")

# Final run with best config
best_units = architectures[best_arch]
h_best, auc_best = run_experiment(
    learning_rate=best_lr, batch_size=best_bs, units=best_units, label='best'
)
print(f"\n  Final model AUC : {auc_best:.4f}")

# ── 7. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Learning rate loss curves
for lr, (h, auc) in lr_results.items():
    axes[0].plot(h.history['val_loss'], label=f'lr={lr} (AUC={auc:.3f})')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Validation Loss')
axes[0].set_title('Effect of Learning Rate')
axes[0].legend()

# Batch size smoothness
for bs, (h, auc) in bs_results.items():
    axes[1].plot(h.history['loss'], label=f'batch={bs} (AUC={auc:.3f})', alpha=0.8)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Training Loss')
axes[1].set_title('Effect of Batch Size (smoothness of curve)')
axes[1].legend()

# Architecture bar chart
arch_names  = list(arch_results.keys())
arch_aucs   = [v[1] for v in arch_results.values()]
colors      = ['steelblue' if a < auc_best * 0.99 else 'crimson' for a in arch_aucs]
bars = axes[2].bar([n.split('(')[0].strip() for n in arch_names], arch_aucs, color='steelblue')
axes[2].set_ylabel('ROC AUC')
axes[2].set_title('Effect of Network Size')
axes[2].set_ylim(min(arch_aucs) - 0.02, 1.0)
for bar, val in zip(bars, arch_aucs):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                 f'{val:.3f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('stage3_neural_networks/lesson4_hyperparameters.png')
plt.show()
print("\nPlot saved to stage3_neural_networks/lesson4_hyperparameters.png")
