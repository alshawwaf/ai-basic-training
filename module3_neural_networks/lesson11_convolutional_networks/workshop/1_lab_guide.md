# Lesson 3.11 — Workshop Guide
## Convolutional Networks

> **Read first:** [../11_convolutional_networks.md](../11_convolutional_networks.md)
> **Reference solution:** [reference_solution.py](reference_solution.py)

## What This Workshop Covers

You will start by understanding why Dense layers fail on images, then build the core components of a CNN (Conv2D + MaxPooling2D), assemble a full CNN and train it on MNIST handwritten digits, and finally explore the direct connection to cybersecurity — malware binaries rendered as greyscale images for visual classification.

This workshop uses the MNIST dataset (handwritten digits, 28×28 greyscale images). All exercises include the data loading and preprocessing code — do not modify it.

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_why_dense_fails_on_images.md](exercise1_why_dense_fails_on_images.md) | [exercise1_why_dense_fails_on_images.py](exercise1_why_dense_fails_on_images.py) | Dense ignores spatial relationships; pixels as flat vector |
| 2 | [exercise2_conv_and_pooling.md](exercise2_conv_and_pooling.md) | [exercise2_conv_and_pooling.py](exercise2_conv_and_pooling.py) | Conv2D filter sliding, MaxPooling2D downsampling, shape arithmetic |
| 3 | [exercise3_build_and_train_cnn.md](exercise3_build_and_train_cnn.md) | [exercise3_build_and_train_cnn.py](exercise3_build_and_train_cnn.py) | Full CNN on MNIST, compare accuracy to Dense baseline |
| 4 | [exercise4_malware_visualisation_context.md](exercise4_malware_visualisation_context.md) | [exercise4_malware_visualisation_context.py](exercise4_malware_visualisation_context.py) | Binary-to-image, malware family visual patterns, CNN relevance |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson11_convolutional_networks/workshop/exercise1_why_dense_fails_on_images.py
```

## Tips

- MNIST downloads automatically on first run (~11MB) and caches locally
- Training the CNN (exercise 3) may take 1-3 minutes without GPU
- Exercise 4 requires only numpy and matplotlib — no TensorFlow download needed

## After This Workshop

Move to [Lesson 3.12 — Hyperparameter Tuning](../../lesson12_hyperparameter_tuning/workshop/1_lab_guide.md)
