# Lab — Exercise 1: Document Chunking

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `01_chunking.py` in this folder.

> No API key or external libraries required — this exercise uses only the Python standard library.

---

## Step 2: Add the imports and document

`re` is needed for sentence-boundary splitting in Task 3. The sample document is a short security article about Mimikatz — long enough to demonstrate three different chunking strategies.

```python
import re

DOCUMENT = """
Mimikatz is a credential dumping tool that extracts plaintext passwords and NTLM hashes
from Windows LSASS memory. It was created by Benjamin Delpy and is used by both red teams
and threat actors. Common techniques include sekurlsa::logonpasswords for plaintext creds,
lsadump::dcsync for domain replication, and kerberos::golden for Golden Ticket attacks.

Detection relies on monitoring LSASS memory access by non-system processes using Sysmon
Event ID 10. Unexpected access to lsass.exe from tools like procdump, taskmgr, or
unsigned binaries should trigger high-severity alerts.

Mitigations include enabling Windows Credential Guard, disabling WDigest authentication,
placing high-value accounts in the Protected Users group, and enabling LSA Protection.
For active directory environments, enable audit policies for privilege use and account
management, and baseline normal dcsync behaviour to detect unauthorized replication.
""".strip()
```

---

## Step 3: Fixed-size chunking

Fixed-size chunking splits the text into equal slices of N words. The minimum length check (10 words) drops any tiny fragment at the end.

Add this to your file:

```python
def chunk_fixed(text, chunk_size=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks

fixed_chunks = chunk_fixed(DOCUMENT, chunk_size=50)
print(f"Fixed-size chunks (size=50): {len(fixed_chunks)} chunks")
for i, chunk in enumerate(fixed_chunks[:2], 1):
    print(f"  Chunk {i}: {chunk[:120]}...")
```

Run your file. You should see:
```
Fixed-size chunks (size=50): 4 chunks
  Chunk 1: Mimikatz is a credential dumping tool that extracts plaintext passwords and NTLM hashes from Windows LSASS memory...
  Chunk 2: Detection relies on monitoring LSASS memory access by non-system processes using Sysmon Event ID 10. Unexpected...
```

---

## Step 4: Overlap chunking

Overlap chunking uses a step smaller than the chunk size so that words near chunk boundaries appear in two consecutive chunks. This prevents important facts from being split and lost. With `chunk_size=50` and `overlap=15`, the step is 35.

Add this to your file:

```python
def chunk_overlap(text, chunk_size=50, overlap=15):
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks

overlap_chunks = chunk_overlap(DOCUMENT, chunk_size=50, overlap=15)
print(f"\nOverlap chunks (size=50, overlap=15): {len(overlap_chunks)} chunks")
for i, chunk in enumerate(overlap_chunks[:2], 1):
    print(f"  Chunk {i}: {chunk[:120]}...")
```

Run your file. You should see more chunks than fixed-size because the step is smaller:
```
Overlap chunks (size=50, overlap=15): 6 chunks
  Chunk 1: Mimikatz is a credential dumping tool that extracts plaintext passwords and NTLM hashes...
  Chunk 2: lsadump::dcsync for domain replication, and kerberos::golden for Golden Ticket attacks...
```

---

## Step 5: Sentence-based chunking

Sentence-based chunking splits on sentence boundaries (period/exclamation/question mark) so complete sentences always stay together. The chunks are variable-length but semantically cleaner.

Add this to your file:

```python
def chunk_sentences(text, sentences_per_chunk=2):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk:
            chunks.append(chunk)
    return chunks

sentence_chunks = chunk_sentences(DOCUMENT, sentences_per_chunk=2)
print(f"\nSentence chunks (2 per chunk): {len(sentence_chunks)} chunks")
for i, chunk in enumerate(sentence_chunks, 1):
    print(f"  Chunk {i}: {chunk}")
```

Run your file. Each chunk should contain exactly 2 complete sentences and no sentence should be cut mid-way.

---

## Step 6: Compare strategies for a query (Bonus Task 4)

Simple keyword overlap counts how many query words appear in each chunk. This is a rough proxy for relevance — the chunk with the highest overlap is likely the best match for that query.

Add this to your file:

```python
query = "how to detect mimikatz LSASS"
query_words = set(query.lower().split())

strategies = {
    "fixed":    fixed_chunks,
    "overlap":  overlap_chunks,
    "sentence": sentence_chunks,
}

print(f"\nQuery: '{query}'")
print("Best matching chunk per strategy:")
for name, chunks in strategies.items():
    scored = [(sum(1 for w in query_words if w in c.lower()), c) for c in chunks]
    best_score, best_chunk = max(scored, key=lambda x: x[0])
    print(f"\n  [{name}] score={best_score}")
    print(f"  {best_chunk[:150]}...")

print("\n--- Exercise 1 complete. Move to 02_retrieval.py ---")
```

Run your file. The detection-focused chunk should score highest across all three strategies.

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_chunking.py`) if anything looks different.
