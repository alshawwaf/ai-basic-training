# Multi-Turn Conversation

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

**Conversation state — `messages` grows on every turn**

| Turn | Length of `messages` you send | Last entry added |
|---:|---:|---|
| 1 | 1 | `{user: "What is lateral movement?"}` |
| 2 | 3 | `{user: "How do I detect it?"}` (after appending the assistant reply from turn 1) |
| 3 | 5 | `{user: "Show me a Sigma rule"}` (after appending the assistant reply from turn 2) |
| N | `2N − 1` | the latest user question |

Every call ships the *entire* history because the API itself is stateless. The list keeps growing until you eventually hit the model's context window — at which point you must summarise older turns or drop them.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_conversation_growth.png" alt="Two side-by-side panels. Left bar chart titled 'Conversation length grows linearly (2N − 1 messages on turn N)' shows five cyan bars rising linearly: turn 1 with 1 message, turn 2 with 3, turn 3 with 5, turn 4 with 7, turn 5 with 9. Right panel titled 'Incident investigation — context builds' shows three rows. Each row has a grey 'turn' box on the left containing new evidence, an arrow, and a green box on the right showing what the model can now reason about. Turn 1: 'WORKSTATION-042 unusual outbound' → 'traffic anomaly, no attribution'. Turn 2: '+ powershell.exe spawned by winword.exe' → 'macro-doc execution → likely spear-phishing'. Turn 3: '+ connected to 185.219.47.33:443' → 'phishing → execution → C2, full kill chain'.">
  <div class="vis-caption">Left: how the messages list grows on every turn — by turn 5 you're shipping 9 messages every call. Right: how that growing list lets the model reason over an entire investigation. Each turn doesn't replace the picture, it extends it.</div>
</div>

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

**Incident investigation — context builds progressively**

| Turn | New evidence the user shares | What the model can now reason about |
|---:|---|---|
| 1 | `"unusual outbound traffic from WORKSTATION-042"` | a traffic anomaly with no attribution |
| 2 | + `"powershell.exe spawned by winword.exe"` | macro-enabled document execution → likely spear-phishing initial access |
| 3 | + `"connected to 185.219.47.33:443"` | full kill chain: phishing → execution → C2 communication |

Each turn doesn't *replace* the picture — it *extends* it. Because the previous turns are still in `messages`, the model's turn-3 answer is informed by everything from turns 1 and 2.

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
