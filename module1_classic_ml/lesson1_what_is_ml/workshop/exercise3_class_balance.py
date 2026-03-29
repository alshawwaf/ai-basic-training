# =============================================================================
# LESSON 1.1 | WORKSHOP | Exercise 3 of 5
# Class Balance — The Silent Model Killer
# =============================================================================
#
# WHAT YOU WILL LEARN
# -------------------
# - What class imbalance is and why it matters
# - How to measure it with value_counts()
# - Why a "95% accurate" model can be completely useless in security
# - How to calculate the naive accuracy baseline (always predict majority class)
#
# RUN THIS FILE
# -------------
#   python module1_classic_ml/lesson1_what_is_ml/workshop/exercise3_class_balance.py
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.datasets import load_digits

# Setup
digits = load_digits()
df = pd.DataFrame(digits.data, columns=[f"pixel_{i}" for i in range(64)])
df["target"] = digits.target


# =============================================================================
# BACKGROUND
# =============================================================================
#
# Imagine you are training an intrusion detection model.
# Your dataset has:
#   950,000 normal connections
#    50,000 malicious connections (5% of all data)
#
# A model that ALWAYS predicts "normal" — without ever learning anything —
# will score 95% accuracy on this dataset.
#
# But it catches ZERO attacks. 100% miss rate. Completely useless.
#
# This is the class imbalance trap. It is the single most common mistake
# in security ML, and it will be present in nearly every real dataset you use.
#
# Metrics like precision, recall, and F1-score exist specifically to expose
# this problem. You will learn them in Lesson 1.5. For now, learn to spot it.


# =============================================================================
# TASK 1 — Count samples per class
# =============================================================================
#
# Use df["target"].value_counts().sort_index() to count how many samples
# exist for each digit class (0-9). Print the result.

# >>> YOUR CODE HERE


# EXPECTED OUTPUT:
# Samples per class:
# 0    178
# 1    182
# 2    177
# 3    183
# 4    181
# 5    182
# 6    181
# 7    179
# 8    174
# 9    180
# Name: target, dtype: int64
#
# This dataset is well balanced. Real security datasets almost never are.


# =============================================================================
# TASK 2 — Calculate the imbalance ratio
# =============================================================================
#
# Imbalance ratio = (count of majority class) / (count of minority class)
# A ratio above 10:1 is considered heavily imbalanced in most domains.
# In security, ratios of 1000:1 are common.
#
# Get the max and min class counts, calculate the ratio, and print it.

# >>> YOUR CODE HERE
# counts = df["target"].value_counts()
# ratio  = counts.max() / counts.min()
# ...


# EXPECTED OUTPUT:
# Majority class: 183 samples
# Minority class: 174 samples
# Imbalance ratio: 1.05 : 1
# This dataset is well balanced.
#
# CONTRAST — typical security scenario:
# Imbalance ratio: 19.0 : 1  (95% vs 5%)
# A naive model predicting "normal" always would score: 95.0% accuracy


# =============================================================================
# TASK 3 — Simulate the imbalanced security scenario
# =============================================================================
#
# Let's make the lesson concrete. Create a fake imbalanced dataset and
# calculate what a "predict majority always" model would score.
#
# Simulate: 950 normal + 50 attack = 1000 total connections

normal_count = 950
attack_count = 50
total = normal_count + attack_count

# >>> YOUR CODE HERE
# Calculate:
#   naive_accuracy  = what % a model achieves by always predicting "normal"
#   attack_recall   = what % of attacks such a model would actually catch
# Print both, formatted as percentages.


# EXPECTED OUTPUT:
# --- Simulated Security Dataset ---
# Normal connections : 950 (95.0%)
# Attack connections :  50  (5.0%)
#
# A naive model (always predicts 'normal'):
#   Accuracy       : 95.0%   <- looks great!
#   Attacks caught :  0.0%   <- completely useless
#
# This is why accuracy alone is a dangerous metric in security.


# =============================================================================
# TASK 4 — Visualise the balance (text bar chart)
# =============================================================================
#
# Print a simple ASCII bar chart showing samples per class.
# Each '#' represents 1 sample (or scale it to fit nicely).

# >>> YOUR CODE HERE
# Loop over each class 0-9, print class label + bar of '#' characters
# Use df["target"].value_counts().sort_index() for the counts


# EXPECTED OUTPUT (approximate):
# Class distribution:
# 0 | ########################################################## (178)
# 1 | ########################################################## (182)
# ...
# 9 | ########################################################## (180)


# =============================================================================
# DONE
# =============================================================================
print("\n--- Exercise 3 complete. Move to exercise4_visualise.py ---")
