# Exercise 1 — Document Chunking

> Read this guide fully before opening the lab.

---

## What You Will Learn

- Why documents must be split before embedding
- Three chunking strategies: fixed-size, fixed-size with overlap, sentence-based
- How chunk size affects retrieval quality
- The tradeoffs between chunk size and context

---

## Concept: Why Chunking Is Necessary

Sentence embedding models have a maximum input length (typically 128–512 tokens). Long documents must be split into chunks before encoding.

But chunking is not just a technical constraint — it also determines retrieval granularity:

| Chunk too large | Chunk too small |
|----------------|----------------|
| Embeddings average too much content — retrieved chunks contain irrelevant information | Context gets split across chunks — answers may be incomplete |
| Model gets confused context | Many more chunks to search through |
| Hard to attribute specific facts | Loses cross-sentence context |

**Rule of thumb:** 100–300 words per chunk, with 20–50 word overlap.

```
Long Document ───► Chunks
──────────────────────────────────────────────────────
 Original document (800 words)
┌────────────────────────────────────────────────────┐
│ word 1 ... word 100 ... word 200 ... word 300 ...  │
│ ... word 400 ... word 500 ... word 600 ... word 800│
└────────────────────────────────────────────────────┘
                      │
                      ▼  split into chunks
 ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
 │ Chunk 1      │ │ Chunk 2      │ │ Chunk 3      │ ...
 │ words 1-100  │ │ words 101-200│ │ words 201-300│
 └──────────────┘ └──────────────┘ └──────────────┘
  each chunk is small enough to embed (128-512 tokens)
```

---

## Concept: Fixed-Size Chunking

Split document text into chunks of N words:

```python
def chunk_fixed(text, chunk_size=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:   # skip tiny trailing chunks
            chunks.append(chunk)
    return chunks
```

Problem: a sentence may be cut in half, losing meaning at chunk boundaries.

```
Fixed-Size Chunking (no overlap) — boundary problem
──────────────────────────────────────────────────────
 ┌──── Chunk 1 ─────┐┌──── Chunk 2 ─────┐
 │ ... detection    ││ relies on Sysmon │
 │ of LSASS access  ││ Event ID 10 ...  │
 └──────────────────┘└──────────────────┘
        ▲ sentence is cut here ▲
        key fact split across two chunks!
```

---

## Concept: Overlap Chunking

Add overlap between chunks so that facts near boundaries appear in at least two chunks:

```python
def chunk_overlap(text, chunk_size=100, overlap=20):
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks
```

```
Overlap Chunking — boundary facts preserved
──────────────────────────────────────────────────────
 chunk_size=100, overlap=20

 ┌──────── Chunk 1 (words 1-100) ────────┐
 │ ... detection of LSASS access         │
 │      relies on Sysmon Event ID 10 ... │
 └───────────────────────┬───────────────┘
                         │ overlap zone
 ┌───────────────────────┼───────────────┐
 │ ... relies on Sysmon  │Event ID 10    │
 │      for detecting... │               │
 └──────── Chunk 2 (words 81-180) ───────┘
            ▲
   words 81-100 appear in BOTH chunks
```

---

## Concept: Sentence-Based Chunking

Split by sentence boundaries (periods, exclamation marks, question marks):

```python
import re

def chunk_sentences(text, sentences_per_chunk=3):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk:
            chunks.append(chunk)
    return chunks
```

Preserves sentence boundaries but produces variable-length chunks.

---

## What Each Task Asks You to Do

### Task 1 — Fixed-size chunking
Implement `chunk_fixed(text, chunk_size=50)`. Apply to a sample document. Print the number of chunks and the first 2 chunks.

### Task 2 — Overlap chunking
Implement `chunk_overlap(text, chunk_size=50, overlap=10)`. Compare to fixed-size: do you get more chunks? Do boundary chunks preserve more meaning?

### Task 3 — Sentence-based chunking
Implement `chunk_sentences(text, sentences_per_chunk=2)`. Print all chunks. Count how many you get.

### Task 4 — Compare strategies (Bonus)
For a query "how to detect mimikatz", show which chunk from each strategy is most likely to be retrieved (highest keyword overlap). Print the best chunk from each method.

---

## Now Open the Lab

[01_lab_chunking.md](01_lab_chunking.md)
## Next

[02_guide_retrieval.md](02_guide_retrieval.md) — encode chunks and retrieve the most relevant ones for a query.
