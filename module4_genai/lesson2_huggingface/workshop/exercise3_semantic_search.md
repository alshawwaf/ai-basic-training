# Exercise 3 — Semantic Search over a Security Knowledge Base

> Read this guide fully before opening the exercise file.

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

## Expected Outputs at a Glance

**Task 3**
```
Query: how do I detect mimikatz credential dumping?
  0.8923 | Mimikatz Credential Theft
  0.6102 | Lateral Movement Detection
  0.4234 | Network Segmentation for Defence

Query: what should I do when ransomware hits?
  0.9234 | Ransomware Incident Response Playbook
  0.5123 | Network Segmentation for Defence
  0.4512 | Lateral Movement Detection

Query: how to prevent attackers from moving between systems?
  0.8412 | Network Segmentation for Defence
  0.7234 | Lateral Movement Detection
  0.4123 | Ransomware Incident Response Playbook
```

---

## Now Open the Exercise File

[exercise3_semantic_search.py](exercise3_semantic_search.py)

---

## Workshop Complete

Open [reference_solution.py](reference_solution.py) to compare, then move to:

**[Lesson 4.3 — LLM API](../../lesson3_llm_api/workshop/1_lab_guide.md)**
