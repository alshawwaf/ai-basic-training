# Lesson 3.3 — Convolutional Neural Networks (CNNs)

**Script:** [3_cnn.py](3_cnn.py)

---

## Concept: Networks That See

A standard Dense layer treats all inputs equally — it doesn't know that pixel (10,10) is adjacent to pixel (10,11). A **Convolutional Neural Network** exploits the *spatial structure* of data.

Instead of connecting every neuron to every input, a CNN slides a small **filter** (kernel) across the input and detects local patterns wherever they appear.

---

## How a Convolution Works

```
Input image patch:   Filter:    Output:
1 0 1               1 0 1      sum of (element-wise multiply)
0 1 0          *    0 1 0   =  1+0+1+0+1+0+1+0+1 = 5
1 0 1               1 0 1
```

The same filter slides over the *entire* image. If it detects an edge in the top-left, it will also detect the same edge in the bottom-right — this is **translation invariance**.

---

## CNN Architecture

```
Input image (28×28×1)
    ↓
Conv2D(32 filters, 3×3) + ReLU   → 32 feature maps: "what's in each region?"
    ↓
MaxPooling2D(2×2)                 → downsample: keep strongest activations
    ↓
Conv2D(64 filters, 3×3) + ReLU   → 64 higher-level feature maps
    ↓
MaxPooling2D(2×2)
    ↓
Flatten()                         → convert 2D feature maps to 1D vector
    ↓
Dense(128) + ReLU
    ↓
Dense(10) + Softmax               → class probabilities
```

---

## Security Applications of CNNs

While CNNs are known for image tasks, they're used in security for:

- **Malware visualisation** — convert binary files to grayscale images; malware families have distinct visual patterns
- **Network traffic fingerprinting** — treat packet sequences as 1D signals
- **Log analysis** — treat log sequences as temporal data
- **CAPTCHA solving** (offensive/research)

---

## Key Keras API

```python
keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))
keras.layers.MaxPooling2D((2, 2))
keras.layers.Flatten()
keras.layers.Dense(128, activation='relu')
```

---

## What to Notice When You Run It

1. The model summary — notice how many parameters are in the Conv layers vs Dense layers
2. The training accuracy — CNNs typically converge quickly on MNIST (~99%)
3. The filter visualisations — can you see what patterns each filter detects?
4. Misclassified examples — which digits does the model confuse?

---

## Next Lesson

**[Lesson 3.4 — Hyperparameters](12_hyperparameter_tuning.md):** Systematically tune your network for better performance.


---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/1_lab_guide.md](workshop/1_lab_guide.md)**
