# =============================================================================
# LESSON 4.3 | WORKSHOP | Exercise 4 of 4
# Multi-Turn Conversation
# =============================================================================
# WHAT YOU WILL LEARN
# -------------------
# - How to maintain conversation history across multiple API calls
# - How accumulated context shapes later responses
# - How to simulate a progressive incident investigation
#
# RUN THIS FILE
# -------------
#   python module4_genai/lesson3_llm_api/workshop/exercise4_conversation.py
# =============================================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
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

# =============================================================================
# BACKGROUND
# =============================================================================
# The LLM API is stateless — it has no memory between calls.
# To create a conversation, you send the FULL message history every time:
#
#   messages = []
#   messages.append({"role": "user",      "content": "question"})
#   reply = client.chat(system=..., messages=messages, ...)
#   messages.append({"role": "assistant", "content": reply})
#
#   messages.append({"role": "user",      "content": "follow-up"})
#   reply2 = client.chat(system=..., messages=messages, ...)   # sees full history
#   messages.append({"role": "assistant", "content": reply2})

# =============================================================================
# TASK 1 — Two-turn conversation demonstrating context retention
# =============================================================================
# Turn 1: Ask "What MITRE technique describes credential dumping from LSASS?"
# Turn 2: Ask "What are the top 2 indicators of compromise for that technique?"
#         (notice: "that technique" works because the model remembers turn 1)
#
# Print each turn's question and response:
#   [Turn 1] User: What MITRE technique...
#   [Turn 1] Analyst: T1003.001 — OS Credential Dumping: LSASS Memory...
#
#   [Turn 2] User: What are the top 2 indicators of compromise for that technique?
#   [Turn 2] Analyst: For T1003.001, the key IOCs are...

# >>> YOUR CODE HERE


# =============================================================================
# TASK 2 — Incident investigation chain (3 turns)
# =============================================================================
# Simulate a progressive incident where each turn adds more detail.
# Use a fresh `messages = []` list for this task.

INCIDENT_TURNS = [
    "We've detected unusual outbound traffic from WORKSTATION-042 in the last 30 minutes. What are the most likely explanations?",
    "Update: logs show powershell.exe was spawned by winword.exe with an encoded base64 command. How does this change your assessment?",
    "Final update: the endpoint connected to 185.219.47.33 on port 443 within 2 seconds of the PowerShell execution. What is your threat assessment and recommended immediate actions?",
]

# For each turn in INCIDENT_TURNS:
#   1. Append user message to messages
#   2. Call client.chat() with max_tokens=250
#   3. Append assistant reply to messages
#   4. Print: "[Turn N] User: ...\n[Turn N] Analyst: ..."

# >>> YOUR CODE HERE


# =============================================================================
# TASK 3 — Print conversation history
# =============================================================================
# After Task 2, print the full conversation history in a clean format.
# Show the role (USER / ANALYST), then the content.
# Also print: "Total turns: N | Total messages: M"
#
# EXPECTED OUTPUT:
#   === Full Conversation History ===
#   [USER]    We've detected unusual outbound traffic from WORKSTATION-042...
#   [ANALYST] This could indicate several threats, ranging from malware C2...
#   [USER]    Update: logs show powershell.exe was spawned by winword.exe...
#   [ANALYST] This significantly changes the assessment. A Word document...
#   [USER]    Final update: the endpoint connected to 185.219.47.33...
#   [ANALYST] This is a critical finding. The immediate C2 connection...
#
#   Total turns: 3 | Total messages: 6

# >>> YOUR CODE HERE


# =============================================================================
# TASK 4 — Interactive mode (BONUS)
# =============================================================================
# Build a simple REPL (Read-Eval-Print Loop) for an interactive session.
# Maintain conversation history across turns.
# Exit when the user types "quit" or "exit".
#
# if __name__ == "__main__":
#     messages = []
#     print("Security Analyst Assistant (type 'quit' to exit)")
#     while True:
#         user_input = input("\nYou: ").strip()
#         if user_input.lower() in ("quit", "exit"):
#             break
#         # append, call, print, append

# >>> YOUR CODE HERE


print("\n--- Exercise 4 complete. Workshop finished! Open reference_solution.py to compare. ---")
print("--- Next: module4_genai/lesson4_rag/workshop/1_lab_guide.md ---")
