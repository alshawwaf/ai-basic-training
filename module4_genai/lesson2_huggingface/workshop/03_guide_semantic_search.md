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

```
Semantic Search: Two-Phase Architecture
───────────────────────────────────────────────────────────────
PHASE 1 — Indexing (offline, done once)

 Doc 1 ──►┐                    ┌───────────────────────────┐
 Doc 2 ──►┤  model.encode()    │ Embedding Matrix (N × 384)│
 Doc 3 ──►┤ ─────────────────► │ [0.23, -0.45, 0.87, ...] │ doc 1
 ...   ──►┤                    │ [0.11,  0.55, 0.02, ...] │ doc 2
 Doc N ──►┘                    │ [...]                     │
                               └───────────────────────────┘

PHASE 2 — Query (real-time)

 "how to stop          model.encode()    cosine_similarity()
  credential theft" ─────────────────► [0.18, 0.52, ...]
                                              │
                                              ▼
                                  scores: [0.34, 0.89, 0.71, ...]
                                              │
                                         argsort + top-k
                                              │
                                              ▼
                                  Doc 2 (0.89), Doc 3 (0.71), ...
```

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

```
Keyword vs Semantic Search
──────────────────────────────────────────────────────
 Query: "how to stop credential theft"

 Keyword search                 Semantic search
 ─────────────────              ────────────────────
 looks for exact words:         looks for meaning:
 "credential" AND "theft"       ● Mimikatz detection
       │                        ● DCSync attacks
       ▼                        ● LSASS memory dumping
 only docs with those words     ● Pass-the-Hash defense
 (misses related concepts)      (finds related concepts!)
```

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

[03_lab_semantic_search.md](03_lab_semantic_search.md)
## Workshop Complete

Compare your code against the matching `_solution_` files, then move to:

**[Lesson 4.3 — LLM API](../../lesson3_llm_api/workshop/00_overview.md)**
