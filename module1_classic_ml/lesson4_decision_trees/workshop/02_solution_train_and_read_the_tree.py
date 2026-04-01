import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
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

print("=" * 60)
print("TASK 1 — Train the decision tree")
print("=" * 60)
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)
train_acc = model.score(X_train, y_train)
test_acc  = model.score(X_test,  y_test)
print(f"Training accuracy: {train_acc:.3f}")
print(f"Test accuracy:     {test_acc:.3f}")

print("\n" + "=" * 60)
print("TASK 2 — Tree rules (first 40 lines)")
print("=" * 60)
rules = export_text(model, feature_names=FEATURES)
lines = rules.split('\n')
for line in lines[:40]:
    print(line)
# The root is the first line that contains '<='
root_line = [l for l in lines if '<=' in l][0].strip()
print(f"\nRoot split: {root_line}")

print("\n" + "=" * 60)
print("TASK 3 — Tree visualisation")
print("=" * 60)
print("Tree visualisation created.")
plt.figure(figsize=(20, 10))
plot_tree(model,
          feature_names=FEATURES,
          class_names=CLASS_NAMES,
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Decision Tree: Network Traffic Classifier (max_depth=4)")
plt.tight_layout()
plt.show()
# a) Root splits on connection_rate: DoS has very high rate, others are lower
# b) Left subtree (low rate): separates benign, port_scan, exfil by bytes_sent and ports

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Trace a sample through the tree")
print("=" * 60)
sample = X_test.iloc[[0]]
print("Sample features:")
print(sample.to_string())
pred_class = model.predict(sample)[0]
pred_proba = model.predict_proba(sample)[0]
print(f"\nPredicted class: {CLASS_NAMES[pred_class]} ({pred_class})")
print("Class probabilities:")
for name, p in zip(CLASS_NAMES, pred_proba):
    print(f"  {name:10s}: {p:.3f}")
