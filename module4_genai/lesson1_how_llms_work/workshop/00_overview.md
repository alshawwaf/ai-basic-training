# Lesson 4.1 — Workshop Guide
## How LLMs Work

> **Read first:** [../notes.md](../notes.md) — theory and concepts
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_tokenisation.py`) — open only after finishing the exercise

---

## What This Workshop Covers

This workshop demystifies Large Language Models from the ground up — no API key required. You will manipulate tokens, vectors, and attention weights directly in NumPy and Python to build genuine intuition for what happens inside a model.

Work through them in order — each exercise builds on the previous.

---

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_tokenisation.md](01_guide_tokenisation.md) | [01_lab_tokenisation.md](01_lab_tokenisation.md) | Text → tokens → token IDs; vocabulary and OOV handling |
| 2 | [02_guide_embeddings.md](02_guide_embeddings.md) | [02_lab_embeddings.md](02_lab_embeddings.md) | Tokens → vectors; cosine similarity; semantic distance |
| 3 | [03_guide_attention.md](03_guide_attention.md) | [03_lab_attention.md](03_lab_attention.md) | Attention weights as "which words matter to which"; Q/K/V intuition |

**For each exercise:** read the guide first, then open the matching `_lab.md` file and follow the steps.

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson1_how_llms_work/workshop/01_solution_tokenisation.py
```

## Tips

- No GPU or internet connection required — all exercises run on NumPy alone
- The numbers you see are simplified toy examples, not real LLM weights
- The goal is intuition, not production-grade code

## After This Workshop

Move to [Lesson 4.2 — HuggingFace Pre-trained Models](../../lesson2_huggingface/workshop/00_overview.md)
