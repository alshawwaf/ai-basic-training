# Your First LLM API Call

> Read this guide fully before opening the lab.

---

## What You Will Learn

- The structure of an LLM API request: system, messages, max_tokens
- How to read and print the response
- How token limits affect response length
- The difference between a completion model and a chat model

---

## Concept: The Chat API Structure

Every modern LLM API uses the same basic structure:

```python
response = client.chat(
    system="You are a helpful assistant.",          # sets the model's role/persona
    messages=[
        {"role": "user", "content": "Hello!"}       # the conversation so far
    ],
    max_tokens=200,                                  # hard cap on response length
)
# response is a string: the model's reply
```

Three parameters control every call:
- **`system`**: Sets who the model is and how it should behave. Not visible to the user.
- **`messages`**: The conversation history — list of `{"role": ..., "content": ...}` dicts.
- **`max_tokens`**: Hard upper limit on output tokens. 100 tokens ≈ 75 words.

**Anatomy of a chat API call**

| Side | What it sends/receives | Example |
|---|---|---|
| **Your Python code** | request payload | `system="You are..."`, `messages=[{"role": "user", "content": "Hello!"}]`, `max_tokens=200` |
| → HTTPS → | | |
| **LLM provider** | runs the model on your payload | (server-side inference) |
| ← HTTPS ← | | |
| **Your Python code** | response | a string with the model's reply |

The whole interaction is one HTTP request and one HTTP response — there is no persistent connection.

<div class="lecture-visual">
  <img src="/static/lecture_assets/gn_api_anatomy.png" alt="A diagram showing two tall boxes connected by HTTPS arrows. Left cyan-bordered box 'YOUR PYTHON CODE' contains the chat call: 'client.chat(', 'system=\"You are...\",', 'messages=[ {role: \"user\", content: \"...\"} ],', 'max_tokens=200', ')'. At the bottom: '→ str (the reply)'. Right orange-bordered box 'LLM PROVIDER' lists: receives JSON payload, runs the model, generates tokens one at a time until end-of-sequence, bills you per token, returns JSON response, stateless — no memory of previous calls. Two grey arrows between the boxes labelled 'HTTPS request' (going right) and 'HTTPS response' (going left).">
  <div class="vis-caption">Anatomy of a single chat API call. Your code builds a request, sends it over HTTPS, the provider runs the model server-side, and a string comes back. The connection is stateless — there is no memory of previous calls on the server side.</div>
</div>

---

## Concept: Why Tokens Show Up on Your Bill

You already know **what** a token is from Lesson 4.1.1 — text gets split into subword pieces, each piece becomes an integer ID, and that is what the model actually consumes. This lesson is where those tokens stop being a learning curiosity and start being a *cost line*.

Two things you only see on the API side:

1. **Pricing is per token**, in both directions. You pay one rate for the tokens you send (input) and a different, usually higher, rate for the tokens the model writes back (output). A request that sends 2,000 tokens of context to get 200 tokens of answer back is billed as `2000 × input_price + 200 × output_price`.
2. **Context limits are measured in tokens**, not words or characters. GPT-4o, Claude 4.5, and Gemini 2.5 all advertise context windows of 128k to 1M+ tokens — the model literally cannot read more than that in one call. Anything beyond the limit must be summarised, retrieved, or dropped.

The `max_tokens` parameter you will set in the next section is the cap on the **output** side only — it has no effect on how many input tokens you send. If you forget about input tokens and stuff a 50,000-token document into every call, you can run a hundred-dollar bill in an afternoon. Watching token counts is the API equivalent of watching memory usage in a long-running process.

---

## Concept: The `llm_client.py` Abstraction

This course uses a helper that auto-detects which API key you have set:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()
# provider = "claude" / "openai" / "gemini"
# client.chat(system=..., messages=..., max_tokens=...) → str
```

The same code works with any provider.

---

## What Each Task Asks You to Do

### Task 1 — Load the client
Import and initialise `get_client()`. Print the provider name.

### Task 2 — First call: ask about a security concept
Send one message asking the model to explain a security concept in 2 sentences. Print the response.

### Task 3 — Analyse a log entry
Send a log entry to the model and ask it to identify the threat. Print the response.

### Task 4 — Token limit experiment (Bonus)
Make the same request with `max_tokens=50` and `max_tokens=400`. Observe how the response is truncated or complete.
