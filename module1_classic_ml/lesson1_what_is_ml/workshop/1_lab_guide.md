# Lesson 1.1 — Workshop Guide
## Exploring Data Before You Train

> **Read first:** [../1_what_is_ml.md](../1_what_is_ml.md) — theory and concepts
> **Reference solution:** [reference_solution.py](reference_solution.py) — open only after finishing all exercises

---

## What This Workshop Covers

Before training any model, you must understand your data. This workshop walks you through the full Exploratory Data Analysis (EDA) process — the same sequence you will run at the start of every ML project.

You will build each piece yourself, step by step, across 5 focused exercises.

---

## How the Workshop Works

Each exercise file is self-contained — it loads the data for you and gives you a set of tasks to complete. Your job is to fill in the `# >>> YOUR CODE HERE` blocks.

Every task shows you the **expected output** in a comment. Run the file after each task and verify your output matches before moving on.

When you are done, open [reference_solution.py](reference_solution.py) to compare your code.

---

## Exercise Overview

Work through them in order — each one builds on the previous.

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_loading_data.md](exercise1_loading_data.md) | [exercise1_loading_data_lab.md](exercise1_loading_data_lab.md) | Loading a dataset — Bunch, DataFrame, features vs labels |
| 2 | [exercise2_statistics.md](exercise2_statistics.md) | [exercise2_statistics_lab.md](exercise2_statistics_lab.md) | Shape and statistics — `.describe()`, missing values, zero-variance features |
| 3 | [exercise3_class_balance.md](exercise3_class_balance.md) | [exercise3_class_balance_lab.md](exercise3_class_balance_lab.md) | Class balance — the naive accuracy trap, imbalance ratio |
| 4 | [exercise4_visualise.md](exercise4_visualise.md) | [exercise4_visualise_lab.md](exercise4_visualise_lab.md) | Visualising data — image grids, average prototypes |
| 5 | [exercise5_what_model_sees.md](exercise5_what_model_sees.md) | [exercise5_what_model_sees_lab.md](exercise5_what_model_sees_lab.md) | What the model sees — number grids, correlations, security analogy |

**For each exercise:** read the `.md` guide first, then open the `.py` file and fill in the tasks.

---

## Running an Exercise

Make sure your virtual environment is active, then from the repo root:

```bash
python module1_classic_ml/lesson1_what_is_ml/workshop/exercise1_loading_data.py
```

Replace `exercise1_loading_data` with whichever exercise you are working on.

---

## Tips

**Stuck on a task?** Re-read the background section at the top of the exercise file. The explanation usually contains the method name you need.

**Output doesn't match?** Check your variable names — Python is case-sensitive. Also check you haven't skipped a line.

**Finished early?** Each exercise has a **BONUS** task at the bottom — experiment freely, no expected output given.

---

## After the Workshop

Once all 5 exercises run cleanly:

1. Open [reference_solution.py](reference_solution.py) and compare it to your code
2. The reference has more inline comments explaining *why* — read those
3. Try the extended exercises in the `EXERCISES` section at the bottom of the reference

---

## Next Lesson

[Lesson 1.2 — Linear Regression](../../lesson2_linear_regression/2_linear_regression.md): build your first trained model — predict server response time from network traffic load.
