# =============================================================================
# LESSON 4.2 | WORKSHOP | Exercise 2 of 3
# Sentence Embeddings
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How SentenceTransformer encodes entire sentences as 384-dimensional vectors
# - How cosine similarity measures semantic relatedness
# - The core technology behind RAG retrieval
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson2_huggingface/workshop/exercise2_sentence_embeddings.py
#
# pip install sentence-transformers
# =============================================================================

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Mix of attack-related and benign security sentences
SENTENCES = [
    "Outbound connection to C2 server after PowerShell one-liner execution",       # 0 attack
    "User authenticated with valid credentials during business hours",              # 1 benign
    "Lateral movement detected: SMB login from WORKSTATION-042 to DC-01",          # 2 attack
    "Scheduled backup job completed successfully at 02:00",                         # 3 benign
    "Ransomware encryption activity detected on file server shares",                # 4 attack
    "Software update deployed to 150 endpoints via SCCM at 03:00",                 # 5 benign
]

QUERY = "Suspicious outbound connection after script execution"

# =============================================================================
# BACKGROUND
# =============================================================================
# SentenceTransformer maps each sentence to a fixed-size vector (384 dims).
# Sentences with similar meaning produce vectors that are close in this space.
# Cosine similarity measures the angle between two vectors:
#   +1.0 = identical direction (same meaning)
#    0.0 = orthogonal (unrelated)
#   -1.0 = opposite direction (opposite meaning)

# =============================================================================
# TASK 1 — Load the model and encode all sentences
# =============================================================================
# Load: model = SentenceTransformer("all-MiniLM-L6-v2")
# Encode: embeddings = model.encode(SENTENCES)
#
# Print:
#   "Model: all-MiniLM-L6-v2"
#   "Encoded 6 sentences. Shape: (6, 384)"
#
# EXPECTED OUTPUT:
#   Model: all-MiniLM-L6-v2
#   Encoded 6 sentences. Shape: (6, 384)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Compute and print the 6×6 similarity matrix
# =============================================================================
# Compute: sim_matrix = cosine_similarity(embeddings)   # shape: (6, 6)
#
# Print each row:
#   "Row 0: [1.00  0.15  0.68  0.07  0.61  0.09]"
#
# Use: " ".join(f"{v:.2f}" for v in row) for formatting.
#
# What to notice:
#   - Rows 0, 2, 4 (attack) are more similar to each other than to rows 1, 3, 5
#   - Rows 1, 3, 5 (benign) cluster together
#
# EXPECTED OUTPUT (approximate):
#   Similarity matrix (6×6):
#   Row 0: [1.00  0.15  0.68  0.07  0.61  0.09]
#   Row 1: [0.15  1.00  0.12  0.55  0.10  0.48]
#   ...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Semantic search: find the most similar sentence to QUERY
# =============================================================================
# Encode QUERY: query_emb = model.encode([QUERY])   # shape: (1, 384)
# Compute: sims = cosine_similarity(query_emb, embeddings)[0]  # shape: (6,)
# Sort indices by similarity descending.
# Print:
#   "Query: [QUERY]"
#   "  1st: [top sentence] ([score:.4f])"
#   "  2nd: [second sentence] ([score:.4f])"
#
# EXPECTED OUTPUT (approximate):
#   Query: Suspicious outbound connection after script execution
#     1st: Outbound connection to C2 server after PowerShell... (0.8923)
#     2nd: Lateral movement detected: SMB login from WORKSTATI... (0.6712)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Batch encoding benchmark (BONUS)
# =============================================================================
# import time
# texts_100 = SENTENCES * 16 + SENTENCES[:4]  # 100 sentences
#
# Time model.encode(texts_100) vs model.encode(texts_100, batch_size=1)
# Print the speedup ratio: "Batch encoding is Xx faster"

# >>> YOUR CODE HERE


print("\n--- Exercise 2 complete. Move to exercise3_semantic_search.py ---")
