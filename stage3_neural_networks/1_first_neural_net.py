# Lesson 3.1 — Your First Neural Network in Keras
#
# We build the same network you constructed in from_scratch/p004-p008,
# but using Keras. Same concepts: layers, activations, loss, training.
#
# Task: binary classification — detect malicious network connections.
# Prerequisite: pip install tensorflow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

import tensorflow as tf
from tensorflow import keras

print(f"TensorFlow version: {tf.__version__}")

np.random.seed(42)
tf.random.set_seed(42)

# ── 1. Dataset: network connection classification ──────────────────────────────
X, y = make_classification(
    n_samples=5000, n_features=12, n_informative=8, n_redundant=2,
    weights=[0.88, 0.12],  # 12% attacks
    flip_y=0.03,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print(f"\nTraining samples: {len(X_train)} | Test samples: {len(X_test)}")
print(f"Attack rate: {y.mean()*100:.1f}%")

# ── 2. Build the model ─────────────────────────────────────────────────────────
# Architecture: 12 inputs → Dense(32) → Dense(16) → Dense(1) output
#
# Compare with from_scratch/p004:
#   Layer_Dense(12, 32)  ← same as keras.layers.Dense(32, input_shape=(12,))
#   Activation_ReLU()    ← same as activation='relu'
#
model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')   # sigmoid → P(attack)
], name='intrusion_detector')

model.summary()

# ── 3. Compile ─────────────────────────────────────────────────────────────────
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',   # log loss for binary classification
    metrics=['accuracy']
)

# ── 4. Train ───────────────────────────────────────────────────────────────────
print("\n=== Training ===")
history = model.fit(
    X_train_s, y_train,
    epochs=60,
    batch_size=64,
    validation_split=0.15,      # hold out 15% of training data for validation
    verbose=1
)

# ── 5. Evaluate ───────────────────────────────────────────────────────────────
y_proba = model.predict(X_test_s, verbose=0).flatten()
y_pred  = (y_proba >= 0.5).astype(int)

print("\n=== Test Results ===")
print(classification_report(y_test, y_pred, target_names=['Benign', 'Attack']))
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# ── 6. Loss curves ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history.history['loss'],     label='Train loss')
axes[0].plot(history.history['val_loss'], label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Training & Validation Loss')
axes[0].legend()

# Is val_loss diverging? → overfitting. Are both high? → underfitting.
gap = [h - t for h, t in zip(history.history['val_loss'], history.history['loss'])]
axes[1].plot(gap, color='crimson')
axes[1].axhline(0, color='black', linestyle='--')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Val loss − Train loss')
axes[1].set_title('Generalisation Gap (0 = perfect, rising = overfitting)')

plt.tight_layout()
plt.savefig('stage3_neural_networks/lesson1_first_nn.png')
plt.show()
print("\nPlot saved to stage3_neural_networks/lesson1_first_nn.png")
