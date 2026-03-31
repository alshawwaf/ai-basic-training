# =============================================================================
# LESSON 3.9 | WORKSHOP | Exercise 4 of 4
# Evaluate and Improve — Test Set Evaluation, Baseline Comparison
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to use model.evaluate() to get final test loss and accuracy
# - How to convert probabilities to class predictions with a threshold
# - How to generate a classification_report from Keras predictions
# - How to compare a neural network's AUC against a logistic regression baseline
#
# RUN THIS FILE
# -------------
#   python module3_neural_networks/lesson9_first_neural_network/workshop/exercise4_evaluate_and_improve.py
# =============================================================================

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow import keras

# --- Dataset setup (do not modify) ------------------------------------------
X, y = make_classification(n_samples=2000, n_features=10, n_informative=6,
                            weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_split=0.2, epochs=20,
          batch_size=32, verbose=0)
print("Model trained. Beginning evaluation...")
# ----------------------------------------------------------------------------

# =============================================================================
# BACKGROUND
# =============================================================================
# model.evaluate() runs a single forward pass on the given data.
# It returns the loss and each metric you specified in model.compile().
# Unlike model.fit(), it does NOT update any weights.
#
# model.predict() returns raw probabilities (for sigmoid output: values ∈ [0,1]).
# To get class labels (0 or 1), apply a threshold — typically 0.5:
#
#   y_pred_proba = model.predict(X_test).flatten()     # shape: (n_samples,)
#   y_pred_class = (y_pred_proba > 0.5).astype(int)
#
# You can adjust the threshold to trade off precision and recall.
# This is the same concept as threshold tuning from Lesson 1.3!
#
# AUC (Area Under the ROC Curve) measures ranking quality — how well the model
# separates positive from negative examples across ALL possible thresholds.
# AUC = 0.5 → random; AUC = 1.0 → perfect.
# For imbalanced datasets like ours (90/10), AUC is more informative than accuracy.

# =============================================================================
# TASK 1 — model.evaluate() on the Test Set
# =============================================================================
# Call model.evaluate(X_test, y_test, verbose=0)
# Unpack the result into test_loss and test_accuracy.
# Print both values.

print("\n" + "=" * 60)
print("TASK 1 — Evaluate on test set")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
#   print(f"Test loss:     {test_loss:.4f}")
#   print(f"Test accuracy: {test_accuracy:.4f}")

# EXPECTED OUTPUT (approximately):
# Test loss:     ~0.17
# Test accuracy: ~0.94

# =============================================================================
# TASK 2 — Predictions and Classification Report
# =============================================================================
# 1. Get predicted probabilities: model.predict(X_test).flatten()
# 2. Convert to class labels: (probabilities > 0.5).astype(int)
# 3. Print sklearn's classification_report(y_test, y_pred)
# Note: with 90/10 class imbalance, accuracy can be misleading. Look at
# the minority class (label=1) precision, recall, and F1 carefully.

print("\n" + "=" * 60)
print("TASK 2 — Classification report")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   y_pred_proba = model.predict(X_test, verbose=0).flatten()
#   y_pred       = (y_pred_proba > 0.5).astype(int)
#   print(classification_report(y_test, y_pred, target_names=['benign','attack']))

# EXPECTED OUTPUT (approximately):
#               precision    recall  f1-score   support
#       benign       0.96      0.97      0.97       362
#       attack       0.73      0.68      0.71        38
#     accuracy                           0.94       400
#    macro avg       0.85      0.83      0.84       400
# weighted avg       0.94      0.94      0.94       400

# =============================================================================
# TASK 3 — Compare with Logistic Regression Baseline (AUC)
# =============================================================================
# 1. Train a LogisticRegression(max_iter=1000) on X_train/y_train
# 2. Get predicted probabilities for both models on X_test
#    (use model.predict for Keras, lr.predict_proba for sklearn)
# 3. Compute roc_auc_score for each model
# 4. Print both AUC scores and which model wins

print("\n" + "=" * 60)
print("TASK 3 — Neural network vs Logistic Regression AUC")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   lr = LogisticRegression(max_iter=1000, random_state=42)
#   lr.fit(X_train, y_train)
#   lr_proba  = lr.predict_proba(X_test)[:, 1]
#   nn_proba  = model.predict(X_test, verbose=0).flatten()
#   lr_auc    = roc_auc_score(y_test, lr_proba)
#   nn_auc    = roc_auc_score(y_test, nn_proba)
#   print(f"Logistic Regression AUC: {lr_auc:.4f}")
#   print(f"Neural Network AUC:      {nn_auc:.4f}")
#   winner = "Neural Network" if nn_auc > lr_auc else "Logistic Regression"
#   print(f"Winner: {winner} (by {abs(nn_auc - lr_auc):.4f})")

# EXPECTED OUTPUT (approximately):
# Logistic Regression AUC: ~0.972
# Neural Network AUC:      ~0.974
# (Results may be very close — this dataset is fairly linearly separable)

# =============================================================================
# TASK 4 (BONUS) — Add a Third Hidden Layer
# =============================================================================
# Build a deeper model: Dense(64) → Dense(64) → Dense(32) → Dense(1, sigmoid)
# Train it for 20 epochs with the same settings.
# Compare test AUC with the original 2-layer model.
# Does deeper always mean better on this dataset?

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Deeper model comparison")
print("=" * 60)

# >>> YOUR CODE HERE
# Hint:
#   model_deep = keras.Sequential([
#       keras.layers.Dense(64, activation='relu', input_shape=(10,)),
#       keras.layers.Dense(64, activation='relu'),
#       keras.layers.Dense(32, activation='relu'),
#       keras.layers.Dense(1,  activation='sigmoid')
#   ])
#   model_deep.compile(optimizer='adam', loss='binary_crossentropy',
#                      metrics=['accuracy'])
#   model_deep.fit(X_train, y_train, validation_split=0.2, epochs=20,
#                  batch_size=32, verbose=0)
#   deep_proba = model_deep.predict(X_test, verbose=0).flatten()
#   deep_auc   = roc_auc_score(y_test, deep_proba)
#   print(f"Original (2 hidden layers) AUC: {nn_auc:.4f}")
#   print(f"Deeper   (3 hidden layers) AUC: {deep_auc:.4f}")
#   print("Note: more depth doesn't always help on simple datasets.")

print("\n--- Workshop complete. Open reference_solution.py ---")
