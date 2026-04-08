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
LESSON_TITLE = "RAG (Retrieval-Augmented Generation)"

# -- Step metadata -----------------------------------------------------------

STEPS = [
    {"id": 0, "title": "Document Chunking",
     "sub": "Split documents into embeddable pieces",
     "icon": "chunk-doc"},
    {"id": 1, "title": "Retrieval",
     "sub": "Find the most relevant chunks for any query",
     "icon": "retrieval-match"},
    {"id": 2, "title": "The Full RAG Pipeline",
     "sub": "Retrieve, augment, generate -- end to end",
     "icon": "rag-pipeline"},
]

CHALLENGES = {
    0: {
        "q": "Chunk a 1000-word CVE advisory with chunk_size=100 and overlap=0, then again with overlap=20. Count the chunks produced. Which approach would you trust more for a question that falls right on a chunk boundary?",
        "a": "Without overlap you get <strong>10 chunks</strong>; with overlap=20 you get <strong>~12 chunks</strong>. The overlapping version duplicates boundary sentences, so a question about content near a split point has a better chance of retrieving a complete answer. In security advisories, <strong>mitigation steps often follow vulnerability descriptions</strong> -- if the split falls between them, a zero-overlap chunking loses the connection. Overlap is a safety net against boundary information loss.",
    },
    1: {
        "q": "Your security knowledge base has a chunk about 'SSH brute force detection' and another about 'SSH key rotation best practices'. A user queries 'how to secure SSH'. Which chunk ranks higher? Is this the right behaviour for an incident responder vs a compliance auditor?",
        "a": "Both chunks are semantically close to the query, but the model might rank <strong>brute force detection higher</strong> because 'secure' and 'detection' share a protective-action semantic cluster. For an <strong>incident responder</strong>, this is correct -- they want detection rules. For a <strong>compliance auditor</strong>, key rotation is more relevant. This shows that <strong>retrieval alone cannot distinguish user intent</strong>. Production RAG systems add metadata filters (role, document type) or use a re-ranker to personalise results.",
    },
    2: {
        "q": "Ask your RAG pipeline a question that IS in the knowledge base, then ask one that is NOT. Compare the two responses. Does the model admit when it does not know?",
        "a": "For in-context questions, the model produces a <strong>grounded, specific answer</strong> citing the retrieved chunks. For out-of-context questions, a well-prompted model says 'the provided context does not contain information about this'. Without the grounding instruction ('answer based on context only'), the model <strong>hallucinates</strong> -- it invents plausible-sounding security guidance from its pre-training. In a SOC setting, <strong>hallucinated remediation steps are dangerous</strong>. The 'based on context only' instruction is a critical safety control.",
    },
}

# -- Course materials mapping ------------------------------------------------

_base = "curriculum/stage4_genai/04_rag"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_chunking/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_chunking/handson.md"),
        ("solution", "Solution", f"{_base}/1_chunking/solution_chunking.py")],
    1: [("lecture", "Lecture", f"{_base}/2_retrieval/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_retrieval/handson.md"),
        ("solution", "Solution", f"{_base}/2_retrieval/solution_retrieval.py")],
    2: [("lecture", "Lecture", f"{_base}/3_rag_pipeline/lecture.md"),
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
    }


# -- Routes ------------------------------------------------------------------

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
