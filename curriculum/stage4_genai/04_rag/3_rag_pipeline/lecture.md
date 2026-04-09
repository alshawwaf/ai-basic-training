# The Full RAG Pipeline

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

**Full RAG pipeline — three stages**

| # | Stage | Input | Operation | Output |
|---:|---|---|---|---|
| 1 | **Retrieve** | user question (`"How do I detect Mimikatz?"`) | `model.encode(query)` → cosine similarity against the vector index | top-k chunk texts |
| 2 | **Augment** | retrieved chunks | inject them into the system prompt under a `CONTEXT:` heading | augmented system prompt |
| 3 | **Generate** | augmented prompt + user question | LLM reads the context and answers | grounded answer |

The LLM never *learned* the knowledge base — it reads it at inference time. Update the KB and the next call automatically uses the new content; no retraining required.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_rag_pipeline.png" alt="A horizontal three-stage pipeline diagram. Stage 1 cyan box 'RETRIEVE' shows a user query going into a vector index labelled 'top-k chunks'. Stage 2 orange box 'AUGMENT' shows the chunks being inserted into a system prompt under a 'CONTEXT:' heading. Stage 3 violet box 'GENERATE' shows the LLM reading the augmented prompt and producing a grounded answer. Arrows connect each stage. A dashed loop labelled 'KB updates' returns to the vector index, showing that updating the knowledge base does not require retraining the model.">
  <div class="vis-caption">The full RAG pipeline as a single diagram. Retrieval pulls the relevant chunks, augmentation injects them into the system prompt, and generation produces an answer that is grounded in those exact chunks. The model itself is never retrained — the knowledge lives entirely in the vector index.</div>
</div>

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

**The augmented prompt — what the LLM actually sees**

| Role | Content |
|---|---|
| **SYSTEM** | `"You are a security analyst assistant. Answer using ONLY the context below.`<br><br>`CONTEXT:`<br>`[mimikatz] Mimikatz uses sekurlsa::logonpasswords to extract plaintext credentials from LSASS memory...`<br><br>`[lsass-detection] Detection relies on monitoring LSASS memory access via Sysmon Event ID 10..."` |
| **USER** | `"How do I detect Mimikatz?"` |
| **ASSISTANT** | the model's answer, drawn from the chunks above |

The retrieved chunks live inside the system prompt — the user question is unchanged. Because the model is told to use *only* the context, it can answer questions about your private data accurately even though it was never trained on any of it.

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

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_rag_vs_llm.png" alt="A two-column comparison diagram. Left column 'Pure LLM' shows a single brain icon with a dashed circle around it labelled 'frozen training data'. A user question 'What does the latest Mimikatz module do?' goes in, and the answer below is shown in red as 'I last trained in 2024 — may hallucinate'. Right column 'RAG' shows the same brain icon plus a stack of document chunks feeding into it via a 'retrieve' arrow. The same user question is answered in green as 'Per the 2026-03 advisory in your KB, ...' with a citation marker. A row of icons below each column compares: knowledge source, hallucination risk, source citation, freshness, and cost.">
  <div class="vis-caption">Why teams reach for RAG. The pure LLM only knows what was in its training data — anything newer or anything private is invisible to it. RAG closes that gap by handing the model the relevant document chunks at inference time, so the answer is grounded in your real, current documentation.</div>
</div>

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
