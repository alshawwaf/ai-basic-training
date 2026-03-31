# =============================================================================
# LESSON 4.1 | WORKSHOP | Exercise 1 of 3
# Tokenisation: Text as Token IDs
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why models process integers, not raw text
# - How to build a toy vocabulary and encode/decode sentences
# - Out-of-vocabulary (OOV) handling with <UNK>
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson1_how_llms_work/workshop/exercise1_tokenisation.py
# =============================================================================

# No external libraries needed — this is pure Python

# =============================================================================
# BACKGROUND
# =============================================================================
# LLMs cannot process text directly. Every word (or subword) is mapped to an
# integer ID. The model learns an embedding vector for each ID. Only numbers
# flow through the network.
#
# Real vocabulary: ~100,000 tokens (GPT-4, Claude).
# This exercise uses a toy 20-token vocabulary so you can see every mapping.

# =============================================================================
# TASK 1 — Build a toy vocabulary
# =============================================================================
# Create a dict called `vocab` that maps word → integer ID.
# Start with <UNK>=0 and <EOS>=19.
# Fill in IDs 1–18 with these 18 words (in this order):
#   the, network, connection, is, suspicious, malicious, benign,
#   port, scan, firewall, blocked, allowed, traffic, alert,
#   endpoint, detected, attack, normal
#
# Print the vocabulary, one token per line: "  0: <UNK>"
#
# EXPECTED OUTPUT:
#   Vocabulary (20 tokens):
#     0: <UNK>
#     1: the
#     2: network
#     ...
#    19: <EOS>

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Encode a sentence to token IDs
# =============================================================================
# Write a function: encode(text) -> list[int]
#   - Split text on spaces (text.split())
#   - Map each word to its ID using vocab.get(word, 0)  ← 0 for unknown
#   - Append vocab["<EOS>"] at the end
#   - Return the list of IDs
#
# Encode these two sentences and print the result:
#   sentence1 = "the network connection is suspicious"
#   sentence2 = "port scan detected on endpoint"
#
# EXPECTED OUTPUT:
#   "the network connection is suspicious" → [1, 2, 3, 4, 5, 19]
#   "port scan detected on endpoint"       → [8, 9, 16, 0, 15, 19]
#   (note: "on" is not in the vocabulary → maps to 0 = <UNK>)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Decode token IDs back to text
# =============================================================================
# Build a reverse vocabulary: id_to_word = {id: word for word, id in vocab.items()}
#
# Write a function: decode(ids) -> str
#   - Map each ID back to its word
#   - Join with spaces
#   - Return the resulting string
#
# Decode the result of Task 2 sentence1 and confirm it matches the original.
# Print: "Round-trip successful: True/False"
#
# EXPECTED OUTPUT:
#   [1, 2, 3, 4, 5, 19] → "the network connection is suspicious <EOS>"
#   Round-trip successful: True

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Observe OOV handling (BONUS)
# =============================================================================
# Encode this sentence (contains words not in the vocabulary):
#   oov_sentence = "the ransomware encrypted all files on the endpoint"
#
# Print the encoded IDs.
# Then decode them.
# Observe: what information is lost when words become <UNK>?
# Print a comment explaining what the model "sees" vs what was intended.

# >>> YOUR CODE HERE


print("\n--- Exercise 1 complete. Move to exercise2_embeddings.py ---")
