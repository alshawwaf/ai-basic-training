"""
Lesson 5.1 — Workforce AI Security
Flask Blueprint — interactive exploration of shadow AI, data classification,
policy enforcement, and dashboard interpretation.
All computation is client-side (JavaScript) — no ML dependencies.
"""

import random
from flask import Blueprint, render_template

bp = Blueprint(
    "s5_01",
    __name__,
    template_folder="templates",
)

LESSON_ID = "s5_01"
LESSON_TITLE = "Workforce AI Security"

# ── Simulated AI traffic data ────────────────────────────────────────────

AI_APPS = [
    {"name": "ChatGPT",   "vendor": "OpenAI",     "cat": "General LLM",     "managed": True,  "risk": "Medium", "users": 312, "sessions": 8420},
    {"name": "Claude",    "vendor": "Anthropic",   "cat": "General LLM",     "managed": True,  "risk": "Low",    "users": 187, "sessions": 4210},
    {"name": "Copilot",   "vendor": "GitHub",      "cat": "Code Assistant",  "managed": True,  "risk": "Medium", "users": 94,  "sessions": 6830},
    {"name": "Gemini",    "vendor": "Google",      "cat": "General LLM",     "managed": False, "risk": "Medium", "users": 63,  "sessions": 1540},
    {"name": "Perplexity","vendor": "Perplexity",  "cat": "Search LLM",      "managed": False, "risk": "Low",    "users": 41,  "sessions": 870},
    {"name": "Cursor",    "vendor": "Cursor Inc.", "cat": "Code Assistant",  "managed": False, "risk": "High",   "users": 28,  "sessions": 2100},
    {"name": "Poe",       "vendor": "Quora",       "cat": "Multi-model",     "managed": False, "risk": "High",   "users": 15,  "sessions": 340},
    {"name": "Hugging Face Chat", "vendor": "HF",  "cat": "Open Source LLM", "managed": False, "risk": "Medium", "users": 12,  "sessions": 210},
]

DEPARTMENTS = [
    {"name": "Engineering", "users": 120, "pct": 34},
    {"name": "Marketing",   "users": 78,  "pct": 22},
    {"name": "Legal",       "users": 64,  "pct": 18},
    {"name": "Sales",       "users": 45,  "pct": 13},
    {"name": "HR",          "users": 28,  "pct": 8},
    {"name": "Executive",   "users": 18,  "pct": 5},
]

# Sample prompts for classification exercise
SAMPLE_PROMPTS = [
    {"text": "Summarise the latest quarterly earnings report for our board presentation",
     "types": ["financial"], "risk": "high"},
    {"text": "Help me write a Python function to parse JSON logs",
     "types": ["safe"], "risk": "low"},
    {"text": "Here is the patient record for John Smith, DOB 03/15/1982, SSN 412-55-8901. Summarise the diagnosis.",
     "types": ["pii", "medical"], "risk": "critical"},
    {"text": "Review this code from our authentication module: def verify_token(token, secret_key='sk-prod-a8f2e...'):",
     "types": ["credentials", "source_code"], "risk": "critical"},
    {"text": "What are the best practices for implementing zero-trust architecture?",
     "types": ["safe"], "risk": "low"},
    {"text": "Translate this marketing email to Spanish: Dear valued customer...",
     "types": ["safe"], "risk": "low"},
    {"text": "Our AWS access key is AKIA3EXAMPLE7KEY and the secret is wJalr... Please help me configure the S3 bucket.",
     "types": ["credentials"], "risk": "critical"},
    {"text": "List all employees in the London office with salaries over £80,000 and their performance ratings",
     "types": ["pii", "financial"], "risk": "high"},
    {"text": "Analyse this network capture: src_ip=10.0.5.23 dst_ip=185.143.223.1 port=4444 payload=0x4d5a90...",
     "types": ["source_code"], "risk": "medium"},
    {"text": "Draft a press release about our new partnership with Acme Corp, announced next Tuesday",
     "types": ["confidential"], "risk": "medium"},
]

