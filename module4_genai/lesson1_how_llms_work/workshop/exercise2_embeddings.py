# =============================================================================
# LESSON 4.1 | WORKSHOP | Exercise 2 of 3
# Embeddings: Tokens as Vectors
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How the embedding matrix maps token IDs to dense vectors
# - How cosine similarity measures semantic closeness
# - Why similar words have similar embeddings after training
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson1_how_llms_work/workshop/exercise2_embeddings.py
# =============================================================================

import numpy as np

# Vocabulary from Exercise 1 (reproduced here so this file runs standalone)
vocab = {
    "<UNK>": 0, "the": 1, "network": 2, "connection": 3, "is": 4,
    "suspicious": 5, "malicious": 6, "benign": 7, "port": 8, "scan": 9,
    "firewall": 10, "blocked": 11, "allowed": 12, "traffic": 13, "alert": 14,
    "endpoint": 15, "detected": 16, "attack": 17, "normal": 18, "<EOS>": 19,
}

# =============================================================================
# BACKGROUND
# =============================================================================
# The embedding matrix converts token IDs to dense vectors.
# Shape: (vocab_size=20, embedding_dim=4)
#
# In a real model, embedding_dim is 768 (BERT), 1024 (Claude Haiku), or 4096+.
# We use 4 dimensions so the numbers stay readable.
#
# These embeddings are hand-crafted to show the structure:
#   - security-threat words (malicious, suspicious, attack) cluster together
#   - network-infrastructure words (firewall, traffic, port) cluster together
#   - benign/normal are positioned opposite to threat words

# =============================================================================
# TASK 1 — Build the embedding matrix
# =============================================================================
# Create a NumPy array called `embeddings` with shape (20, 4).
# Use these values (each row = one token's 4-dimensional vector):
#
#   Row  0  (<UNK>):      [ 0.00,  0.00,  0.00,  0.00]
#   Row  1  (the):        [ 0.10, -0.20,  0.05,  0.10]
#   Row  2  (network):    [ 0.70,  0.20, -0.30,  0.60]
#   Row  3  (connection): [ 0.65,  0.25, -0.25,  0.55]
#   Row  4  (is):         [ 0.08, -0.15,  0.03,  0.08]
#   Row  5  (suspicious): [ 0.90,  0.10, -0.50,  0.75]
#   Row  6  (malicious):  [ 0.92,  0.08, -0.52,  0.78]
#   Row  7  (benign):     [-0.85, -0.10,  0.48, -0.70]
#   Row  8  (port):       [ 0.60,  0.40, -0.20,  0.50]
#   Row  9  (scan):       [ 0.75,  0.35, -0.40,  0.65]
#   Row 10  (firewall):   [ 0.55,  0.45, -0.15,  0.45]
#   Row 11  (blocked):    [ 0.50,  0.30, -0.10,  0.40]
#   Row 12  (allowed):    [-0.45, -0.25,  0.08, -0.35]
#   Row 13  (traffic):    [ 0.60,  0.35, -0.18,  0.50]
#   Row 14  (alert):      [ 0.80,  0.20, -0.45,  0.70]
#   Row 15  (endpoint):   [ 0.65,  0.30, -0.28,  0.55]
#   Row 16  (detected):   [ 0.72,  0.18, -0.38,  0.62]
#   Row 17  (attack):     [ 0.93,  0.05, -0.55,  0.80]
#   Row 18  (normal):     [-0.80, -0.08,  0.45, -0.65]
#   Row 19  (<EOS>):      [ 0.00,  0.01,  0.00,  0.00]
#
# Print: "Embedding matrix shape:", embeddings.shape
#
# EXPECTED OUTPUT:
#   Embedding matrix shape: (20, 4)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Look up embeddings for words
# =============================================================================
# Write a function: get_embedding(word) -> np.ndarray
#   - Look up the word in vocab to get its ID (default 0 for unknown)
#   - Return embeddings[id]
#
# Print the embedding vectors for: "malicious", "benign", "attack"
# Format: "  malicious: [0.92, 0.08, -0.52, 0.78]"
#
# EXPECTED OUTPUT:
#   malicious : [ 0.92  0.08 -0.52  0.78]
#   benign    : [-0.85 -0.10  0.48 -0.70]
#   attack    : [ 0.93  0.05 -0.55  0.80]

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Cosine similarity
# =============================================================================
# Implement: cosine_sim(a, b) -> float
#   return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#
# Compute and print cosine similarity for these pairs:
#   - "malicious"  vs "suspicious"   (expect: high positive, ~0.98)
#   - "malicious"  vs "benign"       (expect: negative,     ~-0.99)
#   - "firewall"   vs "traffic"      (expect: moderate,     ~0.98)
#   - "the"        vs "attack"       (expect: low,          ~0.20)
#
# Format: "  malicious vs suspicious : 0.9834"
#
# EXPECTED OUTPUT (approximate):
#   malicious vs suspicious : 0.9957
#   malicious vs benign     : -0.9991
#   firewall  vs traffic    : 0.9981
#   the       vs attack     : 0.2341

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Find most similar words (BONUS)
# =============================================================================
# Write: most_similar(query_word, top_n=5) -> list of (word, score) tuples
#   - Get query embedding
#   - Compute cosine_sim against every word in vocab (except the query itself and <UNK>, <EOS>)
#   - Sort by similarity descending
#   - Return top_n results
#
# Call it for "attack" and print the top 5.

# >>> YOUR CODE HERE


print("\n--- Exercise 2 complete. Move to exercise3_attention.py ---")
