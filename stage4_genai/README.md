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

### Lesson 4.1 — [How LLMs Work](1_how_llms_work.md)
**Script:** [1_llm_concepts.py](1_llm_concepts.py)
Tokenisation, embeddings, and next-token prediction — the machinery behind ChatGPT/Claude.

### Lesson 4.2 — [HuggingFace Pre-trained Models](2_huggingface_pretrained_models.md)
**Script:** [2_huggingface.py](2_huggingface.py)
Use transformer models out-of-the-box for text classification, NER, and summarisation.

### Lesson 4.3 — [The Claude API](3_claude_api.md)
**Script:** [3_claude_api.py](3_claude_api.py)
Build a conversational threat intelligence assistant using Anthropic's Claude.

### Lesson 4.4 — [Retrieval-Augmented Generation](4_retrieval_augmented_generation.md)
**Script:** [4_rag.py](4_rag.py)
Ground the model's answers in your own security documents to reduce hallucination.

### Milestone — [Security Analyst Assistant](milestone_security_assistant.py)
**Script:** [milestone_security_assistant.py](milestone_security_assistant.py)
A full RAG-based assistant that answers questions about CVEs and threat intelligence.

---

## Setup

```bash
pip install transformers anthropic numpy pandas sentence-transformers
```

For the Claude API lessons you need an Anthropic API key:
```bash
# Set in your terminal (or add to .env file)
set ANTHROPIC_API_KEY=your-key-here     # Windows
export ANTHROPIC_API_KEY=your-key-here  # Mac/Linux
```

Get a key at: https://console.anthropic.com
