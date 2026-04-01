import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

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

print("=" * 60)
print("TASK 1 — Feature importances (sorted)")
print("=" * 60)
importances = model.feature_importances_
imp_df = pd.DataFrame({'feature': FEATURES, 'importance': importances})
imp_df = imp_df.sort_values('importance', ascending=False)
print(imp_df.to_string(index=False))
total = importances.sum()
print(f"\nSum of importances: {total:.3f} {'✓' if abs(total-1.0)<0.001 else '✗'}")

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
