# Lab -- Exercise 4: Anomaly Scoring

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `04_anomaly_scoring.py` in this folder.

---

## Step 2: Add the imports

Add these imports to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
```

---

## Step 3: Set up the dataset

This code creates the data for this exercise. Add it after the imports:

```python
np.random.seed(42)
n_per = 750
def make_full_dataset():
    benign = pd.DataFrame({'connection_rate': np.random.normal(10,3,n_per).clip(1,25),
        'bytes_sent': np.random.normal(5000,1500,n_per).clip(100,15000),
        'bytes_received': np.random.normal(8000,2000,n_per).clip(100,20000),
        'unique_dest_ports': np.random.poisson(3,n_per).clip(1,10),
        'duration_seconds': np.random.normal(30,10,n_per).clip(1,120),
        'failed_connections': np.random.poisson(0.5,n_per), 'true_label':0})
    port_scan = pd.DataFrame({'connection_rate': np.random.normal(25,8,n_per).clip(5,60),
        'bytes_sent': np.random.normal(500,200,n_per).clip(50,2000),
        'bytes_received': np.random.normal(300,100,n_per).clip(0,1000),
        'unique_dest_ports': np.random.normal(45,10,n_per).clip(20,100).astype(int),
        'duration_seconds': np.random.normal(5,2,n_per).clip(1,20),
        'failed_connections': np.random.poisson(8,n_per), 'true_label':1})
    exfil = pd.DataFrame({'connection_rate': np.random.normal(8,2,n_per).clip(1,20),
        'bytes_sent': np.random.normal(80000,25000,n_per).clip(20000,250000),
        'bytes_received': np.random.normal(1000,300,n_per).clip(100,5000),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(180,60,n_per).clip(60,600),
        'failed_connections': np.random.poisson(0.2,n_per), 'true_label':2})
    dos = pd.DataFrame({'connection_rate': np.random.normal(200,40,n_per).clip(80,500),
        'bytes_sent': np.random.normal(200,80,n_per).clip(40,600),
        'bytes_received': np.random.normal(100,40,n_per).clip(0,400),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(0.5,0.2,n_per).clip(0.1,2),
        'failed_connections': np.random.poisson(3,n_per), 'true_label':3})
    return pd.concat([benign,port_scan,exfil,dos],ignore_index=True).sample(frac=1,random_state=42)
df_full = make_full_dataset()
FEATURES = ['connection_rate','bytes_sent','bytes_received',
            'unique_dest_ports','duration_seconds','failed_connections']
X = df_full[FEATURES]
true_labels = df_full['true_label'].values
scaler  = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)
```

---

## Step 4: Compute Anomaly Scores

Use kmeans.transform(X_scaled) to get distances to all centroids. Take np.min(..., axis=1) to get distance to nearest centroid. Print: mean, std, min, max, 95th percentile of anomaly scores.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Anomaly score distribution")
print("=" * 60)
all_distances = kmeans.transform(X_scaled)   # shape (3000, 4)
anomaly_scores = np.min(all_distances, axis=1)
print(f"Mean:       {anomaly_scores.mean():.3f}")
print(f"Std:        {anomaly_scores.std():.3f}")
print(f"Min:        {anomaly_scores.min():.3f}")
print(f"Max:        {anomaly_scores.max():.3f}")
print(f"95th pct:   {np.percentile(anomaly_scores, 95):.3f}")
```

Run your file. You should see:
```
Mean: ~1.82, Std: ~0.94, Max: ~8.21
```

---

## Step 5: Flag Anomalies at 95th Percentile

Set threshold = 95th percentile of anomaly_scores. Flag samples where anomaly_score > threshold. Print: threshold value, number flagged, percentage flagged.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Flag top-5% anomalies")
print("=" * 60)
threshold = np.percentile(anomaly_scores, 95)
flagged   = anomaly_scores > threshold
print(f"Threshold (95th pct): {threshold:.3f}")
print(f"Flagged anomalies:    {flagged.sum()} / {len(anomaly_scores)} ({flagged.mean()*100:.1f}%)")
```

Run your file. You should see:
```
Threshold: ~3.87
Flagged anomalies: ~150 / 3000 (5.0%)
```

---

## Step 6: Verify Against True Labels

Of the flagged anomalies, compute: precision = fraction that are true attacks (true_label != 0) recall    = fraction of ALL attacks that were flagged

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Verification: flagged anomalies vs true attacks")
print("=" * 60)
is_attack = true_labels != 0
true_positives = np.sum(flagged & is_attack)
precision = true_positives / flagged.sum()
recall    = true_positives / is_attack.sum()
print(f"Total attacks in dataset: {is_attack.sum()}")
print(f"Flagged anomalies:        {flagged.sum()}")
print(f"True attacks in flagged:  {true_positives}")
print(f"Precision: {precision:.3f}  (of flagged, fraction are real attacks)")
print(f"Recall:    {recall:.3f}  (of all attacks, fraction were flagged)")
print(f"\nNote: recall is low because attacks form their own clusters.")
print(f"K-Means detects isolated outliers, not attack clusters.")
```

Run your file. You should see:
```
Precision: ~0.79 (most flagged items are truly anomalous)
Recall:    ~0.05 (most attacks form their own dense cluster, are not flagged)
```

---

## Step 7: TASK 4 (BONUS) — Anomaly Score Distribution Plot

Plot histogram of anomaly_scores. Mark the threshold with a vertical red line. Shade the flagged region red, normal region blue.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Anomaly score histogram")
print("=" * 60)
print("\n--- Exercise 4 complete. Lesson 2.3 workshop done! ---")
print("--- Next: stage2_intermediate/04_overfitting_crossval/ ---")
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(anomaly_scores[~flagged], bins=60, color='steelblue', alpha=0.7, label='Normal')
ax.hist(anomaly_scores[flagged],  bins=30, color='red',       alpha=0.7, label='Flagged anomalies')
ax.axvline(threshold, color='black', linestyle='--', label=f'Threshold={threshold:.2f}')
ax.set_xlabel('Anomaly Score (distance to nearest centroid)')
ax.set_ylabel('Count')
ax.set_title('Anomaly Score Distribution')
ax.legend()
plt.show()
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solve.py`) if anything looks different.
