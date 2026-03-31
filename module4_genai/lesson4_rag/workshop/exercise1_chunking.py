# =============================================================================
# LESSON 4.4 | WORKSHOP | Exercise 1 of 3
# Document Chunking
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - Why documents must be split before embedding (context window limits)
# - Three strategies: fixed-size, overlap, sentence-based
# - How chunk size affects the quality of later retrieval
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson4_rag/workshop/exercise1_chunking.py
#
# No API key required — this exercise uses only Python standard library.
# =============================================================================

import re

# Sample security document to chunk
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

# =============================================================================
# BACKGROUND
# =============================================================================
# Embedding models have a max token limit (usually 256–512 tokens).
# Long documents must be split into chunks before encoding.
#
# Chunk size tradeoffs:
#   Large chunks → more context, but embeddings average too much content
#   Small chunks → more precise retrieval, but may lose cross-sentence meaning
#   With overlap → boundaries are preserved at the cost of redundancy

# =============================================================================
# TASK 1 — Fixed-size chunking
# =============================================================================
# Implement: chunk_fixed(text, chunk_size=50) -> list[str]
#   - words = text.split()
#   - Step through words in steps of chunk_size
#   - Join each slice with " "
#   - Skip chunks with fewer than 10 words (trailing fragments)
#
# Apply chunk_fixed(DOCUMENT, chunk_size=50).
# Print: "Fixed-size chunks (size=50): N chunks"
# Print the text of chunks 1 and 2 (first 120 chars each + "...")
#
# EXPECTED OUTPUT (approximate):
#   Fixed-size chunks (size=50): 4 chunks
#   Chunk 1: Mimikatz is a credential dumping tool that extracts plaintext passwords...
#   Chunk 2: Detection relies on monitoring LSASS memory access by non-system processes...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Overlap chunking
# =============================================================================
# Implement: chunk_overlap(text, chunk_size=50, overlap=15) -> list[str]
#   - step = chunk_size - overlap
#   - Step through words in steps of `step`
#   - Each chunk is words[i : i + chunk_size]
#   - Skip chunks with fewer than 10 words
#
# Apply chunk_overlap(DOCUMENT, chunk_size=50, overlap=15).
# Print: "Overlap chunks (size=50, overlap=15): N chunks"
# Print chunk 1 and chunk 2 (first 120 chars each).
#
# Notice: more chunks than fixed-size (because of overlap), but boundary information
# appears in two consecutive chunks rather than being split between them.
#
# EXPECTED OUTPUT (approximate):
#   Overlap chunks (size=50, overlap=15): 6 chunks
#   Chunk 1: Mimikatz is a credential dumping tool...
#   Chunk 2: lsadump::dcsync for domain replication, and kerberos::golden for Golden...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Sentence-based chunking
# =============================================================================
# Implement: chunk_sentences(text, sentences_per_chunk=2) -> list[str]
#   - Split text into sentences: re.split(r'(?<=[.!?])\s+', text.strip())
#   - Group every `sentences_per_chunk` sentences together
#   - Skip empty chunks
#
# Apply chunk_sentences(DOCUMENT, sentences_per_chunk=2).
# Print: "Sentence chunks (2 per chunk): N chunks"
# Print ALL chunks (they should be short enough to fit on screen).
#
# Notice: variable-length chunks, but complete sentences always stay together.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Compare strategies (BONUS)
# =============================================================================
# For the query "how to detect mimikatz LSASS",
# find the best matching chunk from each strategy using simple word overlap:
#   score = number of query words found in chunk (case-insensitive)
#
# Print the best chunk from each strategy and its overlap score.
# Which strategy preserves the detection information most completely?

# >>> YOUR CODE HERE


print("\n--- Exercise 1 complete. Move to exercise2_retrieval.py ---")
