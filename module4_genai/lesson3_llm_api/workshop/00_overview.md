# Lesson 4.3 — Workshop Guide
## Working with LLM APIs

> **Read first:** [../notes.md](../notes.md) — theory and concepts
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_first_api_call.py`) — open only after finishing the exercise

---

## What This Workshop Covers

You will call an LLM API to build a threat intelligence assistant. Starting from a single prompt-response, you will progress to multi-turn conversations, structured JSON output, and prompt engineering — the practical skills you need for every AI-powered security tool.

All exercises use the same `llm_client.py` abstraction, which works with Claude, OpenAI, or Gemini.

Work through them in order.

---

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_first_api_call.md](01_guide_first_api_call.md) | [01_lab_first_api_call.md](01_lab_first_api_call.md) | Make your first LLM call; understand request/response structure |
| 2 | [02_guide_system_prompts.md](02_guide_system_prompts.md) | [02_lab_system_prompts.md](02_lab_system_prompts.md) | System prompt design; security analyst persona; tone control |
| 3 | [03_guide_structured_output.md](03_guide_structured_output.md) | [03_lab_structured_output.md](03_lab_structured_output.md) | JSON output for pipeline integration; parse and validate |
| 4 | [04_guide_conversation.md](04_guide_conversation.md) | [04_lab_conversation.md](04_lab_conversation.md) | Multi-turn conversation; maintaining context across turns |

**For each exercise:** read the guide first, then open the matching `_lab.md` file and follow the steps.

## Setup

Set at least one API key:
```bash
set ANTHROPIC_API_KEY=your-key-here   # Claude (recommended)
set OPENAI_API_KEY=your-key-here      # OpenAI
set GOOGLE_API_KEY=your-key-here      # Gemini
```

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson3_llm_api/workshop/01_solution_first_api_call.py
```

## Tips

- The `llm_client.py` in the `module4_genai/` folder handles provider selection automatically
- If no API key is set, the script will print an error and exit cleanly
- Each API call costs a small amount — keep `max_tokens` reasonable (200–600 for exercises)

## After This Workshop

Move to [Lesson 4.4 — RAG](../../lesson4_rag/workshop/00_overview.md)
