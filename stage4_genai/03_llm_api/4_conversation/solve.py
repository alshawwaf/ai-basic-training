# Exercise 4 — Multi-Turn Conversation
#
# Demonstrates how to maintain conversation history across API calls,
# building a progressive incident investigation with context retention.
# Works with Claude, OpenAI, Gemini, or Ollama -- whichever you have configured.
#
# Set ONE of:
#   set ANTHROPIC_API_KEY=...
#   set OPENAI_API_KEY=...
#   set GOOGLE_API_KEY=...
#   set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B

import sys
import os

# Import the shared LLM client (one directory up from )
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from llm_client import get_client

provider, client = get_client()
if client is None:
    print("No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY.")
    exit(1)

print(f"Provider: {provider}\n")

# System prompt designed for progressive incident analysis
ANALYST_SYSTEM = """You are a senior incident responder at a MSSP.
When given information about a potential security incident, analyse it progressively —
each message will reveal more detail. Build your understanding cumulatively.
Be concise: 3-5 sentences per response. Use bullet points for recommendations."""


# ============================================================
#   TASK 1: Two-turn conversation (context retention)
# ============================================================
print("=" * 60)
print("  TASK 1: Two-Turn Conversation")
print("=" * 60)

# The second question uses "that technique" — a pronoun that only
# makes sense if the model remembers the first answer.
messages = []

turn1_q = "What MITRE technique describes credential dumping from LSASS?"
messages.append({"role": "user", "content": turn1_q})
reply1 = client.chat(system=ANALYST_SYSTEM, messages=messages, max_tokens=200)
messages.append({"role": "assistant", "content": reply1})

print(f"\n[Turn 1] User: {turn1_q}")
print(f"[Turn 1] Analyst: {reply1}\n")

turn2_q = "What are the top 2 indicators of compromise for that technique?"
messages.append({"role": "user", "content": turn2_q})
reply2 = client.chat(system=ANALYST_SYSTEM, messages=messages, max_tokens=200)
messages.append({"role": "assistant", "content": reply2})

print(f"[Turn 2] User: {turn2_q}")
print(f"[Turn 2] Analyst: {reply2}")


# ============================================================
#   TASK 2: Three-turn incident investigation
# ============================================================
print("\n" + "=" * 60)
print("  TASK 2: Incident Investigation (3 turns)")
print("=" * 60)

# Each turn reveals one more piece of evidence.
# Fresh messages list so context from Task 1 does not bleed in.
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


# ============================================================
#   TASK 3: Print conversation history
# ============================================================
print("=" * 60)
print("  TASK 3: Full Conversation History")
print("=" * 60)

print("\n=== Full Conversation History ===")
for msg in messages:
    role_label = "USER   " if msg["role"] == "user" else "ANALYST"
    print(f"[{role_label}] {msg['content'][:120]}...")

print(f"\nTotal turns: {len(INCIDENT_TURNS)} | Total messages: {len(messages)}")


# ============================================================
#   TASK 4 (Bonus): Interactive mode
# ============================================================
print("\n" + "=" * 60)
print("  TASK 4 (Bonus): Interactive Mode")
print("=" * 60)

# Simple REPL that maintains conversation history.
# Type 'quit' or 'exit' to leave.
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

print("\n--- Exercise 4 complete. Workshop finished! ---")
print("--- Next: stage4_genai/04_rag/ ---")
