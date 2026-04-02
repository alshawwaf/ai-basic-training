# Lesson 3.11 — Workshop Guide
## Convolutional Networks

> **Read first:** [../notes.md](../notes.md)
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_why_dense_fails_on_images.py`) — open only after finishing the exercise

## What This Workshop Covers

You will start by understanding why Dense layers fail on images, then build the core components of a CNN (Conv2D + MaxPooling2D), assemble a full CNN and train it on MNIST handwritten digits, and finally explore the direct connection to cybersecurity — malware binaries rendered as greyscale images for visual classification.

This workshop uses the MNIST dataset (handwritten digits, 28×28 greyscale images). All exercises include the data loading and preprocessing code — do not modify it.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_why_dense_fails_on_images.md](01_guide_why_dense_fails_on_images.md) | [01_lab_why_dense_fails_on_images.md](01_lab_why_dense_fails_on_images.md) | Dense ignores spatial relationships; pixels as flat vector |
| 2 | [02_guide_conv_and_pooling.md](02_guide_conv_and_pooling.md) | [02_lab_conv_and_pooling.md](02_lab_conv_and_pooling.md) | Conv2D filter sliding, MaxPooling2D downsampling, shape arithmetic |
| 3 | [03_guide_build_and_train_cnn.md](03_guide_build_and_train_cnn.md) | [03_lab_build_and_train_cnn.md](03_lab_build_and_train_cnn.md) | Full CNN on MNIST, compare accuracy to Dense baseline |
| 4 | [04_guide_malware_visualisation_context.md](04_guide_malware_visualisation_context.md) | [04_lab_malware_visualisation_context.md](04_lab_malware_visualisation_context.md) | Binary-to-image, malware family visual patterns, CNN relevance |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson11_convolutional_networks/workshop/01_solution_why_dense_fails_on_images.py
```

## Tips

- MNIST downloads automatically on first run (~11MB) and caches locally
- Training the CNN (exercise 3) may take 1-3 minutes without GPU
- Exercise 4 requires only numpy and matplotlib — no TensorFlow download needed

## After This Workshop

Move to [Lesson 3.12 — Hyperparameter Tuning](../../lesson12_hyperparameter_tuning/workshop/00_overview.md)
