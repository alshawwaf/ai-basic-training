# Exercise 2 — Sentence Embeddings
#
# Encodes entire sentences as dense vectors using sentence-transformers.
# Demonstrates cosine similarity for semantic comparison -- the foundation
# technology behind every modern RAG system.
#
# pip install sentence-transformers

import numpy as np
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
#   TASK 1: Load model and encode sentences
# ============================================================
print("=" * 60)
print("  TASK 1: Load Model and Encode Sentences")
print("=" * 60)

# all-MiniLM-L6-v2: 80MB model trained on 1 billion sentence pairs.
# Outputs 384-dimensional vectors. Excellent quality/speed tradeoff.
print("\nLoading all-MiniLM-L6-v2 (downloads ~80MB on first run)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 6 security sentences: 3 attack-related, 3 benign/operational
sentences = [
    "Outbound connection to C2 server after PowerShell one-liner",          # attack
    "Scheduled backup completed successfully at 02:00",                      # benign
    "Lateral movement detected: SMB login from WORKSTATION-042 to DC01",    # attack
    "Weekly patch cycle applied to all production servers",                   # benign
    "Credential dumping via Mimikatz on domain controller",                  # attack
    "Normal user login from corporate VPN at 09:15",                        # benign
]

# Encode all sentences into vectors in one batch
embeddings = model.encode(sentences)

print(f"\nModel: all-MiniLM-L6-v2")
print(f"Encoded {len(sentences)} sentences. Shape: {embeddings.shape}")
print(f"Each sentence -> {embeddings.shape[1]}-dimensional vector")


# ============================================================
#   TASK 2: Compute similarity matrix
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Similarity Matrix")
print("=" * 60)

# Cosine similarity: 1.0 = identical meaning, 0.0 = completely unrelated
sim_matrix = cosine_similarity(embeddings)

print(f"\nSimilarity matrix ({sim_matrix.shape[0]}x{sim_matrix.shape[1]}):")
print("\nSentence labels:")
for i, s in enumerate(sentences):
    print(f"  [{i}] {s[:65]}")

print(f"\n{'':>6}", end="")
for i in range(len(sentences)):
    print(f"  [{i}] ", end="")
print()

for i in range(len(sentences)):
    print(f"  [{i}] ", end="")
    for j in range(len(sentences)):
        print(f" {sim_matrix[i][j]:.2f}", end="")
    print()

# Highlight the pattern: attack sentences (0, 2, 4) cluster together,
# benign sentences (1, 3, 5) cluster together
print("\nObservation: attack sentences (rows 0, 2, 4) are more similar to")
print("each other than to benign sentences (rows 1, 3, 5).")


# ============================================================
#   TASK 3: Semantic search — find the most similar sentence
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Semantic Search")
print("=" * 60)

# Encode a new query and find the closest match in our sentence set
queries = [
    "Suspicious outbound connection after script execution",
    "Routine server maintenance completed overnight",
    "Attacker dumped NTLM hashes from memory",
]

for query in queries:
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]

    # Sort by similarity (highest first)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    print(f"\nQuery: {query}")
    for rank, (idx, score) in enumerate(ranked[:3], 1):
        marker = "***" if rank == 1 else "   "
        print(f"  {marker} {rank}. ({score:.4f}) {sentences[idx][:65]}")


# ============================================================
#   TASK 4 (Bonus): Batch timing benchmark
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Batch vs Sequential Encoding Speed")
print("=" * 60)

# Generate 100 sentences by repeating and varying our originals
bulk_sentences = sentences * 17  # 102 sentences (close to 100)
bulk_sentences = bulk_sentences[:100]

# Batch encoding (all at once — GPU/CPU can parallelise)
start = time.time()
_ = model.encode(bulk_sentences)
batch_time = time.time() - start

# Sequential encoding (one at a time — no parallelism)
start = time.time()
_ = model.encode(bulk_sentences, batch_size=1)
sequential_time = time.time() - start

speedup = sequential_time / batch_time if batch_time > 0 else 0

print(f"\n  100 sentences:")
print(f"    Batch encoding:      {batch_time:.3f}s")
print(f"    Sequential (bs=1):   {sequential_time:.3f}s")
print(f"    Speedup:             {speedup:.1f}x")
print(f"\n  Takeaway: always encode in batches when processing large corpora.")

print("\n--- Exercise 2 complete. Move to ../3_semantic_search/solution.py ---")
