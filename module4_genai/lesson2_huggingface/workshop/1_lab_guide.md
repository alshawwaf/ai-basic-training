# Lesson 4.2 — Workshop Guide
## Using Pre-trained Models with HuggingFace

> **Read first:** [../2_huggingface_pretrained_models.md](../2_huggingface_pretrained_models.md) — theory and concepts
> **Reference solution:** [reference_solution.py](reference_solution.py) — open only after finishing all exercises

---

## What This Workshop Covers

You will use HuggingFace's `transformers` and `sentence-transformers` libraries to apply pre-trained models without training anything from scratch. Starting with zero-shot classification on security logs, you will progress to semantic similarity search — the foundation of all modern RAG systems.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_zero_shot_classification.md](exercise1_zero_shot_classification.md) | [exercise1_zero_shot_classification.py](exercise1_zero_shot_classification.py) | Classify security logs with no training — zero-shot NLI pipeline |
| 2 | [exercise2_sentence_embeddings.md](exercise2_sentence_embeddings.md) | [exercise2_sentence_embeddings.py](exercise2_sentence_embeddings.py) | Encode sentences as vectors; cosine similarity; semantic distance |
| 3 | [exercise3_semantic_search.md](exercise3_semantic_search.md) | [exercise3_semantic_search.py](exercise3_semantic_search.py) | Build a semantic search engine over a security knowledge base |

## Setup

```bash
pip install transformers sentence-transformers torch
```

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson2_huggingface/workshop/exercise1_zero_shot_classification.py
```

## Tips

- First run downloads model weights (~200MB–500MB) — subsequent runs are instant (cached)
- If internet is slow, use lighter models: `typeform/distilbart-mnli-12-1` for Exercise 1, `paraphrase-MiniLM-L3-v2` for Exercise 2
- All exercises work on CPU — no GPU required

## After This Workshop

Move to [Lesson 4.3 — LLM API](../../lesson3_llm_api/workshop/1_lab_guide.md)
