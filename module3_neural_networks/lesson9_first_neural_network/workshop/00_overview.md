# Lesson 3.9 — Workshop Guide
## Your First Neural Network in Keras

> **Read first:** [../notes.md](../notes.md)
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_from_numpy_to_keras.py`) — open only after finishing the exercise

## What This Workshop Covers

You will bridge the gap between the NumPy foundations you built by hand and a full Keras neural network. Starting from how a `Dense` layer maps directly to matrix multiplication, you will build, compile, and train a neural network on a binary classification problem, evaluate it properly, and compare it to a logistic regression baseline. By the end you will know exactly what each Keras API call is doing and why.

This workshop uses a synthetic binary classification dataset with class imbalance (90/10 split) — deliberately chosen to mirror the conditions you encounter in real network security data.

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_from_numpy_to_keras.md](01_guide_from_numpy_to_keras.md) | [01_lab_from_numpy_to_keras.md](01_lab_from_numpy_to_keras.md) | Dense layer = matrix multiply + bias + activation |
| 2 | [02_guide_build_the_network.md](02_guide_build_the_network.md) | [02_lab_build_the_network.md](02_lab_build_the_network.md) | Choose layers, activations, output shape |
| 3 | [03_guide_compile_and_train.md](03_guide_compile_and_train.md) | [03_lab_compile_and_train.md](03_lab_compile_and_train.md) | model.fit(), history object, training curves |
| 4 | [04_guide_evaluate_and_improve.md](04_guide_evaluate_and_improve.md) | [04_lab_evaluate_and_improve.md](04_lab_evaluate_and_improve.md) | model.evaluate(), classification report, LR baseline |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module3_neural_networks/lesson9_first_neural_network/workshop/01_solution_from_numpy_to_keras.py
```

## Tips

- If TensorFlow is not installed: `pip install tensorflow`
- The first import of TensorFlow/Keras takes 5-10 seconds — this is normal
- Keras prints verbose GPU/CPU info at startup — you can safely ignore it
- Random weight initialisation means your exact accuracy numbers may differ by ±2%

## After This Workshop

Move to [Lesson 3.10 — Dropout and Regularisation](../../lesson10_dropout_regularisation/workshop/00_overview.md)
