# Lesson 1.1 — Explore First, Read Later

This is the **interactive track** for "What is Machine Learning?". The
rule here is simple: **manipulate things, don't read about them**. Each
script puts a slider, button, or prompt in your hands. Play with it
until something surprises you, then move on.

You'll have answered every question Lesson 1.1 was going to ask you,
without sitting through any lecture.

## How to run

```bash
cd curriculum/stage1_classic_ml/01_what_is_ml/1_interactive_intro
python explore_00_first_look.py
```

You need a **normal terminal** (not a script runner inside an IDE) so
matplotlib can pop up an interactive window. The Jupyter step opens in
JupyterLab or VS Code:

```bash
jupyter lab explore_03_dataset_shape.ipynb
```

## The 10 explorations

| # | File | What you'll discover | Time |
|---|------|----------------------|------|
| 0 | `explore_00_first_look.py` | A random digit pops up. Can you read it? Some are easy, some aren't — that's the model's whole problem. | 3 min |
| 1 | `explore_01_draw_digit.py` | Edit an 8x8 grid of numbers in the source file, save, re-run. Pixels are just numbers. | 10 min |
| 2 | `explore_02_spot_difference.py` | Pick any two digits. The "difference map" is what a classifier actually weights. | 10 min |
| 3 | `explore_03_dataset_shape.ipynb` | Poke the `digits` Bunch object in Jupyter — `data`, `target`, `images`, `DataFrame`. | 10 min |
| 4 | `explore_04_useless_pixels.py` | A slider drops low-variance pixels. Watch the corners disappear first. | 12 min |
| 5 | `explore_05_class_balance.py` | Drag down the count of any class. Imbalance ratio explodes. | 12 min |
| 6 | `explore_06_accuracy_trap.py` | A real LogisticRegression retrains every slider tick. **Accuracy stays high while recall collapses.** | 12 min |
| 7 | `explore_07_average_digits.py` | Average all 1s, all 7s, etc. Compare any pair, then rank every pair by confusability. | 12 min |
| 8 | `explore_08_pixel_importance.py` | A correlation slider highlights the pixels that actually carry the label signal. | 12 min |
| 9 | `explore_09_model_eye_view.py` | A guessing game. You see 64 raw numbers — no image. You'll feel why models need lots of data. | 10 min |

**Total: ~100 min.** Skip in any order. Steps 0 → 1 → 2 → 3 build the
foundation; steps 4-9 can be run independently.

## Once you've finished

Open `challenge_cards.md` for the "what happens if...?" prompts. Each
one has a hidden spoiler with the answer.

When you want the formal write-up, the original lectures are in
`../2_coding_exercises/*/lecture.md`. The hands-on labs are in
`../2_coding_exercises/*/handson.md`. They cover the same material with
more text.

## What you'll be able to answer after this track

- Why is "1797 samples, 64 features" the same shape as a network log?
- Why do models care about *which* pixels differ between classes, not
  the images themselves?
- Why is dropping useless features sometimes more important than picking
  a fancier model?
- Why does class imbalance break accuracy as a metric, and what should
  you use instead?
- What does a model actually "see" when you hand it an image?

If you can answer those without looking back at the scripts, you're
ready for Lesson 1.2 (Linear Regression).
