# Lesson 1.1 — What Is Machine Learning?

**Learn by doing, not reading.** Run each step below, manipulate the controls, and discover the concepts yourself. Theory comes after.

| # | Run this | What you'll discover | Time |
|---|----------|---------------------|------|
| 0 | `python explore_00_first_look.py` | What ML data looks like | 3 min |
| 1 | `python explore_01_draw_digit.py` | Pixels are just numbers you can edit | 10 min |
| 2 | `python explore_02_spot_difference.py` | Models see differences, not images | 10 min |
| 3 | `jupyter notebook explore_03_dataset_shape.ipynb` | Dataset dimensions and structure | 10 min |
| 4 | `python explore_04_useless_pixels.py` | Some features carry zero information | 12 min |
| 5 | `python explore_05_class_balance.py` | Class imbalance distorts everything | 12 min |
| 6 | `python explore_06_accuracy_trap.py` | Accuracy lies — recall tells the truth | 12 min |
| 7 | `python explore_07_average_digits.py` | Prototypes reveal model confusion | 12 min |
| 8 | `python explore_08_pixel_importance.py` | Not all features are created equal | 12 min |
| 9 | `python explore_09_model_eye_view.py` | A model never sees images — just numbers | 10 min |

**Total: ~100 minutes**

## How to use this

1. Open a terminal in this folder
2. Run each script in order (0 → 9)
3. Read the printed message after closing each window — it connects to security
4. Check [challenge_cards.md](challenge_cards.md) for "What happens if...?" prompts

## Requirements

```
pip install numpy matplotlib scikit-learn pandas jupyter
```

## After you finish

The explore scripts give you intuition. The existing exercise folders give you practice writing code:

- [1_loading_data/](1_loading_data/) — Load and inspect the dataset yourself
- [2_statistics/](2_statistics/) — Compute summary statistics with pandas
- [3_class_balance/](3_class_balance/) — Detect and measure imbalance
- [4_visualise/](4_visualise/) — Plot digits and prototypes with matplotlib
- [5_what_model_sees/](5_what_model_sees/) — Work with flat arrays and correlations
