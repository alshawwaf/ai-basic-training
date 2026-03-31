# =============================================================================
# LESSON 4.1 | WORKSHOP | Exercise 3 of 3
# Attention: Which Words Matter to Which
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - What the attention mechanism does: every word looks at every other word
# - How attention weights are computed and interpreted
# - How a context vector blends information from across the sequence
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson1_how_llms_work/workshop/exercise3_attention.py
# =============================================================================

import numpy as np

# The 5-word sentence we will analyse
sentence = ["the", "firewall", "blocked", "malicious", "connection"]
n = len(sentence)

# =============================================================================
# BACKGROUND
# =============================================================================
# Attention lets every token look at every other token in the sequence.
# The attention weight A[i][j] = "how much does position i attend to position j?"
#
# Each row of the attention matrix is a probability distribution (sums to 1).
# This is the output of softmax applied to raw Q·K^T / sqrt(d_k) scores.
#
# In a real transformer: A = softmax(Q @ K.T / sqrt(d_k))
# Here we provide the final weights directly so you can focus on interpretation.

# =============================================================================
# TASK 1 — Build the attention matrix
# =============================================================================
# Create a 5×5 NumPy array called `attention` using these pre-computed weights:
#
#   Row 0 (the):        [0.80, 0.10, 0.05, 0.03, 0.02]
#   Row 1 (firewall):   [0.15, 0.65, 0.10, 0.05, 0.05]
#   Row 2 (blocked):    [0.03, 0.45, 0.00, 0.28, 0.24]
#   Row 3 (malicious):  [0.02, 0.08, 0.12, 0.70, 0.08]
#   Row 4 (connection): [0.04, 0.12, 0.30, 0.25, 0.29]
#
# Verify each row sums to 1.0. Print:
#   "Row sums: [1. 1. 1. 1. 1.]"
#
# EXPECTED OUTPUT:
#   Attention matrix shape: (5, 5)
#   Row sums: [1. 1. 1. 1. 1.]

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Interpret attention: what does each word attend to most?
# =============================================================================
# For each word in `sentence`:
#   - Find the index j of the maximum value in attention[i]
#   - Print: '"word_i" → attends most to: "word_j" (score)'
#
# Hint: np.argmax(attention[i]) gives the index of the max value in row i.
#
# EXPECTED OUTPUT:
#   Attention — what each word attends to most:
#     "the"        → attends most to: "the"        (0.80)
#     "firewall"   → attends most to: "firewall"   (0.65)
#     "blocked"    → attends most to: "firewall"   (0.45)
#     "malicious"  → attends most to: "malicious"  (0.70)
#     "connection" → attends most to: "blocked"    (0.30)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Compute a context vector for "blocked"
# =============================================================================
# The attention output for each position is a weighted sum of VALUE vectors.
# Value vectors (one per word, embedding_dim=5):

values = np.array([
    [ 0.10, -0.20,  0.05,  0.10,  0.05],  # the
    [ 0.70,  0.60, -0.30,  0.20,  0.10],  # firewall
    [ 0.50,  0.40, -0.10,  0.30,  0.20],  # blocked
    [ 0.90,  0.75, -0.50,  0.80,  0.40],  # malicious
    [ 0.65,  0.55, -0.25,  0.60,  0.30],  # connection
])

# Compute the context vector for word index 2 ("blocked"):
#   context = attention[2] @ values
#   (this is equivalent to: sum over j of attention[2][j] * values[j])
#
# Print:
#   Context vector for "blocked": [x.xxx ...]
#   Top 2 contributors by attention weight: firewall (0.45), malicious (0.28)
#
# EXPECTED OUTPUT (approximate):
#   Context vector for "blocked": [ 0.604  0.519 -0.234  0.481  0.235]
#   Top contributors: firewall (0.45), malicious (0.28)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Print the attention matrix as a formatted grid (BONUS)
# =============================================================================
# Print the 5×5 attention matrix with abbreviated word labels on rows and columns.
# Format each value to 2 decimal places.
# Short labels (5 chars): "the  ", "firwl", "blckd", "malcs", "cnnct"
#
# Example format:
#            the   firwl blckd malcs cnnct
#   the    [ 0.80  0.10  0.05  0.03  0.02 ]
#   firwl  [ 0.15  0.65  0.10  0.05  0.05 ]
#   blckd  [ 0.03  0.45  0.00  0.28  0.24 ]
#   malcs  [ 0.02  0.08  0.12  0.70  0.08 ]
#   cnnct  [ 0.04  0.12  0.30  0.25  0.29 ]

# >>> YOUR CODE HERE


print("\n--- Exercise 3 complete. Open reference_solution.py to compare. ---")
print("--- Next: module4_genai/lesson2_huggingface/workshop/1_lab_guide.md ---")
