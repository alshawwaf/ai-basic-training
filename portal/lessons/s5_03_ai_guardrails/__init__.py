"""
Lesson 5.3 — AI Guardrails
Flask Blueprint for the LLM application security workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s5_03",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s5_03"
LESSON_TITLE = "AI Guardrails"

STEPS = [
    {"id": 0, "title": "The Threat Landscape",
     "sub": "Prompt injection, jailbreaks, and why WAFs don't work"},
    {"id": 1, "title": "How Guardrails Work",
     "sub": "Inbound + outbound scanning, detection methods"},
    {"id": 2, "title": "Hands-On Lab",
     "sub": "Attack an LLM, observe what gets caught"},
    {"id": 3, "title": "Positioning Guardrails",
     "sub": "Customer conversations and competitive differentiation"},
]

CHALLENGES = {
    0: {
        "q": "An attacker uses indirect prompt injection \u2014 hiding instructions in a document the LLM summarises. How does this bypass user-facing guardrails?",
        "a": "User-facing guardrails scan the <strong>user's prompt</strong>, which is innocuous ('Summarise this document'). The malicious instructions are in the <strong>document content</strong>, which may bypass input scanning. Defense requires scanning <strong>both the prompt and the context</strong> (RAG documents, tool outputs) before they enter the LLM.",
    },
    1: {
        "q": "Your guardrails add 30ms latency. A customer says that's too slow. How do you respond?",
        "a": "30ms is <strong>invisible to users</strong> \u2014 LLM generation itself takes 500ms\u20133s. The guardrails latency is less than 5% of total response time. Compare: a WAF adds 1\u20135ms but can't detect prompt injection at all. The tradeoff is 30ms of latency for <strong>catching attacks that no other security layer can</strong>.",
    },
    2: {
        "q": "You successfully jailbroke the LLM using a role-play scenario. The guardrails didn't catch it. What does this tell you about defense strategy?",
        "a": "No single detection method catches everything. Role-play jailbreaks exploit the model's <strong>instruction-following training</strong>. Defense should be <strong>layered</strong>: pattern matching catches known attacks, NLP classifiers catch intent, semantic analysis catches variations, and <strong>output scanning</strong> catches whatever slipped through input scanning.",
    },
    3: {
        "q": "A customer says 'We already have DLP \u2014 why do we need AI-specific security?' How do you respond?",
        "a": "DLP catches sensitive <strong>data patterns</strong> (credit card numbers, SSNs) in transit. Prompt injection is not a data pattern \u2014 it's a <strong>semantic attack</strong> using natural language. 'Ignore previous instructions' contains no regulated data. DLP and AI Guardrails solve <strong>different problems</strong>: DLP protects data leaving the org, guardrails protect the AI application itself.",
    },
}

_base = "curriculum/stage5_cp_ai_security/03_ai_guardrails"

MATERIALS = {
    0: [("lecture", "Full Lecture", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    1: [("lecture", "Full Lecture", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    2: [("lecture", "Full Lecture", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    3: [("lecture", "Full Lecture", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
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
    }


@bp.route("/")
def index():
    return render_template("s5_03/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s5_03/step_{n:02d}.html", **base_ctx(n))
