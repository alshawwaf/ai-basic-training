# Exercise 2 — Embeddings: Tokens as Vectors
#
# Shows how token IDs are converted to dense vectors (embeddings) and
# how cosine similarity measures semantic distance between words.
#
# pip install numpy

import numpy as np

# ============================================================
#   TASK 1: Build a toy embedding matrix
# ============================================================
print("=" * 60)
print("  TASK 1: Build a Toy Embedding Matrix")
print("=" * 60)

# Same 20-token vocabulary from Exercise 1
words = [
    "<UNK>", "the", "network", "connection", "is", "suspicious",
    "malicious", "benign", "port", "scan", "firewall",
    "blocked", "allowed", "traffic", "alert", "endpoint",
    "detected", "attack", "normal", "<EOS>",
]

# Word-to-ID mapping
vocab = {w: i for i, w in enumerate(words)}

# Embedding matrix: 20 tokens x 4 dimensions
# Each row is a hand-crafted vector that encodes semantic properties:
#   dim 0 ~ threat level      (high = dangerous)
#   dim 1 ~ network-related   (high = involves networking)
#   dim 2 ~ action/state      (positive = active, negative = passive)
#   dim 3 ~ detection-related  (high = involves monitoring/alerting)
embedding_matrix = np.array([
    [ 0.00,  0.00,  0.00,  0.00],   #  0: <UNK>
    [ 0.01,  0.01,  0.01,  0.01],   #  1: the        (function word, near-zero)
    [ 0.20,  0.90,  0.10,  0.30],   #  2: network
    [ 0.15,  0.85,  0.20,  0.20],   #  3: connection
    [ 0.00,  0.00,  0.00,  0.00],   #  4: is         (function word)
    [ 0.85,  0.30, -0.40,  0.70],   #  5: suspicious
    [ 0.90,  0.25, -0.50,  0.65],   #  6: malicious  (close to suspicious)
    [-0.70,  0.10,  0.60, -0.30],   #  7: benign     (opposite of malicious)
    [ 0.10,  0.80,  0.30,  0.20],   #  8: port
    [ 0.40,  0.70,  0.50,  0.60],   #  9: scan
    [ 0.05,  0.85, -0.20,  0.40],   # 10: firewall
    [ 0.10,  0.50, -0.60,  0.30],   # 11: blocked
    [-0.10,  0.50,  0.60, -0.10],   # 12: allowed
    [ 0.15,  0.80,  0.10,  0.25],   # 13: traffic
    [ 0.60,  0.40,  0.20,  0.85],   # 14: alert
    [ 0.30,  0.50,  0.10,  0.50],   # 15: endpoint
    [ 0.50,  0.30,  0.40,  0.80],   # 16: detected
    [ 0.95,  0.40, -0.30,  0.50],   # 17: attack
    [-0.50,  0.20,  0.50, -0.20],   # 18: normal
    [ 0.00,  0.00,  0.00,  0.00],   # 19: <EOS>
], dtype=np.float32)

print(f"\nEmbedding matrix shape: {embedding_matrix.shape}")
print(f"  {embedding_matrix.shape[0]} tokens, each represented as a {embedding_matrix.shape[1]}-dimensional vector")
print(f"\nSample embeddings:")
for w in ["malicious", "suspicious", "benign", "firewall"]:
    vec = embedding_matrix[vocab[w]]
    print(f"  {w:<12} -> {vec}")


# ============================================================
#   TASK 2: Look up embeddings by word
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Look Up Embeddings")
print("=" * 60)


def get_embedding(word):
    """Return the embedding vector for a word.

    Looks up the word's ID in the vocabulary, then returns the
    corresponding row from the embedding matrix.
    Falls back to <UNK> (row 0) for unknown words.
    """
    token_id = vocab.get(word, 0)
    return embedding_matrix[token_id]


# Demonstrate lookup for a short sentence
sentence = "the firewall blocked malicious traffic"
print(f'\nEmbeddings for: "{sentence}"')
for word in sentence.split():
    vec = get_embedding(word)
    print(f"  {word:<12} (ID {vocab.get(word, 0):>2}) -> {vec}")


# ============================================================
#   TASK 3: Compute cosine similarity
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Cosine Similarity")
print("=" * 60)


def cosine_sim(a, b):
    """Cosine similarity: 1.0 = identical direction, 0.0 = orthogonal, -1.0 = opposite."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    # Small epsilon to avoid division by zero
    return dot / (norm_a * norm_b + 1e-8)


# Compare three pairs that should show different similarity levels
pairs = [
    ("malicious", "suspicious"),   # both are threat-related — should be high
    ("malicious", "benign"),       # semantic opposites — should be negative
    ("firewall", "traffic"),       # both network-related — moderate similarity
    ("attack", "malicious"),       # both high-threat — should be high
    ("normal", "benign"),          # both non-threatening — should be positive
]

print("\nCosine similarities:")
for w1, w2 in pairs:
    v1 = get_embedding(w1)
    v2 = get_embedding(w2)
    sim = cosine_sim(v1, v2)
    bar = "#" * int(max(0, sim) * 20)
    print(f"  {w1:<12} vs {w2:<12} : {sim:+.4f}  {bar}")


# ============================================================
#   TASK 4 (Bonus): Find the most similar words
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Most Similar Words")
print("=" * 60)


def most_similar(query_word, top_k=5):
    """Find the top-k most similar words to the query word by cosine similarity."""
    query_vec = get_embedding(query_word)
    similarities = []
    for word, idx in vocab.items():
        # Skip the query word itself and special tokens with zero vectors
        if word == query_word or word in ("<UNK>", "<EOS>", "is"):
            continue
        sim = cosine_sim(query_vec, embedding_matrix[idx])
        similarities.append((word, sim))
    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


# Find words most similar to "attack"
for query in ["attack", "network", "detected"]:
    print(f'\nTop 5 words most similar to "{query}":')
    for rank, (word, sim) in enumerate(most_similar(query), 1):
        bar = "#" * int(max(0, sim) * 20)
        print(f"  {rank}. {word:<12} {sim:+.4f}  {bar}")

print("\n--- Exercise 2 complete. Move to 03_solution_attention.py ---")
