import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score

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
idx = np.random.permutation(len(y))
X, y = X[idx], y[idx]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Scale features, train model, and extract attack probabilities for threshold tuning
scaler  = StandardScaler()
X_tr_sc = scaler.fit_transform(X_train)
X_te_sc = scaler.transform(X_test)
model   = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_tr_sc, y_train)
probs   = model.predict_proba(X_te_sc)[:, 1]   # P(attack) for each test sample

print("=" * 60)
print("TASK 1 — Full precision-recall-threshold table")
print("=" * 60)
# Sweep thresholds from 0.05 to 0.90 and record metrics at each one
thresholds = np.arange(0.05, 0.95, 0.05)
results = []
for t in thresholds:
    y_pred = (probs >= t).astype(int)
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred, zero_division=0)
    alerts = int(y_pred.sum())
    results.append({'threshold': t, 'precision': p, 'recall': r, 'f1': f, 'alerts': alerts})
# Find the threshold that maximises F1 (the best precision-recall balance)
results_df = pd.DataFrame(results)
best_f1_idx = results_df['f1'].idxmax()
print(f"{'Thresh':>6} {'Precision':>9} {'Recall':>7} {'F1':>7} {'Alerts':>7}")
print("-" * 45)
for i, row in results_df.iterrows():
    marker = " ← max F1" if i == best_f1_idx else ""
    print(f"{row['threshold']:>6.2f} {row['precision']:>9.3f} {row['recall']:>7.3f} "
          f"{row['f1']:>7.3f} {row['alerts']:>7}{marker}")

print("\n" + "=" * 60)
print("TASK 2 — Scenario A: Catch all attacks (recall >= 0.95)")
print("=" * 60)
# Start from a high threshold and lower it until we catch >=95% of attacks
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

print("\n" + "=" * 60)
print("TASK 3 — Scenario B: Trusted alerts only (precision >= 0.95)")
print("=" * 60)
# Start from a low threshold and raise it until >=95% of alerts are real attacks
for t in np.arange(0.0, 0.95, 0.01):
    y_pred = (probs >= t).astype(int)
    p = precision_score(y_test, y_pred, zero_division=0)
    if p >= 0.95:
        r = recall_score(y_test, y_pred)
        alerts_test  = int(y_pred.sum())
        alerts_daily = alerts_test * 5
        print(f"Threshold:         {t:.2f}")
        print(f"Precision:         {p:.3f}")
        print(f"Recall:            {r:.3f}")
        print(f"Test alerts:       {alerts_test} / {len(y_test)}")
        print(f"Estimated daily alerts: {alerts_daily}")
        scenario_b_thresh = t
        scenario_b_p, scenario_b_r = p, r
        break

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Stakeholder report")
print("=" * 60)
print("\n--- Exercise 5 complete. Lesson 1.5 workshop done! ---")
print("--- Module 1 complete! Next: module2_intermediate/ ---")
# Translate metrics into real-world SOC numbers: analyst time, missed attacks, false alarms
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
