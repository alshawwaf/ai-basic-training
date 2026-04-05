# AI Ninja Program — Welcome Packet

> Congratulations on being selected for the AI Ninja Program. This packet covers everything you need to know before Week 0.

---

## What This Program Is

The AI Ninja Program is a 13-week, cohort-based training program that teaches AI and machine learning from the ground up using real cybersecurity scenarios. You will go from understanding how AI claims work in the market to building and demoing a working RAG-based Security Analyst Assistant to stakeholders.

This is not a webinar series. You will write code in every stage, pass 4 graded assessments, and present a live capstone demo in Week 13.

**By the end, you will be able to:**

- Explain how AI/ML works to customers with technical specificity, not buzzwords
- Evaluate and position against competitor AI claims (CrowdStrike, Palo Alto, SentinelOne, Darktrace, Microsoft)
- Handle the top 8 AI objections with frameworks and technical anchors
- Build a working machine learning classifier from scratch
- Build and demo a RAG-based Security Analyst Assistant loaded with real threat intelligence

---

## Program Timeline

| Weeks | Stage | What You Learn | Assessment |
|-------|-------|----------------|------------|
| 0 | Kickoff | Program overview, setup, expectations | — |
| 1–3 | Stage 0: AI Positioning + Stage 1: Classic ML | AI landscape, competitor analysis, objection handling, discovery questions, supervised learning, decision trees, model evaluation | Gate 1: Quiz + Code Challenge |
| 5–6 | Stage 2: Intermediate ML | Feature engineering, random forests, clustering, cross-validation | Gate 2: Timed Project (60 min) |
| 8–9 | Stage 3: Neural Networks | Neurons from scratch, Keras, CNNs, hyperparameter tuning | Gate 3: Architecture Review |
| 11–12 | Stage 4: Generative AI | LLMs, HuggingFace, API calls, RAG pipelines | — |
| 13 | Capstone | Live demo of your Security Analyst Assistant | Gate 4: Demo Day |

Weeks 4, 7, and 10 are assessment weeks. Week 13 is Demo Day.

---

## Weekly Rhythm

| Component | Time | Format |
|-----------|------|--------|
| Self-paced reading and exercises | 3–4 hrs | Async — do this on your own schedule |
| Weekly live session | 1 hr | Sync — Q&A, discussion, workshops |
| Slack/Teams channel activity | 15–30 min | Post progress, ask questions, help peers |
| **Total** | **~5 hrs/week** | |

The live session is the one fixed commitment. Everything else is flexible. You can do the self-paced work at 6am, during lunch, or at 11pm — whatever works for your schedule and time zone.

---

## Certification Tiers

You earn certification based on how far you progress. Every tier is valuable.

| Tier | Name | Requirements | What It Means |
|------|------|-------------|---------------|
| Tier 1 | AI Foundations | Pass Gates 1 + 2 | You understand ML fundamentals and can position AI in customer conversations |
| Tier 2 | AI Practitioner | Pass Gate 3 | You understand neural networks and can evaluate AI architectures |
| Tier 3 | AI Ninja | Pass Gate 4 (Capstone) | You can build and demo AI solutions, and are invited to co-facilitate future cohorts |

---

## Before the Kickoff — Setup Checklist

Complete these steps before Week 0. If you get stuck on any step, post in the cohort Slack channel — don't wait.

### 1. Install Python 3.10+

Check if you already have it:

```bash
python --version
```

If you see `Python 3.10` or higher, you're set. If not:

- **Windows:** Download from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during installation.
- **Mac:** `brew install python` or download from python.org.
- **Linux:** `sudo apt install python3.10` (Ubuntu/Debian) or `sudo dnf install python3.10` (Fedora).

> **Mac/Linux note:** Use `python3` instead of `python` if `python --version` shows Python 2 or "command not found."

### 2. Clone the Repository

```bash
git clone https://github.com/alshawwaf/ai-basic-training.git
cd ai-basic-training
```

### 3. Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

Your terminal prompt should now show `(venv)`. This isolates the program's packages from the rest of your system.

### 4. Verify the Setup

```bash
python --version          # Should show 3.10+
pip --version             # Should work without errors
python -c "import json; print('Ready!')"   # Should print "Ready!"
```

### 5. Complete the Skills Survey

Your tech lead will send you a pre-program skills survey. Complete it before the kickoff — it takes 5 minutes and helps us pair you with the right partner.

### 6. (Optional) Get an LLM API Key

Stage 4 requires an LLM API. You don't need this until Week 11, but if you want to set it up early:

| Provider | Free tier? | How to get a key |
|----------|-----------|-----------------|
| Google Gemini | Yes — generous free tier | [aistudio.google.com](https://aistudio.google.com) |
| Anthropic Claude | Pay-as-you-go | [console.anthropic.com](https://console.anthropic.com) |
| OpenAI | Pay-as-you-go | [platform.openai.com](https://platform.openai.com) |
| Ollama (local) | Free — runs on your machine | [ollama.com](https://ollama.com) |

---

## What to Expect in Week 1

After the kickoff, your first week covers:

- **Stage 0, Session 0.1:** The AI Landscape in Cybersecurity — terminology, where AI is deployed today, and a 5-question framework for evaluating AI claims
- **Stage 1, Lesson 1.1:** What is Machine Learning? — loading data, exploring features, visualising what an ML model sees

Both are self-paced reading + exercises. The first live Q&A session covers both.

---

## How to Get Help

| Situation | What to Do |
|-----------|-----------|
| Stuck on a concept | Post in the Slack channel — someone else probably has the same question |
| Stuck on a Python error | Post the error message and the code that caused it — your pair partner or a peer will help |
| Falling behind | Message the tech lead privately — we'll adjust, not judge |
| Assessment anxiety | The assessments are designed to confirm understanding, not trick you. Retakes are available. |
| Environment/setup issues | Post in Slack immediately — don't spend hours debugging alone |

---

## Ground Rules

1. **No question is too basic.** If you're thinking it, someone else is too.
2. **Post publicly before DMing.** Your question helps the whole cohort.
3. **Help your peers.** Explaining a concept to someone else is the best way to solidify your own understanding.
4. **Do the exercises yourself first.** The solutions are there as a reference, not a shortcut. The struggle is where learning happens.
5. **Show up to live sessions.** They're recorded, but the discussion and Q&A only work live.
6. **Reach out early if you're falling behind.** Week 3 is too late to say you've been stuck since Week 1.

---

## Your Tech Lead

**[Name]** — [Role]

Available via Slack, email, or the weekly live session. Office hours: [TBD based on cohort time zones].

---

We're excited to have you in this cohort. See you at the kickoff.
