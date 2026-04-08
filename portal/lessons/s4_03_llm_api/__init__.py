"""
Lesson 4.3 — Working with LLM APIs
Flask Blueprint for the LLM API and prompt engineering workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s4_03",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s4_03"
LESSON_TITLE = "Working with LLM APIs"

# -- Step metadata -----------------------------------------------------------

STEPS = [
    {"id": 0, "title": "Your First API Call",
     "sub": "Understand the request/response structure",
     "icon": "api-call"},
    {"id": 1, "title": "System Prompt Design",
     "sub": "Control model behaviour with a security analyst persona",
     "icon": "system-prompt"},
    {"id": 2, "title": "Structured JSON Output",
     "sub": "Machine-readable output for pipeline integration",
     "icon": "json-braces"},
    {"id": 3, "title": "Multi-Turn Conversation",
     "sub": "Maintain context across multiple exchanges",
     "icon": "chat-bubbles"},
]

# ── Quiz ────────────────────────────────────────────────────────────────────

QUIZ = [
    {
        "q": "What does the <code>max_tokens</code> parameter actually control on an LLM API call?",
        "options": [
            "The maximum size of the input prompt",
            "The maximum number of tokens the model is allowed to generate in its response &mdash; a hard cost and latency lever",
            "The total tokens in the model's vocabulary",
            "The number of API retries",
        ],
        "answer": 1,
        "explanation": "<code>max_tokens</code> caps the <strong>output length</strong>. Set it too low and answers get truncated mid-sentence; set it too high and you pay for unused capacity. In a security pipeline processing thousands of alerts/hour, this is a primary <strong>cost and latency control</strong>.",
    },
    {
        "q": "What is the purpose of the <strong>system prompt</strong>?",
        "options": [
            "It's the same as the user prompt",
            "It sets the model's persona, role, and behavioural rules &mdash; the most powerful control you have over LLM output without retraining",
            "It logs API errors",
            "It chooses which model to call",
        ],
        "answer": 1,
        "explanation": "The system prompt tells the model <strong>who it is and how it should respond</strong>. The same log entry will get a step-by-step technical reply for a 'junior SOC analyst' persona and a high-level risk briefing for a 'CISO' persona &mdash; same model, same input, completely different output.",
    },
    {
        "q": "You ask the LLM for JSON output and feed it garbage input. What's the most dangerous thing the model is likely to do?",
        "options": [
            "Crash the API",
            "Return well-formed JSON with hallucinated, plausible-looking field values &mdash; downstream automation will trust it because it parses correctly",
            "Refuse to respond entirely",
            "Return an explicit error",
        ],
        "answer": 1,
        "explanation": "LLMs almost always return <em>something</em>, even for nonsensical input. The output may be valid JSON but contain fabricated data. <strong>Always validate field values</strong>, not just JSON structure, before passing model output to automation. Never trust raw LLM output blindly.",
    },
    {
        "q": "How does an LLM API maintain a 'multi-turn conversation' if every API call is stateless?",
        "options": [
            "The API server stores each user's history",
            "<strong>You</strong> send the entire conversation history with every request &mdash; the model has no memory between calls; each call is fresh",
            "It uses cookies",
            "It's not actually possible",
        ],
        "answer": 1,
        "explanation": "LLM APIs are <strong>stateless</strong>. To create the illusion of conversation, you append the user's new message to a list of all prior messages and send the whole list every turn. This is why long conversations get expensive &mdash; you're paying for the full history on every call.",
    },
    {
        "q": "Why is the conversation history itself an <strong>attack surface</strong>?",
        "options": [
            "It uses too much memory",
            "If an attacker can inject text into earlier messages, they can rewrite the model's understanding of context &mdash; a form of prompt injection that bypasses input filtering on the latest message",
            "It can be hashed to reveal secrets",
            "It always contains personal data",
        ],
        "answer": 1,
        "explanation": "If the model sees the full conversation every turn and you only filter the <em>latest</em> user message, an attacker can inject malicious instructions into earlier turns (via tool outputs, RAG context, or compromised history) and bypass your filters. <strong>Treat the entire context window as untrusted input.</strong>",
    },
]


CHALLENGES = {
    0: {
        "q": "Make an API call with max_tokens=10, then the same prompt with max_tokens=500. How does the response change? What happens to the cost?",
        "a": "With <strong>max_tokens=10</strong>, the response is cut off mid-sentence -- the model stops generating even if its answer is incomplete. With <strong>max_tokens=500</strong>, you get a complete answer but pay for more output tokens. In a security pipeline processing thousands of alerts per hour, this difference matters: <strong>token limits are a cost and latency control</strong>. Set them as low as possible while still getting usable output.",
    },
    1: {
        "q": "Write two system prompts for the same log entry: one for a 'junior SOC analyst' persona and one for a 'CISO briefing'. How do the outputs differ in tone, detail, and recommended actions?",
        "a": "The junior SOC prompt produces <strong>step-by-step technical detail</strong> (check this IP, run this query, escalate if X). The CISO prompt produces a <strong>high-level risk summary</strong> (business impact, threat category, strategic recommendation). The system prompt is the most powerful security control you have over LLM output -- it determines <strong>who the model is talking to</strong> and shapes everything from vocabulary to actionability.",
    },
    2: {
        "q": "Send a log entry and ask for JSON output. Then send a malformed log entry (random garbage text). Does the model still return valid JSON? What are the implications for an automated pipeline?",
        "a": "On garbage input, the model may return JSON with <strong>low-confidence values</strong>, or it may hallucinate plausible-looking classifications. This is dangerous in a security pipeline: <strong>the model always returns something</strong>, even for nonsensical input. Production systems must validate JSON structure with <code>json.loads()</code> and also validate that field values are within expected ranges. Never trust raw LLM output without validation.",
    },
    3: {
        "q": "Start a conversation about a suspicious IP. After 3 turns, ask 'what IP were we discussing?' Does the model remember? Now start a new conversation and ask the same question without history. What happens?",
        "a": "With the full conversation history, the model correctly recalls the IP because <strong>you are sending the entire conversation every time</strong>. Without history, the model has no idea -- it is <strong>stateless</strong>. This has security implications: if an attacker can manipulate the conversation history (prompt injection via earlier messages), they can change the model's understanding of the entire context. <strong>Conversation history is an attack surface.</strong>",
    },
}

# -- Course materials mapping ------------------------------------------------

_base = "curriculum/stage4_genai/03_llm_api"

MATERIALS = {
    0: [("lecture", "Lecture", f"{_base}/1_first_api_call/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/1_first_api_call/handson.md"),
        ("solution", "Solution", f"{_base}/1_first_api_call/solution_first_api_call.py")],
    1: [("lecture", "Lecture", f"{_base}/2_system_prompts/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/2_system_prompts/handson.md"),
        ("solution", "Solution", f"{_base}/2_system_prompts/solution_system_prompts.py")],
    2: [("lecture", "Lecture", f"{_base}/3_structured_output/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/3_structured_output/handson.md"),
        ("solution", "Solution", f"{_base}/3_structured_output/solution_structured_output.py")],
    3: [("lecture", "Lecture", f"{_base}/4_conversation/lecture.md"),
        ("lab", "Hands-on Lab", f"{_base}/4_conversation/handson.md"),
        ("solution", "Solution", f"{_base}/4_conversation/solution_conversation.py")],
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
    return render_template("s4_03/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s4_03/step_{n:02d}.html", **base_ctx(n))
