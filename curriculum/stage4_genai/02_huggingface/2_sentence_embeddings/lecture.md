# Sentence Embeddings

---

## What You Will Learn

- How sentence-transformers encode entire sentences as single dense vectors
- Why sentence embeddings differ from word embeddings
- How cosine similarity enables semantic comparison
- The foundation technology behind every modern RAG system

---

## Concept: Sentence Embeddings vs Word Embeddings

In **Lesson 4.1.2** you built a toy embedding matrix by hand: 20 tokens, 4 dimensions each, and you computed cosine similarity with `numpy.dot` and `numpy.linalg.norm`. The mechanics in this lesson are *exactly the same operation* — `cosine_similarity(a, b)` against an embedding matrix — with two upgrades:

- The vectors are no longer 4-dim toys; they are **384-dim** real outputs from a model trained on a billion sentence pairs.
- The unit of embedding is no longer one token at a time, but **a whole sentence** as a single vector.

Word embeddings (covered in Lesson 4.1.2) give one vector per token. The full sentence meaning is lost when you try to compare sentences by averaging or comparing tokens individually.

Sentence embeddings encode the **entire sentence** into one vector that captures its overall meaning:

```
"The system was compromised via phishing"    → [0.23, -0.45, 0.87, ...]  (384 dims)
"A spear-phishing email led to the breach"  → [0.21, -0.42, 0.89, ...]  (similar!)
"Pizza delivery takes 30 minutes"           → [-0.55, 0.31, -0.12, ...] (very different)
```

Semantic similarity → close vectors. Semantic difference → distant vectors.

**Sentence embedding — one vector for the whole sentence**

| Sentence | 384-dim vector | Note |
|---|---|---|
| `"System was compromised via phishing"` | `[0.23, -0.45, 0.87, ...]` |  |
| `"Spear-phishing email led to the breach"` | `[0.21, -0.42, 0.89, ...]` | ← similar to row 1 |
| `"Pizza delivery takes 30 min"` | `[-0.55, 0.31, -0.12, ...]` | ← very different |

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

## Concept: Picking an Embedding Model

`all-MiniLM-L6-v2` is the standard first choice, but it is one of many. The number of dimensions is the main lever &mdash; more dimensions usually means higher quality, at the cost of bigger vectors to store and slower similarity search.

| Embedding model | Dimensions | Notes |
|---|---:|---|
| `all-MiniLM-L6-v2` <small>(free, runs locally)</small> | **384** | Small, fast, good enough for most internal tools |
| OpenAI `text-embedding-3-small` | **1,536** | Cheap API, the default for most RAG apps |
| Cohere `embed-english-v3.0` | **1,024** | Strong on English |
| OpenAI `text-embedding-3-large` | **3,072** | Highest quality, more expensive |
| Llama-3 hidden state | **4,096** | What an LLM uses internally |

> **Important:** all vectors compared with cosine similarity must come from the **same model**. You cannot mix MiniLM vectors with OpenAI vectors &mdash; they live in completely different coordinate systems. Pick one model when you build your index, and use the same model at query time.

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

**Cosine similarity matrix (N × N)**

|  | Sent A | Sent B | Sent C |
|---|---:|---:|---:|
| **Sent A** | 1.00 | 0.91 | 0.12 |
| **Sent B** | 0.91 | 1.00 | 0.15 |
| **Sent C** | 0.12 | 0.15 | 1.00 |

The diagonal is always 1.00 (every sentence is identical to itself). Sentences A and B score 0.91 — nearly identical meaning. Sentence C scores ~0.13 with both — clearly unrelated.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_sentence_similarity.png" alt="A 6×6 cosine similarity heatmap titled 'Real cosine similarity matrix from all-MiniLM-L6-v2'. Rows and columns are six security sentences: outbound connection to suspicious IP, powershell launched from word.exe, user logged in from new location, DNS query to C2 domain, multiple failed logins, and an unrelated FedEx delivery sentence. The diagonal is all 1.00. Security-related sentences show moderate-to-high cosine values with each other (0.4-0.7 range) and the FedEx sentence shows very low similarity to everything else.">
  <div class="vis-caption">Real cosine similarity matrix computed by encoding 6 sentences with <code>all-MiniLM-L6-v2</code> and comparing every pair. The unrelated FedEx sentence (row/column 6) sits at the bottom of the heatmap with low similarity to everything — exactly what we want from a semantic search engine.</div>
</div>

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
