"""
Lesson 5.4 — Positioning Check Point AI Security
Flask Blueprint for the sales enablement workshop.
"""

from flask import Blueprint, render_template

bp = Blueprint(
    "s5_04",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s5_04"
LESSON_TITLE = "Positioning CP AI"

STEPS = [
    {"id": 0, "title": "The Three-Layer Narrative",
     "sub": "Workforce, Applications, Agents \u2014 map concerns to products",
     "icon": "three-layers"},
    {"id": 1, "title": "Competitive Positioning",
     "sub": "Microsoft, Zscaler, Palo Alto, Lakera \u2014 where we win",
     "icon": "compete-bars"},
    {"id": 2, "title": "Building Your Demo",
     "sub": "Three 5-minute demo scripts ready to deliver",
     "icon": "demo-screen"},
    {"id": 3, "title": "Role-Play Scenarios",
     "sub": "Practice with the CISO, the builder, and the AI-first SOC",
     "icon": "roleplay-masks"},
]

CHALLENGES = {
    0: {
        "q": "A customer says 'We don't use AI yet, so we don't need AI security.' How do you respond?",
        "a": "They almost certainly <strong>do</strong> use AI \u2014 they just don't know it. Employees use ChatGPT, Copilot, Gemini, and Claude on personal devices or through browser tabs. Shadow AI is the norm, not the exception. Workforce AI Security discovers this usage and gives them <strong>visibility before governance</strong>.",
    },
    1: {
        "q": "You're in a competitive bake-off against Microsoft Purview. The customer is all-Microsoft. What's your angle?",
        "a": "Purview only covers <strong>Microsoft's AI tools</strong>. Their employees also use ChatGPT, Claude, Gemini, and open-source models \u2014 Purview has zero visibility into those. Plus, Purview doesn't cover custom LLM applications or AI agents. Position Check Point as the <strong>multi-vendor layer</strong> that works alongside Purview, covering the gaps.",
    },
    2: {
        "q": "A customer asks for a proof of concept. Which of the three AI Security products would you start with?",
        "a": "<strong>Workforce AI Security in Detect mode</strong>. It requires zero policy decisions, deploys in minutes (it's a visibility tool), and produces <strong>immediate value</strong>: 'Here's the AI usage in your organisation that you didn't know about.' Once they see the data, the conversation about governance and guardrails happens naturally.",
    },
    3: {
        "q": "The CISO asks: 'Can you guarantee no data will leak to AI tools?' What's the honest answer?",
        "a": "No product can guarantee zero leakage. But you can <strong>reduce risk dramatically</strong>: detect and block sensitive data in AI prompts, restrict usage to approved tools, redact PII automatically, and log everything for audit. The goal is <strong>governance, not prohibition</strong>. Blocking AI just creates shadow AI.",
    },
}

_base = "curriculum/stage5_cp_ai_security/04_positioning_cp_ai"

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
    return render_template("s5_04/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404
    return render_template(f"s5_04/step_{n:02d}.html", **base_ctx(n))
