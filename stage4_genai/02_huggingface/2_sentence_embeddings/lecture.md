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

```
Sentence Embedding: entire sentence ───► one vector
─────────────────────────────────────────────────────
 Sentence                             384-dim vector
┌────────────────────────────────┐   ┌──────────────┐
│"System was compromised via     │──►│ [0.23, -0.45,│
│ phishing"                      │   │  0.87, ...]  │
├────────────────────────────────┤   ├──────────────┤
│"Spear-phishing email led to   │──►│ [0.21, -0.42,│  ← similar!
│ the breach"                    │   │  0.89, ...]  │
├────────────────────────────────┤   ├──────────────┤
│"Pizza delivery takes 30 min"  │──►│[-0.55,  0.31,│  ← very different
│                                │   │ -0.12, ...]  │
└────────────────────────────────┘   └──────────────┘
```

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

```
Cosine Similarity Matrix (N × N)
──────────────────────────────────────────────────────
              Sent A    Sent B    Sent C
           ┌─────────┬─────────┬─────────┐
  Sent A   │  1.00   │  0.91   │  0.12   │
  Sent B   │  0.91   │  1.00   │  0.15   │  ← A and B are similar
  Sent C   │  0.12   │  0.15   │  1.00   │  ← C is unrelated
           └─────────┴─────────┴─────────┘
```

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

## Now Open the Lab

[handson.md](handson.md)
## Next

[../3_semantic_search/lecture.md](../3_semantic_search/lecture.md) — build a full semantic search engine over a security knowledge base.
