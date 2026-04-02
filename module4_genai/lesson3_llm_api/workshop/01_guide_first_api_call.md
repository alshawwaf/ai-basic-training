# Exercise 1 — Your First LLM API Call

> Read this guide fully before opening the exercise file.

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

## Expected Outputs at a Glance

**Task 1**
```
Provider: claude
Client loaded successfully.
```

**Task 2**
```
Q: What is lateral movement in 2 sentences?
A: Lateral movement refers to techniques attackers use to progressively move through a network
   after gaining initial access, expanding their foothold toward high-value targets...
```

**Task 3**
```
Log: Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)
Analysis: This log entry indicates a brute-force SSH attack...
```

---

## Now Open the Exercise File

[01_lab_first_api_call.md](01_lab_first_api_call.md)

---

## Next

[02_guide_system_prompts.md](02_guide_system_prompts.md) — design system prompts for a security analyst persona.
