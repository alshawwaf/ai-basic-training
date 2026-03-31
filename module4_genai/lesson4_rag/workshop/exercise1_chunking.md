# Exercise 1 — Document Chunking

> **Exercise file:** [exercise1_chunking.py](exercise1_chunking.py)
> Read this guide fully before opening the exercise file.

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

## Expected Outputs at a Glance

**Task 1**
```
Fixed-size chunks (size=50): 4 chunks
  Chunk 1: Extracts plaintext passwords and NTLM hashes from Windows LSASS memory.
            Techniques: sekurlsa::logonpasswords, lsadump::dcsync, Golden Ticket attacks.
            Detection: LSASS memory access by...
  Chunk 2: ...non-system processes (Sysmon Event 10).
            Mitigations: Credential Guard, disable WDigest...
```

---

## Now Open the Exercise File

[exercise1_chunking.py](exercise1_chunking.py)

---

## Next

[exercise2_retrieval.md](exercise2_retrieval.md) — encode chunks and retrieve the most relevant ones for a query.
