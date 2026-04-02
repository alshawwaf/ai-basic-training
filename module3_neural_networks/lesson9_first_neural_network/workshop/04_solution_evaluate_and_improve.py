# Exercise 4 — Evaluate and Improve
#
# Demonstrates model.evaluate vs model.predict, converting sigmoid
# probabilities to class labels, reading classification_report on
# imbalanced data, and comparing AUC against a logistic regression baseline.
#
# Prerequisite: pip install tensorflow scikit-learn matplotlib

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression

print("=" * 60)
print("EXERCISE 4 — Evaluate and Improve")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup (same binary classification problem) ───────────────────────────
X, y = make_classification(
    n_samples=5000, n_features=12, n_informative=8, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print(f"Training samples: {len(X_train)} | Test samples: {len(X_test)}")
print(f"Attack rate: {y.mean()*100:.1f}%")

# ── Build, compile, and train ────────────────────────────────────────────────────
model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
], name='intrusion_detector')

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("\nTraining...")
history = model.fit(
    X_train_s, y_train,
    epochs=60,
    batch_size=64,
    validation_split=0.15,
    verbose=0
)
print(f"Trained for {len(history.history['loss'])} epochs.")

# ── TASK 1 — model.evaluate() on the Test Set ───────────────────────────────────
# model.evaluate runs a forward pass (no weight updates) and returns (loss, metrics).
# This is the only honest performance estimate — the test set was never seen
# during training or validation.
print("\n" + "=" * 60)
print("TASK 1 — model.evaluate() on the Test Set")
print("=" * 60)

test_loss, test_acc = model.evaluate(X_test_s, y_test, verbose=0)
print(f"Test loss:     {test_loss:.4f}")
print(f"Test accuracy: {test_acc:.4f}")

# ── TASK 2 — Classification Report ──────────────────────────────────────────────
# model.predict returns raw probabilities (shape (n,1) for binary).
# .flatten() converts to 1D so it works with sklearn metrics.
# Threshold 0.5: P >= 0.5 → predict "attack"; P < 0.5 → predict "benign".
print("\n" + "=" * 60)
print("TASK 2 — Classification Report")
print("=" * 60)

y_proba = model.predict(X_test_s, verbose=0).flatten()
y_pred  = (y_proba >= 0.5).astype(int)

# classification_report shows precision, recall, F1 per class
# Focus on the minority class (attack/label=1) — the interesting one
print(classification_report(y_test, y_pred, target_names=['Benign', 'Attack']))

nn_auc = roc_auc_score(y_test, y_proba)
print(f"Neural Network ROC AUC: {nn_auc:.4f}")

# ── TASK 3 — AUC Comparison with Logistic Regression ────────────────────────────
# Always benchmark against a simple baseline. On small tabular data,
# logistic regression often matches or beats a neural network.
print("\n" + "=" * 60)
print("TASK 3 — AUC Comparison with Logistic Regression")
print("=" * 60)

# Train logistic regression on the same scaled data
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_s, y_train)
lr_proba = lr_model.predict_proba(X_test_s)[:, 1]
lr_auc   = roc_auc_score(y_test, lr_proba)

print(f"Logistic Regression AUC: {lr_auc:.4f}")
print(f"Neural Network AUC:      {nn_auc:.4f}")
diff = nn_auc - lr_auc
print(f"Difference:              {diff:+.4f}")

if abs(diff) < 0.01:
    print("Difference is tiny — the simpler model (LogReg) is probably the right choice.")
elif diff > 0:
    print("Neural network wins, but verify the margin justifies the extra complexity.")
else:
    print("Logistic regression wins — the data may be too simple for a neural network.")

# ── TASK 4 (BONUS) — Deeper Network ─────────────────────────────────────────────
# Adding a third hidden layer doesn't always help on simple tabular data.
# More depth = more capacity, but also more risk of overfitting.
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Deeper Network")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

model_deep = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_s.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(16, activation='relu'),   # additional hidden layer
    keras.layers.Dense(1,  activation='sigmoid')
], name='deeper_detector')

model_deep.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model_deep.fit(
    X_train_s, y_train,
    epochs=60, batch_size=64,
    validation_split=0.15, verbose=0
)

y_proba_deep = model_deep.predict(X_test_s, verbose=0).flatten()
deep_auc = roc_auc_score(y_test, y_proba_deep)

print(f"2-layer NN AUC: {nn_auc:.4f}")
print(f"3-layer NN AUC: {deep_auc:.4f}")
print(f"Difference:     {deep_auc - nn_auc:+.4f}")
print("On simple tabular datasets, deeper doesn't always win.")

# ── Loss curves plot ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history.history['loss'],     label='Train loss')
axes[0].plot(history.history['val_loss'], label='Val loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Training & Validation Loss')
axes[0].legend()

# Generalisation gap: positive = val_loss > train_loss = overfitting
gap = [v - t for v, t in zip(history.history['val_loss'], history.history['loss'])]
axes[1].plot(gap, color='crimson')
axes[1].axhline(0, color='black', linestyle='--')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Val loss - Train loss')
axes[1].set_title('Generalisation Gap (0 = perfect, rising = overfitting)')

plt.tight_layout()
plt.savefig('lesson9_ex4_evaluate.png')
plt.show()
print("\nPlot saved to lesson9_ex4_evaluate.png")

print("\n--- Lesson 9 done. All exercises complete! ---")
