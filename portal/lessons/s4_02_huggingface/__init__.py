"""
Lesson 4.2 — HuggingFace Pre-trained Models
Flask Blueprint for the HuggingFace pipelines and semantic search workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s4_02",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s4_02"
LESSON_TITLE = "HuggingFace Pre-trained Models"

# -- Step metadata -----------------------------------------------------------

STEPS = [
    {"id": 0, "title": "Zero-Shot Classification",
     "sub": "Classify security logs with no training data",
     "icon": "zero-shot"},
    {"id": 1, "title": "Sentence Embeddings",
     "sub": "Encode sentences as vectors for semantic comparison",
     "icon": "embedding-vector"},
    {"id": 2, "title": "Semantic Search",
     "sub": "Build a search engine over a security knowledge base",
     "icon": "semantic-search"},
]

CHALLENGES = {
    0: {
        "q": "Classify 'DNS query to known C2 domain at 3 AM from accounting workstation' using candidate labels: data exfiltration, lateral movement, C2 communication, normal activity. Which label wins? Now add 'scheduled backup' as a fifth label -- does the ranking change?",
        "a": "<strong>C2 communication</strong> should score highest because the text explicitly mentions a C2 domain. Adding 'scheduled backup' may slightly redistribute probabilities but should not displace C2. This demonstrates a key risk: <strong>label design controls model output</strong>. An attacker who understands your labels could craft log entries that push classification toward 'normal activity' -- this is an adversarial evasion technique against NLI-based classifiers.",
    },
    1: {
        "q": "Encode these two sentences: 'User logged in from VPN' and 'Employee accessed system remotely via VPN'. What is their cosine similarity? Now encode 'Pizza delivery at noon'. How does its similarity compare to the first two?",
        "a": "The VPN sentences should have <strong>high cosine similarity (>0.8)</strong> because they express the same semantic meaning with different words. The pizza sentence should have <strong>very low similarity (<0.2)</strong>. This is the foundation of semantic search: <strong>meaning-based matching beats keyword matching</strong>. A keyword search for 'logged in' would miss the second sentence entirely, but embeddings capture the shared meaning.",
    },
    2: {
        "q": "Your knowledge base has 50 security advisories. A SOC analyst queries 'how to detect credential dumping'. The top result is about Mimikatz and LSASS. But the second result is about password spraying. Is this a retrieval failure? Why or why not?",
        "a": "Not a failure -- it is a <strong>semantic neighbourhood effect</strong>. Password spraying and credential dumping are both credential-theft techniques, so their embeddings are close in vector space. In a security context, this is actually <strong>useful</strong>: related techniques surface together. However, for precise retrieval you might need to <strong>re-rank</strong> results or use hybrid search (semantic + keyword) to separate closely related but distinct techniques.",
    },
}

# -- Course materials mapping ------------------------------------------------

_base = "curriculum/stage4_genai/02_huggingface"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_zero_shot_classification/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_zero_shot_classification/handson.md"),
        ("solution", "Solution", f"{_base}/1_zero_shot_classification/solution_zero_shot_classification.py")],
    1: [("lecture", "Lecture", f"{_base}/2_sentence_embeddings/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_sentence_embeddings/handson.md"),
        ("solution", "Solution", f"{_base}/2_sentence_embeddings/solution_sentence_embeddings.py")],
    2: [("lecture", "Lecture", f"{_base}/3_semantic_search/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_semantic_search/handson.md"),
        ("solution", "Solution", f"{_base}/3_semantic_search/solution_semantic_search.py")],
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
    return render_template("s4_02/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s4_02/step_{n:02d}.html", **base_ctx(n))
