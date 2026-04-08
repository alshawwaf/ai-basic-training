import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (precision_score, recall_score, f1_score,
                             classification_report, fbeta_score)

# Same imbalanced dataset (95% benign, 5% attack)
np.random.seed(42)
n_benign, n_attack = 9_500, 500
benign_data = np.column_stack([
    np.random.normal(10, 3, n_benign),
    np.random.normal(5000, 1500, n_benign),
    np.random.poisson(3, n_benign)
])
attack_data = np.column_stack([
    np.random.normal(80, 30, n_attack),
    np.random.normal(500, 300, n_attack),
    np.random.poisson(30, n_attack)
])
X = np.vstack([benign_data, attack_data])
y = np.array([0]*n_benign + [1]*n_attack)
# Add per-feature Gaussian noise so classes overlap the way real captures do.
rng = np.random.default_rng(7)
X = X + rng.normal(0, X.std(axis=0) * 1.9, X.shape)
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Only LogisticRegression needs scaled features; DecisionTree handles raw values fine
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)

print("=" * 60)
print("TASK 1 — Model comparison: attack-class metrics")
print("=" * 60)
# Train 3 models to compare: a baseline that always guesses majority, and 2 real learners
dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
lr    = LogisticRegression(max_iter=1000, random_state=42).fit(X_tr_sc, y_train)
dt    = DecisionTreeClassifier(max_depth=5, random_state=42).fit(X_train, y_train)

models_and_preds = [
    ("DummyClassifier",     dummy.predict(X_test)),
    ("LogisticRegression",  lr.predict(X_te_sc)),
    ("DecisionTree",        dt.predict(X_test)),
]
# All metrics below are for the attack class (class 1) specifically
print(f"{'Model':25s} {'Precision':>9} {'Recall':>7} {'F1':>7}")
print("-" * 55)
for name, y_pred in models_and_preds:
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred)
    print(f"{name:25s} {p:>9.3f} {r:>7.3f} {f:>7.3f}")

print("\n" + "=" * 60)
print("TASK 2 — Full classification report")
print("=" * 60)
# classification_report shows precision/recall/f1 for BOTH classes in one table
y_pred_lr = lr.predict(X_te_sc)
print(classification_report(y_test, y_pred_lr, target_names=['benign', 'attack']))
print("To catch every attack: optimise RECALL for attack class")
print("To minimise false alarms: optimise PRECISION for attack class")

print("\n" + "=" * 60)
print("TASK 3 — Precision and recall across thresholds")
print("=" * 60)
print("Precision-recall vs threshold plot created.")

# Get raw probabilities instead of hard predictions so we can vary the threshold
probs = lr.predict_proba(X_te_sc)[:, 1]
thresholds = np.arange(0.1, 1.0, 0.1)
precisions, recalls = [], []
for t in thresholds:
    # Classify as attack if P(attack) >= threshold (default is 0.5)
    y_pred_t = (probs >= t).astype(int)
    precisions.append(precision_score(y_test, y_pred_t, zero_division=0))
    recalls.append(recall_score(y_test, y_pred_t))
plt.figure(figsize=(9, 5))
plt.plot(thresholds, precisions, 'b-o', label='Precision')
plt.plot(thresholds, recalls,    'r-s', label='Recall')
plt.axvline(0.5, color='grey', linestyle='--', alpha=0.7, label='Default threshold')
plt.xlabel('Decision Threshold')
plt.ylabel('Score')
plt.title('Precision and Recall vs Threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — F1 vs F2 score")
print("=" * 60)
print(f"{'Model':25s} {'F1':>7} {'F2':>7}")
print("-" * 42)
# fbeta_score with beta=2 penalises missed attacks more than false alarms
for name, y_pred in models_and_preds:
    f1 = f1_score(y_test, y_pred, zero_division=0)
    f2 = fbeta_score(y_test, y_pred, beta=2, zero_division=0)
    print(f"{name:25s} {f1:>7.3f} {f2:>7.3f}")
# F2 weighs recall higher than precision -- better for security where missing
# an attack (low recall) is more costly than investigating a false alarm (low precision)
