# Demo Kit — Security Analyst Assistant
#
# A customer-facing RAG demo that loads all .md files from the corpus.
#
# Setup:
#   pip install sentence-transformers numpy
#   Set ONE API key: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY
#   Or use Ollama: set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B
#
# Run:
#   python demo_assistant.py              (scripted demo — 4 pre-built queries)
#   python demo_assistant.py --interactive (open Q&A with the audience)

import os
import sys
import glob
import numpy as np
from typing import List, Dict
from pathlib import Path

# Add parent so we can import llm_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "stage4_genai"))
from llm_client import get_client

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "stage4_genai", "data")


# ── Document Loader ──────────────────────────────────────────────────────────
def load_corpus(data_dir: str) -> Dict[str, str]:
    """Load all .md files from the data directory into a dict of {name: content}."""
    docs = {}
    for filepath in sorted(glob.glob(os.path.join(data_dir, "*.md"))):
        name = Path(filepath).stem.replace("_", " ").title()
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if content.strip():
            docs[name] = content
    return docs


# ── RAG Engine ───────────────────────────────────────────────────────────────
class RAGEngine:
    def __init__(self, docs: Dict[str, str], chunk_size: int = 200, overlap: int = 50):
        self.chunks: List[str] = []
        self.sources: List[str] = []
        for name, text in docs.items():
            words = text.split()
            for i in range(0, len(words), chunk_size - overlap):
                chunk = " ".join(words[i : i + chunk_size])
                if len(chunk.split()) > 30:
                    self.chunks.append(chunk)
                    self.sources.append(name)
        self._build_index()

    def _build_index(self):
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._embeddings = self._model.encode(self.chunks, show_progress_bar=False)
            self._embed = lambda t: self._model.encode([t])[0]
            print(f"  Indexed {len(self.chunks)} chunks from {len(set(self.sources))} documents (sentence-transformers)\n")
        except ImportError:
            from sklearn.feature_extraction.text import TfidfVectorizer

            self._tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self._embeddings = self._tfidf.fit_transform(self.chunks).toarray()
            self._embed = lambda t: self._tfidf.transform([t]).toarray()[0]
            print(f"  Indexed {len(self.chunks)} chunks from {len(set(self.sources))} documents (TF-IDF fallback)\n")

    def retrieve(self, query: str, k: int = 4) -> List[Dict]:
        q = self._embed(query)
        scores = [
            np.dot(q, e) / (np.linalg.norm(q) * np.linalg.norm(e) + 1e-8)
            for e in self._embeddings
        ]
        top = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
        return [
            {"text": self.chunks[i], "source": self.sources[i], "score": s}
            for i, s in top
            if s > 0.05
        ]


# ── Assistant ────────────────────────────────────────────────────────────────
class SecurityAssistant:
    SYSTEM = """You are an expert cybersecurity analyst assistant.
Answer questions ONLY based on the provided context documents.
If the information is not in the context, say "I don't have enough context to answer that question" — do not hallucinate.
Format answers clearly with bullet points where appropriate.
Always cite which document your answer comes from."""

    def __init__(self, data_dir: str = DATA_DIR):
        print("=" * 65)
        print("  SECURITY ANALYST ASSISTANT — DEMO KIT")
        print("=" * 65)
        print(f"\n  Loading corpus from: {os.path.abspath(data_dir)}")
        docs = load_corpus(data_dir)
        if not docs:
            print(f"  ERROR: No .md files found in {data_dir}")
            sys.exit(1)
        print(f"  Found {len(docs)} documents")
        self.rag = RAGEngine(docs)
        self.provider, self.client = get_client()
        self.history: List[Dict] = []

    def ask(self, question: str) -> str:
        retrieved = self.rag.retrieve(question, k=4)

        if not retrieved:
            return "I don't have enough context in the knowledge base to answer that question."

        context = "\n\n".join(
            [f"[Source: {r['source']}]\n{r['text']}" for r in retrieved]
        )
        sources = sorted(set(r["source"] for r in retrieved))

        user_msg = f"Context:\n{context}\n\nQuestion: {question}"
        self.history.append({"role": "user", "content": user_msg})

        if self.client is None:
            answer = (
                f"[No API key — showing retrieval results]\n\n"
                f"Sources: {', '.join(sources)}\n\n"
                f"Top match (score {retrieved[0]['score']:.3f}):\n"
                f"{retrieved[0]['text'][:300]}..."
            )
        else:
            answer = self.client.chat(
                system=self.SYSTEM,
                messages=self.history[-6:],
                max_tokens=600,
            )

        self.history.append({"role": "assistant", "content": answer})

        print(f"\n  Sources: {', '.join(sources)}")
        return answer


# ── Demo Mode ────────────────────────────────────────────────────────────────
def run_demo(assistant: SecurityAssistant):
    queries = [
        ("CVE Deep Dive", "What is Log4Shell and how do I detect if it was exploited on my servers?"),
        ("Incident Response", "Our SOC received a phishing email with a suspicious attachment. Walk me through the first 30 minutes of response."),
        ("Threat Intelligence", "What techniques does APT29 use for initial access and lateral movement?"),
        ("Out of Scope", "How do I configure a Palo Alto firewall to block SQL injection attacks?"),
    ]
    for label, q in queries:
        print(f"\n{'─' * 65}")
        print(f"  [{label}]")
        print(f"  Q: {q}")
        print(f"\n  A: {assistant.ask(q)}")

    print(f"\n{'─' * 65}")
    print("\n  Demo complete. The 4th query demonstrates grounding —")
    print("  the assistant correctly declines when context isn't available.\n")


# ── Interactive Mode ─────────────────────────────────────────────────────────
def run_interactive(assistant: SecurityAssistant):
    print(f"\n  Interactive mode (provider: {assistant.provider})")
    print("  Type your questions. Commands: /quit to exit\n")
    while True:
        try:
            question = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question.lower() in ("/quit", "exit", "quit"):
            break
        print(f"\n  Assistant: {assistant.ask(question)}\n")


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    assistant = SecurityAssistant()

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive(assistant)
    else:
        run_demo(assistant)
        print("=" * 65)
        print("  To run interactively:  python demo_assistant.py --interactive")
        print("  To add documents:      drop .md files into stage4_genai/data/")
        print("=" * 65)
