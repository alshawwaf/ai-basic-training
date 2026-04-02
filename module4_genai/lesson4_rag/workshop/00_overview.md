# Lesson 4.4 — Workshop Guide
## Retrieval-Augmented Generation (RAG)

> **Read first:** [../4_retrieval_augmented_generation.md](../4_retrieval_augmented_generation.md) — theory and concepts
> **Reference solutions:** Each exercise has a matching `_solution_` file (e.g. `01_solution_chunking.py`) — open only after finishing the exercise

---

## What This Workshop Covers

You will build a complete RAG pipeline from scratch — the same architecture used in production security analyst assistants. Starting from raw documents, you will chunk them, encode them, retrieve relevant chunks for a query, and combine retrieval with LLM generation to produce grounded, accurate answers.

Work through them in order — each exercise is a component of the final pipeline.

---

## Exercise Overview

| # | Guide | Lab | Topic |
|---|-------|---------------|-------|
| 1 | [01_guide_chunking.md](01_guide_chunking.md) | [01_lab_chunking.md](01_lab_chunking.md) | Document chunking strategies — fixed-size, overlap, by sentence |
| 2 | [02_guide_retrieval.md](02_guide_retrieval.md) | [02_lab_retrieval.md](02_lab_retrieval.md) | Encode chunks and retrieve top-k by cosine similarity |
| 3 | [03_guide_rag_pipeline.md](03_guide_rag_pipeline.md) | [03_lab_rag_pipeline.md](03_lab_rag_pipeline.md) | Full RAG: retrieve relevant chunks + augment prompt + generate |

## Setup

```bash
pip install sentence-transformers
# Plus one API key for Exercise 3:
set ANTHROPIC_API_KEY=your-key-here
```

## Running an Exercise

```bash
cd "C:/Users/admin/Desktop/AI Basic Training"
python module4_genai/lesson4_rag/workshop/01_solution_chunking.py
```

## Tips

- Exercises 1 and 2 require no API key — they use only local models
- Exercise 3 requires an API key for the generation step
- The same security knowledge base is used throughout all 3 exercises

## After This Workshop

**Congratulations — you have completed all 4 modules.**

Review the [milestone project](../../milestone/) to build a complete security analyst assistant.
