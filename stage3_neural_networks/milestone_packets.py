# Stage 3 Milestone — Neural Network Packet Classifier
#
# Full neural network pipeline on KDD Cup-style network data.
# Demonstrates everything from Stage 3:
#   - Multi-layer network with dropout and batch normalisation
#   - Class weight handling for imbalanced security data
#   - Early stopping
#   - Full comparison: ML baseline vs neural network
#   - Operational deployment simulation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
from sklearn.metrics import (classification_report, roc_auc_score,
                              RocCurveDisplay, confusion_matrix, ConfusionMatrixDisplay)

import tensorflow as tf
from tensorflow import keras

print("=" * 60)
print("  STAGE 3 MILESTONE: NEURAL NETWORK PACKET CLASSIFIER")
print("=" * 60)

np.random.seed(42)
tf.random.set_seed(42)

# ── 1. Generate comprehensive network packet dataset ──────────────────────────
n_normal = 8000

def make_packets(n, attack_type='normal'):
    templates = {
        'normal': dict(
            duration=np.random.exponential(20, n).clip(0, 600),
            src_bytes=np.random.lognormal(8, 1.5, n),
            dst_bytes=np.random.lognormal(9, 1.5, n),
            land=np.zeros(n),
            wrong_fragment=np.zeros(n),
            urgent=np.zeros(n),
            hot=np.random.poisson(1, n).clip(0, 5),
            failed_logins=np.zeros(n),
            logged_in=np.random.binomial(1, 0.7, n),
            compromised=np.zeros(n),
            root_shell=np.zeros(n),
            srv_count=np.random.poisson(20, n).clip(1, 60),
            same_srv_rate=np.random.beta(8, 2, n),
            diff_srv_rate=np.random.beta(1, 9, n),
            serror_rate=np.random.beta(0.5, 15, n),
            rerror_rate=np.random.beta(0.5, 15, n),
        ),
        'dos': dict(
            duration=np.random.exponential(0.3, n).clip(0, 3),
            src_bytes=np.random.lognormal(5, 0.5, n),
            dst_bytes=np.zeros(n),
            land=np.random.binomial(1, 0.1, n),
            wrong_fragment=np.random.poisson(1, n).clip(0, 5),
            urgent=np.zeros(n),
            hot=np.zeros(n),
            failed_logins=np.zeros(n),
            logged_in=np.zeros(n),
            compromised=np.zeros(n),
            root_shell=np.zeros(n),
            srv_count=np.random.poisson(600, n).clip(200, 1000),
            same_srv_rate=np.random.beta(10, 1, n),
            diff_srv_rate=np.random.beta(0.5, 10, n),
            serror_rate=np.random.beta(9, 1, n),
            rerror_rate=np.random.beta(0.5, 10, n),
        ),
        'probe': dict(
            duration=np.random.exponential(0.5, n).clip(0, 5),
            src_bytes=np.random.lognormal(4, 0.5, n),
            dst_bytes=np.zeros(n),
            land=np.zeros(n),
            wrong_fragment=np.zeros(n),
            urgent=np.zeros(n),
            hot=np.zeros(n),
            failed_logins=np.zeros(n),
            logged_in=np.zeros(n),
            compromised=np.zeros(n),
            root_shell=np.zeros(n),
            srv_count=np.random.poisson(3, n).clip(1, 15),
            same_srv_rate=np.random.beta(1, 5, n),
            diff_srv_rate=np.random.beta(5, 3, n),
            serror_rate=np.random.beta(3, 5, n),
            rerror_rate=np.random.beta(3, 5, n),
        ),
    }
    df = pd.DataFrame(templates[attack_type])
    df['label'] = 0 if attack_type == 'normal' else 1
    return df

attack_n = {'dos': 2000, 'probe': 1000}
df = pd.concat(
    [make_packets(n_normal, 'normal')] +
    [make_packets(n, t) for t, n in attack_n.items()],
    ignore_index=True
).sample(frac=1, random_state=42)

