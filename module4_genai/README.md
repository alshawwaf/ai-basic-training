# Module 4 — Generative AI

## Goal
Move from models that classify to models that *generate* — understand how LLMs work, use pre-trained models, call the Claude API, and build a RAG-based security assistant.

---

## The Shift in Thinking

Stages 1–3 were all about **discriminative models**: given input X, predict label Y.

Stage 4 is about **generative models**: given a prompt/context, *produce* meaningful text, code, or structured output.

| Stage 1–3 (Discriminative) | Stage 4 (Generative) |
|---------------------------|----------------------|
| Input → label (0/1) | Input → generated text |
| Train from scratch on your data | Use massive pre-trained models |
| Evaluate with accuracy/AUC | Evaluate with task performance |
| Small models (KBs–MBs) | Large models (GBs–TBs) |

---

## What You'll Build

- **Lesson 4.1** — Understand tokens, embeddings, and how LLMs predict next tokens
- **Lesson 4.2** — Use HuggingFace pipelines for NLP tasks (no training needed)
- **Lesson 4.3** — Call the Claude API to build a threat intelligence assistant
- **Lesson 4.4** — RAG: feed the model your own documents for accurate, grounded answers
- **Milestone** — A working security analyst assistant that answers questions about CVEs and threat reports

---

## Lessons

### Lesson 4.1 — [How LLMs Work](lesson1_how_llms_work/notes.md)
**Workshop:** [lesson1_how_llms_work/workshop/00_overview.md](lesson1_how_llms_work/workshop/00_overview.md)
Tokenisation, embeddings, and next-token prediction — the machinery behind ChatGPT/Claude.

### Lesson 4.2 — [HuggingFace Pre-trained Models](lesson2_huggingface/notes.md)
**Workshop:** [lesson2_huggingface/workshop/00_overview.md](lesson2_huggingface/workshop/00_overview.md)
Use transformer models out-of-the-box for text classification, NER, and summarisation.

### Lesson 4.3 — [The Claude API](lesson3_llm_api/notes.md)
**Workshop:** [lesson3_llm_api/workshop/00_overview.md](lesson3_llm_api/workshop/00_overview.md)
Build a conversational threat intelligence assistant using Anthropic's Claude.

### Lesson 4.4 — [Retrieval-Augmented Generation](lesson4_rag/notes.md)
**Workshop:** [lesson4_rag/workshop/00_overview.md](lesson4_rag/workshop/00_overview.md)
Ground the model's answers in your own security documents to reduce hallucination.

### Milestone — [Security Analyst Assistant](milestone/milestone_security_assistant.py)
**Script:** [milestone/milestone_security_assistant.py](milestone/milestone_security_assistant.py)
A full RAG-based assistant that answers questions about CVEs and threat intelligence.

---

## Setup

```bash
pip install transformers anthropic openai google-generativeai numpy pandas sentence-transformers
```

All scripts use [llm_client.py](llm_client.py) which auto-detects whichever key you have set.
You only need **one** of these:

| Provider | Environment Variable | Where to get it |
|----------|---------------------|-----------------|
| Claude (Anthropic) | `ANTHROPIC_API_KEY` | console.anthropic.com |
| OpenAI | `OPENAI_API_KEY` | platform.openai.com |
| Gemini (Google) | `GOOGLE_API_KEY` | aistudio.google.com (free) |

```bash
set ANTHROPIC_API_KEY=your-key-here    # Windows
export ANTHROPIC_API_KEY=your-key-here # Mac/Linux
```
