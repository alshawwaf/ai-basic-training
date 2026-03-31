# Lesson 4.1 — How LLMs Work: Tokens and Embeddings
#
# This script demonstrates the fundamental building blocks of LLMs:
#   - Tokenisation: how text becomes numbers
#   - Embeddings: how meaning is represented as vectors
#   - Semantic similarity: why "malware" and "ransomware" are close in vector space
#
# No heavy GPU required — we use lightweight models and manual demos.
# pip install transformers sentence-transformers

import numpy as np
import matplotlib.pyplot as plt

# ── 1. Tokenisation demo (no model needed) ─────────────────────────────────────
print("=" * 60)
print("  PART 1: TOKENISATION")
print("=" * 60)

# Simple character-level tokenisation to build intuition
def simple_tokenise(text):
    """Not how real LLMs work, but shows the concept"""
    # Real tokenisers (BPE, WordPiece) use subword units
    return text.split()

security_sentences = [
    "The malware exfiltrated credentials via DNS tunneling",
    "CVE-2024-12345 allows remote code execution",
    "The threat actor used a spear phishing email",
    "Ransomware encrypted 10000 files in 3 seconds",
]

print("\nWord-level tokenisation (simplified):")
for s in security_sentences:
    tokens = simple_tokenise(s)
    print(f"  '{s[:50]}...'")
    print(f"  → {len(tokens)} tokens: {tokens}")

# BPE-style approximation — show subword tokenisation
print("\n\nSubword tokenisation (closer to how GPT/Claude works):")
examples = {
    "cybersecurity":    ["cyber", "security"],
    "CVE-2024-1234":    ["CVE", "-", "2024", "-", "1234"],
    "malware":          ["mal", "ware"],
    "exfiltration":     ["ex", "fil", "tration"],
    "SQL injection":    ["SQL", " injection"],
    "zero-day":         ["zero", "-", "day"],
    "EICAR test file":  ["E", "ICAR", " test", " file"],
}

for word, tokens in examples.items():
    cost = f"~{len(tokens)} tokens = ~${len(tokens) * 0.000003:.7f} per million calls"
    print(f"  '{word}' → {tokens}  ({cost})")

print("\n Key point: API cost = token count. Long prompts with CVE lists are expensive.")

# ── 2. Embeddings demo ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  PART 2: EMBEDDINGS")
print("=" * 60)

# Manual embedding demo — simplified to show the concept
# Real embeddings are learned from data; these are hand-crafted for illustration
security_concepts = {
    # Each concept represented by: [threat_level, network_related, file_related, auth_related]
    "malware":          [0.9, 0.3, 0.8, 0.1],
    "ransomware":       [0.95, 0.2, 0.9, 0.1],
    "spyware":          [0.8, 0.5, 0.6, 0.2],
    "phishing":         [0.85, 0.6, 0.2, 0.7],
    "credential dump":  [0.9, 0.3, 0.4, 0.9],
    "port scan":        [0.4, 0.95, 0.0, 0.1],
    "SQL injection":    [0.8, 0.8, 0.1, 0.3],
    "firewall rule":    [0.1, 0.9, 0.0, 0.2],
    "access log":       [0.1, 0.4, 0.5, 0.4],
    "pizza delivery":   [0.0, 0.1, 0.0, 0.0],   # unrelated concept
}

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

print("\nCosine similarity matrix (1.0 = identical, 0.0 = unrelated):")
concepts = list(security_concepts.keys())
vectors  = list(security_concepts.values())

# Show similarities to "malware"
print(f"\nSimilarity to 'malware':")
malware_vec = security_concepts['malware']
for concept, vec in security_concepts.items():
    sim = cosine_similarity(malware_vec, vec)
    bar = '█' * int(sim * 20)
    print(f"  {concept:<20} {sim:.3f} {bar}")

# ── 3. Real embeddings with sentence-transformers ─────────────────────────────
print("\n" + "=" * 60)
print("  PART 3: REAL EMBEDDINGS (sentence-transformers)")
print("=" * 60)

try:
    from sentence_transformers import SentenceTransformer

    print("Loading model (downloads ~90MB on first run)...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')

    security_phrases = [
        "CVE remote code execution vulnerability",
        "buffer overflow exploit allows privilege escalation",
        "cross-site scripting XSS attack injects JavaScript",
        "SQL injection bypasses authentication",
        "ransomware encrypts files and demands payment",
        "phishing email tricks user into entering password",
        "firewall blocks unauthorised inbound connections",
        "the weather is nice today",   # unrelated
    ]

    embeddings = embed_model.encode(security_phrases)
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(f"Each phrase → {embeddings.shape[1]}-dimensional vector")

    # Similarity between first phrase and all others
    ref = embeddings[0]
    print(f"\nSimilarity to: '{security_phrases[0]}'")
    for i, phrase in enumerate(security_phrases):
        sim = cosine_similarity(ref, embeddings[i])
        bar = '█' * int(sim * 30)
        print(f"  {sim:.3f} {bar} {phrase[:60]}")

    # ── Plot 2D visualisation with PCA ────────────────────────────────────────
    from sklearn.decomposition import PCA

    pca   = PCA(n_components=2)
    coords = pca.fit_transform(embeddings)

    plt.figure(figsize=(10, 7))
    for i, (phrase, coord) in enumerate(zip(security_phrases, coords)):
        color = 'red' if 'weather' in phrase else 'steelblue'
        plt.scatter(*coord, color=color, s=80, zorder=5)
        plt.annotate(phrase[:40], coord, fontsize=8, ha='center',
                     xytext=(0, 8), textcoords='offset points')
    plt.title('Security Phrase Embeddings in 2D (PCA)\nRed = unrelated topic')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.tight_layout()
    plt.savefig('module4_genai/lesson1_embeddings.png')
    plt.show()
    print("\nPlot saved to module4_genai/lesson1_embeddings.png")

except ImportError:
    print("sentence-transformers not installed.")
    print("Run: pip install sentence-transformers")
    print("Skipping real embedding demo — the conceptual demo above still applies.")

# ── 4. Context window demo ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  PART 4: CONTEXT WINDOWS")
print("=" * 60)
print("""
An LLM can only 'see' a limited number of tokens at once.

  Claude 3.5: 200,000 tokens  ≈ 150,000 words  ≈ 600 pages
  GPT-4o:     128,000 tokens  ≈ 100,000 words  ≈ 400 pages

For security log analysis:
  - 10,000 firewall log lines ≈ 200,000 tokens (fills Claude's context)
  - A full week of logs: won't fit → need RAG (Lesson 4.4)

Practical rule: chunk large documents into ~500-token pieces,
embed each chunk, and retrieve only the relevant chunks.
This is what we build in Lesson 4.4.
""")
