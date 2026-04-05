# Exercise 3 — The Full RAG Pipeline

> Read this guide fully before opening the lab.

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

```
Full RAG Pipeline
──────────────────────────────────────────────────────────────
 User question: "How do I detect Mimikatz?"
        │
        ▼
   RETRIEVE       encode query ───► Vector Index (N chunks)
                  ◄──── top-k ─────
        │
        │ top 3 chunks
        ▼
   AUGMENT        stuff chunks into system prompt
                  → "CONTEXT:\n[chunk1]\n[chunk2]\n[chunk3]"
        │
        │ augmented prompt + user question
        ▼
   GENERATE       LLM reads context + answers
        │
        ▼
 Grounded answer (based on your KB, not hallucination)
```

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

```
The Augmented Prompt — what the LLM actually sees
──────────────────────────────────────────────────────

| Role      | Content                                             |
|-----------|-----------------------------------------------------|
| SYSTEM    | "You are a security analyst assistant.               |
|           |  Answer using ONLY the context below.                |
|           |                                                     |
|           |  CONTEXT:                                           |
|           |  [mimikatz]                                         |
|           |  Mimikatz uses sekurlsa::logonpasswords to...       |
|           |                                                     |
|           |  [lsass-detection]                                  |
|           |  Detection relies on monitoring LSASS memory        |
|           |  access via Sysmon Event ID 10..."                  |
| USER      | "How do I detect Mimikatz?"                         |
| ASSISTANT | (LLM generates answer from the context above)       |
```

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

## Now Open the Lab

[handson.md](handson.md)
## Workshop Complete

You have built a complete RAG pipeline. Compare your code against the matching solution files.

**You have now completed all 4 modules.** Review the [milestone project](../../project/) to build a full security analyst assistant.
