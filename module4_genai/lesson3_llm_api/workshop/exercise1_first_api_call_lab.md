# Lab — Exercise 1: Your First LLM API Call

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise1_first_api_call.py` in this folder.

> Requires at least one API key set in your environment:
> - `set ANTHROPIC_API_KEY=...` (Claude — recommended)
> - `set OPENAI_API_KEY=...`
> - `set GOOGLE_API_KEY=...`

---

## Step 2: Add the imports

The `sys.path` fix allows Python to find `llm_client.py` which sits one level up in `module4_genai/`. `get_client()` auto-detects whichever API key you have set.

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from llm_client import get_client
```

---

## Step 3: Load the client

`get_client()` returns a `(provider, client)` tuple. If no API key is found, `client` is `None` and you should exit early rather than receive a cryptic error later.

Add this to your file:

```python
provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}")
print("Client loaded successfully.")
```

Run your file. You should see:
```
Provider: claude
Client loaded successfully.
```

---

## Step 4: Make your first API call

`client.chat()` takes three parameters: `system` (the model's persona), `messages` (the conversation so far), and `max_tokens` (the hard output limit). It returns a plain string.

Add this to your file:

```python
question = "What is lateral movement? Explain in 2 sentences."
response = client.chat(
    system="You are a concise cybersecurity instructor.",
    messages=[{"role": "user", "content": question}],
    max_tokens=150,
)

print(f"\nQ: {question}")
print(f"A: {response}")
```

Run your file. You should see something like:
```
Q: What is lateral movement? Explain in 2 sentences.
A: Lateral movement refers to techniques attackers use to progressively move
   through a network after gaining initial access...
```

---

## Step 5: Analyse a security log entry

A well-designed system prompt constrains the output format. The three-bullet format makes it easy to extract threat type, severity, and action programmatically.

Add this to your file:

```python
LOG_ENTRY = "Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)"

analysis = client.chat(
    system=(
        "You are a SOC analyst. When given a log entry, identify the threat type, "
        "severity (Critical/High/Medium/Low), and one recommended action. "
        "Be concise — 3 bullet points maximum."
    ),
    messages=[{"role": "user", "content": f"Analyse this log entry:\n{LOG_ENTRY}"}],
    max_tokens=200,
)

print(f"\nLog: {LOG_ENTRY}")
print(f"Analysis:\n{analysis}")
```

Run your file. You should see something like:
```
Log: Failed login for root from 45.33.32.156 (198 attempts in 60 seconds)
Analysis:
• Threat: SSH brute-force attack (MITRE T1110)
• Severity: High
• Action: Block IP 45.33.32.156 at firewall; review successful logins from this IP
```

---

## Step 6: Token limit experiment (Bonus Task 4)

Setting `max_tokens` too low cuts the response mid-sentence. This demonstrates that the limit is a hard ceiling, not a target length.

Add this to your file:

```python
for limit in [50, 400]:
    resp = client.chat(
        system="You are a SOC analyst. Give a detailed threat analysis.",
        messages=[{"role": "user", "content": f"Analyse this log entry:\n{LOG_ENTRY}"}],
        max_tokens=limit,
    )
    print(f"\n--- max_tokens={limit} ---")
    print(resp)

print("\n--- Exercise 1 complete. Move to exercise2_system_prompts.py ---")
```

Run your file. The 50-token response will be cut short; the 400-token response will be complete.

---

## Your completed script

At this point your file contains all the working code. Compare it against `reference_solution.py` if anything looks different.
