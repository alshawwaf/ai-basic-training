# Lab — Exercise 4: Multi-Turn Conversation

> Follow each step in order. Copy the code into your script file as you go. By the final step you will have a complete, runnable Python script.

---

## Step 1: Create your script file

Create a new file called `exercise4_conversation.py` in this folder.

---

## Step 2: Add the imports, client setup, and system prompt

The analyst system prompt is designed for progressive incident analysis — each new message should build on the previous context rather than treating each turn as an isolated question.

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from llm_client import get_client

provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}\n")

ANALYST_SYSTEM = """You are a senior incident responder at a MSSP.
When given information about a potential security incident, analyse it progressively —
each message will reveal more detail. Build your understanding cumulatively.
Be concise: 3-5 sentences per response. Use bullet points for recommendations."""
```

---

## Step 3: Two-turn conversation demonstrating context retention

The second question uses "that technique" as a pronoun — it only makes sense in context. The model resolves the reference because the full conversation history is sent with every call.

Add this to your file:

```python
messages = []

turn1_q = "What MITRE technique describes credential dumping from LSASS?"
messages.append({"role": "user", "content": turn1_q})
reply1 = client.chat(system=ANALYST_SYSTEM, messages=messages, max_tokens=200)
messages.append({"role": "assistant", "content": reply1})

print(f"[Turn 1] User: {turn1_q}")
print(f"[Turn 1] Analyst: {reply1}\n")

turn2_q = "What are the top 2 indicators of compromise for that technique?"
messages.append({"role": "user", "content": turn2_q})
reply2 = client.chat(system=ANALYST_SYSTEM, messages=messages, max_tokens=200)
messages.append({"role": "assistant", "content": reply2})

print(f"[Turn 2] User: {turn2_q}")
print(f"[Turn 2] Analyst: {reply2}")
```

Run your file. The second response should reference T1003.001 (or the technique mentioned in turn 1) — demonstrating the model resolved "that technique" from context.

---

## Step 4: Three-turn incident investigation

Each turn reveals one more piece of evidence. A fresh `messages` list starts the incident investigation as a separate conversation so context from Step 3 does not bleed in.

Add this to your file:

```python
INCIDENT_TURNS = [
    "We've detected unusual outbound traffic from WORKSTATION-042 in the last 30 minutes. What are the most likely explanations?",
    "Update: logs show powershell.exe was spawned by winword.exe with an encoded base64 command. How does this change your assessment?",
    "Final update: the endpoint connected to 185.219.47.33 on port 443 within 2 seconds of the PowerShell execution. What is your threat assessment and recommended immediate actions?",
]

print("\n=== Incident Investigation ===\n")
messages = []
for i, user_turn in enumerate(INCIDENT_TURNS, 1):
    messages.append({"role": "user", "content": user_turn})
    reply = client.chat(system=ANALYST_SYSTEM, messages=messages, max_tokens=250)
    messages.append({"role": "assistant", "content": reply})
    print(f"[Turn {i}] User: {user_turn}")
    print(f"[Turn {i}] Analyst: {reply}\n")
```

Run your file. By turn 3 the model should identify a high-confidence C2 beacon and recommend endpoint isolation.

---

## Step 5: Print the full conversation history

This lets you review the complete incident thread and verify the model built understanding progressively across all three turns.

Add this to your file:

```python
print("=== Full Conversation History ===")
for msg in messages:
    role_label = "USER   " if msg["role"] == "user" else "ANALYST"
    print(f"[{role_label}] {msg['content'][:120]}...")

print(f"\nTotal turns: {len(INCIDENT_TURNS)} | Total messages: {len(messages)}")
```

Run your file. You should see:
```
=== Full Conversation History ===
[USER   ] We've detected unusual outbound traffic from WORKSTATION-042...
[ANALYST] This could indicate several threats, ranging from malware C2...
[USER   ] Update: logs show powershell.exe was spawned by winword.exe...
[ANALYST] This significantly changes the assessment. A Word document...
[USER   ] Final update: the endpoint connected to 185.219.47.33...
[ANALYST] This is a critical finding. The immediate C2 connection...

Total turns: 3 | Total messages: 6
```

---

## Step 6: Interactive mode (Bonus Task 4)

A simple REPL that maintains conversation history lets you have an open-ended investigation session. The loop exits when you type `quit` or `exit`.

Add this to your file:

```python
if __name__ == "__main__":
    repl_messages = []
    print("\nSecurity Analyst Assistant (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        repl_messages.append({"role": "user", "content": user_input})
        reply = client.chat(system=ANALYST_SYSTEM, messages=repl_messages, max_tokens=300)
        repl_messages.append({"role": "assistant", "content": reply})
        print(f"Analyst: {reply}")

print("\n--- Exercise 4 complete. Workshop finished! Open 04_solution_conversation.py to compare. ---")
print("--- Next: module4_genai/lesson4_rag/workshop/00_overview.md ---")
```

Run your file and type a few security questions to test the interactive loop. Type `quit` to exit.

---

## Your completed script

At this point your file contains all the working code. Compare it against the matching `_solution_` file (`04_solution_conversation.py`) if anything looks different.