# Feature engineering
df['bytes_ratio']      = df['src_bytes'] / (df['dst_bytes'] + 1)
df['bytes_per_sec']    = (df['src_bytes'] + df['dst_bytes']) / (df['duration'] + 0.001)
df['is_short_conn']    = (df['duration'] < 1).astype(float)
df['srv_rate_diff']    = df['same_srv_rate'] - df['diff_srv_rate']

feature_cols = [c for c in df.columns if c != 'label']
X = df[feature_cols].values.astype(np.float32)
y = df['label'].values

print(f"\nDataset: {len(df)} samples | Attack rate: {y.mean()*100:.1f}%")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 2. Baseline: Random Forest ────────────────────────────────────────────────
print("\n── Training Random Forest baseline ──")
rf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
rf.fit(X_train_s, y_train)
rf_proba = rf.predict_proba(X_test_s)[:, 1]
rf_auc = roc_auc_score(y_test, rf_proba)
print(f"Random Forest AUC: {rf_auc:.4f}")

# ── 3. Neural network ─────────────────────────────────────────────────────────
cw = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = {0: cw[0], 1: cw[1]}

model = keras.Sequential([
    keras.layers.Input(shape=(X_train_s.shape[1],)),
    keras.layers.Dense(128),
    keras.layers.BatchNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64),
    keras.layers.BatchNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid'),
], name='packet_classifier')

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model.summary()

early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=15, restore_best_weights=True
)

print("\n── Training Neural Network ──")
history = model.fit(
    X_train_s, y_train,
    epochs=150,
    batch_size=128,
    validation_split=0.15,
    class_weight=class_weights,
    callbacks=[early_stop],
    verbose=1
)

nn_proba = model.predict(X_test_s, verbose=0).flatten()
nn_pred  = (nn_proba >= 0.5).astype(int)
nn_auc   = roc_auc_score(y_test, nn_proba)

# ── 4. Final evaluation ───────────────────────────────────────────────────────
print(f"\n── Results ──")
print(f"Random Forest AUC : {rf_auc:.4f}")
print(f"Neural Network AUC: {nn_auc:.4f}  (+{nn_auc-rf_auc:.4f})")
print("\nNeural Network Classification Report:")
print(classification_report(y_test, nn_pred, target_names=['Normal', 'Attack']))

# ── 5. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Loss curves
axes[0, 0].plot(history.history['loss'],     label='Train')
axes[0, 0].plot(history.history['val_loss'], label='Val')
axes[0, 0].set_title('Training Loss')
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].legend()

# ROC curves
RocCurveDisplay.from_predictions(y_test, rf_proba,
    name=f'Random Forest (AUC={rf_auc:.3f})', ax=axes[0, 1], color='steelblue')
RocCurveDisplay.from_predictions(y_test, nn_proba,
    name=f'Neural Network (AUC={nn_auc:.3f})', ax=axes[0, 1], color='crimson')
axes[0, 1].set_title('ROC Curve Comparison')

# Confusion matrix
cm = confusion_matrix(y_test, nn_pred)
ConfusionMatrixDisplay(cm, display_labels=['Normal', 'Attack']).plot(
    ax=axes[1, 0], cmap='Blues', colorbar=False)
axes[1, 0].set_title('Neural Network Confusion Matrix')

# Probability distribution
axes[1, 1].hist(nn_proba[y_test == 0], bins=50, alpha=0.6, label='Normal', color='steelblue')
axes[1, 1].hist(nn_proba[y_test == 1], bins=50, alpha=0.8, label='Attack', color='crimson')
axes[1, 1].axvline(0.5, color='black', linestyle='--', label='Threshold (0.5)')
axes[1, 1].set_xlabel('P(Attack)')
axes[1, 1].set_title('Prediction Confidence Distribution')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('stage3_neural_networks/milestone_packets.png')
plt.show()
print("\nPlot saved to stage3_neural_networks/milestone_packets.png")
print("\n" + "=" * 60)
print("  MILESTONE COMPLETE")
print("=" * 60)
