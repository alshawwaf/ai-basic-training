# Lesson 1.1 — Workshop Guide
## Exploring Data Before You Train

> **Read first:** [../notes.md](../notes.md) — theory and concepts
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_loading_data.py`) — open only after finishing the exercise

---

## What This Workshop Covers

Before training any model, you must understand your data. This workshop walks you through the full Exploratory Data Analysis (EDA) process — the same sequence you will run at the start of every ML project.

You will build each piece yourself, step by step, across 5 focused exercises.

---

## How the Workshop Works

Each exercise has three files:

- **Guide** (`_guide_`) — explains the concept and the methods you need
- **Lab** (`_lab_`) — step-by-step instructions to build your script from scratch
- **Solution** (`_solution_`) — reference implementation to compare against when you are done

Every lab shows you the **expected output** at each step. Run your script after each task and verify your output matches before moving on.

---

## Exercise Overview

Work through them in order — each one builds on the previous.

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_loading_data.md](01_guide_loading_data.md) | [01_lab_loading_data.md](01_lab_loading_data.md) | Loading a dataset — Bunch, DataFrame, features vs labels |
| 2 | [02_guide_statistics.md](02_guide_statistics.md) | [02_lab_statistics.md](02_lab_statistics.md) | Shape and statistics — `.describe()`, missing values, zero-variance features |
| 3 | [03_guide_class_balance.md](03_guide_class_balance.md) | [03_lab_class_balance.md](03_lab_class_balance.md) | Class balance — the naive accuracy trap, imbalance ratio |
| 4 | [04_guide_visualise.md](04_guide_visualise.md) | [04_lab_visualise.md](04_lab_visualise.md) | Visualising data — image grids, average prototypes |
| 5 | [05_guide_what_model_sees.md](05_guide_what_model_sees.md) | [05_lab_what_model_sees.md](05_lab_what_model_sees.md) | What the model sees — number grids, correlations, security analogy |

**For each exercise:** read the guide first, then open the matching `_lab.md` file and follow the steps.

---

## Running a Solution

Make sure your virtual environment is active, then from the repo root:

```bash
python module1_classic_ml/lesson1_what_is_ml/workshop/01_solution_loading_data.py
```

Replace the filename with whichever exercise you are working on.

---

## Tips

**Stuck on a task?** Re-read the guide for that exercise. It explains the concept and usually names the exact method you need.

**Output doesn't match?** Check your variable names — Python is case-sensitive. Also check you haven't skipped a step.

**Finished early?** Some labs have a **BONUS** task at the end — experiment freely, no expected output given.

---

## After the Workshop

Once all 5 exercises run cleanly:

1. Compare your code against the matching `_solution_` file for each exercise
2. Review any differences and make sure you understand why

---

## Next Lesson

[Lesson 1.2 — Linear Regression](../../lesson2_linear_regression/notes.md): build your first trained model — predict server response time from network traffic load.
