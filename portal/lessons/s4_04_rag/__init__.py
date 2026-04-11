"""
Lesson 4.4 — RAG (Retrieval-Augmented Generation)
Flask Blueprint for the RAG pipeline workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s4_04",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s4_04"
LESSON_TITLE = "Retrieval-Augmented Generation"

# -- Step metadata -----------------------------------------------------------

STEPS = [
    {"id": 0, "title": "Vector Databases",
     "sub": "Why they exist and how they work",
     "icon": "vector-db"},
    {"id": 1, "title": "Document Chunking",
     "sub": "Split documents into embeddable pieces",
     "icon": "chunk-doc"},
    {"id": 2, "title": "Retrieval",
     "sub": "Find the most relevant chunks for any query",
     "icon": "retrieval-match"},
    {"id": 3, "title": "The Full RAG Pipeline",
     "sub": "Retrieve, augment, generate -- end to end",
     "icon": "rag-pipeline"},
]

CHALLENGES = {
    0: {
        "q": "A SQL query <code>WHERE text LIKE '%credential theft%'</code> returns 3 results from your ticket database. You suspect there are more incidents described with different wording. How would a vector database help, and what would you need to build one?",
        "a": "A vector database would find tickets described as <em>'password harvesting'</em>, <em>'LSASS memory dumping'</em>, or <em>'stolen login tokens'</em> &mdash; all semantically similar to 'credential theft' even though the exact words never appear. To build one you need: <strong>(1)</strong> an embedding model (e.g. <code>all-MiniLM-L6-v2</code> from Lesson 4.2), <strong>(2)</strong> encode every ticket once with <code>model.encode()</code>, and <strong>(3)</strong> store the vectors in a vector DB. At query time, encode the question with the same model and call <code>search(top_k=10)</code>. The keyword gap that SQL cannot bridge is exactly what semantic search solves.",
    },
    1: {
        "q": "Chunk a 1000-word CVE advisory with chunk_size=100 and overlap=0, then again with overlap=20. Count the chunks produced. Which approach would you trust more for a question that falls right on a chunk boundary?",
        "a": "Without overlap you get <strong>10 chunks</strong>; with overlap=20 you get <strong>~12 chunks</strong>. The overlapping version duplicates boundary sentences, so a question about content near a split point has a better chance of retrieving a complete answer. In security advisories, <strong>mitigation steps often follow vulnerability descriptions</strong> -- if the split falls between them, a zero-overlap chunking loses the connection. Overlap is a safety net against boundary information loss.",
    },
    2: {
        "q": "Your security knowledge base has a chunk about 'SSH brute force detection' and another about 'SSH key rotation best practices'. A user queries 'how to secure SSH'. Which chunk ranks higher? Is this the right behaviour for an incident responder vs a compliance auditor?",
        "a": "Both chunks are semantically close to the query, but the model might rank <strong>brute force detection higher</strong> because 'secure' and 'detection' share a protective-action semantic cluster. For an <strong>incident responder</strong>, this is correct -- they want detection rules. For a <strong>compliance auditor</strong>, key rotation is more relevant. This shows that <strong>retrieval alone cannot distinguish user intent</strong>. Production RAG systems add metadata filters (role, document type) or use a re-ranker to personalise results.",
    },
    3: {
        "q": "Ask your RAG pipeline a question that IS in the knowledge base, then ask one that is NOT. Compare the two responses. Does the model admit when it does not know?",
        "a": "For in-context questions, the model produces a <strong>grounded, specific answer</strong> citing the retrieved chunks. For out-of-context questions, a well-prompted model says 'the provided context does not contain information about this'. Without the grounding instruction ('answer based on context only'), the model <strong>hallucinates</strong> -- it invents plausible-sounding security guidance from its pre-training. In a SOC setting, <strong>hallucinated remediation steps are dangerous</strong>. The 'based on context only' instruction is a critical safety control.",
    },
}

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "What is the fundamental advantage of a <strong>vector database</strong> over a SQL <code>LIKE</code> query?",
        "options": [
            "It's faster at exact-match lookups",
            "It finds semantically similar documents even when the exact words are different",
            "It stores more data per row",
            "It supports JOIN operations",
        ],
        "answer": 1,
        "explanation": "A SQL <code>LIKE '%ransomware%'</code> only finds the literal word. A vector database encodes meaning as vectors and finds documents about 'encryption malware demanding bitcoin' even though the word 'ransomware' never appears. <strong>Semantic similarity is the entire point.</strong>",
    },
    {
        "q": "Why must documents be <strong>chunked</strong> before embedding?",
        "options": [
            "To save disk space",
            "Embedding models have a maximum input length (128-512 tokens); a full document is too long and its embedding would be too vague",
            "Chunking is optional and only used for performance",
            "The vector database requires fixed-size inputs",
        ],
        "answer": 1,
        "explanation": "Embedding models collapse an entire input into one vector. If you embed a 10-page document, the vector averages everything &mdash; too vague to match specific questions. Chunking produces focused vectors that match specific queries.",
    },
    {
        "q": "You chunk a document with <code>overlap=0</code>. A question about content right at a chunk boundary fails to retrieve a useful answer. What went wrong?",
        "options": [
            "The embedding model is too small",
            "The chunk size is too large",
            "The relevant sentence was split across two chunks and neither chunk contains the full answer &mdash; overlap would have duplicated boundary content",
            "The vector database index is corrupted",
        ],
        "answer": 2,
        "explanation": "Without overlap, a sentence spanning a chunk boundary appears in neither chunk completely. <strong>Overlap duplicates boundary content</strong> so that both chunks contain the full sentence. For security documents where mitigation steps often follow vulnerability descriptions, this is critical.",
    },
    {
        "q": "What does the instruction 'answer based ONLY on the provided context' do in a RAG prompt?",
        "options": [
            "Makes the model respond faster",
            "Prevents the model from blending pre-training knowledge with your documents &mdash; a safety control against hallucination",
            "Limits the response length",
            "Enables multi-turn conversation",
        ],
        "answer": 1,
        "explanation": "Without this instruction, the model freely mixes its general knowledge with your retrieved chunks. The answer might sound correct but contain fabricated details. In a security context, <strong>hallucinated remediation advice during an active incident could cause real damage</strong>. Grounding is a safety control.",
    },
    {
        "q": "Compared to a pure LLM call, what is the key <strong>attribution</strong> advantage of RAG?",
        "options": [
            "RAG is cheaper per query",
            "RAG responses are always shorter",
            "You know exactly which document chunks were used to generate the answer &mdash; you can verify and cite sources",
            "RAG never hallucinates",
        ],
        "answer": 2,
        "explanation": "A pure LLM gives you an answer with no source trail. RAG returns the retrieved chunks alongside the answer, so you can <strong>verify every claim against the original document</strong>. This is essential when the answer is 'your incident response procedure says to do X' &mdash; you need to know it actually says that.",
    },
]

# -- Course materials mapping ------------------------------------------------

_base = "curriculum/stage4_genai/04_rag"

MATERIALS = {
    0: [("lecture", "Vector Databases", f"{_base}/0_vector_databases/lecture.md")],
    1: [("lecture", "Lecture", f"{_base}/1_chunking/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_chunking/handson.md"),
        ("solution", "Solution", f"{_base}/1_chunking/solution_chunking.py")],
    2: [("lecture", "Lecture", f"{_base}/2_retrieval/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_retrieval/handson.md"),
        ("solution", "Solution", f"{_base}/2_retrieval/solution_retrieval.py")],
    3: [("lecture", "Lecture", f"{_base}/3_rag_pipeline/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_rag_pipeline/handson.md"),
        ("solution", "Solution", f"{_base}/3_rag_pipeline/solution_rag_pipeline.py")],
}


# -- Helper ------------------------------------------------------------------

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


# -- Routes ------------------------------------------------------------------

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
    return render_template("s4_04/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s4_04/step_{n:02d}.html", **base_ctx(n))
