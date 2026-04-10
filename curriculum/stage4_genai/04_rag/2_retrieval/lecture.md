# Retrieval: Finding Relevant Chunks

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How to encode a corpus of chunks into a vector index
- How to retrieve the top-k most relevant chunks for any query
- How retrieval quality depends on chunk quality
- How to evaluate retrieval: does the right chunk come back?

---

## Concept: From Whole-Document Search to Chunk-Aware Retrieval

In **Lesson 4.2.3** you already built a two-phase semantic search engine: indexing once, then querying. This exercise is the same machine, with one change — instead of encoding *whole documents*, you encode the **chunks** you produced in 4.4.1.

| | 4.2.3 Semantic Search | 4.4.2 Retrieval for RAG |
|---|---|---|
| Unit of indexing | Whole documents | Chunks (from 4.4.1) |
| Index shape | `(num_docs, 384)` | `(num_chunks, 384)` — usually much larger |
| What a "hit" returns | A document to read | A passage the LLM can inline into its prompt |
| Tracked alongside each vector | `doc_id` | `(doc_id, chunk_text)` — you need the text itself, not just a label |

That last row is the only real code change. When you built the index in 4.2.3 you stored `(doc_id, vector)` pairs, because the aim was to point the user at a document. Here you store `(doc_id, chunk_text, vector)` triples, because in the next exercise the *chunk text itself* will be pasted into the LLM's system prompt.

Everything else — `model.encode()`, cosine similarity, `argsort`, top-k — is identical to 4.2.3. If that lesson felt shaky, skim it once before continuing; this exercise will assume you remember it.

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
