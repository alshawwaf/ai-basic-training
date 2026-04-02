# Lab — Exercise 4: Evaluate and Improve

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_evaluate_and_improve.py` in this folder.

---

## Step 2: Add the imports, dataset, model, and training setup

This exercise evaluates an already-trained model. Add these imports to the top of your file:

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow import keras

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
```

Run your file. You should see:
```
Model trained. Beginning evaluation...
```

---

## Step 3: Evaluate on the test set (Task 1)

`model.evaluate()` runs a forward pass on labelled data and returns loss and accuracy without updating weights. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 1 — Evaluate on test set")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test loss:     {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")
```

Run your file. You should see:
```
Test loss:     ~0.170
Test accuracy: ~0.940
```

---

## Step 4: Print the classification report (Task 2)

The sigmoid output is a probability. Apply a 0.5 threshold to get class labels, then use sklearn's `classification_report` to see precision, recall, and F1 per class. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Classification report")
print("=" * 60)

y_pred_proba = model.predict(X_test, verbose=0).flatten()
y_pred       = (y_pred_proba > 0.5).astype(int)
print(classification_report(y_test, y_pred, target_names=['benign','attack']))
```

Run your file. You should see:
```
              precision    recall  f1-score   support
      benign       0.96      0.97      0.97       362
      attack       0.73      0.68      0.71        38
    accuracy                           0.94       400
```

---

## Step 5: Compare AUC with logistic regression baseline (Task 3)

AUC is more informative than accuracy on imbalanced data. A simple logistic regression baseline shows whether the neural network is genuinely adding value. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Neural network vs Logistic Regression AUC")
print("=" * 60)

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
lr_proba  = lr.predict_proba(X_test)[:, 1]
nn_proba  = model.predict(X_test, verbose=0).flatten()
lr_auc    = roc_auc_score(y_test, lr_proba)
nn_auc    = roc_auc_score(y_test, nn_proba)
print(f"Logistic Regression AUC: {lr_auc:.4f}")
print(f"Neural Network AUC:      {nn_auc:.4f}")
winner = "Neural Network" if nn_auc > lr_auc else "Logistic Regression"
print(f"Winner: {winner} (by {abs(nn_auc - lr_auc):.4f})")
```

Run your file. You should see approximately:
```
Logistic Regression AUC: ~0.972
Neural Network AUC:      ~0.974
```

---

## Step 6: Test a deeper architecture (Task 4 — Bonus)

Adding a third hidden layer tests whether more depth helps on this dataset. Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Deeper model comparison")
print("=" * 60)

model_deep = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1,  activation='sigmoid')
])
model_deep.compile(optimizer='adam', loss='binary_crossentropy',
                   metrics=['accuracy'])
model_deep.fit(X_train, y_train, validation_split=0.2, epochs=20,
               batch_size=32, verbose=0)
deep_proba = model_deep.predict(X_test, verbose=0).flatten()
deep_auc   = roc_auc_score(y_test, deep_proba)
print(f"Original (2 hidden layers) AUC: {nn_auc:.4f}")
print(f"Deeper   (3 hidden layers) AUC: {deep_auc:.4f}")
print("Note: more depth doesn't always help on simple datasets.")

print("\n--- Workshop complete. Open 04_solution_evaluate_and_improve.py to compare. ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `04_solution_evaluate_and_improve.py` if anything looks different.
