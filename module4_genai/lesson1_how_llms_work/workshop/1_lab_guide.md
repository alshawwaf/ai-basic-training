# Lesson 4.1 — Workshop Guide
## How LLMs Work

> **Read first:** [../1_how_llms_work.md](../1_how_llms_work.md) — theory and concepts
> **Reference solution:** [reference_solution.py](reference_solution.py) — open only after finishing all exercises

---

## What This Workshop Covers

This workshop demystifies Large Language Models from the ground up — no API key required. You will manipulate tokens, vectors, and attention weights directly in NumPy and Python to build genuine intuition for what happens inside a model.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Exercise file | Topic |
|---|-------|---------------|-------|
| 1 | [exercise1_tokenisation.md](exercise1_tokenisation.md) | [exercise1_tokenisation.py](exercise1_tokenisation.py) | Text → tokens → token IDs; vocabulary and OOV handling |
| 2 | [exercise2_embeddings.md](exercise2_embeddings.md) | [exercise2_embeddings.py](exercise2_embeddings.py) | Tokens → vectors; cosine similarity; semantic distance |
| 3 | [exercise3_attention.md](exercise3_attention.md) | [exercise3_attention.py](exercise3_attention.py) | Attention weights as "which words matter to which"; Q/K/V intuition |

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson1_how_llms_work/workshop/exercise1_tokenisation.py
```

## Tips

- No GPU or internet connection required — all exercises run on NumPy alone
- The numbers you see are simplified toy examples, not real LLM weights
- The goal is intuition, not production-grade code

## After This Workshop

Move to [Lesson 4.2 — HuggingFace Pre-trained Models](../../lesson2_huggingface/workshop/1_lab_guide.md)
