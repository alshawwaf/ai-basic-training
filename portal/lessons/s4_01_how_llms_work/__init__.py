"""
Lesson 4.1 — How LLMs Work
Flask Blueprint — interactive exploration of tokenisation, embeddings, and attention.
All computation is client-side (JavaScript) — no heavy ML dependencies.
"""

import numpy as np
from flask import Blueprint, render_template, jsonify

bp = Blueprint(
    "s4_01",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s4_01"
LESSON_TITLE = "How LLMs Work"

# ── Toy vocabulary (20 security-themed tokens) ────────────────────────────

WORDS = [
    "<UNK>", "the", "network", "connection", "is", "suspicious",
    "malicious", "benign", "port", "scan", "firewall",
    "blocked", "allowed", "traffic", "alert", "endpoint",
    "detected", "attack", "normal", "<EOS>",
]
VOCAB = {w: i for i, w in enumerate(WORDS)}

# ── Embedding matrix (20 tokens x 4 dims) ────────────────────────────────
# dim 0 ~ threat level, dim 1 ~ network-related, dim 2 ~ action/state, dim 3 ~ detection

EMBEDDING_MATRIX = [
    [ 0.00,  0.00,  0.00,  0.00],   #  0: <UNK>
    [ 0.01,  0.01,  0.01,  0.01],   #  1: the
    [ 0.20,  0.90,  0.10,  0.30],   #  2: network
    [ 0.15,  0.85,  0.20,  0.20],   #  3: connection
    [ 0.00,  0.00,  0.00,  0.00],   #  4: is
    [ 0.85,  0.30, -0.40,  0.70],   #  5: suspicious
    [ 0.90,  0.25, -0.50,  0.65],   #  6: malicious
    [-0.70,  0.10,  0.60, -0.30],   #  7: benign
    [ 0.10,  0.80,  0.30,  0.20],   #  8: port
    [ 0.40,  0.70,  0.50,  0.60],   #  9: scan
    [ 0.05,  0.85, -0.20,  0.40],   # 10: firewall
    [ 0.10,  0.50, -0.60,  0.30],   # 11: blocked
    [-0.10,  0.50,  0.60, -0.10],   # 12: allowed
    [ 0.15,  0.80,  0.10,  0.25],   # 13: traffic
    [ 0.60,  0.40,  0.20,  0.85],   # 14: alert
    [ 0.30,  0.50,  0.10,  0.50],   # 15: endpoint
    [ 0.50,  0.30,  0.40,  0.80],   # 16: detected
    [ 0.95,  0.40, -0.30,  0.50],   # 17: attack
    [-0.50,  0.20,  0.50, -0.20],   # 18: normal
    [ 0.00,  0.00,  0.00,  0.00],   # 19: <EOS>
]

# Pre-compute cosine similarity matrix
emb = np.array(EMBEDDING_MATRIX, dtype=np.float32)
norms = np.linalg.norm(emb, axis=1, keepdims=True)
norms[norms == 0] = 1e-8
normed = emb / norms
SIM_MATRIX = (normed @ normed.T).tolist()

# ── Attention example ─────────────────────────────────────────────────────

ATTENTION_SENTENCE = ["the", "firewall", "blocked", "malicious", "connection"]
ATTENTION_WEIGHTS = [
    [0.80, 0.10, 0.05, 0.03, 0.02],
    [0.15, 0.65, 0.10, 0.05, 0.05],
    [0.03, 0.45, 0.00, 0.28, 0.24],
    [0.02, 0.08, 0.12, 0.70, 0.08],
    [0.04, 0.12, 0.30, 0.25, 0.29],
]

# ── Step metadata ─────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "Next-Token Prediction", "sub": "The core idea behind every LLM",       "icon": "next-token"},
    {"id": 1, "title": "Tokenisation",          "sub": "Text to numbers",                      "icon": "tokenize"},
    {"id": 2, "title": "Vocabulary Limits",      "sub": "When words go missing",                "icon": "vocab-question"},
    {"id": 3, "title": "Embeddings",             "sub": "Words as vectors",                     "icon": "embedding-vector"},
    {"id": 4, "title": "Cosine Similarity",      "sub": "Measuring meaning",                    "icon": "cosine-angle"},
    {"id": 5, "title": "Attention",              "sub": "Which words matter to which",          "icon": "attention-arrows"},
    {"id": 6, "title": "Context Vectors",        "sub": "Attention in action",                  "icon": "context-vector"},
    {"id": 7, "title": "Pretraining",            "sub": "How the weights get made",             "icon": "loss-curve"},
    {"id": 8, "title": "LLMs vs Classic ML",     "sub": "Different tools, different problems", "icon": "llm-vs-ml"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "What is the fundamental task that every modern Large Language Model is trained to do?",
        "options": [
            "Translate between languages",
            "Predict the next token given the previous tokens",
            "Detect malware in files",
            "Answer questions in a chatbot",
        ],
        "answer": 1,
        "explanation": "<strong>Next-token prediction</strong> is the entire game. Everything else &mdash; chat, code, summarisation &mdash; emerges from doing this one task incredibly well across trillions of tokens. The 'chat' interface is built on top: feed in the conversation so far, ask the model for the next token, repeat.",
    },
    {
        "q": "Why is text like <code>CVE-2024-1234</code> or an IP address often <strong>token-expensive</strong> for LLMs?",
        "options": [
            "Numbers cost more than letters",
            "Real BPE tokenisers split unfamiliar IDs/hashes into many subword tokens, so security text consumes more context window and costs more per API call",
            "Special characters are blocked",
            "LLMs refuse to process them",
        ],
        "answer": 1,
        "explanation": "Common English words map to single tokens, but rare/structured strings like <code>CVE-2024-1234</code>, <code>SHA256</code> hashes, IPs, and registry paths get split into 5-10 subword tokens. <strong>Security text is token-heavy</strong> &mdash; budget for it when processing logs through LLMs.",
    },
    {
        "q": "What does an <strong>embedding</strong> represent?",
        "options": [
            "The compressed file size of a word",
            "A dense vector of numbers that captures the semantic meaning of a token, so semantically similar words have similar vectors",
            "The hash of a word",
            "A pointer to the word in a database",
        ],
        "answer": 1,
        "explanation": "An embedding is a fixed-length vector (e.g. 768 or 4096 numbers) that encodes the meaning of a token. Words with similar meanings end up with similar vectors. This is what lets cosine similarity tell you that 'malicious' and 'suspicious' are related &mdash; the model learned it from context.",
    },
    {
        "q": "When the model processes the word 'blocked' in 'the firewall blocked malicious connection', it pays more attention to 'firewall' (0.45) and 'malicious' (0.28) than to 'the' (0.03). Why?",
        "options": [
            "It's a bug in the attention mechanism",
            "Attention learns to focus on <em>informative</em> tokens and ignore noise; 'the' carries no semantic information, but 'firewall' and 'malicious' tell the model who acted and what kind of thing was acted on",
            "Longer words always get more attention",
            "Attention always focuses on the first word",
        ],
        "answer": 1,
        "explanation": "<strong>Attention</strong> is the mechanism that lets each token decide which other tokens matter for understanding it. Function words like 'the' carry almost no signal; content words like 'firewall' and 'malicious' do. This is the core innovation that made Transformers so powerful.",
    },
    {
        "q": "Why is LLM pretraining called <strong>self-supervised</strong> &mdash; what makes it different from a normal supervised learning setup?",
        "options": [
            "It runs without any training data",
            "Humans label only 1% of the corpus and the model figures out the rest",
            "The label for each example is already inside the source text &mdash; the model is trained to predict the next token, and the next token is just the word that comes next in the sentence (no human labelling needed)",
            "The model supervises itself by checking its own answers against an oracle",
        ],
        "answer": 2,
        "explanation": "Pretraining turns every position in every sentence into a free training example. The input is everything before the cut, and the label is the actual next token in the source text &mdash; <strong>no human ever wrote a label</strong>. That is why a 1 trillion-token corpus produces ~1 trillion training examples without any annotation cost.",
    },
    {
        "q": "Your team has 5,000 labelled firewall logs and wants to classify them as malicious or benign. Should you use an LLM or classic ML?",
        "options": [
            "LLM &mdash; LLMs are better at everything",
            "Classic ML (Random Forest, LogReg) &mdash; structured tabular data with labels is exactly what classic ML excels at; using GPT-4 for CSV classification is absurdly expensive and slower",
            "Neither &mdash; that task is impossible",
            "Both, then average them",
        ],
        "answer": 1,
        "explanation": "LLMs are for <strong>unstructured text</strong> tasks where you need understanding of natural language. For tabular structured data with labels, classic ML is faster, cheaper, more interpretable, and usually more accurate. Right tool, right job.",
    },
]


