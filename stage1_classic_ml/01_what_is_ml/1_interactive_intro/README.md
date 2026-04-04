# Lesson 1.1 — Interactive Introduction

**Learn by doing, not reading.** This is a web app with 10 interactive steps. Manipulate sliders, draw digits, train models, and discover ML concepts yourself.

## How to run

```bash
cd stage1_classic_ml/01_what_is_ml/1_interactive_intro
python app.py
```

Then open **http://localhost:5000** in your browser.

## What you'll explore

| Step | Title | What you'll discover |
|------|-------|---------------------|
| 0 | First Look | What ML data looks like |
| 1 | Draw a Digit | Pixels are just numbers you can edit |
| 2 | Spot the Difference | Models see differences, not images |
| 3 | Dataset Shape | 1,797 samples x 64 features |
| 4 | Useless Pixels | Some features carry zero information |
| 5 | Class Balance | Class imbalance distorts everything |
| 6 | Accuracy Trap | Accuracy lies — recall tells the truth |
| 7 | Average Digits | Prototypes reveal model confusion |
| 8 | Pixel Importance | Not all features are created equal |
| 9 | Model's Eye View | A model never sees images — just numbers |

**Total: ~100 minutes**

## Requirements

```
pip install flask numpy scikit-learn pandas
```

## After you finish

The interactive steps give you intuition. The coding exercises give you practice writing code:

- [1_loading_data/](../2_coding_exercises/1_loading_data/) — Load and inspect the dataset yourself
- [2_statistics/](../2_coding_exercises/2_statistics/) — Compute summary statistics with pandas
- [3_class_balance/](../2_coding_exercises/3_class_balance/) — Detect and measure imbalance
- [4_visualise/](../2_coding_exercises/4_visualise/) — Plot digits and prototypes with matplotlib
- [5_what_model_sees/](../2_coding_exercises/5_what_model_sees/) — Work with flat arrays and correlations
