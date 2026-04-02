# Lab — Exercise 2: Sentence Embeddings

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise2_sentence_embeddings.py` in this folder.

> Requires: `pip install sentence-transformers`

---

## Step 2: Add the imports and data

`SentenceTransformer` encodes full sentences into fixed-size vectors. `cosine_similarity` from scikit-learn computes pairwise similarity between those vectors.

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

SENTENCES = [
    "Outbound connection to C2 server after PowerShell one-liner execution",       # 0 attack
    "User authenticated with valid credentials during business hours",              # 1 benign
    "Lateral movement detected: SMB login from WORKSTATION-042 to DC-01",          # 2 attack
    "Scheduled backup job completed successfully at 02:00",                         # 3 benign
    "Ransomware encryption activity detected on file server shares",                # 4 attack
    "Software update deployed to 150 endpoints via SCCM at 03:00",                 # 5 benign
]

QUERY = "Suspicious outbound connection after script execution"
```

---

## Step 3: Load the model and encode all sentences

`all-MiniLM-L6-v2` (80 MB) was trained on 1 billion sentence pairs. It produces 384-dimensional vectors where semantically similar sentences are geometrically close.

Add this to your file:

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(SENTENCES)

print(f"Model: all-MiniLM-L6-v2")
print(f"Encoded {len(SENTENCES)} sentences. Shape: {embeddings.shape}")
```

Run your file. You should see:
```
Model: all-MiniLM-L6-v2
Encoded 6 sentences. Shape: (6, 384)
```

---

## Step 4: Compute and print the 6×6 similarity matrix

`cosine_similarity` on the full embedding matrix produces a symmetric 6×6 matrix where entry [i][j] is the similarity between sentences i and j. Notice attack sentences (0, 2, 4) form a cluster, and benign sentences (1, 3, 5) form a separate cluster.

Add this to your file:

```python
sim_matrix = cosine_similarity(embeddings)

print("\nSimilarity matrix (6×6):")
for i, row in enumerate(sim_matrix):
    row_str = "  ".join(f"{v:.2f}" for v in row)
    print(f"Row {i}: [{row_str}]")
```

Run your file. You should see (approximate values):
```
Similarity matrix (6×6):
Row 0: [1.00  0.15  0.68  0.07  0.61  0.09]
Row 1: [0.15  1.00  0.12  0.55  0.10  0.48]
Row 2: [0.68  0.12  1.00  0.09  0.58  0.11]
Row 3: [0.07  0.55  0.09  1.00  0.08  0.52]
Row 4: [0.61  0.10  0.58  0.08  1.00  0.07]
Row 5: [0.09  0.48  0.11  0.52  0.07  1.00]
```

---

## Step 5: Semantic search — find the most similar sentence to the query

Encoding the query and computing cosine similarity against all sentence embeddings ranks the corpus by relevance. The top match should be the C2/PowerShell entry (row 0) since it is semantically closest to the query about suspicious outbound connections.

Add this to your file:

```python
query_emb = model.encode([QUERY])
sims = cosine_similarity(query_emb, embeddings)[0]
ranked = np.argsort(sims)[::-1]

print(f"\nQuery: {QUERY}")
print(f"  1st: {SENTENCES[ranked[0]][:60]}... ({sims[ranked[0]]:.4f})")
print(f"  2nd: {SENTENCES[ranked[1]][:60]}... ({sims[ranked[1]]:.4f})")
```

Run your file. You should see (approximate scores):
```
Query: Suspicious outbound connection after script execution
  1st: Outbound connection to C2 server after PowerShell one-liner... (0.8923)
  2nd: Lateral movement detected: SMB login from WORKSTATION-042 to... (0.6712)
```

---

## Step 6: Batch encoding benchmark (Bonus Task 4)

Batch encoding processes multiple sentences together on the GPU/CPU, which is significantly faster than one-at-a-time encoding because overhead per call is amortised across the batch.

Add this to your file:

```python
import time

texts_100 = SENTENCES * 16 + SENTENCES[:4]  # 100 sentences

start = time.time()
model.encode(texts_100)
batch_time = time.time() - start

start = time.time()
model.encode(texts_100, batch_size=1)
single_time = time.time() - start

speedup = single_time / batch_time
print(f"\nBatch encoding : {batch_time:.3f}s")
print(f"Single encoding: {single_time:.3f}s")
print(f"Batch encoding is {speedup:.1f}x faster")

print("\n--- Exercise 2 complete. Move to exercise3_semantic_search.py ---")
```

Run your file. You should see output similar to:
```
Batch encoding : 0.312s
Single encoding: 1.874s
Batch encoding is 6.0x faster

--- Exercise 2 complete. Move to exercise3_semantic_search.py ---
```

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`02_solution_sentence_embeddings.py`) if anything looks different.
