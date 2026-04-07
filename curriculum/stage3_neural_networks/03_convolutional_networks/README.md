# Lesson 3.3 — Convolutional Neural Networks (CNNs)

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

**[Lesson 3.4 — Hyperparameters](../04_hyperparameter_tuning/README.md):** Systematically tune your network for better performance.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open README.md](README.md)**

# Lesson 3.11 — Workshop Guide
## Convolutional Networks

> **Read first:** [README.md](README.md)
> **Reference solutions:** Each exercise has a matching solution file (e.g. `1_why_dense_fails_on_images/solution_convolutional_networks.py`) — open only after finishing the exercise

## What This Workshop Covers

You will start by understanding why Dense layers fail on images, then build the core components of a CNN (Conv2D + MaxPooling2D), assemble a full CNN and train it on MNIST handwritten digits, and finally explore the direct connection to cybersecurity — malware binaries rendered as greyscale images for visual classification.

This workshop uses the MNIST dataset (handwritten digits, 28×28 greyscale images). All exercises include the data loading and preprocessing code — do not modify it.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [lecture.md](1_why_dense_fails_on_images/lecture.md) | [handson.md](1_why_dense_fails_on_images/handson.md) | Dense ignores spatial relationships; pixels as flat vector |
| 2 | [lecture.md](2_conv_and_pooling/lecture.md) | [handson.md](2_conv_and_pooling/handson.md) | Conv2D filter sliding, MaxPooling2D downsampling, shape arithmetic |
| 3 | [lecture.md](3_build_and_train_cnn/lecture.md) | [handson.md](3_build_and_train_cnn/handson.md) | Full CNN on MNIST, compare accuracy to Dense baseline |
| 4 | [lecture.md](4_malware_visualisation_context/lecture.md) | [handson.md](4_malware_visualisation_context/handson.md) | Binary-to-image, malware family visual patterns, CNN relevance |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python stage3_neural_networks/03_convolutional_networks/1_why_dense_fails_on_images/solution_convolutional_networks.py
```

## Tips

- MNIST downloads automatically on first run (~11MB) and caches locally
- Training the CNN (exercise 3) may take 1-3 minutes without GPU
- Exercise 4 requires only numpy and matplotlib — no TensorFlow download needed
