# Exercise 4 — Multi-Turn Conversation

> Read this guide fully before opening the lab.

---

## What You Will Learn

- How multi-turn conversation works in the chat API
- How to maintain conversation history across calls
- How context accumulates and affects later responses
- How to build a simple interactive security assistant

---

## Concept: Stateless API, Stateful Conversation

The LLM API is **stateless** — it has no memory of previous calls. Every call is independent. To create a conversation, you must pass the full history every time:

**Turn 1:**
```python
messages = [{"role": "user", "content": "What is lateral movement?"}]
reply1 = client.chat(system=..., messages=messages, max_tokens=200)
messages.append({"role": "assistant", "content": reply1})
```

**Turn 2 — the model sees the entire history:**
```python
messages.append({"role": "user", "content": "How do I detect it?"})
reply2 = client.chat(system=..., messages=messages, max_tokens=200)
# reply2 is informed by the lateral movement context from turn 1
```

This is why the conversation list grows with each turn. You are sending the entire conversation to the model every time.

---

## Concept: Context Window Limits

Every model has a maximum context window (measured in tokens):
- Claude 3.5 Sonnet: 200,000 tokens
- GPT-4o: 128,000 tokens
- Gemini 1.5 Pro: 1,000,000 tokens

A conversation that grows beyond the context window will fail or get truncated. For long conversations, you need a **summarisation strategy**:
- Summarise earlier turns into a compact paragraph
- Drop old turns once the window is 80% full
- Use a vector store for long-term memory (the RAG approach)

---

## Concept: The Incident Investigation Flow

A typical security investigation conversation:

```
User:  "We've detected unusual outbound traffic. The source is WORKSTATION-042."
Model: [describes likely scenarios]

User:  "Logs show powershell.exe spawned by winword.exe with encoded commands."
Model: [narrows to macro-enabled document execution — likely spear-phishing initial access]

User:  "The endpoint also connected to 185.219.47.33 on port 443."
Model: [assesses C2 communication, recommends isolation and threat hunting]
```

Each turn adds context. The model's later responses are informed by the full incident picture.

---

## What Each Task Asks You to Do

### Task 1 — Two-turn conversation
Ask a security question, get a response, then ask a follow-up that refers to the first answer. Show that the model maintains context.

### Task 2 — Incident investigation chain
Simulate a 3-turn incident investigation. Add context progressively (each turn reveals more about the incident).

### Task 3 — Print conversation history
After the investigation, print the full conversation history in a readable format.

### Task 4 — Interactive mode (Bonus)
Build a simple `while True` input loop that lets you type questions. Maintain the conversation history. Exit on "quit".

---

## Now Open the Lab

[04_lab_conversation.md](04_lab_conversation.md)
## Workshop Complete

Compare your code against the matching `_solution_` files, then move to:

**[Lesson 4.4 — RAG](../../lesson4_rag/workshop/00_overview.md)**
