# Lesson 1.4 — Decision Trees
#
# Goal: Classify network connections as benign (0) or attack (1).
# Features mimic what you'd extract from firewall/NetFlow logs.
# Decision trees are valuable in security because they're interpretable —
# you can read out the exact rules the model learned.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── 1. Generate synthetic network connection data ──────────────────────────────
np.random.seed(42)
n = 1500

# Benign connections (label = 0)
benign = pd.DataFrame({
    'duration':           np.random.exponential(30, n // 2).clip(1, 300),
    'bytes_sent':         np.random.lognormal(8, 1, n // 2).clip(100, 50000),
    'packets_sent':       np.random.poisson(50, n // 2).clip(1, 200),
    'unique_dest_ports':  np.random.poisson(2, n // 2).clip(1, 5),
    'connection_rate':    np.random.exponential(2, n // 2).clip(0.1, 10),
    'label': 0
})

# Attack connections (label = 1) — three attack types mixed together:
# Port scans: many unique ports, very short duration, low bytes
port_scan = pd.DataFrame({
    'duration':           np.random.exponential(0.5, n // 6).clip(0.01, 2),
    'bytes_sent':         np.random.normal(200, 50, n // 6).clip(50, 500),
    'packets_sent':       np.random.poisson(3, n // 6).clip(1, 10),
    'unique_dest_ports':  np.random.poisson(50, n // 6).clip(20, 200),
    'connection_rate':    np.random.normal(80, 20, n // 6).clip(30, 200),
    'label': 1
})

# Data exfil: long duration, high bytes, few ports
exfil = pd.DataFrame({
    'duration':           np.random.normal(200, 50, n // 6).clip(60, 600),
    'bytes_sent':         np.random.lognormal(12, 1, n // 6).clip(50000, 1000000),
    'packets_sent':       np.random.poisson(500, n // 6).clip(100, 2000),
    'unique_dest_ports':  np.random.poisson(1, n // 6).clip(1, 3),
    'connection_rate':    np.random.exponential(1, n // 6).clip(0.1, 5),
    'label': 1
})

# DoS: very high connection rate, short duration
dos = pd.DataFrame({
    'duration':           np.random.exponential(1, n // 6).clip(0.01, 5),
    'bytes_sent':         np.random.normal(1000, 200, n // 6).clip(200, 3000),
    'packets_sent':       np.random.poisson(20, n // 6).clip(5, 80),
    'unique_dest_ports':  np.random.poisson(1, n // 6).clip(1, 3),
    'connection_rate':    np.random.normal(500, 100, n // 6).clip(200, 1000),
    'label': 1
})

df = pd.concat([benign, port_scan, exfil, dos], ignore_index=True).sample(frac=1, random_state=42)

print("=== Dataset ===")
print(df['label'].value_counts().rename({0: 'Benign', 1: 'Attack'}))

# ── 2. Prepare and split ───────────────────────────────────────────────────────
feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Train (depth-limited to avoid overfitting) ─────────────────────────────
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=['Benign', 'Attack']))

# ── 5. Overfitting demo ───────────────────────────────────────────────────────
# An unconstrained tree perfectly memorises training data but may fail on test data
unconstrained = DecisionTreeClassifier(random_state=42)
unconstrained.fit(X_train, y_train)

print("=== Overfitting Demo ===")
print(f"Unconstrained tree — train acc: "
      f"{accuracy_score(y_train, unconstrained.predict(X_train)):.3f} | "
      f"test acc: {accuracy_score(y_test, unconstrained.predict(X_test)):.3f}")
print(f"Depth-5 tree      — train acc: "
      f"{accuracy_score(y_train, model.predict(X_train)):.3f} | "
      f"test acc: {accuracy_score(y_test, model.predict(X_test)):.3f}")
print("→ If train acc >> test acc, the model is overfitting.")

# ── 6. Feature importances ─────────────────────────────────────────────────────
imp_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=True)

print("\n=== Feature Importances ===")
print(imp_df.to_string(index=False))

# ── 7. Visualise the tree ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Left: the tree
plt.sca(axes[0])
plot_tree(model, feature_names=feature_cols, class_names=['Benign', 'Attack'],
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
