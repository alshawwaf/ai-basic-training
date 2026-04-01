# Lesson 1.4 — Decision Trees
#
# Goal: Classify network connections as benign, port_scan, exfil, or DoS.
# Features mimic what you'd extract from firewall/NetFlow logs.
# Decision trees are valuable in security because they're interpretable —
# you can read out the exact rules the model learned.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── 1. Generate synthetic network connection data ──────────────────────────────
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

print("=== Dataset ===")
print(f"Total samples: {len(df)}")
print(df['label'].value_counts().sort_index().rename(
    {0: 'benign', 1: 'port_scan', 2: 'exfil', 3: 'DoS'}))

# ── 2. Prepare and split ───────────────────────────────────────────────────────
X = df[FEATURES]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Train (depth-limited to avoid overfitting) ─────────────────────────────
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))

# ── 5. Read the rules the tree learned ───────────────────────────────────────
print("=== Decision Rules (first 30 lines) ===")
rules = export_text(model, feature_names=FEATURES)
for line in rules.split('\n')[:30]:
    print(line)

# ── 6. Overfitting demo ───────────────────────────────────────────────────────
# An unconstrained tree perfectly memorises training data but may fail on test data
unconstrained = DecisionTreeClassifier(random_state=42)
unconstrained.fit(X_train, y_train)

print("\n=== Overfitting Demo ===")
print(f"Unconstrained tree — train acc: "
      f"{accuracy_score(y_train, unconstrained.predict(X_train)):.3f} | "
      f"test acc: {accuracy_score(y_test, unconstrained.predict(X_test)):.3f}")
print(f"Depth-4 tree       — train acc: "
      f"{accuracy_score(y_train, model.predict(X_train)):.3f} | "
      f"test acc: {accuracy_score(y_test, model.predict(X_test)):.3f}")
print("→ If train acc >> test acc, the model is overfitting.")

# ── 7. Feature importances ─────────────────────────────────────────────────────
imp_df = pd.DataFrame({
    'feature': FEATURES,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=True)

print("\n=== Feature Importances ===")
print(imp_df.to_string(index=False))

# ── 8. Visualise the tree ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Left: the tree
plt.sca(axes[0])
plot_tree(model, feature_names=FEATURES, class_names=CLASS_NAMES,
          filled=True, fontsize=7, max_depth=3)
axes[0].set_title('Decision Tree (top 3 levels shown)')

# Right: feature importances bar chart
axes[1].barh(imp_df['feature'], imp_df['importance'], color='steelblue')
axes[1].set_xlabel('Importance')
axes[1].set_title('Feature Importances')

plt.tight_layout()
plt.savefig('module1_classic_ml/lesson4_decision_tree.png')
plt.show()
print("\nPlot saved to module1_classic_ml/lesson4_decision_tree.png")
