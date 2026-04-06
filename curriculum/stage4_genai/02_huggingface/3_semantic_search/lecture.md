# Exercise 3 — Semantic Search over a Security Knowledge Base

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How to build a minimal semantic search engine from scratch
- How to pre-compute and store embeddings for a document corpus
- How to rank results by cosine similarity
- Why this is the retrieval half of a RAG pipeline

---

## Concept: The Two-Phase Architecture

**Phase 1 — Indexing (done once, offline):**
```
documents → encode → embedding matrix  (N × 384)
```

**Phase 2 — Query (done at search time):**
```
query string → encode → query vector (1 × 384)
             ↓
cosine_similarity(query_vector, embedding_matrix)
             ↓
top-k scores → return ranked documents
```

Phase 2 is fast because document embeddings were computed in Phase 1. Only the query needs encoding at runtime.

**Semantic search — two-phase architecture**

| Phase | When it runs | Input | Operation | Output |
|---|---|---|---|---|
| **1. Indexing** | offline, once per corpus update | `Doc 1 … Doc N` | `model.encode(docs)` | Embedding matrix `(N, 384)` cached on disk |
| **2. Query** | real-time, every search | `"how to stop credential theft"` | `model.encode(query)` → `cosine_similarity(q, matrix)` → `argsort` | top-k document IDs with scores, e.g. `Doc 2 (0.89), Doc 3 (0.71)` |

Phase 1 is the expensive step (encode every document once). Phase 2 only encodes the *query* and runs a single matrix-vector cosine similarity, so it stays fast even with thousands of documents.

---

## Concept: Why Semantic Beats Keyword Search

```
Query: "how to stop credential theft"

Keyword search finds:
  → documents containing the exact words "credential" and "theft"

Semantic search finds:
  → documents about Mimikatz, DCSync, LSASS dumping, Pass-the-Hash
  → even if none of those documents contain "credential theft"
```

Semantic search understands intent. Keyword search matches strings.

**Keyword vs semantic search — same query, very different results**

> Query: `"how to stop credential theft"`

| | Keyword search | Semantic search |
|---|---|---|
| **What it matches** | exact tokens: `"credential"` AND `"theft"` | overall meaning of the sentence |
| **Hits returned** | only documents containing both literal words | Mimikatz detection, DCSync attacks, LSASS memory dumping, Pass-the-Hash defence |
| **Failure mode** | misses related concepts that don't share the exact words | rarely misses relevant docs; may surface loosely related ones |

Semantic search understands intent. Keyword search matches strings.

---

## Concept: Knowledge Base Structure

```python
KB = [
    {"id": "log4shell", "title": "CVE-2021-44228 Log4Shell", "text": "..."},
    {"id": "mimikatz",  "title": "Mimikatz Credential Theft", "text": "..."},
]
```

The `text` field is what gets encoded. `title` and `id` are metadata returned with results but not used for matching.

---

## What Each Task Asks You to Do

### Task 1 — Index the knowledge base
Encode all 6 document `text` fields. Print confirmation with embedding shape.

### Task 2 — Implement the search function
Write `search(query, top_k=3)` → list of `(score, doc)` tuples. Sort by score descending.

### Task 3 — Run 3 queries
Test with 3 security questions. Print ranked results with scores.

### Task 4 — Add threshold filtering (Bonus)
Modify `search()` to accept `min_score`. Only return results above that threshold.

---

## Now Open the Lab

[handson.md](handson.md)
## Workshop Complete

Compare your code against the matching solution files, then move to:

**[Lesson 4.3 — LLM API](../../03_llm_api/README.md)**
