# Lab -- Exercise 2: K-Means and Visualisation

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `02_kmeans_and_visualisation.py` in this folder.

---

## Step 2: Add the imports

Copy this to the top of your file:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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
        'failed_connections': np.random.poisson(0.5,n_per), 'true_label':0,'true_class':'benign'})
    port_scan = pd.DataFrame({'connection_rate': np.random.normal(25,8,n_per).clip(5,60),
        'bytes_sent': np.random.normal(500,200,n_per).clip(50,2000),
        'bytes_received': np.random.normal(300,100,n_per).clip(0,1000),
        'unique_dest_ports': np.random.normal(45,10,n_per).clip(20,100).astype(int),
        'duration_seconds': np.random.normal(5,2,n_per).clip(1,20),
        'failed_connections': np.random.poisson(8,n_per), 'true_label':1,'true_class':'port_scan'})
    exfil = pd.DataFrame({'connection_rate': np.random.normal(8,2,n_per).clip(1,20),
        'bytes_sent': np.random.normal(80000,25000,n_per).clip(20000,250000),
        'bytes_received': np.random.normal(1000,300,n_per).clip(100,5000),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(180,60,n_per).clip(60,600),
        'failed_connections': np.random.poisson(0.2,n_per), 'true_label':2,'true_class':'exfil'})
    dos = pd.DataFrame({'connection_rate': np.random.normal(200,40,n_per).clip(80,500),
        'bytes_sent': np.random.normal(200,80,n_per).clip(40,600),
        'bytes_received': np.random.normal(100,40,n_per).clip(0,400),
        'unique_dest_ports': np.random.poisson(2,n_per).clip(1,5),
        'duration_seconds': np.random.normal(0.5,0.2,n_per).clip(0.1,2),
        'failed_connections': np.random.poisson(3,n_per), 'true_label':3,'true_class':'DoS'})
    return pd.concat([benign,port_scan,exfil,dos],ignore_index=True).sample(frac=1,random_state=42)
df_full = make_full_dataset()
FEATURES = ['connection_rate','bytes_sent','bytes_received',
            'unique_dest_ports','duration_seconds','failed_connections']
X = df_full[FEATURES]
true_labels  = df_full['true_label'].values
true_classes = df_full['true_class'].values
```

---

## Step 4: Scale and Fit K-Means (k=4)

Scale X with StandardScaler. Fit KMeans(n_clusters=4, random_state=42, n_init=10). Print cluster sizes. Compare to expected ~750 per cluster.

Add this to your file:

```python
print("=" * 60)
print("TASK 1 — K-Means clustering (k=4)")
print("=" * 60)
scaler  = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans  = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)
unique, counts = np.unique(cluster_labels, return_counts=True)
print("Cluster sizes:")
for c, n in zip(unique, counts):
    print(f"  Cluster {c}: {n} samples")
```

Run your file. You should see:
```
Cluster sizes: roughly equal (750 each)
```

---

## Step 5: PCA to 2D and Plot Clusters

Fit PCA(n_components=2) on X_scaled. Transform to X_2d. Plot scatter coloured by cluster_labels. Mark centroids with 'X'. Print explained variance ratio.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 2 — PCA visualisation of clusters")
print("=" * 60)
print("Cluster scatter plot created.")
pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X_scaled)
print(f"PCA explained variance: {pca.explained_variance_ratio_}")
colours = ['steelblue','red','green','orange']
plt.figure(figsize=(9,7))
for c in range(4):
    mask = cluster_labels == c
    plt.scatter(X_2d[mask,0], X_2d[mask,1], alpha=0.2, s=8, color=colours[c], label=f'Cluster {c}')
centroids_2d = pca.transform(kmeans.cluster_centers_)
plt.scatter(centroids_2d[:,0], centroids_2d[:,1], c='black', marker='X', s=150, zorder=10, label='Centroids')
plt.xlabel('PC1'), plt.ylabel('PC2')
plt.title('K-Means Clusters in PCA Space')
plt.legend(), plt.show()
```

---

## Step 6: Reveal True Labels

Plot the same PCA 2D scatter, but colour by true_classes. Compare to Task 2. How well do K-Means clusters align with true classes?

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 3 — Reveal true labels for comparison")
print("=" * 60)
print("True label scatter created.")
class_colours = {'benign':'steelblue','port_scan':'orange','exfil':'green','DoS':'red'}
plt.figure(figsize=(9,7))
for cls in ['benign','port_scan','exfil','DoS']:
    mask = true_classes == cls
    plt.scatter(X_2d[mask,0], X_2d[mask,1], alpha=0.2, s=8,
                color=class_colours[cls], label=cls)
plt.xlabel('PC1'), plt.ylabel('PC2')
plt.title('True Class Labels in PCA Space')
plt.legend(), plt.show()
```

---

## Step 7: TASK 4 (BONUS) — Cluster Purity

For each cluster (0-3), print how many samples of each true_class it contains. Compute purity = majority_class_count / cluster_size.

Add this to your file:

```python
print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Cluster purity analysis")
print("=" * 60)
print(f"{'Cluster':>7} | {'Dominant class':>14} | {'Purity':>7} | {'Size':>5}")
print("-" * 45)
for c in range(4):
    mask = cluster_labels == c
    classes_in_cluster = true_classes[mask]
    dominant = pd.Series(classes_in_cluster).value_counts().idxmax()
    count    = pd.Series(classes_in_cluster).value_counts().max()
    total    = mask.sum()
    purity   = count / total
    print(f"{c:>7} | {dominant:>14} | {purity:>7.1%} | {total:>5}")
```

Run your file. You should see:
```
Cluster | Dominant class | Purity |  Size
Cluster 0 → benign    ~91%
Cluster 1 → DoS       ~95%
Cluster 2 → exfil     ~89%
Cluster 3 → port_scan ~87%
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_kmeans_and_visualisation.py`) if anything looks different.
