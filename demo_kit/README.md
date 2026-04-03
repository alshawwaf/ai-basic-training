# Security Analyst Assistant — Demo Kit

This is a packaged version of the Stage 4 Security Analyst Assistant designed for customer demonstrations. It shows how Retrieval-Augmented Generation (RAG) can give SOC analysts instant, source-grounded answers to security questions — without the hallucination risk of a raw LLM.

## What's in the Kit

| File | Purpose |
|------|---------|
| `demo_assistant.py` | The RAG assistant application (Stage 4 capstone) |
| `data/` | Detection engineering guides used as the retrieval corpus |
| `demo_script.md` | A 5-minute customer-facing presentation script |
| `architecture.md` | One-page RAG architecture explainer for technical buyers |
| `demo_queries.md` | 10 pre-built demo queries with expected behaviour notes |

## Prerequisites

- **Python 3.10+**
- **One API key** (set as an environment variable):
  - `ANTHROPIC_API_KEY` — for Claude models, or
  - `OPENAI_API_KEY` — for GPT models, or
  - `GOOGLE_API_KEY` — for Gemini models
- **pip packages:**
  ```
  pip install sentence-transformers numpy
  ```

## Quick Start

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. Run the assistant
python demo_assistant.py
```

The assistant will automatically load and embed every `.md` file in the `data/` folder, then present an interactive prompt where you can ask security questions.

## How to Customise

**Add your own documents:** Drop any `.md` file into the `data/` folder. The assistant chunks and embeds documents at startup, so new files are picked up automatically on the next run. Good candidates include:

- Internal runbooks and playbooks
- Threat intelligence reports
- Vulnerability advisories (CVE write-ups)
- Compliance control descriptions

**Swap the LLM provider:** Change the API key environment variable to switch between Claude, GPT, or Gemini. No code changes needed.

**Adjust retrieval:** Edit the `top_k` and `chunk_size` parameters in `demo_assistant.py` to tune how many chunks are retrieved and how large each chunk is.