CHALLENGES = {
    0: {
        "q": "Type 'The attacker used' and look at the predictions. Now type 'The chef used'. How do predictions change?",
        "a": "The model predicts different next tokens based on context. 'attacker used' suggests security terms (exploit, malware), while 'chef used' suggests cooking terms (knife, oven). This is <strong>contextual prediction</strong> — the same word 'used' leads to different outputs depending on surrounding words.",
    },
    1: {
        "q": "Encode 'CVE-2024-1234'. How many tokens does it become? Why is this expensive?",
        "a": "With a word-level tokenizer, 'CVE-2024-1234' is a single unknown token (&lt;UNK&gt;). Real BPE tokenizers split it into ~5 tokens: 'CVE', '-', '2024', '-', '1234'. More tokens = higher API cost and more context window consumed. <strong>Security text is token-expensive</strong> because of IDs, hashes, and IPs.",
    },
    2: {
        "q": "With the 20-word vocabulary, encode 'the ransomware encrypted all files'. How many words survive?",
        "a": "Only 'the' survives — 'ransomware', 'encrypted', 'all', 'files' all become &lt;UNK&gt;. <strong>4 out of 5 words lost!</strong> This is why real LLMs need 100,000+ tokens. With BPE, even rare words get broken into known subwords.",
    },
    3: {
        "q": "Look at the embedding for 'malicious' vs 'benign'. They're about the same topic (security) but have very different vectors. Why?",
        "a": "Their vectors point in <strong>opposite directions</strong> — 'malicious' has high threat level, 'benign' has negative threat level. Embeddings capture semantic relationships, and <strong>antonyms are opposite vectors</strong>, not similar ones. The model knows they're related but opposite.",
    },
    4: {
        "q": "Which pair has the highest similarity? Which has the lowest? Does this match your security intuition?",
        "a": "Highest: <strong>malicious ↔ suspicious</strong> (both threat indicators). Lowest: <strong>malicious ↔ benign</strong> (semantic opposites). This matches perfectly — a security analyst would group the same way. Embeddings learn the relationships humans intuitively know.",
    },
    5: {
        "q": "When processing 'blocked', the model attends to 'firewall' (0.45) and 'malicious' (0.28). Why not 'the' (0.03)?",
        "a": "'the' carries almost no semantic information — it's a function word. 'firewall' tells the model <strong>who</strong> blocked and 'malicious' tells it <strong>what kind</strong> of thing was blocked. Attention learns to focus on <strong>informative tokens</strong> and ignore noise.",
    },
    6: {
        "q": "The context vector for 'blocked' is a weighted mix of all word vectors. What would happen if all attention weights were equal (0.20 each)?",
        "a": "The context vector would be a simple <strong>average</strong> of all word vectors — treating 'the' as equally important as 'firewall'. This is what bag-of-words models do. Attention is better because it <strong>selectively focuses</strong> on the relevant words.",
    },
    7: {
        "q": "Drag the slider from 0 to 1 trillion tokens. The architecture never changes — only the values of the weights. So where do reasoning, world knowledge, and coding ability actually come from?",
        "a": "They are <strong>emergent side-effects</strong> of getting good at one thing: predicting the next token. To predict the next token <em>well</em>, the model has to implicitly know who Marie Curie was, what TCP port 443 is for, and how a SQL injection works — because all of those facts shaped the next-token statistics in the training corpus. Nothing was explicitly programmed in. The weights just slowly absorbed the structure of human language across trillions of nudges.",
    },
    8: {
        "q": "Your team has 5,000 labelled firewall logs and wants to build a classifier. Should they use an LLM or classic ML?",
        "a": "<strong>Classic ML</strong> (Random Forest, LogReg). Structured tabular data with labels is exactly what classic ML excels at. LLMs are for unstructured text. Using GPT-4 to classify CSV rows is like using a helicopter to cross the street — technically possible, absurdly expensive.",
    },
}