# Dashboard metrics (30-day simulated data)
DASHBOARD = {
    "total_interactions": 47200,
    "unique_users": 812,
    "total_employees": 2000,
    "adoption_pct": 41,
    "sensitive_events": 1340,
    "pii_redacted": 487,
    "code_blocked": 218,
    "warnings_continued": 635,
    "shadow_apps": 7,
    "after_hours_pct": 31,
    "managed_pct": 62,
    "unmanaged_pct": 38,
    "daily_trend": [1200, 1350, 1480, 1520, 1610, 1540, 980, 1020, 1680, 1720,
                    1810, 1790, 1850, 1900, 920, 870, 1950, 2010, 2100, 2050,
                    2150, 2200, 1050, 980, 2250, 2300, 2180, 2350, 2400, 2450],
    "by_app": [
        {"name": "ChatGPT", "pct": 61, "sessions": 28792},
        {"name": "Copilot", "pct": 24, "sessions": 11328},
        {"name": "Gemini",  "pct": 9,  "sessions": 4248},
        {"name": "Claude",  "pct": 4,  "sessions": 1888},
        {"name": "Other",   "pct": 2,  "sessions": 944},
    ],
    "sensitive_by_type": [
        {"type": "PII", "count": 487, "color": "#e11d48"},
        {"type": "Source Code", "count": 312, "color": "#7c3aed"},
        {"type": "Credentials", "count": 89, "color": "#f59e0b"},
        {"type": "Financial", "count": 234, "color": "#0891b2"},
        {"type": "Medical/PHI", "count": 67, "color": "#059669"},
        {"type": "Confidential", "count": 151, "color": "#6366f1"},
    ],
}

# ── Step metadata ─────────────────────────────────────────────────────────

STEPS = [
    {"id": 0, "title": "The Shadow AI Problem",  "sub": "What you can't see can hurt you"},
    {"id": 1, "title": "Data at Risk",            "sub": "Classify sensitive content"},
    {"id": 2, "title": "The Six Policy Actions",  "sub": "Allow, Prevent, Redact, Detect, Block, Ask"},
    {"id": 3, "title": "Policy Matrix Builder",   "sub": "Design your own policy"},
    {"id": 4, "title": "Redaction in Action",     "sub": "Strip sensitive data in real time"},
    {"id": 5, "title": "Dashboard Deep Dive",     "sub": "Read the metrics like a SOC analyst"},
    {"id": 6, "title": "Risk Scoring",            "sub": "Anomaly detection meets AI governance"},
    {"id": 7, "title": "The Full Picture",        "sub": "Connecting all stages to Workforce AI Security"},
]

