# Lesson 4.2 — Workshop Guide
## Using Pre-trained Models with HuggingFace

> **Read first:** [../notes.md](../notes.md) — theory and concepts
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_zero_shot_classification.py`) — open only after finishing the exercise

---

## What This Workshop Covers

You will use HuggingFace's `transformers` and `sentence-transformers` libraries to apply pre-trained models without training anything from scratch. Starting with zero-shot classification on security logs, you will progress to semantic similarity search — the foundation of all modern RAG systems.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_zero_shot_classification.md](01_guide_zero_shot_classification.md) | [01_lab_zero_shot_classification.md](01_lab_zero_shot_classification.md) | Classify security logs with no training — zero-shot NLI pipeline |
| 2 | [02_guide_sentence_embeddings.md](02_guide_sentence_embeddings.md) | [02_lab_sentence_embeddings.md](02_lab_sentence_embeddings.md) | Encode sentences as vectors; cosine similarity; semantic distance |
| 3 | [03_guide_semantic_search.md](03_guide_semantic_search.md) | [03_lab_semantic_search.md](03_lab_semantic_search.md) | Build a semantic search engine over a security knowledge base |

**For each exercise:** read the guide first, then open the matching `_lab.md` file and follow the steps.

## Setup

```bash
pip install transformers sentence-transformers torch
```

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson2_huggingface/workshop/01_solution_zero_shot_classification.py
```

## Tips

- First run downloads model weights (~200MB–500MB) — subsequent runs are instant (cached)
- If internet is slow, use lighter models: `typeform/distilbart-mnli-12-1` for Exercise 1, `paraphrase-MiniLM-L3-v2` for Exercise 2
- All exercises work on CPU — no GPU required

## After This Workshop

Move to [Lesson 4.3 — LLM API](../../lesson3_llm_api/workshop/00_overview.md)
