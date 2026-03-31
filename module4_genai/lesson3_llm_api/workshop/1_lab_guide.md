# Lesson 4.3 — Workshop Guide
## Working with LLM APIs

> **Read first:** [../3_claude_api.md](../3_claude_api.md) — theory and concepts
> **Reference solution:** [reference_solution.py](reference_solution.py) — open only after finishing all exercises

---

## What This Workshop Covers

You will call an LLM API to build a threat intelligence assistant. Starting from a single prompt-response, you will progress to multi-turn conversations, structured JSON output, and prompt engineering — the practical skills you need for every AI-powered security tool.

All exercises use the same `llm_client.py` abstraction, which works with Claude, OpenAI, or Gemini.

Work through them in order.

---

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_first_api_call.md](exercise1_first_api_call.md) | [exercise1_first_api_call.py](exercise1_first_api_call.py) | Make your first LLM call; understand request/response structure |
| 2 | [exercise2_system_prompts.md](exercise2_system_prompts.md) | [exercise2_system_prompts.py](exercise2_system_prompts.py) | System prompt design; security analyst persona; tone control |
| 3 | [exercise3_structured_output.md](exercise3_structured_output.md) | [exercise3_structured_output.py](exercise3_structured_output.py) | JSON output for pipeline integration; parse and validate |
| 4 | [exercise4_conversation.md](exercise4_conversation.md) | [exercise4_conversation.py](exercise4_conversation.py) | Multi-turn conversation; maintaining context across turns |

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
python module4_genai/lesson3_llm_api/workshop/exercise1_first_api_call.py
```

## Tips

- The `llm_client.py` in the `module4_genai/` folder handles provider selection automatically
- If no API key is set, the script will print an error and exit cleanly
- Each API call costs a small amount — keep `max_tokens` reasonable (200–600 for exercises)

## After This Workshop

Move to [Lesson 4.4 — RAG](../../lesson4_rag/workshop/1_lab_guide.md)
