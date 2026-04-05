# Exercise 1 — Your First LLM API Call

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

```
API Call Flow
──────────────────────────────────────────────────────

 Your Python code              LLM Provider
 ─────────────────             ─────────────
 system: "You are..."
 messages: [                    LLM Model
   {user: "Hello!"}    HTTPS
 ]                   ────────►  processes
 max_tokens: 200                  │
                       ◄──────────
                    response (string)
```

---

## Concept: What Are Tokens?

LLMs don't process characters or words — they process **tokens**. A token is roughly:
- A common word: `"the"` → 1 token
- A longer word: `"cybersecurity"` → 2-3 tokens
- A number: `"12345"` → 1-2 tokens
- A code symbol: `"{}"` → 1 token

```
"Analyse this log entry for threats"
 → ["Analyse", " this", " log", " entry", " for", " threats"]
 → 6 tokens
```

Pricing and context limits are measured in tokens. GPT-4 context window = 128,000 tokens ≈ 100,000 words.

```
Tokenisation of a sentence
──────────────────────────────────────────────────────
 "Analyse this log entry for threats"
      │       │     │     │      │     │
      ▼       ▼     ▼     ▼      ▼     ▼
  ["Analyse"," this"," log"," entry"," for"," threats"]
      │       │     │     │      │     │
      ▼       ▼     ▼     ▼      ▼     ▼
     token   token token token  token  token
                   = 6 tokens total
```

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

---

## Now Open the Lab

[handson.md](handson.md)
## Next

[../2_system_prompts/lecture.md](../2_system_prompts/lecture.md) — design system prompts for a security analyst persona.