# ── Course materials mapping ────────────────────────────────────────────────

_base = "curriculum/stage4_genai/01_how_llms_work"

MATERIALS = {
    0: [("lecture", "Next-Token Prediction", f"{_base}/0_next_token_prediction/lecture.md")],
    1: [("lecture", "Tokenisation", f"{_base}/1_tokenisation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_tokenisation/handson.md"),
        ("solution", "Solution", f"{_base}/1_tokenisation/solution_tokenisation.py")],
    2: [("lecture", "Tokenisation", f"{_base}/1_tokenisation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_tokenisation/handson.md"),
        ("solution", "Solution", f"{_base}/1_tokenisation/solution_tokenisation.py")],
    3: [("lecture", "Embeddings", f"{_base}/2_embeddings/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_embeddings/handson.md"),
        ("solution", "Solution", f"{_base}/2_embeddings/solution_embeddings.py")],
    4: [("lecture", "Embeddings", f"{_base}/2_embeddings/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_embeddings/handson.md"),
        ("solution", "Solution", f"{_base}/2_embeddings/solution_embeddings.py")],
    5: [("lecture", "Attention", f"{_base}/3_attention/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_attention/handson.md"),
        ("solution", "Solution", f"{_base}/3_attention/solution_attention.py")],
    6: [("lecture", "Attention", f"{_base}/3_attention/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_attention/handson.md"),
        ("solution", "Solution", f"{_base}/3_attention/solution_attention.py")],
    7: [("lecture", "Pretraining", f"{_base}/4_pretraining/lecture.md")],
    8: [("lecture", "LLMs vs Classic ML", f"{_base}/5_llms_vs_classic_ml/lecture.md")],
}


