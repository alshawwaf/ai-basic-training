# Exercise 3 — Attention: Which Words Matter to Which
#
# Demonstrates the attention mechanism — the core innovation that makes
# transformers powerful. We use a toy 5-word sentence to show how each
# word "attends to" every other word with learned weights.
#
# pip install numpy

import numpy as np

# ============================================================
#   TASK 1: Build a toy attention matrix
# ============================================================
print("=" * 60)
print("  TASK 1: Build a Toy Attention Matrix")
print("=" * 60)

# Our 5-word sentence
sentence = ["the", "firewall", "blocked", "malicious", "connection"]

# Attention weight matrix (5x5)
# Entry [i][j] = how much word i attends to word j.
# Each row sums to 1.0 (output of softmax).
# These values are hand-crafted to illustrate realistic attention patterns:
#   - "blocked" attends strongly to "firewall" (the subject doing the blocking)
#     and "malicious" (the modifier of what was blocked)
#   - "connection" attends to "blocked" and "malicious" (its context)
attention = np.array([
    [0.80, 0.10, 0.05, 0.03, 0.02],   # "the" — mostly self-attends (function word)
    [0.15, 0.65, 0.10, 0.05, 0.05],   # "firewall" — mostly self-attends
    [0.03, 0.45, 0.00, 0.28, 0.24],   # "blocked" — attends to firewall + malicious
    [0.02, 0.08, 0.12, 0.70, 0.08],   # "malicious" — mostly self-attends
    [0.04, 0.12, 0.30, 0.25, 0.29],   # "connection" — attends to blocked + malicious
])

# Verify each row sums to 1.0 (softmax constraint)
print(f"\nSentence: {sentence}")
print(f"Attention matrix shape: {attention.shape}")
print("\nRow sums (should all be 1.0):")
for i, word in enumerate(sentence):
    row_sum = attention[i].sum()
    print(f"  {word:<12} row sum = {row_sum:.2f}")


# ============================================================
#   TASK 2: Interpret attention — what does each word attend to?
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Interpret Attention Weights")
print("=" * 60)

print("\nAttention -- what each word attends to most:")
for i, word in enumerate(sentence):
    # Find the index of the highest attention weight in this row
    max_j = int(np.argmax(attention[i]))
    max_weight = attention[i][max_j]
    target = sentence[max_j]
    print(f'  "{word:<12}" -> attends most to: "{target:<12}" ({max_weight:.2f})')

# Also show the full attention distribution for "blocked" (the most interesting row)
print(f'\nFull attention distribution for "blocked":')
for j, target_word in enumerate(sentence):
    weight = attention[2][j]
    bar = "#" * int(weight * 40)
    print(f"  -> {target_word:<12} {weight:.2f} {bar}")


# ============================================================
#   TASK 3: Compute a weighted context vector
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Weighted Context Vector")
print("=" * 60)

# Value vectors for each word (5 words x 5 dims)
# In a real transformer, these are computed as V = embedding @ W_V.
# Here we define them manually.
values = np.array([
    [ 0.10,  0.05,  0.00,  0.02,  0.01],   # "the"
    [ 0.80,  0.70, -0.20,  0.60,  0.30],   # "firewall"
    [ 0.50,  0.40, -0.50,  0.55,  0.20],   # "blocked"
    [ 0.90,  0.60, -0.30,  0.50,  0.35],   # "malicious"
    [ 0.30,  0.50,  0.10,  0.40,  0.15],   # "connection"
])

# Context vector for "blocked" (index 2):
# weighted sum of all value vectors, using attention[2] as weights.
# This is the core attention computation: output = attention_weights @ values
context_blocked = attention[2] @ values

print(f'\nContext vector for "blocked" (weighted sum of value vectors):')
print(f"  {context_blocked}")

# Show how much each word contributed
print(f"\n  Top contributors:")
sorted_indices = np.argsort(attention[2])[::-1]
for j in sorted_indices:
    if attention[2][j] > 0.01:
        contribution = attention[2][j] * values[j]
        print(f"    {sentence[j]:<12} (weight {attention[2][j]:.2f}) -> contribution: {contribution}")

# For comparison, compute context vectors for all words
print("\nContext vectors for all words:")
all_contexts = attention @ values   # matrix multiply: (5x5) @ (5x5) = (5x5)
for i, word in enumerate(sentence):
    print(f"  {word:<12} -> {all_contexts[i]}")


# ============================================================
#   TASK 4 (Bonus): Visualise as a grid
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Attention Grid Visualisation")
print("=" * 60)

# Print the attention matrix as a formatted grid with word labels
max_word_len = max(len(w) for w in sentence)
header = " " * (max_word_len + 2)
for w in sentence:
    header += f"{w:>{max_word_len + 1}}"
print(f"\n{header}")
print(" " * (max_word_len + 2) + "-" * ((max_word_len + 1) * len(sentence)))

for i, word in enumerate(sentence):
    row_str = f"{word:>{max_word_len}}  "
    for j in range(len(sentence)):
        row_str += f"{attention[i][j]:>{max_word_len + 1}.2f}"
    row_str += f"  | sum = {attention[i].sum():.2f}"
    print(row_str)

print("\nKey takeaway: the attention mechanism lets each word dynamically")
print("decide which other words are relevant to its meaning in context.")
print('"blocked" attends to "firewall" (subject) and "malicious" (modifier)')
print("rather than treating all words equally.")

print("\n--- Exercise 3 complete. Lesson 1 done! ---")
