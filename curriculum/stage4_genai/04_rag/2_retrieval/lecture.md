# Exercise 2 — Retrieval: Finding Relevant Chunks

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How to encode a corpus of chunks into a vector index
- How to retrieve the top-k most relevant chunks for any query
- How retrieval quality depends on chunk quality
- How to evaluate retrieval: does the right chunk come back?

---

## Concept: The Vector Index

After chunking, you encode each chunk into a vector using a sentence embedding model. All chunk vectors together form a **vector index** (an embedding matrix):

```
Corpus: N chunks
Encode: model.encode(chunks)   → shape: (N, 384)

Query: "how to detect LSASS dumping"
Encode: model.encode([query])  → shape: (1, 384)

Retrieve: cosine_similarity(query_vector, index) → scores (N,)
          top_k = argsort(scores)[::-1][:k]
          return [chunks[i] for i in top_k]
```

This is **Phase 1 + Phase 2** of the RAG pipeline — everything except the final LLM generation step.

**Vector retrieval — query embedding vs chunk embeddings**

> Query: `"how to detect LSASS dumping"` → `model.encode()` → `[0.45, 0.12, -0.33, ...]` (1 × 384)

| Chunk | Embedding (truncated) | Cosine score | |
|---|---|---:|---|
| Chunk 1 | `[0.10, -0.55, 0.22, ...]` | 0.31 | |
| **Chunk 2** | `[0.43, 0.15, -0.30, ...]` | **0.92** | ← top match |
| Chunk 3 | `[0.38, 0.08, -0.28, ...]` | 0.78 | |
| … | … | … | |
| Chunk N | `[-0.12, 0.60, 0.05, ...]` | 0.15 | |

The retriever computes cosine similarity between the query vector and every chunk vector in one matrix-vector operation, runs `argsort`, and returns the top-k chunks (e.g. Chunk 2, Chunk 3, Chunk 5). The chunk *text* is then handed to the LLM in the next stage.

---

## Concept: Top-k vs Threshold Retrieval

**Top-k**: always return the k most similar chunks, regardless of their actual similarity score.
- Reliable — always returns k results
- May include irrelevant chunks if no good match exists

**Threshold**: return all chunks above a minimum similarity score.
- More precise — returns only chunks that are genuinely relevant
- May return 0 results if the query is outside the knowledge base scope

For RAG, top-k=3 with threshold filtering is a good default.

**Top-k vs threshold retrieval — same scores, two policies**

> Sorted scores from the index: `[0.92, 0.78, 0.45, 0.31, 0.15, 0.08]`

| Policy | Returned chunks | Note |
|---|---|---|
| **Top-k (k=3)** | Chunk 2 (0.92), Chunk 3 (0.78), Chunk 5 (0.45) | always returns exactly 3, but 0.45 may not actually be relevant |
| **Threshold (min=0.60)** | Chunk 2 (0.92), Chunk 3 (0.78) | only genuinely relevant chunks; may return 0 if the query is out of scope |
| **Top-k + threshold** (recommended) | up to k chunks above the threshold | reliable upper bound on size *and* a quality floor |

---

## Concept: Retrieval Evaluation

For each query where you know the correct answer, check if the answer appears in the top-k retrieved chunks:

```
Query: "What event ID to look for with Mimikatz?"
Expected in: chunk containing "Sysmon Event ID 10"

Retrieved:
  Rank 1 (0.89): "Detection relies on monitoring LSASS memory access... Sysmon Event ID 10."  ✓
  Rank 2 (0.71): "Mitigations include Credential Guard..."
  Rank 3 (0.58): "sekurlsa::logonpasswords for plaintext creds..."
```

Rank 1 hit = the retrieval step is working correctly.

---

## What Each Task Asks You to Do

### Task 1 — Build the vector index
Chunk the knowledge base using overlap chunking. Encode all chunks. Print the index shape.

### Task 2 — Implement retrieve(query, top_k=3)
Encode query, compute cosine similarities, return top_k (score, chunk_text) tuples.

### Task 3 — Run 3 queries and evaluate
Run 3 security queries. For each, print the top 3 results. Check manually: does the relevant chunk appear at rank 1?

### Task 4 — Reciprocal Rank metric (Bonus)
For each query, compute the reciprocal rank (1/rank) of the first relevant result. Average across queries = Mean Reciprocal Rank (MRR). Target: MRR > 0.8.

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../3_rag_pipeline/lecture.md](../3_rag_pipeline/lecture.md) — combine retrieval with LLM generation for grounded answers.
