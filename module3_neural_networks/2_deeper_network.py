# Lesson 3.2 — Deeper Networks, Dropout & Batch Normalisation
#
# Demonstrates: multi-layer networks, dropout, batch norm,
#               early stopping, and class weight handling.
# Task: same intrusion detection problem as 3.1 — compare results.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
from sklearn.metrics import classification_report, roc_auc_score, RocCurveDisplay

import tensorflow as tf
from tensorflow import keras

np.random.seed(42)
tf.random.set_seed(42)

# ── 1. Dataset ─────────────────────────────────────────────────────────────────
X, y = make_classification(
    n_samples=8000, n_features=15, n_informative=10, n_redundant=3,
    weights=[0.92, 0.08],  # 8% attacks — more imbalanced
    flip_y=0.03, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print(f"Attack rate: {y.mean()*100:.1f}%")

# ── 2. Class weights (handle imbalance) ───────────────────────────────────────
cw = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = {0: cw[0], 1: cw[1]}
print(f"Class weights: benign={cw[0]:.2f}, attack={cw[1]:.2f}")

# ── 3. Build models to compare ────────────────────────────────────────────────

def shallow_model(input_dim):
    """Simple 2-layer model from Lesson 3.1 (no dropout/batch norm)"""
    return keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid'),
    ], name='shallow')

def deep_model(input_dim):
    """Deeper model with dropout and batch normalisation"""
    return keras.Sequential([
        keras.layers.Dense(128, input_shape=(input_dim,)),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(0.3),

        keras.layers.Dense(64),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(0.3),

        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.2),

        keras.layers.Dense(1, activation='sigmoid'),
    ], name='deep_with_regularisation')

input_dim = X_train_s.shape[1]

# ── 4. Early stopping callback ────────────────────────────────────────────────
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=12,
    restore_best_weights=True,
    verbose=1
)

# ── 5. Train both models ───────────────────────────────────────────────────────
histories = {}
aucs = {}

for name, build_fn in [('Shallow (no regularisation)', shallow_model),
                        ('Deep + Dropout + BatchNorm',  deep_model)]:
    print(f"\n=== Training: {name} ===")
    model = build_fn(input_dim)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    h = model.fit(
        X_train_s, y_train,
        epochs=150,
        batch_size=64,
        validation_split=0.15,
        class_weight=class_weights,
        callbacks=[early_stop],
        verbose=0
    )
    print(f"Stopped at epoch {len(h.history['loss'])}")

    y_proba = model.predict(X_test_s, verbose=0).flatten()
    y_pred  = (y_proba >= 0.5).astype(int)
    auc = roc_auc_score(y_test, y_proba)
    aucs[name] = (model, y_proba, auc)
    histories[name] = h

    print(classification_report(y_test, y_pred, target_names=['Benign', 'Attack']))
    print(f"ROC AUC: {auc:.4f}")

# ── 6. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
colors = {'Shallow (no regularisation)': 'steelblue',
          'Deep + Dropout + BatchNorm':  'crimson'}

# Loss curves for both models
for name, h in histories.items():
    c = colors[name]
    axes[0].plot(h.history['val_loss'], label=f'{name} (val)', color=c, linewidth=2)
    axes[0].plot(h.history['loss'], linestyle='--', color=c, alpha=0.5, label=f'{name} (train)')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Loss Curves')
axes[0].legend(fontsize=7)

# ROC curves
for name, (model, y_proba, auc) in aucs.items():
    RocCurveDisplay.from_predictions(y_test, y_proba,
                                     name=f'{name} (AUC={auc:.3f})',
                                     ax=axes[1], color=colors[name])
axes[1].set_title('ROC Curves')

# Accuracy comparison
names_short = ['Shallow', 'Deep+Reg']
auc_vals = [v[2] for v in aucs.values()]
bars = axes[2].bar(names_short, auc_vals, color=list(colors.values()))
for bar, val in zip(bars, auc_vals):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.02,
                 f'{val:.3f}', ha='center', va='top', color='white', fontweight='bold')
axes[2].set_ylim(0.5, 1.05)
axes[2].set_ylabel('ROC AUC')
axes[2].set_title('Model Comparison')

plt.tight_layout()
plt.savefig('module3_neural_networks/lesson2_deeper_network.png')
plt.show()
print("\nPlot saved to module3_neural_networks/lesson2_deeper_network.png")
