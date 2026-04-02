import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

np.random.seed(42)
n_per_class = 500

# Generate synthetic network traffic with distinct statistical profiles per attack type
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
# Hold out 20% for testing; stratify keeps class proportions equal in both splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("=" * 60)
print("TASK 1 — Depth sweep (max_depth 1 to 15)")
print("=" * 60)
# Train a separate tree at each depth from 1 to 15 and record both accuracies
# The gap between train and test accuracy reveals overfitting
depths = range(1, 16)
train_accs, test_accs = [], []
print(f"{'Depth':>5} | {'Train Acc':>9} | {'Test Acc':>8} | {'Gap':>6}")
print("-" * 40)
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42)
    m.fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    te = m.score(X_test,  y_test)
    train_accs.append(tr)
    test_accs.append(te)
    print(f"{d:>5} | {tr:>9.3f} | {te:>8.3f} | {tr-te:>6.3f}")

print("\n" + "=" * 60)
print("TASK 2 — Find the optimal depth")
print("=" * 60)
# Pick the depth that gives the highest test accuracy (best generalisation)
best_test_depth = depths[np.argmax(test_accs)]
best_test_acc   = max(test_accs)
print(f"Best test accuracy: {best_test_acc:.3f} at depth={best_test_depth}")
print(f"Recommended max_depth: {best_test_depth}")

print("\n" + "=" * 60)
print("TASK 3 — Train vs test accuracy plot")
print("=" * 60)
print("Depth sweep plot created.")
# Plot train vs test accuracy -- look for where the curves diverge (overfitting begins)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(list(depths), train_accs, 'b-o', label='Training accuracy', markersize=4)
ax.plot(list(depths), test_accs,  'r--o', label='Test accuracy', markersize=4)
# Mark the optimal depth with a vertical line
ax.axvline(x=best_test_depth, color='green', linestyle=':', label=f'Sweet spot (depth={best_test_depth})')
ax.set_xlabel('max_depth')
ax.set_ylabel('Accuracy')
ax.set_title('Decision Tree: Depth vs Accuracy (Overfitting Diagnostic)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("TASK 4 (BONUS) — Underfit vs good fit vs overfit")
print("=" * 60)
# Compare three regimes: too shallow (underfit), just right, too deep (overfit)
# classification_report shows precision/recall/f1 per class -- watch for drops at depth=15
for depth, label in [(1, "Underfit"), (5, "Good fit"), (15, "Overfit")]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    print(f"\n--- depth={depth} ({label}) ---")
    print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))
