# Exercise 4 — Architecture Search

> **Exercise file:** [exercise4_architecture_search.py](exercise4_architecture_search.py)
> Read this guide fully before opening the exercise file.

---

## What You Will Learn

- How to define a search space of architectures (width × depth)
- How to run a manual grid search and store results systematically
- How to read a results table to identify winning configurations
- Why architecture search is the foundation of automated NAS (Neural Architecture Search)

---

## Concept: Architecture as a Hyperparameter

When people talk about hyperparameter tuning, they often mean learning rate and batch size. But the **architecture itself** is also a hyperparameter:

- How many hidden layers? (depth)
- How many units per layer? (width)
- What activation function?
- Should you use dropout? With what rate?

Changing these can make a bigger difference than tuning lr or batch size.

---

## Concept: The Grid Search Strategy

A **grid search** tries every combination in a defined search space:

```
units_options = [32, 64, 128]
depth_options = [1, 2, 3]

Total combinations: 3 × 3 = 9 models to train
```

For each combination:
1. Build the model
2. Train it
3. Record val_accuracy
4. Move to the next

At the end, sort by val_accuracy and pick the winner.

This is the brute-force approach. It works fine when the search space is small. For larger spaces, Bayesian optimisation (used by Keras Tuner, Optuna) is more efficient.

---

## Concept: Why Deeper Is Not Always Better

```
Depth 1 (1 hidden layer): fast, underfit risk for complex problems
Depth 2:                   usually a good balance
Depth 3:                   more capacity, but harder to train, more parameters
```

For this dataset (20 features, 2 classes, 1600 samples) depth 2 often wins. Deeper networks don't always help when the problem isn't complex enough to justify the extra capacity.

---

## Concept: Storing Results in a DataFrame

```python
import pandas as pd

results = []
results.append({"units": 64, "depth": 2, "val_acc": 0.9150, "params": 5000})

df = pd.DataFrame(results).sort_values("val_acc", ascending=False)
print(df.to_string(index=False))
```

This gives you a clean, sortable table — much better than printing raw print statements.

---

## What Each Task Asks You to Do

### Task 1 — Define the search space
Create two lists: `units_options = [32, 64, 128]` and `depth_options = [1, 2, 3]`.

### Task 2 — Run the grid search
Nested loop: for each (units, depth) combination:
- Build the model with that architecture
- Train for 20 epochs (verbose=0)
- Record units, depth, val_accuracy, and model.count_params()
- Append to a results list

### Task 3 — Print the results table
Convert results to a DataFrame, sort by val_accuracy descending, print it.

### Task 4 — Identify the winner (Bonus)
Print the best configuration: units, depth, val_accuracy.
Plot val_accuracy as a heatmap with depth on one axis and units on the other.

---

## Expected Outputs at a Glance

```
Architecture search results (sorted by val_accuracy):
 units  depth  val_acc  params
   128      2   0.9200   10625
    64      2   0.9150    4929
   128      1   0.9100    5505
    64      1   0.9050    2625
    32      2   0.8950    1633
   128      3   0.9150   26945
    64      3   0.9100   12609
    32      3   0.8900    4289
    32      1   0.8850     993

Best architecture: units=128, depth=2, val_accuracy=0.920
```

Exact values will vary between runs. What matters is identifying that depth=2 tends to outperform depth=1 (underfitting) and depth=3 (over-parameterised for this problem).

---

## Common Mistakes

**Loop takes too long**
9 models × 20 epochs should take about 2-5 minutes total on CPU. Use `verbose=0` inside the loop. If it's still too slow, reduce to `units_options = [32, 64]` and `depth_options = [1, 2]`.

**All val_accuracy values identical**
You forgot to reinitialise the model inside the loop — you're training the same model repeatedly. Make sure `build_model(units, depth)` creates a fresh Sequential model each call.

**`count_params()` returns 0**
Call `model.count_params()` after `model.compile()`, not before building the model.

---

## Workshop Complete

You have now tuned the three most important hyperparameters: learning rate, batch size, and architecture. This knowledge applies to every neural network you train from this point forward.

Open [reference_solution.py](reference_solution.py) to compare your code, then move to:

**[Module 4 — Generative AI](../../../module4_genai/lesson1_how_llms_work/workshop/1_lab_guide.md)**
