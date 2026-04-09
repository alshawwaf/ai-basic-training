# Semantic Search over a Security Knowledge Base

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_search_two_phase.png" alt="A two-row pipeline diagram. Top row labelled 'PHASE 1 — Indexing (offline, once per corpus update)' shows three boxes: 'Doc 1 ... Doc N' → 'model.encode(docs)' → 'Embedding matrix (N, 384) on disk'. Bottom row labelled 'PHASE 2 — Query (real-time, every search)' shows four boxes: '\"how to stop credential theft\"' → 'encode(query) (1, 384)' → 'cosine vs index' → 'top-k results'. Caption at the bottom notes 'phase 1 is the slow step — phase 2 only encodes the query'.">
  <div class="vis-caption">The two-phase architecture in one picture. Phase 1 happens once and is cached on disk; Phase 2 runs every time a user searches and is fast because all the document vectors are already computed. This separation is what makes semantic search practical at scale.</div>
</div>

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_keyword_vs_semantic.png" alt="Two side-by-side panels under the query 'how to stop credential theft'. Left red-bordered panel 'Keyword search (matches exact tokens)' shows two green checkmarks for documents containing the literal words 'credential' and 'theft', and four red crosses for missed documents about Mimikatz, DCSync, LSASS dumping, and Pass-the-Hash. Right green-bordered panel 'Semantic search (matches meaning)' shows six green checkmarks for documents about Mimikatz detection, DCSync defence, LSASS memory dumping, Pass-the-Hash mitigation, Credential Guard, and Sysmon Event ID 10.">
  <div class="vis-caption">The same query, two retrieval philosophies. Keyword search only finds documents that contain the literal words "credential" AND "theft". Semantic search finds documents about the underlying concept — even when none of those documents contain the exact query words.</div>
</div>

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
