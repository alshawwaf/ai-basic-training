# Lab — Exercise 2: Train a Random Forest

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_train_random_forest.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
```

---

## Step 3: Generate the PE file dataset

Add this data-generation block. Do not modify it.

```python
np.random.seed(42)
n = 2000
benign = pd.DataFrame({
    'file_entropy':       np.random.normal(5.5, 0.8, n//2).clip(3, 7.9),
    'num_sections':       np.random.poisson(4, n//2).clip(2, 10),
    'num_imports':        np.random.normal(80, 25, n//2).clip(5, 200).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.05).astype(int),
    'virtual_size_ratio': np.random.normal(1.2, 0.3, n//2).clip(0.8, 3),
    'code_section_size':  np.random.normal(50000, 20000, n//2).clip(1000, 200000).astype(int),
    'import_entropy':     np.random.normal(4.2, 0.6, n//2).clip(1, 6),
    'label': 0
})
malware = pd.DataFrame({
    'file_entropy':       np.random.normal(7.2, 0.4, n//2).clip(5, 8),
    'num_sections':       np.random.poisson(6, n//2).clip(2, 15),
    'num_imports':        np.random.normal(35, 20, n//2).clip(0, 150).astype(int),
    'has_packer_sig':     (np.random.rand(n//2) < 0.68).astype(int),
    'virtual_size_ratio': np.random.normal(2.8, 0.8, n//2).clip(0.5, 8),
    'code_section_size':  np.random.normal(15000, 10000, n//2).clip(500, 100000).astype(int),
    'import_entropy':     np.random.normal(3.1, 0.9, n//2).clip(0.5, 5.5),
    'label': 1
})
df = pd.concat([benign, malware], ignore_index=True).sample(frac=1, random_state=42)
FEATURES = ['file_entropy', 'num_sections', 'num_imports', 'has_packer_sig',
            'virtual_size_ratio', 'code_section_size', 'import_entropy']
X = df[FEATURES]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Step 4: Task 1 — Train the random forest

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Train RandomForestClassifier")
print("=" * 60)

rf = RandomForestClassifier(n_estimators=100, oob_score=True,
                             random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
train_acc = rf.score(X_train, y_train)
test_acc  = rf.score(X_test,  y_test)
oob_acc   = rf.oob_score_
print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")
print(f"OOB score:         {oob_acc:.3f}")
```

Run your file. You should see:

```
TASK 1 — Train RandomForestClassifier
============================================================
Training accuracy: ~0.999
Test accuracy:     ~0.943
OOB score:         ~0.941
```

---

## Step 5: Task 2 — Single tree vs forest comparison

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Single tree vs random forest comparison")
print("=" * 60)

dt = DecisionTreeClassifier(max_depth=None, random_state=42)
dt.fit(X_train, y_train)
print(f"{'Model':30s} {'Train':>7} {'Test':>7} {'OOB':>7}")
print("-" * 55)
print(f"{'Single Tree (unlimited)':30s} {dt.score(X_train,y_train):>7.3f} "
      f"{dt.score(X_test,y_test):>7.3f} {'N/A':>7}")
print(f"{'Random Forest (100 trees)':30s} {train_acc:>7.3f} "
      f"{test_acc:>7.3f} {oob_acc:>7.3f}")
```

Run your file. You should see:

```
TASK 2 — Single tree vs random forest comparison
============================================================
Model                          Train    Test     OOB
Single Tree (unlimited)        1.000   0.891     N/A
Random Forest (100 trees)      0.999   0.943   0.941
```

---

## Step 6: Task 3 — Classification report

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Classification report")
print("=" * 60)

y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['benign', 'malware']))
# Malware recall ~0.945 — high recall is critical for security tools
# (missing malware is more costly than a false alarm)
```

Run your file. You should see:

```
TASK 3 — Classification report
============================================================
              precision    recall  f1-score   support

      benign      ~0.948    ~0.941     ~0.944       200
     malware      ~0.939    ~0.945     ~0.942       200

    accuracy                           ~0.943       400
```

---

## Step 7: Task 4 (BONUS) — Hard-to-classify samples

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Hard-to-classify samples")
print("=" * 60)

probs = rf.predict_proba(X_test)[:, 1]   # P(malware)
results = X_test.copy()
results['actual'] = y_test.values
results['P_malware'] = probs

fp = results[results['actual'] == 0].nlargest(5, 'P_malware')
print("Top 5 false positive candidates (benign, high P_malware):")
print(fp[['file_entropy', 'has_packer_sig', 'P_malware']].to_string(index=False))

fn = results[results['actual'] == 1].nsmallest(5, 'P_malware')
print("\nTop 5 hard-to-detect malware (low P_malware):")
print(fn[['file_entropy', 'has_packer_sig', 'P_malware']].to_string(index=False))

print("\n--- Exercise 2 complete. Move to 03_feature_importance.py ---")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_train_random_forest.py`) if anything looks different.
