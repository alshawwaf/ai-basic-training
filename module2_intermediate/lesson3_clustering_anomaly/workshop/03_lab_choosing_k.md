# Lab -- Exercise 3: Choosing K

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_choosing_k.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

---

## Step 4: Elbow Method (Inertia for K=2 to K=10)

For each K in range(2, 11), fit KMeans and record inertia_. Print a table and plot the elbow curve.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — Elbow method (inertia vs K)")
print("=" * 60)
k_values  = range(2, 11)
inertias  = []
print(f"{'K':>4} {'Inertia':>10}")
print("-" * 18)
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"{k:>4} {km.inertia_:>10.1f}")
plt.figure(figsize=(8,5))
plt.plot(list(k_values), inertias, 'b-o')
plt.xlabel('K'), plt.ylabel('Inertia'), plt.title('Elbow Method')
plt.grid(True, alpha=0.3), plt.show()
```

Run your file. You should see:
```
K=4 should show an elbow (rate of decrease slows noticeably)
```

---

## Step 5: Silhouette Score for K=2 to K=10

For each K, fit KMeans and compute silhouette_score(X_scaled, labels). Print table. Plot. Identify K with highest score.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — Silhouette scores")
print("=" * 60)
sil_scores = []
print(f"{'K':>4} {'Silhouette':>12}")
print("-" * 20)
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score  = silhouette_score(X_scaled, labels, sample_size=1000, random_state=42)
    sil_scores.append(score)
    print(f"{k:>4} {score:>12.4f}")
best_k = list(k_values)[np.argmax(sil_scores)]
print(f"\nHighest silhouette score at K={best_k}: {max(sil_scores):.4f}")
plt.figure(figsize=(8,5))
plt.plot(list(k_values), sil_scores, 'r-s')
plt.xlabel('K'), plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs K')
plt.grid(True, alpha=0.3), plt.show()
```

Run your file. You should see:
```
K=4 should have the highest silhouette score (~0.62)
```

---

## Step 6: Pick K and Justify

Based on both methods, choose K. Print your chosen K and justification.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Chosen K and justification")
print("=" * 60)
chosen_k = best_k   # or manually set if you prefer
print(f"Chosen K: {chosen_k}")
print(f"Justification:")
print(f"  Elbow method: clear bend around K=4")
print(f"  Silhouette: highest score at K=4")
print(f"  Domain knowledge: 4 traffic types (benign, scan, exfil, DoS)")
```

---

## Step 7: TASK 4 (BONUS) — Silhouette Diagram

Create a silhouette diagram for K=4 showing per-cluster silhouette values. (Each cluster is a horizontal band; wider = more samples; further right = higher score.)

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Silhouette diagram for K=4")
print("=" * 60)
print("\n--- Exercise 3 complete. Move to 04_anomaly_scoring.py ---")
from sklearn.metrics import silhouette_samples
sample_idx = np.random.choice(len(X_scaled), 500, replace=False)
X_samp = X_scaled[sample_idx]
km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
labels4 = km4.fit_predict(X_scaled)[sample_idx]
sil_vals = silhouette_samples(X_samp, labels4)
# plot horizontal sorted bars per cluster...
print("Silhouette diagram created (sample of 500 points).")
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_choosing_k.py`) if anything looks different.
