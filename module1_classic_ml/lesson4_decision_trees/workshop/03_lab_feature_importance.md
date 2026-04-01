# Lab -- Exercise 3: Feature Importance

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise3_feature_importance.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_per_class = 500
def make_traffic():
    benign = pd.DataFrame({
        'connection_rate':    np.random.normal(10, 3, n_per_class).clip(1, 25),
        'bytes_sent':         np.random.normal(5000, 1500, n_per_class).clip(100, 15000),
        'bytes_received':     np.random.normal(8000, 2000, n_per_class).clip(100, 20000),
        'unique_dest_ports':  np.random.poisson(3, n_per_class).clip(1, 10),
        'duration_seconds':   np.random.normal(30, 10, n_per_class).clip(1, 120),
        'failed_connections': np.random.poisson(0.5, n_per_class),
        'label': 0
    })
    port_scan = pd.DataFrame({
        'connection_rate':    np.random.normal(25, 8, n_per_class).clip(5, 60),
        'bytes_sent':         np.random.normal(500, 200, n_per_class).clip(50, 2000),
        'bytes_received':     np.random.normal(300, 100, n_per_class).clip(0, 1000),
        'unique_dest_ports':  np.random.normal(45, 10, n_per_class).clip(20, 100).astype(int),
        'duration_seconds':   np.random.normal(5, 2, n_per_class).clip(1, 20),
        'failed_connections': np.random.poisson(8, n_per_class),
        'label': 1
    })
    exfil = pd.DataFrame({
        'connection_rate':    np.random.normal(8, 2, n_per_class).clip(1, 20),
        'bytes_sent':         np.random.normal(80000, 25000, n_per_class).clip(20000, 250000),
        'bytes_received':     np.random.normal(1000, 300, n_per_class).clip(100, 5000),
        'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
        'duration_seconds':   np.random.normal(180, 60, n_per_class).clip(60, 600),
        'failed_connections': np.random.poisson(0.2, n_per_class),
        'label': 2
    })
    dos = pd.DataFrame({
        'connection_rate':    np.random.normal(200, 40, n_per_class).clip(80, 500),
        'bytes_sent':         np.random.normal(200, 80, n_per_class).clip(40, 600),
        'bytes_received':     np.random.normal(100, 40, n_per_class).clip(0, 400),
        'unique_dest_ports':  np.random.poisson(2, n_per_class).clip(1, 5),
        'duration_seconds':   np.random.normal(0.5, 0.2, n_per_class).clip(0.1, 2),
        'failed_connections': np.random.poisson(3, n_per_class),
        'label': 3
    })
    return pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(
        frac=1, random_state=42
    )
df = make_traffic()
FEATURES    = ['connection_rate', 'bytes_sent', 'bytes_received',
               'unique_dest_ports', 'duration_seconds', 'failed_connections']
CLASS_NAMES = ['benign', 'port_scan', 'exfil', 'DoS']
X = df[FEATURES]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)
```

---

## Step 4: Extract and Print Feature Importances

Create a DataFrame with columns 'feature' and 'importance'. Sort by importance descending. Print it. Verify that importances sum to 1.0.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Feature importances (sorted)")
print("=" * 60)
importances = model.feature_importances_
imp_df = pd.DataFrame({'feature': FEATURES, 'importance': importances})
imp_df = imp_df.sort_values('importance', ascending=False)
print(imp_df.to_string(index=False))
total = importances.sum()
print(f"\nSum of importances: {total:.3f} {'✓' if abs(total-1.0)<0.001 else '✗'}")
```

Run your file. You should see:
```
feature                 importance
connection_rate           0.524
bytes_sent                0.283
unique_dest_ports         0.107
duration_seconds          0.052
failed_connections        0.024
bytes_received            0.010
Sum of importances: 1.000 ✓
```

---

## Step 5: Feature Importance Bar Chart

Create a HORIZONTAL bar chart. Sort features by importance ascending (so most important is at top). Add the importance value as a text label at the end of each bar.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Feature importance bar chart")
print("=" * 60)
print("Bar chart created.")
sorted_df = imp_df.sort_values('importance', ascending=True)  # ascending for horizontal
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(sorted_df['feature'], sorted_df['importance'], color='steelblue')
for bar, val in zip(bars, sorted_df['importance']):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center')
ax.set_xlabel('Feature Importance (Mean Decrease in Impurity)')
ax.set_title('Decision Tree Feature Importance — Network Traffic Classifier')
plt.tight_layout()
plt.show()
```

---

## Step 6: Retrain with Top-3 Features

Identify the top 3 features from imp_df. Retrain the model using only those features. Print and compare accuracy: full model vs top-3 model.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Top-3 feature model vs full model")
print("=" * 60)
top3 = imp_df.nlargest(3, 'importance')['feature'].tolist()
print(f"Top-3 features: {top3}")
model_top3 = DecisionTreeClassifier(max_depth=4, random_state=42)
model_top3.fit(X_train[top3], y_train)
acc_full = model.score(X_test, y_test)
acc_top3 = model_top3.score(X_test[top3], y_test)
print(f"Full model accuracy:  {acc_full:.3f}")
print(f"Top-3 model accuracy: {acc_top3:.3f}")
print(f"Accuracy drop:        {acc_full - acc_top3:.3f}")
```

Run your file. You should see:
```
Top-3 features: ['connection_rate', 'bytes_sent', 'unique_dest_ports']
Full model accuracy:  ~0.962
Top-3 model accuracy: ~0.951
Accuracy drop:        ~0.011
```

---

## Step 7: TASK 4 (BONUS) — Security Interpretation of Importances

Write a comment for each feature explaining whether its importance rank makes intuitive sense from a network security standpoint. Then answer: which feature would you add to a real-time firewall rule first?

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Security interpretation")
print("=" * 60)
print("\n--- Exercise 3 complete. Move to exercise4_depth_and_overfitting.py ---")
interpretations = {
  "connection_rate":    "Highest importance — DoS is identified by extreme rate.",
  "bytes_sent":         "Separates exfil (very high) from port scans (very low).",
  "unique_dest_ports":  "Port scans hit many ports; benign/exfil hit very few.",
  "duration_seconds":   "Exfil connections last minutes; DoS/port scans last seconds.",
  "failed_connections": "Port scans produce many failed connections; benign has few.",
  "bytes_received":     "Benign receives more data; attacks mostly send or probe.",
}
for feature, interp in interpretations.items():
  print(f"{feature:22s}: {interp}")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
