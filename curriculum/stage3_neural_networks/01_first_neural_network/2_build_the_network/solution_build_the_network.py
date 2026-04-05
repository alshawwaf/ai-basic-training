# Exercise 2 — Build the Network
#
# Covers activation-function choices (relu for hidden layers, sigmoid
# for binary output, softmax for multi-class) and how to compile a
# model with the right optimizer, loss, and metrics.
#
# Prerequisite: pip install tensorflow scikit-learn

import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("EXERCISE 2 — Build the Network")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── Dataset setup ────────────────────────────────────────────────────────────────
# Binary classification: 10 features, 2000 samples, 12% positive class
X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=7, n_redundant=2,
    weights=[0.88, 0.12], flip_y=0.03, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# StandardScaler centres each feature to mean=0, std=1
# Neural networks train much better on standardised input
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

print(f"Training samples: {len(X_train)} | Test samples: {len(X_test)}")
print(f"Input features: {X_train_s.shape[1]}")

# ── TASK 1 — Build the Binary Classifier ────────────────────────────────────────
# Hidden layers use relu: cheap, avoids vanishing gradients.
# Output layer uses sigmoid: maps any real number to [0, 1] probability.
print("\n" + "=" * 60)
print("TASK 1 — Build the Binary Classifier")
print("=" * 60)

model = keras.Sequential([
    # First hidden layer: 64 neurons, relu activation
    # input_shape=(10,) tells Keras the input has 10 features
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_s.shape[1],)),
    # Second hidden layer: 32 neurons, relu activation
    keras.layers.Dense(32, activation='relu'),
    # Output layer: 1 neuron, sigmoid activation
    # sigmoid → P(attack), value between 0 and 1
    keras.layers.Dense(1,  activation='sigmoid')
], name='binary_classifier')

model.summary()

# ── TASK 2 — Parameter Count Breakdown ───────────────────────────────────────────
# Formula per Dense layer: (n_inputs x n_units) + n_units
print("\n" + "=" * 60)
print("TASK 2 — Parameter Count Breakdown")
print("=" * 60)

# Layer 1: Dense(64) receiving 10 inputs
l1 = (10 * 64) + 64   # 640 + 64 = 704
print(f"Dense(64): (10 x 64) + 64 = {l1}")

# Layer 2: Dense(32) receiving 64 inputs (from layer 1)
l2 = (64 * 32) + 32   # 2048 + 32 = 2080
print(f"Dense(32): (64 x 32) + 32 = {l2}")

# Layer 3: Dense(1) receiving 32 inputs (from layer 2)
l3 = (32 * 1) + 1     # 32 + 1 = 33
print(f"Dense(1):  (32 x 1)  + 1  = {l3}")

total_manual = l1 + l2 + l3
total_keras  = model.count_params()
print(f"Total (manual): {total_manual}")
print(f"Total (Keras):  {total_keras}")
print(f"Match: {total_manual == total_keras}")

# ── TASK 3 — Compile the Model ──────────────────────────────────────────────────
# compile() sets up the training configuration — no data is seen yet.
# adam = adaptive optimizer that adjusts learning rate per weight
# binary_crossentropy = log loss for binary classification
# accuracy = displayed during training (but AUC is more informative)
print("\n" + "=" * 60)
print("TASK 3 — Compile the Model")
print("=" * 60)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Model compiled successfully.")
print(f"Optimizer: {model.optimizer.__class__.__name__}")
print(f"Loss:      {model.loss}")

# ── TASK 4 (BONUS) — 3-Class Architecture ────────────────────────────────────────
# For multi-class problems, switch: Dense(N, softmax) + sparse_categorical_crossentropy
# Softmax outputs N probabilities that sum to 1.0
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — 3-Class Architecture")
print("=" * 60)

# Create a 3-class dataset
X_multi, y_multi = make_classification(
    n_samples=2000, n_features=10, n_informative=7,
    n_classes=3, n_clusters_per_class=1, random_state=42
)
print(f"Classes: {np.unique(y_multi)}  (3 classes)")

# Build a multi-class model
# Output layer has 3 units (one per class) with softmax activation
model_multi = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    # 3 output units + softmax: each output = P(class_i), all sum to 1.0
    keras.layers.Dense(3,  activation='softmax')
], name='multiclass_classifier')

# sparse_categorical_crossentropy works with integer labels (0, 1, 2)
# categorical_crossentropy requires one-hot encoded labels
model_multi.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_multi.summary()

# Show that softmax outputs sum to 1.0
X_sample = np.random.randn(1, 10).astype('float32')
probs = model_multi.predict(X_sample, verbose=0)
print(f"\nSoftmax output: {probs.flatten()}")
print(f"Sum of probabilities: {probs.sum():.4f}  (should be 1.0)")

print("\n--- Exercise 2 complete. Move to ../3_compile_and_train/solution.py ---")
