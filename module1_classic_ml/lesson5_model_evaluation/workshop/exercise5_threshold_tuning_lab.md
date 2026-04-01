# Lab -- Exercise 5: Threshold Tuning for Your Use Case

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise5_threshold_tuning.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
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
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)
model   = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_tr_sc, y_train)
probs   = model.predict_proba(X_te_sc)[:, 1]   # P(attack) for each test sample
```

---

## Step 4: Build the Full Precision-Recall-Threshold Table

For each threshold in np.arange(0.05, 0.95, 0.05): - Compute precision, recall, F1, and number of alerts (y_pred.sum()) Print as a formatted table. Mark the row with the highest F1.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Full precision-recall-threshold table")
print("=" * 60)
thresholds = np.arange(0.05, 0.95, 0.05)
results = []
for t in thresholds:
    y_pred = (probs >= t).astype(int)
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred, zero_division=0)
    alerts = int(y_pred.sum())
    results.append({'threshold': t, 'precision': p, 'recall': r, 'f1': f, 'alerts': alerts})
results_df = pd.DataFrame(results)
best_f1_idx = results_df['f1'].idxmax()
print(f"{'Thresh':>6} {'Precision':>9} {'Recall':>7} {'F1':>7} {'Alerts':>7}")
print("-" * 45)
for i, row in results_df.iterrows():
    marker = " ← max F1" if i == best_f1_idx else ""
    print(f"{row['threshold']:>6.2f} {row['precision']:>9.3f} {row['recall']:>7.3f} "
          f"{row['f1']:>7.3f} {row['alerts']:>7}{marker}")
```

Run your file. You should see:
```
Thresh Precision  Recall      F1  Alerts
0.10     ~0.74    ~0.99   ~0.85     267
...
0.50     ~0.93    ~0.91   ~0.92     196   ← max F1
...
0.90     ~0.99    ~0.70   ~0.82     141
```

---

## Step 5: Scenario A: Maximum Coverage (Recall >= 0.95)

Find the LOWEST threshold where recall >= 0.95. Print the threshold, precision, recall, and the daily alert count (scale: test has 2000 samples; assume 10,000 events/day → multiply by 5).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Scenario A: Catch all attacks (recall >= 0.95)")
print("=" * 60)
for t in np.arange(0.9, 0.0, -0.01):
    y_pred = (probs >= t).astype(int)
    r = recall_score(y_test, y_pred)
    if r >= 0.95:
        p = precision_score(y_test, y_pred, zero_division=0)
        alerts_test  = int(y_pred.sum())
        alerts_daily = alerts_test * 5   # scale to 10,000 events/day
        print(f"Threshold:         {t:.2f}")
        print(f"Recall:            {r:.3f}")
        print(f"Precision:         {p:.3f}")
        print(f"Test alerts:       {alerts_test} / {len(y_test)}")
        print(f"Estimated daily alerts: {alerts_daily}")
        scenario_a_thresh = t
        scenario_a_p, scenario_a_r = p, r
        break
```

Run your file. You should see:
```
Threshold:    ~0.20
Recall:       ~0.980
Precision:    ~0.784
Estimated daily alerts: ~1250
```

---

## Step 6: Scenario B: High Fidelity (Precision >= 0.95)

Find the LOWEST threshold where precision >= 0.95. Print the threshold, precision, recall, and daily alert count.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Scenario B: Trusted alerts only (precision >= 0.95)")
print("=" * 60)
```

Run your file. You should see:
```
Threshold:    ~0.68
Precision:    ~0.951
Recall:       ~0.760
Estimated daily alerts: ~400
```

---

## Step 7: TASK 4 (BONUS) — Stakeholder Report

For both thresholds, print a human-readable paragraph describing the tradeoff in business terms (attacks per day, false alarms per day, analyst hours at 5 minutes per alert review).

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Stakeholder report")
print("=" * 60)
print("\n--- Exercise 5 complete. Lesson 1.5 workshop done! ---")
print("--- Module 1 complete! Next: module2_intermediate/ ---")
daily_attacks = 500    # 5% of 10,000
mins_per_alert = 5
for label, thresh, p, r in [
    ("Scenario A (Catch All)", scenario_a_thresh, scenario_a_p, scenario_a_r),
    ("Scenario B (Trusted Alerts)", scenario_b_thresh, scenario_b_p, scenario_b_r),
]:
    caught_per_day     = int(r * daily_attacks)
    missed_per_day     = daily_attacks - caught_per_day
    alerts_per_day     = int(caught_per_day / p) if p > 0 else 0
    false_alarms_day   = alerts_per_day - caught_per_day
    analyst_hours_day  = alerts_per_day * mins_per_alert / 60
    print(f"\n{label} (threshold={thresh:.2f}):")
    print(f"  Attacks caught per day:     {caught_per_day} / {daily_attacks}")
    print(f"  Attacks missed per day:     {missed_per_day}")
    print(f"  False alarms per day:       {false_alarms_day}")
    print(f"  Total analyst reviews/day:  {alerts_per_day}")
    print(f"  Estimated analyst time:     {analyst_hours_day:.1f} hours/day")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
