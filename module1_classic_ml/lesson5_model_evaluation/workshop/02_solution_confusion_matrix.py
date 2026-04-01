import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# Same synthetic network traffic dataset as exercise 1 (95% benign, 5% attack)
np.random.seed(42)
n_total, n_attack, n_benign = 10_000, 500, 9_500
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
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale, train, and get predictions to build a confusion matrix from
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)
model   = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_tr_sc, y_train)
y_pred  = model.predict(X_te_sc)

print("=" * 60)
print("TASK 1 — Manual confusion matrix values")
print("=" * 60)
# Compute the 4 confusion matrix cells by comparing predictions vs ground truth
TP = np.sum((y_pred == 1) & (y_test == 1))  # correctly flagged attacks
TN = np.sum((y_pred == 0) & (y_test == 0))  # correctly ignored benign
FP = np.sum((y_pred == 1) & (y_test == 0))  # false alarms
FN = np.sum((y_pred == 0) & (y_test == 1))  # missed attacks
print(f"True Negatives  (TN) = {TN:4d}  — benign correctly ignored")
print(f"False Positives (FP) = {FP:4d}  — benign falsely flagged (alert fatigue)")
print(f"False Negatives (FN) = {FN:4d}  — ATTACKS MISSED! (most dangerous)")
print(f"True Positives  (TP) = {TP:4d}  — attacks correctly caught")
print(f"\nTotal: {TP+TN+FP+FN} (should be {len(y_test)})")

print("\n" + "=" * 60)
print("TASK 2 — sklearn confusion matrix")
print("=" * 60)
# sklearn's confusion_matrix returns the same 4 values in a 2x2 array
# Layout: rows = actual class, cols = predicted class
cm = confusion_matrix(y_test, y_pred)
print("              Predicted Benign  Predicted Attack")
print(f"Actual Benign      {cm[0,0]:6d}            {cm[0,1]:6d}")
print(f"Actual Attack      {cm[1,0]:6d}            {cm[1,1]:6d}")
matches = (cm[0,0]==TN and cm[0,1]==FP and cm[1,0]==FN and cm[1,1]==TP)
print(f"\nMatches manual calculation: {matches} {'✓' if matches else '✗'}")

print("\n" + "=" * 60)
print("TASK 3 — Metrics derived from confusion matrix")
print("=" * 60)
# Every standard metric can be derived from these 4 values
accuracy    = (TP + TN) / (TP + TN + FP + FN)   # overall correct rate (misleading when imbalanced)
precision   = TP / (TP + FP)                     # of all alerts, how many were real attacks?
recall      = TP / (TP + FN)                     # of all real attacks, how many did we catch?
specificity = TN / (TN + FP)                     # of all benign, how many did we correctly ignore?
f1          = 2 * precision * recall / (precision + recall)  # harmonic mean of precision & recall
print(f"Accuracy    = (TP+TN)/(TP+TN+FP+FN) = {accuracy:.3f}")
print(f"Precision   = TP/(TP+FP)             = {precision:.3f}")
print(f"Recall      = TP/(TP+FN)             = {recall:.3f}")
print(f"Specificity = TN/(TN+FP)             = {specificity:.3f}")
print(f"F1          = 2*P*R/(P+R)            = {f1:.3f}")

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Heatmap visualisation")
print("=" * 60)
print("\n--- Exercise 2 complete. Move to exercise3_precision_recall_f1.py ---")
# Heatmap gives a quick visual feel for where the model gets it right vs wrong
if HAS_SEABORN:
    labels = [['TN', 'FP'], ['FN', 'TP']]
    pcts   = cm / cm.sum() * 100
    annots = [[f"{cm[i,j]}\n({pcts[i,j]:.1f}%)" for j in range(2)] for i in range(2)]
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=annots, fmt='', cmap='Blues',
                xticklabels=['Benign', 'Attack'],
                yticklabels=['Benign', 'Attack'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix — Intrusion Detector')
    plt.tight_layout()
    plt.show()
else:
    print("seaborn not installed — skipping heatmap")