def base_ctx(step_num):
    return {
        "steps": STEPS,
        "current": step_num,
        "challenge": CHALLENGES[step_num],
        "lesson_id": LESSON_ID,
        "lesson_title": LESSON_TITLE,
        "url_prefix": f"/lesson/{LESSON_ID}",
        "materials": MATERIALS.get(step_num, []),
        "quiz_count": len(QUIZ),
        "is_quiz": False,
    }


# ── Routes ────────────────────────────────────────────────────────────────

@bp.route("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        steps=STEPS,
        current=len(STEPS) - 1,
        lesson_id=LESSON_ID,
        lesson_title=LESSON_TITLE,
        url_prefix=f"/lesson/{LESSON_ID}",
        quiz=QUIZ,
        quiz_count=len(QUIZ),
        is_quiz=True,
    )


@bp.route("/")
def index():
    return render_template("s4_01/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404

    ctx = base_ctx(n)

    if n in (1, 2):
        ctx["vocab"] = VOCAB
        ctx["words"] = WORDS

    elif n == 3:
        ctx["words"] = WORDS
        ctx["embeddings"] = EMBEDDING_MATRIX
        ctx["dim_labels"] = ["Threat", "Network", "Action", "Detection"]

    elif n == 4:
        ctx["words"] = WORDS
        ctx["embeddings"] = EMBEDDING_MATRIX
        ctx["sim_matrix"] = SIM_MATRIX

    elif n in (5, 6):
        ctx["attn_sentence"] = ATTENTION_SENTENCE
        ctx["attn_weights"] = ATTENTION_WEIGHTS
        ctx["embeddings"] = EMBEDDING_MATRIX
        ctx["vocab"] = VOCAB

    return render_template(f"s4_01/step_{n:02d}.html", **ctx)