CHALLENGES = {
    0: {
        "q": "Your customer says 'We already block AI at the firewall.' What do they miss? List 3 blind spots.",
        "a": "1. <strong>Personal devices</strong> — employees use ChatGPT on their phones over mobile data. 2. <strong>Embedded AI</strong> — tools like Notion AI, Grammarly, and browser extensions send data to AI APIs without being 'AI apps'. 3. <strong>No visibility</strong> — they don't know what was being sent before the block, so they can't assess past exposure. Blocking ≠ security. <strong>Governance = visibility + control.</strong>",
    },
    1: {
        "q": "A prompt contains a customer name AND an AWS key. Which classification matters more? Why?",
        "a": "The <strong>credential</strong> is more critical — a leaked AWS key provides direct access to infrastructure and can be exploited within minutes by automated scanners. PII exposure is serious but typically requires social engineering to weaponise. Real systems use <strong>highest-severity-wins</strong> for multi-label classification.",
    },
    2: {
        "q": "A customer wants to start with 'Block' on everything. Why is 'Detect' a better first step?",
        "a": "<strong>Detect mode</strong> lets you see the real usage patterns before disrupting workflows. If you block immediately, you'll face employee backlash, shadow workarounds, and you won't know what you're actually protecting against. Start with <strong>Detect → analyse → design targeted policies → enforce gradually.</strong>",
    },
    3: {
        "q": "Your policy blocks PII in ChatGPT but allows it in Claude. A user asks why. What's your answer?",
        "a": "Different AI services have different <strong>data retention policies</strong>. Claude (with a business plan) offers zero-retention by default. ChatGPT's data practices differ by tier. Policy should reflect the actual risk of each service, not apply blanket rules. This is why <strong>per-app, per-data-type policies</strong> are necessary.",
    },
    4: {
        "q": "A redacted prompt loses critical context and the AI gives a useless response. How do you handle this?",
        "a": "This is the <strong>utility vs security trade-off</strong>. Options: 1. Use <strong>Ask</strong> action instead — let the user justify the sensitive data. 2. <strong>Replace with synthetic data</strong> (fake names, placeholder IPs) that preserves structure. 3. Use an <strong>on-prem AI</strong> for prompts requiring sensitive context. The best solution depends on the use case.",
    },
    5: {
        "q": "The dashboard shows 31% after-hours AI usage. Is this a risk indicator or normal? How would you investigate?",
        "a": "It depends on context. Check: 1. <strong>Which departments?</strong> Engineering working late is normal; HR at 2am is suspicious. 2. <strong>What data types?</strong> After-hours + sensitive data = higher risk. 3. <strong>Trend</strong> — is it growing? A sudden spike may indicate a departing employee exfiltrating data. <strong>Context turns a metric into an insight.</strong>",
    },
    6: {
        "q": "A user's risk score jumps from 15 to 78 in one day. They uploaded 50 files to ChatGPT. Is this malicious?",
        "a": "Not necessarily. Check: 1. <strong>File types</strong> — marketing images vs source code. 2. <strong>Context</strong> — were they told to migrate docs? 3. <strong>History</strong> — is this their first spike or a pattern? Anomaly detection flags the <strong>deviation</strong>; human judgement determines the <strong>intent</strong>. This is exactly like UEBA from Stage 2.",
    },
    7: {
        "q": "A customer asks: 'Why do I need Workforce AI Security if I already have DLP?' What do you say?",
        "a": "Traditional DLP inspects <strong>files and emails</strong> — it wasn't designed for AI interactions. Workforce AI Security understands: 1. <strong>AI-specific context</strong> — prompts, completions, system messages 2. <strong>Application-level visibility</strong> — which AI tool, what model, what integration 3. <strong>Inline AI traffic</strong> — real-time scanning of conversational data, not just file transfers. It's not DLP vs WAI — they're complementary layers.",
    },
}


# ── Course materials mapping ────────────────────────────────────────────────

_base = "stage5_cp_ai_security/01_workforce_ai_security"

MATERIALS = {
    0: [("lecture", "Workforce AI Security", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    1: [("lecture", "Workforce AI Security", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    2: [("lecture", "Workforce AI Security", f"{_base}/README.md")],
    3: [("lecture", "Workforce AI Security", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    4: [("lecture", "Workforce AI Security", f"{_base}/README.md")],
    5: [("lecture", "Workforce AI Security", f"{_base}/README.md"),
        ("lab", "Discussion Guide", f"{_base}/discussion_guide.md")],
    6: [("lecture", "Workforce AI Security", f"{_base}/README.md")],
    7: [("lecture", "Workforce AI Security", f"{_base}/README.md")],
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


# ── Routes ────────────────────────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("s5_01/index.html",
                           steps=STEPS, lesson_id=LESSON_ID,
                           lesson_title=LESSON_TITLE,
                           url_prefix=f"/lesson/{LESSON_ID}")


@bp.route("/step/<int:n>")
def step(n):
    if n < 0 or n >= len(STEPS):
        return "Step not found", 404

    ctx = base_ctx(n)

    if n == 0:
        ctx["ai_apps"] = AI_APPS
        ctx["departments"] = DEPARTMENTS

    elif n == 1:
        ctx["prompts"] = SAMPLE_PROMPTS

    elif n == 5:
        ctx["dashboard"] = DASHBOARD

    elif n == 6:
        ctx["departments"] = DEPARTMENTS

    return render_template(f"s5_01/step_{n:02d}.html", **ctx)
