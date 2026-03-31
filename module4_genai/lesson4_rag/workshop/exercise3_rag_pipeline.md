# Exercise 3 — The Full RAG Pipeline

> **Exercise file:** [exercise3_rag_pipeline.py](exercise3_rag_pipeline.py)
> Read this guide fully before opening the exercise file.

---

## What You Will Learn

- How to combine retrieval and generation into a complete RAG pipeline
- How to inject retrieved context into the LLM prompt
- How RAG prevents hallucination by grounding answers in real documents
- The difference between RAG answers and pure LLM answers

---

## Concept: RAG Architecture

```
User query
    ↓
[Retrieval] → top-k relevant chunks from knowledge base
    ↓
[Augmentation] → inject chunks into system prompt as context
    ↓
[Generation] → LLM answers using the provided context
    ↓
Grounded answer
```

The key insight: the LLM is not memorising your security knowledge — it is reading it at inference time, injected as context. This means:
- The knowledge base can be updated without retraining
- The model cites specific information from the retrieved chunks
- Answers are more accurate and auditable

---

## Concept: The Augmented Prompt

```python
context = "\n\n".join([f"[{doc_id}]\n{chunk}" for score, doc_id, chunk in results])

system = f"""You are a security analyst assistant.
Answer the user's question using ONLY the information in the context below.
If the answer is not in the context, say "I don't have that information."

CONTEXT:
{context}
"""
```

The context section is the retrieved chunks. The LLM sees both the original question and the retrieved knowledge.

---

## Concept: RAG vs Pure LLM

| | Pure LLM | RAG |
|--|----------|-----|
| Knowledge source | Training data (fixed) | Your documents (updateable) |
| Hallucination risk | Higher | Lower |
| Cites sources | No | Can be instructed to |
| Domain specificity | General | As specific as your KB |
| Answers about recent events | No (cutoff date) | Yes (if KB is current) |
| Cost | Same per call | Slightly higher (retrieval step) |

RAG is the standard architecture for any production AI assistant over private or dynamic knowledge.

---

## What Each Task Asks You to Do

### Task 1 — Build the augmented prompt
For a query, retrieve top-3 chunks and format them as context. Print the full system prompt that would be sent to the LLM.

### Task 2 — Full RAG call
Send the augmented prompt + user query to the LLM. Print the response. Compare it to a no-context call (pure LLM).

### Task 3 — 3 question Q&A session
Ask 3 security questions through the full RAG pipeline. For each, show which chunks were retrieved and the final answer.

### Task 4 — Out-of-scope question (Bonus)
Ask a question whose answer is NOT in the knowledge base. Observe whether the model correctly says "I don't have that information" rather than hallucinating.

---

## Expected Outputs at a Glance

**Task 2**

Pure LLM (no context):
```
Mimikatz is a well-known post-exploitation tool... (general knowledge, may be less specific)
```

RAG answer (with context):
```
Based on the provided documentation, detecting Mimikatz involves monitoring LSASS memory
access using Sysmon Event ID 10. Specifically, you should alert on unexpected access to
lsass.exe from non-system processes such as procdump, taskmgr, or unsigned binaries...
```

The RAG answer is more specific because it is drawing from your knowledge base.

---

## Now Open the Exercise File

[exercise3_rag_pipeline.py](exercise3_rag_pipeline.py)

---

## Workshop Complete

You have built a complete RAG pipeline. Open [reference_solution.py](reference_solution.py) to compare.

**You have now completed all 4 modules.** Review the [milestone project](../../milestone/) to build a full security analyst assistant.
