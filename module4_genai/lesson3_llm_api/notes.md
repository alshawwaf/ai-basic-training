# Lesson 4.3 — Working with LLM APIs

---

## Concept: Directing a Powerful Model with Natural Language

HuggingFace models are task-specific (summarise this, classify that). A conversational LLM API gives you a general-purpose AI that you direct entirely through natural language instructions — the **system prompt**.

This lesson works with **Claude, OpenAI, Gemini, or Ollama** — set whichever you have:

```bash
set ANTHROPIC_API_KEY=...   # Claude  (recommended)
set OPENAI_API_KEY=...      # OpenAI
set GOOGLE_API_KEY=...      # Gemini  (free tier available)
set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B     # Ollama  (local, no key needed)
```

The `llm_client.py` helper auto-detects which key is available and wraps it in a common interface, so the rest of the code is identical regardless of provider:

```python
from llm_client import get_client
provider, client = get_client()   # auto-detects your key

response = client.chat(
    system="You are a threat intelligence analyst. Be concise and technical.",
    messages=[{"role": "user", "content": "Analyse this log entry: ..."}]
)
```

---

## The System Prompt: Your Most Powerful Tool

The system prompt defines the model's behaviour for the entire conversation:

```python
system = """
You are a cybersecurity analyst specialising in threat intelligence.
When given a log entry or IOC:
1. Identify the attack technique (MITRE ATT&CK if applicable)
2. Assess severity (Critical/High/Medium/Low)
3. Recommend immediate response actions
Always be concise. Use bullet points for recommendations.
"""
```

The quality of your system prompt directly determines the quality of the output.

---

## The Messages Format

Conversations are a list of alternating user/assistant messages:

```python
messages = [
    {"role": "user",      "content": "What does this log mean?"},
    {"role": "assistant", "content": "This indicates a brute force attack..."},
    {"role": "user",      "content": "What should I do about it?"},
]
```

You maintain conversation history manually — just append each turn and send the full list.

---

## Structured Output

Claude can return JSON reliably when instructed:

```python
system = "Always respond with valid JSON only. No prose."
prompt = "Classify this alert as JSON with fields: tactic, severity, confidence"
```

This is how you integrate Claude into automated security pipelines.

---

## Setup

```bash
pip install anthropic          # if using Claude
pip install openai             # if using OpenAI
pip install google-generativeai  # if using Gemini
pip install ollama             # if using Ollama (local)
```

---

## Running Locally with Ollama

Ollama lets you run open-source LLMs entirely on your own machine — no API key, no internet connection required after the initial model download.

**Why this matters for security work:**
- Sensitive data (malware samples, IR reports, CVE details) never leaves your machine
- Works in air-gapped or restricted network environments
- No usage costs, no rate limits

**Setup:**

1. Download and install Ollama from [ollama.com](https://ollama.com)
2. Pull the model (one-time download, ~2 GB):
   ```bash
   ollama pull huihui_ai/qwen3.5-abliterated:2B
   ```
3. Set the environment variable — no API key needed:
   ```bash
   set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B   # Windows
   export OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B  # Mac/Linux
   ```

All Module 4 scripts will automatically use your local model. No code changes required.

**Trade-off to be aware of:** Local models are generally less capable than cloud APIs for complex reasoning tasks like RAG. For development and learning they work well; for production security tooling, a cloud API will give better results.

---

## API Cost Awareness (Cloud Providers)

Claude pricing (as of 2025):
- Input tokens: $3 / million tokens (Sonnet)
- Output tokens: $15 / million tokens (Sonnet)

A 1,000-word security report analysis costs ~$0.001 — effectively free for development. Gemini offers a free tier. Ollama is free indefinitely.

---

## What to Notice When You Run It

1. How the system prompt shapes the response format
2. Multi-turn conversation maintaining context
3. Structured JSON output for pipeline integration
4. Response time (usually 1–5 seconds for moderate-length outputs)

---

## Next Lesson

**[Lesson 4.4 — RAG](../lesson4_rag/notes.md):** The model's knowledge has a cutoff date and doesn't know your internal documents. RAG fixes both problems.

---

## Ready for the Workshop?

You have covered the concepts. Now build it yourself.

**[Open workshop/00_overview.md](workshop/00_overview.md)**
