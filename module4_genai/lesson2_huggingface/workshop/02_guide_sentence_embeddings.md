# Exercise 2 — Sentence Embeddings

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How sentence-transformers encode entire sentences as single dense vectors
- Why sentence embeddings differ from word embeddings
- How cosine similarity enables semantic comparison
- The foundation technology behind every modern RAG system

---

## Concept: Sentence Embeddings vs Word Embeddings

Word embeddings (covered in Lesson 4.1) give one vector per token. The full sentence meaning is lost.

Sentence embeddings encode the **entire sentence** into one vector that captures its overall meaning:

```
"The system was compromised via phishing"    → [0.23, -0.45, 0.87, ...]  (384 dims)
"A spear-phishing email led to the breach"  → [0.21, -0.42, 0.89, ...]  (similar!)
"Pizza delivery takes 30 minutes"           → [-0.55, 0.31, -0.12, ...] (very different)
```

Semantic similarity → close vectors. Semantic difference → distant vectors.

---

## Concept: The SentenceTransformer Model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 80MB, excellent quality/speed
embeddings = model.encode(["sentence one", "sentence two"])
# shape: (2, 384)
```

`all-MiniLM-L6-v2` was trained on 1 billion sentence pairs. Similar sentences were pulled together, dissimilar ones pushed apart (contrastive learning). It is the standard first choice for semantic similarity tasks.

---

## Concept: Cosine Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

# cosine_similarity(A, B) returns values from -1 (opposite) to +1 (identical direction)
scores = cosine_similarity(embeddings)  # shape: (N, N)
```

Practical thresholds for security text:
- `> 0.85` → nearly identical meaning
- `0.60–0.85` → related topic, different specifics
- `< 0.40` → likely unrelated

---

## What Each Task Asks You to Do

### Task 1 — Load model and encode sentences
Load `all-MiniLM-L6-v2`. Encode 6 security sentences. Print the shape of the result.

### Task 2 — Similarity matrix
Compute a 6×6 cosine similarity matrix. Print it rounded to 2 decimal places.

### Task 3 — Semantic search
For a query sentence, find and print the most similar entry in the set.

### Task 4 — Batch timing benchmark (Bonus)
Compare `model.encode(texts)` vs `model.encode(texts, batch_size=1)` on 100 sentences. Batch encoding should be 5-10× faster.

---

## Expected Outputs at a Glance

**Task 1**
```
Model: all-MiniLM-L6-v2
Encoded 6 sentences. Shape: (6, 384)
```

**Task 2**
```
Similarity matrix (6×6):
Row 0: [1.00  0.15  0.68  0.07  0.61  0.09]
Row 1: [0.15  1.00  0.12  0.55  0.10  0.48]
Row 2: [0.68  0.12  1.00  0.09  0.58  0.11]
Row 3: [0.07  0.55  0.09  1.00  0.08  0.52]
Row 4: [0.61  0.10  0.58  0.08  1.00  0.07]
Row 5: [0.09  0.48  0.11  0.52  0.07  1.00]
```
(Attack entries cluster in rows 0, 2, 4; benign entries in rows 1, 3, 5.)

**Task 3**
```
Query: Suspicious outbound connection after script execution
  1st: Outbound connection to C2 server after PowerShell one-liner (0.8923)
  2nd: Lateral movement detected: SMB login from WORKSTATION-042  (0.6712)
```

---

## Now Open the Exercise File

[02_lab_sentence_embeddings.md](02_lab_sentence_embeddings.md)

---

## Next

[03_guide_semantic_search.md](03_guide_semantic_search.md) — build a full semantic search engine over a security knowledge base.
