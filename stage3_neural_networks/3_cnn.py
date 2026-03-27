# Lesson 3.3 — Convolutional Neural Networks (CNNs)
#
# We use MNIST (handwritten digits) as the gateway task — it's simple
# enough to train quickly but demonstrates all CNN concepts clearly.
#
# Security connection: the same CNN approach is used to classify malware
# by converting binary files to grayscale images. The visual structure
# of different malware families is surprisingly distinctive.
#
# Prerequisite: pip install tensorflow

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

print(f"TensorFlow version: {tf.__version__}")

np.random.seed(42)
tf.random.set_seed(42)

# ── 1. Load MNIST ──────────────────────────────────────────────────────────────
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Normalise pixel values 0–255 → 0–1 and add channel dimension
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0
X_train = X_train[..., np.newaxis]   # shape: (60000, 28, 28, 1)
X_test  = X_test[..., np.newaxis]    # shape: (10000, 28, 28, 1)

print(f"Training images: {X_train.shape}")
print(f"Test images    : {X_test.shape}")
print(f"Classes        : {np.unique(y_train)}")

# ── 2. Build CNN ───────────────────────────────────────────────────────────────
model = keras.Sequential([
    # Block 1: detect low-level features (edges, corners)
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),

    # Block 2: detect higher-level patterns (curves, strokes)
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),

    # Classifier head
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(10, activation='softmax')   # 10 digit classes
], name='mnist_cnn')

model.summary()

# ── 3. Compile and train ───────────────────────────────────────────────────────
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stop = keras.callbacks.EarlyStopping(
    monitor='val_accuracy', patience=5, restore_best_weights=True
)

print("\n=== Training ===")
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# ── 4. Evaluate ───────────────────────────────────────────────────────────────
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest accuracy: {test_acc:.4f}  ({test_acc*100:.2f}%)")
print(f"Test loss    : {test_loss:.4f}")

y_pred = model.predict(X_test, verbose=0).argmax(axis=1)

# ── 5. Malware visualisation demo ─────────────────────────────────────────────
# This section shows how the SAME idea applies to malware detection.
# Real tools like Malconv treat malware binaries as 1D signals.
print("\n=== Security Connection: Malware Visualisation ===")
print("In real malware detection (e.g. VirusTotal's VGG-based classifier):")
print("  1. Convert .exe binary → grayscale image (each byte = one pixel)")
print("  2. CNN learns to recognise visual 'fingerprints' of malware families")
print("  3. Same CNN architecture, different input format")
print("  4. Packed/encrypted malware appears as high-entropy random noise")

# ── 6. Plots ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 10))

# Training history
ax1 = fig.add_subplot(2, 3, 1)
ax1.plot(history.history['accuracy'],     label='Train')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Accuracy over Epochs')
ax1.set_xlabel('Epoch')
ax1.legend()

ax2 = fig.add_subplot(2, 3, 2)
ax2.plot(history.history['loss'],     label='Train')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Loss over Epochs')
ax2.set_xlabel('Epoch')
ax2.legend()

# Sample predictions
ax3 = fig.add_subplot(2, 3, 3)
n_show = 25
indices = np.random.choice(len(X_test), n_show, replace=False)
correct = y_pred == y_test
for i, idx in enumerate(indices[:10]):
    ax_sub = fig.add_subplot(2, 5, i + 6)
    ax_sub.imshow(X_test[idx, :, :, 0], cmap='gray')
    color = 'green' if correct[idx] else 'red'
    ax_sub.set_title(f'P:{y_pred[idx]} T:{y_test[idx]}', color=color, fontsize=8)
    ax_sub.axis('off')

# Confusion for a few digits
misclassified = np.where(y_pred != y_test)[0]
print(f"\nMisclassified: {len(misclassified)} / {len(y_test)} "
      f"({len(misclassified)/len(y_test)*100:.2f}%)")

plt.suptitle(f'CNN on MNIST — Test Accuracy: {test_acc*100:.2f}%', fontsize=14)
plt.tight_layout()
plt.savefig('stage3_neural_networks/lesson3_cnn.png')
plt.show()
print("\nPlot saved to stage3_neural_networks/lesson3_cnn.png")

# ── 7. First-layer filter visualisation ───────────────────────────────────────
fig2, axes = plt.subplots(4, 8, figsize=(12, 6))
conv_weights = model.layers[0].get_weights()[0]   # shape: (3, 3, 1, 32)
for i, ax in enumerate(axes.flat):
    ax.imshow(conv_weights[:, :, 0, i], cmap='RdBu', vmin=-1, vmax=1)
    ax.axis('off')
fig2.suptitle('32 Learned Filters in Conv Layer 1\n(each detects a different low-level pattern)')
plt.tight_layout()
plt.savefig('stage3_neural_networks/lesson3_cnn_filters.png')
plt.show()
print("Filter plot saved to stage3_neural_networks/lesson3_cnn_filters.png")
