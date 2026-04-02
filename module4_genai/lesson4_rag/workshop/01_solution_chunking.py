# Exercise 1 — Document Chunking
#
# Demonstrates three chunking strategies: fixed-size, overlap, and
# sentence-based. Compares how each handles a security document.
# No API key or external libraries required — standard library only.

import re


# ============================================================
#   Sample Security Document
# ============================================================

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


# ============================================================
#   TASK 1: Fixed-size chunking
# ============================================================
print("=" * 60)
print("  TASK 1: Fixed-Size Chunking")
print("=" * 60)

# Splits text into equal slices of N words.
# Drops any tiny fragment (< 10 words) at the end.
def chunk_fixed(text, chunk_size=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks

fixed_chunks = chunk_fixed(DOCUMENT, chunk_size=50)
print(f"\nFixed-size chunks (size=50): {len(fixed_chunks)} chunks")
for i, chunk in enumerate(fixed_chunks[:2], 1):
    print(f"  Chunk {i}: {chunk[:120]}...")


# ============================================================
#   TASK 2: Overlap chunking
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Overlap Chunking")
print("=" * 60)

# Uses a step smaller than chunk_size so words near boundaries
# appear in two consecutive chunks. Prevents facts from being
# split across chunks and lost.
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


# ============================================================
#   TASK 3: Sentence-based chunking
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Sentence-Based Chunking")
print("=" * 60)

# Splits on sentence boundaries so complete sentences stay
# together. Chunks are variable-length but semantically cleaner.
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


# ============================================================
#   TASK 4 (Bonus): Compare strategies for a query
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Compare Strategies")
print("=" * 60)

# Simple keyword overlap counts how many query words appear
# in each chunk — a rough proxy for relevance.
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

print("\n--- Exercise 1 complete. Move to 02_solution_retrieval.py ---")
